# Private Release Plan: Pseudonymize

## Current State
- **Just Completed:** `0.22.0` (Massive Recall Boost)
- **Current Baseline (0.22.0):** 
  - Precision: `0.9380`
  - Recall: `0.9468`
  - F1 Score: `0.9424`
  *(Measured against `ai4privacy/pii-masking-openpii-1.5m` validation split, 1000 samples).*

## Immediate Next Milestone: `0.13.0`
**Focus:** The 90% Benchmark Gate (Custom Fine-Tuning Pathways)

### Objective for the next session
The F1 score is hovering around 90.70%. The goal of 0.13.0 is to establish pathways to exceed this ceiling. This involves ensuring the ML backend is configurable enough for custom fine-tuning pathways (e.g. allowing users to provide custom model artifacts easily) or squeezing the last remaining false negative drops out of the pipeline to firmly secure the 90%+ baseline.

### Hard Constraints (DO NOT VIOLATE)
1. **The 90% Benchmark Gate:** You are strictly forbidden from finalizing the `0.13.0` release unless `uv run python benchmarks/evaluate_quality.py --ml --samples 1000` proves that either Precision, Recall, or F1 has materially improved without degrading the others to an unacceptable level. The ultimate goal is to break the 90% flat barrier across all three.
2. **Strict Benchmark Integrity:** You must not hardcode regexes tailored to specific strings in the dataset. Heuristics must generalize.
3. **BLIND EVALUATION:** You must never inspect, print, or analyze the evaluation/holdout dataset (`validation` split of `ai4privacy/pii-masking-openpii-1.5m`) to find missed edge cases. If you need to debug False Positives or False Negatives to build heuristics, you MUST write temporary scripts to parse the `train` split exclusively. 
4. **Execution Context:** Use the `uv` toolchain for all checks.

### Instructions to resume
1. Review `src/pseudonymize/backends/ml/onnx.py` and analyze the current ML inference limitations.
2. Review the remaining false negatives from the `benchmarks/train_eval.py` output. Look for systemic patterns (e.g. specific entity types like URL or STREET being missed by both ML and Rules).
3. Verify improvements using `benchmarks/train_eval.py`.
4. Run the benchmarks, format/lint, and execute the standard release pipeline in `docs/releasing.md`.