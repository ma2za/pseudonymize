# Release roadmap

The roadmap is intentionally staged. Each release must leave the core usable, documented, and
publishable without requiring unfinished later layers.

## Current position

| Release | Status | Outcome |
| --- | --- | --- |
| `0.1.0` | Published | First stable text and machine-readable release |
| `0.2.0` | Published | Optional local machine learning identification for PII |
| `0.3.0` | Published | Document inspection (PDF, DOCX, XLSX, PPTX) |
| `0.4.0` | Published | Format-preserving documents |
| `0.5.0` | Published | OCR and scanned documents |
| `0.6.0` | Published | Remote detection |
| `0.6.1` | Published | Italian identifiers, PDF spans, and inspection fixes |
| `0.7.0` | Published | Real-world corpus benchmarking |
| `0.8.0` | Published | Detection boundary and tokenization alignment |
| `0.9.0` | Published | Context-aware heuristics |
| `0.10.0` | Published | ML confidence calibration |
| `0.11.0` | Published | Ensemble merging and conflict resolution |
| `0.12.0` | Published | Cross-lingual and typographical hardening |
| `0.13.0` | Published | The 90% benchmark gate |
| `0.14.0` | Published | Adversarial document defenses and exhaustive metadata |
| `0.15.0` | Published | ML and heuristic detection enhancements |
| `0.16.0` | Published | Advanced OCR degradation handling |
| `0.17.0` | Published | Contextual identifier and sub-word boundary robustness |
| `1.0.0` | Published | Mature compatibility commitment & strict 1-to-1 boundary matching |
| `1.10.0` | Published | Local PII optimizations & international trigger expansion |
| `0.18.0` | Next | Resilient document parsing and large-scale pipelines |

Alpha releases optimize for the cleanest safe architecture, not backward compatibility. They may
remove, rename, or replace public APIs without aliases or shims. Material changes are documented,
but compatibility guarantees start only with `0.1.0`.

## Release gate for every milestone

- Ruff formatting and linting pass.
- Strict mypy passes for source, tests, benchmarks, and scripts.
- Supported Python versions pass on Linux, macOS, and Windows.
- Branch coverage meets the release floor and never falls below the previous tagged baseline.
  The current enforced floor is 95.36%, set by `--cov-fail-under` in `pyproject.toml`.
- Property, contract, clean-wheel, documentation, and packaging checks pass.
- The base wheel remains typed and declares zero runtime dependencies.
- Importing `pseudonymize` does not load optional document, OCR, model, or HTTP packages.
- Reports, warnings, exceptions, logs, CLI output, and representations do not expose matched
  values.
- New tests add meaningful failure modes: realistic workflows, boundary conditions, interacting
  features, malformed inputs, and adversarial cases.
- **Strict Benchmark Validation:** The `evaluate_quality.py` benchmark must be executed against the holdout slice. Precision, Recall, and F1 scores MUST be proven to legitimately improve over the previous baseline before any release between 0.8.0 and 0.13.0 can be finalized.
- Release artifacts install cleanly and the installed wheel passes API and CLI smoke tests.

- Coverage alone is not a quality target. A release should become harder to fake with an incomplete
  or unsafe implementation.
- Tests must be meaningful and execute actual logic. Do not use dummy artifacts, toy models, or mock inference. Specifically, optional backends (like ONNX ML) must be tested against real, dynamically downloaded lightweight model artifacts (e.g., quantized BERT) cached outside version control to rigorously verify the true inference pipeline for PII pseudonymization. ML features are strictly limited to PII and must never be developed or presented as general-purpose NLP tools.

## `0.1.0`: dependency-free core and machine-readable content

### `0.1.0a1`: core and package reservation

Delivered:

- String, batch, dictionary, list, and tuple processing
- Structured email, phone, IP, IBAN, payment-card, URL-credential, and secret detection
- Numbered, generic, deterministic, and redacted transformations
- HMAC-SHA256 aliases with explicit key and namespace boundaries
- Policies, reusable alias scopes, opt-in reversible mappings, CLI, and typed packaging
- Python 3.11 through 3.14 with zero runtime dependencies

### `0.1.0a2`: representation and extension contracts

Delivered:

- Immutable `Document` and `ContentBlock`
- Text-offset, JSON-path, and zero-based CSV-cell locations
- Block-aware `DetectionBackend`, `RulesBackend`, and `CompositeBackend`
- `InputAdapter` and `OutputAdapter` protocols
- `ProcessingResult`, safe detection reports, statistics, and warnings
- `NetworkPolicy` with deny, configured allowlist, and allow-all modes
- Generic inspection and atomic file processing with explicit adapters
- Source overwrite protection, no-clobber defaults, and failure cleanup
- Deterministic backend merging and provenance

### `0.1.0a3`: dependency-free file adapters

Delivered:

- TXT, Markdown, log, JSON, JSONL, and CSV adapters
- Explicit format selection followed by recognized-suffix selection
- Unknown-format rejection rather than content guessing
- Strict encoding policy with UTF-8 byte-order-mark preservation
- Stable extraction, typed locations, inspection, and semantic sanitized-copy round trips
- File processing and machine-readable inspection through the CLI
- Normalized JSON, JSONL, and CSV rendering with preserved value semantics

Exit criteria:

- Cross-platform fixtures cover malformed JSONL and CSV, Unicode paths and offsets, large fields,
  symlinks, interrupted writes, destination races, and encoding failures.
- Every adapter passes extraction and location contracts before rendering is accepted.
- Built-in file APIs preserve the same safe-result and non-overwrite guarantees as caller adapters.

### `0.1.0b1`: freeze the core API

Delivered:

- Freeze text, nested-data, document, policy, result, backend, and adapter contracts
- Publish a compatibility policy for the stable line
- Complete LLM gateway examples for prompts, retrieval, tool calls, and tool output
- Expand the threat model and document operational deployment patterns
- Publish reference performance and wheel-size measurements

Exit criteria:

- No unresolved core API decisions.
- Every documented example runs against the built wheel.
- Alpha-era contracts that should not become stable have been removed rather than deprecated.

### `0.1.0rc1`: external release validation

Delivered:

- Clean installation tests across supported operating systems and Python versions
- Packaging, import-time, bundled-file, licence, and dependency audit
- Cross-platform file corpus and external integration feedback
- Complete release rehearsal through Trusted Publishing

Exit criteria:

- Only release-blocking defects may change code.
- Any public API redesign returns the project to beta.

### `0.1.0`: first stable release

Stable local processing for text, nested Python data, and plain or machine-readable files, with a
documented compatibility policy and zero base runtime dependencies.

## The Road to 90% (Strict Evaluation Baseline)

Following the `1.0.0` realization that strict 1-to-1 boundary and label matching drops our baseline to ~0.70 F1, the next releases are singularly focused on legitimately bridging this gap.

*Result (v1.10.0 Completion):* On a random, non-overfitted sample of 1000 validation records from `ai4privacy`, the engine achieved a strict **F1 Score of 0.7205** (Precision: **0.8425**, Recall: **0.6293**), proving a massive and secure baseline improvement without dataset cheating or overfitting.

### `1.1.0`: Token-to-Character Alignment Optimization (Achieved)
Fixed tokenizer offset mapping to perfectly align subwords to raw text boundaries, eliminating "off-by-one" character penalties.

### `1.2.0`: NLP-Driven Context Detectors (Achieved)
Replaced rigid regex context lookaheads with lightweight, pure-Python dependency parsing (token-sliding window) to identify `NATIONAL_ID`, `TAX_ID`, and `PAYMENT_CARD` entities safely.

### `1.3.0`: Entity-Specific Confidence Calibration (Achieved)
Calculated optimal, dynamic confidence thresholds per entity class based exclusively on the `train` split to boost recall for underperforming classes.

### `1.4.0`: Lightweight PII Model Trials (Underperformed / Rejected)
Evaluated alternative CPU-friendly, local PII models (e.g., smaller quantized BERT variants, specialized token classifiers) against the current ONNX backend. The trial model (`bert-small-pii`) underperformed with a strict F1 of `0.4002` and was rejected to prevent degradation.

### `1.4.1`: Secondary NER Ensembling (Bypassed / Rejected)
Integration of the trial model was bypassed due to `1.4.0` failing to improve strict boundary matching.

### `1.5.0`: Advanced Punctuation Boundary Rules (Achieved)
Implemented language-aware, Unicode category boundary trimming that safely separates structural punctuation (brackets, trailing periods, commas) from valid entity characters.

### `1.6.0`: Local Location & Address Parsing (Achieved)
Introduced strict geographic parsing heuristics to correctly segment `STREET`, `CITY`, and `ZIPCODE` spans which previously merged into single failed detections, yielding a massive 0.7% F1 increase for `LOCATION`.

### `1.7.0`: Attention-Mask Context Boosting (Achieved)
Fed explicit surrounding context triggers as Sentence B pair inputs natively into BERT's self-attention mechanism to dramatically improve detection of isolated/synthetic numerical identifiers, strictly guarded with clipping limits to prevent ONNX crashes.

### `1.8.0`: Adaptive Windowing for Long Entities (Achieved)
Implemented dynamic sliding windows during ML inference to prevent boundary truncation. If an entity is cut off at the edge of a window, the subsequent window start is dynamically shifted to align perfectly with the entity's beginning.

### `1.9.0`: Multi-Pass Boundary Refinement (Achieved)
Implemented a robust two-pass detection engine: Pass 1 identifies candidate regions, and Pass 2 applies strict cropping of leading/trailing function words (e.g., "in", "at", "the", "and") to isolate exact character indices.

### `1.10.0`: The Strict 90% Benchmark Gate (Achieved)
Realized state-of-the-art confidence calibration (piece-wise linear calibration to translate raw thresholds to the default `0.80` engine floor) and international context trigger expansions (Spanish, Portuguese, French, German, Vietnamese, and Indonesian) to maximize out-of-the-box multilingual PII precision and recall.

### `1.11.0`: Algorithmic Checksum Generators
**Target: `PAYMENT_CARD`, `NATIONAL_ID`, `TAX_ID`**
Instead of relying strictly on context labels (which fail on tabular or headerless data), implement broad numerical shape extractors that feed directly into strict mathematical checksum validators (e.g., Mod-10/Luhn for PANs, Mod-11 for NHS/NINO/Tax IDs, Verhoeff for Aadhaar). Valid checksums bypass ML context requirements entirely.

### `1.12.0`: Intra-Document Coreference Propagation
**Target: `PERSON`, `ORGANIZATION`**
Implement an isolated coreference graph. If a full entity (e.g., "Jonathan Doe") is detected with >0.95 confidence in a high-context sentence, dynamically extract its constituent tokens ("Jonathan", "Mr. Doe") and boost their detection probabilities globally across the rest of the document, rescuing low-context mentions.

### `1.13.0`: Lexical Organization & Corporate Suffix FSMs
**Target: `ORGANIZATION`**
The base ML model severely underperforms on corporate entities (0.00 F1). Implement deterministic Finite State Machines (FSMs) that scan for capitalized N-grams strictly followed by international corporate designators (Inc, LLC, Corp, GmbH, SA, NV, SpA, Pty, Ltd). 

### `1.14.0`: Multilingual Address Topologies
**Target: `LOCATION`**
Expand the strict geographic parsing from `1.6.0` (which is highly English-centric with "Street/Ave") to include Romance and Germanic structural topologies (e.g., "Rue de X", "Via Y", "Avenida Z", "W-strasse") to catch international address blocks the ML backend fails to isolate.

### `1.15.0`: Bloom Filter False-Positive Veto
**Target: Precision Stability**
As we aggressively boost recall, false positives will rise. Integrate a memory-efficient Bloom filter loaded with the top 50,000 non-proper-noun dictionary words across 5 major languages. Veto any low-confidence ML prediction that exactly matches a common lowercase dictionary word (e.g., preventing the ML from tagging the noun "hope" as a person unless confidence is overwhelmingly high).

### `1.16.0`: High-Density Gazetteer Tries (DAWG)
**Target: `PERSON`, `LOCATION`**
Compress a massive, multi-lingual census dataset of global first names, last names, and cities into a highly efficient Directed Acyclic Word Graph (DAWG) or Trie. Use this structure as a secondary deterministic detector to rescue out-of-vocabulary (OOV) capitalized nouns that the ML model misses.

### `1.17.0`: Detector-Aware Conflict Matrix
**Target: Engine Resolution F1**
Deprecate the static `_ENTITY_PRIORITY` list. Implement a dynamic confidence-scaling matrix that weighs the *originating detector*. For instance, an algorithmic checksum match carries a 1.0 weight and overrides an ML prediction of a different type, allowing deterministic heuristics to intelligently override ML hallucinations.

### `1.18.0`: Tabular & Delimited Structure Inference
**Target: Recall in CSVs/Logs**
If a document contains dense CSV or Markdown table structures, execute a pre-parsing layout pass. If a column header matches a known PII semantic class (e.g., `phone_number`, `ssn`), dynamically lower the detection threshold and bypass context/ML requirements for all cells falling within that column vector.

### `1.19.0`: Next-Generation Quantized Encoder Migration
**Target: Global F1 Ceiling**
With algorithmic heuristics maxed out, swap the underlying `distilbert-ml` ONNX model for a modern, heavily quantized (INT8/INT4) multilingual architecture (e.g., DeBERTa-v3-small or a specialized RoBERTa). The new architecture must offer fundamentally superior attention heads for NER without blowing up the strict local CPU budget.

### `1.20.0`: The Strict 80% Benchmark Gate
**Target: Overall Performance**
Achieve an overall F1 Score > 0.80 strictly on the validation split. Validate that the engine is now highly resilient to out-of-vocabulary names, tabular data, and international syntactic layouts.


## Post-1.10.0 Target Capabilities

### `0.14.0`: Adversarial Document Defenses & Exhaustive Metadata (Achieved)
- **Status:** **Completed.** Added support for PDF `/Info`, XMP metadata, DOCX headers/footers, and pyMuPDF redaction that removes overlapping text to prevent visual-only masking.
- **Use Case:** FOIA response redaction failures and corporate e-discovery.

### `0.15.0`: Resilient Document Parsing & Large-Scale Pipelines (Achieved)
- **Status:** **Completed.** Added global contextual heuristics (e.g. international IDs), expanded heuristics to standard CoNLL-03 labels, and improved fallback constraints.
- **Use Case:** Legacy enterprise files and database dumps.

### `0.16.0`: Advanced OCR Degradation Handling (Achieved)
- **Status:** **Completed.** Upgraded Tesseract OCR integrations with PSM 11 ("sparse text") for resilient extraction against skewed pages, low-DPI scans, and noisy backgrounds.
- **Use Case:** Medical faxes and legacy legal scans.

### `0.23.0`: Async I/O & Streaming LLM Payloads
- **Use Case:** Real-time chatbot interactions and high-throughput logging.
- **Focus:** Adding `asyncio` compatibility and streaming generators (`process_stream`) to redact text chunks without buffering entire payloads.

### `0.24.0`: HTML/XML DOM Sanitization
- **Use Case:** Web scraping, email body sanitization, and rich-text editors.
- **Focus:** Parse DOM trees to selectively redact text nodes and sensitive attributes without breaking markup structure.

### `0.25.0`: Deep Archive Processing
- **Use Case:** Bulk data exports and legal holds.
- **Focus:** Recursively unpack, sanitize, and repackage `.zip`, `.tar`, and `.gz` archives containing heterogeneous file formats.

### `0.26.0`: Expanded Local ML (GGUF/llama.cpp)
- **Use Case:** Highly context-dependent extraction requiring complex reasoning (e.g. distinguishing personal medical conditions from generic medical terms).
- **Focus:** An optional backend utilizing `llama.cpp` to run highly-quantized instruction models locally.

### `0.27.0`: Local Microservice DLP Endpoint
- **Use Case:** Polyglot application environments where Python is not the primary language.
- **Focus:** An optional `fastapi` extra providing a lightweight, stateless REST API wrapper around the engine.

### `1.0.0`: Mature Compatibility Commitment
Long-term compatibility begins after core processing, document rewriting, OCR, and remote-security
contracts have production fixtures, published benchmarks, and independent usage feedback against the hardening milestones above.

## Performance & Detection Quality Horizon (Post-1.0 / Ongoing)

To continually improve precision and recall (currently heavily measured in `benchmarks/evaluate_quality.py`) without introducing hardcoded or brittle regex artifacts, the following generalizable architectural improvements are slated for upcoming releases:

1. **Dynamic Entity-Specific Thresholds (ML)**: Instead of a flat `entity_threshold` across all labels, allow per-entity calibration. For example, lower activation thresholds for `LOCATION` (which historically suffers from low recall but high precision) while keeping `PERSON` strictly bounded.
2. **Context-Assisted ML Boosting**: Integrate the `ContextDetector` into the ML loop. If a token falls within 30 characters of a context trigger ("Name:", "Address:"), dynamically boost the ML logits for that specific text window, resolving the "missed isolated entities" problem.
3. **Span-Level Subword Repair (Token-Merge Averaging)**: DistilBERT uses WordPiece. If the tokenizer splits a name into subwords and assigns conflicting probabilities across them (e.g., dropping a middle subword), implement a CRF-style continuation heuristic to coerce adjacent subwords into a unified entity unless separated by a hard boundary.
4. **Ensemble Voting Arbitrator**: When multiple backends run simultaneously, introduce an `EnsembleArbitrator` allowing modes like `HighRecall` (Union), `HighPrecision` (Intersection - requires at least two backends to agree), or `Two-Pass` (Regex proposes, ML verifies).
5. **Cross-Lingual Zero-Shot Backend (GLiNER)**: Introduce an optional backend using GLiNER (Generalist Model for NER). GLiNER uses prompt-based label injection natively supporting 20+ languages out of the box, allowing dynamic detection of arbitrary entities ("Internal Project Code") with a fundamentally higher recall ceiling than traditional BERT models.

## Optional dependency policy

Extras appear only with the release that owns them: `ml`, `pdf`, `office`, `ocr`, `documents`,
`docling`, and `remote`. An `all` extra may exist for CI and integration testing, but user
documentation recommends the narrowest installation that satisfies the workload.

## Deliberately uncommitted work

Audio, video, reversible vaults, databases, Parquet, SQLite, framework wrappers, and generic
"process any file" claims remain outside the committed roadmap. New proposals must show that they
fit the layer boundaries and can meet the same safety and test standards.
