import logging
import os
from collections import defaultdict
from pathlib import Path

from datasets import load_dataset

from pseudonymize.backends.ml.onnx import LocalONNXPIIBackend
from pseudonymize.engine import Pseudonymizer
from pseudonymize.memory.bloom import BloomFilter
from pseudonymize.result import EntityType

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("analyze_failures")

SUPPORTED_LABELS = {
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


def analyze():
    # Only use train split to avoid benchmark cheating
    ds = load_dataset("ai4privacy/pii-masking-openpii-1.5m", split="train", streaming=True).shuffle(
        seed=42
    )

    bloom_path = Path("data/gazetteer/common_words.txt")
    bloom_filter = None
    if bloom_path.exists():
        with open(bloom_path, encoding="utf-8") as f:
            bloom_filter = BloomFilter.from_words(
                [line.strip().lower() for line in f if line.strip()]
            )

    CACHE_DIR = Path(".cache/pseudonymize-tests/models/llama-ai4privacy-ml")
    backend = LocalONNXPIIBackend(
        model_path=CACHE_DIR / "model_int8.onnx",
        tokenizer_path=CACHE_DIR / "tokenizer.json",
        config_path=CACHE_DIR / "config.json",
    )
    engine = Pseudonymizer(backends=[*Pseudonymizer().backends, backend], bloom_filter=bloom_filter)

    count = 0
    fn_samples = defaultdict(list)
    fp_samples = defaultdict(list)

    os.environ["SYNTHETIC_BENCHMARK"] = "1"

    for row in ds:
        if row["language"] != "en":
            continue
        text = row["source_text"]
        scored_spans = [
            (m["start"], m["end"], m["label"])
            for m in row["privacy_mask"]
            if m["label"] in SUPPORTED_LABELS
        ]

        result = engine.process_with_report(text)
        detections = [(d.start, d.end, d.entity_type) for d in result.detections]

        # Simple overlap check for analysis (not strict scoring)
        matched_truth = set()
        matched_det = set()

        for ti, (t_start, t_end, t_label) in enumerate(scored_spans):
            t_entity = SUPPORTED_LABELS[t_label]
            for di, (d_start, d_end, d_entity) in enumerate(detections):
                overlap = min(d_end, t_end) - max(d_start, t_start)
                if overlap > 0 and d_entity == t_entity:
                    matched_truth.add(ti)
                    matched_det.add(di)
                    break

            if ti not in matched_truth:
                context = text[max(0, t_start - 30) : min(len(text), t_end + 30)].replace("\n", " ")
                val = text[t_start:t_end]
                fn_samples[t_entity.name].append(
                    f"Val: '{val}' | Ctx: '{context}' | Lbl: {t_label}"
                )

        for di, (d_start, d_end, d_entity) in enumerate(detections):
            if di not in matched_det:
                context = text[max(0, d_start - 30) : min(len(text), d_end + 30)].replace("\n", " ")
                val = text[d_start:d_end]
                fp_samples[d_entity.name].append(f"Val: '{val}' | Ctx: '{context}'")

        count += 1
        if count >= 300:
            break

    print("\n=== TOP FALSE NEGATIVES (MISSED BY ENGINE) ===")
    for entity, samples in sorted(fn_samples.items()):
        if samples:
            print(f"\n{entity} ({len(samples)} misses):")
            for s in samples[:10]:
                print(f"  - {s}")

    print("\n=== TOP FALSE POSITIVES (WRONGLY FLAGGED BY ENGINE) ===")
    for entity, samples in sorted(fp_samples.items()):
        if samples:
            print(f"\n{entity} ({len(samples)} false alarms):")
            for s in samples[:10]:
                print(f"  - {s}")


if __name__ == "__main__":
    analyze()
