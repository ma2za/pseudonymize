import inspect
from collections.abc import Callable
from dataclasses import fields

import pseudonymize as package
from pseudonymize import (
    ContentBlock,
    CSVCellLocation,
    Detection,
    DetectionReport,
    Document,
    EntityType,
    FileFormat,
    JSONPathLocation,
    NetworkPolicy,
    Policy,
    ProcessingResult,
    ProcessingStatistics,
    ProcessingWarning,
    Pseudonymizer,
    Replacement,
    Result,
    TextOffsetLocation,
    TransformationMode,
    pseudonymize,
    redact,
)

KEY = b"k" * 32


def _shape(value: Callable[..., object]) -> tuple[tuple[str, str], ...]:
    return tuple(
        (name, parameter.kind.name)
        for name, parameter in inspect.signature(value).parameters.items()
    )


def test_frozen_constructor_and_method_shapes() -> None:
    assert _shape(Pseudonymizer) == (
        ("mode", "KEYWORD_ONLY"),
        ("key", "KEYWORD_ONLY"),
        ("namespace", "KEYWORD_ONLY"),
        ("policy", "KEYWORD_ONLY"),
        ("detectors", "KEYWORD_ONLY"),
        ("backends", "KEYWORD_ONLY"),
        ("resolver", "KEYWORD_ONLY"),
        ("assigner", "KEYWORD_ONLY"),
        ("transformer", "KEYWORD_ONLY"),
        ("typed_redaction", "KEYWORD_ONLY"),
    )
    expected = {
        "detect": ("self", "text"),
        "process": ("self", "text", "include_mapping"),
        "process_with_report": ("self", "text"),
        "process_batch": ("self", "texts", "include_mapping"),
        "process_data": ("self", "data", "serializer"),
        "process_data_with_report": ("self", "data", "serializer"),
        "process_document": ("self", "document"),
        "inspect_document": ("self", "document"),
        "process_file": (
            "self",
            "source",
            "destination",
            "format",
            "encoding",
            "overwrite",
            "input_adapter",
            "output_adapter",
        ),
        "inspect_file": ("self", "source", "format", "encoding", "input_adapter"),
        "new_scope": ("self",),
    }
    assert {
        name: tuple(inspect.signature(getattr(Pseudonymizer, name)).parameters) for name in expected
    } == expected
    assert _shape(pseudonymize) == (
        ("text", "POSITIONAL_OR_KEYWORD"),
        ("mode", "KEYWORD_ONLY"),
        ("key", "KEYWORD_ONLY"),
        ("namespace", "KEYWORD_ONLY"),
        ("policy", "KEYWORD_ONLY"),
        ("backends", "KEYWORD_ONLY"),
    )
    assert _shape(redact) == (
        ("text", "POSITIONAL_OR_KEYWORD"),
        ("typed", "KEYWORD_ONLY"),
        ("policy", "KEYWORD_ONLY"),
        ("backends", "KEYWORD_ONLY"),
    )


def test_frozen_enums_and_data_models() -> None:
    assert [(item.name, item.value) for item in EntityType] == [
        ("PERSON", "PERSON"),
        ("ORGANIZATION", "ORGANIZATION"),
        ("LOCATION", "LOCATION"),
        ("EMAIL", "EMAIL"),
        ("PHONE", "PHONE"),
        ("IP_ADDRESS", "IP_ADDRESS"),
        ("IBAN", "IBAN"),
        ("PAYMENT_CARD", "PAYMENT_CARD"),
        ("URL_CREDENTIAL", "URL_CREDENTIAL"),
        ("SECRET", "SECRET"),
    ]
    assert [item.value for item in TransformationMode] == [
        "numbered",
        "generic",
        "deterministic",
        "redacted",
    ]
    assert [item.value for item in NetworkPolicy] == ["deny", "allow_configured", "allow_all"]
    assert [item.value for item in FileFormat] == [
        "text",
        "markdown",
        "log",
        "json",
        "jsonl",
        "csv",
    ]
    expected_fields = {
        Document: ("id", "blocks", "metadata"),
        ContentBlock: ("id", "text", "location", "metadata"),
        Detection: ("entity_type", "start", "end", "confidence", "detector", "backend"),
        Replacement: ("detection", "output_start", "output_end", "token"),
        Result: ("text", "replacements", "mapping"),
        ProcessingResult: ("output", "detections", "statistics", "warnings"),
        ProcessingStatistics: (
            "blocks_processed",
            "detections_found",
            "replacements_applied",
            "backend_invocations",
            "local_block_calls",
            "remote_block_calls",
        ),
        DetectionReport: (
            "entity_type",
            "block_id",
            "location",
            "start",
            "end",
            "confidence",
            "backend",
            "detector",
            "token",
        ),
        ProcessingWarning: ("code", "message", "block_id"),
        TextOffsetLocation: ("start", "end"),
        JSONPathLocation: ("path",),
        CSVCellLocation: ("row", "column"),
    }
    assert {
        model: tuple(field.name for field in fields(model)) for model in expected_fields
    } == expected_fields


def test_frozen_defaults_and_deterministic_vectors() -> None:
    assert Policy.default() == Policy()
    assert pseudonymize("maria@example.com") == "<EMAIL_1>"
    assert redact("maria@example.com") == "[REDACTED]"
    assert (
        pseudonymize("maria@example.com", mode="deterministic", key=KEY, namespace="compat")
        == "<EMAIL_6IHXRTFNJ2JY>"
    )
    assert (
        pseudonymize("192.0.2.10", mode="deterministic", key=KEY, namespace="compat")
        == "<IP_ADDRESS_DXX4QY54GKHT>"
    )
    result = Pseudonymizer().process("maria@example.com", include_mapping=True)
    assert result.restore("Reply to <EMAIL_1>") == "Reply to maria@example.com"
    assert set(package.__all__)
