import json
from pathlib import Path

import pytest

from pseudonymize import Pseudonymizer

KEY = b"benchmark-only-key-material-0001"


@pytest.mark.parametrize("size", [4 * 1024, 64 * 1024], ids=["4 KiB", "64 KiB"])
def test_process_synthetic_messages(benchmark: object, size: int) -> None:
    rows = (
        Path("benchmarks/datasets/synthetic_messages.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    )
    sample = "\n".join(json.loads(row)["content"] for row in rows)
    text = (sample * (size // len(sample) + 1))[:size]
    engine = Pseudonymizer(mode="deterministic", key=KEY)
    benchmark(engine.process, text)  # type: ignore[operator]
