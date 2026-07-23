from dataclasses import FrozenInstanceError
from typing import cast

import pytest

from pseudonymize import (
    ContentBlock,
    Document,
    EntityType,
    JSONPathLocation,
    Policy,
    ProcessingResult,
    Pseudonymizer,
    TextOffsetLocation,
)
from pseudonymize.engine import Data


def test_text_report_has_relative_unicode_offsets_and_no_source_value() -> None:
    source = "π maria@example.com"
    result = Pseudonymizer().process_with_report(source)
    report = result.detections[0]

    assert result.output == "π <EMAIL_1>"
    assert (report.start, report.end) == (2, 19)
    assert report.entity_type is EntityType.EMAIL
    assert report.block_id == "text"
    assert report.location == TextOffsetLocation(0, len(source))
    assert report.backend == "rules"
    assert report.detector == "email"
    assert report.token == "<EMAIL_1>"
    assert result.statistics.blocks_processed == 1
    assert result.statistics.detections_found == 1
    assert result.statistics.replacements_applied == 1
    assert source not in repr(result)
    assert "maria@example.com" not in repr(result)
    with pytest.raises(FrozenInstanceError):
        result.output = "changed"  # type: ignore[misc]


def test_nested_data_reports_stable_ids_and_typed_json_paths() -> None:
    source = {
        "messages": [
            {"content": "maria@example.com"},
            {"content": "192.0.2.10."},
        ],
        "temperature": 0.2,
    }
    result = Pseudonymizer().process_data_with_report(source)
    output = cast(dict[str, Data], result.output)

    assert output["messages"] == [
        {"content": "<EMAIL_1>"},
        {"content": "<IP_ADDRESS_1>."},
    ]
    assert tuple(report.block_id for report in result.detections) == (
        "block-000000",
        "block-000001",
    )
    assert tuple(report.location for report in result.detections) == (
        JSONPathLocation(("messages", 0, "content")),
        JSONPathLocation(("messages", 1, "content")),
    )
    assert result.statistics.blocks_processed == 2
    assert result.statistics.backend_invocations == 2
    assert "maria@example.com" not in repr(result)
    assert "192.0.2.10" not in repr(result)


def test_document_processing_preserves_structure_identifiers_and_metadata() -> None:
    document = Document(
        "request",
        (
            ContentBlock(
                "subject",
                "Contact maria@example.com",
                TextOffsetLocation(0, 25),
                {"kind": "subject"},
            ),
            ContentBlock(
                "body",
                "No PII",
                TextOffsetLocation(26, 32),
                {"kind": "body"},
            ),
        ),
        {"format": "custom"},
    )
    result = Pseudonymizer().process_document(document)

    assert result.output.id == "request"
    assert tuple(block.id for block in result.output.blocks) == ("subject", "body")
    assert result.output.blocks[0].text == "Contact <EMAIL_1>"
    assert result.output.blocks[1].text == "No PII"
    assert result.output.blocks[0].location == TextOffsetLocation(0, 25)
    assert result.output.blocks[0].metadata == {"kind": "subject"}
    assert result.output.metadata == {"format": "custom"}
    assert document.blocks[0].text == "Contact maria@example.com"
    assert result.statistics.blocks_processed == 2
    assert result.statistics.backend_invocations == 2


def test_document_inspection_returns_no_transformed_output() -> None:
    document = Document(
        "request",
        (
            ContentBlock(
                "body",
                "maria@example.com",
                TextOffsetLocation(0, 17),
            ),
        ),
    )
    result: ProcessingResult[None] = Pseudonymizer().inspect_document(document)

    assert result.output is None
    assert result.detections[0].token is None
    assert result.statistics.detections_found == 1
    assert result.statistics.replacements_applied == 0
    assert "maria@example.com" not in repr(result)


def test_empty_document_and_excluded_document_blocks_are_counted() -> None:
    empty = Pseudonymizer().process_document(Document("empty", ()))
    assert empty.output.blocks == ()
    assert empty.statistics.blocks_processed == 0

    document = Document(
        "request",
        (
            ContentBlock(
                "model",
                "maria@example.com",
                JSONPathLocation(("model",)),
            ),
        ),
    )
    result = Pseudonymizer(policy=Policy.llm()).process_document(document)
    assert result.output.blocks[0].text == "maria@example.com"
    assert result.detections == ()
    assert result.statistics.blocks_processed == 1
    assert result.statistics.backend_invocations == 0
    inspected = Pseudonymizer(policy=Policy.llm()).inspect_document(document)
    assert inspected.detections == ()
    assert inspected.statistics.blocks_processed == 1
