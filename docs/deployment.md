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

Load deterministic keys from the deployment's secret manager and pass bytes directly to the
process. Separate tenants with different keys or namespaces, rotate keys under an application-level
version, and never log keys. Reversible mappings contain the original values. Keep them disabled
unless restoration is required, then encrypt them, restrict access, and apply a short retention
period outside this package.

## Logging and failure handling

Log operation identifiers, statistics, warning codes, and backend names, not source payloads or
reversible mappings. Do not log arbitrary custom-backend exceptions before sanitizing them. Treat a
processing failure as fail-closed: do not send the original payload as a fallback.

## Remote backends

The base package ships no remote backend. If an application supplies one, enable it only with both
backend consent and a matching `NetworkPolicy`. Restrict network egress to the intended provider,
set bounded timeouts outside the core, and verify that retries and provider SDK diagnostics cannot
record plaintext.

## Operational checklist

- Pin an exact release and verify the wheel provenance and digest.
- Run the installed-wheel smoke test in the deployment image.
- Keep outbound network access denied for local-only deployments.
- Test representative synthetic payloads and known detector limitations.
- Monitor safe counts and warning codes for unexpected shifts.
- Define incident response for leaked keys, mappings, or unsanitized payloads.
