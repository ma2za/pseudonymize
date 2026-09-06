import json
import os
import re
import typing
from collections.abc import Sequence
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
    (("PER", "FIRSTNAME", "LASTNAME", "MIDDLENAME"), EntityType.PERSON),
    (("ORG", "COMPANYNAME"), EntityType.ORGANIZATION),
    (
        ("LOC", "CITY", "STATE", "COUNTY", "STREET", "ZIPCODE", "SECONDARYADDRESS", "BUILDINGNUM"),
        EntityType.LOCATION,
    ),
    (("EMAIL",), EntityType.EMAIL),
    (("PHONENUMBER", "PHONEIMEI"), EntityType.PHONE),
    (("IP", "IPV4", "IPV6"), EntityType.IP_ADDRESS),
    (("IBAN",), EntityType.IBAN),
    (("CREDITCARDNUMBER", "CREDITCARDCVV", "CREDITCARDISSUER"), EntityType.PAYMENT_CARD),
    (("SSN",), EntityType.NATIONAL_ID),
    (("URL",), EntityType.URL_CREDENTIAL),
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
    EntityType.PERSON: 0.10,
    EntityType.ORGANIZATION: 0.10,
}

_CONTEXT_BOOSTS: tuple[tuple[re.Pattern[str], EntityType, int], ...] = (
    (
        re.compile(r"(?i)\b(?:mr|ms|mrs|dr|prof|sir|ceo|name is|named)\b\.?\s*"),
        EntityType.PERSON,
        20,
    ),
    (
        re.compile(r"(?i)\b(?:in|at|from|city of|visit|street|road|address)\b\.?\s*"),
        EntityType.LOCATION,
        20,
    ),
)


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

        self._name = name
        self._entity_threshold = entity_threshold
        self._entity_thresholds = (
            entity_thresholds if entity_thresholds is not None else _DEFAULT_ENTITY_THRESHOLDS
        )
        self._window_overlap_tokens = window_overlap_tokens
        self._model_path = str(model_path)
        self._tokenizer_path = str(tokenizer_path)
        self._config_path = str(config_path) if config_path else None
        self._providers = providers

        self._session: Any = None
        self._tokenizer: Any = None
        self._id2label: dict[int, str] | None = None
        self._max_tokens: int = _DEFAULT_MAX_TOKENS

    @property
    def name(self) -> str:
        return self._name

    @property
    def capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(
            entity_types=frozenset(
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
                    EntityType.URL_CREDENTIAL,
                }
            ),
            remote=False,
        )

    @property
    def allow_remote_processing(self) -> bool:
        return False

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

    def detect(self, block: ContentBlock, policy: Policy) -> Sequence[Detection]:
        if not block.text.strip():
            return []

        try:
            self._load_model()

            # Calculate explicit global surrounding context (v1.7.0)
            global_context_triggers = []
            for pattern, _, _ in _CONTEXT_BOOSTS:
                for match in pattern.finditer(block.text):
                    trigger_word = match.group().strip().strip(":.-#")
                    if trigger_word and trigger_word not in global_context_triggers:
                        global_context_triggers.append(trigger_word)

            global_context_str = (
                " ".join(global_context_triggers) if global_context_triggers else None
            )

            detections: list[Detection] = []
            seen: dict[tuple[EntityType, int, int], Detection] = {}
            for window_start, window_end in self._windows(block.text):
                for detection in self._detect_window(
                    block.text[window_start:window_end], window_start, policy, global_context_str
                ):
                    # Windows overlap, so the same entity can be produced twice.
                    # The higher-confidence copy of an identical span wins.
                    key = (detection.entity_type, detection.start, detection.end)
                    previous = seen.get(key)
                    if previous is None or detection.confidence > previous.confidence:
                        seen[key] = detection
            detections = sorted(seen.values(), key=lambda item: (item.start, item.end))
            return tuple(detections)

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

    def _detect_window(
        self, text: str, char_offset: int, policy: Policy, context_pair: str | None = None
    ) -> list[Detection]:
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

        exp_logits = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
        probs = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)

        # Pre-calculate boosted ranges based on context keywords in window text
        boosted_ranges: dict[EntityType, list[tuple[int, int]]] = {
            EntityType.PERSON: [],
            EntityType.LOCATION: [],
        }
        for pattern, boost_entity_type, boost_len in _CONTEXT_BOOSTS:
            for match in pattern.finditer(text):
                start = match.end()
                end = start + boost_len
                boosted_ranges[boost_entity_type].append((start, end))

        predictions = []
        confidences = []
        o_label_id = next((k for k, v in (self._id2label or {}).items() if v == "O"), 0)

        for idx, token_probs in enumerate(probs):
            is_seq_b = idx < len(type_ids) and type_ids[idx] == 1
            if is_seq_b:
                predictions.append(o_label_id)
                confidences.append(1.0)
                continue

            best_label = int(np.argmax(token_probs))
            best_prob = float(token_probs[best_label])

            label_str = (self._id2label or {}).get(best_label)

            if label_str == "O" or not label_str:
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

        # Repair pass for subwords / zero-gap tokens to prevent premature entity truncation
        for idx in range(1, len(predictions)):
            label_id = predictions[idx]
            label_str = (self._id2label or {}).get(int(label_id))

            if not label_str or label_str == "O":
                prev_label_id = predictions[idx - 1]
                prev_label_str = (self._id2label or {}).get(int(prev_label_id))

                if prev_label_str and prev_label_str != "O":
                    _prev_start, prev_end = encoding.offsets[idx - 1]
                    curr_start, curr_end = encoding.offsets[idx]

                    if curr_start == prev_end:
                        # Only coerce if the token contains alphanumeric content,
                        # preventing trailing punctuation (.,!?) from being dragged in.
                        token_text = text[curr_start:curr_end]
                        if any(c.isalnum() for c in token_text):
                            predictions[idx] = prev_label_id
                            confidences[idx] = confidences[idx - 1]

        # Token predictions are merged into entity spans: subword continuations
        # (zero gap) and same-type tokens separated by one whitespace character
        # collapse into a single detection so that "John Smith" is one PERSON.
        spans: list[tuple[EntityType, int, int, list[float]]] = []

        for idx, label_id in enumerate(predictions):
            label_str = (self._id2label or {}).get(int(label_id))
            if not label_str or label_str == "O":
                continue
            entity_type = _entity_type_for(label_str)
            if entity_type is None:
                continue
            start, end = encoding.offsets[idx]
            if start >= end:
                continue

            conf = float(confidences[idx])

            if spans:
                previous_type, previous_start, previous_end, previous_confs = spans[-1]
                gap = text[previous_end:start]

                # Tolerate whitespace and common structural punctuation between
                # same-type entities
                # (e.g., hyphenated names, comma-separated addresses, apostrophes)
                if entity_type is previous_type and (
                    not gap.strip() or gap.strip() in ("-", ",", "'", ".", "/", "\\")
                ):
                    previous_confs.append(conf)
                    spans[-1] = (previous_type, previous_start, end, previous_confs)
                    continue
            spans.append((entity_type, start, end, [conf]))

        results = []
        for entity_type, start, end, token_confs in spans:
            confidence = max(token_confs)

            # Token-to-Character Alignment Optimization
            # If an ML span cuts a word in half, expand the boundary to the full word
            # using the tokenizer's exact character offsets to prevent leaking sub-words.
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

            if confidence >= policy.minimum_confidence:
                results.append(
                    Detection(
                        entity_type=entity_type,
                        start=start + char_offset,
                        end=end + char_offset,
                        confidence=confidence,
                        backend=self.name,
                        detector="onnx",
                    )
                )

        return results
