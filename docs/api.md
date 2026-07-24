# API

::: pseudonymize

::: pseudonymize.policy.Policy

::: pseudonymize.engine.Pseudonymizer

::: pseudonymize.document.Document

::: pseudonymize.document.ContentBlock

::: pseudonymize.processing.ProcessingResult

::: pseudonymize.processing.DetectionReport

::: pseudonymize.backends.base.DetectionBackend

::: pseudonymize.adapters.InputAdapter

::: pseudonymize.adapters.OutputAdapter

::: pseudonymize.formats.FileFormat

## Transformation modes

`TransformationMode.NUMBERED` is the default. `GENERIC` keeps only the entity type,
`DETERMINISTIC` requires a key and namespace, and `REDACTED` produces `[REDACTED]` or an explicitly
requested typed form.

`Pseudonymizer.new_scope()` creates an explicit reusable alias session. `process_data()` uses one
scope across the complete nested payload. Person, organization, and location aliases require an
optional detection backend.

Detailed methods return `ProcessingResult[T]`: `process_with_report`,
`process_data_with_report`, `process_document`, `inspect_document`, `process_file`, and
`inspect_file`.

`process_file()` and `inspect_file()` select TXT, Markdown, log, JSON, JSONL, or CSV handling from
an explicit `FileFormat` or a recognized suffix. Unknown formats are rejected without content
guessing. Custom adapters remain available through keyword-only `input_adapter` and
`output_adapter` arguments.
