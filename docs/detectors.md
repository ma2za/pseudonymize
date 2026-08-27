# Detectors

Bundled detectors cover email, phone, IP address, IBAN, payment card, URL credential, and secret
entities. Italian fiscal codes and VAT identifiers are also supported as `NATIONAL_ID` and
`TAX_ID`. Candidate extraction is followed by normalization and validation. IBANs require MOD-97,
cards require Luhn, Italian identifiers require their official check character or digit, and IP
candidates must parse with the standard library. An Italian VAT number without an `IT` prefix is
considered only next to an explicit VAT label to avoid treating arbitrary 11-digit values as tax
identifiers.

Detector results contain type, offsets, confidence, and detector name. They never contain the raw
matched value. Custom thread-safe detectors can implement the `Detector` protocol.
