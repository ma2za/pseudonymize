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
| `1.0.0`  | Published | Mature compatibility commitment & strict 1-to-1 boundary matching |
| `1.20.0` | Published | Stable evaluation baseline achievement (0.8292 F1) |
| `1.21.0` | Published | Scale & Integration (Batched Vectorization & LRU Caching Fast-Paths) |
| `1.22.0` | Published | Next-Generation Semantic Recall & Schema-Preserving Agent Sanitation (MCP) |
| `1.23.0` | Published | Ecosystem Integration & Regional EU Identifier Depth (German Steuer-IdNr, Spanish NIF/NIE/CIF) |
| `1.24.0` | Published | Asynchronous Observability & Distributed DLP Adapter (Zero-Overhead OpenTelemetry & Logging) |
| `1.25.0` | Published | Distributed Scaling, Property Test Resilience & Pre-Commit Verification |
| `1.26.0` | In development | Contract reconciliation and release-proof baseline |
| `1.27.0` | Planned | Reproducible evaluation, production-safety hardening, and detector evidence |
| `1.28.0` | Planned | Measured multilingual contextual recall improvements |
| `1.29.0` | Planned | ML calibration, entity linking, and robust boundary alignment |
| `1.30.0` | Planned | Ensemble conflict resolution only if it improves held-out metrics |

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

### Baseline facts to preserve

- The package is a pseudonymization boundary, not anonymization, compliance certification, or an
  enterprise DLP system.
- The published strict quality baseline is 0.8292 F1 (precision 0.8587, recall 0.8016) on 1,000
  sampled validation rows of `ai4privacy/pii-masking-openpii-1.5m`, with one-to-one matching,
  exact entity types, and strict boundaries. It is a point-in-time measurement, not a guarantee.
- The base distribution declares no runtime dependencies. Optional remote support declares
  `httpx`; the base package remains dependency-free, while the project still ships an optional
  HTTP provider.
- `HTTPRemoteBackend` sends raw block text to its configured endpoint only after the engine's
  explicit network-policy checks. Its presence means remote processing is a shipped capability,
  even if no hosted service is operated by this project.
- `SYNTHETIC_BENCHMARK=1` bypasses checksum validation. It is test/benchmark scaffolding and must
  not be usable accidentally by an application process.

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
   - Preferred: restore a standard-library-only core by moving DAWG/gazetteer and all HTTP code
     behind narrow extras, and ensure base imports cannot require those packages. This is complete
     for the current base wheel; retain the release checks and clean-wheel coverage.
   - Alternative: retain the dependencies and remove every zero-dependency/dependency-free claim
     from README, vision, roadmap, release verifier output, package metadata descriptions, and
     release materials.
   - In either case, add a test that builds the wheel and asserts the exact non-extra
     `Requires-Dist` set expected for that policy.
2. Resolve the remote-backend contract.
   - Either keep `HTTPRemoteBackend`, document it in README, API docs, threat model, dependency
     policy, and limitations, and test its payload, timeout, retry, authentication, and error
     sanitization behavior; or remove it and its `remote` extra/tests/docs completely.
   - If retained, document that configured endpoints receive raw content blocks, identify the
     outbound fields, require TLS validation by default, bound payload size, and make endpoint,
     timeout, retry, and redirect behavior explicit.
   - Ensure transport errors never include request text, authorization values, or server response
     bodies. Add regression tests for each leak vector.
3. Remove contradictory release checks.
   - Make `scripts/verify_release.py` and `scripts/audit_install.py` enforce the selected base
     dependency policy rather than contain no-op or misleading checks.
   - Correct their user-facing output so it cannot claim dependency-free after accepting base
     dependencies.
   - State the actual coverage floor only once, sourced from `pyproject.toml`; either raise it
     deliberately with a passing suite or leave it at 94.10%.
4. Fix release metadata discipline.
   - A version becomes “Published” only after its matching `v<version>` tag, successful release
     workflow, PyPI artifact, and GitHub release exist.
   - Keep unreleased work under an `[Unreleased]` changelog section. Do not date a release entry
     before publication or label a planned feature as shipped.
   - Update comparison links to current tags and add a release-script assertion that the current
     version is not accidentally described as published without a matching tag.
5. Constrain benchmark-only bypasses.
   - Replace ambient `SYNTHETIC_BENCHMARK` behavior with an explicit benchmark-only dependency
     injection or an opt-in object unavailable from normal public processing APIs.
   - If environment configuration remains, reject it outside a dedicated benchmark command and
     add subprocess tests proving production execution cannot enable it.

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
   - Pin the dataset revision, split, language filtering, random seed, sample-selection algorithm,
     supported labels, scoring mode, policy configuration, model artifact URLs, and SHA-256 values.
   - Emit a machine-readable result containing revision, command arguments, package commit,
     Python/OS/CPU information, model hashes, annotation/detection/true-positive/false-positive/
     false-negative counts, and per-entity precision/recall/F1.
   - Keep the validation set measurement-only. Use a separate train/development workflow for
     experimentation and never tune on the fixed held-out sample.
   - Add a CI job that at least validates evaluator determinism on a committed small synthetic
     fixture. Run the full external benchmark on a scheduled/manual trusted workflow and attach
     result artifacts to releases.
2. Establish a security regression corpus.
   - Cover Unicode normalization, zero-width and bidi controls, escaped/encoded structured values,
     chunk boundaries, nested payloads, CSV/JSON/XML/HTML boundaries, document metadata, and
     hostile remote responses.
   - For each past leak or bypass, retain the smallest regression fixture and a test that proves
     both detection/replacement and safe diagnostics.
3. Audit defaults and unsafe configuration.
   - Verify default policy behavior for every entity type and extension.
   - Ensure remote processing requires both explicit policy permission and per-backend consent;
     prove denied paths cannot open a client or resolve a network destination.
   - Document residual risks: false negatives, alias linkability, mappings, deterministic keys,
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

1. Add contextual identifier triggers only through data-driven, locale-scoped rules. Each rule must
   specify supported languages, positive examples, negative examples, window length, and why it
   cannot match ordinary prose or version/page/reference values.
2. Replace binary proximity boosts with explainable bounded scoring: candidate confidence, nearby
   positive evidence, negative evidence, distance, and final threshold. Keep explanations
   value-free in reports.
3. Test mixed-language text, accent/Unicode variants, punctuation, tables, no-context identifiers,
   and negative contexts such as software versions, revision IDs, HTTP values, and page numbers.
4. Compare against the frozen held-out benchmark and an adversarial precision corpus. Revert any
   rule that improves aggregate recall but regresses an entity family or materially degrades
   precision without a documented policy decision.

Exit criteria:

- Every new rule has a bounded matching contract and regression tests.
- Published benchmark evidence shows the change relative to the `1.27.0` baseline with identical
  scorer, data revision, model, and configuration.

### `1.29.0`: ML reliability and in-document linking

Goal: improve model-derived detections without pretending heuristic aliases are semantic truth.

Required work:

1. Audit ONNX token-to-character mapping with multilingual, combining-character, emoji, CJK,
   hyphenated, possessive, and window-boundary fixtures. Preserve exact original offsets.
2. Calibrate thresholds from a development set only. Store calibration inputs and results, make
   the threshold policy-visible, and measure per-label calibration rather than a single opaque
   global boost.
3. Keep coreference/session linking conservative and scope-bound. It may propagate only from
   high-confidence full entities; it must never persist across scopes, mutate caller input, or
   invent a match from an ambiguous token alone.
4. Add false-positive tests for common names, month names, titles, organizations, locations, and
   document headings. Test that reset/new scope removes all learned linking state.

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
2. Test every pairwise conflict among rules, gazetteer, ML, coreference, and remote backends,
   including same-span, partial overlap, nested spans, and detector-order permutation.
3. Separate optional observability from privacy processing. Verify OpenTelemetry and logging
   integrations cannot import optional packages at base import, cannot expose source values, and
   have explicit performance measurements rather than unsupported latency claims.
4. Publish an operational deployment guide with key rotation, mapping handling, policy review,
   remote endpoint approval, rate/size limits, monitoring without raw values, incident response,
   and known non-goals.

Exit criteria:

- Results are deterministic across backend order and supported Python versions.
- Each claimed enterprise/operational capability has an end-to-end test, documentation, and a
  clearly named responsible configuration boundary.

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

## The Road to 90% (Strict Evaluation Baseline)

Following the `1.0.0` realization that strict 1-to-1 boundary and label matching drops our baseline to ~0.70 F1, the next releases are singularly focused on legitimately bridging this gap.

*Result (v1.20.0 Completion):* On a random, non-overfitted sample of 1000 validation records from `ai4privacy`, the engine achieved a strict **F1 Score of 0.8292** (Precision: **0.8587**, Recall: **0.8016**), proving a massive and secure baseline improvement without dataset cheating or overfitting.

### `1.1.0` to `1.20.0`: The Road to 82% F1 (Achieved)

Between versions 1.1.0 and 1.20.0, the engine underwent a massive architectural overhaul to achieve state-of-the-art local PII detection, culminating in a verified **0.8292 F1 Score** (Precision: 0.8587, Recall: 0.8016) against the strict `ai4privacy` holdout validation dataset.

Key structural achievements included:
- **Algorithmic Heuristics**: Integrated Mod-10/11 checksums, Bloom Filter false-positive vetoes, and high-density Gazetteer DAWGs for zero-shot accuracy.
- **ML Optimizations**: Dynamic confidence calibration, token-to-character alignment, attention-mask context boosting, and multi-pass boundary refinement.
- **Structural Parsing**: Multi-lingual address topologies, corporate suffix FSMs, intra-document coreference propagation, and dynamic detector-aware conflict matrices.
- **Artifact & Performance**: Stripped all heavy NLP dependencies (like Llama/Torch), focusing entirely on lightning-fast ONNX quantized inference and pure-Python heuristics.

### `1.27.0` to `1.31.0`: Legitimate Quality & Benchmark Optimization (Planned)

To legitimately bridge the gap to a 90% F1 score without overfitting or cheating on the `ai4privacy` dataset, the following staged releases focus on robust ML engineering, structural heuristics, and contextual calibration:

#### `1.27.0`: Multi-Lingual Contextual Proximity & Cross-Entropy Boosting
- **Soft-Matching Windowed Context Vectorizer**: Replace rigid regex-based context triggers with a soft-matching multi-lingual keyword similarity matrix (covering German, Spanish, French, Italian, and English TIN/SSN/VAT variants).
- **Context-Proximity Decay**: Implement an exponential distance decay scorer, boosting candidate confidence if a verified context keyword is nearby (decaying smoothly up to an 80-character window).
- **Negative-Evidence Vetoes**: Add rules that instantly veto candidates if surrounding negative context is found (e.g., preceded by "vversion", "revision", "page", or "HTTP").

#### `1.28.0`: Semantic Coreference Propagation & Entity-Component Linker
- **Component-Level Dynamic Gazetteers**: Register individual parts of high-confidence full names (e.g., "Jonathan" from "Jonathan Miller") into an in-memory session DAWG to propagate and detect subsequent partial mentions.
- **Fuzzy Sequence Alignment**: Match and link typographical variations, nicknames, or misspelled occurrences of the same name within a single document session to ensure consistent mapping and avoid boundary errors.

#### `1.29.0`: Contrastive Subword Alignment & Bayesian ML Calibration
- **Contrastive Subword Aligner (CSA)**: Analyze character-level morphology around boundaries to snap raw model token index offsets to the nearest valid Unicode word boundaries or strip trailing word-pieces (e.g., `##son`).
- **Bayesian Calibration Layer**: Calibrate raw confidence scores using token-level attributes (token length, capitalization ratio, vocabulary frequency, and position) to replace static thresholds with adaptive decision boundaries.

#### `1.30.0`: Graph-Based Entity Disambiguation & Gazetteer-Veto Tries
- **Bipartite Entity Disambiguation Graph**: Disambiguate entities (e.g., "Washington" as `PERSON` if near "George" or `LOCATION` if near "street") by building dynamic co-occurrence relationships.
- **Compact Prose Veto DAWG**: Map standard dictionary words using an optimized trie to veto low-confidence NER predictions that fall onto common prose words (like "Hope" or "May") unless strong local context is present.

#### `1.31.0`: Multi-Pass Ensemble Fusion & Adaptive Conflict-Resolution Matrices
- **Adaptive Conflict-Resolution Matrix**: Replace simple priority ranking with type-specific conditional probabilities where rules (like checksummed `IBAN`) can veto ML, but high-confidence ML `PERSON` overrides generic rules.
- **Two-Pass Attention Consolidator**: Extract high-confidence structural anchors in Pass 1, then inject them as localized attention/mask hints back to the ONNX model in Pass 2 to guide prediction of complex surrounding entities.

## Optional dependency policy

Extras appear only with the release that owns them: `ml`, `pdf`, `office`, `ocr`, `documents`,
`docling`, and `remote`. An `all` extra may exist for CI and integration testing, but user
documentation recommends the narrowest installation that satisfies the workload.

## Deliberately uncommitted work

Audio, video, reversible vaults, databases, Parquet, SQLite, framework wrappers, and generic
"process any file" claims remain outside the committed roadmap. New proposals must show that they
fit the layer boundaries and can meet the same safety and test standards.
