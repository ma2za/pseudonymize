"""External generalization benchmark runner (PIIMB / multi-source).

Evaluates pseudonymize against an independent, multi-source external benchmark
(such as PIIMB) using label-agnostic character-level masking metrics.
Never averages incompatible strict-typed metrics into this headline number.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import platform
import shutil
import subprocess
import sys
import time
from dataclasses import replace
from pathlib import Path
from typing import Any

from pseudonymize import Pseudonymizer
from pseudonymize.backends.ml.onnx import LocalONNXPIIBackend
from pseudonymize.detectors import DEFAULT_DETECTORS, Detector
from pseudonymize.detectors.checksums import AlgorithmicChecksumDetector
from pseudonymize.detectors.iban import IbanDetector
from pseudonymize.detectors.payment_card import PaymentCardDetector

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("evaluate_external")

DEFAULT_EXTERNAL_DATASET = "piimb/pii-masking-benchmark"
SHUFFLE_SEED = 42


def _sha256(path: Path | str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def _git_commit() -> str | None:
    git_bin = shutil.which("git")
    if not git_bin:
        return os.environ.get("GITHUB_SHA")
    try:
        completed = subprocess.run(  # noqa: S603
            [git_bin, "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode == 0:
            commit = completed.stdout.strip()
            if commit:
                return commit
    except Exception:  # noqa: S110
        pass
    return os.environ.get("GITHUB_SHA")


def load_local_jsonl(file_path: Path) -> list[dict[str, Any]]:
    with open(file_path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def extract_spans_from_row(row: dict[str, Any]) -> tuple[str, list[tuple[int, int]]]:
    """Extract source text and ground truth character spans from varied dataset formats."""
    # Format A: source_text + privacy_mask (e.g. AI4Privacy / standardized)
    if "source_text" in row:
        text = str(row["source_text"])
        masks = row.get("privacy_mask", [])
        spans = [(m["start"], m["end"]) for m in masks if "start" in m and "end" in m]
        return text, spans

    # Format B: text + spans
    if "text" in row:
        text = str(row["text"])
        spans_raw = row.get("spans", [])
        spans = [(s["start"], s["end"]) for s in spans_raw if "start" in s and "end" in s]
        return text, spans

    # Format C: tokens + ner_tags / spans (e.g. token-classification PIIMB format)
    if "tokens" in row:
        tokens = row["tokens"]
        text = " ".join(tokens)
        spans_raw = row.get("spans", [])
        if spans_raw:
            spans = [(s["start"], s["end"]) for s in spans_raw if "start" in s and "end" in s]
            return text, spans

        # Compute spans from BIO tags if tokens and ner_tags are provided
        ner_tags = row.get("ner_tags", [])
        spans = []
        current_start: int | None = None
        current_offset = 0

        for token, tag in zip(tokens, ner_tags, strict=False):
            token_start = current_offset
            token_end = current_offset + len(token)
            current_offset = token_end + 1  # accounts for space

            # If tag is non-zero (assuming 0 is 'O')
            if tag != 0:
                if current_start is None:
                    current_start = token_start
            else:
                if current_start is not None:
                    spans.append((current_start, token_start - 1))
                    current_start = None

        if current_start is not None:
            spans.append((current_start, len(text)))

        return text, spans

    raise ValueError(f"Unsupported row schema: keys={list(row.keys())}")


def evaluate_external(
    num_samples: int = 1000,
    dataset_name: str = DEFAULT_EXTERNAL_DATASET,
    dataset_revision: str | None = None,
    split: str = "test",
    file_path: Path | None = None,
    use_ml: bool = True,
    allow_unverified_checksums: bool = False,
    explain: bool = False,
    samples: int | None = None,
) -> dict[str, Any]:
    """Evaluate pseudonymize against an external multi-source benchmark."""
    if samples is not None:
        num_samples = samples
    if file_path is not None:
        logger.info(f"Loading local external dataset from {file_path}...")
        ds = load_local_jsonl(file_path)
    else:
        try:
            from datasets import load_dataset
        except ImportError:
            print("Error: 'datasets' library not found.")
            print("Run: uv run --with datasets python benchmarks/evaluate_external.py")
            sys.exit(1)

        logger.info(f"Loading {dataset_name}@{dataset_revision or 'latest'} ({split} split)...")
        ds = load_dataset(
            dataset_name,
            split=split,
            streaming=True,
            revision=dataset_revision,
        ).shuffle(seed=SHUFFLE_SEED)

    from pseudonymize.memory.bloom import BloomFilter

    bloom_path = Path("data/gazetteer/common_words.txt")
    bloom_filter = None
    if bloom_path.exists():
        with open(bloom_path, encoding="utf-8") as f:
            bloom_filter = BloomFilter.from_words(
                [line.strip().lower() for line in f if line.strip()]
            )

    detectors: tuple[Detector, ...] = tuple(
        replace(detector, _accept_unverified=True)
        if allow_unverified_checksums
        and isinstance(detector, (AlgorithmicChecksumDetector, IbanDetector, PaymentCardDetector))
        else detector
        for detector in DEFAULT_DETECTORS
    )
    engine = Pseudonymizer(detectors=detectors, bloom_filter=bloom_filter)

    model_hashes: dict[str, str] = {}
    if use_ml:
        CACHE_DIR = Path(".cache/pseudonymize-tests/models/multilang-pii-ner-ml")
        onnx_model_path = CACHE_DIR / "model_int8.onnx"
        tokenizer_path = CACHE_DIR / "tokenizer.json"
        config_path = CACHE_DIR / "config.json"

        if not onnx_model_path.exists() or not tokenizer_path.exists() or not config_path.exists():
            logger.error(f"ML artifacts not found in {CACHE_DIR}.")
            logger.error("Please run 'uv run pytest tests/unit/backends/test_onnx.py' first.")
            sys.exit(1)

        backend = LocalONNXPIIBackend(
            model_path=onnx_model_path,
            tokenizer_path=tokenizer_path,
            config_path=config_path,
        )
        model_hashes = {
            "model": _sha256(onnx_model_path),
            "tokenizer": _sha256(tokenizer_path),
            "config": _sha256(config_path),
        }
        engine = Pseudonymizer(backends=[*engine.backends, backend], bloom_filter=bloom_filter)

    total_true_chars = 0
    total_detected_chars = 0
    total_masked_chars = 0

    doc_precisions: list[float] = []
    doc_recalls: list[float] = []
    doc_f1s: list[float] = []

    # Per source breakdown (e.g. finer-139, ai4privacy, isotonic, etc.)
    source_stats: dict[str, dict[str, int]] = {}

    count = 0
    start_time = time.time()

    for row in ds:
        text, truth_spans = extract_spans_from_row(row)
        source_name = str(row.get("source", row.get("dataset", "external_unknown")))

        result = engine.process_with_report(text)
        det_spans = [(d.start, d.end) for d in result.detections]

        true_char_indices: set[int] = set()
        for s, e in truth_spans:
            true_char_indices.update(range(max(0, s), min(len(text), e)))

        det_char_indices: set[int] = set()
        for s, e in det_spans:
            det_char_indices.update(range(max(0, s), min(len(text), e)))

        masked_chars = len(true_char_indices & det_char_indices)
        num_true = len(true_char_indices)
        num_det = len(det_char_indices)

        total_true_chars += num_true
        total_detected_chars += num_det
        total_masked_chars += masked_chars

        # Per document metrics
        p = masked_chars / num_det if num_det > 0 else (1.0 if num_true == 0 else 0.0)
        r = masked_chars / num_true if num_true > 0 else (1.0 if num_det == 0 else 0.0)
        f1 = (2 * p * r) / (p + r) if (p + r) > 0 else 0.0

        doc_precisions.append(p)
        doc_recalls.append(r)
        doc_f1s.append(f1)

        if source_name not in source_stats:
            source_stats[source_name] = {
                "true_chars": 0,
                "detected_chars": 0,
                "masked_chars": 0,
                "docs": 0,
            }
        source_stats[source_name]["true_chars"] += num_true
        source_stats[source_name]["detected_chars"] += num_det
        source_stats[source_name]["masked_chars"] += masked_chars
        source_stats[source_name]["docs"] += 1

        if explain and (r < 0.5 or p < 0.5):
            logger.info(
                f"Low-coverage doc ({source_name}): Recall={r:.2f}, Precision={p:.2f} "
                f"({len(text)} chars)"
            )

        count += 1
        if count >= num_samples:
            break

    duration = time.time() - start_time

    micro_precision = total_masked_chars / total_detected_chars if total_detected_chars > 0 else 0.0
    micro_recall = total_masked_chars / total_true_chars if total_true_chars > 0 else 0.0
    micro_f1 = (
        (2 * micro_precision * micro_recall) / (micro_precision + micro_recall)
        if (micro_precision + micro_recall) > 0
        else 0.0
    )

    macro_precision = sum(doc_precisions) / len(doc_precisions) if doc_precisions else 0.0
    macro_recall = sum(doc_recalls) / len(doc_recalls) if doc_recalls else 0.0
    macro_f1 = sum(doc_f1s) / len(doc_f1s) if doc_f1s else 0.0

    # Per source micro metrics
    per_source_report: dict[str, dict[str, Any]] = {}
    for s_name, s_data in source_stats.items():
        s_tc = s_data["true_chars"]
        s_dc = s_data["detected_chars"]
        s_mc = s_data["masked_chars"]
        s_p = s_mc / s_dc if s_dc > 0 else 0.0
        s_r = s_mc / s_tc if s_tc > 0 else 0.0
        s_f1 = (2 * s_p * s_r) / (s_p + s_r) if (s_p + s_r) > 0 else 0.0
        per_source_report[s_name] = {
            "documents": s_data["docs"],
            "micro_precision": s_p,
            "micro_recall": s_r,
            "micro_f1": s_f1,
            "true_chars": s_tc,
            "detected_chars": s_dc,
            "masked_chars": s_mc,
        }

    return {
        "benchmark": "external_generalization_track",
        "dataset": dataset_name if file_path is None else None,
        "dataset_revision": dataset_revision,
        "split": split,
        "file": str(file_path) if file_path is not None else None,
        "file_sha256": _sha256(file_path) if file_path is not None else None,
        "git_commit": _git_commit(),
        "model_sha256": model_hashes,
        "python": sys.version,
        "platform": platform.platform(),
        "samples": count,
        "duration_seconds": duration,
        "character_micro_metrics": {
            "precision": micro_precision,
            "recall": micro_recall,
            "f1": micro_f1,
            "true_chars": total_true_chars,
            "detected_chars": total_detected_chars,
            "masked_chars": total_masked_chars,
        },
        "character_macro_metrics": {
            "precision": macro_precision,
            "recall": macro_recall,
            "f1": macro_f1,
        },
        "sources": per_source_report,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate pseudonymize on external generalization benchmark (PIIMB)."
    )
    parser.add_argument("--samples", type=int, default=1000, help="Number of samples to evaluate.")
    parser.add_argument(
        "--dataset",
        default=DEFAULT_EXTERNAL_DATASET,
        help="External dataset name (default: piimb/pii-masking-benchmark).",
    )
    parser.add_argument(
        "--dataset-revision",
        default=None,
        help="Immutable dataset revision hash.",
    )
    parser.add_argument(
        "--split",
        default="test",
        help="Dataset split to evaluate.",
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="Optional local JSONL file for offline or test evaluation.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("benchmarks/results/external_generalization.json"),
        help="Output path for evaluation JSON.",
    )
    parser.add_argument(
        "--no-ml",
        action="store_true",
        help="Run without ONNX ML backend (rules only).",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Log low-coverage documents for causal analysis.",
    )
    args = parser.parse_args()

    results = evaluate_external(
        num_samples=args.samples,
        dataset_name=args.dataset,
        dataset_revision=args.dataset_revision,
        split=args.split,
        file_path=args.file,
        use_ml=not args.no_ml,
        explain=args.explain,
    )

    print("\n" + "=" * 78)
    print("EXTERNAL GENERALIZATION TRACK (LABEL-AGNOSTIC CHARACTER METRICS)")
    print("=" * 78)
    micro = results["character_micro_metrics"]
    macro = results["character_macro_metrics"]
    print(f"Evaluated Samples: {results['samples']}")
    print(
        f"Micro Character:   Precision={micro['precision']:.4f}, Recall={micro['recall']:.4f}, "
        f"F1={micro['f1']:.4f}"
    )
    print(
        f"                   ({micro['masked_chars']} / {micro['true_chars']} sensitive "
        f"chars masked, {micro['detected_chars']} detected)"
    )
    print(
        f"Macro Document:    Precision={macro['precision']:.4f}, Recall={macro['recall']:.4f}, "
        f"F1={macro['f1']:.4f}"
    )
    print("-" * 78)
    print("Per-Source Breakdown:")
    for s_name, s_data in results.get("sources", {}).items():
        print(
            f"  {s_name:<25} | Docs: {s_data['documents']:<4} | "
            f"P={s_data['micro_precision']:.4f} | R={s_data['micro_recall']:.4f} | "
            f"F1={s_data['micro_f1']:.4f}"
        )
    print("=" * 78)

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
        logger.info(f"Saved external generalization results to {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
