import sys

from pseudonymize import Pseudonymizer, pseudonymize

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
    _require(
        FORBIDDEN_OPTIONAL_IMPORTS.isdisjoint(sys.modules),
        "base import loaded an optional dependency",
    )


if __name__ == "__main__":
    main()
