import base64
import io
import json
import os
import re
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
    monkeypatch.setenv("PZ_KEY", KEY)  # type: ignore[attr-defined]
    assert main(["text", "--key-env", "PZ_KEY", "maria@example.com"]) == 0
    assert re.fullmatch(r"<PZ1:EMAIL:[A-Z2-7]{16}>\n", capsys.readouterr().out)  # type: ignore[attr-defined]
    monkeypatch.setattr(sys, "stdin", io.StringIO("maria@example.com"))  # type: ignore[attr-defined]
    assert main(["text", "--key-env", "PZ_KEY", "--redact", "-"]) == 0
    assert capsys.readouterr().out == "<EMAIL>\n"  # type: ignore[attr-defined]


def test_json_cli(monkeypatch: object, capsys: object) -> None:
    monkeypatch.setenv("PZ_KEY", KEY)  # type: ignore[attr-defined]
    monkeypatch.setattr(  # type: ignore[attr-defined]
        sys, "stdin", io.StringIO(json.dumps({"content": "maria@example.com"}))
    )
    assert main(["json", "--key-env", "PZ_KEY"]) == 0
    assert "maria@example.com" not in capsys.readouterr().out  # type: ignore[attr-defined]


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


def test_cli_reports_bad_key(monkeypatch: object) -> None:
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
    assert main(["text", "--key-stdin", "maria@example.com"]) == 0
    assert "maria@example.com" not in capsys.readouterr().out  # type: ignore[attr-defined]
    monkeypatch.setattr(sys, "stdin", io.StringIO(KEY))  # type: ignore[attr-defined]
    with pytest.raises(SystemExit):
        main(["text", "--key-stdin", "-"])
