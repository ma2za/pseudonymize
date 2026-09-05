import pytest
from pathlib import Path
from pseudonymize.bench import evaluate, main
from pseudonymize.result import EntityType

def test_bench_evaluate(tmp_path: Path) -> None:
    sample_file = tmp_path / "test_bench.jsonl"
    sample_file.write_text(
        '{"source_text": "Hello John, mail bob@example.com.", "privacy_mask": [{"start": 6, "end": 10, "label": "PERSON"}, {"start": 17, "end": 32, "label": "EMAIL"}]}\n',
        encoding="utf-8"
    )
    # Run evaluation on our dummy file
    evaluate(sample_file, use_ml=False, strict_labels=True, explain=True)
    evaluate(sample_file, use_ml=False, strict_labels=False, explain=False)
    # Run evaluation with ML enabled
    evaluate(sample_file, use_ml=True, strict_labels=True, explain=True)

def test_bench_main(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    sample_file = tmp_path / "test_bench.jsonl"
    sample_file.write_text(
        '{"source_text": "Hello John, mail bob@example.com.", "privacy_mask": [{"start": 6, "end": 10, "label": "PERSON"}]}\n',
        encoding="utf-8"
    )
    monkeypatch.setattr("sys.argv", ["pseudonymize.bench", str(sample_file), "--ml"])
    main()
