"""Automated Quality Release Gate for 1.34.0 milestone.

Evaluates candidate models and versions against 5 strict pre-release criteria:
1. Pinned input hashes (model, config, dataset revision).
2. Paired 95% bootstrap F1-delta confidence interval.
3. Strict precision protection (no statistically clear regression).
4. Zero recall regression for high-risk identifiers and credentials.
5. Independent external-family generalization proof (PIIMB).
"""

from __future__ import annotations

import argparse
import json
import logging
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from benchmarks.compare_quality import compare_results
except ImportError:
    from compare_quality import compare_results  # type: ignore[import-not-found,no-redef]

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("quality_gate")

HIGH_RISK_ENTITY_TYPES = frozenset(
    {"PAYMENT_CARD", "IBAN", "NATIONAL_ID", "TAX_ID", "URL_CREDENTIAL", "EMAIL", "PHONE"}
)


@dataclass(frozen=True)
class QualityGateCriteriaResult:
    """Evaluation result for an individual quality gate rule."""

    criterion_name: str
    passed: bool
    details: dict[str, Any]
    failure_reason: str | None = None


@dataclass(frozen=True)
class QualityGateReport:
    """Comprehensive release gate report."""

    passed: bool
    recommendation: str  # "SHIP" | "REJECT"
    criteria_results: dict[str, QualityGateCriteriaResult]
    summary_reasons: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "recommendation": self.recommendation,
            "summary_reasons": self.summary_reasons,
            "criteria": {
                name: {
                    "passed": res.passed,
                    "details": res.details,
                    "failure_reason": res.failure_reason,
                }
                for name, res in self.criteria_results.items()
            },
        }


def evaluate_quality_gate(
    baseline_record: dict[str, Any],
    candidate_record: dict[str, Any],
    external_eval_record: dict[str, Any] | None = None,
    precision_tolerance: float = 0.005,
    critical_recall_tolerance: float = 0.001,
    external_f1_floor: float = 0.70,
    num_resamples: int = 500,
) -> QualityGateReport:
    """Evaluate candidate against all five quality gate criteria."""
    results: dict[str, QualityGateCriteriaResult] = {}
    failure_reasons: list[str] = []

    # 1. Pinned Input Hashes & Provenance
    base_rev = baseline_record.get("dataset_revision")
    cand_rev = candidate_record.get("dataset_revision")
    cand_hashes = candidate_record.get("model_sha256", {})

    provenance_ok = (
        bool(cand_rev)
        and (base_rev == cand_rev or base_rev is None)
        and (bool(cand_hashes) or not candidate_record.get("use_ml", True))
    )

    if not provenance_ok:
        reason = "Candidate lacks pinned immutable dataset revision or model hashes."
        failure_reasons.append(reason)
        results["pinned_provenance"] = QualityGateCriteriaResult(
            criterion_name="pinned_provenance",
            passed=False,
            details={
                "baseline_revision": base_rev,
                "candidate_revision": cand_rev,
                "candidate_hashes": cand_hashes,
            },
            failure_reason=reason,
        )
        return QualityGateReport(
            passed=False,
            recommendation="REJECT",
            criteria_results=results,
            summary_reasons=failure_reasons,
        )

    results["pinned_provenance"] = QualityGateCriteriaResult(
        criterion_name="pinned_provenance",
        passed=True,
        details={
            "dataset_revision": cand_rev,
            "model_hashes_verified": bool(cand_hashes),
        },
    )

    # 2. Statistical Paired Bootstrap Comparison
    try:
        comparison = compare_results(baseline_record, candidate_record, num_resamples=num_resamples)
    except ValueError as err:
        reason = f"Evaluation compatibility failure: {err}"
        failure_reasons.append(reason)
        results["paired_f1_delta"] = QualityGateCriteriaResult(
            criterion_name="paired_f1_delta",
            passed=False,
            details={"error": str(err)},
            failure_reason=reason,
        )
        return QualityGateReport(
            passed=False,
            recommendation="REJECT",
            criteria_results=results,
            summary_reasons=failure_reasons,
        )

    delta_f1 = comparison["metrics"]["delta_f1"]
    ci_95 = comparison["metrics"]["ci_95"]
    lower_ci = ci_95[0]

    # Rule: F1 delta must be non-negative within uncertainty bounds
    f1_ok = delta_f1 >= -0.002 and lower_ci >= -0.01
    if not f1_ok:
        reason = (
            f"Primary strict F1 delta ({delta_f1:+.4f}, 95% CI: {ci_95}) "
            "fails non-regression threshold."
        )
        failure_reasons.append(reason)
        results["paired_f1_delta"] = QualityGateCriteriaResult(
            criterion_name="paired_f1_delta",
            passed=False,
            details={"delta_f1": delta_f1, "ci_95": ci_95},
            failure_reason=reason,
        )
    else:
        results["paired_f1_delta"] = QualityGateCriteriaResult(
            criterion_name="paired_f1_delta",
            passed=True,
            details={"delta_f1": delta_f1, "ci_95": ci_95},
        )

    # 3. Precision Protection
    base_p = baseline_record.get("metrics", {}).get("precision", 0.0)
    cand_p = candidate_record.get("metrics", {}).get("precision", 0.0)
    delta_p = cand_p - base_p
    precision_ok = delta_p >= -precision_tolerance

    if not precision_ok:
        reason = (
            f"Precision regressed by {delta_p:+.4f} (baseline: {base_p:.4f}, "
            f"candidate: {cand_p:.4f}), exceeding tolerance {precision_tolerance}."
        )
        failure_reasons.append(reason)
        results["precision_protection"] = QualityGateCriteriaResult(
            criterion_name="precision_protection",
            passed=False,
            details={
                "baseline_precision": base_p,
                "candidate_precision": cand_p,
                "delta_precision": delta_p,
                "tolerance": precision_tolerance,
            },
            failure_reason=reason,
        )
    else:
        results["precision_protection"] = QualityGateCriteriaResult(
            criterion_name="precision_protection",
            passed=True,
            details={
                "baseline_precision": base_p,
                "candidate_precision": cand_p,
                "delta_precision": delta_p,
            },
        )

    # 4. Critical Identifier & Secret Recall Floor
    base_per_entity = baseline_record.get("per_entity", {})
    cand_per_entity = candidate_record.get("per_entity", {})
    critical_regressions: list[dict[str, Any]] = []
    missing_critical_evidence: list[str] = []
    checked_entities: list[str] = []

    for ent in sorted(HIGH_RISK_ENTITY_TYPES):
        if ent in base_per_entity:
            b_et = base_per_entity[ent]
            c_et = cand_per_entity.get(ent, {})
            b_tp = b_et.get("true_positives")
            b_fn = b_et.get("false_negatives")
            c_tp = c_et.get("true_positives")
            c_fn = c_et.get("false_negatives")
            counts = (b_tp, b_fn, c_tp, c_fn)
            if not all(isinstance(n, int) and not isinstance(n, bool) and n >= 0 for n in counts):
                missing_critical_evidence.append(ent)
                continue
            if b_tp + b_fn != c_tp + c_fn:
                missing_critical_evidence.append(ent)
                continue
            if b_tp + b_fn == 0:
                continue
            checked_entities.append(ent)

            b_rec = b_tp / (b_tp + b_fn) if (b_tp + b_fn) > 0 else 1.0
            c_rec = c_tp / (c_tp + c_fn) if (c_tp + c_fn) > 0 else 1.0
            delta_rec = c_rec - b_rec

            if delta_rec < -critical_recall_tolerance:
                critical_regressions.append(
                    {
                        "entity_type": ent,
                        "baseline_recall": b_rec,
                        "candidate_recall": c_rec,
                        "delta_recall": delta_rec,
                    }
                )

    critical_ok = (
        not critical_regressions and not missing_critical_evidence and bool(checked_entities)
    )
    if not critical_ok:
        if missing_critical_evidence or not checked_entities:
            reason = "Critical identifier recall evidence is missing, invalid or incomparable."
        else:
            reason = (
                f"Recall regressed for {len(critical_regressions)} high-risk identifiers: "
                f"{[r['entity_type'] for r in critical_regressions]}"
            )
        failure_reasons.append(reason)
        results["critical_entities_floor"] = QualityGateCriteriaResult(
            criterion_name="critical_entities_floor",
            passed=False,
            details={
                "regressed_entities": critical_regressions,
                "missing_or_incomparable_entities": missing_critical_evidence,
            },
            failure_reason=reason,
        )
    else:
        results["critical_entities_floor"] = QualityGateCriteriaResult(
            criterion_name="critical_entities_floor",
            passed=True,
            details={
                "protected_entities_checked": checked_entities,
                "unrepresented_entities": sorted(HIGH_RISK_ENTITY_TYPES - set(checked_entities)),
            },
        )

    # 5. Independent External Generalization Track (PIIMB)
    if external_eval_record is not None:
        ext_micro = external_eval_record.get("character_micro_metrics", {})
        ext_f1 = ext_micro.get("f1") if isinstance(ext_micro, dict) else None
        valid_score = (
            isinstance(ext_f1, (int, float))
            and not isinstance(ext_f1, bool)
            and math.isfinite(ext_f1)
            and 0 <= ext_f1 <= 1
        )
        ext_ok = valid_score and isinstance(ext_f1, (int, float)) and ext_f1 >= external_f1_floor
        if not ext_ok:
            reason = (
                "External benchmark character F1 is missing, invalid or below the required floor."
            )
            failure_reasons.append(reason)
            results["external_generalization"] = QualityGateCriteriaResult(
                criterion_name="external_generalization",
                passed=False,
                details={
                    "external_f1": ext_f1 if valid_score else None,
                    "required_floor": external_f1_floor,
                },
                failure_reason=reason,
            )
        else:
            results["external_generalization"] = QualityGateCriteriaResult(
                criterion_name="external_generalization",
                passed=True,
                details={
                    "external_f1": ext_f1 if valid_score else None,
                    "required_floor": external_f1_floor,
                },
            )
    else:
        reason = "Independent external generalization evidence is required for shipment."
        failure_reasons.append(reason)
        results["external_generalization"] = QualityGateCriteriaResult(
            criterion_name="external_generalization",
            passed=False,
            details={"status": "not_evaluated_in_current_run"},
            failure_reason=reason,
        )

    all_passed = all(r.passed for r in results.values())
    recommendation = "SHIP" if all_passed else "REJECT"

    return QualityGateReport(
        passed=all_passed,
        recommendation=recommendation,
        criteria_results=results,
        summary_reasons=failure_reasons,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate candidate against 1.34.0 Quality Gate.")
    parser.add_argument(
        "--baseline",
        type=Path,
        default=Path("benchmarks/results/1.26.0_ai4privacy_validation_1000.json"),
        help="Path to frozen baseline artifact JSON.",
    )
    parser.add_argument(
        "--candidate",
        type=Path,
        required=True,
        help="Path to candidate artifact JSON.",
    )
    parser.add_argument(
        "--external",
        type=Path,
        default=None,
        help="External generalization artifact JSON (PIIMB), required for a passing gate.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("benchmarks/results/1.34.0_quality_gate_report.json"),
        help="Path to write gate report JSON.",
    )
    args = parser.parse_args()

    baseline_data = json.loads(args.baseline.read_text(encoding="utf-8"))
    candidate_data = json.loads(args.candidate.read_text(encoding="utf-8"))
    external_data = None
    if args.external is not None:
        external_data = json.loads(args.external.read_text(encoding="utf-8"))

    report = evaluate_quality_gate(
        baseline_record=baseline_data,
        candidate_record=candidate_data,
        external_eval_record=external_data,
    )

    print("\n" + "=" * 78)
    print("1.34.0 QUALITY RELEASE GATE REPORT")
    print("=" * 78)
    print(f"Overall Gate Status: {'PASSED' if report.passed else 'FAILED'}")
    print(f"Recommendation:      {report.recommendation}")
    print("-" * 78)
    for name, crit in report.criteria_results.items():
        status = "PASSED" if crit.passed else "FAILED"
        print(f"  [{status}] {name}")
        if not crit.passed and crit.failure_reason:
            print(f"         Reason: {crit.failure_reason}")
    print("=" * 78)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report.to_dict(), indent=2) + "\n", encoding="utf-8")
        logger.info(f"Saved quality gate report to {args.output}")

    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
