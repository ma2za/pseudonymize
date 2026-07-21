# Detectors

Bundled detectors cover email, phone, IP address, IBAN, payment card, URL credential, and secret
entities. Candidate extraction is followed by normalization and validation. IBANs require MOD-97,
cards require Luhn, and IP candidates must parse with the standard library.

Detector results contain type, offsets, confidence, and detector name. They never contain the raw
matched value. Custom thread-safe detectors can implement the `Detector` protocol.
