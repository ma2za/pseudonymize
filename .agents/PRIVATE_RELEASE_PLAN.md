# Private Release Plan: Pseudonymize

## Current State
- **Just Completed:** `0.9.0` (Context-Aware Heuristics)
- **Current Baseline (0.9.0):** 
  - Precision: `0.9511`
  - Recall: `0.8333`
  - F1 Score: `0.8883`
  *(Measured against `ai4privacy/pii-masking-openpii-1.5m` validation split, 1000 samples).*

## Immediate Next Milestone: `0.10.0`
**Focus:** ML Confidence Calibration & Dynamic Thresholding

### Objective for the next session
Improve the DistilBERT ONNX confidence scores and thresholds. Currently, the ML backend has a hardcoded default minimum confidence. We need to tune this or introduce dynamic policy-based thresholds to boost recall without destroying our 95% precision. 

### Hard Constraints (DO NOT VIOLATE)
1. **The 90% Benchmark Gate:** You are strictly forbidden from finalizing the `0.10.0` release unless `uv run python benchmarks/evaluate_quality.py --ml --samples 1000` proves that either Precision, Recall, or F1 has materially improved without degrading the others to an unacceptable level. The ultimate goal is to break the 90% flat barrier across all three.
2. **Strict Benchmark Integrity:** You must not hardcode regexes tailored to specific strings in the dataset. Heuristics must generalize.
3. **Execution Context:** Use the `uv` toolchain for all checks.

### Instructions to resume
1. Review `src/pseudonymize/backends/ml/onnx.py` and see how confidence scores are extracted/applied from the ONNX logits.
2. Review `src/pseudonymize/policy.py` to see how `minimum_confidence` is currently passed to the backends.
3. Implement calibration, run the benchmarks, format/lint, and execute the standard release pipeline in `docs/releasing.md`.