# Pseudonymize

Pseudonymize is a typed, dependency-free, local-first toolkit for detecting and transforming
sensitive values in Python applications and LLM payloads.

The core has no runtime dependencies, makes no network calls, and provides numbered, generic,
deterministic, and redacted transformations for strings, nested data, TXT, Markdown, log, JSON,
JSONL, and CSV files. Safe detailed results expose locations and provenance without copying
matched values.

Start with the [quickstart](quickstart.md), then read the [architecture](architecture.md),
[policies](policies.md), [security model](security.md), and [limitations](limitations.md).

The API is in active alpha development. Contracts may change without compatibility shims before
the stable `0.1.0` release.
