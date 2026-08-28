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
| `0.7.0` | Next | Real-world corpus benchmarking |

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

## The Road to 1.0 (Hardening and Production Readiness)

### `0.7.0`: Real-World Corpus Benchmarking
- **Use Case:** Medical/Legal data mining.
- **Focus:** Integrate public datasets (Enron corpus, MIMIC-III synthetic variants, SEC filings) to establish precision/recall baselines for existing detectors.

### `0.8.0`: Adversarial Document Defenses
- **Use Case:** FOIA response redaction failures (e.g., Manafort, AstraZeneca leaks).
- **Focus:** Prevent visual-only masking, hidden OCR layers, overlapping z-index elements, and scrub incremental document revisions.

### `0.9.0`: Exhaustive Metadata & Hidden Structure Extraction
- **Use Case:** Corporate e-discovery.
- **Focus:** Parse PDF `/Info` dictionaries, XMP metadata, DOCX headers/footers, and XLSX comments.

### `0.10.0`: Large-Scale & Streaming Data Pipelines
- **Use Case:** Database dumps and bulk analytics exports.
- **Focus:** Bounded-memory processing for multi-gigabyte CSV/JSONL files; parallel block processing.

### `0.11.0`: Resilient Document Parsing
- **Use Case:** Legacy enterprise files.
- **Focus:** Gracefully handle corrupt XML schemas, custom OOXML namespaces, and safely extract embedded OLE objects.

### `0.12.0`: Advanced OCR Degradation Handling
- **Use Case:** Medical faxes and legacy legal scans.
- **Focus:** Handle low-dpi faxes, skewed pages, noisy backgrounds, and watermark interference mimicking structural data.

### `0.13.0`: ML Confidence Calibration & Thresholding
- **Use Case:** Reducing false positives in unstructured clinical notes.
- **Focus:** Tune ONNX backend confidence scores against ambiguous texts and introduce dynamic, policy-based confidence thresholds.

### `0.14.0`: Telemetry, Observability & Auditing
- **Use Case:** Enterprise compliance reporting and SLA monitoring.
- **Focus:** Structured JSON logging, processing timeouts, latency tracing, and detailed audit trails without leaking PII.

### `0.15.0`: Remote Backend Fault Tolerance
- **Use Case:** High-throughput API gateway integration.
- **Focus:** Circuit breakers, adaptive retries, rate-limit handling, and strict latency bounds for the HTTP provider transport.

### `0.16.0`: Cross-Lingual & Typographical Boundary Hardening (Pre-1.0 Audit)
- **Use Case:** Global support ticket sanitization.
- **Focus:** Audit detectors against non-Latin scripts, CJK spacing, RTL text, and bidirectional text overrides. Final security fuzzing (Zip-bombs, XXE).

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
