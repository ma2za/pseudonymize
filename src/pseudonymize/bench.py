import argparse
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from pseudonymize.backends.ml.onnx import LocalONNXPIIBackend
from pseudonymize.engine import Pseudonymizer
from pseudonymize.result import EntityType

# We duplicate the minimum necessary parts from evaluate_quality.py
# to make it completely stand-alone and zero-dependency (other than what's already in core).

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("pseudonymize.bench")

SUPPORTED_LABELS = {
    "EMAIL",
    "PHONE",
    "PAYMENT_CARD",
    "IBAN",
    "IP_ADDRESS",
    "URL_CREDENTIAL",
    "NATIONAL_ID",
    "TAX_ID",
    "PERSON",
    "ORGANIZATION",
    "LOCATION",
}


def _match(
    detections: list[tuple[int, int, EntityType]],
    truth: list[tuple[int, int, str]],
    strict_labels: bool,
) -> tuple[set[int], set[int]]:
    candidates = []
    for detection_index, (d_start, d_end, entity_type) in enumerate(detections):
        for truth_index, (g_start, g_end, label) in enumerate(truth):
            overlap = min(d_end, g_end) - max(d_start, g_start)
            if overlap <= 0:
                continue
            if strict_labels and label != entity_type.name:
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


def load_local_jsonl(file_path: Path) -> Iterator[Any]:
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
    file_path: Path,
    use_ml: bool = False,
    strict_labels: bool = True,
    explain: bool = False,
) -> None:
    logger.info(f"Loading local evaluation dataset from {file_path}...")
    ds = load_local_jsonl(file_path)

    engine = Pseudonymizer()
    if use_ml:
        CACHE_DIR = Path(".cache/pseudonymize-tests/models/distilbert-ml")
        onnx_model_path = CACHE_DIR / "model_int8.onnx"
        tokenizer_path = CACHE_DIR / "tokenizer.json"
        config_path = CACHE_DIR / "config.json"

        if onnx_model_path.exists() and tokenizer_path.exists() and config_path.exists():
            backend = LocalONNXPIIBackend(
                model_path=onnx_model_path,
                tokenizer_path=tokenizer_path,
                config_path=config_path,
            )
            engine = Pseudonymizer(backends=[*engine.backends, backend])
        else:
            logger.warning(f"ML artifacts not found in {CACHE_DIR}, running without ML backend.")

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    tp_per_type: dict[EntityType, int] = dict.fromkeys(EntityType, 0)
    fp_per_type: dict[EntityType, int] = dict.fromkeys(EntityType, 0)
    fn_per_type: dict[EntityType, int] = dict.fromkeys(EntityType, 0)

    count = 0
    for row in ds:
        text = row["source_text"]
        masks = row["privacy_mask"]

        scored_spans = []
        for mask in masks:
            label = mask["label"]
            if label in SUPPORTED_LABELS:
                scored_spans.append((mask["start"], mask["end"], label))

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
            entity_type = EntityType[label]
            tp_per_type[entity_type] += 1

        # Unmatched Truth (False Negatives)
        for index, (g_start, g_end, label) in enumerate(scored_spans):
            if index not in matched_truth:
                entity_type = EntityType[label]
                fn_per_type[entity_type] += 1
                if explain:
                    logger.info(f"FN: '{text[g_start:g_end]}' should be {label}")

        # Unmatched Detections (False Positives)
        for index, (d_start, d_end, entity_type) in enumerate(detections):
            if index in matched_detections:
                continue

            fp_per_type[entity_type] += 1
            false_positives += 1
            if explain:
                logger.info(f"FP: '{text[d_start:d_end]}' as {entity_type.value}")

        count += 1

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
    logger.info(f"True Positives:  {true_positives}")
    logger.info(f"False Positives: {false_positives}")
    logger.info(f"False Negatives: {false_negatives}")
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


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Local evaluation harness for pseudonymize quality testing."
    )
    parser.add_argument("file", type=str, help="Path to local JSONL evaluation file.")
    parser.add_argument(
        "--ml", action="store_true", help="Include the ONNX ML backend in evaluation."
    )
    parser.add_argument(
        "--span-only",
        action="store_true",
        help="Score any overlap as a hit, ignoring whether the entity type matches.",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Log details of all False Positives and False Negatives.",
    )
    args = parser.parse_args()

    evaluate(
        file_path=Path(args.file),
        use_ml=args.ml,
        strict_labels=not args.span_only,
        explain=args.explain,
    )


if __name__ == "__main__":
    main()
