import tempfile

import pytest

from pseudonymize.backends.ner.onnx import LocalONNXNERBackend
from pseudonymize.document import ContentBlock, TextOffsetLocation
from pseudonymize.exceptions import BackendExecutionError
from pseudonymize.policy import NetworkPolicy, Policy
from pseudonymize.result import EntityType


def test_ner_backend_capabilities() -> None:
    with (
        tempfile.NamedTemporaryFile() as model_file,
        tempfile.NamedTemporaryFile() as tokenizer_file,
    ):
        backend = LocalONNXNERBackend(
            model_path=model_file.name, tokenizer_path=tokenizer_file.name
        )
        caps = backend.capabilities

        assert backend.name == "local_onnx_ner"
        assert not caps.remote
        assert not backend.allow_remote_processing
        assert EntityType.PERSON in caps.entity_types
        assert EntityType.ORGANIZATION in caps.entity_types
        assert EntityType.LOCATION in caps.entity_types


def test_ner_backend_missing_files() -> None:
    with pytest.raises(FileNotFoundError, match="ONNX model not found"):
        LocalONNXNERBackend(model_path="nonexistent.onnx", tokenizer_path="tokenizer.json")

    with pytest.raises(FileNotFoundError, match="Tokenizer not found"):
        LocalONNXNERBackend(model_path=__file__, tokenizer_path="nonexistent.json")


def test_ner_detect_empty_block() -> None:
    with (
        tempfile.NamedTemporaryFile() as model_file,
        tempfile.NamedTemporaryFile() as tokenizer_file,
    ):
        backend = LocalONNXNERBackend(
            model_path=model_file.name, tokenizer_path=tokenizer_file.name
        )
        policy = Policy(network_policy=NetworkPolicy.DENY)
        block = ContentBlock(id="1", text="   \n", location=TextOffsetLocation(0, 4))

        detections = backend.detect(block, policy)
        assert len(detections) == 0


def test_ner_detect_stub_returns_empty_and_raises_on_invalid_model() -> None:
    with (
        tempfile.NamedTemporaryFile() as model_file,
        tempfile.NamedTemporaryFile() as tokenizer_file,
    ):
        backend = LocalONNXNERBackend(
            model_path=model_file.name, tokenizer_path=tokenizer_file.name
        )
        policy = Policy(network_policy=NetworkPolicy.DENY)
        block = ContentBlock(id="1", text="Hello John Doe", location=TextOffsetLocation(0, 14))

        # This will attempt to load the actual model/tokenizer with empty files, which should fail
        with pytest.raises(BackendExecutionError, match="ONNX NER inference failed"):
            backend.detect(block, policy)
