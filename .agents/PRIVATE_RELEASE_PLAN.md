# Private Release Plan: Pseudonymize

## Current State
- **Just Completed:** `0.27.0` (Local Microservice DLP Endpoint)
- **Current Baseline (1.0.0 - Strict Match Rules):** 
  - Precision: `0.9410`
  - Recall: `0.5356`
  - F1 Score: `0.6826`
  *(Measured against `ai4privacy/pii-masking-openpii-1.5m` validation split, strict rules).*

## Immediate Next Milestone: `1.1.0` to `1.10.0`
**Focus:** Benchmark Recovery Pipeline

The next 10 releases are singularly focused on improving the F1 score back to >0.90 under the strict evaluation rules:
- **1.1.0:** Token-to-Character Alignment Optimization
- **1.2.0:** NLP-Driven Context Detectors
- **1.3.0:** Entity-Specific Confidence Calibration
- **1.4.0:** Secondary NER Ensembling
- **1.5.0:** Advanced Punctuation Boundary Rules
- **1.6.0:** Local Location & Address Parsing
- **1.7.0:** Attention-Mask Context Boosting
- **1.8.0:** Adaptive Windowing for Long Entities
- **1.9.0:** Multi-Pass Boundary Refinement
- **1.10.0:** The Strict 90% Benchmark Gate

### Instructions to resume
1. Start by investigating the fast tokenizer alignment offsets for 1.1.0.
2. Develop robust boundary trim heuristics on the 	rain split exclusively.