import hashlib
import urllib.request
from pathlib import Path
from typing import Any

import pytest

from pseudonymize.backends.ml.onnx import LocalONNXPIIBackend
from pseudonymize.document import ContentBlock, TextOffsetLocation
from pseudonymize.exceptions import BackendExecutionError
from pseudonymize.policy import NetworkPolicy, Policy
from pseudonymize.result import EntityType

# Keep downloaded artifacts outside pytest's configured basetemp, which is cleared at startup.
CACHE_DIR = Path(".cache/pseudonymize-tests/models/distilbert-ml")
MODEL_URL_BASE = (
    "https://huggingface.co/onnx-community/distilbert_finetuned_ai4privacy_v2-ONNX/resolve/main/"
)
MODEL_FILES = {
    "config.json": (
        "config.json",
        "5155e76f303c68ee15d8f01b580550c062cebfbb42dda3f5f3698b2d75424216",
    ),
    "tokenizer.json": (
        "tokenizer.json",
        "cb374d6bc042c22455946f4e09a89d29882a199fdaf8fb25be00dc8b8857a448",
    ),
    "model_int8.onnx": (
        "onnx/model_int8.onnx",
        "6faa1d7f5b54140bbba18ba87480e11073927b5fff16f69558bd51058a05b305",
    ),
}


def download_file(url: str, dest: Path, sha256: str) -> None:
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})  # noqa: S310
        with urllib.request.urlopen(req) as response, open(dest, "wb") as f:  # noqa: S310
            f.write(response.read())
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    if digest != sha256:
        dest.unlink()
        raise RuntimeError(f"checksum mismatch for {dest.name}: {digest}")


@pytest.fixture(scope="session")
def distilbert_artifacts() -> tuple[Path, Path, Path]:
    paths = []
    for local_name, (remote_path, sha256) in MODEL_FILES.items():
        dest = CACHE_DIR / local_name
        download_file(MODEL_URL_BASE + remote_path, dest, sha256)
        paths.append(dest)
    # Returns (config, tokenizer, model)
    return (paths[0], paths[1], paths[2])


def test_ml_backend_capabilities(distilbert_artifacts: tuple[Path, Path, Path]) -> None:
    config_path, tokenizer_path, model_path = distilbert_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    caps = backend.capabilities

    assert backend.name == "local_onnx_pii"
    assert not caps.remote
    assert not backend.allow_remote_processing
    assert EntityType.PERSON in caps.entity_types
    assert EntityType.ORGANIZATION in caps.entity_types
    assert EntityType.LOCATION in caps.entity_types


def test_ml_backend_missing_files() -> None:
    with pytest.raises(FileNotFoundError, match="ONNX model not found"):
        LocalONNXPIIBackend(model_path="nonexistent.onnx", tokenizer_path="tokenizer.json")

    with pytest.raises(FileNotFoundError, match="Tokenizer not found"):
        LocalONNXPIIBackend(model_path=__file__, tokenizer_path="nonexistent.json")


def test_ml_backend_missing_optional_dependency(monkeypatch: pytest.MonkeyPatch) -> None:
    import pseudonymize.backends.ml.onnx

    monkeypatch.setattr(pseudonymize.backends.ml.onnx, "ort", None)

    with pytest.raises(ImportError, match="The 'ml' extra is required"):
        LocalONNXPIIBackend(model_path="model", tokenizer_path="tok")

    # Cover Tokenizer missing
    monkeypatch.setattr(pseudonymize.backends.ml.onnx, "ort", "mock_ort")
    monkeypatch.setattr(pseudonymize.backends.ml.onnx, "Tokenizer", None)

    with pytest.raises(ImportError, match="The 'ml' extra is required"):
        LocalONNXPIIBackend(model_path="model", tokenizer_path="tok")

    # Cover np missing
    monkeypatch.setattr(pseudonymize.backends.ml.onnx, "Tokenizer", "mock_tok")
    monkeypatch.setattr(pseudonymize.backends.ml.onnx, "np", None)

    with pytest.raises(ImportError, match="The 'ml' extra is required"):
        LocalONNXPIIBackend(model_path="model", tokenizer_path="tok")


def test_ml_detect_config_missing_fallback(distilbert_artifacts: tuple[Path, Path, Path]) -> None:
    _, tokenizer_path, model_path = distilbert_artifacts

    # Do not provide config path, this forces _id2label to evaluate to {}
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=None
    )
    policy = Policy(network_policy=NetworkPolicy.DENY)
    block = ContentBlock(id="1", text="My name is Sarah", location=TextOffsetLocation(0, 16))

    detections = backend.detect(block, policy)
    assert len(detections) == 0


def test_ml_detect_empty_block(distilbert_artifacts: tuple[Path, Path, Path]) -> None:
    config_path, tokenizer_path, model_path = distilbert_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    policy = Policy(network_policy=NetworkPolicy.DENY)

    assert (
        len(
            backend.detect(ContentBlock(id="1", text="", location=TextOffsetLocation(0, 0)), policy)
        )
        == 0
    )
    assert (
        len(
            backend.detect(
                ContentBlock(id="1", text="   \n", location=TextOffsetLocation(0, 4)), policy
            )
        )
        == 0
    )


def test_ml_detect_handles_unmapped_labels(
    distilbert_artifacts: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path, tokenizer_path, model_path = distilbert_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    policy = Policy(network_policy=NetworkPolicy.DENY)
    block = ContentBlock(id="1", text="My name is Sarah", location=TextOffsetLocation(0, 16))

    backend._load_model()
    # Remove the id2label mapping entirely after it's loaded
    # Set it to {} so _load_model() won't reload it during detect()
    backend._id2label = {}
    detections = backend.detect(block, policy)
    assert len(detections) == 0

    # Put a fake label map that yields 'O' for everything
    backend._id2label = dict.fromkeys(range(100), "O")
    detections = backend.detect(block, policy)
    assert len(detections) == 0


def test_ml_detect_real_inference_returns_meaningful_detections(
    distilbert_artifacts: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path, tokenizer_path, model_path = distilbert_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    policy = Policy(network_policy=NetworkPolicy.DENY)

    # A hardened, highly specific text to test offsets, multiple contiguous entities,
    # punctuation handling, subwords, and mixed entity types all in one string.
    text = "John Smith is currently visiting Microsoft's headquarters in Seattle, Washington!"
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))

    detections = backend.detect(block, policy)

    # Sort detections by offset for deterministic assertion
    sorted_detections = sorted(detections, key=lambda d: d.start)

    # Token predictions merge into entity spans, so we expect:
    # PERSON: "John Smith" (0,10) as one span, subwords and the space included
    # LOC: "Seattle" (61,68) and "Washington" (70,80) kept apart by the comma
    assert len(sorted_detections) >= 3

    # Let's map out the exact expected strings for the entities found
    found_entities = [(d.entity_type, text[d.start : d.end]) for d in sorted_detections]

    assert (EntityType.PERSON, "John Smith") in found_entities
    assert (EntityType.LOCATION, "Seattle") in found_entities
    assert (EntityType.LOCATION, "Washington") in found_entities

    # Make sure we didn't accidentally include punctuation like "'s" or "," as part of the entity
    for _entity_type, chunk in found_entities:
        assert "'" not in chunk
        assert "," not in chunk
        assert "!" not in chunk

    # Add artificial label mappings to cover branches
    # (PER is hit in earlier version, here we can hit the loop)
    backend._load_model()
    # Intercept outputs to artificially trigger `start == 0 and end == 0` check bypassing
    original_encode = backend._tokenizer.encode

    class FakeEncoding:
        def __init__(self, original: Any):
            self.ids = original.ids
            self.attention_mask = original.attention_mask
            self.tokens = original.tokens
            self.offsets = [(1, 1)] * len(original.offsets)

    def fake_encode(t: str) -> Any:
        encoding = original_encode(t)
        return FakeEncoding(encoding)

    monkeypatch.setattr(backend._tokenizer, "encode", fake_encode)
    detections = backend.detect(block, policy)
    assert len(detections) == 0

    # Ensure coverage for when label_str exists but isn't something we map
    backend._id2label = dict.fromkeys(range(100), "B-UNKNOWN")
    detections = backend.detect(block, policy)
    assert len(detections) == 0

    # Ensure coverage for standard CoNLL-03 mapping (PER, ORG, LOC)
    monkeypatch.undo()  # Remove the fake encode to get real offsets again
    backend._id2label = {
        0: "O",
        1: "B-PER",
        2: "I-PER",
        3: "B-ORG",
        4: "I-ORG",
        5: "B-LOC",
        6: "I-LOC",
    }
    # Artificially force predictions by monkeypatching the run output

    def fake_run(output_names: Any, input_feed: Any) -> Any:
        import numpy as np

        # Return fake logits where index 1 (B-PER), 3 (B-ORG), and 5 (B-LOC) win
        # sequence length is len(input_ids)
        seq_len = len(input_feed["input_ids"][0])
        logits = np.zeros((1, seq_len, 7))
        # Set some tokens to our fake labels (skipping first and last [CLS]/[SEP])
        if seq_len > 3:
            logits[0, 1, 1] = 10.0  # B-PER
            logits[0, 2, 3] = 10.0  # B-ORG
            logits[0, 3, 5] = 10.0  # B-LOC
        return [logits]

    monkeypatch.setattr(backend._session, "run", fake_run)
    detections = backend.detect(block, policy)
    assert len(detections) >= 3
    found_types = {d.entity_type for d in detections}
    assert EntityType.PERSON in found_types
    assert EntityType.ORGANIZATION in found_types
    assert EntityType.LOCATION in found_types


def test_ml_engine_shares_one_alias_per_merged_entity(
    distilbert_artifacts: tuple[Path, Path, Path],
) -> None:
    from pseudonymize import Pseudonymizer

    config_path, tokenizer_path, model_path = distilbert_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    engine = Pseudonymizer(backends=[backend])
    result = engine.process("John Smith emailed John Smith from Seattle.")

    assert "John" not in result.text
    assert "Smith" not in result.text
    person_tokens = {
        replacement.token
        for replacement in result.replacements
        if replacement.detection.entity_type is EntityType.PERSON
    }
    assert person_tokens == {"<PERSON_1>"}


def test_ml_detect_raises_on_inference_failure(
    distilbert_artifacts: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path, tokenizer_path, model_path = distilbert_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    policy = Policy(network_policy=NetworkPolicy.DENY)
    block = ContentBlock(id="1", text="Hello John Doe", location=TextOffsetLocation(0, 14))

    # Sabotage the _session object post-loading
    backend._load_model()
    monkeypatch.setattr(backend._session, "run", lambda *args, **kwargs: 1 / 0)

    with pytest.raises(BackendExecutionError, match="ONNX PII inference failed: division by zero"):
        backend.detect(block, policy)


def test_ml_detect_raises_on_tokenizer_failure(
    distilbert_artifacts: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path, tokenizer_path, model_path = distilbert_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    policy = Policy(network_policy=NetworkPolicy.DENY)
    block = ContentBlock(id="1", text="Hello John Doe", location=TextOffsetLocation(0, 14))

    # Sabotage the _tokenizer object post-loading
    backend._load_model()
    monkeypatch.setattr(backend._tokenizer, "encode", lambda *args, **kwargs: 1 / 0)

    with pytest.raises(BackendExecutionError, match="ONNX PII inference failed: division by zero"):
        backend.detect(block, policy)
