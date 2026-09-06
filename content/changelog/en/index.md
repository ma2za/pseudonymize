---
title: "Changelog"
lastUpdated: "2026-09-06"
---

# Changelog

All notable changes to the pseudonymize.io managed API and open-source engine will be documented in this file.

## [2026-09-06]
### Added
- **Predictable transformations:** Expanded core documentation around scopes, determinism, and behavior under uncertainty.
- **Identity Consistency:** Implemented sequential pseudonym tracking per-request to ensure robust context handling for LLMs.
- **Developer Onboarding:** Introduced automated API key generation during the first sign-up flow, drastically reducing Time to First Successful Request (TTFSR).

### Improved
- Complete UI refactoring to enforce full semantic dark mode across the entire dashboard and documentation platform.
- Re-architected marketing site to clearly delineate Redaction vs Pseudonymization.

### Security
- Published reproducible benchmarks directly on the marketing domain.
- Formalized zero-retention application lifecycle in the Security Architecture.

## [2026-08-15]
### Added
- Initial managed API launch (Release 1.0).
- Text, Structured Data, and File parsing endpoints.
- Base integration with local NER models and exact validators.
