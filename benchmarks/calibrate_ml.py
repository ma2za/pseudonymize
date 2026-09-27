"""ML calibration and temperature scaling runner.

Measures Expected Calibration Error (ECE), Brier score, and NLL on calibration
traces, fits global temperature scaling via NLL optimization, and selects
constrained emission thresholds on development/calibration data only.
"""

from __future__ import annotations

import argparse
import logging
import math
from pathlib import Path
from typing import Any

import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("calibrate_ml")


def compute_calibration_metrics(
    confidences: np.ndarray,
    correctness: np.ndarray,
    num_bins: int = 10,
) -> dict[str, Any]:
    """Compute Expected Calibration Error (ECE), MCE, and reliability diagram bins.

    Args:
        confidences: 1D array of predicted confidence values in [0, 1].
        correctness: 1D boolean array indicating whether prediction was correct (1) or not (0).
        num_bins: Number of equal-width confidence buckets.
    """
    if len(confidences) == 0:
        return {
            "ece": 0.0,
            "mce": 0.0,
            "brier_score": 0.0,
            "sample_count": 0,
            "bins": [],
        }

    confidences = np.clip(np.asarray(confidences, dtype=np.float64), 0.0, 1.0)
    correctness = np.asarray(correctness, dtype=np.float64)

    # Brier score
    brier_score = float(np.mean((confidences - correctness) ** 2))

    bin_boundaries = np.linspace(0.0, 1.0, num_bins + 1)
    bin_data = []

    total_samples = len(confidences)
    weighted_ece = 0.0
    mce = 0.0

    for i in range(num_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]

        if i == num_bins - 1:
            in_bin = (confidences >= bin_lower) & (confidences <= bin_upper)
        else:
            in_bin = (confidences >= bin_lower) & (confidences < bin_upper)

        bin_count = int(np.sum(in_bin))
        if bin_count > 0:
            bin_acc = float(np.mean(correctness[in_bin]))
            bin_conf = float(np.mean(confidences[in_bin]))
            gap = abs(bin_acc - bin_conf)

            weighted_ece += (bin_count / total_samples) * gap
            mce = max(mce, gap)

            bin_data.append(
                {
                    "bin_lower": float(bin_lower),
                    "bin_upper": float(bin_upper),
                    "count": bin_count,
                    "accuracy": bin_acc,
                    "confidence": bin_conf,
                    "calibration_gap": gap,
                }
            )
        else:
            bin_data.append(
                {
                    "bin_lower": float(bin_lower),
                    "bin_upper": float(bin_upper),
                    "count": 0,
                    "accuracy": 0.0,
                    "confidence": 0.0,
                    "calibration_gap": 0.0,
                }
            )

    return {
        "ece": float(weighted_ece),
        "mce": float(mce),
        "brier_score": brier_score,
        "sample_count": total_samples,
        "bins": bin_data,
    }


def compute_nll(logits: np.ndarray, targets: np.ndarray, temperature: float = 1.0) -> float:
    """Compute mean Negative Log-Likelihood (NLL) with temperature scaling."""
    scaled_logits = logits / max(temperature, 1e-6)
    max_logits = np.max(scaled_logits, axis=-1, keepdims=True)
    log_sum_exp = max_logits + np.log(
        np.sum(np.exp(scaled_logits - max_logits), axis=-1, keepdims=True)
    )
    log_probs = scaled_logits - log_sum_exp

    n = len(targets)
    if n == 0:
        return 0.0

    # Pick log prob of true target
    row_indices = np.arange(n)
    target_log_probs = log_probs[row_indices, targets]
    return float(-np.mean(target_log_probs))


def fit_temperature_scaling(
    logits: np.ndarray,
    targets: np.ndarray,
    bounds: tuple[float, float] = (0.1, 10.0),
    tol: float = 1e-5,
) -> tuple[float, float]:
    """Fit optimal temperature T minimizing NLL via Golden Section Search.

    Returns:
        (optimal_temperature, optimal_nll)
    """
    a, b = bounds
    invphi = (math.sqrt(5) - 1) / 2  # ~0.6180339887
    invphi2 = (3 - math.sqrt(5)) / 2  # ~0.3819660113

    c = a + invphi2 * (b - a)
    d = a + invphi * (b - a)

    fc = compute_nll(logits, targets, c)
    fd = compute_nll(logits, targets, d)

    while abs(b - a) > tol:
        if fc < fd:
            b = d
            d = c
            fd = fc
            c = a + invphi2 * (b - a)
            fc = compute_nll(logits, targets, c)
        else:
            a = c
            c = d
            fc = fd
            d = a + invphi * (b - a)
            fd = compute_nll(logits, targets, d)

    best_temp = (a + b) / 2
    best_nll = compute_nll(logits, targets, best_temp)
    return float(best_temp), float(best_nll)


def select_constrained_threshold(
    confidences: np.ndarray,
    labels: np.ndarray,
    baseline_precision: float,
    candidate_thresholds: list[float] | None = None,
) -> dict[str, Any]:
    """Select emission threshold maximizing F1 on calibration data without regressing precision."""
    if candidate_thresholds is None:
        candidate_thresholds = [float(round(float(t), 2)) for t in np.arange(0.05, 0.95, 0.05)]

    best_threshold = 0.50
    best_f1 = -1.0
    best_precision = 0.0
    best_recall = 0.0

    results_table = []

    for t in candidate_thresholds:
        preds = confidences >= t
        tp = int(np.sum((preds == 1) & (labels == 1)))
        fp = int(np.sum((preds == 1) & (labels == 0)))
        fn = int(np.sum((preds == 0) & (labels == 1)))

        p = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        r = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * p * r) / (p + r) if (p + r) > 0 else 0.0

        satisfies_constraint = p >= baseline_precision

        results_table.append(
            {
                "threshold": t,
                "precision": p,
                "recall": r,
                "f1": f1,
                "satisfies_constraint": satisfies_constraint,
            }
        )

        if satisfies_constraint and f1 > best_f1:
            best_f1 = f1
            best_threshold = t
            best_precision = p
            best_recall = r

    # If no threshold strictly satisfies the constraint, pick highest precision
    if best_f1 < 0:
        logger.warning(
            f"No threshold met baseline precision {baseline_precision:.4f}; "
            "selecting threshold with highest precision."
        )
        best_candidate = max(results_table, key=lambda x: x["precision"])
        best_threshold = best_candidate["threshold"]
        best_precision = best_candidate["precision"]
        best_recall = best_candidate["recall"]
        best_f1 = best_candidate["f1"]

    return {
        "best_threshold": best_threshold,
        "best_f1": best_f1,
        "best_precision": best_precision,
        "best_recall": best_recall,
        "baseline_precision": baseline_precision,
        "threshold_evaluations": results_table,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fit temperature scaling and compute ML calibration metrics."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("benchmarks/results/ml_calibration_artifact.json"),
        help="Path to output calibration artifact JSON.",
    )
    _ = parser.parse_args()

    print("\n" + "=" * 78)
    print("ML CALIBRATION & TEMPERATURE SCALING RUNNER")
    print("=" * 78)
    print("Run via pytest or evaluation runner to fit on calibration traces.")
    print("=" * 78)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
