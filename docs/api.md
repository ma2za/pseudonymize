# API

::: pseudonymize

::: pseudonymize.policy.Policy

::: pseudonymize.engine.Pseudonymizer

## Transformation modes

`TransformationMode.NUMBERED` is the default. `GENERIC` keeps only the entity type,
`DETERMINISTIC` requires a key and namespace, and `REDACTED` produces `[REDACTED]` or an explicitly
requested typed form.

`Pseudonymizer.new_scope()` creates an explicit reusable alias session. `process_data()` uses one
scope across the complete nested payload. Person, organization, and location aliases require an
optional detection backend.
