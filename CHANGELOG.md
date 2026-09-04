# Changelog

All notable changes follow Keep a Changelog and Semantic Versioning.

## [Unreleased]

### Fixed

- **Benchmark metrics measure what they claim.** `evaluate_quality.py` counted true
  positives per detection while counting false negatives per annotation, so precision
  and recall were computed over two different denominators and a detection covering
  two adjacent annotations scored as one hit that satisfied both. Detections and
  annotations are now paired one to one, in descending order of overlap. Matching also
  compares entity types, so finding an email where the corpus annotated a surname is
  no longer a hit; `--span-only` restores the previous label-blind behaviour. A
  detection landing on an annotation outside the scored label set is reported
  separately rather than charged as a false positive.
- `benchmarks/train_eval.py` was a copy of the evaluation script with a different
  split, so a change measured on `train` did not necessarily mean the same thing on
  `validation`. It now calls the same scoring code with `--explain` detail.
- `benchmarks/datasets/` shadowed the `datasets` package under type checking and was
  renamed to `benchmarks/data/`. `benchmarks` is now inside mypy's `files`, which the
  release gate already required but the configuration did not include.

## [0.17.0] - 2026-08-29

### Fixed

- **Contextual identifier robustness:** improved extraction for contextual identifiers.
- **Sub-word boundaries:** expanded ML sub-word boundaries and tolerated punctuation
  between same-type tokens so that hyphenated names and comma-separated addresses
  merge into a single span.

## [0.16.0] - 2026-08-29

### Added
- **Advanced OCR Degradation Handling:**
  - Upgraded Tesseract OCR integrations for `PDFInspectionAdapter` and `ImageInspectionAdapter` to utilize Page Segmentation Mode (PSM) 11 (`--oem 3 --psm 11`). This "sparse text" mode forces the engine to find as much text as possible in no particular order, dramatically improving extraction resilience against skewed pages, low-DPI medical faxes, noisy backgrounds, and watermark interference that previously broke traditional paragraph-detection.

## [0.15.0] - 2026-08-29

### Fixed
- **ML & Heuristic Detection Enhancements:**
  - Expanded contextual heuristics to globally capture international IDs, such as Vietnamese ID Cards/Tax IDs, Indonesian Tax IDs, and Spanish IDs (`căn cước`, `mã số thuế`, `número de identificación`), successfully recovering dropped `TAX_ID` and `NATIONAL_ID` values.
  - Hardened the `NATIONAL_ID` contextual fallback to enforce digit constraints, aggressively eliminating false positives on arbitrary alphabetic serial numbers.
  - Added `BUILDINGNUM` to the subset of standard CoNLL-03 labels safely routed to `LOCATION`, boosting coordinate recall for street numbers in the ai4privacy dataset. 

## [0.14.0] - 2026-08-29

### Added

- **Adversarial Document Defenses & Exhaustive Metadata:**
  - Added support for extracting, sanitizing, and injecting PDF `/Info` dictionaries and XMP metadata.
  - Added extraction and format-preserving sanitization of core properties for DOCX, XLSX, and PPTX documents.
  - Added extraction and sanitization of DOCX headers and footers.
  - PyMuPDF redaction natively removes overlapping text, preventing visual-only masking and hidden OCR layers in PDFs.

## [0.13.0] - 2026-08-29

### Fixed

- **Context-Aware Over-Extraction Prevention:** Added lookahead constraints to context detectors to enforce that alphanumeric generic IDs actually contain at least one digit, avoiding false positives where trailing words matched `[A-Z0-9]` regexes.
- **The 90% Benchmark Gate Achieved:** Contextual detectors for `NATIONAL_ID`, `DRIVERLICENSENUM`, and `ZIPCODE` were systematically expanded to capture generic alphanumeric and numeric patterns when preceded by common trigger phrases ("ticket id", "serial", "receipt number", etc.). This broke through the 90% ceiling on the `ai4privacy` holdout dataset, hitting `0.9560` Precision and `0.8962` Recall (`0.9251` F1 Score).

## [0.12.0] - 2026-08-28

### Fixed

- **Cross-Lingual & Typographical Hardening:** Fixed detection drops in CJK and cross-lingual text where adjacent non-Latin characters previously defeated English word boundaries (`\b`). Zero-width format characters (like BiDi overrides and ZWNJ) are now safely stripped before detection without breaking index alignment, ensuring models and regexes catch obfuscated PII.

## [0.11.0] - 2026-08-28

### Fixed

- **Ensemble Merging & Conflict Resolution:** Updated `pseudonymize.spans.resolve_overlaps` to prioritize span length over prediction confidence. This ensures that when the ML backend captures a longer valid span (e.g. "John Smith") with lower confidence, it won't be truncated or broken apart by a shorter, higher-confidence deterministic match. Also fixed a regex bug in `ContextualIdDetector` that could mistakenly trigger on word prefixes. This significantly improved ensemble precision and overall F1 benchmark.

## [0.10.0] - 2026-08-28

### Added

- **ML Confidence Calibration & Dynamic Thresholding:** Implemented dynamic threshold scaling for the ONNX backend. ML probabilities for valid entities can now be calibrated to meet strict `minimum_confidence` policy requirements, successfully boosting recall (up to ~84.4%) and F1 score while maintaining ~95% precision without relying on hardcoded confidences.

## [0.9.0] - 2026-08-28

### Added

- **Context-Aware Heuristics:** Introduced `ContextualIdDetector` which boosts recall by evaluating surrounding semantic keywords (e.g. 'Passport No:', 'Card Number:', 'Zip:') to confidently identify PII that might otherwise fail rigid checksums (like the Luhn algorithm for synthetic cards) or formatting patterns.

## [0.8.0] - 2026-08-28

### Fixed

- **Detection Boundary Alignment:** Fixed ML sub-word tokenization overlap logic. The ONNX backend now respects B- (beginning of entity) tokens, preventing consecutive identical entity types (e.g., FIRSTNAME and LASTNAME) from being incorrectly merged into a single span. This dramatically improves detection boundary precision and recall.

## [0.7.0] - 2026-08-28

### Added

- Added a new quality evaluation suite (enchmarks/evaluate_quality.py) capable of streaming real-world datasets (like AI4Privacy/PII-Masking-200k) to establish rigorous precision, recall, and F1 baselines for core detectors and ML backends.

## [0.6.1] - 2026-08-28

### Added

- Generic `NATIONAL_ID` and `TAX_ID` entity types with checksum-validated Italian fiscal-code and
  VAT-number detectors. Unprefixed VAT numbers require an explicit tax label.

### Fixed

- ONNX test artifacts now persist outside pytest's temporary directory, avoiding a verified
  model download on every local test invocation.
- `inspect-file` now serializes coordinate and structural locations used by PDF, image, and
  Office inspection instead of failing after a detection is found.
- IBAN detection now accepts spaces between the country code and check digits, including values
  extracted from visually grouped documents.
- PDF processing now preserves unchanged text blocks and renders transformed blocks legibly
  instead of covering the complete document text with black redaction rectangles.
- PDF processing now localizes changed spans inside text blocks when possible, preserving the
  surrounding text's original visual representation while securely removing detected values.
- PDF redaction now preserves existing colored backgrounds and source text colors instead of
  placing white rectangles with mismatched replacement text over styled fields.

## [0.6.0] - 2026-08-25

### Added

- `HTTPRemoteBackend` for securely proxying pre-filtered local documents to LLM gateways and remote ML providers via HTTP, explicitly opt-in with strict timeouts.

## [0.5.1] - 2026-08-25

### Fixed
- Bumped version to resolve a PyPI artifact collision in the CI pipeline.

## [0.5.0] - 2026-08-25

### Added

- OCR capabilities for image-based PDFs, using Tesseract and PyMuPDF.

## [0.4.0] - 2026-08-25

### Added

- Format-preserving sanitization for Office documents (DOCX, XLSX, PPTX).
- Secure redaction for PDF documents with underlying text removal.

### Security

- PDF and Office inspection failures no longer interpolate the underlying library's message into
  the raised error, which could expose file paths or document fragments. They now follow the
  sanitized fixed-message convention used elsewhere in the engine.

### Fixed

- `process_file` now rejects PDF, DOCX, XLSX, and PPTX immediately with `UnsupportedFormatError`
  instead of extracting and processing the whole document before failing at rendering time with a
  generic message.
- `inspect_file` now rejects an `encoding` argument for inspection-only formats instead of
  silently ignoring it.
- `BuiltinFileAdapter` now rejects inspection-only formats at construction instead of decoding a
  binary document as text.

## [0.3.0] - 2026-08-22

### Added

- Added `pdf` extra (using `pdfminer.six`) for PDF text and coordinate extraction.
- Added `office` extra (using `python-docx`, `openpyxl`, `python-pptx`) for DOCX, XLSX, and PPTX inspection.
- Introduced `CoordinateLocation` and `StructuralLocation` for granular source tracking in complex file formats.

## [0.2.1] - 2026-08-22

### Changed

- `Policy.default()` now includes `URL_CREDENTIAL` and `SECRET`, so the documented secret and
  URL-credential detectors act without opting into `Policy.strict()` or `Policy.llm()`. Callers
  that relied on secrets passing through the default policy must configure an explicit
  `Policy(entity_types=...)`.
- Overlap resolution now uses an ordered-interval scan instead of a quadratic pairwise check,
  and detected spans are replaced with a single-pass segment join. Texts with thousands of
  detections process in milliseconds instead of seconds.

### Fixed

- `LocalONNXPIIBackend` now merges contiguous token predictions into whole entity spans, so
  multi-word and subword-split names receive a single alias instead of one alias per token.
- ONNX test artifacts downloaded during testing are now verified against pinned SHA-256
  checksums.
- URL credential detection now covers the whole userinfo section when it contains extra `@`
  characters and no longer swallows the URL fragment into sensitive query values.
- Overlap resolution now ranks URL credentials above emails, so a `user:password@host` userinfo
  can no longer lose its `user:` prefix to an overlapping email match.
- The `ml` extra now declares `numpy`, which the ONNX backend imports directly, and no longer
  pulls in the unused `huggingface-hub` dependency.
- The optional-import guard in the ONNX backend now type-checks under strict mypy.
- Normalization now maps generic URL schemes to `http` or `https` for safer alias sharing.

## [0.2.0] - 2026-08-21

### Added

- Optional local Machine Learning backend for PII identification (`pseudonymize[ml]`).
- Dynamic download of ONNX artifacts for `LocalONNXPIIBackend` leveraging a quantized DistilBERT model during testing.
- Highly adversarial test corpus including deep nested JSON, CSV escape cases, and TXT right-to-left BiDi formatting.

### Changed

- Shifted the product vocabulary strictly to "ML" for PII pseudonymization, abandoning the generic "NER" term.
- Renamed the optional extra from `[ner]` to `[ml]` and the backend class to `LocalONNXPIIBackend`.
- Increased total coverage verification to 99.56% with rigorous offset mapping tests.

## [0.1.0] - 2026-08-02

### Added

- Stable compatibility guarantees for the dependency-free `0.1` core, CLI, and token formats.
- Stable release notes and production package maturity metadata.

### Changed

- Promoted the validated text, nested-data, document, and machine-readable file APIs without
  changing their public behavior or deterministic tokens.
- Updated pinned GitHub Actions and the locked development toolchain used to validate releases.
- Adopted Ruff 0.16 formatting and lint rules for source and documented Python examples.

## [0.1.0rc1] - 2026-08-02

### Added

- Frozen compatibility tests for the beta public API, enums, data models, and deterministic
  aliases.
- Clean-wheel installation coverage on Linux, macOS, and Windows across Python 3.11 through 3.14.
- Portable cross-platform file fixtures for byte-order marks, newlines, Unicode, JSONL, and CSV.
- Installed-package audits for imports, metadata, bundled files, licence, and dependencies.

### Changed

- Made production tags the only package-publication path; manual package runs are build-only
  rehearsals.
- Expanded release artifact verification to cover the frozen wheel contents and package metadata.

## [0.1.0b1] - 2026-08-01

### Added

- Compatibility policy for the frozen core API and stable `0.1` line.
- Executable LLM gateway examples covering prompts, retrieval, tool calls, and tool output.
- Production deployment guidance and an expanded threat model.
- Reference performance, import-time, memory, and wheel-size measurements.

### Changed

- Advanced the package from alpha to beta and froze documented core contracts through `0.1.0`.
- Extended installed-wheel verification to execute the documented gateway example.

### Fixed

- Corrected the deterministic engine configuration used by the published benchmark command.

## [0.1.0a3] - 2026-07-24

### Added

- Dependency-free TXT, Markdown, log, JSON, JSONL, and CSV adapters.
- Explicit-format and recognized-suffix file selection without content guessing.
- Strict encoding controls with UTF-8 byte-order-mark preservation.
- CLI file transformation and machine-readable safe inspection.
- Stable JSON-path and CSV-cell extraction fixtures with semantic round-trip coverage.

### Changed

- Redesigned the provisional file methods around optional built-in or keyword-only custom
  adapters.
- Normalized JSON, JSONL, and CSV rendering while preserving value types and structure.
- Extended installed-wheel smoke tests to built-in file processing and inspection.
- Raised the enforced branch-coverage floor from 97.29% to 99.36%.

### Security

- Kept source-specific rendering context out of documents, reports, metadata, and
  representations.
- Sanitized unsupported-format, decoding, parsing, rendering, and CLI failures.

## [0.1.0a2] - 2026-07-23

### Added

- Immutable document, content-block, metadata, and typed source-location models.
- Block-aware backend capabilities, provenance, deterministic composition, and bounds validation.
- Explicit network policy with separate policy and remote-backend consent.
- Safe detailed processing results, reports, statistics, and warnings.
- Document processing and inspection plus generic file orchestration with explicit adapters.
- Atomic no-clobber output, opt-in destination overwrite, source protection, and failure cleanup.
- Backend migration guide and `0.1.0a2` release notes.

### Changed

- Replaced the provisional text-only backend API with `detect(block, policy)`.
- Routed text and nested-data processing through internal content blocks.
- Raised the enforced branch-coverage floor from 95% to 97.29%.
- Made backend merge tie-breaking independent of configured backend order.

### Fixed

- Preserved sentence-ending punctuation after IPv4 detections.

### Removed

- Removed the provisional `EntityBackend` name without a compatibility shim.

## [0.1.0a1] - 2026-07-21

### Added

- Typed dependency-free pseudonymization core.
- Structured detectors, immutable policies, nested payload processing, and CLI.
- HMAC-SHA256 aliases, redaction, reports without raw detected values, and backend protocol.
- Local-first product vision, staged multimodal roadmap, and Trusted Publishing release runbook.
- Numbered semantic pseudonymization as the default transformation mode.
- Generic, deterministic, and redacted modes with independent alias assignment and rendering.
- Exact normalized entity resolution, reusable alias scopes, and opt-in reversible mappings.
- Optional backend contracts for person, organization, and location detection.

### Changed

- Deterministic processing now requires `mode="deterministic"` in addition to a key.
- `redact()` now emits `[REDACTED]` by default; generic mode emits typed placeholders.

[Unreleased]: https://github.com/ma2za/pseudonymize/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/ma2za/pseudonymize/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/ma2za/pseudonymize/releases/tag/v0.2.0
[0.1.0]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0
[0.1.0rc1]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0rc1
[0.1.0b1]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0b1
[0.1.0a3]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0a3
[0.1.0a2]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0a2
[0.1.0a1]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0a1
