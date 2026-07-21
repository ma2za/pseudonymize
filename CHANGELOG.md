# Changelog

All notable changes follow Keep a Changelog and Semantic Versioning.

## [Unreleased]

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

[Unreleased]: https://github.com/ma2za/pseudonymize/compare/v0.1.0a1...HEAD
[0.1.0a1]: https://github.com/ma2za/pseudonymize/releases/tag/v0.1.0a1
