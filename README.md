# Pseudonymize

Local-first semantic pseudonymization for text, JSON payloads, documents, and LLM applications.

**Detect once, transform in different ways.**

```text
I am Paolo Mazza and my email is paolo@example.com.
              ↓
I am <PERSON_1> and my email is <EMAIL_1>.
```

Person detection requires an optional local NER or custom detection backend. The dependency-free
core detects structured entities such as the email in this example. Pseudonymize processes data
locally by default; remote processing is disabled unless explicitly configured in a future backend.

The `0.1.0a2` API is a prerelease and may change before `0.1.0`.

## Installation

```console
pip install pseudonymize
```

The base package has no runtime dependencies and supports Python 3.11 or newer.

## Thirty-second example

```python
from pseudonymize import pseudonymize

safe_text = pseudonymize("Email paolo@example.com")

assert safe_text == "Email <EMAIL_1>"
```

Numbered semantic aliases are the default. Numbering starts from one for every convenience call.

## Transformation modes

| Mode | Example | Identity behavior |
| --- | --- | --- |
| `numbered` | `<PERSON_1>` | Stable for each normalized entity inside one scope |
| `generic` | `<PERSON>` | Does not distinguish entities of the same type |
| `deterministic` | `<PERSON_K8M42PX7D3Q>` | Stable across calls for the same key and namespace |
| `redacted` | `[REDACTED]` | Removes type and identity distinction |

```python
from pseudonymize import Pseudonymizer, TransformationMode

engine = Pseudonymizer(mode=TransformationMode.GENERIC)
assert engine.process("paolo@example.com").text == "<EMAIL>"

deterministic = Pseudonymizer(
    mode=TransformationMode.DETERMINISTIC,
    key=b"a-32-byte-or-longer-secret-key...",
    namespace="customer-42",
)
```

Typed redaction is available with `redact(text, typed=True)`, producing values such as
`[REDACTED_EMAIL]`.

## Alias scope

`engine.process(...)`, like the convenience function, uses a fresh alias scope for each call. Use
an explicit scope when multiple texts must share identity numbering:

```python
from pseudonymize import Pseudonymizer

scope = Pseudonymizer().new_scope()
first = scope.process("paolo@example.com")
second = scope.process("maria@example.com and paolo@example.com")

assert first.text == "<EMAIL_1>"
assert second.text == "<EMAIL_2> and <EMAIL_1>"
```

`process_batch` and each `process_data` call also use one shared scope across their complete input.

## Optional reversible mapping

Mappings are disabled by default and are available only for numbered and deterministic modes:

```python
result = Pseudonymizer().process("paolo@example.com", include_mapping=True)

assert result.mapping == {"<EMAIL_1>": "paolo@example.com"}
assert result.restore("Reply to <EMAIL_1>.") == "Reply to paolo@example.com."
```

Mappings contain personal or sensitive data. They are excluded from `repr(result)`, never logged or
persisted by the package, and must be protected separately by the application.

## LLM payloads

```python
from pseudonymize import Policy, Pseudonymizer

engine = Pseudonymizer(policy=Policy.llm())
payload = {
    "messages": [
        {"role": "user", "content": "Email paolo@example.com"},
        {"role": "user", "content": "Use paolo@example.com again"},
    ],
    "temperature": 0.2,
}

safe_payload = engine.process_data(payload)
```

Both occurrences become `<EMAIL_1>`. Container structure and non-string values remain unchanged,
and the input is not mutated.

## Safe reports and documents

Detailed APIs return transformed output together with reports that never copy matched values:

```python
from pseudonymize import Pseudonymizer

result = Pseudonymizer().process_with_report("Email paolo@example.com")

assert result.output == "Email <EMAIL_1>"
assert result.detections[0].entity_type == "EMAIL"
assert result.detections[0].backend == "rules"
assert result.statistics.replacements_applied == 1
```

`process_data_with_report`, `process_document`, and `inspect_document` use the same safe report
model. Documents contain immutable content blocks with stable identifiers, typed source locations,
and immutable JSON-scalar metadata.

`process_file` and `inspect_file` require caller-provided input and output adapters in `0.1.0a2`.
There is no built-in suffix detection or file-format adapter yet. Dependency-free TXT, JSON,
JSONL, and CSV adapters arrive in `0.1.0a3`.

## Detection backends

The core includes validated rules for email addresses, phone numbers, IPv4 and IPv6 addresses,
IBANs, payment cards, URL credentials, sensitive URL query values, and common credential formats.

`PERSON`, `ORGANIZATION`, and `LOCATION` are supported entity types but require an optional backend:

```python
engine = Pseudonymizer(backends=[RulesBackend(), local_ner_backend])
```

No person detector based on capitalization heuristics is included. Exact normalized matches such
as `Paolo Mazza` and `Paolo   Mazza` share an alias, but ambiguous references such as `Paolo` and
`Mr. Mazza` are not merged automatically.

Backends receive one `ContentBlock` and the active `Policy`, declare supported entity types and
remote capability, and return relative offsets. See the
[alpha migration guide](docs/migration-a2.md) for the complete contract.

## Security and limitations

Pseudonymize performs pseudonymization, not guaranteed anonymization. Pseudonymized data can remain
personal data. Detection has false positives and false negatives, and contextual information can
remain identifying. Logs, traces, retrieved documents, tool inputs, and tool outputs need the same
protection as prompts.

Deterministic mode uses HMAC-SHA256 over a versioned, domain-separated input. It requires a key of
at least 32 bytes; the package never generates or persists one silently. Different tenants should
use different keys or namespaces.

The default `NetworkPolicy.DENY` prevents remote-capable backends from being called. Permitting a
remote backend also requires a configured network policy and
`allow_remote_processing=True` on that backend. `0.1.0a2` defines and enforces this contract but
does not ship an HTTP client or remote provider.

## Migration from the initial prototype

- Numbered mode is now the default. Use `mode="deterministic"` when providing `key` and `namespace`.
- Generic mode produces typed placeholders such as `<EMAIL>`.
- `redact(...)` now produces `[REDACTED]`; use `typed=True` for `[REDACTED_EMAIL]`.
- Existing `<PZ1:TYPE:IDENTIFIER>` placeholders remain protected from reprocessing.
- The provisional text-only backend protocol is replaced by the block-aware contract in the
  [0.1.0a2 migration guide](docs/migration-a2.md). There is no compatibility shim.

## Roadmap and contributing

The full local-first document and backend plan is in [`VISION.md`](VISION.md) and
[`ROADMAP.md`](ROADMAP.md). See [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting changes.

## Licence

Apache-2.0. Optional model licences are reviewed and documented separately.
