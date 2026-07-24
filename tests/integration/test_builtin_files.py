import codecs
import csv
import io
import json
from pathlib import Path

import pytest

from pseudonymize import CSVCellLocation, JSONPathLocation, Pseudonymizer
from pseudonymize.exceptions import AdapterExecutionError, UnsupportedFormatError


@pytest.mark.parametrize(
    ("suffix", "content"),
    [
        (".txt", "maria@example.com"),
        (".MD", "maria@example.com"),
        (".markdown", "maria@example.com"),
        (".LOG", "maria@example.com"),
        (".json", '{"value":"maria@example.com"}'),
        (".JSONL", '{"value":"maria@example.com"}\n'),
        (".ndjson", '{"value":"maria@example.com"}\n'),
        (".csv", "maria@example.com\n"),
    ],
)
def test_builtin_suffixes_create_safe_copies(tmp_path: Path, suffix: str, content: str) -> None:
    source = tmp_path / f"input{suffix}"
    source.write_text(content, encoding="utf-8")

    result = Pseudonymizer().process_file(source)

    assert result.output == tmp_path / f"input.safe{suffix}"
    assert "maria@example.com" not in result.output.read_text(encoding="utf-8")
    assert source.read_text(encoding="utf-8") == content
    assert result.statistics.replacements_applied == 1


def test_explicit_format_overrides_unknown_suffix(tmp_path: Path) -> None:
    source = tmp_path / "payload.unknown"
    source.write_text('{"value":"maria@example.com"}', encoding="utf-8")

    result = Pseudonymizer().process_file(source, format="json")

    assert json.loads(result.output.read_text(encoding="utf-8")) == {"value": "<EMAIL_1>"}


def test_unknown_format_is_rejected_without_creating_output(tmp_path: Path) -> None:
    source = tmp_path / "payload.unknown"
    source.write_text("maria@example.com", encoding="utf-8")

    with pytest.raises(UnsupportedFormatError) as captured:
        Pseudonymizer().process_file(source)

    assert "maria@example.com" not in str(captured.value)
    assert not (tmp_path / "payload.safe.unknown").exists()


def test_json_semantic_round_trip_preserves_keys_and_non_strings(
    tmp_path: Path,
) -> None:
    source = tmp_path / "payload.json"
    payload = {
        "maria@example.com": "key is unchanged",
        "message": "maria@example.com",
        "values": [1, True, None, "192.0.2.10"],
    }
    source.write_text(json.dumps(payload), encoding="utf-8")

    result = Pseudonymizer().process_file(source)
    output = json.loads(result.output.read_text(encoding="utf-8"))

    assert output == {
        "maria@example.com": "key is unchanged",
        "message": "<EMAIL_1>",
        "values": [1, True, None, "<IP_ADDRESS_1>"],
    }
    assert tuple(report.location for report in result.detections) == (
        JSONPathLocation(("message",)),
        JSONPathLocation(("values", 3)),
    )


def test_jsonl_uses_one_alias_scope_and_record_locations(tmp_path: Path) -> None:
    source = tmp_path / "payload.jsonl"
    source.write_text(
        '{"message":"maria@example.com"}\n{"again":"maria@example.com","ip":"192.0.2.10"}\n',
        encoding="utf-8",
    )

    result = Pseudonymizer().process_file(source)
    records = [json.loads(line) for line in result.output.read_text(encoding="utf-8").splitlines()]

    assert records == [
        {"message": "<EMAIL_1>"},
        {"again": "<EMAIL_1>", "ip": "<IP_ADDRESS_1>"},
    ]
    assert tuple(report.location for report in result.detections) == (
        JSONPathLocation((0, "message")),
        JSONPathLocation((1, "again")),
        JSONPathLocation((1, "ip")),
    )


def test_csv_preserves_matrix_and_reports_cell_locations(tmp_path: Path) -> None:
    source = tmp_path / "payload.csv"
    source.write_text(
        "email,note,formula\n"
        'maria@example.com,"line one\nline two","=A2"\n'
        "192.0.2.10,,tail,extra\n",
        encoding="utf-8",
        newline="",
    )

    result = Pseudonymizer().process_file(source)
    rows = tuple(
        csv.reader(
            io.StringIO(result.output.read_text(encoding="utf-8"), newline=""),
            strict=True,
        )
    )

    assert rows == (
        ["email", "note", "formula"],
        ["<EMAIL_1>", "line one\nline two", "=A2"],
        ["<IP_ADDRESS_1>", "", "tail", "extra"],
    )
    assert tuple(report.location for report in result.detections) == (
        CSVCellLocation(1, 0),
        CSVCellLocation(2, 0),
    )


def test_encoding_is_strict_explicit_and_bom_preserving(tmp_path: Path) -> None:
    bom_source = tmp_path / "bom.txt"
    bom_source.write_bytes(codecs.BOM_UTF8 + b"maria@example.com\r\n")
    bom_result = Pseudonymizer().process_file(bom_source)
    assert bom_result.output.read_bytes().startswith(codecs.BOM_UTF8)
    assert bom_result.output.read_bytes().endswith(b"\r\n")

    encoded_source = tmp_path / "encoded.txt"
    encoded_source.write_bytes("café maria@example.com".encode("cp1252"))
    encoded_result = Pseudonymizer().process_file(encoded_source, encoding="cp1252")
    assert encoded_result.output.read_bytes().decode("cp1252") == "café <EMAIL_1>"


def test_invalid_encoding_and_malformed_inputs_are_sanitized(tmp_path: Path) -> None:
    source_value = "maria@example.com"
    invalid_bytes = tmp_path / "invalid.txt"
    invalid_bytes.write_bytes(source_value.encode() + b"\xff")
    with pytest.raises(AdapterExecutionError) as decoded:
        Pseudonymizer().inspect_file(invalid_bytes)
    assert source_value not in str(decoded.value)

    malformed = tmp_path / "malformed.json"
    malformed.write_text(f'{{"value":"{source_value}"', encoding="utf-8")
    with pytest.raises(AdapterExecutionError) as parsed:
        Pseudonymizer().inspect_file(malformed)
    assert source_value not in str(parsed.value)

    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text(
        f'{{"value":"{source_value}","value":"other"}}',
        encoding="utf-8",
    )
    with pytest.raises(AdapterExecutionError) as duplicated:
        Pseudonymizer().inspect_file(duplicate)
    assert source_value not in str(duplicated.value)


@pytest.mark.parametrize(
    ("suffix", "accepted"),
    [
        (".txt", True),
        (".md", True),
        (".log", True),
        (".json", False),
        (".jsonl", True),
        (".csv", True),
    ],
)
def test_empty_file_behavior(tmp_path: Path, suffix: str, accepted: bool) -> None:
    source = tmp_path / f"empty{suffix}"
    source.write_bytes(b"")
    if accepted:
        result = Pseudonymizer().process_file(source)
        assert result.output.read_bytes() == b""
        assert result.statistics.blocks_processed == (1 if suffix in {".txt", ".md", ".log"} else 0)
    else:
        with pytest.raises(AdapterExecutionError):
            Pseudonymizer().process_file(source)


def test_custom_adapters_cannot_mix_with_builtin_configuration(tmp_path: Path) -> None:
    source = tmp_path / "input.txt"
    source.write_text("maria@example.com", encoding="utf-8")

    class Input:
        def extract(self, source: Path) -> object:
            return object()

    class Output:
        def render(self, document: object) -> bytes:
            return b""

    with pytest.raises(ValueError, match="input and output"):
        Pseudonymizer().process_file(source, input_adapter=Input())  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="cannot be combined"):
        Pseudonymizer().process_file(
            source,
            format="text",
            input_adapter=Input(),  # type: ignore[arg-type]
            output_adapter=Output(),
        )
    with pytest.raises(ValueError, match="cannot be combined"):
        Pseudonymizer().inspect_file(
            source,
            encoding="utf-8",
            input_adapter=Input(),  # type: ignore[arg-type]
        )
