import json
import os
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from pseudonymize.backends.base import BackendCapabilities, DetectionBackend
from pseudonymize.document import ContentBlock
from pseudonymize.exceptions import BackendExecutionError
from pseudonymize.policy import Policy
from pseudonymize.result import Detection, EntityType

try:
    import numpy as np  # type: ignore[import-untyped]
    import onnxruntime as ort  # type: ignore[import-untyped]
    from tokenizers import Tokenizer
except ImportError:
    np = None  # type: ignore[misc,assignment]
    ort = None
    Tokenizer = None  # type: ignore[misc,assignment]


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

            detections = []

            for idx, label_id in enumerate(predictions):
                if label_id == 0 or self._id2label is None:
                    continue

                label_str = self._id2label.get(label_id)
                if not label_str or label_str == "O":
                    continue

                entity_type = None

                # Standard CoNLL-03 tags
                if label_str.endswith("PER"):
                    entity_type = EntityType.PERSON
                elif label_str.endswith("ORG"):
                    entity_type = EntityType.ORGANIZATION
                elif label_str.endswith("LOC"):
                    entity_type = EntityType.LOCATION

                # Ai4Privacy tags mapping
                elif any(label_str.endswith(s) for s in ("FIRSTNAME", "LASTNAME", "MIDDLENAME")):
                    entity_type = EntityType.PERSON
                elif label_str.endswith("COMPANYNAME"):
                    entity_type = EntityType.ORGANIZATION
                elif any(
                    label_str.endswith(s) for s in ("CITY", "STATE", "COUNTY", "STREET", "ZIPCODE")
                ):
                    entity_type = EntityType.LOCATION

                if entity_type:
                    start, end = encoding.offsets[idx]
                    if start == 0 and end == 0 and idx not in (0, len(predictions) - 1):
                        continue
                    if start == end:
                        continue

                    detections.append(
                        Detection(
                            entity_type=entity_type,
                            start=start,
                            end=end,
                            confidence=0.99,
                            backend=self.name,
                            detector="onnx",
                        )
                    )

            return tuple(detections)

        except Exception as e:
            raise BackendExecutionError(f"ONNX PII inference failed: {e}") from e
