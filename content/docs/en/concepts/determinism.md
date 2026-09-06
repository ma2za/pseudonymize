---
title: "Determinism"
lastUpdated: "2026-09-06"
---

# Determinism

Pseudonymize.io uses **deterministic mapping** to ensure the same identifier becomes the same pseudonym, preserving data integrity for downstream models.

## How it works
By default, when `alias_format` is set to `hash`, we generate pseudonyms using `HMAC(secret, normalized_value)`. 

1. **Normalization:** The input `alice@example.com` and `Alice@Example.com` are both normalized to `alice@example.com`.
2. **Key ownership:** The `secret` is an ephemeral salt generated at the beginning of the Request scope. It is never stored.
3. **Hashing:** The normalized value is hashed. 
4. **Prefixing:** The hash is truncated and prepended with the entity type (e.g. `EMAIL_a1b2c3d4`).

## Security Properties
Because the secret salt is ephemeral (in Request scope) or strictly isolated to your project (in Project scope), attackers cannot pre-compute rainbow tables to guess the original values from the hashes. 

If you use the open-source engine locally, you are entirely responsible for the generation, rotation, and security of the salt used for deterministic generation.
