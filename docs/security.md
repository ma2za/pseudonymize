# Security

Deterministic aliases have the form `<TYPE:IDENTIFIER>` and derive their identifier from
HMAC-SHA256. The MAC input is separated by token format version, namespace, entity type, and
detector-specific normalized value. The key must contain at least 32 bytes and is excluded from
assigner representations.

Changing normalization changes aliases. Email domains are lowercased, IBANs compacted and
uppercased, cards reduced to digits, phone separators removed without inventing a country code,
and IP addresses canonicalized.

Numbered aliases are stable only inside one explicit processing scope. Reversible mappings are
disabled by default, omitted from result representations, and contain personal data when enabled.
