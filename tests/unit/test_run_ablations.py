import json
from pathlib import Path

from benchmarks.run_ablations import run_ablation_suite


def test_run_ablation_suite_on_local_file(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus.jsonl"
    corpus.write_text(
        json.dumps(
            {
                "language": "en",
                "source_text": "Email alice@example.com directly.",
                "privacy_mask": [{"start": 6, "end": 23, "label": "EMAIL"}],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    res = run_ablation_suite(file_path=corpus, samples=1)
    assert res["samples"] == 1
    assert "baseline_metrics" in res
    assert "baseline_exact" in res
    assert "baseline_errors" in res
    assert "ablations" in res
    assert "rules_only" in res["ablations"]
    assert "delta_f1" in res["ablations"]["rules_only"]
