import json
from pathlib import Path

from pseudonymize import Pseudonymizer

KEY = b"release-audit-key-material-00000001"


def test_large_jsonl_preserves_scope_and_removes_every_match(tmp_path: Path) -> None:
    source = tmp_path / "large.jsonl"
    records = [
        {
            "record": index,
            "owner": "maria@example.com" if index % 2 else "paolo@example.com",
            "message": f"Contact maria@example.com from 192.0.2.{index % 250 + 1}",
        }
        for index in range(2_000)
    ]
    source.write_text("".join(f"{json.dumps(record)}\n" for record in records), encoding="utf-8")

    result = Pseudonymizer().process_file(source)
    rendered = result.output.read_text(encoding="utf-8")
    output = [json.loads(line) for line in rendered.splitlines()]

    assert "maria@example.com" not in rendered
    assert "paolo@example.com" not in rendered
    assert result.statistics.blocks_processed == 4_000
    assert result.statistics.replacements_applied == 6_000
    assert output[1_999]["record"] == 1_999
    assert {record["owner"] for record in output} == {"<EMAIL_1>", "<EMAIL_2>"}


def test_deterministic_batch_is_stable_unique_and_idempotent() -> None:
    inputs = [f"user{index}@example.com" for index in range(1_000)]
    engine = Pseudonymizer(mode="deterministic", key=KEY, namespace="release-audit")

    first = tuple(result.text for result in engine.process_batch(inputs))
    second = tuple(result.text for result in engine.process_batch(inputs))

    assert first == second
    assert len(set(first)) == len(inputs)
    assert tuple(engine.process(value).text for value in first) == first


def test_control_characters_do_not_leak_matches_into_reports() -> None:
    source = "\x00\u202e\u2066maria@example.com\u2069\n192.0.2.10\x1f"

    result = Pseudonymizer().process_with_report(source)

    assert result.output == "\x00\u202e\u2066<EMAIL_1>\u2069\n<IP_ADDRESS_1>\x1f"
    assert "maria@example.com" not in repr(result)
    assert "192.0.2.10" not in repr(result)
