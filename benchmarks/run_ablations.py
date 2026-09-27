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

ABLATION_CONFIGS: dict[str, dict[str, Any]] = {
    "rules_only": {
        "description": "Rules only without ONNX ML backend",
        "kwargs": {"use_ml": False, "use_rules": True},
    },
    "ml_only": {
        "description": "ML only without rule detectors",
        "kwargs": {"use_ml": True, "use_rules": False},
    },
    "no_context_boost": {
        "description": "Disable ML context keyword triggers and threshold halving",
        "kwargs": {"use_ml": True, "enable_context_boost": False},
    },
    "no_runner_up": {
        "description": "Disable ML runner-up promotion when 'O' is predicted",
        "kwargs": {"use_ml": True, "enable_runner_up": False},
    },
    "no_confidence_remapping": {
        "description": "Disable piece-wise linear confidence calibration",
        "kwargs": {"use_ml": True, "enable_confidence_remapping": False},
    },
    "no_subword_repair": {
        "description": "Disable subword / zero-gap token continuation repair",
        "kwargs": {"use_ml": True, "enable_subword_repair": False},
    },
    "no_word_expansion": {
        "description": "Disable token-to-character word boundary expansion",
        "kwargs": {"use_ml": True, "enable_word_expansion": False},
    },
    "no_coreference": {
        "description": "Disable intra-document coreference graph tracking",
        "kwargs": {"use_ml": True, "enable_coreference": False},
    },
    "no_bloom_filter": {
        "description": "Disable gazetteer / bloom filter common word suppression",
        "kwargs": {"use_ml": True, "enable_bloom_filter": False},
    },
    "no_ensemble_merging": {
        "description": "Disable contiguous adjacent same-type ensemble span merging",
        "kwargs": {"use_ml": True, "enable_adjacent_merge": False},
    },
    "constrained_bio": {
        "description": "Evaluate constrained BIO transition decoding instead of legacy joining",
        "kwargs": {"use_ml": True, "decoder_mode": "constrained_bio"},
    },
    "temperature_scaled": {
        "description": "Evaluate temperature scaling (T=1.20) on raw logits",
        "kwargs": {"use_ml": True, "temperature": 1.20},
    },
    "span_agg_mean": {
        "description": "Evaluate mean token confidence span aggregation instead of max",
        "kwargs": {"use_ml": True, "span_aggregator": "mean"},
    },
    "span_agg_min": {
        "description": "Evaluate minimum token confidence span aggregation instead of max",
        "kwargs": {"use_ml": True, "span_aggregator": "min"},
    },
    "span_agg_geom": {
        "description": "Evaluate geometric mean token confidence span aggregation instead of max",
        "kwargs": {"use_ml": True, "span_aggregator": "geometric_mean"},
    },
}


def build_error_atlas(
    baseline_result: dict[str, Any],
    ablation_reports: dict[str, Any],
) -> dict[str, Any]:
    """Construct a ranked causal error atlas from baseline errors and ablation deltas."""
    base_errors = baseline_result.get("error_categories", {})
    sorted_error_categories = sorted(base_errors.items(), key=lambda item: item[1], reverse=True)
    total_errors = sum(base_errors.values())

    top_error_categories = [
        {
            "category": cat,
            "count": count,
            "share": count / total_errors if total_errors > 0 else 0.0,
        }
        for cat, count in sorted_error_categories[:3]
    ]

    # Rank entity vulnerabilities by total errors (FP + FN) in baseline
    entity_errors: dict[str, int] = {}
    per_entity = baseline_result.get("per_entity", {})
    for entity, metrics in per_entity.items():
        err_count = metrics.get("false_positives", 0) + metrics.get("false_negatives", 0)
        if err_count > 0:
            entity_errors[entity] = err_count

    sorted_entities = sorted(entity_errors.items(), key=lambda item: item[1], reverse=True)
    top_entity_vulnerabilities = [
        {"entity_type": ent, "total_errors": errs} for ent, errs in sorted_entities[:3]
    ]

    # Rank components by impact
    ranked_components = []
    for name, data in ablation_reports.items():
        ranked_components.append(
            {
                "ablation": name,
                "delta_f1": data["delta_f1"],
                "delta_exact_f1": data["delta_exact_f1"],
                "recoverable_fp": data.get("recoverable_fp", 0),
                "prevented_fn": data.get("prevented_fn", 0),
            }
        )
    ranked_components.sort(key=lambda x: abs(x["delta_f1"]), reverse=True)

    return {
        "total_baseline_errors": total_errors,
        "top_three_error_categories": top_error_categories,
        "top_three_entity_vulnerabilities": top_entity_vulnerabilities,
        "ranked_components_by_impact": ranked_components,
    }


def run_ablation_suite(
    file_path: Path | None = None,
    dataset_revision: str | None = None,
    samples: int = 200,
    manifest_path: Path | None = None,
    use_ml: bool = True,
    ablations: list[str] | None = None,
    num_resamples: int = 500,
) -> dict[str, Any]:
    """Execute the development ablation matrix on identical rows."""
    logger.info(f"--- Running Baseline (Rules + ML={use_ml}) on {samples} rows ---")
    base_result = evaluate(
        num_samples=samples,
        use_ml=use_ml,
        file_path=file_path,
        dataset_revision=dataset_revision,
        manifest_path=manifest_path,
    )

    ablation_reports: dict[str, Any] = {}

    to_run = ablations or list(ABLATION_CONFIGS.keys())
    for name in to_run:
        if name not in ABLATION_CONFIGS:
            logger.warning(f"Unknown ablation '{name}', skipping")
            continue

        cfg = ABLATION_CONFIGS[name]
        kwargs = dict(cfg["kwargs"])

        # If running without ML environment, skip ML-only or ML-dependent ablations
        if not use_ml and kwargs.get("use_ml", False):
            continue

        logger.info(f"--- Running Ablation: {name} ({cfg['description']}) ---")
        cand_result = evaluate(
            num_samples=samples,
            file_path=file_path,
            dataset_revision=dataset_revision,
            manifest_path=manifest_path,
            **kwargs,
        )

        comp = compare_results(base_result, cand_result, num_resamples=num_resamples, seed=42)

        base_counts = base_result.get("counts")
        base_fp = int(base_counts.get("false_positives", 0)) if isinstance(base_counts, dict) else 0
        base_fn = int(base_counts.get("false_negatives", 0)) if isinstance(base_counts, dict) else 0

        cand_counts = cand_result.get("counts")
        cand_fp = int(cand_counts.get("false_positives", 0)) if isinstance(cand_counts, dict) else 0
        cand_fn = int(cand_counts.get("false_negatives", 0)) if isinstance(cand_counts, dict) else 0

        ablation_reports[name] = {
            "description": cfg["description"],
            "delta_f1": comp["metrics"]["delta_f1"],
            "ci_95": comp["metrics"]["ci_95"],
            "delta_exact_f1": comp["metrics"]["exact_delta_f1"],
            "exact_ci_95": comp["metrics"]["exact_ci_95"],
            "recoverable_fp": max(0, base_fp - cand_fp),
            "prevented_fn": max(0, cand_fn - base_fn),
            "error_shifts": comp["error_categories"],
            "per_entity_shifts": comp["per_entity"],
        }

    error_atlas = build_error_atlas(base_result, ablation_reports)

    return {
        "samples": samples,
        "dataset_revision": dataset_revision,
        "baseline_metrics": base_result["metrics"],
        "baseline_exact": base_result["exact_metrics"],
        "baseline_errors": base_result["error_categories"],
        "ablations": ablation_reports,
        "error_atlas": error_atlas,
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
        "--no-ml",
        action="store_true",
        help="Run without ONNX ML backend (evaluates rules ablations only).",
    )
    parser.add_argument(
        "--ablations",
        type=str,
        default=None,
        help="Comma-separated list of ablation names to run.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("benchmarks/results/development_ablations.json"),
        help="Output path for ablation results JSON.",
    )
    args = parser.parse_args()

    selected = [a.strip() for a in args.ablations.split(",")] if args.ablations else None

    results = run_ablation_suite(
        file_path=args.file,
        dataset_revision=args.dataset_revision,
        samples=args.samples,
        manifest_path=args.manifest,
        use_ml=not args.no_ml,
        ablations=selected,
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
        print(f"  Recoverable FP: {data['recoverable_fp']} | Prevented FN: {data['prevented_fn']}")
        print("  Error Category Shifts:")
        for cat, shift in data["error_shifts"].items():
            print(
                f"    {cat:<21}: {shift['baseline']:>5} -> {shift['candidate']:>5} "
                f"(Δ {shift['delta']:+d})"
            )
    print("-" * 78)
    atlas = results.get("error_atlas", {})
    print("RANKED CAUSAL ERROR ATLAS")
    print("  Top Error Categories:")
    for cat in atlas.get("top_three_error_categories", []):
        print(f"    - {cat['category']}: {cat['count']} errors ({cat['share']:.1%})")
    print("  Top Entity Vulnerabilities:")
    for ent in atlas.get("top_three_entity_vulnerabilities", []):
        print(f"    - {ent['entity_type']}: {ent['total_errors']} errors")
    print("=" * 78)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        logger.info(f"Saved ablation results to {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
