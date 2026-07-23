# Product vision

Pseudonymize is the small, local-first privacy boundary between sensitive application data and the
systems that should not receive it unchanged.

It starts with Python strings and nested payloads, grows through format-aware documents and local
models, and permits remote processing only through an explicit security contract. The core remains
typed, dependency-free, offline-capable, and network-denied by default.

**Local by default. Structure-aware. Backend-agnostic. Safe to observe.**

## The problem

Applications increasingly move text and structured payloads through LLMs, logs, queues, analytics,
document pipelines, and third-party APIs. Sensitive values can cross those boundaries long before
a traditional data-loss-prevention system sees them.

Most teams need a composable library rather than another service:

- local processing for common identifiers;
- stable aliases when repeated identity matters;
- redaction when identity does not matter;
- safe reports for audit and testing;
- format-aware locations without coupling detectors to file libraries;
- optional stronger detection without forcing models or network clients on every installation.

Pseudonymize should make that boundary explicit and testable.

## Product principles

1. **Keep the trusted core small.** Text, nested data, policies, structured detectors,
   transformations, reports, and extension contracts remain standard-library only.
2. **Stay local unless the caller opts in twice.** `NetworkPolicy.DENY` is the default. Remote work
   requires both policy permission and backend-level consent.
3. **Use native structure before inference.** Traverse JSON paths directly, preserve document
   structure and coordinates, prefer native PDF text, and use OCR only when required.
4. **Separate format handling from privacy policy.** Adapters extract and render. Backends detect.
   Policies filter. Transformers replace. No layer silently takes ownership of another.
5. **Never make observability another leak.** Reports, statistics, warnings, exceptions, logs, CLI
   diagnostics, and representations must not copy matched source values.
6. **Make identity behavior explicit.** Numbered, generic, deterministic, and redacted modes have
   different semantics. Reversible mappings are always opt-in and treated as sensitive data.
7. **Add formats only when they can be handled safely.** Inspection precedes rewriting. A rendered
   PDF is accepted only when underlying content is removed, not visually covered.
8. **Keep optional dependencies narrow.** Models, PDF, Office, OCR, Docling, and HTTP libraries
   live only in the extras that own them and never load during a base import.
9. **Earn compatibility after the architecture is proven.** Alpha releases may replace public
   contracts without shims. Compatibility begins only at the documented stable milestone.
10. **Raise the verification bar with every release.** Coverage never falls below the tagged
    baseline. New tests must add realistic workflows, interacting invariants, malformed inputs,
    and adversarial failure modes rather than merely execute new lines.

## Product layers

```text
source
  -> input adapter
  -> immutable document and content blocks
  -> local or explicitly permitted detection backends
  -> policy, overlap resolution, identity resolution, transformation
  -> safe result and optional output adapter
```

Detectors operate on `ContentBlock` values, not on file formats. A JSON string, CSV cell, DOCX
paragraph, PDF text span, and OCR bounding box can therefore share detection logic while retaining
their own typed source locations.

## Modalities

The committed progression is:

1. Text and nested JSON-compatible Python values.
2. Dependency-free text, JSON, JSONL, and CSV files.
3. Optional local NER for names, organizations, locations, and contextual addresses.
4. Detection-only PDF and Office inspection.
5. Format-preserving document output and secure PDF redaction.
6. Local OCR for images, scanned PDFs, and mixed documents.
7. Explicitly configured remote providers with bounded transport behavior.

Native structure always wins over a more expensive or lossy modality.

## Who it is for

- Python developers building privacy-aware application and data pipelines
- Teams placing a local redaction boundary before hosted LLMs
- Security and privacy engineers who need inspectable, deterministic behavior
- Library authors implementing specialized document adapters or detection backends
- Researchers who need a small baseline with explicit limitations and reproducible tests

## Differentiation

Pseudonymize does not compete on the number of extensions it claims to accept. It competes on:

- a dependency-free, typed core;
- deterministic, namespace-isolated HMAC aliases;
- nested-payload and LLM-friendly processing;
- typed source locations across modalities;
- reports designed not to contain raw detections;
- explicit remote consent with no vendor SDK in the base package;
- increasingly adversarial, cross-platform release gates.

## Boundaries and non-goals

Pseudonymization does not guarantee anonymization, complete PII detection, regulatory compliance,
or immunity from contextual re-identification.

The committed roadmap excludes audio, video, reversible token vaults, database engines, Parquet,
SQLite, framework-specific wrappers, and generic claims to process every file. These can be
reconsidered only after the core roadmap is proven and should not distort the current architecture.

## Success

The project succeeds when an application can place a narrow local boundary around sensitive
content, choose the appropriate transformation, inspect what happened without leaking what was
found, and add only the format or detection dependencies it actually needs.
