# ruff: noqa: E501
from pathlib import Path

import pytest

from pseudonymize.bench import evaluate, main


def test_bench_evaluate(tmp_path: Path) -> None:
    sample_file = tmp_path / "test_bench.jsonl"
    sample_file.write_text(
        '{"source_text": "Hello John, mail bob@example.com.", "privacy_mask": [{"start": 6, "end": 10, "label": "PERSON"}, {"start": 17, "end": 32, "label": "EMAIL"}]}\n',
        encoding="utf-8",
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
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", ["pseudonymize.bench", str(sample_file), "--ml"])
    main()


@pytest.mark.parametrize(
    "detections,truth",
    [
        ([], []),
        ([(0, 3, "EMAIL")], []),
        ([], [(0, 3, "EMAIL")]),
        ([(0, 3, "EMAIL")], [(4, 7, "EMAIL")]),
    ],
)
def test_match_empty_and_disjoint_spans(
    detections: list[tuple[int, int, str]], truth: list[tuple[int, int, str]]
) -> None:
    from pseudonymize.bench import _match
    from pseudonymize.result import EntityType

    assert _match(
        [(start, end, EntityType(kind)) for start, end, kind in detections], truth, True
    ) == (set(), set())


def test_match_is_one_to_one() -> None:
    from pseudonymize.bench import _match
    from pseudonymize.result import EntityType

    assert _match(
        [(0, 8, EntityType.EMAIL), (1, 7, EntityType.EMAIL)], [(0, 8, "EMAIL")], True
    ) == ({0}, {0})
    assert _match([(0, 8, EntityType.EMAIL)], [(0, 8, "EMAIL"), (1, 7, "EMAIL")], True) == (
        {0},
        {0},
    )
    assert _match(
        [(0, 3, EntityType.EMAIL), (5, 8, EntityType.PHONE)],
        [(0, 3, "EMAIL"), (5, 8, "PHONE")],
        True,
    ) == ({0, 1}, {0, 1})
    assert _match([(0, 3, EntityType.EMAIL)], [(0, 3, "PHONE")], True) == (set(), set())
    assert _match([(0, 3, EntityType.EMAIL)], [(0, 3, "PHONE")], False) == ({0}, {0})


def test_benchmark_metrics_and_explanations(
    tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    import json
    import logging

    email = "synthetic@example.com"
    missing = "Syntheticname"
    rows = [
        {"source_text": email, "privacy_mask": [{"start": 0, "end": len(email), "label": "EMAIL"}]},
        {"source_text": email, "privacy_mask": []},
        {
            "source_text": missing,
            "privacy_mask": [{"start": 0, "end": len(missing), "label": "PERSON"}],
        },
        {"source_text": "nothing sensitive here", "privacy_mask": []},
    ]
    sample = tmp_path / "corpus.jsonl"
    sample.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
    with caplog.at_level(logging.INFO, logger="pseudonymize.bench"):
        evaluate(sample, explain=True)
    assert "True Positives:  1" in caplog.text
    assert "False Positives: 1" in caplog.text
    assert "False Negatives: 1" in caplog.text
    assert "Precision:       0.5000" in caplog.text
    assert "Recall:          0.5000" in caplog.text
    assert "F1 Score:        0.5000" in caplog.text
    assert email not in caplog.text
    assert missing not in caplog.text


def test_import_does_not_load_optional_ml_or_configure_logging() -> None:
    import subprocess
    import sys

    subprocess.run(
        [
            sys.executable,
            "-c",
            "import logging, sys; before = list(logging.getLogger().handlers); "
            "import pseudonymize.bench; "
            "assert logging.getLogger().handlers == before; "
            "assert not {'onnxruntime', 'tokenizers', 'numpy'} & sys.modules.keys()",
        ],
        check=True,
        capture_output=True,
        timeout=30,
    )
