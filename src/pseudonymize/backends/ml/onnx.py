import functools
import json
import math
import os
import re
import typing
from collections.abc import Collection, Sequence
from dataclasses import replace
from pathlib import Path
from typing import Any

from pseudonymize.backends.base import BackendCapabilities, DetectionBackend
from pseudonymize.document import ContentBlock
from pseudonymize.exceptions import BackendExecutionError
from pseudonymize.policy import Policy
from pseudonymize.result import Detection, EntityType

if typing.TYPE_CHECKING:
    import numpy as np
    import onnxruntime as ort
    from tokenizers import Tokenizer
else:
    try:
        import numpy as np
        import onnxruntime as ort
        from tokenizers import Tokenizer
    except ImportError:  # pragma: no cover
        np = None
        ort = None
        Tokenizer = None

_LABEL_SUFFIXES: tuple[tuple[tuple[str, ...], EntityType], ...] = (
    # Standard CoNLL-03 suffixes plus Ai4Privacy fine-grained labels.
    (("PER", "FIRSTNAME", "LASTNAME", "MIDDLENAME", "GIVENNAME", "SURNAME"), EntityType.PERSON),
    (("ORG", "COMPANYNAME"), EntityType.ORGANIZATION),
    (
        (
            "LOC",
            "CITY",
            "STATE",
            "COUNTY",
            "STREET",
            "ZIPCODE",
            "SECONDARYADDRESS",
            "BUILDINGNUM",
            "BUILDINGNUMBER",
        ),
        EntityType.LOCATION,
    ),
    (("EMAIL",), EntityType.EMAIL),
    (("PHONENUMBER", "PHONEIMEI", "TELEPHONENUM"), EntityType.PHONE),
    (("IP", "IPV4", "IPV6"), EntityType.IP_ADDRESS),
    (("IBAN",), EntityType.IBAN),
    (("CREDITCARDNUMBER", "CREDITCARDCVV", "CREDITCARDISSUER"), EntityType.PAYMENT_CARD),
    (("SSN", "SOCIALNUM", "IDCARDNUM", "PASSPORTNUM", "DRIVERLICENSENUM"), EntityType.NATIONAL_ID),
    (("TAXNUM",), EntityType.TAX_ID),
    (("URL",), EntityType.URL_CREDENTIAL),
)

_ALL_SUPPORTED_ENTITY_TYPES: frozenset[EntityType] = frozenset(
    {
        EntityType.PERSON,
        EntityType.ORGANIZATION,
        EntityType.LOCATION,
        EntityType.EMAIL,
        EntityType.PHONE,
        EntityType.IP_ADDRESS,
        EntityType.IBAN,
        EntityType.PAYMENT_CARD,
        EntityType.NATIONAL_ID,
        EntityType.TAX_ID,
        EntityType.URL_CREDENTIAL,
    }
)


_DEFAULT_MAX_TOKENS = 512


def _positive_int(value: object, fallback: int) -> int:
    return (
        value if isinstance(value, int) and not isinstance(value, bool) and value > 0 else fallback
    )


def _entity_type_for(label: str) -> EntityType | None:
    for suffixes, entity_type in _LABEL_SUFFIXES:
        if label.endswith(suffixes):
            return entity_type
    return None


_DEFAULT_ENTITY_THRESHOLDS: dict[EntityType, float] = {
    EntityType.LOCATION: 0.20,
    EntityType.PERSON: 0.05,
    EntityType.ORGANIZATION: 0.05,
    EntityType.PAYMENT_CARD: 0.05,
    EntityType.NATIONAL_ID: 0.05,
}

_CONTEXT_BOOSTS: tuple[tuple[re.Pattern[str], EntityType, int], ...] = (
    (
        re.compile(
            r"(?i)\b(?:"
            r"mr|ms|mrs|miss|dr|prof|sir|madam|madame|mme|monsieur|herr|frau|"
            r"señor|señora|sr|sra|signor|signora|sig|bapak|ibu|pak|sdri|sdr|"
            r"ông|bà|cô|anh|chị|군|양|name is|named|họ và tên"
            r")\b\.?\s*"
        ),
        EntityType.PERSON,
        25,
    ),
    (
        re.compile(r"(?i)\b(?:in|at|from|city of|visit|street|road|address)\b\.?\s*"),
        EntityType.LOCATION,
        20,
    ),
)

_TRAILING_PERSON_BOOST = (
    re.compile(r"[様さん君ちゃん氏님씨]"),
    EntityType.PERSON,
    20,
)

_ADDRESS_CONTEXT_RX = re.compile(
    r"(?i)\b(?:"
    r"street|st|avenue|ave|road|rd|boulevard|blvd|lane|ln|drive|dr|way|court|ct|"
    r"rue|via|viale|corso|piazza|calle|paseo|avenida|av|strasse|str|weg|platz|"
    r"allee|damm|số|số\s*nhà|nhà|phố|haus|building|bldg|apt|apartment|suite|floor|fl|block|blk"
    r")\b"
)


def _aggregate_confidences(token_confs: list[float], mode: str) -> float:
    if not token_confs:
        return 0.0
    if mode == "max":
        return max(token_confs)
    if mode == "mean":
        return float(sum(token_confs) / len(token_confs))
    if mode == "min":
        return min(token_confs)
    if mode == "geometric_mean":
        log_sum = sum(math.log(max(c, 1e-6)) for c in token_confs)
        return float(math.exp(log_sum / len(token_confs)))
    return max(token_confs)


_LEADING_STRIP_CHARS = frozenset(
    "()[]{}<>\"'\u201c\u201d\u2018\u2019\u00ab\u00bb\u00bf\u00a1.,:;!?` \t\r\n"
)
_TRAILING_STRIP_CHARS = frozenset(
    "()[]{}<>\"'\u201c\u201d\u2018\u2019\u00ab\u00bb\u00bf\u00a1,:;!?` \t\r\n"
)

_ORGANIZATION_PERIOD_SUFFIXES = (
    "inc.",
    "corp.",
    "ltd.",
    "co.",
    "llc.",
    "gmbh.",
    "s.a.",
    "s.p.a.",
    "b.v.",
)
_PERSON_PERIOD_SUFFIXES = ("jr.", "sr.", "iii.", "ii.")


def _trim_span_boundaries(
    text: str, start: int, end: int, entity_type: EntityType | None = None
) -> tuple[int, int]:
    """Trim peripheral punctuation while preserving legitimate entity abbreviations."""
    while start < end and text[start] in _LEADING_STRIP_CHARS:
        start += 1

    while end > start:
        last_char = text[end - 1]
        if last_char in _TRAILING_STRIP_CHARS:
            end -= 1
        elif last_char == ".":
            span_lower = text[start:end].lower()
            if entity_type == EntityType.ORGANIZATION and any(
                span_lower.endswith(s) for s in _ORGANIZATION_PERIOD_SUFFIXES
            ):
                break
            if entity_type == EntityType.PERSON and any(
                span_lower.endswith(s) for s in _PERSON_PERIOD_SUFFIXES
            ):
                break
            end -= 1
        elif (
            entity_type == EntityType.PERSON
            and text[start:end].endswith(("'s", "\u2019s", "'S", "\u2019S"))
            and (end - start) > 2
        ):
            end -= 2
        else:
            break

    return start, end


class LocalONNXPIIBackend(DetectionBackend):
    def __init__(
        self,
        model_path: str | Path,
        tokenizer_path: str | Path,
        config_path: str | Path | None = None,
        name: str = "local_onnx_pii",
        providers: Sequence[str] = ("CPUExecutionProvider",),
        entity_threshold: float = 0.5,
        window_overlap_tokens: int = 64,
        entity_thresholds: dict[EntityType, float] | None = None,
        *,
        enable_context_boost: bool = True,
        enable_runner_up: bool = True,
        enable_confidence_remapping: bool = True,
        enable_subword_repair: bool = True,
        enable_word_expansion: bool = True,
        temperature: float = 1.0,
        decoder_mode: str = "legacy",
        span_aggregator: str = "max",
        allowed_entity_types: Collection[EntityType] | None = None,
    ) -> None:
        if ort is None or Tokenizer is None or np is None:
            raise ImportError(
                "The 'ml' extra is required to use LocalONNXPIIBackend. "
                "Install it with `pip install pseudonymize[ml]`."
            )

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"ONNX model not found at {model_path}")
        if not os.path.exists(tokenizer_path):
            raise FileNotFoundError(f"Tokenizer not found at {tokenizer_path}")
        if not 0 < entity_threshold <= 1:
            raise ValueError("entity_threshold must be between 0 and 1")
        if window_overlap_tokens < 0:
            raise ValueError("window_overlap_tokens must not be negative")
        if temperature <= 0:
            raise ValueError("temperature must be positive")
        if decoder_mode not in ("legacy", "constrained_bio"):
            raise ValueError(f"Unknown decoder_mode '{decoder_mode}'")
        if span_aggregator not in ("max", "mean", "min", "geometric_mean"):
            raise ValueError(f"Unknown span_aggregator '{span_aggregator}'")

        self._name = name
        self._entity_threshold = entity_threshold
        self._entity_thresholds = (
            entity_thresholds if entity_thresholds is not None else _DEFAULT_ENTITY_THRESHOLDS
        )
        self._window_overlap_tokens = window_overlap_tokens
        self._enable_context_boost = enable_context_boost
        self._enable_runner_up = enable_runner_up
        self._enable_confidence_remapping = enable_confidence_remapping
        self._enable_subword_repair = enable_subword_repair
        self._enable_word_expansion = enable_word_expansion
        self._temperature = float(temperature)
        self._decoder_mode = decoder_mode
        self._span_aggregator = span_aggregator
        self._allowed_entity_types = (
            frozenset(allowed_entity_types) if allowed_entity_types is not None else None
        )
        self._model_path = str(model_path)
        self._tokenizer_path = str(tokenizer_path)
        self._config_path = str(config_path) if config_path else None
        self._providers = providers

        self._session: Any = None
        self._tokenizer: Any = None
        self._id2label: dict[int, str] | None = None
        self._label2id: dict[str, int] | None = None
        self._max_tokens: int = _DEFAULT_MAX_TOKENS

        # Zero-Copy & LRU Caching Fast-Path (1.21.0)
        self._infer_text_cached = functools.lru_cache(maxsize=1024)(self._infer_batch)

    @property
    def temperature(self) -> float:
        return self._temperature

    @property
    def decoder_mode(self) -> str:
        return self._decoder_mode

    @property
    def span_aggregator(self) -> str:
        return self._span_aggregator

    @property
    def name(self) -> str:
        return self._name

    @property
    def allowed_entity_types(self) -> frozenset[EntityType] | None:
        """Return allowed entity types for this backend, or None if unrestricted."""
        return self._allowed_entity_types

    @property
    def capabilities(self) -> BackendCapabilities:
        types = (
            (self._allowed_entity_types & _ALL_SUPPORTED_ENTITY_TYPES)
            if self._allowed_entity_types is not None
            else _ALL_SUPPORTED_ENTITY_TYPES
        )
        return BackendCapabilities(
            entity_types=types,
            remote=False,
        )

    @property
    def allow_remote_processing(self) -> bool:
        return False

    @property
    def entity_thresholds(self) -> dict[EntityType, float]:
        """Return a copy of the per-entity calibration thresholds."""
        return dict(self._entity_thresholds)

    def _load_model(self) -> None:
        if self._session is None:
            self._session = ort.InferenceSession(self._model_path, providers=self._providers)
        if self._tokenizer is None:
            self._tokenizer = Tokenizer.from_file(self._tokenizer_path)
            # A tokenizer configured with truncation silently discards every token
            # past its limit, which for a redaction tool means the tail of a long
            # block is never inspected and its personal data survives untouched.
            # The limit is kept as the window size and the truncation is turned off
            # so that detect() can window the text itself.
            truncation = self._tokenizer.truncation
            if truncation:
                self._max_tokens = min(
                    self._max_tokens, _positive_int(truncation.get("max_length"), self._max_tokens)
                )
            self._tokenizer.no_truncation()
        if self._id2label is None:
            if self._config_path and os.path.exists(self._config_path):
                with open(self._config_path, encoding="utf-8") as f:
                    config = json.load(f)
                    id2label = config.get("id2label", {})
                    self._id2label = {int(k): str(v) for k, v in id2label.items()}
                    self._max_tokens = min(
                        self._max_tokens,
                        _positive_int(config.get("max_position_embeddings"), _DEFAULT_MAX_TOKENS),
                    )
            else:
                self._id2label = {}
        if self._label2id is None and self._id2label is not None:
            self._label2id = {v: k for k, v in self._id2label.items()}

    def detect(self, block: ContentBlock, policy: Policy) -> Sequence[Detection]:
        return self.detect_batch([block], policy)[0]

    def detect_batch(
        self, blocks: Sequence[ContentBlock], policy: Policy
    ) -> Sequence[Sequence[Detection]]:
        if not blocks:
            return ()

        try:
            self._load_model()

            windows_to_process: list[tuple[int, str, int, str | None]] = []
            block_seens: list[dict[tuple[EntityType, int, int], Detection]] = [
                {} for _ in range(len(blocks))
            ]

            budget = max(self._max_tokens - 2, 1)
            stride = max(budget - min(self._window_overlap_tokens, budget - 1), 1)

            for block_idx, block in enumerate(blocks):
                if not block.text.strip():
                    continue

                # Calculate explicit global surrounding context (v1.7.0)
                global_context_triggers = []
                if self._enable_context_boost:
                    for pattern, _, _ in _CONTEXT_BOOSTS:
                        for match in pattern.finditer(block.text):
                            trigger_word = match.group().strip().strip(":.-#")
                            if trigger_word and trigger_word not in global_context_triggers:
                                global_context_triggers.append(trigger_word)

                global_context_str = (
                    " ".join(global_context_triggers) if global_context_triggers else None
                )

                # Get tokenizer offsets for adaptive window slicing (v1.8.0)
                encoding = self._tokenizer.encode(block.text)
                offsets = [span for span in encoding.offsets if span[1] > span[0]]
                if not offsets:
                    continue

                token_start_idx = 0
                while token_start_idx < len(offsets):
                    token_end_idx = min(token_start_idx + budget, len(offsets))
                    window_start = offsets[token_start_idx][0]
                    window_end = offsets[token_end_idx - 1][1]

                    windows_to_process.append(
                        (
                            block_idx,
                            block.text[window_start:window_end],
                            window_start,
                            global_context_str,
                        )
                    )

                    token_start_idx += stride

            if not windows_to_process:
                return tuple(() for _ in blocks)

            if len(windows_to_process) == 1:
                # Single window fast-path (hits L1 cache natively)
                block_idx, w_text, w_start, w_context = windows_to_process[0]
                window_detections = self._detect_window(w_text, w_start, policy, w_context)
                for detection in window_detections:
                    key = (detection.entity_type, detection.start, detection.end)
                    block_seens[block_idx][key] = detection
            else:
                # Multi-window batched AVX processing (bypasses L1 for throughput)
                texts = [w[1] for w in windows_to_process]
                contexts = [w[3] for w in windows_to_process]

                # Split into chunks of 32 to avoid massive memory spikes
                batch_size = 32
                for i in range(0, len(texts), batch_size):
                    batch_texts = texts[i : i + batch_size]
                    batch_contexts = contexts[i : i + batch_size]

                    batch_results = self._infer_batch(batch_texts, policy, batch_contexts)

                    for j, win_detections in enumerate(batch_results):
                        global_idx = i + j
                        block_idx = windows_to_process[global_idx][0]
                        w_start = windows_to_process[global_idx][2]

                        for d in win_detections:
                            # Apply character offset
                            detection = replace(d, start=d.start + w_start, end=d.end + w_start)

                            key = (detection.entity_type, detection.start, detection.end)
                            previous = block_seens[block_idx].get(key)
                            if previous is None or detection.confidence > previous.confidence:
                                block_seens[block_idx][key] = detection

            results: list[tuple[Detection, ...]] = []
            for block_seen in block_seens:
                sorted_detections = sorted(
                    block_seen.values(), key=lambda item: (item.start, item.end)
                )
                results.append(tuple(sorted_detections))

            return tuple(results)

        except Exception as e:
            # The originating message can quote the tokenized input, so it never
            # reaches the caller. The chained cause is dropped for the same reason.
            raise BackendExecutionError(f"ONNX PII inference failed: {e}") from e

    def _windows(self, text: str) -> list[tuple[int, int]]:
        """Split text into overlapping character ranges that each fit the model.

        A transformer encoder has a fixed position budget. Feeding it more tokens
        than that either fails or silently ignores the tail, which for a redaction
        tool means personal data passes through untouched with no warning. Text is
        therefore cut into token windows that fit, overlapping so that an entity
        straddling a boundary is still seen whole by at least one window.
        """
        encoding = self._tokenizer.encode(text)
        # Two positions are reserved for the sequence's special tokens.
        budget = max(self._max_tokens - 2, 1)
        offsets = [span for span in encoding.offsets if span[1] > span[0]]
        if len(offsets) <= budget:
            return [(0, len(text))]

        stride = max(budget - min(self._window_overlap_tokens, budget - 1), 1)
        windows: list[tuple[int, int]] = []
        for first in range(0, len(offsets), stride):
            chunk = offsets[first : first + budget]
            windows.append((chunk[0][0], chunk[-1][1]))
            if first + budget >= len(offsets):
                break
        return windows

    def _infer_text(
        self, text: str, policy: Policy, context_pair: str | None = None
    ) -> tuple[Detection, ...]:
        # Only use context pair boosting for short, isolated texts (v1.7.0)
        # to prevent format mismatch degradation on long natural sentences.
        if context_pair and len(text.split()) < 10:
            encoding = self._tokenizer.encode(text, pair=context_pair)
        else:
            encoding = self._tokenizer.encode(text)

        ids = encoding.ids
        attention_mask = encoding.attention_mask
        type_ids = encoding.type_ids

        # Safeguard against ONNX broadcasting errors by strictly clipping to max_tokens (v1.7.0)
        if len(ids) > self._max_tokens:
            ids = ids[: self._max_tokens]
            attention_mask = attention_mask[: self._max_tokens]
            type_ids = type_ids[: self._max_tokens]
            ids[-1] = 102  # force last token to [SEP]

        inputs = {
            "input_ids": [ids],
            "attention_mask": [attention_mask],
            "token_type_ids": [type_ids],
        }
        expected_inputs = [i.name for i in self._session.get_inputs()]
        filtered_inputs = {
            k: np.array(v, dtype=np.int64) for k, v in inputs.items() if k in expected_inputs
        }

        outputs = self._session.run(None, filtered_inputs)
        logits = outputs[0][0]

        scaled_logits = logits / self._temperature
        exp_logits = np.exp(scaled_logits - np.max(scaled_logits, axis=-1, keepdims=True))
        probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

        return self._decode_window_spans(text, encoding, probs, policy)

    def _decode_window_spans(
        self, text: str, encoding: Any, probs: np.ndarray, policy: Policy
    ) -> tuple[Detection, ...]:
        # Pre-calculate boosted ranges based on context keywords in window text
        boosted_ranges: dict[EntityType, list[tuple[int, int]]] = {
            EntityType.PERSON: [],
            EntityType.LOCATION: [],
        }
        if self._enable_context_boost:
            for pattern, boost_entity_type, boost_len in _CONTEXT_BOOSTS:
                for match in pattern.finditer(text):
                    start = match.end()
                    end = start + boost_len
                    boosted_ranges[boost_entity_type].append((start, end))

            t_pattern, t_entity_type, t_len = _TRAILING_PERSON_BOOST
            for match in t_pattern.finditer(text):
                end = match.start()
                start = max(0, end - t_len)
                boosted_ranges[t_entity_type].append((start, end))

        predictions: list[int] = []
        confidences: list[float] = []
        o_label_id = next((k for k, v in (self._id2label or {}).items() if v == "O"), 0)

        for idx, token_probs in enumerate(probs):
            if idx >= len(encoding.offsets):
                break

            is_seq_b = hasattr(encoding, "sequence_ids") and encoding.sequence_ids[idx] == 1
            if is_seq_b:
                predictions.append(o_label_id)
                confidences.append(1.0)
                continue

            best_label = int(np.argmax(token_probs))
            best_prob = float(token_probs[best_label])

            label_str = (self._id2label or {}).get(best_label)

            if self._enable_runner_up and (label_str == "O" or not label_str):
                # A sharp softmax often puts "O" first while still giving a real
                # entity label substantial mass. The runner-up wins only when it
                # clears entity_threshold, an absolute probability configured on
                # the backend. The reported confidence stays the model's own
                # probability so that policy.minimum_confidence keeps meaning what
                # it says: raising it can only ever remove detections.
                runner_up_probs = np.copy(token_probs)
                runner_up_probs[best_label] = 0.0
                second_best = int(np.argmax(runner_up_probs))
                second_prob = float(runner_up_probs[second_best])

                second_label_str = (self._id2label or {}).get(second_best)
                second_entity_type = (
                    _entity_type_for(second_label_str) if second_label_str else None
                )

                threshold = self._entity_threshold
                if second_entity_type is not None:
                    threshold = self._entity_thresholds.get(second_entity_type, threshold)

                    # Apply context boosting: if this token lands in a boosted zone, cut threshold
                    if self._enable_context_boost:
                        token_start, _token_end = encoding.offsets[idx]
                        is_boosted = False
                        if second_entity_type in boosted_ranges:
                            for b_start, b_end in boosted_ranges[second_entity_type]:
                                if b_start <= token_start < b_end:
                                    is_boosted = True
                                    break
                        if is_boosted:
                            threshold *= 0.5

                if second_prob >= threshold:
                    best_label = second_best
                    best_prob = second_prob

            predictions.append(best_label)
            confidences.append(best_prob)

        # Repair pass for subwords / zero-gap tokens and compound connectors
        if self._enable_subword_repair:
            for idx in range(1, len(predictions)):
                label_id = predictions[idx]
                label_str = (self._id2label or {}).get(int(label_id))

                if not label_str or label_str == "O":
                    prev_label_id = predictions[idx - 1]
                    prev_label_str = (self._id2label or {}).get(int(prev_label_id))

                    is_same_seq = True
                    if hasattr(encoding, "sequence_ids"):
                        is_same_seq = encoding.sequence_ids[idx - 1] == encoding.sequence_ids[idx]

                    if prev_label_str and prev_label_str != "O" and is_same_seq:
                        _prev_start, prev_end = encoding.offsets[idx - 1]
                        curr_start, curr_end = encoding.offsets[idx]

                        tag = (
                            prev_label_str[2:]
                            if prev_label_str.startswith(("B-", "I-"))
                            else prev_label_str
                        )
                        i_label_str = f"I-{tag}"
                        continuation_id: int = (
                            self._label2id[i_label_str]
                            if self._label2id and i_label_str in self._label2id
                            else prev_label_id
                        )

                        # Case 1: Subword continuation (zero gap without leading space)
                        if curr_start == prev_end and not text[curr_start].isspace():
                            token_text = text[curr_start:curr_end]
                            if any(c.isalnum() for c in token_text):
                                predictions[idx] = continuation_id
                                entity_prob = (
                                    float(probs[idx][continuation_id])
                                    if continuation_id < len(probs[idx])
                                    else 0.0
                                )
                                # Token-merge averaging: smooth entity probabilities across subwords
                                confidences[idx] = (
                                    (confidences[idx - 1] + entity_prob) / 2.0
                                    if entity_prob > 0.0
                                    else confidences[idx - 1]
                                )

                        # Case 2: Internal compound connector (hyphen, apostrophe, slash)
                        # e.g. Jean-Paul, O'Connor, Smith-Jones
                        elif curr_start == prev_end and text[curr_start:curr_end] in (
                            "-",
                            "'",
                            "\u2019",
                            "/",
                        ):
                            if idx + 1 < len(predictions):
                                next_start, next_end = encoding.offsets[idx + 1]
                                if next_start == curr_end and any(
                                    c.isalnum() for c in text[next_start:next_end]
                                ):
                                    predictions[idx] = continuation_id
                                    confidences[idx] = confidences[idx - 1]

        # Token predictions are merged into entity spans: subword continuations
        # (zero gap) and same-type tokens separated by one whitespace character
        # collapse into a single detection so that "John Smith" is one PERSON.
        spans: list[tuple[EntityType, int, int, list[float], str]] = []

        for idx, label_id in enumerate(predictions):
            label_str = (self._id2label or {}).get(int(label_id))
            if not label_str or label_str == "O":
                continue
            entity_type = _entity_type_for(label_str)
            if entity_type is None:
                continue
            if self._allowed_entity_types and entity_type not in self._allowed_entity_types:
                continue
            start, end = encoding.offsets[idx]
            if start >= end:
                continue

            curr_tag = label_str[2:] if label_str.startswith(("B-", "I-")) else label_str

            raw_conf = float(confidences[idx])
            thresh = self._entity_thresholds.get(entity_type, self._entity_threshold)

            # Piece-wise linear confidence calibration (v1.10.0)
            # Maps the raw optimal threshold `thresh` directly onto the default 0.80 engine floor,
            # ensuring that highly accurate low-probability detections survive policy filtering.
            # Bypassed for extremely permissive development thresholds (less than 0.05)
            # to keep real low confidences.
            if self._enable_confidence_remapping and thresh >= 0.05:
                if raw_conf >= thresh:
                    conf = 0.80 + 0.20 * (raw_conf - thresh) / max(1.0 - thresh, 1e-5)
                else:
                    conf = 0.80 * raw_conf / max(thresh, 1e-5)
            else:
                conf = raw_conf

            if spans:
                previous_type, previous_start, previous_end, previous_confs, previous_tag = spans[
                    -1
                ]
                gap = text[previous_end:start]

                can_merge = False
                if self._decoder_mode == "constrained_bio":
                    is_b = label_str.startswith("B-")
                    if is_b:
                        # Same exact tag (e.g. B-CITY + B-CITY or B-GIVENNAME + B-GIVENNAME)
                        # indicates two distinct entities unless zero-gap subword
                        if curr_tag == previous_tag:
                            can_merge = (entity_type is previous_type) and (start == previous_end)
                        else:
                            # Different tag components of same entity (e.g. GIVENNAME + SURNAME)
                            can_merge = (entity_type is previous_type) and (
                                not gap.strip() or gap.strip() in ("-", ",", "'", ".", "/", "\\")
                            )
                    else:
                        # I- token or continuation
                        can_merge = (entity_type is previous_type) and (
                            not gap.strip() or gap.strip() in ("-", ",", "'", ".", "/", "\\")
                        )
                else:
                    # Legacy: tolerate whitespace and punctuation between same-type entities
                    can_merge = (entity_type is previous_type) and (
                        not gap.strip() or gap.strip() in ("-", ",", "'", ".", "/", "\\")
                    )

                if can_merge:
                    previous_confs.append(conf)
                    merged_tag = (
                        curr_tag
                        if previous_tag in ("B-BUILDINGNUM", "I-BUILDINGNUM")
                        else previous_tag
                    )
                    spans[-1] = (previous_type, previous_start, end, previous_confs, merged_tag)
                    continue
            spans.append((entity_type, start, end, [conf], curr_tag))

        results = []
        for entity_type, start, end, token_confs, _tag in spans:
            # Standalone building numbers (e.g. "370", "18", "11번") are numeric components
            # of addresses, not standalone locations. They are only valid locations when
            # contiguous with an address/street span or surrounded by address context.
            if _tag in ("B-BUILDINGNUM", "I-BUILDINGNUM"):
                ctx = text[max(0, start - 35) : min(len(text), end + 35)]
                if not _ADDRESS_CONTEXT_RX.search(ctx):
                    continue

            confidence = _aggregate_confidences(token_confs, self._span_aggregator)

            # Token-to-Character Alignment Optimization
            # If an ML span cuts a word in half, expand the boundary to the full word
            # using the tokenizer's exact character offsets to prevent leaking sub-words.
            if self._enable_word_expansion:
                if start < len(text):
                    start_word = encoding.char_to_word(start)
                    if start_word is not None:
                        word_chars = encoding.word_to_chars(start_word)
                        if word_chars is not None:
                            start = min(start, word_chars[0])

                if end > 0 and end <= len(text):
                    end_word = encoding.char_to_word(end - 1)
                    if end_word is not None:
                        word_chars = encoding.word_to_chars(end_word)
                        if word_chars is not None:
                            end = max(end, word_chars[1])

            # Trim peripheral punctuation and whitespace that cannot be part of an entity boundary
            start, end = _trim_span_boundaries(text, start, end, entity_type)
            if start >= end:
                continue

            if confidence >= policy.minimum_confidence:
                results.append(
                    Detection(
                        entity_type=entity_type,
                        start=start,
                        end=end,
                        confidence=confidence,
                        backend=self.name,
                        detector="onnx",
                    )
                )

        return tuple(results)

    def _detect_window(
        self, text: str, char_offset: int, policy: Policy, context_pair: str | None = None
    ) -> list[Detection]:
        # Fast-Path: Bypass ML loop entirely for cached tokens/windows
        # Wrap single string into list to match signature of _infer_batch
        cached = self._infer_text_cached((text,), policy, (context_pair,))[0]
        if char_offset == 0:
            return list(cached)
        return [replace(d, start=d.start + char_offset, end=d.end + char_offset) for d in cached]

    def _infer_batch(
        self, texts: list[str], policy: Policy, context_pairs: list[str | None]
    ) -> list[tuple[Detection, ...]]:

        batch_size = len(texts)
        if batch_size == 0:
            return []

        if hasattr(self._tokenizer, "encode_batch"):
            # Dynamic padding to longest sequence in batch (snapped to 8 for SIMD alignment)
            self._tokenizer.enable_padding(direction="right", pad_to_multiple_of=8)

            encode_inputs: list[str | tuple[str, str]] = []
            for text, pair in zip(texts, context_pairs, strict=False):
                if pair and len(text.split()) < 10:
                    encode_inputs.append((text, pair))
                else:
                    encode_inputs.append(text)

            encodings = self._tokenizer.encode_batch(encode_inputs)
            # Disable padding again so single window doesn't get padded unnecessarily
            self._tokenizer.no_padding()
        else:
            # Fallback if tokenizer doesn't support batch directly (should not happen)
            encodings = []
            for text, pair in zip(texts, context_pairs, strict=False):
                if pair and len(text.split()) < 10:
                    encodings.append(self._tokenizer.encode(text, pair=pair))
                else:
                    encodings.append(self._tokenizer.encode(text))

            # Dynamic padding to batch max length snapped to 8
            raw_max = max(len(e.ids) for e in encodings)
            max_len = min(raw_max + (8 - raw_max % 8) % 8, self._max_tokens)

            for e in encodings:
                ids = e.ids[:max_len]
                mask = e.attention_mask[:max_len]
                type_ids = e.type_ids[:max_len]

                pad_len = max_len - len(ids)
                if pad_len > 0:
                    ids.extend([0] * pad_len)
                    mask.extend([0] * pad_len)
                    type_ids.extend([0] * pad_len)

                e.ids = ids
                e.attention_mask = mask
                e.type_ids = type_ids

        batch_ids = []
        batch_mask = []
        batch_type_ids = []

        for encoding in encodings:
            ids = encoding.ids
            mask = encoding.attention_mask
            type_ids = encoding.type_ids

            if len(ids) > self._max_tokens:
                ids = ids[: self._max_tokens]
                mask = mask[: self._max_tokens]
                type_ids = type_ids[: self._max_tokens]
                ids[-1] = 102

            batch_ids.append(ids)
            batch_mask.append(mask)
            batch_type_ids.append(type_ids)

        inputs = {
            "input_ids": batch_ids,
            "attention_mask": batch_mask,
            "token_type_ids": batch_type_ids,
        }

        expected_inputs = [i.name for i in self._session.get_inputs()]
        filtered_inputs = {
            k: np.array(v, dtype=np.int64) for k, v in inputs.items() if k in expected_inputs
        }

        outputs = self._session.run(None, filtered_inputs)
        batch_logits = outputs[0]

        batch_results = []

        for batch_idx, logits in enumerate(batch_logits):
            text = texts[batch_idx]
            encoding = encodings[batch_idx]

            scaled_logits = logits / self._temperature
            exp_logits = np.exp(scaled_logits - np.max(scaled_logits, axis=-1, keepdims=True))
            probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

            batch_results.append(self._decode_window_spans(text, encoding, probs, policy))

        return batch_results
