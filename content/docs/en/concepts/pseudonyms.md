---
title: "Pseudonyms"
lastUpdated: "2026-09-06"
---

# Pseudonyms

Pseudonymize.io replaces detected entities with deterministic alias strings called **pseudonyms**. 

## What it means
A pseudonym is a structured alias that retains the semantic type of the original entity but destroys the original sensitive information. 

**Example:**
```text
alice@example.com → EMAIL_01
bob@example.com   → EMAIL_02
```

## Why it exists
Generic redaction (like replacing all names with `[PERSON]`) destroys all relationships within a payload. Pseudonymization retains identity mapping so downstream systems (like LLMs or analytics engines) can group actions by the same entity without knowing who that entity is.

## Exact Behavior

* **Sequential mapping:** Within a single request scope, the first detected email becomes `EMAIL_01`, the second distinct email becomes `EMAIL_02`, and so on.
* **Type-specific:** Pseudonyms always carry a prefix indicating the entity type (e.g., `PERSON_`, `ORG_`, `EMAIL_`).
* **Stability:** Pseudonyms are strictly stable **within a single API request** (the default scope). See [Scopes](/docs/concepts/scopes) and [Determinism](/docs/concepts/determinism) for cross-request stability.
* **Collisions:** Due to deterministic HMacing (when enabled), collisions between distinct source identities are mathematically improbable.
* **Ordering leakage:** Sequential aliases (`_01`, `_02`) leak the order of appearance in a specific document. This is usually acceptable for LLM context, but can be disabled via policy if strict opacity is required.

## API Parameters
You can configure pseudonym format in your policy payload:
```json
{
  "policy": {
    "alias_format": "sequential" // or "hash"
  }
}
```
