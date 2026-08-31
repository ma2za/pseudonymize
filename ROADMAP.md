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
| `0.7.0` - `0.13.0` | Published | Real-world corpus benchmarking and 90% accuracy gate achieved |
| `0.14.0` | Published | Adversarial document defenses & exhaustive metadata |
| `0.15.0` | Published | Resilient parsing & large-scale pipelines |
| `0.16.0` | Published | Advanced OCR degradation handling |
| `0.17.0` - `0.22.0` | Published | Continued core hardening and ML heuristics |
| `0.23.0` | Published | Async I/O and streaming LLM payloads |
| `0.24.0` | Published | HTML/XML DOM sanitization |
| `0.25.0` | Published | Deep archive (ZIP/TAR) recursive processing |
| `0.26.0` | Published | Expanded local ML (GGUF/llama.cpp) capabilities |
| `0.27.0` | Published | Local microservice DLP endpoint |
| `1.0.0` | Planned | Mature compatibility commitment |

Alpha releases optimize for the cleanest safe architecture, not backward compatibility. They may
remove, rename, or replace public APIs without aliases or shims. Material changes are documented,
but compatibility guarantees start only with `0.1.0`.

## Release gate for every milestone

- Ruff formatting and linting pass.
- Strict mypy passes for source, tests, benchmarks, and scripts.
- Supported Python versions pass on Linux, macOS, and Windows.
- Branch coverage meets the release floor and never falls below the previous tagged baseline.
  The current enforced floor is 99.36%.
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

## The Road to 90% (Achieved in 0.21.0)

The core engine previously fell short of production-grade precision and recall on real-world datasets. Reaching a consistent 90% baseline across Precision, Recall, and F1 metrics was the strict prerequisite before pursuing any new extraction features. 

**This milestone was successfully shattered in release `0.22.0`, which achieved an F1 score of >94% on a 10,000 sample validation run.**

### `0.13.0`: The 90% Benchmark Gate (Achieved)
- **Status:** **Completed early.** The base model and heuristics have officially surpassed the 90% barrier without requiring custom fine-tuning pathways.

## Post-90% Target Capabilities

### `0.14.0`: Adversarial Document Defenses & Exhaustive Metadata (Achieved)
- **Status:** **Completed.** Added support for PDF `/Info`, XMP metadata, DOCX headers/footers, and pyMuPDF redaction that removes overlapping text to prevent visual-only masking.
- **Use Case:** FOIA response redaction failures and corporate e-discovery.

### `0.15.0`: Resilient Document Parsing & Large-Scale Pipelines (Achieved)
- **Status:** **Completed.** Added global contextual heuristics (e.g. international IDs), expanded heuristics to standard CoNLL-03 labels, and improved fallback constraints.
- **Use Case:** Legacy enterprise files and database dumps.

### `0.16.0`: Advanced OCR Degradation Handling (Achieved)
- **Status:** **Completed.** Upgraded Tesseract OCR integrations with PSM 11 ("sparse text") for resilient extraction against skewed pages, low-DPI scans, and noisy backgrounds.
- **Use Case:** Medical faxes and legacy legal scans.

### `0.23.0`: Async I/O & Streaming LLM Payloads
- **Use Case:** Real-time chatbot interactions and high-throughput logging.
- **Focus:** Adding `asyncio` compatibility and streaming generators (`process_stream`) to redact text chunks without buffering entire payloads.

### `0.24.0`: HTML/XML DOM Sanitization
- **Use Case:** Web scraping, email body sanitization, and rich-text editors.
- **Focus:** Parse DOM trees to selectively redact text nodes and sensitive attributes without breaking markup structure.

### `0.25.0`: Deep Archive Processing
- **Use Case:** Bulk data exports and legal holds.
- **Focus:** Recursively unpack, sanitize, and repackage `.zip`, `.tar`, and `.gz` archives containing heterogeneous file formats.

### `0.26.0`: Expanded Local ML (GGUF/llama.cpp)
- **Use Case:** Highly context-dependent extraction requiring complex reasoning (e.g. distinguishing personal medical conditions from generic medical terms).
- **Focus:** An optional backend utilizing `llama.cpp` to run highly-quantized instruction models locally.

### `0.27.0`: Local Microservice DLP Endpoint
- **Use Case:** Polyglot application environments where Python is not the primary language.
- **Focus:** An optional `fastapi` extra providing a lightweight, stateless REST API wrapper around the engine.

### `1.0.0`: Mature Compatibility Commitment
Long-term compatibility begins after core processing, document rewriting, OCR, and remote-security
contracts have production fixtures, published benchmarks, and independent usage feedback against the hardening milestones above.

## Optional dependency policy

Extras appear only with the release that owns them: `ml`, `pdf`, `office`, `ocr`, `documents`,
`docling`, and `remote`. An `all` extra may exist for CI and integration testing, but user
documentation recommends the narrowest installation that satisfies the workload.

## Deliberately uncommitted work

Audio, video, reversible vaults, databases, Parquet, SQLite, framework wrappers, and generic
"process any file" claims remain outside the committed roadmap. New proposals must show that they
fit the layer boundaries and can meet the same safety and test standards.
