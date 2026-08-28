# Private Release Plan: Pseudonymize

## Current State
- **Just Completed:** `0.10.0` (ML Confidence Calibration & Dynamic Thresholding)
- **Current Baseline (0.10.0):** 
  - Precision: `0.9359`
  - Recall: `0.8686`
  - F1 Score: `0.9010`
  *(Measured against `ai4privacy/pii-masking-openpii-1.5m` validation split, 1000 samples).*

## Immediate Next Milestone: `0.11.0`
**Focus:** Ensemble Merging & Conflict Resolution

### Objective for the next session
Improve the resolution logic when deterministic rules and ML backends flag the same or overlapping text with different entity labels. The goal is to prevent duplicate or conflicting entity tags in the final output, improving precision and recall further.

### Hard Constraints (DO NOT VIOLATE)
1. **The 90% Benchmark Gate:** You are strictly forbidden from finalizing the `0.11.0` release unless `uv run python benchmarks/evaluate_quality.py --ml --samples 1000` proves that either Precision, Recall, or F1 has materially improved without degrading the others to an unacceptable level. The ultimate goal is to break the 90% flat barrier across all three.
2. **Strict Benchmark Integrity:** You must not hardcode regexes tailored to specific strings in the dataset. Heuristics must generalize.
3. **BLIND EVALUATION:** You must never inspect, print, or analyze the evaluation/holdout dataset (`validation` split of `ai4privacy/pii-masking-openpii-1.5m`) to find missed edge cases. If you need to debug False Positives or False Negatives to build heuristics, you MUST write temporary scripts to parse the `train` split exclusively. 
4. **Execution Context:** Use the `uv` toolchain for all checks.

### Instructions to resume
1. Review `src/pseudonymize/engine.py` and see how detections from multiple backends are currently merged.
2. Implement conflict resolution logic based on confidence, detector type, or span length.
3. Verify improvements using `benchmarks/train_eval.py`.
4. Run the benchmarks, format/lint, and execute the standard release pipeline in `docs/releasing.md`.