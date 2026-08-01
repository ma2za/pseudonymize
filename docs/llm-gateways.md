# LLM gateway patterns

Pseudonymization belongs at every boundary where application data can leave the trusted process.
Sanitize prompts, retrieved content, tool arguments, and tool output independently. Do not assume
that protecting chat messages also protects traces, retries, caches, or provider error logs.

The complete runnable example is in
[`examples/llm_gateway.py`](https://github.com/ma2za/pseudonymize/blob/main/examples/llm_gateway.py).
It is executed by tests and again against the built wheel during package verification.

## Prompts

```python
from examples.llm_gateway import sanitize_prompt

safe_prompt = sanitize_prompt("Contact maria@example.com")
assert safe_prompt == "Contact <EMAIL_1>"
```

## Retrieval

Sanitize both the query and retrieved text before constructing the provider request:

```python
from examples.llm_gateway import sanitize_retrieval

safe = sanitize_retrieval(
    "Find maria@example.com",
    [{"id": "doc-1", "text": "Owner: maria@example.com"}],
)
assert safe["documents"][0]["text"] == "Owner: <EMAIL_1>"
```

## Tool calls

Tool names and numeric values pass through, while strings inside arguments are processed:

```python
from examples.llm_gateway import sanitize_tool_call

safe = sanitize_tool_call(
    "lookup_account",
    {"email": "maria@example.com", "limit": 5},
)
assert safe["arguments"]["email"] == "<EMAIL_1>"
```

## Tool output

Treat tool results as untrusted application data before returning them to a model:

```python
from examples.llm_gateway import sanitize_tool_output

safe = sanitize_tool_output(
    "lookup_account",
    {"email": "maria@example.com", "active": True},
)
assert safe["output"]["email"] == "<EMAIL_1>"
```

Each helper creates a fresh alias scope. A gateway that needs consistent aliases across several
boundaries should own one `Pseudonymizer.new_scope()` for that request and discard it afterward.
Never share numbered scopes between tenants or unrelated requests. For cross-request correlation,
use deterministic mode with tenant-specific key or namespace boundaries.
