---
title: "Supported Entities"
lastUpdated: "2026-09-06"
---

# Supported Entities

Pseudonymize.io uses a combination of ML models, pattern matching, and exact validators to detect sensitive data. Not all entity detection is equivalent; understanding the underlying detector helps you anticipate reliability.

## Capability Matrix

| Entity | Example | Detector | Deterministic | Reversible |
| :--- | :--- | :--- | :--- | :--- |
| **Email** | alice@example.com | pattern | yes | yes/no |
| **Phone** | +49 151 2345678 | pattern/library | yes | yes/no |
| **Person** | Alice Rossi | ML (NER) | yes | yes/no |
| **Location** | Munich | ML (NER) | yes | yes/no |
| **Organization** | Acme Corp | ML (NER) | yes | yes/no |
| **IP Address** | 192.168.1.1 | pattern | yes | yes/no |
| **IBAN** | DE89370400440532013000 | validator | yes | yes/no |
| **Payment Card** | 4532... | validator (Luhn) | yes | yes/no |

## Detector Types

1. **Pattern:** Extremely reliable Regex implementations. Expect near 100% precision and recall for properly formatted strings (like IP addresses).
2. **Validator:** Regex followed by an algorithmic validation check (e.g. Luhn algorithm for credit cards, checksums for IBANs). Prevents false positives on random 16-digit numbers.
3. **ML (NER):** Natural Language Processing models (Named Entity Recognition). Highly dependent on context. Precision and recall typically hover between 85% - 95%. Expect some false negatives if a name is completely isolated without surrounding grammatical context.

## Custom Entities
If your application uses proprietary identifiers (like internal `TK-XXXX` support ticket IDs), you can pass custom Regex patterns in the API payload under `custom_entities` (Coming in v1.2).
