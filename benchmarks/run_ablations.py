"""Development ablation matrix runner.

Evaluates component contributions on identical rows to measure recoverable
and harmful errors by entity and causal error category.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

from benchmarks.compare_quality import compare_results
from benchmarks.evaluate_quality import evaluate

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("run_ablations")


def run_ablation_suite(
    file_path: Path | None = None,
    dataset_revision: str | None = None,
    samples: int = 200,
    manifest_path: Path | None = None,
) -> dict[str, Any]:
    """Execute the development ablation matrix on identical rows."""
    logger.info(f"--- Running Baseline (Rules + ML) on {samples} rows ---")
    base_result = evaluate(
        num_samples=samples,
        use_ml=True,
        file_path=file_path,
        dataset_revision=dataset_revision,
        manifest_path=manifest_path,
    )

    logger.info(f"--- Running Rules-Only Ablation on {samples} rows ---")
    rules_only_result = evaluate(
        num_samples=samples,
        use_ml=False,
        file_path=file_path,
        dataset_revision=dataset_revision,
        manifest_path=manifest_path,
    )

    ablation_reports: dict[str, Any] = {}

    # Compare Rules-Only vs Baseline
    rules_comp = compare_results(base_result, rules_only_result, num_resamples=500, seed=42)
    ablation_reports["rules_only"] = {
        "description": "Rules only without ONNX ML backend",
        "delta_f1": rules_comp["metrics"]["delta_f1"],
        "ci_95": rules_comp["metrics"]["ci_95"],
        "delta_exact_f1": rules_comp["metrics"]["exact_delta_f1"],
        "exact_ci_95": rules_comp["metrics"]["exact_ci_95"],
        "error_shifts": rules_comp["error_categories"],
        "per_entity_shifts": rules_comp["per_entity"],
    }

    return {
        "samples": samples,
        "dataset_revision": dataset_revision,
        "baseline_metrics": base_result["metrics"],
        "baseline_exact": base_result["exact_metrics"],
        "baseline_errors": base_result["error_categories"],
        "ablations": ablation_reports,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run development ablation matrix on identical rows."
    )
    parser.add_argument("--samples", type=int, default=200, help="Number of samples to evaluate.")
    parser.add_argument(
        "--dataset-revision",
        default="a785eb528e28be2693c3718a27e066970de5dadb",
        help="Pinned immutable dataset revision.",
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Optional local JSONL file to evaluate.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Optional manifest file containing row hashes.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("benchmarks/results/development_ablations.json"),
        help="Output path for ablation results JSON.",
    )
    args = parser.parse_args()

    results = run_ablation_suite(
        file_path=args.file,
        dataset_revision=args.dataset_revision,
        samples=args.samples,
        manifest_path=args.manifest,
    )

    print("\n" + "=" * 78)
    print("DEVELOPMENT ABLATION MATRIX SUMMARY")
    print("=" * 78)
    print(f"Baseline F1:       {results['baseline_metrics']['f1']:.4f}")
    print(f"Baseline Exact F1: {results['baseline_exact']['f1']:.4f}")
    print(f"Baseline Errors:   {results['baseline_errors']}")
    print("-" * 78)
    for name, data in results["ablations"].items():
        print(f"Ablation: {name} ({data['description']})")
        print(f"  Δ Overlap F1: {data['delta_f1']:+.4f} (95% CI: {data['ci_95']})")
        print(f"  Δ Exact F1:   {data['delta_exact_f1']:+.4f} (95% CI: {data['exact_ci_95']})")
        print("  Error Category Shifts:")
        for cat, shift in data["error_shifts"].items():
            print(
                f"    {cat:<21}: {shift['baseline']:>5} -> {shift['candidate']:>5} "
                f"(Δ {shift['delta']:+d})"
            )
    print("=" * 78)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        logger.info(f"Saved ablation results to {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
