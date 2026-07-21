# Pseudonymize

Local-first PII detection, redaction and deterministic pseudonymization for text, JSON payloads,
documents and LLM applications.

Pseudonymize processes data locally by default. Remote processing is disabled unless explicitly
configured. The `0.1.0a1` API is a prerelease and may change before `0.1.0`.

## Installation

```console
pip install pseudonymize
```

The base package has no runtime dependencies and supports Python 3.11 or newer.

## Thirty-second example

```python
from pseudonymize import pseudonymize

safe_text = pseudonymize(
    "Email maria@example.com",
    key=b"a-32-byte-or-longer-secret-key...",
)
```

The output is a stable token such as `Email <PZ1:EMAIL:QF7S8G2JW4NC6T9R>`. Use
`redact("Email maria@example.com")` when linkability is not needed.

## Supported entity types

The dependency-free detectors cover email addresses, phone numbers, IPv4 and IPv6 addresses,
MOD-97-valid IBANs, Luhn-valid payment cards, URL credentials, sensitive URL query values, and
common credential formats. Policies decide which detectors are active.

## LLM payloads

```python
from pseudonymize import Policy, Pseudonymizer

engine = Pseudonymizer(
    key=b"a-32-byte-or-longer-secret-key...",
    namespace="customer-42",
    policy=Policy.llm(),
)
safe_payload = engine.process_data(
    {"messages": [{"role": "user", "content": "My email is maria@example.com"}]}
)
```

Dictionary keys, container types, and non-string primitive values remain unchanged.

## Security model

Tokens use HMAC-SHA256 over a versioned, domain-separated input and expose 80 pseudonym bits.
Keys must contain at least 32 bytes and should be supplied by a secret manager. Different tenants
should use different keys or namespaces. The library performs no network calls, background work,
logging, or runtime file writes.

Pseudonymize reduces exposure of personal and sensitive data. It does not guarantee detection of
all personal data and does not by itself establish GDPR compliance. Pseudonymised data can remain
personal data, and aliases remain linkable inside a namespace.

## Limitations

Rule detectors produce false positives and false negatives. This release does not recognize names
or natural-language addresses, protect a compromised host, or remove identifying context. Filter
logs, tracing, retrieved documents, tool inputs, and tool outputs as well as chat messages.

## Benchmarks

Benchmark commands and the required hardware-reporting template are in
[`benchmarks/README.md`](benchmarks/README.md). No performance claim is published until results are
recorded on named hardware.

## Optional NER roadmap

Version 0.2.0 is planned to add an optional local NER backend. The core only defines the backend
protocol and never downloads models or imports model runtimes.

The full local-first document and backend plan is in [`VISION.md`](VISION.md) and
[`ROADMAP.md`](ROADMAP.md).

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Privacy-impacting detector reports are welcome with
synthetic reproductions only.

## Licence

Apache-2.0. Model licences, if models are later supported, are evaluated separately.
