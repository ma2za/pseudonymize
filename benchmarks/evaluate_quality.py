import argparse
import logging
import sys
import time
from pathlib import Path

try:
    from datasets import load_dataset
except ImportError:
    print("Error: 'datasets' library not found.")
    print("Run: uv run --with datasets python benchmarks/evaluate_quality.py")
    sys.exit(1)

from pseudonymize.backends.ml.onnx import LocalONNXPIIBackend
from pseudonymize.engine import Pseudonymizer
from pseudonymize.result import EntityType

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("evaluate_quality")

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


def load_local_jsonl(file_path: Path):
    import json

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            if "language" not in row:
                row["language"] = "en"
            yield row


def evaluate(
    num_samples: int,
    use_ml: bool,
    strict_labels: bool = True,
    split: str = "validation",
    explain: bool = False,
    file_path: Path | None = None,
) -> None:
    print(INTEGRITY_NOTICE)

    if file_path is not None:
        logger.info(f"Loading local evaluation dataset from {file_path}...")
        ds = load_local_jsonl(file_path)
    else:
        logger.info(
            f"Loading ai4privacy/pii-masking-openpii-1.5m ({split} split, English subset)..."
        )
        # We shuffle with a fixed seed to ensure a consistent, reproducible
        # pseudo-random sample of the evaluation dataset for A/B testing versions.
        ds = load_dataset("ai4privacy/pii-masking-openpii-1.5m", split=split, streaming=True)
        ds = ds.shuffle(seed=42)

    engine = Pseudonymizer()
    if use_ml:
        # We need the model downloaded. The test suite uses the distilbert model.
        # Let's assume it's already cached or we can fetch it.
        # To keep it simple, we'll try to initialize it. If it fails, we fall back or error.
        CACHE_DIR = Path(".cache/pseudonymize-tests/models/distilbert-ml")
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
        engine = Pseudonymizer(backends=[*engine.backends, backend])

    true_positives = 0
    false_positives = 0
    false_negatives = 0
    out_of_scope = 0

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

        true_positives += len(matched_truth)
        false_negatives += len(scored_spans) - len(matched_truth)

        # Matched (True Positives)
        for truth_index in matched_truth:
            _, _, label = scored_spans[truth_index]
            entity_type = _LABEL_TO_ENTITY.get(label)
            if entity_type is not None:
                tp_per_type[entity_type] += 1

        # Unmatched Truth (False Negatives)
        for index, (g_start, g_end, label) in enumerate(scored_spans):
            if index not in matched_truth:
                entity_type = _LABEL_TO_ENTITY.get(label)
                if entity_type is not None:
                    fn_per_type[entity_type] += 1

                if explain:
                    context = text[max(0, g_start - 40) : min(len(text), g_end + 40)]
                    logger.info(f"FN: '{text[g_start:g_end]}' should be {label} ({context})")

        # Unmatched Detections (False Positives)
        for index, (d_start, d_end, entity_type) in enumerate(detections):
            if index in matched_detections:
                continue
            # A detection landing on an annotation we do not claim to support is
            # neither credited nor penalized.
            if any(
                max(d_start, o_start) < min(d_end, o_end) for o_start, o_end in out_of_scope_spans
            ):
                out_of_scope += 1
                continue

            fp_per_type[entity_type] += 1
            false_positives += 1
            if explain:
                logger.info(f"FP: '{text[d_start:d_end]}' as {entity_type.value}")

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate pseudonymize precision and recall against real-world datasets."
    )
    parser.add_argument("--samples", type=int, default=1000, help="Number of samples to evaluate.")
    parser.add_argument(
        "--file", type=str, default=None, help="Path to local JSONL evaluation file."
    )
    parser.add_argument(
        "--ml", action="store_true", help="Include the ONNX ML backend in evaluation."
    )
    parser.add_argument(
        "--span-only",
        action="store_true",
        help="Score any overlap as a hit, ignoring whether the entity type matches.",
    )
    args = parser.parse_args()

    file_path = Path(args.file) if args.file is not None else None
    evaluate(args.samples, args.ml, strict_labels=not args.span_only, file_path=file_path)
