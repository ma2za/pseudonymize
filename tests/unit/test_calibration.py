import numpy as np
import pytest
from benchmarks.calibrate_ml import (
    compute_calibration_metrics,
    compute_nll,
    fit_temperature_scaling,
    select_constrained_threshold,
)


def test_compute_calibration_metrics_perfect_calibration() -> None:
    # Confidences match actual empirical frequencies exactly:
    # 10 samples at 0.9 confidence, 9 correct, 1 incorrect -> acc = 0.9, gap = 0.0
    confidences = np.array([0.9] * 10)
    correctness = np.array([1] * 9 + [0] * 1)

    metrics = compute_calibration_metrics(confidences, correctness, num_bins=10)
    assert metrics["sample_count"] == 10
    assert pytest.approx(metrics["ece"], abs=1e-5) == 0.0
    assert pytest.approx(metrics["mce"], abs=1e-5) == 0.0
    # Brier score:
    # 9 * (0.9 - 1)^2 + 1 * (0.9 - 0)^2 = 9 * 0.01 + 0.81 = 0.90 / 10 = 0.09
    assert pytest.approx(metrics["brier_score"], abs=1e-5) == 0.09


def test_compute_calibration_metrics_empty() -> None:
    metrics = compute_calibration_metrics(np.array([]), np.array([]))
    assert metrics["sample_count"] == 0
    assert metrics["ece"] == 0.0
    assert metrics["mce"] == 0.0
    assert metrics["brier_score"] == 0.0


def test_compute_calibration_metrics_overconfident() -> None:
    # Predicted 0.95 confidence for 10 samples, but all are incorrect (acc = 0.0)
    confidences = np.array([0.95] * 10)
    correctness = np.array([0] * 10)

    metrics = compute_calibration_metrics(confidences, correctness, num_bins=10)
    assert metrics["sample_count"] == 10
    assert pytest.approx(metrics["ece"], abs=1e-4) == 0.95
    assert pytest.approx(metrics["mce"], abs=1e-4) == 0.95


def test_fit_temperature_scaling_sharpens_underconfident() -> None:
    # Logits: high uncertainty, but targets are consistent -> optimal T should be < 1.0 (sharpen)
    logits = np.array(
        [
            [1.0, 0.5, 0.0],
            [1.2, 0.4, 0.1],
            [0.9, 0.3, 0.2],
            [1.1, 0.2, 0.0],
        ]
    )
    targets = np.array([0, 0, 0, 0])

    t_opt, nll_opt = fit_temperature_scaling(logits, targets, bounds=(0.1, 5.0))
    initial_nll = compute_nll(logits, targets, temperature=1.0)

    assert t_opt < 1.0
    assert nll_opt < initial_nll


def test_fit_temperature_scaling_softens_overconfident() -> None:
    # Logits are extreme, but some targets are wrong -> optimal T should be > 1.0 (soften)
    logits = np.array(
        [
            [10.0, 0.0, 0.0],
            [10.0, 0.0, 0.0],
            [10.0, 0.0, 0.0],
            [10.0, 0.0, 0.0],
        ]
    )
    targets = np.array([0, 0, 0, 1])  # One mistake under extreme confidence

    t_opt, nll_opt = fit_temperature_scaling(logits, targets, bounds=(0.5, 10.0))
    initial_nll = compute_nll(logits, targets, temperature=1.0)

    assert t_opt > 1.0
    assert nll_opt < initial_nll


def test_select_constrained_threshold_respects_precision_floor() -> None:
    # 5 true positives, 5 false positives at low threshold
    confidences = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95])
    # Ground truth: only items with conf >= 0.6 are true
    labels = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

    # Required baseline precision: 0.90
    res = select_constrained_threshold(
        confidences=confidences,
        labels=labels,
        baseline_precision=0.90,
        candidate_thresholds=[0.1, 0.3, 0.5, 0.6, 0.7, 0.8],
    )

    assert res["best_threshold"] >= 0.6
    assert res["best_precision"] >= 0.90
    assert res["best_f1"] > 0.0
