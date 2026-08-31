from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from pseudonymize.backends.ml.llama import LocalLlamaBackend
from pseudonymize.document import ContentBlock, TextOffsetLocation
from pseudonymize.exceptions import BackendExecutionError
from pseudonymize.policy import Policy
from pseudonymize.result import EntityType


def test_llama_backend_missing_model() -> None:
    with patch("pseudonymize.backends.ml.llama.Llama", MagicMock()):
        with pytest.raises(FileNotFoundError):
            LocalLlamaBackend(model_path="nonexistent.gguf")


def test_llama_capabilities(tmp_path: Path) -> None:
    model = tmp_path / "fake.gguf"
    model.write_text("fake")

    mock_llama = MagicMock(side_effect=Exception("Failed to load"))
    with patch("pseudonymize.backends.ml.llama.Llama", mock_llama):
        with pytest.raises(BackendExecutionError):
            LocalLlamaBackend(model_path=model)


@patch("pseudonymize.backends.ml.llama.Llama")
def test_llama_detect(mock_llama_class: MagicMock, tmp_path: Path) -> None:
    model = tmp_path / "fake.gguf"
    model.write_text("fake")

    mock_instance = MagicMock()
    mock_llama_class.return_value = mock_instance
    mock_instance.return_value = {"choices": [{"text": '[{"type": "PERSON", "text": "John Doe"}]'}]}

    backend = LocalLlamaBackend(model_path=model)

    block = ContentBlock("id1", "Hello John Doe", TextOffsetLocation(0, 14))
    policy = Policy.default()

    detections = backend.detect(block, policy)

    assert len(detections) == 1
    assert detections[0].entity_type == EntityType.PERSON
    assert detections[0].start == 6
    assert detections[0].end == 14
    assert detections[0].backend == "local_llama"
    assert detections[0].detector == "llama_cpp"
