---
title: "API Documentation"
lastUpdated: "2026-09-06"
---

# pseudonymize.io API

Welcome to the pseudonymize.io documentation. Put this API in the path of your sensitive data before it reaches external systems (like LLMs, analytics warehouses, or third-party support tools).

## Quickstart

Send a request to the Text API to pseudonymize prose.

```bash
curl -X POST https://api.pseudonymize.io/v1/text \
  -H "Authorization: Bearer pz_live_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Alice Rossi disputed invoice INV-204 from alice@example.com",
    "policy": "default"
  }'
```

**Response:**

```json
{
  "text": "PERSON_01 disputed invoice INV-204 from EMAIL_01",
  "entities": [
    { "type": "PERSON", "original": "Alice Rossi", "pseudonym": "PERSON_01" },
    { "type": "EMAIL", "original": "alice@example.com", "pseudonym": "EMAIL_01" }
  ]
}
```

## Authentication

All API requests must include your API key in the `Authorization` header.

```http
Authorization: Bearer pz_live_...
```

You can manage your API keys in the [Dashboard](/dashboard).

## Text API

`POST /v1/text`

Replaces identifiers inside prose without flattening the text around them.

### Request Body

* `text` (string, required): The text to process.
* `policy` (string, optional): The policy to use. Defaults to `"default"`.
* `detect` (array, optional): Specific entity types to detect.

```json
{
  "text": "Call me at +39 333 1234567.",
  "detect": ["PHONE"]
}
```

## Structured Data API

`POST /v1/data`

Pseudonymize identifier fields while keeping rows and schemas usable.

### Request Body

* `payload` (object | array, required): The JSON structure to process.
* `policy` (string, optional): The policy to use.

```json
{
  "payload": {
    "user": {
      "name": "Mario Rossi",
      "email": "mario@example.com"
    }
  }
}
```

## Pseudonyms & Deterministic Identity

Pseudonymize.io uses **deterministic identity preservation** within a single request. 
If "Alice" appears three times in the same document, she becomes `PERSON_01` all three times.
This allows LLMs to understand that it is the *same* person without knowing *who* it is.

## Errors & Limits

We use standard HTTP status codes.

* `200 OK`: Successful processing.
* `400 Bad Request`: Invalid payload format.
* `401 Unauthorized`: Missing or invalid API key.
* `429 Too Many Requests`: You have run out of credits.

## Supported Entities

* `PERSON` (Names)
* `ORGANIZATION` (Company names)
* `EMAIL` (Email addresses)
* `PHONE` (Phone numbers)
* `LOCATION` (Cities, addresses)
* `IP` (IPv4 and IPv6)
* `IBAN` (Bank accounts)
* `CARD` (Credit/Debit cards)

## Security

* **Zero-retention in-memory processing**: Your request and response payloads are processed entirely in memory.
* **No logging of payload data**: Application logs only contain request metadata (timestamp, latency, account ID). The payload and detected values are never written to disk.
* For more architecture details, see the [Security Architecture](/security).
