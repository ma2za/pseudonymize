import argparse
import contextlib
import hashlib
import json
import logging
import os
import platform
import shutil
import subprocess
import sys
import time
import typing
from dataclasses import replace
from importlib.metadata import version
from pathlib import Path

from pseudonymize.backends.base import invoke_backend
from pseudonymize.backends.ml.onnx import LocalONNXPIIBackend
from pseudonymize.detectors import DEFAULT_DETECTORS, Detector
from pseudonymize.detectors.checksums import AlgorithmicChecksumDetector
from pseudonymize.detectors.iban import IbanDetector
from pseudonymize.detectors.payment_card import PaymentCardDetector
from pseudonymize.document import ContentBlock, TextOffsetLocation
from pseudonymize.engine import Pseudonymizer
from pseudonymize.result import EntityType

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("evaluate_quality")
DATASET_NAME = "ai4privacy/pii-masking-openpii-1.5m"
SHUFFLE_SEED = 42

# We evaluate precision and recall against these specific AI4Privacy labels
# that map to the capabilities of pseudonymize's core detectors and ML backend.
SUPPORTED_LABELS = {
    # Core detectors mapped to OpenPII-1.5m labels
    "EMAIL",
    "TELEPHONENUM",
    "CREDITCARDNUMBER",
    "IBAN",
    "IPV4",
    "IPV6",
    "IP",
    "URL",
    "SOCIALNUM",
    "IDCARDNUM",
    "PASSPORTNUM",
    "TAXNUM",
    "DRIVERLICENSENUM",
    # ML Backend (DistilBERT ONNX) mapped to OpenPII-1.5m labels
    "GIVENNAME",
    "SURNAME",
    "MIDDLENAME",
    "ORGANISATION",
    "CITY",
    "STATE",
    "COUNTY",
    "STREET",
    "ZIPCODE",
}

# Corpus labels grouped by the entity type this package would report for them.
# Matching a detection to an annotation compares these, so that finding an email
# where the corpus annotated a surname is not scored as a hit.
_LABEL_TO_ENTITY: dict[str, EntityType] = {
    "EMAIL": EntityType.EMAIL,
    "TELEPHONENUM": EntityType.PHONE,
    "CREDITCARDNUMBER": EntityType.PAYMENT_CARD,
    "IBAN": EntityType.IBAN,
    "IPV4": EntityType.IP_ADDRESS,
    "IPV6": EntityType.IP_ADDRESS,
    "IP": EntityType.IP_ADDRESS,
    "URL": EntityType.URL_CREDENTIAL,
    "SOCIALNUM": EntityType.NATIONAL_ID,
    "IDCARDNUM": EntityType.NATIONAL_ID,
    "PASSPORTNUM": EntityType.NATIONAL_ID,
    "DRIVERLICENSENUM": EntityType.NATIONAL_ID,
    "TAXNUM": EntityType.TAX_ID,
    "GIVENNAME": EntityType.PERSON,
    "SURNAME": EntityType.PERSON,
    "MIDDLENAME": EntityType.PERSON,
    "ORGANISATION": EntityType.ORGANIZATION,
    "CITY": EntityType.LOCATION,
    "STATE": EntityType.LOCATION,
    "COUNTY": EntityType.LOCATION,
    "STREET": EntityType.LOCATION,
    "ZIPCODE": EntityType.LOCATION,
}


def _match(
    detections: list[tuple[int, int, EntityType]],
    truth: list[tuple[int, int, str]],
    strict_labels: bool,
) -> tuple[set[int], set[int]]:
    """Pair each detection with at most one annotation, and vice versa.

    Precision and recall are only meaningful when their numerator counts the
    same thing. Pairing one-to-one means a detection spanning two adjacent
    annotations, such as "John Smith" against separate GIVENNAME and SURNAME
    masks, is one hit and leaves the second annotation to be counted as a miss,
    rather than crediting a numerator of detections against a denominator of
    annotations.

    Candidate pairs are taken in descending order of overlap so that the closest
    fit wins when several spans compete for the same text.
    """
    candidates = []
    for detection_index, (d_start, d_end, entity_type) in enumerate(detections):
        for truth_index, (g_start, g_end, label) in enumerate(truth):
            overlap = min(d_end, g_end) - max(d_start, g_start)
            if overlap <= 0:
                continue
            if strict_labels and _LABEL_TO_ENTITY.get(label) is not entity_type:
                continue
            candidates.append((overlap, detection_index, truth_index))

    matched_detections: set[int] = set()
    matched_truth: set[int] = set()
    for _, detection_index, truth_index in sorted(candidates, reverse=True):
        if detection_index in matched_detections or truth_index in matched_truth:
            continue
        matched_detections.add(detection_index)
        matched_truth.add(truth_index)
    return matched_detections, matched_truth


def _match_exact(
    detections: list[tuple[int, int, EntityType]],
    truth: list[tuple[int, int, str]],
    strict_labels: bool,
) -> tuple[set[int], set[int]]:
    """Pair each detection with at most one annotation requiring exact boundary and label."""
    candidates = []
    for d_idx, (d_start, d_end, d_type) in enumerate(detections):
        for t_idx, (g_start, g_end, label) in enumerate(truth):
            if (
                d_start == g_start
                and d_end == g_end
                and (not strict_labels or _LABEL_TO_ENTITY.get(label) is d_type)
            ):
                candidates.append((d_idx, t_idx))

    matched_detections: set[int] = set()
    matched_truth: set[int] = set()
    for d_idx, t_idx in candidates:
        if d_idx in matched_detections or t_idx in matched_truth:
            continue
        matched_detections.add(d_idx)
        matched_truth.add(t_idx)
    return matched_detections, matched_truth


def _length_bucket(length: int) -> str:
    if length < 100:
        return "<100"
    if length < 500:
        return "100-500"
    if length < 1000:
        return "500-1000"
    return ">=1000"


INTEGRITY_NOTICE = """
================================================================================
STRICT BENCHMARK INTEGRITY NOTICE
================================================================================
1. NO HARDCODING: Do not write regex or rules targeting specific strings, names, 
   or artifacts found exclusively in this dataset.
2. NO DATA LEAKAGE: If a model is fine-tuned, it MUST NOT be fine-tuned on the 
   exact slice of data used for this evaluation.
3. GENERALIZATION ONLY: All heuristics and thresholds must generalize to unseen 
   real-world text.
4. BLIND EVALUATION: Do not inspect the validation split to build rules. Debug 
   and develop heuristics exclusively on the `train` split.

Any PR that artificially inflates these numbers by 'cheating' the dataset
will be rejected. The goal is real-world safety, not a high scoreboard number.
================================================================================
"""


def load_local_jsonl(file_path: Path) -> typing.Iterator[dict[str, typing.Any]]:
    import json

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            if "language" not in row:
                row["language"] = "en"
            yield row


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def evaluate(
    num_samples: int = 1000,
    use_ml: bool = True,
    strict_labels: bool = True,
    split: str = "validation",
    explain: bool = False,
    file_path: Path | None = None,
    allow_unverified_checksums: bool = False,
    dataset_revision: str | None = None,
    manifest_path: Path | None = None,
) -> dict[str, object]:
    print(INTEGRITY_NOTICE)

    manifest_hashes: set[str] | None = None
    if manifest_path is not None:
        manifest_content = json.loads(manifest_path.read_text(encoding="utf-8"))
        if isinstance(manifest_content, dict) and "row_hashes" in manifest_content:
            manifest_hashes = set(manifest_content["row_hashes"])
        elif isinstance(manifest_content, list):
            manifest_hashes = set(manifest_content)

    if file_path is not None:
        logger.info(f"Loading local evaluation dataset from {file_path}...")
        ds = load_local_jsonl(file_path)
    else:
        if dataset_revision is None:
            raise ValueError("dataset_revision is required when evaluating a remote dataset")
        try:
            from datasets import load_dataset
        except ImportError:
            print("Error: 'datasets' library not found.")
            print("Run: uv run --with datasets python benchmarks/evaluate_quality.py")
            sys.exit(1)
        logger.info(f"Loading {DATASET_NAME}@{dataset_revision} ({split} split, English subset)...")
        # We shuffle with a fixed seed to ensure a consistent, reproducible
        # pseudo-random sample of the evaluation dataset for A/B testing versions.
        ds = load_dataset(
            DATASET_NAME, split=split, streaming=True, revision=dataset_revision
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
        # We need the model downloaded. The test suite uses the multilang-pii-ner model.
        # Let's assume it's already cached or we can fetch it.
        # To keep it simple, we'll try to initialize it. If it fails, we fall back or error.
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

    true_positives = 0
    false_positives = 0
    false_negatives = 0
    out_of_scope = 0

    exact_true_positives = 0
    exact_false_negatives = 0

    error_totals = {
        "missing_candidate": 0,
        "threshold_suppression": 0,
        "label_confusion": 0,
        "boundary_mismatch": 0,
        "conflict_loss": 0,
    }

    total_true_chars = 0
    total_masked_chars = 0
    total_detected_chars = 0

    row_stats: list[dict[str, typing.Any]] = []

    # Per-entity metrics
    tp_per_type: dict[EntityType, int] = dict.fromkeys(EntityType, 0)
    fp_per_type: dict[EntityType, int] = dict.fromkeys(EntityType, 0)
    fn_per_type: dict[EntityType, int] = dict.fromkeys(EntityType, 0)

    count = 0
    start_time = time.time()

    for row in ds:
        if row["language"] != "en":
            continue

        text = row["source_text"]
        row_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if manifest_hashes is not None and row_hash not in manifest_hashes:
            continue

        masks = row["privacy_mask"]

        # Annotations we claim to support are the ones scored. The rest are kept
        # aside rather than dropped: a correct detection of a label outside our
        # scope is not a false positive, it is simply not being measured here.
        scored_spans = [
            (mask["start"], mask["end"], mask["label"])
            for mask in masks
            if mask["label"] in SUPPORTED_LABELS
        ]
        out_of_scope_spans = [
            (mask["start"], mask["end"]) for mask in masks if mask["label"] not in SUPPORTED_LABELS
        ]

        result = engine.process_with_report(text)
        detections = [
            (detection.start, detection.end, detection.entity_type)
            for detection in result.detections
        ]

        matched_detections, matched_truth = _match(detections, scored_spans, strict_labels)
        matched_exact_dets, matched_exact_truth = _match_exact(
            detections, scored_spans, strict_labels
        )

        true_positives += len(matched_truth)
        false_negatives += len(scored_spans) - len(matched_truth)
        exact_true_positives += len(matched_exact_truth)
        exact_false_negatives += len(scored_spans) - len(matched_exact_truth)

        # Candidate lifecycle tracing
        block = ContentBlock("text", text, TextOffsetLocation(0, len(text)))
        raw_candidates: list[typing.Any] = []
        for backend_obj in engine.backends:
            with contextlib.suppress(Exception):
                raw_candidates.extend(invoke_backend(backend_obj, block, engine.policy))

        retained_candidates = [
            c
            for c in raw_candidates
            if c.entity_type in engine.policy.entity_types
            and c.confidence >= engine.policy.minimum_confidence
        ]

        row_errors = {
            "missing_candidate": 0,
            "threshold_suppression": 0,
            "label_confusion": 0,
            "boundary_mismatch": 0,
            "conflict_loss": 0,
        }

        row_tp: dict[str, int] = {}
        row_fp: dict[str, int] = {}
        row_fn: dict[str, int] = {}
        row_exact_tp: dict[str, int] = {}
        row_exact_fp: dict[str, int] = {}
        row_exact_fn: dict[str, int] = {}

        # Matched (True Positives)
        for truth_index in matched_truth:
            _, _, label = scored_spans[truth_index]
            entity_type = _LABEL_TO_ENTITY.get(label)
            if entity_type is not None:
                tp_per_type[entity_type] += 1
                row_tp[entity_type.value] = row_tp.get(entity_type.value, 0) + 1

        for truth_index in matched_exact_truth:
            _, _, label = scored_spans[truth_index]
            entity_type = _LABEL_TO_ENTITY.get(label)
            if entity_type is not None:
                row_exact_tp[entity_type.value] = row_exact_tp.get(entity_type.value, 0) + 1

        # Truth analysis (FN & Error categorization)
        for index, (g_start, g_end, label) in enumerate(scored_spans):
            target_type = _LABEL_TO_ENTITY.get(label)
            if target_type is None:
                continue

            if index in matched_truth:
                if index not in matched_exact_truth:
                    row_errors["boundary_mismatch"] += 1
            else:
                fn_per_type[target_type] += 1
                row_fn[target_type.value] = row_fn.get(target_type.value, 0) + 1

                # Causal failure classification
                overlapping_raw = [
                    c for c in raw_candidates if min(c.end, g_end) > max(c.start, g_start)
                ]
                if not overlapping_raw:
                    row_errors["missing_candidate"] += 1
                else:
                    overlapping_retained = [
                        c for c in retained_candidates if min(c.end, g_end) > max(c.start, g_start)
                    ]
                    matching_type_retained = [
                        c for c in overlapping_retained if c.entity_type is target_type
                    ]
                    if not matching_type_retained:
                        matching_type_raw = [
                            c for c in overlapping_raw if c.entity_type is target_type
                        ]
                        if matching_type_raw:
                            row_errors["threshold_suppression"] += 1
                        else:
                            row_errors["label_confusion"] += 1
                    else:
                        row_errors["conflict_loss"] += 1

                if explain:
                    context = text[max(0, g_start - 40) : min(len(text), g_end + 40)]
                    logger.info(f"FN: '{text[g_start:g_end]}' should be {label} ({context})")

            if index not in matched_exact_truth:
                row_exact_fn[target_type.value] = row_exact_fn.get(target_type.value, 0) + 1

        # Unmatched Detections (False Positives)
        row_oos = 0
        for index, (d_start, d_end, entity_type) in enumerate(detections):
            is_oos = any(
                max(d_start, o_start) < min(d_end, o_end) for o_start, o_end in out_of_scope_spans
            )
            if is_oos:
                row_oos += 1

            if index not in matched_detections:
                if is_oos:
                    out_of_scope += 1
                    continue

                fp_per_type[entity_type] += 1
                false_positives += 1
                row_fp[entity_type.value] = row_fp.get(entity_type.value, 0) + 1
                if explain:
                    logger.info(f"FP: '{text[d_start:d_end]}' as {entity_type.value}")

            if index not in matched_exact_dets and not is_oos:
                row_exact_fp[entity_type.value] = row_exact_fp.get(entity_type.value, 0) + 1

        for err_k, err_v in row_errors.items():
            error_totals[err_k] += err_v

        # Character masking coverage
        row_true_char_indices: set[int] = set()
        for g_start, g_end, _ in scored_spans:
            row_true_char_indices.update(range(g_start, g_end))

        row_det_char_indices: set[int] = set()
        for d_start, d_end, _ in detections:
            row_det_char_indices.update(range(d_start, d_end))

        masked_row_chars = len(row_true_char_indices & row_det_char_indices)
        total_true_chars += len(row_true_char_indices)
        total_detected_chars += len(row_det_char_indices)
        total_masked_chars += masked_row_chars

        row_stats.append(
            {
                "row_hash": row_hash,
                "length_bucket": _length_bucket(len(text)),
                "language": str(row.get("language", "en")),
                "source": str(row.get("source", "unknown")),
                "tp": row_tp,
                "fp": row_fp,
                "fn": row_fn,
                "out_of_scope": row_oos,
                "exact_tp": row_exact_tp,
                "exact_fp": row_exact_fp,
                "exact_fn": row_exact_fn,
                "error_categories": row_errors,
                "char_masking": {
                    "true_chars": len(row_true_char_indices),
                    "detected_chars": len(row_det_char_indices),
                    "masked_true_chars": masked_row_chars,
                },
            }
        )

        count += 1
        if count % 50 == 0:
            logger.info(f"Processed {count}/{num_samples} samples...")
        if count >= num_samples:
            break

    elapsed = time.time() - start_time

    precision = (
        true_positives / (true_positives + false_positives)
        if (true_positives + false_positives) > 0
        else 0
    )
    recall = (
        true_positives / (true_positives + false_negatives)
        if (true_positives + false_negatives) > 0
        else 0
    )
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    # Exact boundary metrics
    exact_false_positives = sum(sum(r["exact_fp"].values()) for r in row_stats)
    exact_p = (
        exact_true_positives / (exact_true_positives + exact_false_positives)
        if (exact_true_positives + exact_false_positives) > 0
        else 0.0
    )
    exact_r = (
        exact_true_positives / (exact_true_positives + exact_false_negatives)
        if (exact_true_positives + exact_false_negatives) > 0
        else 0.0
    )
    exact_f1 = 2 * (exact_p * exact_r) / (exact_p + exact_r) if (exact_p + exact_r) > 0 else 0.0

    # Macro F1 (unweighted average across entity types with ground truth support > 0)
    per_entity_f1s = []
    for et in EntityType:
        tp = tp_per_type.get(et, 0)
        fp = fp_per_type.get(et, 0)
        fn = fn_per_type.get(et, 0)
        if tp + fn > 0:
            p_e = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            r_e = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1_e = 2 * (p_e * r_e) / (p_e + r_e) if (p_e + r_e) > 0 else 0.0
            per_entity_f1s.append(f1_e)
    macro_f1 = sum(per_entity_f1s) / len(per_entity_f1s) if per_entity_f1s else 0.0

    char_recall = total_masked_chars / total_true_chars if total_true_chars > 0 else 0.0
    char_precision = total_masked_chars / total_detected_chars if total_detected_chars > 0 else 0.0

    # Partitioned statistics
    by_length_bucket: dict[str, dict[str, int]] = {}
    by_language: dict[str, dict[str, int]] = {}
    for r in row_stats:
        b = r["length_bucket"]
        if b not in by_length_bucket:
            by_length_bucket[b] = {"tp": 0, "fp": 0, "fn": 0}
        by_length_bucket[b]["tp"] += sum(r["tp"].values())
        by_length_bucket[b]["fp"] += sum(r["fp"].values())
        by_length_bucket[b]["fn"] += sum(r["fn"].values())

        lang = r["language"]
        if lang not in by_language:
            by_language[lang] = {"tp": 0, "fp": 0, "fn": 0}
        by_language[lang]["tp"] += sum(r["tp"].values())
        by_language[lang]["fp"] += sum(r["fp"].values())
        by_language[lang]["fn"] += sum(r["fn"].values())

    logger.info(f"--- Benchmark Results ({count} samples) ---")
    logger.info(f"Label matching:  {'strict' if strict_labels else 'span only'}")
    logger.info(f"Time elapsed: {elapsed:.2f}s")
    logger.info(f"True Positives:  {true_positives}")
    logger.info(f"False Positives: {false_positives}")
    logger.info(f"False Negatives: {false_negatives}")
    logger.info(f"Unscored:        {out_of_scope} (detections on labels outside the scored set)")
    logger.info(f"Precision:       {precision:.4f}")
    logger.info(f"Recall:          {recall:.4f}")
    logger.info(f"F1 Score:        {f1:.4f}")
    logger.info(
        f"Exact Boundary:  P={exact_p:.4f}, R={exact_r:.4f}, F1={exact_f1:.4f} "
        f"(TP={exact_true_positives}, FP={exact_false_positives}, FN={exact_false_negatives})"
    )
    logger.info(f"Macro F1:        {macro_f1:.4f}")
    logger.info(
        f"Char Masking:    Recall={char_recall:.4f}, Precision={char_precision:.4f} "
        f"({total_masked_chars}/{total_true_chars} sensitive chars masked)"
    )
    logger.info(f"Error Breakdown: {error_totals}")
    logger.info("\n--- Per-Entity Metrics ---")
    logger.info(
        f"{'Entity Type':<20} | {'TP':<6} | {'FP':<6} | {'FN':<6} | "
        f"{'Precision':<9} | {'Recall':<6} | {'F1':<6}"
    )
    logger.info("-" * 75)
    for et in sorted(EntityType, key=lambda x: x.name):
        tp = tp_per_type.get(et, 0)
        fp = fp_per_type.get(et, 0)
        fn = fn_per_type.get(et, 0)
        if tp == 0 and fp == 0 and fn == 0:
            continue
        et_precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        et_recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        et_f1 = (
            2 * (et_precision * et_recall) / (et_precision + et_recall)
            if (et_precision + et_recall) > 0
            else 0
        )
        logger.info(
            f"{et.name:<20} | {tp:<6} | {fp:<6} | {fn:<6} | "
            f"{et_precision:.4f}    | {et_recall:.4f} | {et_f1:.4f}"
        )

    per_entity = {
        entity_type.value: {
            "true_positives": tp_per_type[entity_type],
            "false_positives": fp_per_type[entity_type],
            "false_negatives": fn_per_type[entity_type],
        }
        for entity_type in EntityType
        if tp_per_type[entity_type] or fp_per_type[entity_type] or fn_per_type[entity_type]
    }
    return {
        "package_version": version("pseudonymize"),
        "package_commit": _git_commit(),
        "policy_configuration": {
            "entity_types": sorted(e.value for e in engine.policy.entity_types),
            "network_policy": engine.policy.network_policy.name,
            "backends": [b.name for b in engine.backends],
            "allow_unverified_checksums": allow_unverified_checksums,
            "strict_labels": strict_labels,
        },
        "dataset": DATASET_NAME if file_path is None else None,
        "dataset_revision": dataset_revision,
        "file": str(file_path) if file_path is not None else None,
        "file_sha256": _sha256(file_path) if file_path is not None else None,
        "manifest": str(manifest_path) if manifest_path is not None else None,
        "split": split,
        "shuffle_seed": SHUFFLE_SEED,
        "samples": count,
        "strict_labels": strict_labels,
        "allow_unverified_checksums": allow_unverified_checksums,
        "use_ml": use_ml,
        "python": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "model_sha256": model_hashes,
        "counts": {
            "true_positives": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "out_of_scope": out_of_scope,
        },
        "metrics": {"precision": precision, "recall": recall, "f1": f1},
        "exact_metrics": {"precision": exact_p, "recall": exact_r, "f1": exact_f1},
        "macro_f1": macro_f1,
        "character_masking": {
            "recall": char_recall,
            "precision": char_precision,
            "total_true_chars": total_true_chars,
            "masked_chars": total_masked_chars,
        },
        "error_categories": error_totals,
        "by_length_bucket": by_length_bucket,
        "by_language": by_language,
        "per_entity": per_entity,
        "rows": row_stats,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate pseudonymize precision and recall against real-world datasets."
    )
    parser.add_argument("--samples", type=int, default=1000, help="Number of samples to evaluate.")
    parser.add_argument(
        "--file", type=str, default=None, help="Path to local JSONL evaluation file."
    )
    parser.add_argument(
        "--dataset-revision",
        help="Immutable dataset revision required when --file is not supplied.",
    )
    parser.add_argument("--output", type=Path, help="Write the result record as JSON.")
    parser.add_argument(
        "--ml", action="store_true", help="Include the ONNX ML backend in evaluation."
    )
    parser.add_argument(
        "--span-only",
        action="store_true",
        help="Score any overlap as a hit, ignoring whether the entity type matches.",
    )
    parser.add_argument(
        "--split",
        type=str,
        default="validation",
        help="Dataset split to evaluate (e.g., train, validation).",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Print false positive and false negative explanations.",
    )
    parser.add_argument(
        "--allow-unverified-checksums",
        action="store_true",
        help="Benchmark synthetic checksum-shaped values without a library-wide bypass.",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        help="Path to JSON manifest containing row hashes to evaluate.",
    )
    args = parser.parse_args()

    file_path = Path(args.file) if args.file is not None else None
    manifest_path = Path(args.manifest) if args.manifest is not None else None
    if file_path is None and args.dataset_revision is None:
        parser.error("--dataset-revision is required when --file is not supplied")
    result = evaluate(
        args.samples,
        args.ml,
        strict_labels=not args.span_only,
        split=args.split,
        explain=args.explain,
        file_path=file_path,
        allow_unverified_checksums=args.allow_unverified_checksums,
        dataset_revision=args.dataset_revision,
        manifest_path=manifest_path,
    )
    if args.output is not None:
        args.output.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
