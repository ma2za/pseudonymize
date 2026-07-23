# Migrating to 0.1.0a2

`0.1.0a2` replaces the provisional text-only backend protocol. There is no compatibility shim and
`EntityBackend` no longer exists.

## Backend contract

A text-only alpha backend previously accepted a string:

```python
class LocalNames:
    name = "local_names"

    def detect(self, text):
        ...
```

The block-aware backend declares its capabilities and remote behavior, then accepts a
`ContentBlock` and `Policy`:

```python
from pseudonymize import (
    BackendCapabilities,
    ContentBlock,
    Detection,
    EntityType,
    Policy,
)


class LocalNames:
    name = "local_names"
    capabilities = BackendCapabilities(frozenset({EntityType.PERSON}))
    allow_remote_processing = False

    def detect(
        self, block: ContentBlock, policy: Policy
    ) -> tuple[Detection, ...]:
        start = block.text.find("Paolo Mazza")
        if start < 0:
            return ()
        return (
            Detection(
                EntityType.PERSON,
                start,
                start + len("Paolo Mazza"),
                0.95,
                "local_names",
            ),
        )
```

Detection offsets remain relative to `block.text`. The executor adds backend provenance when the
returned `Detection` leaves its `backend` field empty. Returned entity types must be declared in
`capabilities`, and all offsets must fit inside the block.

Remote-capable backends set `remote=True` in `BackendCapabilities`. Invocation requires both an
allowing `NetworkPolicy` and `allow_remote_processing=True` on the backend. A failed consent check
raises before `detect` is called.

## Detailed results

`process()` still returns the existing `Result`, while `process_with_report()` returns safe
details:

```python
from pseudonymize import Pseudonymizer

result = Pseudonymizer().process_with_report("Email paolo@example.com")

assert result.output == "Email <EMAIL_1>"
assert result.detections[0].backend == "rules"
assert result.detections[0].token == "<EMAIL_1>"
```

Reports contain locations and relative offsets, never the matched value. The same model is used by
`process_data_with_report`, `process_document`, `inspect_document`, `process_file`, and
`inspect_file`.

## File adapters

`0.1.0a2` provides orchestration but no built-in file formats. Callers supply adapters explicitly:

```python
from pathlib import Path

from pseudonymize import ContentBlock, Document, Pseudonymizer, TextOffsetLocation


class TextInput:
    def extract(self, source: Path) -> Document:
        text = source.read_text(encoding="utf-8")
        block = ContentBlock("body", text, TextOffsetLocation(0, len(text)))
        return Document("input", (block,))


class TextOutput:
    def render(self, document: Document) -> bytes:
        return document.blocks[0].text.encode("utf-8")


result = Pseudonymizer().process_file(
    Path("request.custom"),
    TextInput(),
    TextOutput(),
)
```

The default output is `request.safe.custom`. Source overwrite is forbidden, existing destinations
require `overwrite=True`, and publication is atomic. Built-in TXT, JSON, JSONL, and CSV adapters
remain scheduled for `0.1.0a3`.
