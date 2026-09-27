# Model Card: Multilingual PII Detection Backend

## Model Overview
- **Identifier:** `multilang-pii-ner-onnx-int8`
- **Repository:** [`onnx-community/multilang-pii-ner-ONNX`](https://huggingface.co/onnx-community/multilang-pii-ner-ONNX)
- **Base Architecture:** XLM-RoBERTa Token Classifier
- **Quantization:** INT8 Dynamic Quantization
- **Artifact Hashes:**
  - `config.json`: `3503fb27021640b315b1e7636933f7df9c209746251cae4975bdef46be4e8158`
  - `tokenizer.json`: `8373f9cd3d27591e1924426bcc1c8799bc5a9affc4fc857982c5d66668dd1f41`
  - `model_int8.onnx`: `1d02f3829ad90d95dea5e64d35f5528f96d7b223c1e056a96075c6229a484356`
- **License:** Apache-2.0 (Permissive, commercial redistribution approved)

## Training Lineage
- **Dataset:** AI4Privacy Multilingual Synthetic Corpus (~500,000 synthetic documents).
- **Supported Languages:** English (`en`), German (`de`), French (`fr`), Italian (`it`), Spanish (`es`), Portuguese (`pt`), Dutch (`nl`), Chinese (`zh`).

## Verified Quality Metrics

### Strict Typed Evaluation (AI4Privacy Validation Split, 1,000 samples)
- **Dataset Revision:** `a785eb528e28be2693c3718a27e066970de5dadb`
- **Precision:** `0.8611`
- **Recall:** `0.8026`
- **F1 Score:** `0.8308`
- **Counts:** True Positives: 4,155, False Positives: 670, False Negatives: 1,022, Out-of-Scope: 250.

### External Multi-Source Evaluation (PIIMB Character-Level Zero-Shot)
- **Label-Agnostic Character Precision:** `0.8840`
- **Label-Agnostic Character Recall:** `0.8420`
- **Label-Agnostic Character F1:** `0.8625`

## Operational Profile
- **Size on Disk:** ~285 MB
- **Peak Memory (RSS):** ~420 MB
- **CPU Inference Latency:** ~85 ms per 1,000 characters
- **Execution Providers:** `CPUExecutionProvider`

## Known Limitations and Failure Modes
From the Causal Error Atlas analysis:
1. **Rare Name Out-of-Vocabulary:** Extreme foreign or rare proper nouns outside training vocabulary can result in missing candidate omissions.
2. **Boundary Sensitivity:** Without constrained BIO decoding, adjacent entities of the same type separated only by whitespace risk merging.
3. **Hard Safety Separation:** Mathematical identifiers (credit cards, IBANs, tax IDs) are handled by deterministic algorithmic detectors with hard precedence over model outputs.
