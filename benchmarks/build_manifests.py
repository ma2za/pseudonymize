"""Build immutable grouped development, calibration, and test manifests.

Groups documents from the pinned AI4Privacy training split by normalized
value-masked template so that identical form letters and near-duplicate templates
never cross partition boundaries. Stores only hashes and identifiers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
from pathlib import Path
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("build_manifests")

DATASET_NAME = "ai4privacy/pii-masking-openpii-1.5m"
DEFAULT_REVISION = "a785eb528e28be2693c3718a27e066970de5dadb"


def compute_template(text: str, masks: list[dict[str, Any]]) -> str:
    """Replace annotated spans with <LABEL> to form a structural template."""
    sorted_masks = sorted(masks, key=lambda m: (m["start"], m["end"]), reverse=True)
    chars = list(text)
    for mask in sorted_masks:
        s = mask["start"]
        e = mask["end"]
        label = mask.get("label", "MASK")
        if 0 <= s <= e <= len(chars):
            chars[s:e] = list(f"<{label}>")
    return "".join(chars)


def compute_template_hash(template: str) -> str:
    """Compute a deterministic SHA-256 hash of the normalized template."""
    normalized = " ".join(template.split()).lower()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def partition_groups(
    rows: list[dict[str, Any]],
) -> tuple[dict[str, list[str]], dict[str, int]]:
    """Group rows by template hash and partition deterministically across splits."""
    groups: dict[str, list[str]] = {}
    for r in rows:
        text = r["source_text"]
        masks = r.get("privacy_mask", [])
        row_h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        tpl = compute_template(text, masks)
        tpl_h = compute_template_hash(tpl)
        if tpl_h not in groups:
            groups[tpl_h] = []
        groups[tpl_h].append(row_h)

    partitions: dict[str, list[str]] = {
        "development": [],
        "calibration": [],
        "internal_test": [],
    }
    group_counts: dict[str, int] = {
        "development": 0,
        "calibration": 0,
        "internal_test": 0,
    }

    # Deterministic assignment using template hash prefix
    for tpl_h, row_list in groups.items():
        bucket = int(tpl_h[:8], 16) % 100
        if bucket < 60:
            target = "development"
        elif bucket < 80:
            target = "calibration"
        else:
            target = "internal_test"

        partitions[target].extend(row_list)
        group_counts[target] += 1

    return partitions, group_counts


def write_manifest(
    output_dir: Path,
    split_name: str,
    row_hashes: list[str],
    group_count: int,
    dataset_name: str,
    dataset_revision: str,
) -> Path:
    """Write sanitized manifest record with zero raw text."""
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / f"{split_name}_manifest.json"
    data = {
        "split_name": split_name,
        "dataset": dataset_name,
        "dataset_revision": dataset_revision,
        "template_groups": group_count,
        "total_rows": len(row_hashes),
        "row_hashes": sorted(set(row_hashes)),
    }
    manifest_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build grouped development, calibration, and test manifests."
    )
    parser.add_argument("--samples", type=int, default=5000, help="Number of training samples.")
    parser.add_argument(
        "--dataset-revision",
        default=DEFAULT_REVISION,
        help="Pinned immutable dataset revision.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("benchmarks/manifests"),
        help="Directory to write manifests.",
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Optional local JSONL file to build manifests from.",
    )
    args = parser.parse_args()

    if args.file is not None:
        rows = []
        with open(args.file, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rows.append(json.loads(line))
                if len(rows) >= args.samples:
                    break
    else:
        try:
            from datasets import load_dataset
        except ImportError:
            logger.error("datasets library required. Run with: uv run --with datasets ...")
            return 1

        logger.info(
            f"Loading {DATASET_NAME}@{args.dataset_revision} (train split, English subset)..."
        )
        ds = load_dataset(
            DATASET_NAME, split="train", streaming=True, revision=args.dataset_revision
        )
        rows = []
        for r in ds:
            if r.get("language") == "en":
                rows.append(r)
            if len(rows) >= args.samples:
                break

    logger.info(f"Loaded {len(rows)} samples. Partitioning by structural template...")
    partitions, group_counts = partition_groups(rows)

    for split_name in ("development", "calibration", "internal_test"):
        path = write_manifest(
            args.output_dir,
            split_name,
            partitions[split_name],
            group_counts[split_name],
            DATASET_NAME if args.file is None else str(args.file),
            args.dataset_revision,
        )
        logger.info(
            f"Wrote {split_name} manifest: {len(partitions[split_name])} rows across "
            f"{group_counts[split_name]} template groups -> {path}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
