import argparse
import base64
import binascii
import json
import os
import stat
import sys
from collections.abc import Sequence
from pathlib import Path

from pseudonymize.api import generate_key
from pseudonymize.detectors import DEFAULT_DETECTORS
from pseudonymize.document import CSVCellLocation, JSONPathLocation, TextOffsetLocation
from pseudonymize.engine import Data, Pseudonymizer
from pseudonymize.exceptions import PseudonymizeError
from pseudonymize.formats import FileFormat
from pseudonymize.policy import Policy
from pseudonymize.processing import DetectionReport, ProcessingResult
from pseudonymize.transforms import TransformationMode


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pseudonymize")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("keygen", help="print a new base64-encoded key")
    subparsers.add_parser("detectors", help="list bundled detectors")

    text_parser = subparsers.add_parser("text", help="process text")
    text_parser.add_argument("text", help="text to process, or - for standard input")
    _add_key_options(text_parser, allow_stdin=True)
    text_parser.add_argument("--namespace", default="default")
    _add_mode_options(text_parser)

    json_parser = subparsers.add_parser("json", help="process JSON from standard input")
    _add_key_options(json_parser)
    json_parser.add_argument("--namespace", default="default")
    _add_mode_options(json_parser)

    file_parser = subparsers.add_parser("file", help="process a supported file")
    file_parser.add_argument("source", type=Path)
    file_parser.add_argument("--output", type=Path)
    file_parser.add_argument("--format", choices=tuple(FileFormat))
    file_parser.add_argument("--encoding")
    file_parser.add_argument("--overwrite", action="store_true")
    _add_key_options(file_parser, allow_stdin=True)
    file_parser.add_argument("--namespace", default="default")
    _add_mode_options(file_parser)

    inspect_parser = subparsers.add_parser(
        "inspect-file", help="inspect a supported file without writing output"
    )
    inspect_parser.add_argument("source", type=Path)
    inspect_parser.add_argument("--format", choices=tuple(FileFormat))
    inspect_parser.add_argument("--encoding")
    return parser


def _add_key_options(parser: argparse.ArgumentParser, *, allow_stdin: bool = False) -> None:
    sources = parser.add_mutually_exclusive_group()
    sources.add_argument("--key-env", metavar="NAME")
    sources.add_argument("--key-file", type=Path)
    sources.add_argument("--key-fd", type=int)
    if allow_stdin:
        sources.add_argument("--key-stdin", action="store_true")


def _add_mode_options(parser: argparse.ArgumentParser) -> None:
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--mode", choices=tuple(TransformationMode), default=TransformationMode.NUMBERED
    )
    modes.add_argument(
        "--redact", action="store_const", const=TransformationMode.REDACTED, dest="mode"
    )
    parser.add_argument("--typed-redaction", action="store_true")


def _has_key_source(arguments: argparse.Namespace) -> bool:
    return any(
        (
            getattr(arguments, "key_env", None),
            getattr(arguments, "key_file", None),
            getattr(arguments, "key_fd", None) is not None,
            getattr(arguments, "key_stdin", False),
        )
    )


def _read_key(arguments: argparse.Namespace) -> bytes:
    encoded: str
    if getattr(arguments, "key_env", None):
        encoded = os.environ.get(arguments.key_env, "")
        if not encoded:
            raise ValueError(f"environment variable {arguments.key_env!r} is empty or unset")
    elif getattr(arguments, "key_file", None):
        path: Path = arguments.key_file
        if os.name != "nt" and stat.S_IMODE(path.stat().st_mode) & 0o077:
            raise ValueError("key file must not be accessible by group or other users")
        encoded = path.read_text(encoding="ascii").strip()
    elif getattr(arguments, "key_fd", None) is not None:
        with os.fdopen(os.dup(arguments.key_fd), encoding="ascii") as stream:
            encoded = stream.read().strip()
    else:
        if getattr(arguments, "text", None) == "-":
            raise ValueError("standard input cannot provide both the key and text")
        encoded = sys.stdin.read().strip()
    try:
        return base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as error:
        raise ValueError("key must be valid base64") from error


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    arguments = parser.parse_args(argv)
    if arguments.command == "keygen":
        print(base64.b64encode(generate_key()).decode("ascii"))
        return 0
    if arguments.command == "detectors":
        print("\n".join(detector.name for detector in DEFAULT_DETECTORS))
        return 0
    try:
        if arguments.command == "inspect-file":
            inspected = Pseudonymizer().inspect_file(
                arguments.source,
                format=arguments.format,
                encoding=arguments.encoding,
            )
            json.dump(_inspection_payload(inspected), sys.stdout, ensure_ascii=False)
            sys.stdout.write("\n")
            return 0
        key = _read_key(arguments) if _has_key_source(arguments) else None
        engine = Pseudonymizer(
            mode=arguments.mode,
            key=key,
            namespace=arguments.namespace,
            policy=Policy.llm() if arguments.command == "json" else Policy.default(),
            typed_redaction=arguments.typed_redaction,
        )
        if arguments.command == "text":
            source = sys.stdin.read() if arguments.text == "-" else arguments.text
            print(engine.process(source).text)
            return 0
        if arguments.command == "file":
            result = engine.process_file(
                arguments.source,
                arguments.output,
                format=arguments.format,
                encoding=arguments.encoding,
                overwrite=arguments.overwrite,
            )
            print(result.output)
            return 0
        payload = json.load(sys.stdin)
        output: Data = engine.process_data(payload)
        json.dump(output, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    except (LookupError, OSError, ValueError, json.JSONDecodeError, PseudonymizeError) as error:
        parser.exit(2, f"pseudonymize: error: {error}\n")


def _inspection_payload(result: ProcessingResult[None]) -> dict[str, object]:
    return {
        "detections": [_detection_payload(report) for report in result.detections],
        "statistics": {
            "blocks_processed": result.statistics.blocks_processed,
            "detections_found": result.statistics.detections_found,
            "replacements_applied": result.statistics.replacements_applied,
            "backend_invocations": result.statistics.backend_invocations,
            "local_block_calls": result.statistics.local_block_calls,
            "remote_block_calls": result.statistics.remote_block_calls,
        },
        "warnings": [
            {"code": warning.code, "message": warning.message, "block_id": warning.block_id}
            for warning in result.warnings
        ],
    }


def _detection_payload(report: DetectionReport) -> dict[str, object]:
    return {
        "entity_type": report.entity_type.value,
        "block_id": report.block_id,
        "location": _location_payload(report),
        "start": report.start,
        "end": report.end,
        "confidence": report.confidence,
        "backend": report.backend,
        "detector": report.detector,
    }


def _location_payload(report: DetectionReport) -> dict[str, object]:
    location = report.location
    if isinstance(location, TextOffsetLocation):
        return {"kind": "text_offset", "start": location.start, "end": location.end}
    if isinstance(location, JSONPathLocation):
        return {"kind": "json_path", "path": location.path}
    if isinstance(location, CSVCellLocation):
        return {"kind": "csv_cell", "row": location.row, "column": location.column}
    raise TypeError("unsupported report location")


if __name__ == "__main__":
    raise SystemExit(main())
