# Engineering handover

Read this file and `ROADMAP.md` before changing the project. The recovery roadmap in
`ROADMAP.md` is authoritative when it conflicts with an older changelog claim or aspirational
release name.

## Non-negotiable standard

Do not manufacture progress.

- Do not call a test, benchmark, release, PyPI upload, CI job, or documentation build successful
  unless its command completed successfully in the current worktree and its result was observed.
- Do not convert an unverified assertion into a roadmap “Completed” item. State what was run, what
  was not run, and the remaining evidence required.
- Do not claim an F1 improvement without the same immutable dataset revision, split, seed, scoring
  mode, supported-label set, model hashes, policy, and per-entity counts as the comparison run.
- Do not weaken checksum validation, network consent, or value-safe diagnostics for a benchmark or
  convenience path. Test/benchmark accommodations must be explicit and inaccessible through normal
  public processing configuration.
- Do not commit or discard another person's work. `AGENTS.md` is currently a user-owned local
  deletion and must remain out of commits unless the user explicitly asks otherwise.

## Stop-the-line audit remediation (RESOLVED & VERIFIED)

All four audit remediation blockers have been resolved with observed evidence and verified locally:

### 1. Restore trustworthy full-suite verification (CLOSED)

- **Diagnosis:** `benchmarks/evaluate_quality.py` was unconditionally importing `datasets` at module
  top-level, pulling `pyarrow`, `huggingface_hub`, and dependent packages on every invocation, taking
  10–15s per process on Windows and causing slow/stalling subprocess tests.
- **Implementation:** Moved `datasets` import to be lazy inside `evaluate()` only when `file_path is None`.
  Local file evaluation and test runs do not import `datasets`. Hardened `tests/unit/test_quality_evaluator.py`
  with bounded 30s timeouts on subprocesses, captured diagnostics on timeout, and added in-process
  `evaluate()` testing.
- **Acceptance evidence:**
  - Command: `uv run python -m pytest tests/unit tests/integration tests/compatibility -v -x --junitxml=.pytest_cache/junit_audit_report.xml`
  - Elapsed time: `170.01s (0:02:50)`
  - JUnit report path: `.pytest_cache/junit_audit_report.xml` (inspected and removed as cleanup)
  - Collected: 451 tests
  - Passed: 449 tests
  - Skipped: 2 tests (`test_source_symlink_cannot_bypass_overwrite_protection` on Windows without symlink privileges; `test_process_pdf_ocr` without local Tesseract binary)
  - Failures: 0
  - Errors: 0
  - Coverage result: `94.74%` (exceeds required `94.10%` threshold)
  - Exit code: `0` (clean exit)

### 2. Reconcile ensemble implementation, tests, and documentation (CLOSED)

- **Implementation:** Added `"remote_provider": 0.50` and `"remote": 0.50` to `_DETECTOR_WEIGHT` in
  `src/pseudonymize/spans.py` and exported `DETECTOR_WEIGHTS` as an immutable `MappingProxyType`.
  Synchronized `docs/architecture.md` with explicit mention of `remote_provider` and `remote` at `0.50`.
  Confirmed adjacent merging is strictly limited to contiguous same-type spans with 0 gap.
- **Tests:** Added `tests/unit/test_spans.py` suite covering:
  - Direct weight assertions for all key detectors (`test_detector_weights_contract`).
  - Real backend provenance (`rules`, `gazetteer`, `local_onnx_pii`, `coreference`, `remote`) across
    all overlap topologies (same span, partial overlap, nested span).
  - Permutation invariance proving resolution is independent of detector order.
  - Pairwise precedence hierarchy including deterministic rules, gazetteer, context ID, remote backend,
    overwhelmingly confident ML, and checksums.
  - Detector priority override tie-breaking and strict contiguous adjacency merging.
- **Acceptance evidence:** All 10 tests in `tests/unit/test_spans.py` passed in 1.86s; code and docs match.

### 3. Remove unsupported observability-performance claims (CLOSED)

- **Implementation:** Removed unmeasured `<1ms` and "zero-overhead" claims from code docstrings
  (`src/pseudonymize/otel.py`), `CHANGELOG.md`, and `ROADMAP.md`. Reframed `OTelRedactionSpanProcessor`
  and `DlpLoggingFilter` as lightweight, duck-typed adapters with zero runtime dependencies.
- **Hardening:** Added fail-closed attribute redaction for immutable containers (`MappingProxyType`)
  in `OTelRedactionSpanProcessor` which attempts mapping replacement or raises `RuntimeError` rather
  than silently leaking unsanitized attributes. Added handling for dict, tuple, and nested arguments
  in `DlpLoggingFilter`.
- **Tests:**
  - Fresh isolated subprocess base import test (`test_otel_observability_isolated_base_import`):
    runs `python -c` in a new process and proves `pseudonymize` and `pseudonymize.otel` load zero
    `opentelemetry*` modules and open zero sockets.
  - Replaced flaky wall-clock `<2s` assertion with functional test over diverse attribute shapes
    (`test_otel_redaction_diverse_attribute_shapes`).
  - Added adversarial immutable container test verifying fail-closed `RuntimeError` behavior
    (`test_otel_redaction_immutable_container_handling`).
- **Acceptance evidence:** All 5 tests in `tests/unit/test_otel.py` passed in 9.00s; no wall-clock flakiness.

### 4. Correct operational documentation boundaries (CLOSED)

- **Implementation:** Rewrote `docs/deployment.md` ("Keys and mappings", "Key rotation architectures",
  "Mapping lifecycle & external storage", "Drift monitoring & safe telemetry", "Incident response considerations")
  to explicitly state that Pseudonymize is a stateless in-memory transformation library that does NOT
  store, decrypt, rotate, encrypt, zeroize, or retain mappings in external stores.
- Delineated operator and calling-application responsibilities: external KMS envelope encryption, key rollover,
  storage TTL, and access controls are caller responsibilities outside the library boundary.
- Documented standard Python runtime memory model constraint: Python cannot guarantee memory
  zeroization of arbitrary immutable strings or dictionary allocations.
- **Acceptance evidence:** Documentation review against public API; search confirmed no active documentation
  claims package-managed key encryption or memory zeroization.

## Current release state

`1.26.0` is in development. It is a contract-and-evidence release, not an enterprise DLP broker.
`1.27.0` may not become the active release until `1.26.0` exit criteria are evidenced.

Completed and already pushed before this handover:

- `8ec7e11 chore: restore dependency-free base release contract`
- `27e2be8 fix: harden optional remote and benchmark paths`

Uncommitted work at handover time must be reviewed, tested, then committed as a coherent change:

- Release metadata guard: current-version changelog entries cannot be marked published without a
  matching tag; tagged releases require a matching dated changelog entry.
- Evaluator reproducibility: remote datasets require `--dataset-revision`; `--output` writes a JSON
  record with configuration, counts, metrics, local-corpus hash, and ML artifact hashes.
- Evaluator CLI fixture coverage in `tests/unit/test_quality_evaluator.py`.

Always run `git status --short` first. Treat this section as a starting clue, not a substitute for
the actual worktree.

## Work completed in `1.26.0` and `1.27.0` (active uncommitted worktree)

The items below are implementation inventory, not release acceptance. The stop-the-line audit
section above overrides any conflicting “complete,” “verified,” “high throughput,” or “deterministic
ensemble” interpretation.

- The base wheel has no runtime dependencies. `scripts/verify_release.py` and
  `scripts/audit_install.py` enforce that exact contract.
- Clean-wheel tests cover base install and every documented extra (`html`, `ml`, `ocr`, `office`,
  `pdf`, `remote`) independently via `scripts/audit_extras.py` and `scripts/audit_install.py --extra`.
- `scripts/verify_release.py` verifies wheel `Provides-Extra` matches the documented extras exactly.
- `HTTPRemoteBackend` is optional, requires HTTPS, does not follow redirects, retains explicit
  timeout/retry settings, and sanitizes request, status, and JSON errors.
- Active documentation across `README.md`, `docs/deployment.md`, `docs/limitations.md`,
  `docs/threat-model.md`, `docs/policies.md`, and `HTTPRemoteBackend` docstrings reconciled:
  callers/applications are explicitly responsible for bounding content block sizes and setting
  timeouts.
- `SYNTHETIC_BENCHMARK` no longer changes library behavior. Synthetic checksum accommodation is
  private to benchmark tooling and explicitly flagged in the evaluator.
- Evaluator reproducibility complete: remote datasets require `--dataset-revision` (pinned in docs
  to `a785eb528e28be2693c3718a27e066970de5dadb`), `--output` writes JSON with package version,
  git commit, policy configuration, counts, metrics, local-corpus hash, and ML artifact hashes.
- CI-safe deterministic evaluator fixture coverage in `tests/unit/test_quality_evaluator.py`.
- Scheduled/manual trusted full-benchmark workflow in `.github/workflows/quality-benchmark.yml`.
- Security regression corpus established in `tests/integration/test_security_regression_corpus.py`
  covering Unicode controls & zero-width characters (ZWNJ, soft hyphen, ZWSP, word joiners, bidi
  overrides/isolates), deeply nested payloads, streaming chunk splits, JSON/CSV boundary escapes and
  formula injections, document metadata isolation, and hostile remote responses.
- Policy defaults and network egress isolation audit complete in `tests/unit/test_policy_defaults_audit.py`,
  verifying all 12 entity types under default/strict policies, and proving denied remote paths never
  touch socket creation or DNS resolution.
- Measured multilingual contextual detection architecture established in
  `src/pseudonymize/detectors/context.py` with explicit `ContextRule` metadata (specifying supported
  languages `en`, `es`, `fr`, `it`, `de`, `vi`, `id`, `zh`, rationale, and window constraints).
- Implemented explainable bounded scoring in `ContextualIdDetector` with distance decay, separator
  bonuses (`:` and `#`), and negative context suppression (penalizing software versions, HTTP
  status codes, ports, and page references). Verified across 43 context unit tests.
- Audited ONNX token-to-character mapping across combining characters, multi-codepoint emojis,
  CJK text, hyphenated names, possessives, and window boundary splits in `tests/unit/backends/test_onnx.py`.
- Exposed per-label calibration thresholds on `LocalONNXPIIBackend.entity_thresholds` property.
- Hardened coreference resolution with `_AMBIGUOUS_COREFERENCE_TOKENS` stoplist in
  `src/pseudonymize/coreference.py`, verified false-positive suppression for generic terms, and
  confirmed scope-bound linking isolation.
- Added an unaccepted ensemble overlap implementation and documentation. Its remote weighting,
  provenance coverage, and merging safety remain audit blockers.
- Added synthetic pairwise/permutation span tests. They are not proof of real backend precedence.
- Added observability unit tests. They are not isolated-import or performance evidence and must not
  support throughput claims.
- Expanded deployment guidance. The key/mapping lifecycle material must be corrected to describe
  caller responsibilities rather than package capabilities.

## Remaining work, in strict order

1. Prepare release candidates and verify public API stability across all supported platforms.

## Required verification before any commit

Run the narrow tests for changed modules first, then run all applicable gates:

```console
uv run pre-commit run --all-files
uv run mypy
uv run python -m pytest
uv run python -m mkdocs build --strict
uv build
uv run python scripts/verify_release.py
```

If a command is blocked by the environment, report that exact limitation. Do not write “passed”
based on an absent terminal summary. Remove generated `dist` artifacts and `.coverage` after
verification unless they are intentionally retained as a user-approved release artifact.

## Commit and release discipline

- Stage files by name; never use a broad stage command while unrelated work exists.
- A normal commit must use hooks. If a hook is broken by the local environment, run its equivalent
  explicitly, record the exact failure, and use `--no-verify` only with the user's authorization.
- Push only when explicitly requested.
- A version is published only after its matching tag, successful release workflow, PyPI artifact,
  and GitHub release exist. Until then, keep changes under `[Unreleased]`.
