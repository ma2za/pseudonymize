# Private Release Plan: Pseudonymize

## Current State
- **Just Completed:** `0.11.0` (Ensemble Merging & Conflict Resolution)
- **Current Baseline (0.11.0):** 
  - Precision: `0.9486`
  - Recall: `0.8673`
  - F1 Score: `0.9061`
  *(Measured against `ai4privacy/pii-masking-openpii-1.5m` validation split, 1000 samples).*

## Immediate Next Milestone: `0.12.0`
**Focus:** Cross-Lingual & Typographical Hardening

### Objective for the next session
Fix detection drops caused by non-Latin scripts, CJK spacing, RTL text, and bidirectional text overrides. We need to ensure that adversarial Unicode characters (like BiDi overrides `\u202e`, zero-width spaces, etc.) do not cause the regex engines or the ML backend to miss PII.

### Hard Constraints (DO NOT VIOLATE)
1. **The 90% Benchmark Gate:** You are strictly forbidden from finalizing the `0.12.0` release unless `uv run python benchmarks/evaluate_quality.py --ml --samples 1000` proves that either Precision, Recall, or F1 has materially improved without degrading the others to an unacceptable level. The ultimate goal is to break the 90% flat barrier across all three.
2. **Strict Benchmark Integrity:** You must not hardcode regexes tailored to specific strings in the dataset. Heuristics must generalize.
3. **BLIND EVALUATION:** You must never inspect, print, or analyze the evaluation/holdout dataset (`validation` split of `ai4privacy/pii-masking-openpii-1.5m`) to find missed edge cases. If you need to debug False Positives or False Negatives to build heuristics, you MUST write temporary scripts to parse the `train` split exclusively. 
4. **Execution Context:** Use the `uv` toolchain for all checks.
5. **Span Offset Integrity:** If you strip characters before detection, ensure that the detection offsets still map correctly to the original un-normalized string.

### Instructions to resume
1. Review `src/pseudonymize/engine.py` and `src/pseudonymize/normalization.py`.
2. Implement cross-lingual and typographical hardening (handling BiDi, CJK, zero-width characters).
3. Verify improvements using `benchmarks/train_eval.py`.
4. Run the benchmarks, format/lint, and execute the standard release pipeline in `docs/releasing.md`.