from typing import Any

from benchmarks.quality_gate import evaluate_quality_gate


def _make_dummy_eval_record(
    precision: float = 0.86,
    recall: float = 0.80,
    f1: float = 0.83,
    card_recall: float = 1.0,
    dataset_revision: str = "a785eb528e28be2693c3718a27e066970de5dadb",
    model_sha: str = "1d02f3829ad90d95dea5e64d35f5528f96d7b223c1e056a96075c6229a484356",
) -> dict[str, Any]:
    return {
        "dataset": "ai4privacy/pii-masking-openpii-1.5m",
        "dataset_revision": dataset_revision,
        "split": "validation",
        "samples": 2,
        "metrics": {"f1": f1, "precision": precision, "recall": recall},
        "exact_metrics": {"f1": f1, "precision": precision, "recall": recall},
        "model_sha256": {"model_int8.onnx": model_sha},
        "per_entity": {
            "EMAIL": {"true_positives": 10, "false_positives": 1, "false_negatives": 1},
            "PAYMENT_CARD": {
                "true_positives": int(10 * card_recall),
                "false_positives": 0,
                "false_negatives": 10 - int(10 * card_recall),
            },
        },
        "error_categories": {
            "missing_candidate": 1,
            "threshold_suppression": 0,
            "label_confusion": 0,
            "boundary_mismatch": 0,
            "conflict_loss": 0,
        },
        "rows": [
            {
                "row_hash": "hash_row_1",
                "length_bucket": "100-500",
                "language": "en",
                "source": "wiki",
                "tp": {"EMAIL": 5, "PAYMENT_CARD": int(5 * card_recall)},
                "fp": {"EMAIL": 0, "PAYMENT_CARD": 0},
                "fn": {"EMAIL": 0, "PAYMENT_CARD": 5 - int(5 * card_recall)},
                "exact_tp": {"EMAIL": 5, "PAYMENT_CARD": int(5 * card_recall)},
                "exact_fp": {"EMAIL": 0, "PAYMENT_CARD": 0},
                "exact_fn": {"EMAIL": 0, "PAYMENT_CARD": 5 - int(5 * card_recall)},
                "error_categories": {},
            },
            {
                "row_hash": "hash_row_2",
                "length_bucket": "100-500",
                "language": "en",
                "source": "wiki",
                "tp": {"EMAIL": 5, "PAYMENT_CARD": int(5 * card_recall)},
                "fp": {"EMAIL": 1, "PAYMENT_CARD": 0},
                "fn": {"EMAIL": 1, "PAYMENT_CARD": 5 - int(5 * card_recall)},
                "exact_tp": {"EMAIL": 5, "PAYMENT_CARD": int(5 * card_recall)},
                "exact_fp": {"EMAIL": 1, "PAYMENT_CARD": 0},
                "exact_fn": {"EMAIL": 1, "PAYMENT_CARD": 5 - int(5 * card_recall)},
                "error_categories": {},
            },
        ],
    }


def test_quality_gate_passes_healthy_candidate() -> None:
    base = _make_dummy_eval_record(f1=0.83, precision=0.86)
    cand = _make_dummy_eval_record(f1=0.84, precision=0.865)

    report = evaluate_quality_gate(
        base, cand, {"character_micro_metrics": {"f1": 0.82}}, num_resamples=50
    )
    assert report.passed
    assert report.recommendation == "SHIP"
    assert report.criteria_results["pinned_provenance"].passed
    assert report.criteria_results["paired_f1_delta"].passed
    assert report.criteria_results["precision_protection"].passed
    assert report.criteria_results["critical_entities_floor"].passed


def test_quality_gate_rejects_precision_regression() -> None:
    base = _make_dummy_eval_record(precision=0.86)
    cand = _make_dummy_eval_record(precision=0.84)  # Drops by 0.02

    report = evaluate_quality_gate(base, cand, num_resamples=50)
    assert not report.passed
    assert report.recommendation == "REJECT"
    assert not report.criteria_results["precision_protection"].passed
    assert "Precision regressed" in report.summary_reasons[0]


def test_quality_gate_rejects_critical_identifier_recall_regression() -> None:
    base = _make_dummy_eval_record(card_recall=1.0)
    cand = _make_dummy_eval_record(card_recall=0.8)  # Payment cards missed

    report = evaluate_quality_gate(base, cand, num_resamples=50)
    assert not report.passed
    assert report.recommendation == "REJECT"
    assert not report.criteria_results["critical_entities_floor"].passed
    assert "Recall regressed for 1 high-risk" in (
        report.criteria_results["critical_entities_floor"].failure_reason or ""
    )


def test_quality_gate_rejects_unpinned_provenance() -> None:
    base = _make_dummy_eval_record()
    cand = _make_dummy_eval_record(dataset_revision="")  # Missing revision

    report = evaluate_quality_gate(base, cand, num_resamples=50)
    assert not report.passed
    assert not report.criteria_results["pinned_provenance"].passed


def test_quality_gate_verifies_external_generalization_floor() -> None:
    base = _make_dummy_eval_record()
    cand = _make_dummy_eval_record()

    ext_pass = {"character_micro_metrics": {"f1": 0.82}}
    report_pass = evaluate_quality_gate(base, cand, external_eval_record=ext_pass, num_resamples=50)
    assert report_pass.passed

    ext_fail = {"character_micro_metrics": {"f1": 0.50}}  # Below 0.70 floor
    report_fail = evaluate_quality_gate(base, cand, external_eval_record=ext_fail, num_resamples=50)
    assert not report_fail.passed
    assert not report_fail.criteria_results["external_generalization"].passed


def test_quality_gate_rejects_missing_external_evidence() -> None:
    report = evaluate_quality_gate(
        _make_dummy_eval_record(), _make_dummy_eval_record(), num_resamples=10
    )
    assert not report.passed
    assert not report.criteria_results["external_generalization"].passed


def test_quality_gate_rejects_missing_critical_entity_counts() -> None:
    base = _make_dummy_eval_record()
    candidate = _make_dummy_eval_record()
    del candidate["per_entity"]["PAYMENT_CARD"]
    report = evaluate_quality_gate(
        base, candidate, {"character_micro_metrics": {"f1": 0.82}}, num_resamples=10
    )
    assert not report.passed
    assert not report.criteria_results["critical_entities_floor"].passed


def test_quality_gate_rejects_invalid_external_scores() -> None:
    for f1 in (float("inf"), float("nan"), -0.1, 1.1, True, "0.82", None):
        report = evaluate_quality_gate(
            _make_dummy_eval_record(),
            _make_dummy_eval_record(),
            {"character_micro_metrics": {"f1": f1}},
            num_resamples=10,
        )
        assert not report.passed
        assert not report.criteria_results["external_generalization"].passed


def test_zero_critical_recall_is_rejected_without_division_error() -> None:
    base = _make_dummy_eval_record()
    candidate = _make_dummy_eval_record(card_recall=0.0)
    candidate["per_entity"]["PAYMENT_CARD"]["false_positives"] = 1
    report = evaluate_quality_gate(
        base, candidate, {"character_micro_metrics": {"f1": 0.82}}, num_resamples=10
    )
    assert not report.passed
    assert not report.criteria_results["critical_entities_floor"].passed


def test_quality_gate_rejects_changed_critical_support() -> None:
    base = _make_dummy_eval_record()
    candidate = _make_dummy_eval_record()
    candidate["per_entity"]["EMAIL"]["false_negatives"] = 0
    report = evaluate_quality_gate(
        base, candidate, {"character_micro_metrics": {"f1": 0.82}}, num_resamples=10
    )
    assert not report.passed
    assert not report.criteria_results["critical_entities_floor"].passed
