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

## The Road to 90% (Detection Quality Focus)

The current core engine falls short of production-grade precision and recall on real-world datasets. Reaching a consistent 90% baseline across Precision, Recall, and F1 metrics is the strict prerequisite before pursuing any new extraction features (like advanced parsing or metadata). Releases 0.8.0 through 0.13.0 are exclusively dedicated to accuracy.

### `0.8.0`: Detection Boundary & Tokenization Alignment
- **Use Case:** Preventing partial string matches and sub-word truncation.
- **Focus:** Resolve token overlaps, enforce strict word boundaries on regex engines, and align ML sub-word tokens back to exact character spans to immediately improve recall.

### `0.9.0`: Context-Aware Heuristics & Rule Augmentation
- **Use Case:** Resolving ambiguous numbers and false-positive IDs.
- **Focus:** Augment regex and algorithmic rules with surrounding text context (e.g., distinguishing an account number from a random digit sequence using adjacent keywords).

### `0.10.0`: ML Confidence Calibration & Dynamic Thresholding
- **Use Case:** Reducing false positives in unstructured clinical/legal notes.
- **Focus:** Tune ONNX backend confidence scores against ambiguous texts and introduce dynamic, policy-based confidence thresholds to balance precision and recall.

### `0.11.0`: Ensemble Merging & Conflict Resolution
- **Use Case:** Preventing duplicate or conflicting entity tags.
- **Focus:** Improve resolution logic when deterministic rules and ML backends flag the same or overlapping text with different entity labels.

### `0.12.0`: Cross-Lingual & Typographical Hardening
- **Use Case:** Global support ticket sanitization.
- **Focus:** Fix detection drops caused by non-Latin scripts, CJK spacing, RTL text, and bidirectional text overrides.

### `0.13.0`: The 90% Benchmark Gate (Custom Fine-Tuning Pathways)
- **Use Case:** Hitting the accuracy ceiling.
- **Focus:** Provide mechanisms to load domain-specific, fine-tuned models (e.g., Legal or Medical BERT variants) if the base model hits a ceiling. **This release acts as the barrier; subsequent roadmap items will not proceed until benchmarks pass 90%.**

## Post-90% Target Capabilities

### `0.14.0`: Adversarial Document Defenses & Exhaustive Metadata
- **Use Case:** FOIA response redaction failures and corporate e-discovery.
- **Focus:** Prevent visual-only masking, hidden OCR layers, overlapping z-index elements, and parse PDF `/Info` dictionaries, XMP metadata, DOCX headers/footers.

### `0.15.0`: Resilient Document Parsing & Large-Scale Pipelines
- **Use Case:** Legacy enterprise files and database dumps.
- **Focus:** Gracefully handle corrupt schemas, extract embedded OLE objects, and process multi-gigabyte files via bounded memory streams.

### `0.16.0`: Advanced OCR Degradation Handling
- **Use Case:** Medical faxes and legacy legal scans.
- **Focus:** Handle low-dpi faxes, skewed pages, noisy backgrounds, and watermark interference mimicking structural data.

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
