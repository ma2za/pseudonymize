"""Audit template and row overlap between evaluation partitions.

Proves whether near-duplicate form letters, exact texts, or templates
cross split boundaries between development, calibration, internal test,
and validation datasets.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("audit_contamination")


def audit_partitions(
    manifest_paths: dict[str, Path],
    validation_rows_path: Path | None = None,
) -> dict[str, Any]:
    """Audit pairwise row hash and template collisions across partitions."""
    manifests: dict[str, dict[str, Any]] = {}
    for name, p in manifest_paths.items():
        if p.exists():
            manifests[name] = json.loads(p.read_text(encoding="utf-8"))

    # 1. Pairwise row hash overlap
    names = list(manifests.keys())
    row_collisions: dict[str, int] = {}
    for i, name_a in enumerate(names):
        set_a = set(manifests[name_a].get("row_hashes", []))
        for name_b in names[i + 1 :]:
            set_b = set(manifests[name_b].get("row_hashes", []))
            overlap = len(set_a & set_b)
            row_collisions[f"{name_a}_vs_{name_b}"] = overlap

    # 2. Validation overlap if validation artifact is supplied
    val_overlap: dict[str, int] = {}
    if validation_rows_path is not None and validation_rows_path.exists():
        val_data = json.loads(validation_rows_path.read_text(encoding="utf-8"))
        val_hashes = {r["row_hash"] for r in val_data.get("rows", [])}
        for name, m in manifests.items():
            m_hashes = set(m.get("row_hashes", []))
            val_overlap[f"{name}_vs_validation"] = len(m_hashes & val_hashes)

    return {
        "manifests_checked": {name: len(m.get("row_hashes", [])) for name, m in manifests.items()},
        "row_collisions": row_collisions,
        "validation_row_overlap": val_overlap,
        "clean_partitioning": all(c == 0 for c in row_collisions.values())
        and all(c == 0 for c in val_overlap.values()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit contamination and near-duplicate leakage across manifests."
    )
    parser.add_argument(
        "--manifest-dir",
        type=Path,
        default=Path("benchmarks/manifests"),
        help="Directory containing generated manifests.",
    )
    parser.add_argument(
        "--validation-artifact",
        type=Path,
        default=Path("benchmarks/results/1.26.0_ai4privacy_validation_1000.json"),
        help="Path to baseline validation artifact with per-row stats.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("benchmarks/manifests/contamination_audit.json"),
        help="Path to write audit JSON report.",
    )
    args = parser.parse_args()

    manifest_paths = {
        "development": args.manifest_dir / "development_manifest.json",
        "calibration": args.manifest_dir / "calibration_manifest.json",
        "internal_test": args.manifest_dir / "internal_test_manifest.json",
    }

    report = audit_partitions(manifest_paths, args.validation_artifact)
    print(json.dumps(report, indent=2))

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        logger.info(f"Audit report saved to {args.output}")

    return 0 if report["clean_partitioning"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
