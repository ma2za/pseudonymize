# Private Release Plan: Pseudonymize

## Current State
- **Just Completed:** `1.20.2` (Fixing CI DAWG tests, fully eradicating `llama-cpp-python` dependency).
- **Current Baseline (1.20.0):** 
  - Precision: `0.8587`
  - Recall: `0.8016`
  - F1 Score: `0.8292`
  *(Measured against `ai4privacy/pii-masking-openpii-1.5m` validation split, 1000 samples).*

## Strategic Imperative: High-Throughput & Semantic Depth
Following the stabilization of our 0.8292 F1 baseline, the roadmap must now aggressively prioritize **Performance, Memory Efficiency, and CPU-level optimizations** alongside our recall improvements. We cannot afford latency regressions as we introduce heavier semantic models (GLiNER). The architecture must transition to batched, zero-copy, and highly optimized pipelines.

---

### `1.21.0`: The Performance & Core Algorithmic Release
**Focus:** Eradicating memory bottlenecks, maximizing ONNX CPU saturation, and extracting "free" recall from algorithmic repairs.

- **ONNX Inference Batching & Vectorization (NEW):** Refactor the `DetectionBackend` interface to support dynamic batching. Shift from sequential tokenization to padded batch inference to saturate CPU vector lanes (AVX2/AVX512), targeting a 4x throughput increase (>5000 docs/sec).
- **Zero-Copy & LRU Caching Fast-Paths (NEW):** Implement L1/L2 caching for frequent tokens (e.g., common nouns, repeated names) to bypass the ML inference loop entirely. Reduce string allocation overhead during payload reassembly.
- **Span-Level Subword Repair (Token-Merge Averaging):** Address DistilBERT WordPiece fragmentation. Implement a CRF-style continuation heuristic to coerce adjacent split subwords into a unified entity, fixing broken names without adding new neural layers.
- **Dynamic Entity-Specific Thresholds (ML):** Calibrate activation thresholds per entity via logit tuning. Drop confidence requirements for `LOCATION` (traditionally low recall, high precision) while keeping `PERSON` strictly bounded, optimizing the F1 curve mathematically.

---

### `1.22.0`: Next-Generation Semantic Recall
**Focus:** Integrating state-of-the-art zero-shot NER architectures (GLiNER) within our strict local, offline boundaries.

- **Advanced Local ML (GLiNER2 ONNX):** Integrate prompt-based NER models natively within the ONNX local boundary. Crucial for dynamically capturing domain-specific jargon (e.g., "Project Codename X") without fine-tuning. Must run under tight latency budgets.
- **Cross-Lingual Zero-Shot Capabilities:** Leverage GLiNER's inherent multi-lingual support (20+ languages) to scale beyond English-centric BERT variants, fundamentally raising our recall ceiling.
- **Context-Assisted ML Boosting:** Integrate the `ContextDetector` tightly with the ML loop. If a token falls within 30 characters of a hard trigger ("Address:", "Name:"), dynamically boost the model's logits for that specific text window to recover missed isolated entities.
- **Ensemble Voting Arbitrator:** With multiple backends (RegEx, BERT, GLiNER) running, introduce an `EnsembleArbitrator`. Support topological modes: `HighRecall` (Union), `HighPrecision` (Intersection), or `Two-Pass` (Heuristics propose, ML verifies).

---

### `1.23.0`: Ecosystem Integration & Structural Depth
**Focus:** Securely bridging the gap between local privacy and complex nested/agentic environments.

- **Schema-Preserving Agent Sanitation (MCP Integration):** Redact JSON-RPC and MCP tool call payloads natively using structural AST traversal. Must guarantee that redaction never breaks the strict JSON schemas required by LLM agent logic.
- **Zero-Overhead OpenTelemetry Integration:** A dedicated middleware adapter for redacting application logs and trace spans. Must operate entirely asynchronously with <1ms overhead on the hot path.
- **Regional EU Identifier Depth:** Expand algorithmic coverage with mathematically verified checksums and topological FSMs for French, German, Italian, and Spanish national systems (NIS, SSN, VAT).

---

## Future Explorations & Architectural R&D
Long-term proposals remain actively tracked for architectural validation and scalability bounds:

- **#36 Architecture and scalability review:** Investigating Rust/Cython extensions for the core Regex/DAWG scanning loop to achieve 10x throughput on heavy gigabyte-scale logs.
- **#34 Vision proposal:** Worldwide language and locale coverage via systematic dataset generation.
- **#35 Vision proposal:** Maintained structured registry of privacy regulations per jurisdiction.
- **#66 Proposal:** Training-corpus de-identification mode with erasure-by-key (crypto-shredding).
- **#70 Proposal:** Residual re-identification risk report (the honest dual of detection).
- **#71 Proposal:** Processing receipts (signed, value-free provenance manifests) to cryptographically prove a payload was sanitized.
- **#73 Proposal:** Pseudonym interchange spec with cross-language test vectors.
