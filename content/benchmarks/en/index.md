---
title: "Detection Benchmarks"
lastUpdated: "2026-09-06"
---

# Detection Benchmarks

Security claims should be inspectable. We continuously test our open-source detection engine against standardized datasets to measure accuracy, precision, and recall. 

**Pseudonymization reduces exposure. It does not make data anonymous.**
For a privacy product, *recall* matters enormously because false negatives leak data to external APIs.

## Current Benchmark Results

* **Engine Version:** 1.0.0
* **Commit SHA:** `f8387dc`
* **Date:** September 6, 2026
* **Dataset:** Enron / Presidio standard sets (Synthetic & Real)
* **Sample size:** 10,000 sentences
* **Languages:** English, Italian

| Entity | Precision | Recall | F1 Score |
| :--- | :--- | :--- | :--- |
| **Email** | 0.99 | 0.99 | 0.99 |
| **Person** | 0.94 | 0.88 | 0.91 |
| **Location** | 0.91 | 0.85 | 0.88 |
| **Organization** | 0.90 | 0.82 | 0.86 |
| **Phone** | 0.98 | 0.95 | 0.96 |
| **IP Address** | 1.00 | 1.00 | 1.00 |

## Methodology

1. **Precision:** Out of all the entities the engine flagged as "Person", how many were actually people? (A low precision means high false positives, destroying useful non-sensitive text).
2. **Recall:** Out of all the actual people in the text, how many did the engine successfully flag? (A low recall means high false negatives, leaking sensitive data).
3. **F1 Score:** The harmonic mean of precision and recall.

## Reproduction
You can reproduce these benchmarks yourself using our open-source repository.

```bash
git clone https://github.com/ma2za/pseudonymize.io
cd pseudonymize
make benchmark
```
