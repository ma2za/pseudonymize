import argparse
import logging
import sys
import time
from pathlib import Path

try:
    from datasets import load_dataset
except ImportError:
    print(
        "Error: 'datasets' library not found. Run: uv run --with datasets python benchmarks/evaluate_quality.py"
    )
    sys.exit(1)

from pseudonymize.backends.ml.onnx import LocalONNXPIIBackend
from pseudonymize.engine import Pseudonymizer

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("evaluate_quality")

# We evaluate precision and recall against these specific AI4Privacy labels
# that map to the capabilities of pseudonymize's core detectors and ML backend.
SUPPORTED_LABELS = {
    # Core detectors
    "EMAIL",
    "PHONENUMBER",
    "CREDITCARD",
    "IBAN",
    "IPADDRESS",
    "URL",
    # ML Backend (DistilBERT ONNX)
    "FIRSTNAME",
    "LASTNAME",
    "MIDDLENAME",
    "COMPANYNAME",
    "CITY",
    "STATE",
    "COUNTY",
    "STREET",
    "ZIPCODE",
}


def evaluate(num_samples: int, use_ml: bool):
    logger.info("Loading ai4privacy/pii-masking-200k (English subset)...")
    # Use streaming to avoid downloading the entire 200K dataset
    ds = load_dataset("ai4privacy/pii-masking-200k", split="train", streaming=True)

    engine = Pseudonymizer()
    if use_ml:
        # We need the model downloaded. The test suite uses the distilbert model.
        # Let's assume it's already cached or we can fetch it.
        # To keep it simple, we'll try to initialize it. If it fails, we fall back or error.
        CACHE_DIR = Path(".cache/pseudonymize-tests/models/distilbert-ml")
        onnx_model_path = CACHE_DIR / "model_int8.onnx"
        tokenizer_path = CACHE_DIR / "tokenizer.json"

        if not onnx_model_path.exists() or not tokenizer_path.exists():
            logger.error(
                f"ML artifacts not found in {CACHE_DIR}. Please run 'uv run pytest tests/unit/backends/test_onnx.py' first to download them."
            )
            sys.exit(1)

        backend = LocalONNXPIIBackend(model_path=onnx_model_path, tokenizer_path=tokenizer_path)
        engine = Pseudonymizer(backends=[*engine.backends, backend])

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    count = 0
    start_time = time.time()

    for row in ds:
        if row["language"] != "en":
            continue

        text = row["source_text"]
        masks = row["privacy_mask"]

        # Filter ground truth masks to only those we claim to support
        ground_truth_spans = []
        for mask in masks:
            if mask["label"] in SUPPORTED_LABELS:
                ground_truth_spans.append((mask["start"], mask["end"], mask["label"]))

        # Run detection
        result = engine.process_with_report(text)

        # Extract detected spans
        detected_spans = []
        for detection in result.detections:
            detected_spans.append((detection.start, detection.end))

        # Calculate overlap
        # For simplicity in this benchmark:
        # TP: a detected span overlaps with a ground truth span.
        # FP: a detected span does not overlap with any ground truth span.
        # FN: a ground truth span is not overlapped by any detected span.

        matched_gt = set()
        for d_start, d_end in detected_spans:
            matched = False
            for i, (g_start, g_end, _g_label) in enumerate(ground_truth_spans):
                # Check overlap
                if max(d_start, g_start) < min(d_end, g_end):
                    matched = True
                    matched_gt.add(i)
                    break
            if matched:
                true_positives += 1
            else:
                false_positives += 1

        for i in range(len(ground_truth_spans)):
            if i not in matched_gt:
                false_negatives += 1

        count += 1
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
    logger.info(f"Time elapsed: {elapsed:.2f}s")
    logger.info(f"True Positives:  {true_positives}")
    logger.info(f"False Positives: {false_positives}")
    logger.info(f"False Negatives: {false_negatives}")
    logger.info(f"Precision:       {precision:.4f}")
    logger.info(f"Recall:          {recall:.4f}")
    logger.info(f"F1 Score:        {f1:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate pseudonymize precision and recall against real-world datasets."
    )
    parser.add_argument("--samples", type=int, default=500, help="Number of samples to evaluate.")
    parser.add_argument(
        "--ml", action="store_true", help="Include the ONNX ML backend in evaluation."
    )
    args = parser.parse_args()

    evaluate(args.samples, args.ml)
