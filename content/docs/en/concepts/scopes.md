---
title: "Scopes"
lastUpdated: "2026-09-06"
---

# Scopes

A scope determines where identical source values resolve to identical pseudonyms.

## Why it exists
Different architectural use cases have different requirements for identity persistence. An LLM summarizing a single ticket only needs identity consistency within that one ticket. An analytics warehouse tracking customer churn over a year needs identity consistency across millions of events spanning months.

## Exact Behavior

### `scope = request` (Default)
Identities are consistent only within a single HTTP API call. Memory mappings are destroyed immediately after the response is returned.

```text
Request A
Alice → PERSON_01

Request B
Alice → PERSON_01? NO (Could be PERSON_01, PERSON_03, etc., depending on appearance order in Request B)
```

### `scope = project` (Coming soon)
Identities remain stable indefinitely across all requests made using API keys belonging to the same project. This relies on stable [Deterministic keys](/docs/concepts/determinism) tied to your project configuration.

```text
Request A
Alice → PERSON_7CX2

Request B (Next day)
Alice → PERSON_7CX2
```

## API Parameters
```json
{
  "policy": {
    "scope": "request" // default
  }
}
```