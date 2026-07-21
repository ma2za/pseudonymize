# Threat model

## Protected

- Accidental structured PII exposure to hosted LLMs and logs
- Cross-request correlation controlled by namespace or key boundaries
- Dictionary attacks against unkeyed hashes
- Credentials in URLs, tool payloads, and nested structured data

## Excluded

- A compromised host, stolen keys, side channels, or malicious same-process code
- Perfect detection, complete regulatory compliance, or contextual re-identification
- Natural-language names and addresses in the dependency-free release
