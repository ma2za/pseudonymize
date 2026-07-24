# Pseudonymize

[![PyPI](https://img.shields.io/pypi/v/pseudonymize.svg)](https://pypi.org/project/pseudonymize/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pseudonymize.svg)](https://pypistats.org/packages/pseudonymize)
[![Python](https://img.shields.io/pypi/pyversions/pseudonymize.svg)](https://pypi.org/project/pseudonymize/)
[![CI](https://github.com/ma2za/pseudonymize/actions/workflows/ci.yml/badge.svg)](https://github.com/ma2za/pseudonymize/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Typed](https://img.shields.io/badge/typing-py.typed-blue.svg)](src/pseudonymize/py.typed)

Typed, dependency-free, local-first PII pseudonymization for Python applications and LLM
payloads.

```text
Email paolo@example.com from 192.0.2.10.
                ↓
Email <EMAIL_1> from <IP_ADDRESS_1>.
```

Pseudonymize detects structured sensitive values locally and transforms them into numbered,
generic, deterministic, or redacted tokens. The base package has no runtime dependencies, performs
no telemetry or model downloads, and denies remote-capable backends by default.

> [!IMPORTANT]
> Pseudonymization is not anonymization. Detection can miss sensitive data, and transformed data
> can remain personal data. Review the [security model](docs/security.md) and
> [limitations](docs/limitations.md) before using the package with real data.

## Why Pseudonymize

- **Local by default.** The standard-library core makes no network calls.
- **Useful identity semantics.** Repeated normalized values share an alias inside an explicit
  processing scope.
- **Safe observability.** Detailed reports expose types, offsets, provenance, and counts without
  copying matched values.
- **Small installation.** The wheel is typed and has zero base runtime dependencies.
- **Explicit extension points.** Detection and format handling are separate, so custom backends
  and adapters do not replace the core policy and transformation logic.
- **Designed for LLM boundaries.** Nested payload processing preserves structure and lets policies
  include or exclude paths such as `messages.*.content`.

## What works today

| Capability | Status | Notes |
| --- | --- | --- |
| Strings | Shipped | Pseudonymization, redaction, batch processing, and safe reports |
| Nested Python data | Shipped | Dictionaries, lists, tuples, JSON scalars, and path policies |
| Structured detection | Shipped | Email, phone, IP, IBAN, payment card, URL credentials, and common secrets |
| Document representation | Shipped | Immutable blocks, typed locations, sanitized metadata, and inspection |
| Generic file orchestration | Shipped | Built-in or caller-provided adapters and atomic safe-copy output |
| TXT, Markdown, log, JSON, JSONL, and CSV files | Shipped | Explicit format or recognized suffix; no content guessing |
| Names, organizations, and locations | Planned | Requires a custom backend today; optional local NER is planned |
| PDF, Office, images, and OCR | Planned | Not supported by the current package |
| Remote providers | Contract only | No HTTP client or provider implementation is included |

The [roadmap](ROADMAP.md) separates shipped behavior from planned work.

## Installation

```console
python -m pip install pseudonymize
```

Python 3.11 through 3.14 is supported.

## Quickstart

### Transform text

```python
from pseudonymize import pseudonymize, redact

safe = pseudonymize("Email paolo@example.com")
hidden = redact("Email paolo@example.com")

assert safe == "Email <EMAIL_1>"
assert hidden == "Email [REDACTED]"
```

Numbered aliases are the default. Numbering starts from one for each convenience call.

### Get a safe report

```python
from pseudonymize import Pseudonymizer

result = Pseudonymizer().process_with_report(
    "Email paolo@example.com from 192.0.2.10."
)

assert result.output == "Email <EMAIL_1> from <IP_ADDRESS_1>."
assert result.statistics.detections_found == 2
assert result.detections[0].backend == "rules"
assert "paolo@example.com" not in repr(result)
```

Reports include entity type, block identifier, typed source location, relative offsets,
confidence, detector, backend provenance, and an optional replacement token. They never include
the matched value.

### Process an LLM payload

```python
from pseudonymize import Policy, Pseudonymizer

payload = {
    "model": "example-model",
    "messages": [
        {"role": "user", "content": "Email paolo@example.com"},
        {"role": "user", "content": "Use paolo@example.com again"},
    ],
    "temperature": 0.2,
}

result = Pseudonymizer(policy=Policy.llm()).process_data_with_report(payload)

assert result.output["messages"][0]["content"] == "Email <EMAIL_1>"
assert result.output["messages"][1]["content"] == "Use <EMAIL_1> again"
assert result.output["model"] == "example-model"
```

The input is not mutated. Dictionary keys and non-string values are preserved.

## Transformation modes

| Mode | Example | Identity behavior |
| --- | --- | --- |
| `numbered` | `<EMAIL_1>` | Stable inside one explicit scope |
| `generic` | `<EMAIL>` | Does not distinguish values of the same type |
| `deterministic` | `<EMAIL_K8M42PX7D3Q>` | Stable for the same key, namespace, type, and normalized value |
| `redacted` | `[REDACTED]` | Removes type and identity distinction |

```python
from pseudonymize import Pseudonymizer

scope = Pseudonymizer().new_scope()

assert scope.process("paolo@example.com").text == "<EMAIL_1>"
assert scope.process("maria@example.com and paolo@example.com").text == (
    "<EMAIL_2> and <EMAIL_1>"
)
```

Deterministic mode uses HMAC-SHA256 and requires a key of at least 32 bytes:

```python
engine = Pseudonymizer(
    mode="deterministic",
    key=b"a-32-byte-or-longer-secret-key...",
    namespace="customer-42",
)
```

Different tenants should use different keys or namespaces. The package never generates, stores,
or transmits a key silently.

## Documents and files

`Document` contains immutable `ContentBlock` values. Each block has a stable identifier, text, a
typed source location, and immutable JSON-scalar metadata. Detection offsets remain relative to
the block text.

`process_document()` returns a transformed document. `inspect_document()` returns detections
without transformed output.

`process_file()` selects a built-in adapter from an explicit format or a recognized suffix. It
never overwrites the source, defaults to `<stem>.safe<suffix>`, refuses an existing destination
unless `overwrite=True`, and publishes rendered bytes atomically:

```python
from pseudonymize import Pseudonymizer

result = Pseudonymizer().process_file("requests.json")

assert result.output.name == "requests.safe.json"
assert result.statistics.replacements_applied >= 0
```

TXT, Markdown, log, JSON, JSONL, and strict comma-separated CSV files are dependency-free.
`inspect_file()` reports detections without writing output. Pass `format="json"` to override an
unknown suffix or use `input_adapter` and `output_adapter` for a custom format.

JSON, JSONL, and CSV outputs preserve data semantics but normalize insignificant whitespace,
quoting, and record endings. UTF-8 is strict by default, an existing UTF-8 BOM is preserved, and
an explicit codec can be supplied with `encoding=`.

The CLI exposes the same workflow:

```console
pseudonymize file requests.json
pseudonymize inspect-file requests.json
```

## Detection backends

The dependency-free `RulesBackend` handles structured values. A custom backend receives one
`ContentBlock` and the active `Policy`, then returns relative `Detection` offsets. Backends declare
supported entity types, provenance, remote capability, and remote-processing consent.

`CompositeBackend` merges leaf results through the same deterministic overlap resolver used by the
core. Malformed and out-of-range detections fail with sanitized exceptions.

No capitalization heuristic is used for names. `PERSON`, `ORGANIZATION`, and `LOCATION` are public
entity types, but the base package does not detect them.

## Network policy

`NetworkPolicy.DENY` is the default. A remote-capable backend is called only when both conditions
are true:

1. The active policy is `ALLOW_CONFIGURED` with the backend allowlisted, or `ALLOW_ALL`.
2. The backend explicitly sets `allow_remote_processing=True`.

An API key alone never enables network access. The current package defines this security contract
but ships no remote provider or HTTP dependency.

## Reversible mappings

Mappings are opt-in and available only in numbered and deterministic modes:

```python
result = Pseudonymizer().process(
    "paolo@example.com",
    include_mapping=True,
)

assert result.restore("Reply to <EMAIL_1>.") == "Reply to paolo@example.com."
```

Mappings contain sensitive source values. They are hidden from `repr`, never persisted by the
package, and must be protected separately by the application.

## Alpha policy

The project is in active alpha development. Until the stable `0.1.0` release:

- public APIs, token details, adapters, and backend contracts may change between releases;
- architectural clarity and safe defaults take priority over backward-compatibility shims;
- deprecated aliases are not retained unless a release milestone explicitly requires them;
- every release documents material changes and raises or preserves the verification baseline.

Pin an exact prerelease when evaluating the package in an application.

## Development

```console
git clone https://github.com/ma2za/pseudonymize.git
cd pseudonymize
uv sync --all-groups
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
uv run mkdocs build --strict
```

Tests must use synthetic values only. New capabilities require positive, negative, boundary,
Unicode, adversarial, and cross-feature coverage where relevant.

Read [CONTRIBUTING.md](CONTRIBUTING.md), [SUPPORT.md](SUPPORT.md), and
[SECURITY.md](SECURITY.md) before opening an issue or pull request.

## Project status

- Package: [PyPI](https://pypi.org/project/pseudonymize/)
- Changes: [CHANGELOG.md](CHANGELOG.md)
- Architecture: [docs/architecture.md](docs/architecture.md)
- Vision: [VISION.md](VISION.md)
- Roadmap: [ROADMAP.md](ROADMAP.md)
- Licence: [Apache-2.0](LICENSE)
