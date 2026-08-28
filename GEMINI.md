# pseudonymize maintainer instructions

## Project

This repository is a Python 3.11+ library and CLI for local-first PII pseudonymization for text, structured data, and LLM payloads. `uv` owns dependencies, packaging, scripts, and the lock file. The public package is `pseudonymize`.

Read the relevant implementation, tests, and documentation before editing.
Keep changes focused and preserve existing public interfaces, defaults, JSON
keys, environment variables, console scripts, and tool signatures through
the 0.1.x series as required by `docs/compatibility.md`.

- **Strict PII Scope:** The sole purpose of this package is PII pseudonymization. Any ML capabilities (like `LocalONNXPIIBackend`) must be explicitly framed, designed, and tested exclusively for detecting and pseudonymizing PII. Never treat, use, or document ML detection as a general-purpose NLP or entity extraction tool.

## Development

- Use the existing style and the simplest working implementation.
- Add a regression test for every bug fix and offline tests for new behavior.
- Update user-facing documentation and `CHANGELOG.md` for behavior changes.
- Do not edit `uv.lock` manually; use `uv` commands.
- Never expose or commit `.env` contents, passwords, credentials,
  tokens, captured request headers, or local service-account files.
- Preserve user changes in a dirty worktree. Do not reset, restore, or delete
  unrelated work.
- **Never use dummy models, fake artifacts, or excessive mocking for integration tests.** If an external model or binary is needed to test an inference pipeline, write a setup script or test fixture to dynamically download a real, lightweight version (e.g., a quantized BERT model) to a local cache directory excluded from version control. Tests must exercise actual logic against real weights.
- **Strict Benchmark Integrity:** You are absolutely forbidden from "cheating" the quality benchmarks. You must NEVER hardcode strings, names, or regexes designed specifically to patch failures found *only* in the benchmark dataset (e.g., `ai4privacy/pii-masking-200k`). You must NEVER fine-tune a model on the benchmark evaluation slice. All improvements to precision, recall, and F1 must stem from generalized heuristics, better token alignment, and robust ML calibration that apply to unseen, real-world text.
- **Adversarial Testing:** New tests must include extremely hard, adversarial edge cases (e.g., bidirectional overrides, deep nesting, escaped structures) to challenge the parsers and detectors.

Install and validate with:

```bash
uv sync --all-extras --all-groups --frozen
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
```

## Releases

Follow `docs/releasing.md` exactly. Use `/release:prepare X.Y.Z` to prepare a
candidate and `/release:verify` to validate it.

- Keep version files unchanged during ordinary development.
- For a release candidate, synchronize `pyproject.toml`, prepend `CHANGELOG.md`, and
  update README examples using only verified changes.
- Treat the Git tag, GitHub release, and built distributions as one immutable
  release. Never reuse a published version.
- You have explicit standing maintainer authorization to commit, tag, push, create GitHub releases, publish to PyPI, run tests, and check, approve, or close PRs when requested.
- Never bypass a failing check. Report the failure and preserve its output.
- Publish only from the exact commit that passed CI, using tag `vX.Y.Z`.

At handoff, state files changed, checks run, checks not run, and any external
actions still requiring maintainer approval.
