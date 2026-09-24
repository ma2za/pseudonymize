import pytest
from benchmarks.compare_quality import (
    compare_results,
    format_comparison,
    validate_compatibility,
)


def _make_dummy_run(
    dataset_revision: str = "rev1",
    samples: int = 2,
    row_hashes: list[str] | None = None,
    f1: float = 0.80,
    tp_offset: int = 0,
) -> dict[str, object]:
    if row_hashes is None:
        row_hashes = ["hash_row_001", "hash_row_002"]

    rows = [
        {
            "row_hash": h,
            "length_bucket": "100-500",
            "language": "en",
            "source": "wiki",
            "tp": {"EMAIL": 1 + tp_offset},
            "fp": {"EMAIL": 0},
            "fn": {"EMAIL": 0},
            "exact_tp": {"EMAIL": 1 + tp_offset},
            "exact_fp": {"EMAIL": 0},
            "exact_fn": {"EMAIL": 0},
            "error_categories": {
                "missing_candidate": 0,
                "threshold_suppression": 0,
                "label_confusion": 0,
                "boundary_mismatch": 0,
                "conflict_loss": 0,
            },
        }
        for h in row_hashes
    ]

    return {
        "dataset": "ai4privacy/pii-masking-openpii-1.5m",
        "dataset_revision": dataset_revision,
        "split": "validation",
        "samples": samples,
        "metrics": {"f1": f1, "precision": 1.0, "recall": f1},
        "exact_metrics": {"f1": f1, "precision": 1.0, "recall": f1},
        "macro_f1": f1,
        "per_entity": {
            "EMAIL": {
                "true_positives": (1 + tp_offset) * samples,
                "false_positives": 0,
                "false_negatives": 0,
            }
        },
        "error_categories": {
            "missing_candidate": 0,
            "threshold_suppression": 0,
            "label_confusion": 0,
            "boundary_mismatch": 0,
            "conflict_loss": 0,
        },
        "rows": rows,
    }


def test_validate_compatibility_rejects_mismatched_revisions() -> None:
    base = _make_dummy_run(dataset_revision="rev1")
    cand = _make_dummy_run(dataset_revision="rev2")
    with pytest.raises(ValueError, match="dataset_revision"):
        validate_compatibility(base, cand)


def test_validate_compatibility_rejects_mismatched_row_manifests() -> None:
    base = _make_dummy_run(row_hashes=["row_a", "row_b"])
    cand = _make_dummy_run(row_hashes=["row_a", "row_c"])
    with pytest.raises(ValueError, match="Row manifests do not match"):
        validate_compatibility(base, cand)


def test_compare_identical_runs_yields_zero_delta() -> None:
    base = _make_dummy_run(f1=0.85)
    cand = _make_dummy_run(f1=0.85)

    res = compare_results(base, cand, num_resamples=100, seed=42)
    assert res["metrics"]["delta_f1"] == 0.0
    assert res["metrics"]["ci_95"] == [0.0, 0.0]
    assert res["metrics"]["exact_ci_95"] == [0.0, 0.0]
    assert res["per_entity"]["EMAIL"]["delta_tp"] == 0


def test_compare_improved_candidate_yields_positive_delta() -> None:
    base = _make_dummy_run(f1=0.80, tp_offset=0)
    cand = _make_dummy_run(f1=0.90, tp_offset=1)

    res = compare_results(base, cand, num_resamples=100, seed=42)
    assert res["metrics"]["delta_f1"] == pytest.approx(0.10)
    assert res["per_entity"]["EMAIL"]["delta_tp"] > 0

    report = format_comparison(res)
    assert "EVALUATION COMPARISON REPORT" in report
    assert "EMAIL" in report
