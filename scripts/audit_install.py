import argparse
import importlib
import json
import socket
import sys
import time
import tracemalloc
from importlib.metadata import distribution

FORBIDDEN_IMPORTS = {
    "aiohttp",
    "docling",
    "docx",
    "httpx",
    "onnxruntime",
    "openpyxl",
    "pypdf",
    "pytesseract",
}
EXPECTED_BASE_REQUIREMENTS = frozenset()


def _blocked_network(*arguments: object, **keywords: object) -> None:
    raise RuntimeError("network access during import")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=False)
    arguments = parser.parse_args()

    expected_version = arguments.version
    if not expected_version:
        import tomllib

        with open("pyproject.toml", "rb") as stream:
            expected_version = tomllib.load(stream)["project"]["version"]

    installed = distribution("pseudonymize")
    if installed.version != expected_version:
        raise RuntimeError("installed version does not match release")
    base_requirements = frozenset(
        requirement.split(";", 1)[0].strip()
        for requirement in installed.requires or ()
        if "extra ==" not in requirement
    )
    if base_requirements != EXPECTED_BASE_REQUIREMENTS:
        raise RuntimeError("installed base dependencies do not match the release contract")
    files = {str(path).replace("\\", "/") for path in installed.files or ()}
    if "pseudonymize/py.typed" not in files:
        raise RuntimeError("installed package is missing py.typed")
    if not any(path.endswith(".dist-info/licenses/LICENSE") for path in files):
        raise RuntimeError("installed package is missing its licence")

    socket.socket = _blocked_network  # type: ignore[misc,assignment]
    socket.create_connection = _blocked_network  # type: ignore[assignment]
    tracemalloc.start()
    started = time.perf_counter()
    importlib.import_module("pseudonymize")
    elapsed_ms = (time.perf_counter() - started) * 1_000
    peak_bytes = tracemalloc.get_traced_memory()[1]
    loaded = {name.partition(".")[0] for name in sys.modules}
    forbidden = FORBIDDEN_IMPORTS.intersection(loaded)
    if forbidden:
        raise RuntimeError(f"optional imports loaded: {', '.join(sorted(forbidden))}")
    print(json.dumps({"import_ms": round(elapsed_ms, 3), "peak_bytes": peak_bytes}))


if __name__ == "__main__":
    main()
