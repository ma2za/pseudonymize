# Threat model

## Assets and boundaries

Protected assets are plaintext input, deterministic keys, reversible mappings, and the association
between an alias and a person. The trusted boundary contains the host process, configured local
backends, and application-owned key storage. Provider APIs, telemetry, queues, traces, caches,
generated model output, and remote backends are outside that boundary.

## Attacker capabilities

The model assumes an attacker may read outbound provider requests, application logs, safe reports,
or stored pseudonymized data. They may know likely source values and submit chosen inputs. They do
not control the trusted host process, read process memory, steal keys, or replace installed code.

## Security goals

- Accidental structured PII exposure to hosted LLMs and logs
- Cross-request correlation controlled by namespace or key boundaries
- Dictionary attacks against unkeyed hashes
- Credentials in URLs, tool payloads, and nested structured data

Pseudonymize also aims to keep matched values out of reports, warnings, exceptions, CLI output, and
representations; require explicit dual consent before invoking remote-capable backends; and avoid
source overwrite or partial file publication.

## Failure modes

- False negatives leave source values unchanged.
- False positives transform non-sensitive values and may reduce utility.
- Numbered aliases can reveal equality and occurrence order inside a scope.
- Deterministic aliases can reveal equality across data processed with the same key and namespace.
- Surrounding context can re-identify a person after direct identifiers are transformed.
- Reversible mappings and custom adapter metadata can expose plaintext if applications retain or
  log them.
- Sanitizing only prompts misses retrieval, tool, cache, trace, and error boundaries.

Applications must fail closed when processing fails. Sending the original input as a fallback
defeats the boundary.

## Controls

- Use request-scoped numbered aliases unless cross-request correlation is required.
- Separate tenants with keys or namespaces and store keys outside application configuration.
- Keep reversible mappings disabled by default and apply encryption, access control, and retention
  when enabled.
- Process every outbound string-bearing structure and test known detector limitations.
- Keep the default network policy denied and restrict host egress for local-only deployments.
- Treat custom backends and adapters as privileged in-process code.

## Excluded

- A compromised host, stolen keys, side channels, or malicious same-process code
- Perfect detection, complete regulatory compliance, or contextual re-identification
- Natural-language names and addresses in the dependency-free release
- Protection after an application deliberately logs or transmits plaintext
