import base64
import csv
import io
import json
from pathlib import Path
from typing import Any

import pytest

from pseudonymize import CSVCellLocation, JSONPathLocation, Pseudonymizer, TextOffsetLocation
from pseudonymize.exceptions import AdapterExecutionError

CORPUS = json.loads(Path("tests/corpus/files.json").read_text(encoding="utf-8"))


def _location(location: object) -> dict[str, object]:
    if isinstance(location, TextOffsetLocation):
        return {"kind": "text_offset", "start": location.start, "end": location.end}
    if isinstance(location, JSONPathLocation):
        return {"kind": "json_path", "path": list(location.path)}
    if isinstance(location, CSVCellLocation):
        return {"kind": "csv_cell", "row": location.row, "column": location.column}
    raise TypeError("unsupported corpus location")


@pytest.mark.parametrize("case", CORPUS, ids=lambda case: str(case["name"]))
def test_cross_platform_file_corpus(tmp_path: Path, case: dict[str, Any]) -> None:
    source = tmp_path / f"input{case['suffix']}"
    original = base64.b64decode(case["input_base64"])
    source.write_bytes(original)
    output = tmp_path / f"input.safe{case['suffix']}"

    if "error" in case:
        with pytest.raises(AdapterExecutionError, match=str(case["error"])) as captured:
            Pseudonymizer().process_file(source)
        assert "maria@example.com" not in str(captured.value)
        assert source.read_bytes() == original
        assert not output.exists()
        return

    result = Pseudonymizer().process_file(source)
    rendered = result.output.read_bytes()

    assert source.read_bytes() == original
    assert b"maria@example.com" not in rendered
    assert b"192.0.2.10" not in rendered
    assert [_location(report.location) for report in result.detections] == case["locations"]
    if "expected_base64" in case:
        assert rendered == base64.b64decode(case["expected_base64"])
    elif "expected_json" in case:
        assert json.loads(rendered) == case["expected_json"]
    elif "expected_jsonl" in case:
        assert [json.loads(line) for line in rendered.splitlines()] == case["expected_jsonl"]
    else:
        assert (
            list(csv.reader(io.StringIO(rendered.decode(), newline=""), strict=True))
            == case["expected_csv"]
        )
