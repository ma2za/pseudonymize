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
    import onnxruntime as ort  # type: ignore[import-untyped]
    from tokenizers import Tokenizer
except ImportError:
    ort = None
    Tokenizer = None  # type: ignore[misc,assignment]


class LocalONNXNERBackend(DetectionBackend):
    def __init__(
        self,
        model_path: str | Path,
        tokenizer_path: str | Path,
        name: str = "local_onnx_ner",
        providers: Sequence[str] = ("CPUExecutionProvider",),
    ) -> None:
        if ort is None or Tokenizer is None:
            raise ImportError(
                "The 'ner' extra is required to use LocalONNXNERBackend. "
                "Install it with `pip install pseudonymize[ner]`."
            )

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"ONNX model not found at {model_path}")
        if not os.path.exists(tokenizer_path):
            raise FileNotFoundError(f"Tokenizer not found at {tokenizer_path}")

        self._name = name
        self._model_path = str(model_path)
        self._tokenizer_path = str(tokenizer_path)
        self._providers = providers

        self._session: Any = None
        self._tokenizer: Any = None

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

    def detect(self, block: ContentBlock, policy: Policy) -> Sequence[Detection]:
        if not block.text.strip():
            return []

        try:
            self._load_model()

            # Simple fallback for text that doesn't trigger the model nicely
            # This is a stub for the actual inference logic which will map token predictions
            # to EntityType and map token offsets back to character offsets.
            # 
            # In a real implementation we would do:
            # 1. encoding = self._tokenizer.encode(block.text)
            # 2. outputs = self._session.run(None, {"input_ids": [encoding.ids], ...})
            # 3. decode predictions to EntityType and use encoding.offsets to yield
            #    Detection objects.

            # Since this is a placeholder/stub without real weights to test against,
            # we return an empty sequence until a concrete model logic is wired in.
            return []

        except Exception as e:
            raise BackendExecutionError(f"ONNX NER inference failed: {e}") from e
