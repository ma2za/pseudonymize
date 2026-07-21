# Quickstart

```python
from pseudonymize import Pseudonymizer

engine = Pseudonymizer()
result = engine.process("Contact maria@example.com")
print(result.text)
```

The result is `Contact <EMAIL_1>`. Numbering resets for each call; use `new_scope()` to share aliases
across calls. Deterministic aliases require `mode="deterministic"` and a securely managed key.
