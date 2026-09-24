"""Deterministic artifact comparator with paired document-level bootstrap resampling.

Validates that baseline and candidate evaluation runs share identical dataset
revisions, samples, and row manifests before computing metric deltas, 95%
confidence intervals, per-entity shifts, and causal error category migrations.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any


def validate_compatibility(baseline: dict[str, Any], candidate: dict[str, Any]) -> None:
    """Ensure two evaluation records can be legitimately compared."""
    for key in ("dataset", "dataset_revision", "split"):
        if baseline.get(key) != candidate.get(key):
            msg = (
                f"Incompatible evaluation records: '{key}' differs "
                f"(baseline: {baseline.get(key)!r}, candidate: {candidate.get(key)!r})"
            )
            raise ValueError(msg)

    if baseline.get("samples") != candidate.get("samples"):
        msg = (
            f"Sample count mismatch: baseline has {baseline.get('samples')} "
            f"rows but candidate has {candidate.get('samples')} rows"
        )
        raise ValueError(msg)

    if "rows" not in baseline or "rows" not in candidate:
        raise ValueError("Both evaluation records must contain 'rows' sufficient statistics")

    base_hashes = [r["row_hash"] for r in baseline["rows"]]
    cand_hashes = [r["row_hash"] for r in candidate["rows"]]
    if base_hashes != cand_hashes:
        raise ValueError("Row manifests do not match in sequence or row content")


def compute_paired_bootstrap(
    baseline_rows: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
    num_resamples: int = 1000,
    seed: int = 42,
) -> dict[str, Any]:
    """Perform paired document-level bootstrap resampling to compute 95% CIs for metric deltas."""
    n = len(baseline_rows)
    if n == 0:
        return {"ci_95": [0.0, 0.0], "exact_ci_95": [0.0, 0.0]}

    rng = random.Random(seed)  # noqa: S311
    f1_deltas: list[float] = []
    exact_f1_deltas: list[float] = []

    for _ in range(num_resamples):
        sample_indices = [rng.randrange(n) for _ in range(n)]

        # Baseline overlap metrics
        b_tp = sum(sum(baseline_rows[i]["tp"].values()) for i in sample_indices)
        b_fp = sum(sum(baseline_rows[i]["fp"].values()) for i in sample_indices)
        b_fn = sum(sum(baseline_rows[i]["fn"].values()) for i in sample_indices)
        b_p = b_tp / (b_tp + b_fp) if (b_tp + b_fp) > 0 else 0.0
        b_r = b_tp / (b_tp + b_fn) if (b_tp + b_fn) > 0 else 0.0
        b_f1 = (2 * b_p * b_r) / (b_p + b_r) if (b_p + b_r) > 0 else 0.0

        # Candidate overlap metrics
        c_tp = sum(sum(candidate_rows[i]["tp"].values()) for i in sample_indices)
        c_fp = sum(sum(candidate_rows[i]["fp"].values()) for i in sample_indices)
        c_fn = sum(sum(candidate_rows[i]["fn"].values()) for i in sample_indices)
        c_p = c_tp / (c_tp + c_fp) if (c_tp + c_fp) > 0 else 0.0
        c_r = c_tp / (c_tp + c_fn) if (c_tp + c_fn) > 0 else 0.0
        c_f1 = (2 * c_p * c_r) / (c_p + c_r) if (c_p + c_r) > 0 else 0.0

        f1_deltas.append(c_f1 - b_f1)

        # Baseline exact metrics
        b_etp = sum(sum(baseline_rows[i].get("exact_tp", {}).values()) for i in sample_indices)
        b_efp = sum(sum(baseline_rows[i].get("exact_fp", {}).values()) for i in sample_indices)
        b_efn = sum(sum(baseline_rows[i].get("exact_fn", {}).values()) for i in sample_indices)
        b_ep = b_etp / (b_etp + b_efp) if (b_etp + b_efp) > 0 else 0.0
        b_er = b_etp / (b_etp + b_efn) if (b_etp + b_efn) > 0 else 0.0
        b_ef1 = (2 * b_ep * b_er) / (b_ep + b_er) if (b_ep + b_er) > 0 else 0.0

        # Candidate exact metrics
        c_etp = sum(sum(candidate_rows[i].get("exact_tp", {}).values()) for i in sample_indices)
        c_efp = sum(sum(candidate_rows[i].get("exact_fp", {}).values()) for i in sample_indices)
        c_efn = sum(sum(candidate_rows[i].get("exact_fn", {}).values()) for i in sample_indices)
        c_ep = c_etp / (c_etp + c_efp) if (c_etp + c_efp) > 0 else 0.0
        c_er = c_etp / (c_etp + c_efn) if (c_etp + c_efn) > 0 else 0.0
        c_ef1 = (2 * c_ep * c_er) / (c_ep + c_er) if (c_ep + c_er) > 0 else 0.0

        exact_f1_deltas.append(c_ef1 - b_ef1)

    f1_deltas.sort()
    exact_f1_deltas.sort()

    lower_idx = int(0.025 * num_resamples)
    upper_idx = int(0.975 * num_resamples)

    return {
        "ci_95": [f1_deltas[lower_idx], f1_deltas[upper_idx]],
        "exact_ci_95": [exact_f1_deltas[lower_idx], exact_f1_deltas[upper_idx]],
    }


def compare_results(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
    num_resamples: int = 1000,
    seed: int = 42,
) -> dict[str, Any]:
    """Compare baseline and candidate evaluation runs and compute statistical deltas."""
    validate_compatibility(baseline, candidate)

    base_m = baseline.get("metrics", {})
    cand_m = candidate.get("metrics", {})
    f1_delta = cand_m.get("f1", 0.0) - base_m.get("f1", 0.0)
    precision_delta = cand_m.get("precision", 0.0) - base_m.get("precision", 0.0)
    recall_delta = cand_m.get("recall", 0.0) - base_m.get("recall", 0.0)

    base_exact = baseline.get("exact_metrics", {})
    cand_exact = candidate.get("exact_metrics", {})
    exact_f1_delta = cand_exact.get("f1", 0.0) - base_exact.get("f1", 0.0)

    base_macro = baseline.get("macro_f1", 0.0)
    cand_macro = candidate.get("macro_f1", 0.0)
    macro_f1_delta = cand_macro - base_macro

    bootstrap = compute_paired_bootstrap(
        baseline["rows"], candidate["rows"], num_resamples=num_resamples, seed=seed
    )

    # Per-entity deltas
    all_entities = sorted(
        set(baseline.get("per_entity", {}).keys()) | set(candidate.get("per_entity", {}).keys())
    )
    per_entity_shifts: dict[str, dict[str, Any]] = {}
    for et in all_entities:
        b_et = baseline.get("per_entity", {}).get(et, {})
        c_et = candidate.get("per_entity", {}).get(et, {})

        b_tp = b_et.get("true_positives", 0)
        b_fp = b_et.get("false_positives", 0)
        b_fn = b_et.get("false_negatives", 0)
        b_f1 = (
            (2 * (b_tp / (b_tp + b_fp)) * (b_tp / (b_tp + b_fn)))
            / ((b_tp / (b_tp + b_fp)) + (b_tp / (b_tp + b_fn)))
            if (b_tp + b_fp > 0 and b_tp + b_fn > 0)
            else 0.0
        )

        c_tp = c_et.get("true_positives", 0)
        c_fp = c_et.get("false_positives", 0)
        c_fn = c_et.get("false_negatives", 0)
        c_f1 = (
            (2 * (c_tp / (c_tp + c_fp)) * (c_tp / (c_tp + c_fn)))
            / ((c_tp / (c_tp + c_fp)) + (c_tp / (c_tp + c_fn)))
            if (c_tp + c_fp > 0 and c_tp + c_fn > 0)
            else 0.0
        )

        per_entity_shifts[et] = {
            "delta_tp": c_tp - b_tp,
            "delta_fp": c_fp - b_fp,
            "delta_fn": c_fn - b_fn,
            "delta_f1": c_f1 - b_f1,
            "baseline_f1": b_f1,
            "candidate_f1": c_f1,
        }

    # Error category shift
    error_keys = (
        "missing_candidate",
        "threshold_suppression",
        "label_confusion",
        "boundary_mismatch",
        "conflict_loss",
    )
    base_err = baseline.get("error_categories", {})
    cand_err = candidate.get("error_categories", {})
    error_shifts = {
        k: {
            "baseline": base_err.get(k, 0),
            "candidate": cand_err.get(k, 0),
            "delta": cand_err.get(k, 0) - base_err.get(k, 0),
        }
        for k in error_keys
    }

    return {
        "dataset": baseline.get("dataset"),
        "dataset_revision": baseline.get("dataset_revision"),
        "samples": baseline.get("samples"),
        "metrics": {
            "baseline_f1": base_m.get("f1", 0.0),
            "candidate_f1": cand_m.get("f1", 0.0),
            "delta_f1": f1_delta,
            "ci_95": bootstrap["ci_95"],
            "delta_precision": precision_delta,
            "delta_recall": recall_delta,
            "exact_baseline_f1": base_exact.get("f1", 0.0),
            "exact_candidate_f1": cand_exact.get("f1", 0.0),
            "exact_delta_f1": exact_f1_delta,
            "exact_ci_95": bootstrap["exact_ci_95"],
            "macro_f1_delta": macro_f1_delta,
        },
        "per_entity": per_entity_shifts,
        "error_categories": error_shifts,
    }


def format_comparison(result: dict[str, Any]) -> str:
    """Format comparison result as a readable ASCII report."""
    m = result["metrics"]
    lines = [
        "=" * 78,
        "EVALUATION COMPARISON REPORT (Paired Bootstrap Resampling)",
        "=" * 78,
        f"Dataset:  {result.get('dataset')}@{result.get('dataset_revision')}",
        f"Samples:  {result.get('samples')} rows",
        "-" * 78,
        f"Overlap F1:       {m['baseline_f1']:.4f} -> {m['candidate_f1']:.4f} "
        f"(Δ {m['delta_f1']:+.4f}, 95% CI: [{m['ci_95'][0]:+.4f}, {m['ci_95'][1]:+.4f}])",
        f"Exact F1:         {m['exact_baseline_f1']:.4f} -> {m['exact_candidate_f1']:.4f} "
        f"(Δ {m['exact_delta_f1']:+.4f}, "
        f"95% CI: [{m['exact_ci_95'][0]:+.4f}, {m['exact_ci_95'][1]:+.4f}])",
        f"Precision Δ:      {m['delta_precision']:+.4f}",
        f"Recall Δ:         {m['delta_recall']:+.4f}",
        f"Macro F1 Δ:       {m['macro_f1_delta']:+.4f}",
        "-" * 78,
        "CAUSAL ERROR SHIFTS (Negative Δ = Improvement):",
    ]
    for cat, data in result["error_categories"].items():
        lines.append(
            f"  {cat:<23}: {data['baseline']:>5} -> {data['candidate']:>5} (Δ {data['delta']:+d})"
        )

    lines.append("-" * 78)
    lines.append("PER-ENTITY SHIFTS:")
    lines.append(
        f"  {'Entity':<16} | {'Base F1':<7} | {'Cand F1':<7} | {'Δ F1':<7} | "
        f"{'Δ TP':<5} | {'Δ FP':<5} | {'Δ FN':<5}"
    )
    lines.append("  " + "-" * 74)
    for et, sh in sorted(result["per_entity"].items()):
        lines.append(
            f"  {et:<16} | {sh['baseline_f1']:.4f}  | {sh['candidate_f1']:.4f}  | "
            f"{sh['delta_f1']:+.4f} | {sh['delta_tp']:+5d} | {sh['delta_fp']:+5d} | "
            f"{sh['delta_fn']:+5d}"
        )
    lines.append("=" * 78)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Statistically compare two pseudonymize evaluation artifacts."
    )
    parser.add_argument("baseline", type=Path, help="Path to baseline evaluation JSON artifact.")
    parser.add_argument("candidate", type=Path, help="Path to candidate evaluation JSON artifact.")
    parser.add_argument(
        "--rounds",
        type=int,
        default=1000,
        help="Number of bootstrap resample rounds (default: 1000).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Pseudo-random generator seed for reproducible sampling (default: 42).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path to write comparison record as JSON.",
    )
    args = parser.parse_args()

    base_data = json.loads(args.baseline.read_text(encoding="utf-8"))
    cand_data = json.loads(args.candidate.read_text(encoding="utf-8"))

    try:
        comparison = compare_results(
            base_data, cand_data, num_resamples=args.rounds, seed=args.seed
        )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    report = format_comparison(comparison)
    print(report)

    if args.output is not None:
        args.output.write_text(
            json.dumps(comparison, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
