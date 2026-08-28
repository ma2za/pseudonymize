import json
import os
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
    except ImportError:
        np = None
        ort = None
        Tokenizer = None

_LABEL_SUFFIXES: tuple[tuple[tuple[str, ...], EntityType], ...] = (
    # Standard CoNLL-03 suffixes plus Ai4Privacy fine-grained labels.
    (("PER", "FIRSTNAME", "LASTNAME", "MIDDLENAME"), EntityType.PERSON),
    (("ORG", "COMPANYNAME"), EntityType.ORGANIZATION),
    (
        ("LOC", "CITY", "STATE", "COUNTY", "STREET", "ZIPCODE", "SECONDARYADDRESS"),
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

def _entity_type_for(label: str) -> EntityType | None:
    for suffixes, entity_type in _LABEL_SUFFIXES:
        if label.endswith(suffixes):
            return entity_type
    return None

class LocalONNXPIIBackend(DetectionBackend):
    def __init__(
        self,
        model_path: str | Path,
        tokenizer_path: str | Path,
        config_path: str | Path | None = None,
        name: str = "local_onnx_pii",
        providers: Sequence[str] = ("CPUExecutionProvider",),
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

        self._name = name
        self._model_path = str(model_path)
        self._tokenizer_path = str(tokenizer_path)
        self._config_path = str(config_path) if config_path else None
        self._providers = providers

        self._session: Any = None
        self._tokenizer: Any = None
        self._id2label: dict[int, str] | None = None

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
        if self._id2label is None:
            if self._config_path and os.path.exists(self._config_path):
                with open(self._config_path, encoding="utf-8") as f:
                    config = json.load(f)
                    id2label = config.get("id2label", {})
                    self._id2label = {int(k): str(v) for k, v in id2label.items()}
            else:
                self._id2label = {}

    def detect(self, block: ContentBlock, policy: Policy) -> Sequence[Detection]:
        if not block.text.strip():
            return []

        try:
            self._load_model()

            encoding = self._tokenizer.encode(block.text)

            inputs = {"input_ids": [encoding.ids], "attention_mask": [encoding.attention_mask]}
            expected_inputs = [i.name for i in self._session.get_inputs()]
            filtered_inputs = {
                k: np.array(v, dtype=np.int64) for k, v in inputs.items() if k in expected_inputs
            }

            outputs = self._session.run(None, filtered_inputs)
            logits = outputs[0][0]

            predictions = np.argmax(logits, axis=-1)

            # Token predictions are merged into entity spans: subword continuations
            # (zero gap) and same-type tokens separated by one whitespace character
            # collapse into a single detection so that "John Smith" is one PERSON.
            spans: list[tuple[EntityType, int, int]] = []

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
                if spans:
                    previous_type, previous_start, previous_end = spans[-1]
                    gap = block.text[previous_end:start]
                    if (
                        entity_type is previous_type
                        and previous_end <= start <= previous_end + 1
                        and not gap.strip()
                    ):
                        spans[-1] = (previous_type, previous_start, end)
                        continue
                spans.append((entity_type, start, end))

            return tuple(
                Detection(
                    entity_type=entity_type,
                    start=start,
                    end=end,
                    confidence=0.99,
                    backend=self.name,
                    detector="onnx",
                )
                for entity_type, start, end in spans
            )

        except Exception as e:
            raise BackendExecutionError(f"ONNX PII inference failed: {e}") from e
