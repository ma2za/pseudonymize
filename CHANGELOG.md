# Changelog

All notable changes follow Keep a Changelog and Semantic Versioning.

## [Unreleased]

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

[Unreleased]: https://github.com/ma2za/pseudonymize/compare/v0.1.0a2...HEAD
[0.1.0a2]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0a2
[0.1.0a1]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0a1
