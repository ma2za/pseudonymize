import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from pseudonymize.backends.base import BackendCapabilities, DetectionBackend
from pseudonymize.document import ContentBlock
from pseudonymize.exceptions import BackendExecutionError
from pseudonymize.policy import Policy
from pseudonymize.result import Detection, EntityType

try:
    from llama_cpp import Llama
except ImportError:  # pragma: no cover
    Llama = None


class LocalLlamaBackend(DetectionBackend):
    def __init__(
        self,
        model_path: str | Path,
        name: str = "local_llama",
        capabilities: BackendCapabilities | None = None,
        **llama_kwargs: Any,
    ) -> None:
        if Llama is None:
            raise ImportError(
                "The 'llama' extra is required to use LocalLlamaBackend. "
                "Install it with `pip install pseudonymize[llama]`."
            )

        if not Path(model_path).exists():
            raise FileNotFoundError(f"GGUF model not found at {model_path}")

        self._name = name

        if capabilities is None:
            self._capabilities = BackendCapabilities(frozenset(EntityType))
        else:
            self._capabilities = capabilities

        llama_kwargs.setdefault("n_ctx", 2048)
        llama_kwargs.setdefault("verbose", False)

        try:
            self._llm = Llama(model_path=str(model_path), **llama_kwargs)
        except Exception as e:
            raise BackendExecutionError(f"failed to load llama model: {e}") from e

    @property
    def name(self) -> str:
        return self._name

    @property
    def capabilities(self) -> BackendCapabilities:
        return self._capabilities

    @property
    def allow_remote_processing(self) -> bool:
        return False

    def detect(self, block: ContentBlock, policy: Policy) -> Sequence[Detection]:
        if not block.text.strip():
            return ()

        requested_types = {t for t in policy.entity_types if t in self._capabilities.entity_types}
        if not requested_types:
            return ()

        req_str = ", ".join(t.value for t in requested_types)
        prompt = (
            "You are a strict data extraction tool. Extract the following entities from the text: "
            f"{req_str}.\n"
            "Return ONLY a valid JSON array of objects with keys 'type' and 'text'.\n"
            f"Text: {block.text}\n"
            "JSON:"
        )

        try:
            response = self._llm(
                prompt,
                max_tokens=512,
                stop=["```", "\n\n"],
                temperature=0.0,
            )
            raw_output = response["choices"][0]["text"].strip()

            if not raw_output.startswith("["):
                idx = raw_output.find("[")
                if idx != -1:
                    raw_output = raw_output[idx:]
            if not raw_output.endswith("]"):
                idx = raw_output.rfind("]")
                if idx != -1:
                    raw_output = raw_output[: idx + 1]

            if not raw_output or not raw_output.startswith("[") or not raw_output.endswith("]"):
                return ()

            extracted = json.loads(raw_output)

            detections = []
            for item in extracted:
                t = item.get("type")
                text = item.get("text")
                if not t or not text:
                    continue

                try:
                    entity_type = EntityType(t)
                except ValueError:
                    continue

                if entity_type not in requested_types:
                    continue

                start = block.text.find(text)
                if start != -1:
                    detections.append(
                        Detection(
                            entity_type=entity_type,
                            start=start,
                            end=start + len(text),
                            confidence=0.8,
                            detector="llama_cpp",
                            backend=self.name,
                        )
                    )

            return tuple(detections)

        except Exception as e:
            raise BackendExecutionError(f"Llama inference failed: {e}") from e
