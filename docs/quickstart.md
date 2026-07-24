# Quickstart

```python
from pseudonymize import Pseudonymizer

engine = Pseudonymizer()
result = engine.process("Contact maria@example.com")
print(result.text)
```

The result is `Contact <EMAIL_1>`. Numbering resets for each call; use `new_scope()` to share aliases
across calls. Deterministic aliases require `mode="deterministic"` and a securely managed key.

Process a supported file without configuring an adapter:

```python
result = engine.process_file("payload.json")
print(result.output)
```

The default destination is `payload.safe.json`. The source is never overwritten. Use
`inspect_file("payload.json")` to return safe detection details without writing an output file.
