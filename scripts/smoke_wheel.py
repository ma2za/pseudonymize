import json
import subprocess
import sys
import tempfile
from pathlib import Path

from pseudonymize import JSONPathLocation, Pseudonymizer, pseudonymize

FORBIDDEN_OPTIONAL_IMPORTS = {
    "docling",
    "docx",
    "httpx",
    "onnxruntime",
    "openpyxl",
    "pypdf",
    "pytesseract",
    "requests",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    _require(
        pseudonymize("maria@example.com") == "<EMAIL_1>",
        "email smoke test failed",
    )
    _require(
        pseudonymize("Server 192.0.2.10.") == "Server <IP_ADDRESS_1>.",
        "IP punctuation smoke test failed",
    )
    result = Pseudonymizer().process_with_report("maria@example.com")
    _require(result.output == "<EMAIL_1>", "detailed output smoke test failed")
    _require(result.detections[0].backend == "rules", "backend provenance smoke test failed")
    _require("maria@example.com" not in repr(result), "report representation leaked input")
    with tempfile.TemporaryDirectory() as directory:
        source = Path(directory) / "payload.json"
        source.write_text('{"value":"maria@example.com"}', encoding="utf-8")
        file_result = Pseudonymizer().process_file(source)
        _require(
            file_result.output.read_text(encoding="utf-8") == '{\n  "value": "<EMAIL_1>"\n}\n',
            "built-in JSON file smoke test failed",
        )
        inspected = Pseudonymizer().inspect_file(source)
        _require(inspected.output is None, "inspection wrote output")
        _require(
            inspected.detections[0].location == JSONPathLocation(("value",)),
            "installed-wheel JSON location smoke test failed",
        )
        _require(
            "maria@example.com" not in repr(inspected),
            "installed-wheel inspection leaked input",
        )
        cli_source = Path(directory) / "cli.json"
        cli_source.write_text('{"value":"maria@example.com"}', encoding="utf-8")
        processed_cli = subprocess.run(  # noqa: S603
            [sys.executable, "-m", "pseudonymize.cli", "file", str(cli_source)],
            check=True,
            capture_output=True,
            text=True,
        )
        _require(
            "maria@example.com" not in processed_cli.stdout,
            "installed-wheel file CLI leaked input",
        )
        inspected_cli = subprocess.run(  # noqa: S603
            [sys.executable, "-m", "pseudonymize.cli", "inspect-file", str(cli_source)],
            check=True,
            capture_output=True,
            text=True,
        )
        inspection = json.loads(inspected_cli.stdout)
        _require(
            inspection["detections"][0]["location"] == {"kind": "json_path", "path": ["value"]},
            "installed-wheel inspection CLI smoke test failed",
        )
        _require(
            "maria@example.com" not in inspected_cli.stdout,
            "installed-wheel inspection CLI leaked input",
        )
    _require(
        FORBIDDEN_OPTIONAL_IMPORTS.isdisjoint(sys.modules),
        "base import loaded an optional dependency",
    )
    subprocess.run(
        [sys.executable, "examples/llm_gateway.py"],
        check=True,
        capture_output=True,
        text=True,
    )


if __name__ == "__main__":
    main()
