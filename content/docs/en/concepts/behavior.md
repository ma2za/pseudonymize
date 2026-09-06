---
title: "Behavior Under Uncertainty"
lastUpdated: "2026-09-06"
---

# Behavior Under Uncertainty

When building privacy infrastructure, silent ambiguity is dangerous. Pseudonymize.io fails closed and maintains strict payload contracts.

### What if nothing is detected?
The API returns your payload entirely unchanged with a `200 OK` status and an empty `entities` array.

### What if only some values are detected?
The API transforms the detected entities with pseudonyms, and returns the rest of the text/JSON exactly as it was. 

### What if the input is malformed JSON?
The API immediately drops the payload and returns a `400 Bad Request`.

### What if the processing exceeds your credit limits?
The API immediately drops the payload and returns `429 Too Many Requests`.

### What if the ML detector is uncertain?
Named Entity Recognition (NER) models use probability thresholds.
* By default, we use a strict confidence threshold (typically `0.85+`) to avoid destroying non-sensitive text (false positives).
* We prioritize maintaining the integrity of your prompts/data. 
* **Important:** This means a highly ambiguous word (e.g. "May went to Paris." where "May" could be a month or a person) might result in a false negative (the name is not redacted). You must account for this in highly regulated environments.
