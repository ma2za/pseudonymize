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
from pseudonymize.engine import Data, Pseudonymizer
from pseudonymize.exceptions import PseudonymizeError
from pseudonymize.policy import Policy


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pseudonymize")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("keygen", help="print a new base64-encoded key")
    subparsers.add_parser("detectors", help="list bundled detectors")

    text_parser = subparsers.add_parser("text", help="process text")
    text_parser.add_argument("text", help="text to process, or - for standard input")
    _add_key_options(text_parser, allow_stdin=True)
    text_parser.add_argument("--namespace", default="default")
    text_parser.add_argument("--redact", action="store_true")

    json_parser = subparsers.add_parser("json", help="process JSON from standard input")
    _add_key_options(json_parser)
    json_parser.add_argument("--namespace", default="default")
    return parser


def _add_key_options(parser: argparse.ArgumentParser, *, allow_stdin: bool = False) -> None:
    sources = parser.add_mutually_exclusive_group(required=True)
    sources.add_argument("--key-env", metavar="NAME")
    sources.add_argument("--key-file", type=Path)
    sources.add_argument("--key-fd", type=int)
    if allow_stdin:
        sources.add_argument("--key-stdin", action="store_true")


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
        if arguments.text == "-":
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
        key = _read_key(arguments)
        engine = Pseudonymizer(
            key=key,
            namespace=arguments.namespace,
            policy=Policy.llm() if arguments.command == "json" else Policy.default(),
        )
        if arguments.command == "text":
            source = sys.stdin.read() if arguments.text == "-" else arguments.text
            if arguments.redact:
                from pseudonymize.transforms import RedactTransformer

                engine = Pseudonymizer(
                    key=key, policy=Policy.default(), transformer=RedactTransformer()
                )
            print(engine.process(source).text)
            return 0
        payload = json.load(sys.stdin)
        output: Data = engine.process_data(payload)
        json.dump(output, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
        return 0
    except (OSError, ValueError, json.JSONDecodeError, PseudonymizeError) as error:
        parser.exit(2, f"pseudonymize: error: {error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
