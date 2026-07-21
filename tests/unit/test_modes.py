import re
from dataclasses import dataclass

import pytest

from pseudonymize import (
    CompositeBackend,
    Detection,
    EntityType,
    Pseudonymizer,
    RulesBackend,
    TransformationMode,
    pseudonymize,
    redact,
)
from pseudonymize.exceptions import InvalidKeyError

KEY = b"k" * 32


@dataclass(frozen=True, slots=True)
class PersonBackend:
    name: str = "test_person"

    def detect(self, text: str) -> tuple[Detection, ...]:
        return tuple(
            Detection(EntityType.PERSON, match.start(), match.end(), 0.98, self.name)
            for match in re.finditer(r"Paolo\s+Mazza|Maria\s+Rossi", text)
        )


def test_numbered_mode_is_default() -> None:
    assert pseudonymize("Email paolo@example.com.") == "Email <EMAIL_1>."


def test_person_backend_and_exact_normalized_resolution() -> None:
    engine = Pseudonymizer(backends=[RulesBackend(), PersonBackend()])
    result = engine.process("Paolo Mazza met Paolo   Mazza and Maria Rossi.")
    assert result.text == "<PERSON_1> met <PERSON_1> and <PERSON_2>."


def test_generic_mode() -> None:
    result = pseudonymize(
        "paolo@example.com then maria@example.com", mode=TransformationMode.GENERIC
    )
    assert result == "<EMAIL> then <EMAIL>"


def test_deterministic_mode_is_stable_and_namespaced() -> None:
    first = pseudonymize(
        "paolo@example.com", mode=TransformationMode.DETERMINISTIC, key=KEY, namespace="a"
    )
    assert first == pseudonymize("paolo@example.com", mode="deterministic", key=KEY, namespace="a")
    assert first != pseudonymize("paolo@example.com", mode="deterministic", key=KEY, namespace="b")
    assert re.fullmatch(r"<EMAIL_[A-Z2-7]{12}>", first)


def test_deterministic_configuration_is_explicit() -> None:
    with pytest.raises(InvalidKeyError):
        Pseudonymizer(mode="deterministic")
    with pytest.raises(ValueError, match="only valid"):
        Pseudonymizer(key=KEY)
    with pytest.raises(ValueError, match="namespace"):
        Pseudonymizer(namespace="tenant")
    with pytest.raises(ValueError, match="typed_redaction"):
        Pseudonymizer(typed_redaction=True)


def test_redacted_mode() -> None:
    assert redact("paolo@example.com") == "[REDACTED]"
    assert redact("paolo@example.com", typed=True) == "[REDACTED_EMAIL]"


def test_numbering_is_per_type_and_per_call() -> None:
    engine = Pseudonymizer()
    text = "paolo@example.com 192.168.1.1 maria@example.com"
    assert engine.process(text).text == "<EMAIL_1> <IP_ADDRESS_1> <EMAIL_2>"
    assert engine.process("maria@example.com").text == "<EMAIL_1>"


def test_explicit_scope_preserves_aliases_across_calls() -> None:
    scope = Pseudonymizer().new_scope()
    assert scope.process("paolo@example.com").text == "<EMAIL_1>"
    assert scope.process("maria@example.com paolo@example.com").text == ("<EMAIL_2> <EMAIL_1>")


def test_batch_uses_one_scope() -> None:
    results = Pseudonymizer().process_batch(
        ["paolo@example.com", "maria@example.com paolo@example.com"]
    )
    assert tuple(result.text for result in results) == (
        "<EMAIL_1>",
        "<EMAIL_2> <EMAIL_1>",
    )


def test_existing_placeholders_are_ignored_and_processing_is_idempotent() -> None:
    engine = Pseudonymizer()
    once = engine.process("paolo@example.com").text
    assert engine.process(once).text == once
    assert engine.process(
        "<PERSON_1> <EMAIL> [REDACTED_EMAIL] <PZ1:EMAIL:ABCDEFGHIJKLMNOP>"
    ).text == ("<PERSON_1> <EMAIL> [REDACTED_EMAIL] <PZ1:EMAIL:ABCDEFGHIJKLMNOP>")


def test_explicit_empty_backends_disable_detection() -> None:
    assert Pseudonymizer(backends=[]).process("paolo@example.com").text == "paolo@example.com"


def test_mapping_is_opt_in_hidden_and_restorable() -> None:
    engine = Pseudonymizer(backends=[PersonBackend()])
    without_mapping = engine.process("Paolo Mazza")
    assert without_mapping.mapping is None
    with pytest.raises(ValueError, match="include_mapping"):
        without_mapping.restore("<PERSON_1>")

    result = engine.process("Paolo Mazza", include_mapping=True)
    assert result.mapping == {"<PERSON_1>": "Paolo Mazza"}
    assert "Paolo Mazza" not in repr(result)
    assert result.restore("<PERSON_1> should verify PERSON_1 and <PERSON_10>.") == (
        "Paolo Mazza should verify PERSON_1 and <PERSON_10>."
    )
    with pytest.raises(TypeError):
        result.mapping["<PERSON_2>"] = "Maria Rossi"  # type: ignore[index]


def test_deterministic_mapping_and_empty_mapping() -> None:
    result = Pseudonymizer(mode="deterministic", key=KEY).process(
        "paolo@example.com", include_mapping=True
    )
    assert result.mapping is not None
    assert result.restore(next(iter(result.mapping))) == "paolo@example.com"
    empty = Pseudonymizer().process("nothing sensitive", include_mapping=True)
    assert empty.mapping == {}
    assert empty.restore("unchanged") == "unchanged"


def test_mapping_requires_identity_preserving_mode() -> None:
    with pytest.raises(ValueError, match="numbered and deterministic"):
        Pseudonymizer(mode="generic").process("paolo@example.com", include_mapping=True)


def test_nested_payload_uses_one_alias_scope_without_mutation() -> None:
    payload = {
        "first": "paolo@example.com",
        "nested": ["maria@example.com", "paolo@example.com"],
        "temperature": 0.2,
    }
    output = Pseudonymizer().process_data(payload)
    assert output == {
        "first": "<EMAIL_1>",
        "nested": ["<EMAIL_2>", "<EMAIL_1>"],
        "temperature": 0.2,
    }
    assert payload["first"] == "paolo@example.com"


def test_structured_entity_wins_overlap() -> None:
    @dataclass(frozen=True, slots=True)
    class BroadPersonBackend:
        name: str = "broad_person"

        def detect(self, text: str) -> tuple[Detection, ...]:
            return (Detection(EntityType.PERSON, 0, len(text), 0.99, self.name),)

    result = Pseudonymizer(backends=[RulesBackend(), BroadPersonBackend()]).process(
        "paolo@example.com"
    )
    assert result.text == "<EMAIL_1>"


def test_composite_backend_combines_optional_and_rule_detection() -> None:
    backend = CompositeBackend([RulesBackend(), PersonBackend()])
    result = Pseudonymizer(backends=[backend]).process("Paolo Mazza paolo@example.com")
    assert result.text == "<PERSON_1> <EMAIL_1>"
