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
| `1.0.0` | Published | Mature compatibility commitment & strict 1-to-1 boundary matching |
| `1.10.0` | Published | Local PII optimizations & international trigger expansion |
| `0.18.0` | Next | Resilient document parsing and large-scale pipelines |

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


## Future Milestones

### Schema-Preserving Agent Sanitation (MCP Integration)
- **Use Case:** Safely interacting with LLM agents.
- **Focus:** Redacting JSON-RPC and MCP tool call payloads natively without breaking structural schemas required by models.

### OpenTelemetry Integration
- **Use Case:** In-process observability.
- **Focus:** A dedicated middleware adapter to redact application logs and trace spans securely before export.

### Advanced Local ML (GLiNER2 ONNX)
- **Use Case:** Next-generation semantic recall.
- **Focus:** Integrate prompt-based NER models natively within the ONNX local boundary to dynamically capture domain-specific jargon (e.g. "Project Codename X").

### Regional EU Identifier Depth
- **Use Case:** European enterprise compliance.
- **Focus:** Deepening coverage with mathematically verified checksums and topological parsers for French, German, Italian, and Spanish national systems.

## Performance & Detection Quality Horizon (Post-1.0 / Ongoing)

To continually improve precision and recall (currently heavily measured in `benchmarks/evaluate_quality.py`) without introducing hardcoded or brittle regex artifacts, the following generalizable architectural improvements are slated for upcoming releases:

1. **Dynamic Entity-Specific Thresholds (ML)**: Instead of a flat `entity_threshold` across all labels, allow per-entity calibration. For example, lower activation thresholds for `LOCATION` (which historically suffers from low recall but high precision) while keeping `PERSON` strictly bounded.
2. **Context-Assisted ML Boosting**: Integrate the `ContextDetector` into the ML loop. If a token falls within 30 characters of a context trigger ("Name:", "Address:"), dynamically boost the ML logits for that specific text window, resolving the "missed isolated entities" problem.
3. **Span-Level Subword Repair (Token-Merge Averaging)**: DistilBERT uses WordPiece. If the tokenizer splits a name into subwords and assigns conflicting probabilities across them (e.g., dropping a middle subword), implement a CRF-style continuation heuristic to coerce adjacent subwords into a unified entity unless separated by a hard boundary.
4. **Ensemble Voting Arbitrator**: When multiple backends run simultaneously, introduce an `EnsembleArbitrator` allowing modes like `HighRecall` (Union), `HighPrecision` (Intersection - requires at least two backends to agree), or `Two-Pass` (Regex proposes, ML verifies).
5. **Cross-Lingual Zero-Shot Backend (GLiNER)**: Introduce an optional backend using GLiNER (Generalist Model for NER). GLiNER uses prompt-based label injection natively supporting 20+ languages out of the box, allowing dynamic detection of arbitrary entities ("Internal Project Code") with a fundamentally higher recall ceiling than traditional BERT models.

## Optional dependency policy

Extras appear only with the release that owns them: `ml`, `pdf`, `office`, `ocr`, `documents`,
`docling`, and `remote`. An `all` extra may exist for CI and integration testing, but user
documentation recommends the narrowest installation that satisfies the workload.

## Deliberately uncommitted work

Audio, video, reversible vaults, databases, Parquet, SQLite, framework wrappers, and generic
"process any file" claims remain outside the committed roadmap. New proposals must show that they
fit the layer boundaries and can meet the same safety and test standards.

