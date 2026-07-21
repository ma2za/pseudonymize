# Release roadmap

Alpha releases may change public APIs. Compatibility commitments begin with `0.1.0` and expand at
`1.0.0`. A release ships only after its exit criteria pass on every supported platform.

## 0.1.0: dependency-free core and machine-readable content

### 0.1.0a1: reserve the package and publish the tested core

- Strings, nested dictionaries, lists, and tuples
- Email, phone, IP, IBAN, payment-card, URL-credential, and common-secret detectors
- Deterministic HMAC aliases, redaction, policies, safe reports, batch processing, and CLI
- Python 3.11 through 3.14, typed wheel, and zero runtime dependencies

Exit: strict quality checks pass, branch coverage is at least 95%, artifacts install in a clean
environment, TestPyPI rehearsal succeeds, and the tagged artifact is published through OIDC.

### 0.1.0a2: representation and extension contracts

- Immutable `Document` and `ContentBlock`
- Typed text-offset, JSON-path, and CSV-cell locations
- `InputAdapter`, `DetectionBackend`, and `OutputAdapter` protocols
- `RulesBackend` and `CompositeBackend`
- `ProcessingResult`, safe reports, statistics, warnings, and `NetworkPolicy`

Exit: contract tests prove stable extraction, deterministic backend merging, safe representations,
and that `NetworkPolicy.DENY` cannot invoke a remote-capable backend.

### 0.1.0a3: dependency-free file adapters

- `.txt`, `.md`, `.log`, JSON, JSONL, and CSV
- Detection-only inspection and sanitized-copy APIs
- Explicit format selection before suffix-based selection
- Atomic output with `<stem>.safe<suffix>` defaults and opt-in overwrite

Exit: cross-platform fixtures cover encoding, malformed records, Unicode locations, symlinks,
large fields, interrupted writes, destination collisions, and supported round trips.

### 0.1.0b1: API freeze

- Public API and compatibility policy frozen
- Alpha migration notes and complete architecture documentation
- Realistic LLM request, tool-call, tool-output, and retrieval examples
- Published limitations, threat model, and reference benchmarks

Exit: no unresolved public-API decisions and all documented examples run from the built wheel.

### 0.1.0rc1: external release validation

- Clean installation tests across supported operating systems and Python versions
- Packaging, import-time, dependency, and bundled-file audit
- TestPyPI rehearsal and external integration feedback

Exit: only release-blocking defects may change code; any API change returns the project to beta.

### 0.1.0: first stable release

Stable text, nested data, and plain or machine-readable file processing with no runtime dependency.

## Later capabilities

### 0.2.0: optional local NER

Add explicitly installed ONNX models for people, organizations, locations, and contextual
addresses. Benchmark English, German, and Italian. Model revisions and checksums are pinned; model
downloads never occur during import or first inference.

### 0.3.0: document inspection

Add optional PDF, DOCX, XLSX, and PPTX extraction with coordinate or structural locations.
Support is detection-only so the representation can mature before document mutation is trusted.

### 0.4.0: format-preserving documents

Produce sanitized DOCX, XLSX, and PPTX copies, securely redact text PDFs, remove relevant document
metadata, and validate output integrity with application-specific fixtures.

### 0.5.0: OCR and scanned documents

Add local OCR for images, scanned PDFs, and mixed PDFs with bounding-box transformations. Native
text remains preferred whenever it is reliable.

### 0.6.0: remote detection

Add a vendor-neutral provider protocol, optional HTTP transport, explicit dual consent, timeouts,
bounded retries, provider capability declarations, remote audit statistics, and a mode that locally
replaces structured identifiers before permitted blocks are sent remotely.

### 1.0.0: mature compatibility commitment

Commit to long-term interfaces after core processing, document rewriting, OCR, and remote-security
contracts have production fixtures, published benchmarks, and independent user feedback.

## Optional dependency policy

Extras appear only with their owning release: `ner`, `pdf`, `office`, `ocr`, `documents`, `docling`,
and `remote`. An `all` extra may exist for testing, but documentation will recommend the narrowest
extra that satisfies the user's workload.
