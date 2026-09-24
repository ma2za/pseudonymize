# Release roadmap

The roadmap is intentionally staged. Each release must leave the core usable, documented, and
publishable without requiring unfinished later layers.

## Current position

| Release | Status | Outcome |
| --- | --- | --- |
| `0.1.0` | Published | First stable text and machine-readable release |
| `0.2.0` | Published | Optional local machine learning identification for PII |
| `0.3.0` | Published | Document inspection (PDF, DOCX, XLSX, PPTX) |
| `0.4.0` | Published | Format-preserving documents |
| `0.5.0` | Published | OCR and scanned documents |
| `0.6.0` | Published | Remote detection |
| `0.6.1` | Published | Italian identifiers, PDF spans, and inspection fixes |
| `0.7.0` | Published | Real-world corpus benchmarking |
| `0.8.0` | Published | Detection boundary and tokenization alignment |
| `0.9.0` | Published | Context-aware heuristics |
| `0.10.0` | Published | ML confidence calibration |
| `0.11.0` | Published | Ensemble merging and conflict resolution |
| `0.12.0` | Published | Cross-lingual and typographical hardening |
| `0.13.0` | Published | The 90% benchmark gate |
| `0.14.0` | Published | Adversarial document defenses and exhaustive metadata |
| `0.15.0` | Published | ML and heuristic detection enhancements |
| `0.16.0` | Published | Advanced OCR degradation handling |
| `0.17.0` | Published | Contextual identifier and sub-word boundary robustness |
| `0.18.0` | Published | Contextual Heuristic Augmentation |
| `1.0.0`  | Published | Mature compatibility commitment and type-aware 1-to-1 overlap scoring |
| `1.20.0` | Published | Stable evaluation baseline achievement (0.8292 F1) |
| `1.21.0` | Published | Scale & Integration (Batched Vectorization & LRU Caching Fast-Paths) |
| `1.22.0` | Published | Next-Generation Semantic Recall & Schema-Preserving Agent Sanitation (MCP) |
| `1.23.0` | Published | Ecosystem Integration & Regional EU Identifier Depth (German Steuer-IdNr, Spanish NIF/NIE/CIF) |
| `1.24.0` | Published | Observability & Distributed DLP Adapter (OpenTelemetry & Logging Integration) |
| `1.25.0` | Published | Distributed Scaling, Property Test Resilience & Pre-Commit Verification |
| `1.26.0` | Published | Contract reconciliation and release-proof baseline |
| `1.27.0` | Planned | Reproducible evaluation, production-safety hardening, and detector evidence |
| `1.28.0` | Planned | Measured multilingual contextual recall improvements |
| `1.29.0` | Planned | ML calibration, entity linking, and robust boundary alignment |
| `1.30.0` | Planned | Ensemble conflict resolution only if it improves held-out metrics |
| `1.31.0` | Next priority | Benchmark integrity, error atlas, and contamination controls |
| `1.32.0` | Planned | Development-only calibration and constrained span decoding |
| `1.33.0` | Planned | Reproducible model and hybrid-ensemble bake-off |
| `1.34.0` | Planned | Independent generalization proof and quality release gate |

Alpha releases optimize for the cleanest safe architecture, not backward compatibility. They may
remove, rename, or replace public APIs without aliases or shims. Material changes are documented,
but compatibility guarantees start only with `0.1.0`.

## Release gate for every milestone

- Ruff formatting and linting pass.
- Strict mypy passes for source, tests, benchmarks, and scripts.
- Supported Python versions pass on Linux, macOS, and Windows.
- Branch coverage meets the release floor and never falls below the previous tagged baseline.
  `pyproject.toml` is the source of truth; its current enforced floor is 94.10%.
- Property, contract, clean-wheel, documentation, and packaging checks pass.
- The base wheel remains typed. Its runtime-dependency policy exactly matches
  `pyproject.toml`, wheel metadata, installed-wheel audit output, and public documentation.
- Importing `pseudonymize` does not load optional document, OCR, model, or HTTP packages.
- Reports, warnings, exceptions, logs, CLI output, and representations do not expose matched
  values.
- New tests add meaningful failure modes: realistic workflows, boundary conditions, interacting
  features, malformed inputs, and adversarial cases.
- **Strict Benchmark Validation:** The `evaluate_quality.py` benchmark must be executed against the holdout slice. Precision, Recall, and F1 scores MUST be proven to legitimately improve over the previous baseline before any release between 0.8.0 and 0.13.0 can be finalized.
- Release artifacts install cleanly and the installed wheel passes API and CLI smoke tests.

- Coverage alone is not a quality target. A release should become harder to fake with an incomplete
  or unsafe implementation.
- Tests must be meaningful and execute actual logic. Do not use dummy artifacts, toy models, or mock inference. Specifically, optional backends (like ONNX ML) must be tested against real, dynamically downloaded lightweight model artifacts (e.g., quantized BERT) cached outside version control to rigorously verify the true inference pipeline for PII pseudonymization. ML features are strictly limited to PII and must never be developed or presented as general-purpose NLP tools.

## Recovery roadmap: `1.26.0` onward

This section is the operating plan for a fresh implementation chat. It takes precedence over
aspirational feature names elsewhere in this file. Do not start a new detector, provider, or
enterprise integration while an earlier release's exit criteria are unmet.

`HANDOVER.md` records the active worktree and required evidence protocol. Update it whenever work
is handed off, a release gate changes, or an uncommitted implementation slice changes materially.

### Evidence discipline

- “Completed” means the implementation, focused tests, and relevant static checks have passed and
  are named in the handover. It does not mean unrun CI, packaging, external benchmarks, or release
  publication passed.
- A command with missing, truncated, or ambiguous output is not proof of success. Rerun it in an
  observable form or record it as unverified.
- Never merge, publish, or advertise a quality/security claim on coverage alone. Preserve the raw
  command, immutable inputs, machine-readable output, and per-entity counts.
- Preserve unrelated worktree changes. Stage named files, inspect the staged diff, and seek the
  user's direction before committing or discarding user-owned changes.

### Stop-the-line audit remediation (RESOLVED & VERIFIED)

All four blockers have been resolved with observed evidence recorded in `HANDOVER.md`:
1. **Full-suite observability blocker (CLOSED):** Evaluator made lazy; bounded timeouts and captured diagnostics added; full test suite ran with observable JUnit XML report: 451 collected, 449 passed, 2 skipped, 0 failures, 0 errors, 94.74% coverage, clean exit code 0.
2. **Ensemble-contract blocker (CLOSED):** `remote_provider` / `remote` weight reconciled to 0.50 in `src/pseudonymize/spans.py` (`DETECTOR_WEIGHTS`) and `docs/architecture.md`; provenance-based tests across rules/gazetteer/ONNX/coreference/remote and all topologies pass.
3. **Observability-claim blocker (CLOSED):** Unsubstantiated `<1ms` and "zero-overhead" claims removed; isolated subprocess base import test proves zero telemetry modules loaded and no sockets opened; fail-closed immutable container and nested collection handling verified.
4. **Operational-boundary blocker (CLOSED):** Deployment guidance reframed to explicitly delineate caller/operator responsibilities (KMS envelope encryption, key rotation, TTL retention, and Python memory constraints) from package boundaries.

### Baseline facts to preserve

- The package is a pseudonymization boundary, not anonymization, compliance certification, or an
  enterprise DLP system.
- The published quality baseline is 0.8292 F1 (precision 0.8587, recall 0.8016) on 1,000 sampled
  validation rows of `ai4privacy/pii-masking-openpii-1.5m`, with one-to-one matching, exact entity
  types, and any positive boundary overlap. It is a point-in-time measurement, not an exact-boundary
  result or a guarantee.
- The base distribution declares no runtime dependencies. Optional remote support declares
  `httpx`; the base package remains dependency-free, while the project still ships an optional
  HTTP provider.
- `HTTPRemoteBackend` sends raw block text to its configured endpoint only after the engine's
  explicit network-policy checks. Its presence means remote processing is a shipped capability,
  even if no hosted service is operated by this project.
- Checksum validation remains enabled in normal library processing. Synthetic benchmark diagnostics
  may use a private detector configuration through the explicit benchmark flag only.

### Working rules for fresh chats

1. Read `pyproject.toml`, `README.md`, `VISION.md`, `docs/limitations.md`, this roadmap, and the
   affected implementation and tests before editing.
2. Treat `pyproject.toml`, built wheel metadata, and installed-wheel behavior as authoritative for
   packaging claims. Treat a reproducibly rerunnable benchmark command and its raw result as
   authoritative for quality claims.
3. Do not add a feature merely because it appears in an old changelog or roadmap entry. Verify it
   exists, is covered, is packaged, and is documented accurately.
4. Preserve the no-raw-value rule for public reports, logs, exceptions, warnings, CLI diagnostics,
   telemetry, and object representations. Tests may use synthetic values only.
5. Make changes in small independently releasable units. Every behavior change needs positive,
   negative, boundary, Unicode, adversarial, and interaction coverage appropriate to its risk.
6. A quality change may ship only when it improves the fixed held-out evaluation with per-entity
   counts and a committed command/configuration record. Do not claim improvement from a changed
   scoring rule, sample, label set, model artifact, or environment variable.

### `1.26.0`: make the contract true

Goal: remove the gap between what the project says, what installation declares, and what the wheel
does. This release is documentation, packaging, and safety work, not an enterprise broker.

Required work:

1. Choose and document one base dependency policy.
   - Completed: base package has zero runtime dependencies. `scripts/verify_release.py` and
     `scripts/audit_install.py` enforce dependency-free base contract and declared extras.
   - Clean-wheel tests cover base install and every documented extra (`html`, `ml`, `ocr`,
     `office`, `pdf`, `remote`) independently via `scripts/audit_extras.py`.
2. Resolve the remote-backend contract.
   - Completed: `HTTPRemoteBackend` requires HTTPS, disables redirects, preserves bounded
     timeout/retry configuration, sanitizes transport/status/JSON errors, and has unit coverage
     for its outbound payload, authentication, HTTPS rejection, and diagnostic safety.
   - Documented in README, API docs, threat model, dependency policy, and limitations:
     configured endpoints receive raw content blocks, outbound fields are identified, redirects
     are denied, and caller responsibility for bounding payload sizes and configuring timeouts
     is explicitly specified.
3. Remove contradictory release checks.
   - Completed: `scripts/verify_release.py` and `scripts/audit_install.py` enforce the selected base
     dependency policy and declared extras rather than contain no-op or misleading checks.
   - Coverage floor is maintained consistently at 94.10% sourced from `pyproject.toml`.
4. Fix release metadata discipline.
   - Completed: development verification rejects a changelog entry that marks the current version
     as published; tagged verification requires a matching dated changelog entry.
   - A version becomes “Published” only after its matching `v<version>` tag, successful release
     workflow, PyPI artifact, and GitHub release exist.
   - Unreleased work is maintained under `[Unreleased]`.
5. Constrain benchmark-only bypasses.
   - Completed: removed `SYNTHETIC_BENCHMARK`; normal detectors ignore that environment variable.
     Synthetic analysis configures private detector state directly, while the evaluator exposes an
     explicit `--allow-unverified-checksums` flag whose results are not baseline-comparable.

Exit criteria:

- README, vision, roadmap, package metadata, generated wheel metadata, and installed behavior all
  state the same dependency and remote-processing contract.
- Clean-wheel tests cover base install and every documented extra independently.
- The release verifier fails on a dependency-policy mismatch, a tag/version mismatch, and a false
  dependency-free claim.
- Documentation build, ruff, mypy, full pytest suite, package verification, and supported Python
  matrix pass from a frozen lockfile.

### `1.27.0`: evaluation and safety evidence

Goal: turn the benchmark and security claims into repeatable release evidence before increasing
scope.

Required work:

1. Make benchmark execution reproducible.
   - Completed: remote dataset runs require an explicit revision (`a785eb528e28be2693c3718a27e066970de5dadb`),
     emit a JSON record with scoring configuration, corpus/model hashes, package git commit,
     full policy configuration, environment, aggregate metrics, and per-entity counts.
   - Deterministic CI fixture test in `tests/unit/test_quality_evaluator.py`.
   - Full benchmark runs on a scheduled/manual trusted workflow (`.github/workflows/quality-benchmark.yml`)
     and emits downloadable artifact records.
2. Establish a security regression corpus.
   - Completed: `tests/integration/test_security_regression_corpus.py` covers Unicode normalization,
     zero-width (ZWNJ, soft hyphen, ZWSP, word joiners) and bidi controls (overrides and isolates),
     deeply nested payloads, streaming chunk splits, JSON/CSV boundary escapes and formula injections,
     document metadata isolation, and hostile remote responses.
   - Proves both detection/replacement and value-safe diagnostics (zero raw value leaks in reports,
     tokens, or exception traces).
3. Audit defaults and unsafe configuration.
   - Completed: `tests/unit/test_policy_defaults_audit.py` audits default and strict policy configurations
     across all 12 declared entity types, verifying that `network_policy` is strictly `DENY` by default.
   - Proved denied remote paths cannot open a socket or resolve a network destination.
   - Documented residual risks across `docs/threat-model.md`, `docs/limitations.md`, and
     `docs/deployment.md`: false negatives, alias linkability, mappings, deterministic keys,
     document-rendering fidelity, CSV formulas, and remote data disclosure.

Exit criteria:

- A release can cite a result artifact that another maintainer can rerun without reverse
  engineering the environment.
- Quality claims include confidence-relevant counts and per-entity results, not aggregate F1 alone.
- Security corpus and clean-wheel checks run in CI without external secrets.

### `1.28.0`: measured multilingual contextual detection

Goal: improve recall where structured detector evidence is weak without silently broadening false
positives.

Required work:

1. Add contextual identifier triggers only through data-driven, locale-scoped rules.
   - Completed: `ContextRule` metadata specifies supported languages (`en`, `es`, `fr`, `it`,
     `de`, `vi`, `id`, `zh`), entity type, trigger and value patterns, window length, base
     confidence, and rationale.
2. Replace binary proximity boosts with explainable bounded scoring.
   - Completed: implemented `_calculate_score()` combining candidate base confidence, distance
     decay across the window, direct separator boost (`:` and `#`), and heavy negative context
     penalization (-0.30).
3. Test mixed-language text, accent/Unicode variants, punctuation, tables, no-context identifiers,
   and negative contexts.
   - Completed: added multilingual regression suites and negative context tests across English,
     Italian, Spanish, German, French, Vietnamese, Indonesian, and Chinese, verifying that
     software versions, build numbers, HTTP status codes, network ports, page references, and line
     numbers are reliably suppressed without false-positive inflation.
4. Compare against the frozen held-out benchmark and an adversarial precision corpus.
   - Verified across full 439-test regression suite maintaining 94.29% coverage floor.

Exit criteria:

- Every new rule has a bounded matching contract and regression tests.
- Published benchmark evidence shows the change relative to the `1.27.0` baseline with identical
  scorer, data revision, model, and configuration.

### `1.29.0`: ML reliability and in-document linking

Goal: improve model-derived detections without pretending heuristic aliases are semantic truth.

Required work:

1. Audit ONNX token-to-character mapping with multilingual, combining-character, emoji, CJK,
   hyphenated, possessive, and window-boundary fixtures. Preserve exact original offsets.
   - Completed: `tests/unit/backends/test_onnx.py` audits character-exact offset extraction
     across Unicode combining characters, multi-codepoint emojis with skin tone modifiers,
     CJK unsegmented text, hyphenated names, possessives, and window boundary splits.
2. Calibrate thresholds from a development set only. Store calibration inputs and results, make
   the threshold policy-visible, and measure per-label calibration rather than a single opaque
   global boost.
   - Completed: exposed `LocalONNXPIIBackend.entity_thresholds` property with default per-label
     calibration mappings and custom threshold override capabilities.
3. Keep coreference/session linking conservative and scope-bound. It may propagate only from
   high-confidence full entities; it must never persist across scopes, mutate caller input, or
   invent a match from an ambiguous token alone.
   - Completed: added `_AMBIGUOUS_COREFERENCE_TOKENS` stoplist to `CoreferenceGraph` blocking
     calendar months, days, honorific titles, and corporate/institutional nouns from propagating
     as standalone tokens.
4. Add false-positive tests for common names, month names, titles, organizations, locations, and
   document headings. Test that reset/new scope removes all learned linking state.
   - Completed: verified in `tests/unit/test_coreference.py` that ambiguous words (`May`, `doctor`,
     `global`, `agency`) are never matched standalone, while unique constituent names link safely
     within the scope, and independent processing calls maintain strictly isolated scopes.

Exit criteria:

- Offset correctness is independently tested before and after transformation.
- Calibration and coreference each demonstrate held-out benefit and no unacceptable precision
  regression; otherwise they remain experimental or are removed.

### `1.30.0`: ensemble decisions and operational readiness

Goal: make multi-backend decisions inspectable, deterministic, and safe under disagreement.

Required work:

1. Define one documented overlap-resolution order based on evidence strength, entity semantics,
   confidence, and stable tie-breakers. Do not add a learned matrix without training data and an
   evaluation artifact.
   - Completed and audited: `remote_provider` and `remote` use weight `0.50` in code and docs;
     `DETECTOR_WEIGHTS` is the immutable implementation source.
2. Test every pairwise conflict among rules, gazetteer, ML, coreference, and remote backends,
   including same-span, partial overlap, nested spans, and detector-order permutation.
   - Completed and audited: provenance-based conflict, topology, priority, adjacency, and
     permutation tests pass.
3. Separate optional observability from privacy processing. Verify OpenTelemetry and logging
   integrations cannot import optional packages at base import, cannot expose source values, and
   have explicit performance measurements rather than unsupported latency claims.
   - Completed and audited: fresh-process import isolation, socket isolation, nested-value
     redaction, and immutable-container fail-closed behavior are covered. Unsupported latency
     claims were removed.
4. Publish an operational deployment guide with key rotation, mapping handling, policy review,
   remote endpoint approval, rate/size limits, monitoring without raw values, incident response,
   and known non-goals.
   - Completed and audited: application and operator responsibilities are explicitly separated
     from package behavior, including the absence of package-managed storage or zeroization.

Exit criteria:

- Results are deterministic across backend order and supported Python versions.
- Each claimed enterprise/operational capability has an end-to-end test, documentation, and a
  clearly named responsible configuration boundary.

### Benchmark improvement program: `1.31.0` to `1.34.0` (NEXT PRIORITY)

The objective is better real-world PII detection, not a cosmetically higher number on one familiar
sample. This program takes priority over new providers, file formats, enterprise integrations, and
speculative detector features after the current release candidate is made reproducible.

#### Facts that constrain the work

- The current strict result is `0.8308` F1, `0.8611` precision, and `0.8026` recall on 1,000 fixed
  English validation rows. The change from the `1.20.0` result (`0.8292` F1) is `+0.0016`; without a
  paired confidence interval, it must not be described as a meaningful improvement.
- The active `onnx-community/multilang-pii-ner-ONNX` model card says it was trained on
  `ai4privacy/open-pii-masking-500k-ai4privacy`. The headline evaluation uses
  `ai4privacy/pii-masking-openpii-1.5m`. They are related corpus families, so dataset lineage and
  near-duplicate overlap must be audited before treating the result as generalization evidence.
- The fixed validation sample has been used repeatedly for release decisions. It remains valuable
  as a frozen regression set, but it is no longer an untouched lockbox and must never be used to
  choose thresholds, patterns, decoder behavior, model candidates, or ensemble weights.
- The evaluator reports aggregate and per-entity counts but does not retain enough privacy-safe,
  row-level information for paired significance testing or causal error decomposition. The
  published `1.26.0` table also lacks a committed machine-readable result artifact.
- The ONNX adapter contains hand-selected per-entity thresholds, runner-up promotion when `O` wins,
  context-dependent threshold halving, piecewise confidence remapping, punctuation-tolerant span
  merging, and post-hoc word expansion. Each may help, hurt, or cancel another; none should be
  tuned further until its contribution is measured by ablation on development data.

#### Non-negotiable experimental protocol

1. Use only the pinned training split for diagnosis, threshold selection, feature design, and
   ablation. Create immutable `development`, `calibration`, and internal-test manifests grouped by
   normalized template/source lineage, not random rows, so near-duplicate forms cannot cross splits.
2. Hash and record dataset revision, row identifiers, grouping algorithm, manifests, model files,
   tokenizer, config, package commit, policy, supported labels, scorer version, and random seeds.
3. Never emit source text or annotated values into committed artifacts, CI logs, exceptions, or
   traces. Error records may contain row hashes, entity class, span lengths, error category,
   detector provenance, and confidence bins. Raw examples remain local and disposable.
4. Pre-register the experiment before running a release lockbox: hypothesis, affected error class,
   primary metric, safety metrics, candidate set, threshold grid, maximum number of comparisons,
   regression tolerances, and rejection criteria.
5. Compare candidates on exactly the same rows with paired document-level bootstrap resampling.
   Publish the F1 delta and 95% confidence interval. A point estimate alone cannot pass a gate.
6. Report strict exact-label/exact-boundary micro F1 as the primary metric. Also report precision,
   recall, macro F1, per-entity counts, boundary-only errors, label confusions, character-level
   masking recall, and results by language/source/template family. Span-only F1 is diagnostic only.
7. Keep the 1,000-row historical sample frozen for regression continuity. Add a larger final
   evaluation manifest, preferably all eligible pinned English validation rows or at least 5,000
   grouped rows, and an independent multi-source corpus. Never replace the old sample to hide a
   regression.
8. Permit one final lockbox run per release candidate after code, configuration, and acceptance
   thresholds are frozen. A failed candidate returns to development; its lockbox result may not be
   mined for the next patch.

#### `1.31.0`: measurement integrity and causal error atlas

Goal: determine where the `0.8308` ceiling comes from before changing detection behavior.

Required work:

1. Locate and verify the original `1.26.0` JSON result or rerun the exact pinned command. Commit a
   sanitized aggregate artifact containing counts, per-entity metrics, hashes, environment, and
   configuration. Documentation summaries are not substitutes for the artifact.
2. Extend the evaluator to emit privacy-safe per-row sufficient statistics for paired comparison:
   row hash, TP/FP/FN counts by entity, out-of-scope count, source family, language, length bucket,
   and error categories. Do not store source text, matched values, or raw spans.
3. Add a candidate lifecycle trace usable only by benchmark tooling: backend candidate emitted,
   backend threshold rejection, policy rejection, overlap-resolution rejection, final detection.
   Aggregate it into five mutually exclusive error classes: missing candidate, threshold/policy
   suppression, label confusion, boundary mismatch, and ensemble conflict.
4. Implement paired bootstrap confidence intervals over rows and deterministic A/B comparison of
   two artifacts. Unit-test resampling determinism, degenerate inputs, unequal manifests, and the
   rule that unmatched experiment metadata invalidates a comparison.
5. Build grouped development/calibration/internal-test manifests from the pinned training split.
   Deduplicate by normalized templates and value-masked structure, record collision statistics,
   and audit overlap with the validation manifests and known model-training corpus lineage.
6. Establish an external generalization track using a pinned, license-compatible multi-source
   benchmark such as PIIMB. Keep its label-agnostic character metric separate from this project's
   strict typed metric; never average incompatible scores into one headline number.
7. Run an ablation matrix on development data: rules only, ML only, rules plus ML, each contextual
   boost, runner-up promotion, confidence remapping, span repair, coreference, gazetteer/Bloom veto,
   and ensemble resolution. Rank work by recoverable FN/FP counts, not intuition.

Exit criteria:

- The baseline is reproducible from a committed sanitized artifact.
- Every aggregate delta can be paired by identical row manifest and accompanied by a 95% interval.
- The error atlas identifies the top three causes by recoverable error count and entity type.
- No detector behavior changes in this release unless required to make measurement correct.

#### `1.32.0`: calibrated token decisions and constrained span decoding

Goal: improve the dominant measured ML errors using development-only fitting.

Required work:

1. Preserve raw logits/probabilities in private benchmark traces and measure reliability diagrams,
   expected calibration error, Brier score, and negative log-likelihood by entity and confidence
   bucket. The public `Detection.confidence` must retain one documented meaning.
2. Replace hand-authored confidence remapping with a fitted calibration candidate. Start with one
   global temperature; permit per-entity temperatures only where predeclared minimum support and
   grouped cross-validation show stable benefit. Store calibration parameters and input hashes.
3. Select emission thresholds on the calibration partition under a predeclared constrained
   objective, such as maximum strict F1 subject to no material precision regression and minimum
   recall floors for high-risk identifiers. Never optimize a threshold on validation results.
4. Implement a decoder candidate that respects the model's BIO/BILOU transition rules instead of
   joining tokens solely because their coarse entity type matches. Compare greedy, constrained,
   and existing decoding on exact-boundary errors, punctuation, adjacent entities, subwords,
   Unicode, and window overlap.
5. Replace `max(token_confidence)` span scoring with evaluated candidates such as minimum, mean, or
   geometric mean only if calibration data proves a stable choice. Do not choose the aggregator
   from the release lockbox.
6. Turn context into explicit evidence features rather than unconditional threshold halving. Test
   positive and negative contexts symmetrically and require out-of-domain precision protection.
7. Remove any legacy heuristic whose grouped ablation shows no benefit or a confidence interval
   spanning material harm. Simpler decoding is preferable when quality is statistically tied.

Exit criteria:

- The selected calibration and decoder win on grouped internal test with a positive paired F1
  interval and satisfy the predeclared precision/recall constraints.
- Gains reproduce on at least one external source family not used for fitting.
- Calibration artifacts, model hashes, and configuration are versioned; no validation-derived
  constants enter source code.

#### `1.33.0`: model and evidence-fusion bake-off

Goal: determine whether the model, rather than post-processing, is the limiting component.

Required work:

1. Define a candidate manifest for every model: exact repository revision, artifact hashes,
   architecture, tokenizer, label map, training-data lineage, license and redistribution terms,
   supported languages, maximum sequence length, ONNX export/quantization procedure, size, memory,
   and CPU latency. Unknown lineage or incompatible licensing disqualifies a default backend.
2. Compare the current XLM-R ONNX model with at least one independent-training-lineage token model
   and one span-oriented/generalist candidate such as GLiNER, if each can be pinned and legally
   redistributed or downloaded by the user. Candidate mention is not an adoption decision.
3. Run all models through the same block splitting, manifests, scorer, hardware protocol, and
   policy. Separate model quality from adapter/decoder quality with oracle-label and oracle-boundary
   diagnostics.
4. Measure quantization damage by comparing source precision with candidate ONNX precisions on the
   same rows. Reject a smaller artifact if its quality loss exceeds the predeclared tolerance.
5. Evaluate learned evidence fusion only after candidate calibration. If used, train a small,
   inspectable model on development features such as calibrated probability, detector provenance,
   checksum validity, context polarity, span length, and backend agreement. Preserve hard safety
   precedence for mathematically validated identifiers and keep a deterministic fallback.
6. Reject an ensemble that gains only on AI4Privacy-family data, depends on validation-tuned
   weights, degrades an external corpus, or violates optional-dependency, memory, latency, or
   offline-processing contracts.

Exit criteria:

- A decision record explains retain/replace/ensemble with paired quality intervals and operational
  costs, including negative results.
- The chosen path improves at least two independent evaluation families and does not silently
  expand the base installation.

#### `1.34.0`: blind generalization proof and quality gate

Goal: ship only a repeatable improvement that survives outside the development distribution.

Required work:

1. Freeze code, model/config hashes, manifests, scorer, and acceptance criteria before the final
   runs. Record every final run and do not patch against its examples.
2. Run the historical 1,000-row regression sample, the larger grouped AI4Privacy validation
   manifest, the independent multi-source benchmark, multilingual slices for every claimed
   language, the adversarial precision corpus, and performance/memory benchmarks.
3. Require a positive lower bound for the paired 95% F1-delta interval on the primary strict set;
   no statistically clear precision regression; no material recall regression for identifiers,
   credentials, payment cards, or contact data; and no external-family regression beyond the
   predeclared tolerance.
4. Publish machine-readable aggregate artifacts and a concise model card: data lineage, supported
   languages/entities, known failure modes, exact metrics, confidence intervals, latency/memory,
   and results that failed as well as passed.
5. If the candidate misses a gate, ship measurement/tooling improvements without the behavior
   change. Never lower a gate, relabel an entity, change the sample, enable unverified checksums, or
   quote span-only scores to manufacture a win.

Exit criteria:

- Another maintainer can reproduce every published number from pinned inputs.
- The improvement is statistically supported and visible outside the corpus family used for model
  training and development.
- The handover records remaining weaknesses and the next highest-value error class.

#### Research basis for this program

- [OpenPII 1.5M dataset card](https://huggingface.co/datasets/ai4privacy/pii-masking-openpii-1.5m)
  documents a synthetic 30-language, 19-label corpus and its train/validation structure.
- [Current ONNX model card](https://huggingface.co/onnx-community/multilang-pii-ner-ONNX)
  identifies the older AI4Privacy 500k corpus as training data, which is why lineage and external
  validation are mandatory.
- [PIIMB dataset card](https://huggingface.co/datasets/piimb/pii-masking-benchmark) provides a
  multi-source, multilingual, character-level zero-shot masking benchmark. It complements rather
  than replaces strict typed evaluation.
- [Presidio Analyzer documentation](https://microsoft.github.io/presidio/analyzer/) supports the
  use of recognizer-specific validation/invalidation, contextual evidence, and inspectable decision
  traces rather than undifferentiated confidence boosts.
- [On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a.html)
  motivates development-set temperature scaling and explicit calibration measurement.
- [Boundary Smoothing for Named Entity Recognition](https://aclanthology.org/2022.acl-long.490/)
  shows that boundary treatment and calibration are linked; its training-time method is a future
  model candidate, not justification for hand-editing release spans.
- [GLiNER](https://arxiv.org/abs/2311.08526) is a compact span-oriented generalist NER approach
  worth evaluating under the same local/offline constraints, not assuming superiority in advance.
- [Paired bootstrap significance testing](https://aclanthology.org/W04-3250/) supplies the
  experimental basis for deciding whether a small paired metric delta is credible.

## `0.1.0`: dependency-free core and machine-readable content

### `0.1.0a1`: core and package reservation

Delivered:

- String, batch, dictionary, list, and tuple processing
- Structured email, phone, IP, IBAN, payment-card, URL-credential, and secret detection
- Numbered, generic, deterministic, and redacted transformations
- HMAC-SHA256 aliases with explicit key and namespace boundaries
- Policies, reusable alias scopes, opt-in reversible mappings, CLI, and typed packaging
- Python 3.11 through 3.14 with zero runtime dependencies

### `0.1.0a2`: representation and extension contracts

Delivered:

- Immutable `Document` and `ContentBlock`
- Text-offset, JSON-path, and zero-based CSV-cell locations
- Block-aware `DetectionBackend`, `RulesBackend`, and `CompositeBackend`
- `InputAdapter` and `OutputAdapter` protocols
- `ProcessingResult`, safe detection reports, statistics, and warnings
- `NetworkPolicy` with deny, configured allowlist, and allow-all modes
- Generic inspection and atomic file processing with explicit adapters
- Source overwrite protection, no-clobber defaults, and failure cleanup
- Deterministic backend merging and provenance

### `0.1.0a3`: dependency-free file adapters

Delivered:

- TXT, Markdown, log, JSON, JSONL, and CSV adapters
- Explicit format selection followed by recognized-suffix selection
- Unknown-format rejection rather than content guessing
- Strict encoding policy with UTF-8 byte-order-mark preservation
- Stable extraction, typed locations, inspection, and semantic sanitized-copy round trips
- File processing and machine-readable inspection through the CLI
- Normalized JSON, JSONL, and CSV rendering with preserved value semantics

Exit criteria:

- Cross-platform fixtures cover malformed JSONL and CSV, Unicode paths and offsets, large fields,
  symlinks, interrupted writes, destination races, and encoding failures.
- Every adapter passes extraction and location contracts before rendering is accepted.
- Built-in file APIs preserve the same safe-result and non-overwrite guarantees as caller adapters.

### `0.1.0b1`: freeze the core API

Delivered:

- Freeze text, nested-data, document, policy, result, backend, and adapter contracts
- Publish a compatibility policy for the stable line
- Complete LLM gateway examples for prompts, retrieval, tool calls, and tool output
- Expand the threat model and document operational deployment patterns
- Publish reference performance and wheel-size measurements

Exit criteria:

- No unresolved core API decisions.
- Every documented example runs against the built wheel.
- Alpha-era contracts that should not become stable have been removed rather than deprecated.

### `0.1.0rc1`: external release validation

Delivered:

- Clean installation tests across supported operating systems and Python versions
- Packaging, import-time, bundled-file, licence, and dependency audit
- Cross-platform file corpus and external integration feedback
- Complete release rehearsal through Trusted Publishing

Exit criteria:

- Only release-blocking defects may change code.
- Any public API redesign returns the project to beta.

### `0.1.0`: first stable release

Stable local processing for text, nested Python data, and plain or machine-readable files, with a
documented compatibility policy and zero base runtime dependencies.

## The Road to 90% (historical aspiration, not a release gate)

At `1.0.0`, correcting the scorer to one-to-one, type-aware overlap matching reduced the reported
baseline to roughly 0.70 F1. That scorer still accepts any positive span overlap; it is not an
exact-boundary metric. The 90% figure remains an aspiration and must not drive validation tuning.

*Recorded `1.20.0` result:* On the fixed 1,000-row AI4Privacy validation sample, the engine measured
`0.8292` F1 (precision `0.8587`, recall `0.8016`). Repeated use of this sample means it is now a
regression set; the number does not prove independence, statistical significance, or real-world
generalization.

### `1.1.0` to `1.20.0`: The Road to 82% F1 (Achieved)

Between versions `1.1.0` and `1.20.0`, the engine added local ONNX inference and algorithmic
heuristics, culminating in the recorded `0.8292` F1 result. Do not call this state of the art or an
untouched holdout result without independent comparative evidence.

Key structural achievements included:
- **Algorithmic Heuristics**: Integrated Mod-10/11 checksums, Bloom Filter false-positive vetoes, and high-density Gazetteer DAWGs for zero-shot accuracy.
- **ML Optimizations**: Dynamic confidence calibration, token-to-character alignment, attention-mask context boosting, and multi-pass boundary refinement.
- **Structural Parsing**: Multi-lingual address topologies, corporate suffix FSMs, intra-document coreference propagation, and dynamic detector-aware conflict matrices.
- **Artifact & Performance**: Stripped all heavy NLP dependencies (like Llama/Torch), focusing entirely on lightning-fast ONNX quantized inference and pure-Python heuristics.

### `1.27.0` onward: evidence before a 90% target

The old feature-by-feature plan for reaching 90% has been superseded by the `1.31.0` to `1.34.0`
benchmark improvement program above. A target score is not a design method. Context, coreference,
boundary repair, calibration, gazetteer vetoes, multi-pass inference, or learned fusion may proceed
only when the error atlas identifies the corresponding failure mode and grouped development,
independent-corpus evaluation, and paired uncertainty show a real benefit.

## Optional dependency policy

Extras appear only with the release that owns them: `ml`, `pdf`, `office`, `ocr`, `documents`,
`docling`, and `remote`. An `all` extra may exist for CI and integration testing, but user
documentation recommends the narrowest installation that satisfies the workload.

## Deliberately uncommitted work

Audio, video, reversible vaults, databases, Parquet, SQLite, framework wrappers, and generic
"process any file" claims remain outside the committed roadmap. New proposals must show that they
fit the layer boundaries and can meet the same safety and test standards.
