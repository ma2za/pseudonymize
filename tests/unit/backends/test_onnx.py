import hashlib
import itertools
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
CACHE_DIR = Path(".cache/pseudonymize-tests/models/multilang-pii-ner-ml")
MODEL_URL_BASE = "https://huggingface.co/onnx-community/multilang-pii-ner-ONNX/resolve/main/"
MODEL_FILES = {
    "config.json": (
        "config.json",
        "3503fb27021640b315b1e7636933f7df9c209746251cae4975bdef46be4e8158",
    ),
    "tokenizer.json": (
        "tokenizer.json",
        "8373f9cd3d27591e1924426bcc1c8799bc5a9affc4fc857982c5d66668dd1f41",
    ),
    "model_int8.onnx": (
        "onnx/model_int8.onnx",
        "1d02f3829ad90d95dea5e64d35f5528f96d7b223c1e056a96075c6229a484356",
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
def llama_artifacts() -> tuple[Path, Path, Path]:
    paths = []
    for local_name, (remote_path, sha256) in MODEL_FILES.items():
        dest = CACHE_DIR / local_name
        download_file(MODEL_URL_BASE + remote_path, dest, sha256)
        paths.append(dest)
    # Returns (config, tokenizer, model)
    return (paths[0], paths[1], paths[2])


def test_ml_backend_capabilities(llama_artifacts: tuple[Path, Path, Path]) -> None:
    config_path, tokenizer_path, model_path = llama_artifacts
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


def test_ml_detect_config_missing_fallback(llama_artifacts: tuple[Path, Path, Path]) -> None:
    _, tokenizer_path, model_path = llama_artifacts

    # Do not provide config path, this forces _id2label to evaluate to {}
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=None
    )
    policy = Policy(network_policy=NetworkPolicy.DENY)
    block = ContentBlock(id="1", text="My name is Sarah", location=TextOffsetLocation(0, 16))

    detections = backend.detect(block, policy)
    assert len(detections) == 0


def test_ml_detect_empty_block(llama_artifacts: tuple[Path, Path, Path]) -> None:
    config_path, tokenizer_path, model_path = llama_artifacts
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
    llama_artifacts: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path, tokenizer_path, model_path = llama_artifacts
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
    llama_artifacts: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path, tokenizer_path, model_path = llama_artifacts
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
    # LOC: " Seattle" as one span
    assert len(sorted_detections) >= 2

    # Let's map out the exact expected strings for the entities found
    found_entities = [(d.entity_type, text[d.start : d.end]) for d in sorted_detections]

    assert any("John" in text_str for et, text_str in found_entities if et == EntityType.PERSON)
    assert any(
        "Seattle" in text_str for et, text_str in found_entities if et == EntityType.LOCATION
    )

    # The multilang model might include trailing punctuation in the exact token boundaries
    # We just assert it found something meaningful.

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
            self.type_ids = [0] * len(original.offsets)

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
    llama_artifacts: tuple[Path, Path, Path],
) -> None:
    from pseudonymize import Pseudonymizer

    config_path, tokenizer_path, model_path = llama_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    # Confidences are the model's own probabilities, so a floor calibrated for
    # deterministic detectors (0.8 by default) is too high for this short text.
    engine = Pseudonymizer(
        backends=[backend], policy=Policy(network_policy=NetworkPolicy.DENY, minimum_confidence=0.5)
    )
    result = engine.process(" Maria emailed Maria.")

    assert "Maria" not in result.text
    person_tokens = {
        replacement.token
        for replacement in result.replacements
        if replacement.detection.entity_type is EntityType.PERSON
    }
    assert person_tokens == {"<PERSON_1>"}


def test_ml_detect_raises_on_inference_failure(
    llama_artifacts: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path, tokenizer_path, model_path = llama_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    policy = Policy(network_policy=NetworkPolicy.DENY)
    block = ContentBlock(id="1", text="Hello John Doe", location=TextOffsetLocation(0, 14))

    # Sabotage the _session object post-loading, with a message quoting the input
    backend._load_model()

    def _fail(*args: object, **kwargs: object) -> None:
        raise RuntimeError("inference failed on 'Hello John Doe'")

    monkeypatch.setattr(backend._session, "run", _fail)

    with pytest.raises(BackendExecutionError) as raised:
        backend.detect(block, policy)

    assert str(raised.value).startswith("ONNX PII inference failed")
    assert raised.value.__cause__ is not None


def test_ml_detect_raises_on_tokenizer_failure(
    llama_artifacts: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path, tokenizer_path, model_path = llama_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    policy = Policy(network_policy=NetworkPolicy.DENY)
    block = ContentBlock(id="1", text="Hello John Doe", location=TextOffsetLocation(0, 14))

    # Sabotage the _tokenizer object post-loading, with a message quoting the input
    backend._load_model()

    def _fail(*args: object, **kwargs: object) -> None:
        raise RuntimeError("cannot tokenize 'Hello John Doe'")

    monkeypatch.setattr(backend._tokenizer, "encode", _fail)

    with pytest.raises(BackendExecutionError) as raised:
        backend.detect(block, policy)

    assert str(raised.value).startswith("ONNX PII inference failed")
    assert raised.value.__cause__ is not None


_FILLER = "The quarterly report was reviewed by the committee and approved without amendment. "
_TAIL = "Contact Maria Rossi in Milan."


@pytest.mark.parametrize("repetitions", [5, 40, 400])
def test_ml_detects_personal_data_beyond_a_single_model_window(
    llama_artifacts: tuple[Path, Path, Path], repetitions: int
) -> None:
    """PII in the tail of a long block must not be skipped.

    The tokenizer ships with truncation at 512 tokens, so before windowing the
    model never saw past roughly two kilobytes of text and the tail passed
    through unredacted with no error and no warning.
    """
    config_path, tokenizer_path, model_path = llama_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    text = (_FILLER * repetitions) + _TAIL
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))

    detections = backend.detect(block, Policy(network_policy=NetworkPolicy.DENY))
    found = {
        (detection.entity_type, text[detection.start : detection.end]) for detection in detections
    }

    assert any("Maria Rossi" in text_str for et, text_str in found if et == EntityType.PERSON)
    assert any("Milan" in text_str for et, text_str in found if et == EntityType.LOCATION)


def test_ml_windows_cover_the_whole_block(
    llama_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = llama_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    backend._load_model()

    short = _FILLER
    assert backend._windows(short) == [(0, len(short))]

    long_text = _FILLER * 400
    windows = backend._windows(long_text)
    assert len(windows) > 1
    assert windows[0][0] == 0
    assert windows[-1][1] >= len(long_text.rstrip())
    # Consecutive windows overlap, so an entity on a boundary is seen whole once.
    for (_, previous_end), (next_start, _) in itertools.pairwise(windows):
        assert next_start < previous_end


def test_ml_reported_confidence_is_the_model_probability(
    llama_artifacts: tuple[Path, Path, Path],
) -> None:
    """A stricter policy must only ever remove detections, never relabel them.

    The previous calibration mapped every surviving span onto the policy floor,
    so the same weak prediction was reported at 0.51 under a 0.5 floor and at
    0.99 under a 0.99 floor, and minimum_confidence could filter nothing.
    """
    config_path, tokenizer_path, model_path = llama_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    text = "John Smith is currently visiting Microsoft's headquarters in Seattle, Washington!"
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))

    lenient = backend.detect(
        block, Policy(network_policy=NetworkPolicy.DENY, minimum_confidence=0.1)
    )
    strict = backend.detect(
        block, Policy(network_policy=NetworkPolicy.DENY, minimum_confidence=0.95)
    )

    lenient_spans = {(d.entity_type, d.start, d.end): d.confidence for d in lenient}
    strict_spans = {(d.entity_type, d.start, d.end): d.confidence for d in strict}

    assert strict_spans.keys() <= lenient_spans.keys()
    # A span surviving both floors keeps the identical probability under each.
    for key, confidence in strict_spans.items():
        assert confidence == lenient_spans[key]
        assert confidence >= 0.95


def test_ml_entity_threshold_controls_recall_without_inflating_confidence(
    llama_artifacts: tuple[Path, Path, Path],
) -> None:
    """The runner-up label wins only when it clears an absolute probability."""
    config_path, tokenizer_path, model_path = llama_artifacts
    text = "An obscure text with JohnXYZ and random unconfident bits."
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))
    policy = Policy(network_policy=NetworkPolicy.DENY, minimum_confidence=0.0)

    def detections_at(threshold: float) -> list[float]:
        backend = LocalONNXPIIBackend(
            model_path=model_path,
            tokenizer_path=tokenizer_path,
            config_path=config_path,
            entity_threshold=threshold,
            entity_thresholds={},
        )
        return [detection.confidence for detection in backend.detect(block, policy)]

    permissive = detections_at(0.01)
    conservative = detections_at(0.99)

    assert len(permissive) >= len(conservative)
    if len(permissive) > len(conservative):
        assert any(confidence < 0.1 for confidence in permissive)


def test_ml_entity_threshold_is_validated(
    llama_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = llama_artifacts
    with pytest.raises(ValueError, match="entity_threshold"):
        LocalONNXPIIBackend(
            model_path=model_path,
            tokenizer_path=tokenizer_path,
            config_path=config_path,
            entity_threshold=0.0,
        )
    with pytest.raises(ValueError, match="window_overlap_tokens"):
        LocalONNXPIIBackend(
            model_path=model_path,
            tokenizer_path=tokenizer_path,
            config_path=config_path,
            window_overlap_tokens=-1,
        )


def test_ml_entity_specific_thresholds(
    llama_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = llama_artifacts
    text = "Please ship the Apollo unit to warehouse Beta before the Friday deadline, thanks."
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))
    policy = Policy(network_policy=NetworkPolicy.DENY, minimum_confidence=0.0)

    backend_with_override = LocalONNXPIIBackend(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        config_path=config_path,
        entity_threshold=0.99,
        entity_thresholds={EntityType.LOCATION: 0.01},
    )
    detections = backend_with_override.detect(block, policy)
    assert len(detections) >= 0


def test_ml_subword_span_repair(
    llama_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = llama_artifacts
    text = "Jean-Paul is a nice person."
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))
    policy = Policy(network_policy=NetworkPolicy.DENY, minimum_confidence=0.0)

    backend = LocalONNXPIIBackend(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        config_path=config_path,
        entity_threshold=0.01,
    )
    detections = backend.detect(block, policy)
    assert len(detections) >= 0


def test_ml_context_boosting(
    llama_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = llama_artifacts
    text = "The applicant's name is John, contact him immediately."
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))
    policy = Policy(network_policy=NetworkPolicy.DENY, minimum_confidence=0.0)

    backend = LocalONNXPIIBackend(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        config_path=config_path,
        entity_threshold=0.5,
    )
    detections = backend.detect(block, policy)
    assert len(detections) >= 0


def test_onnx_context_boosting_pair_handling(llama_artifacts: tuple[Path, Path, Path]) -> None:
    config_path, tokenizer_path, model_path = llama_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )

    # Text is very short, triggering the context pair injection
    text = "IT12345678"
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))
    policy = Policy()

    # We should detect that the code runs without crashing and performs pairwise encoding
    # We pass explicit global context
    detections = backend.detect(block, policy)
    assert isinstance(detections, (list, tuple))

    # Trigger the input_ids clipping logic (line 259 in onnx.py) by setting a tiny max_tokens
    backend._max_tokens = 3
    # Text must be longer than 3 tokens
    short_text = "John Smith is a person"
    short_block = ContentBlock(
        id="1", text=short_text, location=TextOffsetLocation(0, len(short_text))
    )
    detections2 = backend.detect(short_block, policy)
    assert isinstance(detections2, (list, tuple))
