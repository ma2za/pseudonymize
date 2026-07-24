import codecs
import csv
import io
import json
from dataclasses import replace
from pathlib import Path

import pytest

from pseudonymize import (
    ContentBlock,
    CSVCellLocation,
    Document,
    JSONPathLocation,
    TextOffsetLocation,
)
from pseudonymize.exceptions import (
    AdapterContractError,
    AdapterExecutionError,
    UnsupportedFormatError,
)
from pseudonymize.formats import BuiltinFileAdapter, FileFormat, select_file_format


@pytest.mark.parametrize(
    ("suffix", "expected"),
    [
        (".txt", FileFormat.TEXT),
        (".MD", FileFormat.MARKDOWN),
        (".markdown", FileFormat.MARKDOWN),
        (".LOG", FileFormat.LOG),
        (".json", FileFormat.JSON),
        (".JSONL", FileFormat.JSONL),
        (".ndjson", FileFormat.JSONL),
        (".csv", FileFormat.CSV),
    ],
)
def test_format_selection_is_explicit_or_suffix_based(suffix: str, expected: FileFormat) -> None:
    assert select_file_format(Path(f"input{suffix}"), None) is expected
    assert select_file_format(Path("input.unknown"), expected) is expected


def test_format_selection_rejects_unknown_values_without_guessing() -> None:
    with pytest.raises(UnsupportedFormatError, match="pass format explicitly"):
        select_file_format(Path("input.unknown"), None)
    with pytest.raises(UnsupportedFormatError, match="unsupported file format"):
        select_file_format(Path("input.txt"), "pdf")


@pytest.mark.parametrize("format", [FileFormat.TEXT, FileFormat.MARKDOWN, FileFormat.LOG])
def test_text_formats_preserve_unicode_newlines_and_bom(tmp_path: Path, format: FileFormat) -> None:
    source = tmp_path / "input"
    original = "\N{GREEK SMALL LETTER ALPHA}\r\nmaria@example.com\n"
    source.write_bytes(codecs.BOM_UTF8 + original.encode())
    adapter = BuiltinFileAdapter(format)

    document = adapter.extract(source)

    assert document.blocks[0].id == "body"
    assert document.blocks[0].location == TextOffsetLocation(0, len(original))
    assert document.metadata == {
        "format": format.value,
        "encoding": "utf-8",
        "bom": True,
    }
    assert adapter.render(document) == codecs.BOM_UTF8 + original.encode()


def test_render_requires_a_matching_extraction() -> None:
    adapter = BuiltinFileAdapter(FileFormat.TEXT)
    with pytest.raises(AdapterContractError, match="extract"):
        adapter.render(
            Document(
                "file",
                (ContentBlock("body", "text", TextOffsetLocation(0, 4)),),
            )
        )


def test_json_extracts_only_strings_with_stable_paths_and_semantic_rendering(
    tmp_path: Path,
) -> None:
    source = tmp_path / "input.json"
    source.write_text(
        '{"message":"maria@example.com","nested":[1,true,null,"192.0.2.10"]}',
        encoding="utf-8",
    )
    adapter = BuiltinFileAdapter(FileFormat.JSON)

    document = adapter.extract(source)

    assert tuple(block.id for block in document.blocks) == ("block-000000", "block-000001")
    assert tuple(block.location for block in document.blocks) == (
        JSONPathLocation(("message",)),
        JSONPathLocation(("nested", 3)),
    )
    transformed = replace(
        document,
        blocks=(
            replace(document.blocks[0], text="<EMAIL_1>"),
            replace(document.blocks[1], text="<IP_ADDRESS_1>"),
        ),
    )
    assert json.loads(adapter.render(transformed)) == {
        "message": "<EMAIL_1>",
        "nested": [1, True, None, "<IP_ADDRESS_1>"],
    }
    assert adapter.render(transformed).endswith(b"\n")


@pytest.mark.parametrize(
    "source_text",
    ['{"same":"one","same":"two"}', '{"value":NaN}', '{"value":Infinity}'],
)
def test_json_rejects_ambiguous_or_non_standard_values(tmp_path: Path, source_text: str) -> None:
    source = tmp_path / "input.json"
    source.write_text(source_text, encoding="utf-8")
    with pytest.raises(ValueError):
        BuiltinFileAdapter(FileFormat.JSON).extract(source)


def test_jsonl_locations_include_record_index_and_output_is_compact(
    tmp_path: Path,
) -> None:
    source = tmp_path / "input.jsonl"
    source.write_text(
        '{"value":"maria@example.com"}\n["192.0.2.10",2]\n',
        encoding="utf-8",
    )
    adapter = BuiltinFileAdapter(FileFormat.JSONL)

    document = adapter.extract(source)

    assert tuple(block.location for block in document.blocks) == (
        JSONPathLocation((0, "value")),
        JSONPathLocation((1, 0)),
    )
    rendered = adapter.render(document).decode()
    assert rendered == ('{"value":"maria@example.com"}\n["192.0.2.10",2]\n')


def test_jsonl_rejects_blank_records_with_line_number(tmp_path: Path) -> None:
    source = tmp_path / "input.jsonl"
    source.write_text('{"ok":"value"}\n\n{"ok":"value"}\n', encoding="utf-8")
    with pytest.raises(AdapterExecutionError, match="line 2"):
        BuiltinFileAdapter(FileFormat.JSONL).extract(source)


def test_csv_extracts_every_cell_and_normalizes_dialect(tmp_path: Path) -> None:
    source = tmp_path / "input.csv"
    source.write_text(
        'email,note\r\nmaria@example.com,"line one\nline two"\r\nempty,\r\n',
        encoding="utf-8",
        newline="",
    )
    adapter = BuiltinFileAdapter(FileFormat.CSV)

    document = adapter.extract(source)

    assert document.blocks[0].id == "row-000000-column-000000"
    assert document.blocks[0].location == CSVCellLocation(0, 0)
    assert document.blocks[-1].location == CSVCellLocation(2, 1)
    assert document.blocks[-1].text == ""
    rows = tuple(
        csv.reader(io.StringIO(adapter.render(document).decode(), newline=""), strict=True)
    )
    assert rows == (
        ["email", "note"],
        ["maria@example.com", "line one\nline two"],
        ["empty", ""],
    )


def test_csv_accepts_fields_larger_than_the_standard_library_default(
    tmp_path: Path,
) -> None:
    source = tmp_path / "large.csv"
    value = "x" * 200_000
    source.write_text(f"{value},maria@example.com\n", encoding="utf-8")

    document = BuiltinFileAdapter(FileFormat.CSV).extract(source)

    assert document.blocks[0].text == value


def test_adapter_state_and_document_representations_hide_source_values(
    tmp_path: Path,
) -> None:
    source = tmp_path / "input.json"
    source.write_text('{"value":"maria@example.com"}', encoding="utf-8")
    adapter = BuiltinFileAdapter(FileFormat.JSON)
    document = adapter.extract(source)

    assert "maria@example.com" not in repr(adapter)
    assert "maria@example.com" not in repr(document)

    with pytest.raises(AdapterContractError, match="structure changed"):
        adapter.render(replace(document, metadata={"format": "changed"}))
