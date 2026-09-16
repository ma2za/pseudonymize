# Private Release Plan: Pseudonymize

## Current State
- **Just Completed:** `1.20.2` (Fixing CI DAWG tests, fully eradicating `llama-cpp-python` dependency).
- **Current Baseline (1.20.0):** 
  - Precision: `0.8587`
  - Recall: `0.8016`
  - F1 Score: `0.8292`
  *(Measured against `ai4privacy/pii-masking-openpii-1.5m` validation split, 1000 samples).*

## Immediate Next Milestone: `1.21.0` (Scale & Integration)

The upcoming releases will focus on expanding integration capabilities, observability, and advanced recall improvements without sacrificing the strict performance boundaries.

### Schema-Preserving Agent Sanitation (MCP Integration)
- **Use Case:** Safely interacting with LLM agents.
- **Focus:** Redacting JSON-RPC and MCP tool call payloads natively without breaking structural schemas required by models.

### OpenTelemetry Integration
- **Use Case:** In-process observability.
- **Focus:** A dedicated middleware adapter to redact application logs and trace spans securely before export.

### Advanced Local ML (GLiNER2 ONNX)
- **Use Case:** Next-generation semantic recall.
- **Focus:** Integrate prompt-based NER models natively within the ONNX local boundary to dynamically capture domain-specific jargon (e.g. "Project Codename X").

### Regional EU Identifier Depth
- **Use Case:** European enterprise compliance.
- **Focus:** Deepening coverage with mathematically verified checksums and topological parsers for French, German, Italian, and Spanish national systems.

## Performance & Detection Quality Horizon (Ongoing)

To continually improve precision and recall without introducing hardcoded or brittle regex artifacts, the following generalizable architectural improvements are slated for upcoming releases:

1. **Dynamic Entity-Specific Thresholds (ML)**: Instead of a flat `entity_threshold` across all labels, allow per-entity calibration. For example, lower activation thresholds for `LOCATION` (which historically suffers from low recall but high precision) while keeping `PERSON` strictly bounded.
2. **Context-Assisted ML Boosting**: Integrate the `ContextDetector` into the ML loop. If a token falls within 30 characters of a context trigger ("Name:", "Address:"), dynamically boost the ML logits for that specific text window, resolving the "missed isolated entities" problem.
3. **Span-Level Subword Repair (Token-Merge Averaging)**: DistilBERT uses WordPiece. If the tokenizer splits a name into subwords and assigns conflicting probabilities across them (e.g., dropping a middle subword), implement a CRF-style continuation heuristic to coerce adjacent subwords into a unified entity unless separated by a hard boundary.
4. **Ensemble Voting Arbitrator**: When multiple backends run simultaneously, introduce an `EnsembleArbitrator` allowing modes like `HighRecall` (Union), `HighPrecision` (Intersection - requires at least two backends to agree), or `Two-Pass` (Regex proposes, ML verifies).
5. **Cross-Lingual Zero-Shot Backend (GLiNER)**: Introduce an optional backend using GLiNER (Generalist Model for NER). GLiNER uses prompt-based label injection natively supporting 20+ languages out of the box, allowing dynamic detection of arbitrary entities ("Internal Project Code") with a fundamentally higher recall ceiling than traditional BERT models.

## Future Exploration & Open Proposals

The following architectural and visionary proposals are under consideration for the long-term future:

- **#34 Vision proposal: worldwide language and locale coverage**
- **#35 Vision proposal: maintained structured registry of privacy regulations per jurisdiction**
- **#36 Architecture and scalability review: current limits and proposed solutions**
- **#66 Proposal: training-corpus de-identification mode with erasure-by-key (crypto-shredding)**
- **#70 Proposal: residual re-identification risk report (the honest dual of detection)**
- **#71 Proposal: processing receipts (signed, value-free provenance manifests)**
- **#73 Proposal: pseudonym interchange spec with cross-language test vectors**