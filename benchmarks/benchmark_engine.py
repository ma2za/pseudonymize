import json
from pathlib import Path

from pseudonymize import Pseudonymizer

KEY = b"benchmark-only-key-material-0001"


def test_process_synthetic_messages(benchmark: object) -> None:
    rows = (
        Path("benchmarks/datasets/synthetic_messages.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    )
    text = "\n".join(json.loads(row)["content"] for row in rows)
    engine = Pseudonymizer(key=KEY)
    benchmark(engine.process, text)  # type: ignore[operator]
