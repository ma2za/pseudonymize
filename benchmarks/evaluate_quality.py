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

Any PR that artificially inflates these numbers by 'cheating' the dataset 
will be rejected. The goal is real-world safety, not a high scoreboard number.
================================================================================
"""


def evaluate(num_samples: int, use_ml: bool):
    print(INTEGRITY_NOTICE)
    logger.info("Loading ai4privacy/pii-masking-openpii-1.5m (English subset)...")

    # We use the validation split of the 1.5M dataset.
    # We shuffle with a fixed seed to ensure a consistent, reproducible 
    # pseudo-random sample of the evaluation dataset for A/B testing versions.
    ds = load_dataset("ai4privacy/pii-masking-openpii-1.5m", split="validation", streaming=True)
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

    count = 0
    start_time = time.time()

    for row in ds:
        if row["language"] != "en":
            continue

        text = row["source_text"]
        masks = row["privacy_mask"]

        # Filter ground truth masks to only those we claim to support
        ground_truth_spans = [
            (mask["start"], mask["end"], mask["label"])
            for mask in masks
            if mask["label"] in SUPPORTED_LABELS
        ]

        # Run detection
        result = engine.process_with_report(text)

        # Extract detected spans
        detected_spans = [(detection.start, detection.end) for detection in result.detections]

        # Calculate overlap
        # A single detected span can overlap with multiple ground truth spans
        # (e.g. "John Smith" detected as one PERSON span but annotated as FIRSTNAME and LASTNAME).
        matched_gt = set()
        for d_start, d_end in detected_spans:
            matched = False
            for i, (g_start, g_end, _g_label) in enumerate(ground_truth_spans):
                # Check overlap
                if max(d_start, g_start) < min(d_end, g_end):
                    matched = True
                    matched_gt.add(i)
            if matched:
                true_positives += 1
            else:
                false_positives += 1

        for i in range(len(ground_truth_spans)):
            if i not in matched_gt:
                false_negatives += 1

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
    parser.add_argument("--samples", type=int, default=1000, help="Number of samples to evaluate.")
    parser.add_argument(
        "--ml", action="store_true", help="Include the ONNX ML backend in evaluation."
    )
    args = parser.parse_args()

    evaluate(args.samples, args.ml)
