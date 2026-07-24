# Migrating to 0.1.0a3

`0.1.0a3` replaces the provisional positional file-adapter signature from `0.1.0a2`. Alpha
releases do not retain compatibility shims.

## Built-in formats

TXT, Markdown, log, JSON, JSONL, and CSV files now need no adapter arguments:

```python
from pseudonymize import Pseudonymizer

result = Pseudonymizer().process_file("payload.json")
inspection = Pseudonymizer().inspect_file("payload.csv")
```

An explicit format overrides suffix selection:

```python
result = Pseudonymizer().process_file("payload.data", format="json")
```

Unknown suffixes are rejected without content inspection.

## Custom adapters

Move custom adapters to keyword arguments:

```python
result = Pseudonymizer().process_file(
    "input.custom",
    "output.custom",
    input_adapter=CustomInputAdapter(),
    output_adapter=CustomOutputAdapter(),
)

inspection = Pseudonymizer().inspect_file(
    "input.custom",
    input_adapter=CustomInputAdapter(),
)
```

Custom adapters cannot be mixed with built-in `format` or `encoding` options. Processing requires
both adapters; inspection requires only an input adapter.

## Structured output

JSON, JSONL, and CSV promise semantic, not lexical, round trips. Values, types, order, records,
rows, and cells are preserved, but whitespace, quoting, escapes, and record endings may be
normalized. JSON object keys are not transformed.

UTF-8 is strict by default. An existing UTF-8 byte-order mark is preserved. Use `encoding=` when a
different codec is required; no fallback or content-based encoding detection occurs.
