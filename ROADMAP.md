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
| `1.26.0` | Next      | Enterprise DLP Broker & Active Policy Sync |
| `1.27.0` | Next      | Multi-Lingual Contextual Proximity & Cross-Entropy Boosting |
| `1.28.0` | Next      | Semantic Coreference Propagation & Entity-Component Linker |
| `1.29.0` | Next      | Contrastive Subword Alignment & Bayesian ML Calibration |
| `1.30.0` | Next      | Graph-Based Entity Disambiguation & Gazetteer-Veto Tries |
| `1.31.0` | Next      | Multi-Pass Ensemble Fusion & Adaptive Conflict-Resolution Matrices |

Alpha releases optimize for the cleanest safe architecture, not backward compatibility. They may
remove, rename, or replace public APIs without aliases or shims. Material changes are documented,
but compatibility guarantees start only with `0.1.0`.

## Release gate for every milestone

- Ruff formatting and linting pass.
- Strict mypy passes for source, tests, benchmarks, and scripts.
- Supported Python versions pass on Linux, macOS, and Windows.
- Branch coverage meets the release floor and never falls below the previous tagged baseline.
  The current enforced floor is 95.36%, set by `--cov-fail-under` in `pyproject.toml`.
- Property, contract, clean-wheel, documentation, and packaging checks pass.
- The base wheel remains typed and declares zero runtime dependencies.
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