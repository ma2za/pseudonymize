# Detectors

Bundled detectors cover email, phone, IP address, IBAN, payment card, URL credential, and secret
entities. Italian fiscal codes and VAT identifiers are also supported as `NATIONAL_ID` and
`TAX_ID`. Candidate extraction is followed by normalization and validation. IBANs require MOD-97,
cards require Luhn, Italian identifiers require their official check character or digit, and IP
candidates must parse with the standard library. An Italian VAT number without an `IT` prefix is
considered only next to an explicit VAT label to avoid treating arbitrary 11-digit values as tax
identifiers.

Contextual detection (`ContextualIdDetector`) provides data-driven, locale-scoped identification
for national IDs, tax IDs, postal codes, and account numbers across English, Spanish, French,
Italian, German, Vietnamese, Indonesian, and Chinese. Candidate values are scored through an
explainable bounded scoring model that incorporates token distance, explicit punctuation
separators, and negative context suppression (penalizing software versions, HTTP status codes,
network ports, and page numbers to prevent false-positive inflation).

Detector results contain type, offsets, confidence, and detector name. They never contain the raw
matched value. Custom thread-safe detectors can implement the `Detector` protocol.
