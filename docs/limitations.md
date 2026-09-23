# Limitations

Pseudonymised values can remain personal data. Detectors have false positives and false negatives,
and undetected context can identify a person. Phone formats are deliberately conservative. Secret
patterns cannot cover every provider. Applications remain responsible for key management, access
control, retention, logging, incident response, and legal obligations.

JSON object keys are locations, not content blocks, and are not transformed. JSON, JSONL, and CSV
rendering preserves data semantics but not original whitespace, quoting, escapes, or record
endings. The built-in CSV adapter uses strict comma-separated `excel` rules and does not sniff
dialects.

CSV formulas are preserved as cell content. Pseudonymize does not evaluate or neutralize formulas,
so applications exporting files for spreadsheet software remain responsible for formula-injection
controls.

## Remote detection and payload sizing

Remote backends send complete configured content blocks over HTTPS to external endpoints.
Pseudonymize does not impose an arbitrary general payload size ceiling because provider constraints
vary widely; applications are responsible for sizing and bounding content blocks before remote
invocation, configuring transport timeouts, and verifying provider compliance.

