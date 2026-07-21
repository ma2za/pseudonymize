# Product vision

Pseudonymize is a local-first Python toolkit for detecting and transforming sensitive information
in text, structured payloads, and documents. It uses lightweight local processing by default and
supports explicitly configured remote detection providers.

**Local by default. Format-aware. Backend-agnostic.**

## Product principles

1. **Keep the core small.** Text, JSON-compatible data, policies, deterministic transformations,
   and validated rule detectors remain dependency-free.
2. **Choose the best available modality.** Traverse structured values directly, use native text
   when present, preserve source locations, and use OCR only when native text is unavailable.
3. **Separate format handling from privacy logic.** Adapters extract and render content; backends
   detect entities; policies and transformers decide what happens to detections.
4. **Make network disclosure explicit.** The default network policy is `DENY`. A remote backend
   must be configured explicitly and separately consent to remote processing.
5. **Never put raw detections in reports.** Results expose locations, entity types, provenance,
   statistics, and warnings without copying sensitive values.
6. **Add formats only when they can be handled safely.** Detection-only support precedes document
   rewriting. PDF support must remove underlying content rather than draw visual overlays.
7. **Keep optional dependencies optional.** Importing `pseudonymize` must never import document,
   OCR, model, or HTTP packages.

## Modalities

The committed progression is:

1. Strings and nested JSON-compatible Python values.
2. Plain-text and machine-readable files.
3. Local natural-language entity recognition.
4. Detection-only inspection of PDF and Office documents.
5. Format-preserving document output.
6. Images, scanned PDFs, and mixed-document OCR.
7. Explicitly configured remote detection providers.

The package will use native structure or text before more expensive inference. A structured object
is traversed by path, a text PDF uses positioned text, and a scanned page uses OCR. A future remote
backend receives only blocks permitted by both the processing policy and network policy.

## Differentiation

Pseudonymize is not intended to win by accepting the largest number of file extensions. Its value
is a small local core, deterministic and namespace-isolated aliases, LLM-friendly dictionary
processing, safe reports, and extension contracts that do not force heavyweight dependencies on
base-package users.

## Non-goals

The committed roadmap excludes audio, video, reversible token vaults, database engines, Parquet,
SQLite, framework-specific wrappers, and generic claims to process every file. Pseudonymization
does not guarantee complete PII detection, anonymization, or regulatory compliance.
