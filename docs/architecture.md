# Architecture

Text processing separates identity and presentation:

```text
Input -> detection -> overlap resolution -> entity resolution
      -> alias assignment -> transformation rendering -> result
```

Exact normalized matching is the initial entity resolver. It deliberately does not merge partial
names or other ambiguous references. Alias assignment owns numbered or deterministic identity;
rendering owns placeholder or redaction syntax.

The long-term multimodal pipeline has five independent layers:

```text
Input adapter
    -> content representation
    -> detection backends
    -> policy and transformations
    -> output adapter
```

The dependency-free `0.1.0a2` release routes text, nested data, documents, and caller-supplied file
adapters through this representation. These interfaces remain provisional until beta.

## Content representation

Every adapter extracts an immutable `Document` containing immutable `ContentBlock` instances. A
block has a stable identifier, text, a typed source location, and sanitized metadata. Metadata is
copied into an immutable mapping and must not contain extracted text or credentials.

Initial location variants represent text offsets, JSON paths, and CSV row and column coordinates.
Future variants add PDF page rectangles, spreadsheet cells, DOCX elements, and presentation slide
elements. Detector offsets remain relative to block text; safe reports combine those offsets with
the block location without carrying the matched value.

## Adapters

`InputAdapter` extracts a `Document` from a caller-defined source type. `OutputAdapter` renders
bytes from a transformed document. Adapters understand serialization and layout, but never choose
entity types or detection thresholds.

In `0.1.0a2`, file APIs require explicit caller-provided adapters and perform no format selection.
File transformation writes atomically, never overwrites the source, defaults to
`<stem>.safe<suffix>`, and requires `overwrite=True` for an existing destination. Built-in format
selection begins in `0.1.0a3`; explicit format then takes precedence over recognized suffixes, and
unknown formats fail rather than being guessed.

Extraction support always precedes rendering support. Office and PDF adapters first provide
detection-only inspection. A PDF renderer is accepted only when tests prove the underlying content
is removed rather than merely covered.

## Detection backends

`DetectionBackend.detect(block, policy)` accepts one content block and the active policy.
`RulesBackend` adapts the existing structured detectors. `CompositeBackend` invokes leaf backends
through the same policy-enforcing executor and sends all candidates through one deterministic
overlap resolver. Each detection records both detector and backend provenance.

Backends declare capabilities and provenance. They do not transform content, write files, log
matched text, or silently perform network calls. Local NER and OCR are optional backends with
explicit model paths and no import-time or first-inference downloads.

## Policy and transformation

Policies choose entity types, confidence thresholds, detector priorities, paths, permitted blocks,
and network behavior. Transformations implement redaction or deterministic aliases independently
of source format. Existing HMAC normalization and token versioning remain the alias contract.

The network policy is `DENY`, `ALLOW_CONFIGURED`, or `ALLOW_ALL`, with `DENY` as the default. A
remote-capable backend must additionally be constructed with `allow_remote_processing=True`.
Possessing an API key never enables network access.

`ALLOW_CONFIGURED` additionally requires the backend name in the policy's immutable allowlist.
`ALLOW_ALL` removes only that allowlist check. Both modes still require the backend's explicit
`allow_remote_processing=True` consent.

## Results

Convenience APIs keep returning transformed values. Explicit report APIs return
`ProcessingResult[T]` with:

- The transformed output or output path
- Safe detection reports containing type, location, confidence, and backend provenance
- Counts for processed blocks and local or remote activity
- Warnings that contain no source content

Reports, exceptions, logs, CLI diagnostics, and object representations must never contain the raw
detected value. File inspection can return a report before a safe renderer exists.

## Optional dependency boundary

The root package imports only the standard-library core. Optional imports occur inside their owning
adapter or backend loader and raise a targeted missing-extra error. PDF, Office, OCR, NER, Docling,
and HTTP dependencies are never imported by `import pseudonymize`.

See the [0.1.0a2 migration guide](migration-a2.md) for the backend change and the
[release roadmap](https://github.com/ma2za/pseudonymize/blob/main/ROADMAP.md) for later adapters.
