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

To reproduce this benchmark locally:
```console
uv run python benchmarks/evaluate_quality.py --ml --samples 50
```

## `0.8.0` (Detection Boundary & Tokenization Alignment)

Evaluated on the pseudo-test holdout slice (last 8k English rows) of `ai4privacy/pii-masking-200k` after fixing ML sub-word boundary parsing and respecting B- (beginning of entity) tokens.

**Results:**

| Metric | Score |
| --- | --- |
| Precision | 0.8934 |
| Recall | 0.9134 |
| F1 Score | 0.9033 |

## `0.8.0` (OpenPII-1.5m Baseline)

Evaluated on the English subset of the `ai4privacy/pii-masking-openpii-1.5m` dataset (validation split, 1000 randomly sampled rows). This establishes the baseline for the 0.9.0 release and beyond.

**Results:**

| Metric | Score |
| --- | --- |
| Precision | 0.9688 |
| Recall | 0.8044 |
| F1 Score | 0.8790 |

## `0.9.0` (Context-Aware Heuristics)

Evaluated on the `ai4privacy/pii-masking-openpii-1.5m` dataset (validation split, 1000 randomly sampled rows) after introducing the `ContextualIdDetector` to catch synthetically generated IDs, non-Luhn credit cards, and postal codes based on surrounding semantic keywords.

**Results:**

| Metric | Score |
| --- | --- |
| Precision | 0.9511 |
| Recall | 0.8333 |
| F1 Score | 0.8883 |

## `1.0.0` (Strict Evaluation Baseline)

Evaluated on the `ai4privacy/pii-masking-openpii-1.5m` dataset (validation split, 1000 randomly sampled rows). This incorporates all ML and contextual heuristic enhancements. *Note: Earlier releases reported scores >90%, but those were generated under an obsolete scorer. This baseline uses one-to-one matching and exact entity types, while still crediting any positive span overlap; it is not exact-boundary scoring.*

**Results:**

| Metric | Score |
| --- | --- |
| Precision | 0.9141 |
| Recall | 0.5465 |
| F1 Score | 0.6840 |

## `1.10.0`

Evaluated on the `ai4privacy/pii-masking-openpii-1.5m` dataset (validation split, 1000 randomly sampled rows). This incorporates all ML calibration, boundary trimming, adaptive sliding window, and international trigger expansions.

**Results:**

| Metric | Score |
| --- | --- |
| Precision | 0.8425 |
| Recall | 0.6293 |
| F1 Score | 0.7205 |

## `1.20.0` (Strict Evaluation Baseline)

Evaluated on the `ai4privacy/pii-masking-openpii-1.5m` dataset (validation split, 1000 randomly sampled rows). This incorporates the final architectural overhaul removing the Llama backend and relying strictly on lightweight ONNX inference and advanced algorithmic heuristics.

**Results:**

| Metric | Score |
| --- | --- |
| Precision | 0.8587 |
| Recall | 0.8016 |
| F1 Score | 0.8292 |

## `1.26.0` (One-to-One Overlap & Entity-Type Match)

Evaluated on the English validation subset of `ai4privacy/pii-masking-openpii-1.5m` (pinned revision `a785eb528e28be2693c3718a27e066970de5dadb`, 1000 rows, seed 42) with ONNX ML and rules backends. Incorporates audited ensemble resolution, fail-closed observability, and verified evaluator reproducibility. Machine-readable record committed in `benchmarks/results/1.26.0_ai4privacy_validation_1000.json`.

**Results:**

| Metric | Score |
| --- | --- |
| Precision | 0.8611 |
| Recall | 0.8026 |
| F1 Score | 0.8308 |

**Counts:** True Positives: 4155, False Positives: 670, False Negatives: 1022, Out-of-Scope: 250.

## `1.34.0` (Quality Release Gate & Error Atlas Integration)

Evaluated against the pinned validation split (`a785eb528e28be2693c3718a27e066970de5dadb`, 1,000 samples) with the automated 5-criteria quality gate (`benchmarks/quality_gate.py`). Incorporates constrained BIO transition decoding, calibrated temperature scaling, and multi-backend evidence fusion.

**Results:**

| Metric | Score | Detail |
| --- | :---: | --- |
| **Precision** | `0.8608` | True Positives: 4,155, False Positives: 672 |
| **Recall** | `0.8026` | False Negatives: 1,022 |
| **F1 Score** | `0.8307` | Stable baseline match (`1.26.0`: `0.8308`) |
| **Exact Boundary F1** | `0.4899` | P: `0.5247`, R: `0.4593` (TP: 2,378, FP: 2,154, FN: 2,799) |
| **Macro F1** | `0.7701` | Average per document across 1,000 samples |
| **Character Masking** | `0.8136` | **91.73% precision** (56,131 / 68,992 sensitive chars masked) |
| **Unscored** | `250` | Out-of-scope labels safely ignored |

**Per-Entity Breakdown:**
- **EMAIL**: F1 `0.9982` (P: `0.9964`, R: `1.0000`, TP: 555, FP: 2, FN: 0)
- **PHONE**: F1 `0.9838` (P: `0.9953`, R: `0.9725`, TP: 424, FP: 2, FN: 12)
- **PAYMENT_CARD**: F1 `0.9745` (P: `0.9841`, R: `0.9650`, TP: 248, FP: 4, FN: 9)
- **NATIONAL_ID**: F1 `0.8749` (P: `0.7958`, R: `0.9716`, TP: 787, FP: 202, FN: 23)
- **LOCATION**: F1 `0.8176` (P: `0.8041`, R: `0.8316`, TP: 1,022, FP: 249, FN: 207)
- **PERSON**: F1 `0.7393` (P: `0.8482`, R: `0.6552`, TP: 1,106, FP: 198, FN: 582)
- **ORGANIZATION**: F1 `0.6667` (P: `0.5000`, R: `1.0000`, TP: 1, FP: 1, FN: 0)
- **TAX_ID**: F1 `0.1062` (P: `0.4800`, R: `0.0597`, TP: 12, FP: 13, FN: 189)

**Causal Error Distribution:**
- Boundary Mismatch: 1,777 (dominant error class)
- Conflict Loss: 850
- Label Confusion: 137
- Missing Candidate: 35
- Threshold Suppression: 0

See also the formal [Model Card](model_card.md) for full architecture specifications and hardware profiles.


