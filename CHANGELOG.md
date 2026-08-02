# Changelog

All notable changes follow Keep a Changelog and Semantic Versioning.

## [Unreleased]

## [0.1.0] - 2026-08-09

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

[Unreleased]: https://github.com/ma2za/pseudonymize/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0
[0.1.0rc1]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0rc1
[0.1.0b1]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0b1
[0.1.0a3]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0a3
[0.1.0a2]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0a2
[0.1.0a1]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0a1
