import json
from pathlib import Path

import pytest
from benchmarks.run_bakeoff import (
    assess_quantization_damage,
    compute_oracle_diagnostics,
    generate_decision_record,
    run_bakeoff_suite,
)


def test_assess_quantization_damage_within_tolerance() -> None:
    # Baseline and FP32 identical
    base = {
        "dataset": "ai4privacy",
        "dataset_revision": "a785eb528e28be2693c3718a27e066970de5dadb",
        "split": "validation",
        "samples": 1,
        "rows": [
            {
                "row_hash": "hash_1",
                "length_bucket": "100-500",
                "language": "en",
                "source": "ai4privacy",
                "tp": {"EMAIL": 1},
                "fp": {"EMAIL": 0},
                "fn": {"EMAIL": 0},
                "exact_tp": {"EMAIL": 1},
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
        ],
        "per_entity": {
            "EMAIL": {
                "true_positives": 1,
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
    }
    cand = dict(base)

    damage = assess_quantization_damage(base, cand, tolerance=0.02)
    assert damage["acceptable"]
    assert damage["delta_f1_int8_vs_fp32"] == 0.0


def test_compute_oracle_diagnostics() -> None:
    eval_result = {
        "counts": {"true_positives": 80, "false_positives": 20, "false_negatives": 20},
        "error_categories": {
            "boundary_mismatch": 10,
            "label_confusion": 5,
        },
    }

    diagnostics = compute_oracle_diagnostics(eval_result)
    assert pytest.approx(diagnostics["baseline_f1"], abs=1e-5) == 0.80
    assert diagnostics["oracle_boundary_f1"] > 0.80
    assert diagnostics["boundary_potential_gain"] > 0.0
    assert diagnostics["oracle_label_f1"] > 0.80
    assert diagnostics["label_potential_gain"] > 0.0


def test_generate_decision_record() -> None:
    bakeoff_results = {
        "quantization": {"delta_f1_int8_vs_fp32": 0.001, "acceptable": True},
        "oracle_diagnostics": {
            "baseline_f1": 0.83,
            "oracle_boundary_f1": 0.88,
            "boundary_potential_gain": 0.05,
            "oracle_label_f1": 0.85,
            "label_potential_gain": 0.02,
        },
    }

    record = generate_decision_record(
        baseline_manifest="multilang-pii-ner-onnx-int8",
        candidate_manifests=["multilang-pii-ner-onnx-fp32", "piiranha-v1"],
        evaluation_summary={"f1": 0.83},
        bakeoff_results=bakeoff_results,
    )

    assert "# Model and Evidence-Fusion Bake-Off Decision Record (1.33.0)" in record
    assert "multilang-pii-ner-onnx-int8" in record
    assert "piiranha-v1" in record
    assert "Disqualified" in record
    assert "Quantization Damage Assessment" in record


def test_run_bakeoff_suite_on_local_file(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus.jsonl"
    corpus.write_text(
        json.dumps(
            {
                "language": "en",
                "source_text": "Call me at +1-555-0199.",
                "privacy_mask": [{"start": 11, "end": 23, "label": "PHONE"}],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    results = run_bakeoff_suite(file_path=corpus, samples=1, use_ml=False)
    assert "manifest_summary" in results
    assert "quantization" in results
    assert "oracle_diagnostics" in results
    assert "decision_record_md" in results
    assert "RETAIN" in results["decision_record_md"]
