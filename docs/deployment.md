# Deployment

## Trust boundary

Run Pseudonymize inside the trusted application boundary, before provider SDK calls, queues,
tracing exporters, analytics, or persistent prompt caches. The dependency-free core performs no
network calls. Custom backends and adapters execute in-process and inherit the application's data
access, so review them as privileged code.

## Request lifecycle

1. Validate the accepted input size and structure.
2. Select an explicit policy for the workflow.
3. Create a request-scoped engine or alias scope.
4. Process every outbound field, including retrieval and tool data.
5. Send only transformed data across the boundary.
6. Keep safe reports separate from application logs unless their metadata is required.
7. Destroy request-scoped mappings and plaintext buffers as soon as the application permits.

## Keys and mappings

Pseudonymize is a stateless, in-memory transformation library. The package neither stores,
decrypts, rotates, encrypts, zeroizes, nor retains mappings in persistent storage or external
key-management systems.

When deterministic pseudonymization is configured, the calling application loads secret keys from
its secret manager and supplies them as raw bytes to the engine. Tenants should be separated with
distinct keys or namespaces. When `include_mapping=True` is explicitly requested, the reversible
mapping dictionary is returned directly to the caller. Callers and system operators are entirely
responsible for mapping lifecycle, external envelope encryption, access controls, and retention
outside this package. Note that standard Python runtimes cannot guarantee memory zeroization for
arbitrary immutable strings or dictionary allocations.

## Key rotation architectures (Application responsibility)

Key rotation is an operational concern managed by the calling application:

1. **Namespace versioning:** Applications can deploy dual keys using explicit namespaces (e.g.
   `namespace="v1"` and `namespace="v2"`). Inbound verification can accept both versions, while
   outbound pseudonymization signs with the active version (`v2`).
2. **Re-pseudonymization migrations:** When migrating persisted deterministic records, the calling
   service reads records under `v1`, resolves the entity, and re-pseudonymizes under `v2`.
3. **Revocation:** If a key compromise occurs, operators decommission the affected key version
   in their external secret manager and purge application-level caches.

## Mapping lifecycle & external storage (Application responsibility)

Reversible mappings (`include_mapping=True`) expose plaintext associations and must be handled
with strict operational care by the integrating service:

- **Ephemeral request scope:** Discard mapping dictionaries immediately when the request
  terminates. Avoid writing raw in-memory mappings to persistent disk or unencrypted caches.
- **Envelope encryption for persistence:** If regulatory or customer requirements require
  persisting mapping associations, the integrating application must encrypt the mapping payload
  with an external KMS envelope key before writing to storage.
- **Retention policies:** Define organization-specific retention windows after which persisted
  mapping records and ciphertext are purged according to data-governance requirements.

## Drift monitoring & safe telemetry

Callers can inspect the structured `Report` object returned by `process_with_report` or file
inspection APIs:

- Monitor detection counts, block counts, and warning codes (`ProcessingWarning`) in safe reports.
- Track distribution shifts across entity types to detect changes in incoming schema formats or
  adversarial evasion attempts.
- Safe reports expose matched entity types, character/record locations, and counts without
  exposing raw matched values.

## Incident response considerations (Operational guidance)

- **Suspected leakage:** If unredacted PII is suspected downstream, inspect safe report statistics
  and audit logs. Verify that output files carry `<stem>.safe<suffix>` and that `overwrite=True`
  was not abused to bypass file isolation.
- **Fail-closed pipeline design:** In an outage or unhandled exception scenario, applications
  must fail-closed rather than transmitting unredacted plaintext as a fallback.
- **Key revocation:** On confirmed compromise of a tenant key, decommission the key in the secret
  manager and invalidate active application session caches.

## Logging and failure handling

Log operation identifiers, statistics, warning codes, and backend names, not source payloads or
reversible mappings. Do not log arbitrary custom-backend exceptions before sanitizing them. Treat a
processing failure as fail-closed: do not send the original payload as a fallback.

## Remote backends

The optional `remote` extra supplies `HTTPRemoteBackend`. It sends the complete configured content
block and requested entity-type names to the caller-selected HTTPS endpoint. Use it only with both
backend consent and a matching `NetworkPolicy`; the default policy denies it. Redirects are not
followed, requests use a bounded timeout and retry count, and transport diagnostics are sanitized.
Pseudonymize does not enforce an arbitrary payload-size ceiling because provider constraints vary;
callers and applications are responsible for bounding content block sizes, selecting appropriate
transport timeouts, restricting network egress to the intended provider, choosing the smallest
processable blocks, and verifying that provider-side retries, logs, and diagnostics cannot retain
plaintext.

## Operational checklist

- Pin an exact release and verify the wheel provenance and digest.
- Run the installed-wheel smoke test in the deployment image.
- Keep outbound network access denied for local-only deployments.
- Test representative synthetic payloads and known detector limitations.
- Monitor safe counts and warning codes for unexpected shifts.
- Define incident response for leaked keys, mappings, or unsanitized payloads.
