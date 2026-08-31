# Private Release Plan: Pseudonymize

## Current State
- **Just Completed:** `0.26.0` (Expanded Local ML (GGUF/llama.cpp))
- **Current Baseline (0.26.0):** 
  - Precision: `0.9406`
  - Recall: `0.9406`
  - F1 Score: `0.9406`
  *(Measured against `ai4privacy/pii-masking-openpii-1.5m` validation split, 100 samples).*

## Immediate Next Milestone: `0.27.0`
**Focus:** Local Microservice DLP Endpoint

### Objective for the next session
We need to provide an optional `fastapi` extra that exposes the `pseudonymize` engine as a lightweight, stateless REST API. This acts as a local DLP microservice for polyglot applications.

### Hard Constraints (DO NOT VIOLATE)
1. **Quality Maintenance:** You are strictly forbidden from finalizing the `0.27.0` release if `uv run python benchmarks/evaluate_quality.py --ml --samples 1000` proves that Precision, Recall, or F1 scores have materially degraded.
2. **Execution Context:** Use the `uv` toolchain for all checks.

### Instructions to resume
1. Design a simple FastAPI application in `src/pseudonymize/server.py`.
2. Ensure you use `fastapi` and `uvicorn`. Add the required dependency to an `[api]` extra in `pyproject.toml`.
3. Add rigorous test cases for the API endpoints.
4. Run all tests, formatting, and standard release validation steps.