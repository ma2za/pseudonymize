import base64
import io
import json
import os
import subprocess
import sys
from argparse import Namespace
from pathlib import Path

import pytest

from pseudonymize.cli import _read_key, main

KEY = base64.b64encode(b"k" * 32).decode("ascii")


def test_keygen_and_detectors(capsys: object) -> None:
    assert main(["keygen"]) == 0
    output = capsys.readouterr().out.strip()  # type: ignore[attr-defined]
    assert len(base64.b64decode(output)) == 32
    assert main(["detectors"]) == 0
    assert "email" in capsys.readouterr().out  # type: ignore[attr-defined]


def test_text_cli(monkeypatch: object, capsys: object) -> None:
    assert main(["text", "maria@example.com"]) == 0
    assert capsys.readouterr().out == "<EMAIL_1>\n"  # type: ignore[attr-defined]
    monkeypatch.setattr(sys, "stdin", io.StringIO("maria@example.com"))  # type: ignore[attr-defined]
    assert main(["text", "--redact", "-"]) == 0
    assert capsys.readouterr().out == "[REDACTED]\n"  # type: ignore[attr-defined]


def test_json_cli(monkeypatch: object, capsys: object) -> None:
    monkeypatch.setattr(  # type: ignore[attr-defined]
        sys, "stdin", io.StringIO(json.dumps({"content": "maria@example.com"}))
    )
    assert main(["json"]) == 0
    assert "maria@example.com" not in capsys.readouterr().out  # type: ignore[attr-defined]


def test_file_and_inspection_cli(tmp_path: Path, capsys: object) -> None:
    source = tmp_path / "payload.json"
    source.write_text('{"value":"maria@example.com"}', encoding="utf-8")

    assert main(["inspect-file", str(source)]) == 0
    inspected = json.loads(capsys.readouterr().out)  # type: ignore[attr-defined]
    assert inspected["detections"][0] == {
        "entity_type": "EMAIL",
        "block_id": "block-000000",
        "location": {"kind": "json_path", "path": ["value"]},
        "start": 0,
        "end": 17,
        "confidence": 0.99,
        "backend": "rules",
        "detector": "email",
    }
    assert inspected["statistics"]["replacements_applied"] == 0
    assert "maria@example.com" not in json.dumps(inspected)

    destination = tmp_path / "output.json"
    assert (
        main(
            [
                "file",
                str(source),
                "--output",
                str(destination),
                "--redact",
            ]
        )
        == 0
    )
    assert capsys.readouterr().out.strip() == str(destination)  # type: ignore[attr-defined]
    assert json.loads(destination.read_text(encoding="utf-8")) == {"value": "[REDACTED]"}


def test_file_cli_format_override_and_sanitized_failure(tmp_path: Path, capsys: object) -> None:
    source = tmp_path / "payload.data"
    source.write_text("maria@example.com", encoding="utf-8")
    assert main(["file", str(source), "--format", "text"]) == 0
    assert "maria@example.com" not in capsys.readouterr().out  # type: ignore[attr-defined]

    malformed = tmp_path / "malformed.json"
    malformed.write_text('{"value":"maria@example.com"', encoding="utf-8")
    with pytest.raises(SystemExit) as failure:
        main(["inspect-file", str(malformed)])
    assert failure.value.code == 2
    assert "maria@example.com" not in capsys.readouterr().err  # type: ignore[attr-defined]


def test_inspection_cli_serializes_text_and_csv_locations(tmp_path: Path, capsys: object) -> None:
    text_source = tmp_path / "payload.txt"
    text_source.write_text("maria@example.com", encoding="utf-8")
    assert main(["inspect-file", str(text_source)]) == 0
    text_report = json.loads(capsys.readouterr().out)  # type: ignore[attr-defined]
    assert text_report["detections"][0]["location"] == {
        "kind": "text_offset",
        "start": 0,
        "end": 17,
    }

    csv_source = tmp_path / "payload.csv"
    csv_source.write_text("maria@example.com\n", encoding="utf-8")
    assert main(["inspect-file", str(csv_source)]) == 0
    csv_report = json.loads(capsys.readouterr().out)  # type: ignore[attr-defined]
    assert csv_report["detections"][0]["location"] == {
        "kind": "csv_cell",
        "row": 0,
        "column": 0,
    }


def test_installed_console_entrypoint() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pseudonymize.cli", "keygen"],
        check=True,
        capture_output=True,
        text=True,
        env={**os.environ},
    )
    assert len(base64.b64decode(result.stdout)) == 32


def test_key_file_and_file_descriptor(tmp_path: Path) -> None:
    key_file = tmp_path / "key"
    key_file.write_text(KEY, encoding="ascii")
    key_file.chmod(0o600)
    assert _read_key(Namespace(key_env=None, key_file=key_file, key_fd=None)) == b"k" * 32
    with key_file.open(encoding="ascii") as stream:
        assert (
            _read_key(Namespace(key_env=None, key_file=None, key_fd=stream.fileno())) == b"k" * 32
        )


def test_cli_reports_missing_or_bad_key(monkeypatch: object) -> None:
    with pytest.raises(SystemExit) as missing:
        main(["text", "--mode", "deterministic", "text"])
    assert missing.value.code == 2
    monkeypatch.delenv("MISSING_KEY", raising=False)  # type: ignore[attr-defined]
    with pytest.raises(SystemExit) as error:
        main(["text", "--key-env", "MISSING_KEY", "text"])
    assert error.value.code == 2


def test_read_key_rejects_invalid_base64(monkeypatch: object) -> None:
    monkeypatch.setenv("PZ_BAD", "***")  # type: ignore[attr-defined]
    with pytest.raises(ValueError, match="base64"):
        _read_key(Namespace(key_env="PZ_BAD", key_file=None, key_fd=None))


def test_key_from_standard_input(monkeypatch: object, capsys: object) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO(KEY))  # type: ignore[attr-defined]
    assert main(["text", "--mode", "deterministic", "--key-stdin", "maria@example.com"]) == 0
    assert "maria@example.com" not in capsys.readouterr().out  # type: ignore[attr-defined]
    monkeypatch.setattr(sys, "stdin", io.StringIO(KEY))  # type: ignore[attr-defined]
    with pytest.raises(SystemExit):
        main(["text", "--mode", "deterministic", "--key-stdin", "-"])
