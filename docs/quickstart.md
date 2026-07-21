# Quickstart

```python
from pseudonymize import Pseudonymizer, generate_key

engine = Pseudonymizer(key=generate_key(), namespace="tenant-a")
result = engine.process("Contact maria@example.com")
print(result.text)
```

Store the generated key in a secret manager. Reusing a key and namespace makes equal normalized
values produce equal aliases.
