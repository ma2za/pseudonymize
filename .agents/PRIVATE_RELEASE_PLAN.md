# Private Release Plan: Pseudonymize

## Current State
- **Just Completed:** `0.27.0` (Local Microservice DLP Endpoint)
- **Current Baseline (0.27.0):** 
  - Precision: `0.9406`
  - Recall: `0.9406`
  - F1 Score: `0.9406`
  *(Measured against `ai4privacy/pii-masking-openpii-1.5m` validation split, 100 samples).*

## Immediate Next Milestone: `1.0.0`
**Focus:** Mature Compatibility Commitment

### Objective for the next session
The final push to `1.0.0`. We need to freeze the public API, enforce `__all__` exports, run the full 10,000 sample benchmark one last time, and officially guarantee semantic versioning backward compatibility going forward.

### Hard Constraints (DO NOT VIOLATE)
1. **Quality Maintenance:** You are strictly forbidden from finalizing the `1.0.0` release if `uv run python benchmarks/evaluate_quality.py --ml --samples 1000` proves that Precision, Recall, or F1 scores have materially degraded.
2. **Execution Context:** Use the `uv` toolchain for all checks.

### Instructions to resume
1. Audit `__all__` in `src/pseudonymize/__init__.py`.
2. Final review of test coverage and `mypy --strict` compliance.
3. Run all tests, formatting, and standard release validation steps.