# Detection Quality Benchmarks

This document tracks the precision and recall of the `pseudonymize` engine across real-world and synthetic evaluation corpora. Unlike performance benchmarks (which measure throughput and latency), quality benchmarks ensure the core detectors and ML backends accurately identify PII without excessive false positives.

## `0.7.0` Baseline (AI4Privacy PII-Masking-200k)

Evaluated against the English subset of the `ai4privacy/pii-masking-200k` dataset, comparing the engine's detections against the dataset's ground-truth `privacy_mask`.

**Setup:**
- Model: `LocalONNXPIIBackend` (DistilBERT ONNX int8)
- Target Entities: `EMAIL`, `PHONENUMBER`, `CREDITCARD`, `IBAN`, `IPADDRESS`, `URL`, `FIRSTNAME`, `LASTNAME`, `MIDDLENAME`, `COMPANYNAME`, `CITY`, `STATE`, `COUNTY`, `STREET`, `ZIPCODE`
- Sample Size: 50 documents (Streaming)

**Results (Preliminary Baseline):**

| Metric | Score |
| --- | --- |
| Precision | 0.4091 |
| Recall | 0.1875 |
| F1 Score | 0.2571 |

*Note: These baseline metrics reflect zero-configuration default detectors and the stock ML backend on a highly ambiguous, fine-grained synthetic dataset. Future releases (e.g., 0.13.0 ML Calibration) will optimize these metrics through tuned thresholds and improved boundaries.*

To reproduce this benchmark locally:
```console
uv run python benchmarks/evaluate_quality.py --ml --samples 50
```
## `0.8.0` (Detection Boundary & Tokenization Alignment)

Evaluated on the pseudo-test holdout slice (last 8k English rows) of i4privacy/pii-masking-200k after fixing ML sub-word boundary parsing and respecting B- (beginning of entity) tokens.

**Results:**

| Metric | Score |
| --- | --- |
| Precision | 0.8934 |
| Recall | 0.9134 |
| F1 Score | 0.9033 |
