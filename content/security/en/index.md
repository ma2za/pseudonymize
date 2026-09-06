---
title: "Security Architecture"
lastUpdated: "2026-09-06"
---

# Security Architecture

Security claims should be inspectable. This page documents how pseudonymize.io handles data and infrastructure. 

## Request Architecture

```text
                 ┌─────────────────────┐
Request ─TLS──→  │ pseudonymize.io API │
                 │                     │
                 │ Detect              │
                 │ Transform           │
                 │ Return              │
                 └─────────┬───────────┘
                           │
                           X
                    payload storage
```

### Logging

Application logs contain **metadata only**: request ID, latency, status code, payload size, account ID.
Application logs **never contain** request or response bodies, nor detected values.

## Payload Lifecycle

1. Request enters the server.
2. HTTPS terminates at the application boundary.
3. The JSON body enters application memory.
4. The open-source detector engine processes it.
5. The transformed response is created.
6. The response is returned to the client.
7. Memory references are immediately released.
8. No payload data is ever stored to disk or transmitted to a subprocessor.

## Infrastructure

* **Hosting:** Hetzner
* **Location:** Germany / EU
* **Application deployment:** Self-managed containers
* **Database:** PostgreSQL (Stores: accounts, API keys metadata, billing metadata. **Does not store: API payloads.**)

## Threat Model

**Pseudonymization reduces exposure. It does not make data anonymous.**

Detection systems can produce false negatives. You remain responsible for determining whether transformed data is appropriate for your downstream use. Our service is designed to mitigate the accidental leakage of known PII structures into external APIs, not to defeat targeted deanonymization attacks by state actors.

## Detection Quality

Benchmarks are run against standardized datasets and published openly.

* **Benchmark dataset:** Enron / Presidio standard sets
* **Version:** 1.0.0
* **Sample size:** 10,000 sentences
* **Precision:** 0.94
* **Recall:** 0.88
* **F1 Score:** 0.91

For complete raw results, see our [open source repository](https://github.com/ma2za/pseudonymize).
