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

## Active priority: honest benchmark improvement

This is the next engineering program. Read the `1.31.0` to `1.34.0` section of `ROADMAP.md` before
touching detector behavior. Do not jump directly to a new rule, lower threshold, model swap, or
ensemble weight.

### Current evidence and its limits

- Headline strict result: `0.8308` F1, `0.8611` precision, `0.8026` recall on 1,000 fixed English
  validation rows from pinned revision `a785eb528e28be2693c3718a27e066970de5dadb` of
  `ai4privacy/pii-masking-openpii-1.5m`.
- Previous result: `0.8292` F1. The observed delta is only `+0.0016`. There is no paired confidence
  interval, so the repository must not call that delta significant or evidence of a real gain.
- The aggregate `1.26.0` result is documented, but its machine-readable JSON artifact is not
  committed. Per-entity counts, exact hashes, and the row-level sufficient statistics needed for
  paired comparison are therefore not available from the repository alone.
- The active ONNX model is `onnx-community/multilang-pii-ner-ONNX`. Its model card identifies
  `ai4privacy/open-pii-masking-500k-ai4privacy` as training data. The evaluation corpus is a newer
  AI4Privacy family dataset. This does not prove literal row leakage, but it creates enough lineage
  risk that the headline score cannot be the sole generalization claim.
- The same fixed validation sample has informed many releases. It is now a regression set, not an
  untouched holdout. Future chats must not inspect its errors or use its score to choose code.
- The evaluator is strict at the entity level but matches any positive overlap after type agreement;
  the roadmap now requires exact-boundary metrics and explicit boundary-error reporting in addition
  to the historical metric. Do not silently redefine the old series.
- The adapter has several manually chosen interactions that have not been causally isolated:
  per-entity thresholds, runner-up promotion, context threshold halving, piecewise confidence
  remapping, punctuation-tolerant merge behavior, word-boundary expansion, and fixed ensemble
  weights. Treat each as an experimental factor, not an established optimization.

### Strict implementation order

#### 1. Recover and freeze the baseline

1. Search CI artifacts or prior local output for the exact `1.26.0` JSON record. If it cannot be
   recovered, rerun the documented pinned command without changing code, model files, policy,
   scorer, sample order, or supported labels.
2. Verify model/tokenizer/config SHA-256 values, dataset revision, package commit, Python/platform,
   sample count, policy configuration, TP/FP/FN/out-of-scope counts, and per-entity counts.
3. Store only the sanitized aggregate record in a versioned benchmark-results location. Never
   commit source text, annotation values, raw matched spans, or `--explain` output.
4. Reconcile `docs/benchmarks.md`, `docs/quality_benchmarks.md`, and the result artifact. The two
   documentation pages currently present overlapping histories and must not disagree.

Stop condition: if the baseline cannot be reproduced from pinned inputs, fix reproducibility before
any quality experiment. Do not approximate missing counts from rounded metrics.

#### 2. Make comparisons statistically and causally useful (`1.31.0`)

1. Extend `benchmarks/evaluate_quality.py` with privacy-safe per-row sufficient statistics: stable
   row hash, TP/FP/FN by entity, source/language/length buckets, and error category. Raw text and
   values remain local only.
2. Add a deterministic artifact comparator with paired document-level bootstrap resampling, F1
   delta, and 95% confidence interval. Refuse comparison when row manifests, scorer, label map,
   model hashes, policy, or dataset revision differ.
3. Preserve the historical overlap-based strict metric under its existing name for continuity.
   Add separate exact-boundary/exact-label, boundary-only, label-confusion, character-masking,
   macro, per-entity, per-language, and per-source metrics.
4. Instrument benchmark-only candidate lifecycle counts across backend emission, backend threshold,
   policy threshold, overlap resolution, and final output. Aggregate failures into missing
   candidate, suppression, wrong label, wrong boundary, and conflict loss.
5. Build immutable grouped development, calibration, and internal-test manifests from the pinned
   training split. Group/deduplicate by normalized value-masked template or source lineage, store
   only identifiers/hashes, and prove that near-duplicate groups do not cross partitions.
6. Audit overlap between those manifests, the validation manifests, and what is known about the
   older AI4Privacy 500k model-training corpus. Record unknowns explicitly; absence of proof is not
   proof of independence.
7. Run the full development ablation matrix named in `ROADMAP.md`. The output must show how many
   TP/FP/FN each component adds or removes, by entity and error class, on identical rows.

Expected first files: `benchmarks/evaluate_quality.py`, a focused comparator module or script,
`tests/unit/test_quality_evaluator.py`, additional comparator tests, sanitized manifests/results,
`docs/benchmarks.md`, `ROADMAP.md`, and this handover. Keep benchmark-only instrumentation out of
the public runtime API unless a separate API design is justified.

#### 3. Fit calibration and decoding on development data only (`1.32.0`)

Proceed only after the error atlas exists. Measure raw-logit calibration, fit a global temperature
first, require support and grouped cross-validation before per-entity calibration, select thresholds
under predeclared precision/recall constraints, and compare existing versus BIO/BILOU-constrained
decoding. Remove heuristics that do not survive ablation. Never derive constants from validation.

#### 4. Run a licensed, reproducible model bake-off (`1.33.0`)

Proceed only if the error atlas shows the current model is the bottleneck. Every candidate needs a
pinned revision, hashes, training lineage, compatible license, ONNX/export reproducibility,
supported-label mapping, CPU latency, memory, and size. Compare the existing model, at least one
independent-lineage token model, and a span-oriented candidate such as GLiNER when legally and
operationally viable. Piiranha's published model is non-commercial/no-derivatives and must not be
assumed suitable for redistribution or default use.

#### 5. Run one blind release evaluation (`1.34.0`)

Freeze the code and acceptance criteria, then run the historical 1,000-row sample, a larger grouped
AI4Privacy validation manifest, an independent multi-source corpus such as PIIMB, every claimed
language, adversarial precision cases, and timing/memory checks. A behavior change ships only if the
primary paired 95% F1-delta interval is positive, protected entity classes do not materially regress,
and the improvement survives outside the AI4Privacy family. A failed behavior change is removed;
the measurement tooling may still ship.

### Anti-cheating and anti-overfitting rules

- Never read validation examples to author a rule, exception, vocabulary entry, boundary repair,
  or context phrase. Use grouped training-derived development data and independently authored
  adversarial cases.
- Never move an unsupported label out of scope, loosen matching, change entity mapping, change the
  sample, quote span-only results, or enable invalid checksums to improve the headline number.
- Never run broad threshold/model searches against a release lockbox. Pre-register a bounded
  candidate set and preserve all attempted results, including regressions.
- Never accept an aggregate gain that is carried by one frequent entity while high-risk or rare
  entities regress. Inspect counts and confidence intervals, not rounded F1 alone.
- Never merge a model whose training data or license is unknown. Same-family synthetic evaluation
  is supporting evidence, not independent proof.
- Never add a second ML model merely because an ensemble point estimate rises. Require calibrated,
  complementary errors and account for latency, memory, wheel/extras, offline behavior, and
  determinism.
- Never commit raw PII or source examples in diagnostic artifacts. The public corpus is synthetic,
  but the tooling must remain safe when used with private evaluation data.

### Research already checked

Primary sources and their implications are recorded in `ROADMAP.md`: the OpenPII 1.5M and PIIMB
dataset cards, the current ONNX model card, Presidio's inspectable recognizer/context design,
temperature scaling research, NER boundary-smoothing research, GLiNER, and paired bootstrap
significance testing. Future chats should use those as starting points, then verify model revisions,
licenses, and datasets again because those external facts can change.

## Current release state

`1.26.0` is published and tagged (`v1.26.0`).
`1.27.0` is the active development version. The immediate priority is the `1.31.0` benchmark
integrity and causal error atlas program.

Before this roadmap/handover update, `main` was clean at `71513da` and matched `origin/main`.
Relevant integrated commits are:

- `8ec7e11 chore: restore dependency-free base release contract`
- `27e2be8 fix: harden optional remote and benchmark paths`
- `4b17227 chore: complete 1.26.0 contract evidence and 1.27.0 evaluation safety gates`
- `7a199f3 feat: implement measured multilingual contextual detection and bounded scoring`
- `1b093b3 feat: audit ONNX token alignment, calibrate thresholds, and harden coreference`
- `71513da feat: resolve audit remediation blockers and update 1.26.0 benchmark baseline`

The roadmap/handover edits described here are documentation changes after that commit. Always run
`git status --short` first and inspect the actual diff. Do not infer release publication from an
implemented milestone or from this commit list.

## Work completed in `1.26.0` through `1.30.0`

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
- Audited ensemble overlap resolution with synchronized remote weighting, immutable detector
  weights, provenance-based conflict/topology tests, permutation invariance, and strict contiguous
  same-type adjacency merging.
- Hardened observability with fresh-process optional-import and socket isolation, nested-value
  sanitization, and immutable-container fail-closed behavior. No latency claim is attached.
- Corrected deployment guidance so key rotation, mapping encryption/storage/retention, and memory
  handling are explicitly application/operator responsibilities rather than package guarantees.

## Remaining work, in strict order

1. Finish and evidence the current release candidate without adding scope. Verify public API,
   package, docs, supported-platform, and clean-wheel gates.
2. Execute `1.31.0` measurement integrity and error-atlas work. This is the immediate engineering
   priority and must not change detector behavior except to correct a proven measurement defect.
3. Use the resulting ranked error causes to decide whether `1.32.0` calibration/decoding work is
   justified. Pre-register experiments and fit on grouped development/calibration data only.
4. Run the `1.33.0` model/hybrid bake-off only if evidence says model capacity or error
   complementarity is the bottleneck.
5. Run the `1.34.0` blind generalization gate once after freezing the candidate. Ship no claimed
   benchmark improvement without paired uncertainty and independent-corpus support.

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
