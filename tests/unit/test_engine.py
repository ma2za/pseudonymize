import unicodedata
from dataclasses import dataclass
from typing import cast

import pytest

from pseudonymize import Policy, Pseudonymizer
from pseudonymize.engine import Data, _strip_format_characters
from pseudonymize.exceptions import UnsupportedDataError


def test_process_replaces_right_to_left_and_reports_output_offsets() -> None:
    result = Pseudonymizer().process("maria@example.com then 192.168.1.1")
    assert "maria@example.com" not in result.text
    assert "192.168.1.1" not in result.text
    assert tuple(
        result.text[item.output_start : item.output_end] for item in result.replacements
    ) == tuple(item.token for item in result.replacements)
    assert all(not hasattr(item.detection, "value") for item in result.replacements)


def test_process_is_idempotent() -> None:
    engine = Pseudonymizer()
    once = engine.process("maria@example.com").text
    assert engine.process(once).text == once
    assert tuple(result.text for result in engine.process_batch(["maria@example.com", once])) == (
        once,
        once,
    )


def test_sentence_terminated_ip_wins_over_phone_candidate() -> None:
    engine = Pseudonymizer()
    text = "Server 192.0.2.10."
    detections = engine.detect(text)
    assert [item.entity_type.value for item in detections] == ["IP_ADDRESS"]
    assert engine.process(text).text == "Server <IP_1>."


def test_nested_data_preserves_structure_and_primitives() -> None:
    engine = Pseudonymizer(policy=Policy.llm())
    payload = {
        "messages": [{"role": "user", "content": "maria@example.com"}],
        "temperature": 0.2,
        "flags": (True, None),
    }
    output = engine.process_data(payload)
    assert isinstance(output, dict)
    messages = cast(list[Data], output["messages"])
    first_message = cast(dict[str, Data], messages[0])
    assert first_message["content"] != "maria@example.com"
    assert output["temperature"] == 0.2
    assert output["flags"] == (True, None)


def test_nested_path_policy() -> None:
    policy = Policy.llm(include_paths=["messages.*.content"])
    output = Pseudonymizer(policy=policy).process_data(
        {"messages": [{"content": "maria@example.com"}], "metadata": "maria@example.com"}
    )
    assert isinstance(output, dict)
    assert output["metadata"] == "maria@example.com"
    assert output["messages"] != [{"content": "maria@example.com"}]


@dataclass
class Custom:
    value: str


def test_custom_serializer_and_unsupported_values() -> None:
    engine = Pseudonymizer()
    with pytest.raises(UnsupportedDataError):
        engine.process_data(Custom("maria@example.com"))
    output = engine.process_data(Custom("maria@example.com"), serializer=lambda item: item.__dict__)
    assert isinstance(output, dict)
    assert output["value"] != "maria@example.com"
    with pytest.raises(UnsupportedDataError, match="keys"):
        engine.process_data({1: "maria@example.com"})


def test_engine_remote_offset_mapping() -> None:
    from pseudonymize import BackendCapabilities, NetworkPolicy
    from pseudonymize.backends.rules import RulesBackend
    from pseudonymize.detectors import DEFAULT_DETECTORS
    from pseudonymize.document import ContentBlock
    from pseudonymize.result import Detection, EntityType

    # We define a custom remote backend to intercept sanitized text
    @dataclass
    class MockRemoteBackend:
        name: str = "mock_remote"

        @property
        def capabilities(self) -> BackendCapabilities:
            return BackendCapabilities(frozenset({EntityType.PERSON}), remote=True)

        @property
        def allow_remote_processing(self) -> bool:
            return True

        def detect(self, block: ContentBlock, policy: Policy) -> list[Detection]:
            # The input block.text here must be the local-sanitized text!
            # Original: "Call maria@example.com to reach Maria."
            # Sanitized: "Call <EML_1> to reach Maria." (length of <EML_1> is 7)
            text = block.text
            assert text == "Call <EML_1> to reach Maria."
            # "Maria" starts at index 24, ends at 29 in the sanitized text
            return [
                Detection(
                    entity_type=EntityType.PERSON,
                    start=22,
                    end=27,
                    confidence=1.0,
                    detector="mock_remote",
                )
            ]

    policy = Policy(
        network_policy=NetworkPolicy.ALLOW_CONFIGURED,
        allowed_remote_backends=frozenset({"mock_remote"}),
    )

    # Instantiate engine with default local rules AND our mock remote backend
    engine = Pseudonymizer(
        policy=policy, backends=(RulesBackend(DEFAULT_DETECTORS), MockRemoteBackend())
    )

    result = engine.process("Call maria@example.com to reach Maria.")
    # Standard translation should redact BOTH the email and Maria
    assert "maria@example.com" not in result.text
    assert "Maria" not in result.text
    assert result.text == "Call <EML_1> to reach <PER_1>."


@pytest.mark.parametrize(
    "text",
    [
        "maria@example.com",
        "mar​ia@example.com",
        "‮maria@example.com‬",
        "Écrire à maria@example.com",
        "⁦mar‌ia@example.com⁩ puis 192.168.1.1",
    ],
)
def test_format_characters_never_shift_detection_offsets(text: str) -> None:
    """The ASCII fast path and the stripping path must agree on source offsets."""
    detections = Pseudonymizer().detect(text)
    assert detections
    for detection in detections:
        matched = text[detection.start : detection.end]
        assert "".join(char for char in matched if unicodedata.category(char) != "Cf").endswith(
            ("example.com", "192.168.1.1")
        )


def test_format_character_stripping_skips_rebuild_when_nothing_is_removed() -> None:
    assert _strip_format_characters("plain ascii") == ("plain ascii", None)
    assert _strip_format_characters("café sans contrôles") == ("café sans contrôles", None)
    stripped, mapping = _strip_format_characters("a​b")
    assert stripped == "ab"
    assert mapping == [0, 2, 3]


def test_mcp_schema_preserving_redaction() -> None:
    # A full MCP / JSON-RPC payload including a tool definition with schemas
    # and tool arguments with PII.
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "send_email",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The user email address, e.g. john.smith@example.com",
                    }
                },
                "required": ["email"],
            },
            "arguments": {
                "email": "john.smith@example.com",
                "text": "My email is john.smith@example.com and phone is +39 333 123 4567.",
            },
        },
        "id": 1,
    }

    engine = Pseudonymizer()
    sanitized = engine.process_data(payload)
    assert isinstance(sanitized, dict)

    # 1. Structural schema components and metadata MUST be preserved untouched!
    # (i.e. 'john.smith@example.com' inside description must NOT be redacted
    # because it's part of the Schema description)
    assert sanitized["jsonrpc"] == "2.0"
    assert sanitized["method"] == "tools/call"

    params = sanitized["params"]
    assert isinstance(params, dict)
    input_schema = params["inputSchema"]
    assert isinstance(input_schema, dict)
    properties = input_schema["properties"]
    assert isinstance(properties, dict)
    email_prop = properties["email"]
    assert isinstance(email_prop, dict)

    expected_desc = "The user email address, e.g. john.smith@example.com"
    assert email_prop["description"] == expected_desc
    assert input_schema["required"] == ["email"]

    # 2. Runtime execution arguments containing PII MUST be redacted/pseudonymized!
    arguments = params["arguments"]
    assert isinstance(arguments, dict)
    assert arguments["email"] != "john.smith@example.com"
    text_arg = arguments["text"]
    assert isinstance(text_arg, str)
    assert "john.smith@example.com" not in text_arg
    assert "+39 333 123 4567" not in text_arg


def test_pseudonymizer_ablation_flags() -> None:
    from pseudonymize.engine import ProcessingScope

    engine = Pseudonymizer()
    engine._enable_coreference = False
    engine._enable_adjacent_merge = False
    assert not engine._enable_coreference
    assert not engine._enable_adjacent_merge
    res = engine.process("Contact alice@example.com.")
    assert "alice@example.com" not in res.text

    scope = ProcessingScope(engine)
    assert scope._coreferences is None


def test_process_batch_features_and_edge_cases() -> None:
    from pseudonymize import TransformationMode

    engine = Pseudonymizer()
    assert engine.process_batch(()) == ()

    # Batch with mapping
    texts = ["Contact alice@example.com", "No identifiers here", "Phone is +1 415 555 2671"]
    results = engine.process_batch(texts, include_mapping=True)
    assert len(results) == 3
    assert "<EML_1>" in results[0].text
    assert results[0].mapping is not None
    assert results[0].restore(results[0].text) == texts[0]
    assert results[1].text == texts[1]
    assert "<PHN_1>" in results[2].text
    assert results[2].mapping is not None

    # Invalid mapping mode
    redact_engine = Pseudonymizer(mode=TransformationMode.REDACTED)
    with pytest.raises(ValueError, match="mappings are available only"):
        redact_engine.process_batch(texts, include_mapping=True)


def test_engine_remote_process_document_and_batch() -> None:
    from dataclasses import dataclass

    from pseudonymize import Detection, EntityType, NetworkPolicy, TextOffsetLocation
    from pseudonymize.backends import BackendCapabilities, RulesBackend
    from pseudonymize.detectors import DEFAULT_DETECTORS
    from pseudonymize.document import ContentBlock, Document

    @dataclass
    class SimpleMockRemoteBackend:
        name: str = "mock_remote"

        @property
        def capabilities(self) -> BackendCapabilities:
            return BackendCapabilities(frozenset({EntityType.PERSON}), remote=True)

        @property
        def allow_remote_processing(self) -> bool:
            return True

        def detect(self, block: ContentBlock, policy: Policy) -> list[Detection]:
            idx = block.text.find("Maria")
            if idx >= 0:
                return [
                    Detection(
                        entity_type=EntityType.PERSON,
                        start=idx,
                        end=idx + 5,
                        confidence=1.0,
                        detector="mock_remote",
                    )
                ]
            return []

    policy = Policy(
        network_policy=NetworkPolicy.ALLOW_CONFIGURED,
        allowed_remote_backends=frozenset({"mock_remote"}),
    )
    engine = Pseudonymizer(
        policy=policy, backends=(RulesBackend(DEFAULT_DETECTORS), SimpleMockRemoteBackend())
    )

    # 1. Test process_batch with remote backend
    texts = ["Contact maria@example.com for Maria.", "No PII here."]
    batch_res = engine.process_batch(texts)
    assert len(batch_res) == 2
    assert "<EML_1>" in batch_res[0].text
    assert "<PER_1>" in batch_res[0].text
    assert "Maria" not in batch_res[0].text

    # 2. Test process_document with remote backend
    doc = Document(
        "doc1",
        (
            ContentBlock("b1", "Contact maria@example.com for Maria.", TextOffsetLocation(0, 35)),
            ContentBlock("b2", "Plain text block", TextOffsetLocation(0, 16)),
        ),
    )
    doc_res = engine.process_document(doc)
    assert doc_res.output.blocks[0].text == "Contact <EML_1> for <PER_1>."
    assert doc_res.output.blocks[1].text == "Plain text block"
    assert doc_res.statistics.remote_block_calls == 2
