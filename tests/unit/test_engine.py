from dataclasses import dataclass
from typing import cast

import pytest

from pseudonymize import Policy, Pseudonymizer
from pseudonymize.engine import Data
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
    assert engine.process(text).text == "Server <IP_ADDRESS_1>."


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
            # Sanitized: "Call <EMAIL_1> to reach Maria." (length of <EMAIL_1> is 9)
            text = block.text
            assert text == "Call <EMAIL_1> to reach Maria."
            # "Maria" starts at index 24, ends at 29 in the sanitized text
            return [
                Detection(
                    entity_type=EntityType.PERSON,
                    start=24,
                    end=29,
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
    assert result.text == "Call <EMAIL_1> to reach <PERSON_1>."
