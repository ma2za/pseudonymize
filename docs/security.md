# Security

Aliases have the form `<PZ1:TYPE:BASE32>` and carry 80 bits from HMAC-SHA256. The MAC input is
separated by format version, namespace, entity type, and detector-specific normalized value. The
key must contain at least 32 bytes and is excluded from transformer representations.

Changing normalization changes aliases. Email domains are lowercased, IBANs compacted and
uppercased, cards reduced to digits, phone separators removed without inventing a country code,
and IP addresses canonicalized.
