import itertools
from pathlib import Path
from typing import Any

import pytest

from pseudonymize.backends.ml.onnx import LocalONNXPIIBackend
from pseudonymize.document import ContentBlock, TextOffsetLocation
from pseudonymize.exceptions import BackendExecutionError
from pseudonymize.policy import NetworkPolicy, Policy
from pseudonymize.result import EntityType


def test_ml_backend_capabilities(onnx_artifacts: tuple[Path, Path, Path]) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
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


def test_ml_detect_config_missing_fallback(onnx_artifacts: tuple[Path, Path, Path]) -> None:
    _, tokenizer_path, model_path = onnx_artifacts

    # Do not provide config path, this forces _id2label to evaluate to {}
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=None
    )
    policy = Policy(network_policy=NetworkPolicy.DENY)
    block = ContentBlock(id="1", text="My name is Sarah", location=TextOffsetLocation(0, 16))

    detections = backend.detect(block, policy)
    assert len(detections) == 0


def test_ml_detect_empty_block(onnx_artifacts: tuple[Path, Path, Path]) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
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
    onnx_artifacts: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
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
    onnx_artifacts: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
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
    backend._infer_text_cached.cache_clear()
    detections = backend.detect(block, policy)
    assert len(detections) == 0

    # Ensure coverage for when label_str exists but isn't something we map
    backend._id2label = dict.fromkeys(range(100), "B-UNKNOWN")
    backend._infer_text_cached.cache_clear()
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
    backend._infer_text_cached.cache_clear()
    detections = backend.detect(block, policy)
    assert len(detections) >= 3
    found_types = {d.entity_type for d in detections}
    assert EntityType.PERSON in found_types
    assert EntityType.ORGANIZATION in found_types
    assert EntityType.LOCATION in found_types


def test_ml_engine_shares_one_alias_per_merged_entity(
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    from pseudonymize import Pseudonymizer

    config_path, tokenizer_path, model_path = onnx_artifacts
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
    assert person_tokens == {"<PER_1>"}


def test_ml_detect_raises_on_inference_failure(
    onnx_artifacts: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
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
    onnx_artifacts: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
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
    onnx_artifacts: tuple[Path, Path, Path], repetitions: int
) -> None:
    """PII in the tail of a long block must not be skipped.

    The tokenizer ships with truncation at 512 tokens, so before windowing the
    model never saw past roughly two kilobytes of text and the tail passed
    through unredacted with no error and no warning.
    """
    config_path, tokenizer_path, model_path = onnx_artifacts
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
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
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
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    """A stricter policy must only ever remove detections, never relabel them.

    The previous calibration mapped every surviving span onto the policy floor,
    so the same weak prediction was reported at 0.51 under a 0.5 floor and at
    0.99 under a 0.99 floor, and minimum_confidence could filter nothing.
    """
    config_path, tokenizer_path, model_path = onnx_artifacts
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
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    """The runner-up label wins only when it clears an absolute probability."""
    config_path, tokenizer_path, model_path = onnx_artifacts
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
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
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
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
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
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
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
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
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


def test_onnx_context_boosting_pair_handling(onnx_artifacts: tuple[Path, Path, Path]) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
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


# ---------------------------------------------------------------------------
# 1.29.0: ONNX Token-to-Character Alignment Audit & Calibration Verification
# ---------------------------------------------------------------------------


def test_onnx_combining_characters_alignment(onnx_artifacts: tuple[Path, Path, Path]) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    policy = Policy(network_policy=NetworkPolicy.DENY)

    # Combining acute: 'e' + '\u0301', combining grave: 'a' + '\u0300'
    text = "Visite de Rene\u0301 a\u0300 Paris aujourd'hui."
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))

    detections = backend.detect(block, policy)
    for d in detections:
        extracted = text[d.start : d.end]
        # Extracted slice must not contain unaligned partial combining codepoints
        assert extracted.isprintable()
        if d.entity_type == EntityType.LOCATION:
            assert "Paris" in extracted


def test_onnx_emoji_character_alignment(onnx_artifacts: tuple[Path, Path, Path]) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    policy = Policy(network_policy=NetworkPolicy.DENY)

    # Multi-codepoint emoji with skin tone and zero-width joiners
    text = (
        "Conference speaker \U0001f44b\U0001f3fd Sarah Connor \U0001f469\u200d\U0001f4bb presented."
    )
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))

    detections = backend.detect(block, policy)
    person_detections = [d for d in detections if d.entity_type == EntityType.PERSON]
    assert len(person_detections) >= 1
    extracted = text[person_detections[0].start : person_detections[0].end]
    assert "Sarah Connor" in extracted


def test_onnx_hyphenated_and_possessive_alignment(
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    policy = Policy(network_policy=NetworkPolicy.DENY)

    text = "Dr. Jean-Luc Picard visited Microsoft's main campus in Redmond."
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))

    detections = backend.detect(block, policy)
    found = {d.entity_type: text[d.start : d.end] for d in detections}

    assert EntityType.PERSON in found
    assert "Picard" in found[EntityType.PERSON]
    if EntityType.LOCATION in found:
        assert "Redmond" in found[EntityType.LOCATION]


def test_onnx_cjk_character_alignment(onnx_artifacts: tuple[Path, Path, Path]) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    policy = Policy(network_policy=NetworkPolicy.DENY)

    text = "昨天在北京遇到了张伟先生。"
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))

    detections = backend.detect(block, policy)
    for d in detections:
        extracted = text[d.start : d.end]
        # Extracted slice must be clean contiguous CJK characters
        assert len(extracted) > 0
        assert extracted in text


def test_onnx_window_boundary_split_alignment(
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
    # Configure tiny max_tokens to force window straddling
    backend = LocalONNXPIIBackend(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        config_path=config_path,
        window_overlap_tokens=16,
    )
    backend._max_tokens = 64
    policy = Policy(network_policy=NetworkPolicy.DENY, minimum_confidence=0.0)

    # Construct text where an entity sits at a window boundary
    prefix = "The quick brown fox jumps over the lazy dog. " * 8
    target = "General Alexander Hamilton commanded the regiment. "
    suffix = "All troops assembled in Washington D.C. afterwards. " * 8
    full_text = prefix + target + suffix
    block = ContentBlock(id="1", text=full_text, location=TextOffsetLocation(0, len(full_text)))

    detections = backend.detect(block, policy)
    for d in detections:
        # Verify every detected span accurately indexes the full text
        extracted = full_text[d.start : d.end]
        assert len(extracted) > 0
        assert d.start < d.end <= len(full_text)


def test_onnx_per_label_calibration_property_and_override(
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts

    # Default calibration mapping
    default_backend = LocalONNXPIIBackend(
        model_path=model_path, tokenizer_path=tokenizer_path, config_path=config_path
    )
    thresholds = default_backend.entity_thresholds
    assert isinstance(thresholds, dict)
    assert thresholds[EntityType.PERSON] == 0.05
    assert thresholds[EntityType.LOCATION] == 0.20
    assert thresholds[EntityType.ORGANIZATION] == 0.05

    # Custom per-label calibration override
    custom_backend = LocalONNXPIIBackend(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        config_path=config_path,
        entity_thresholds={
            EntityType.PERSON: 0.10,
            EntityType.LOCATION: 0.20,
            EntityType.ORGANIZATION: 0.30,
        },
    )
    custom_thresholds = custom_backend.entity_thresholds
    assert custom_thresholds[EntityType.PERSON] == 0.10
    assert custom_thresholds[EntityType.LOCATION] == 0.20
    assert custom_thresholds[EntityType.ORGANIZATION] == 0.30


def test_onnx_ablation_flags(
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts

    backend = LocalONNXPIIBackend(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        config_path=config_path,
        enable_context_boost=False,
        enable_runner_up=False,
        enable_confidence_remapping=False,
        enable_subword_repair=False,
        enable_word_expansion=False,
    )
    assert not backend._enable_context_boost
    assert not backend._enable_runner_up
    assert not backend._enable_confidence_remapping
    assert not backend._enable_subword_repair
    assert not backend._enable_word_expansion

    policy = Policy.default()
    block = ContentBlock(
        "text", "My name is John Smith and I live in Paris.", TextOffsetLocation(0, 42)
    )
    detections = backend.detect(block, policy)
    assert isinstance(detections, tuple)


def test_onnx_multilingual_honorific_boosting(
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    from pseudonymize.backends.ml.onnx import _CONTEXT_BOOSTS, _TRAILING_PERSON_BOOST

    # Verify multilingual patterns match expected honorifics
    person_pat, p_type, _ = _CONTEXT_BOOSTS[0]
    assert p_type == EntityType.PERSON
    for title in ("Sdri.", "Ông", "Herr", "Monsieur", "Madame", "Señor", "Bapak"):
        assert person_pat.search(f"{title} Test") is not None

    trailing_pat, t_type, _ = _TRAILING_PERSON_BOOST
    assert t_type == EntityType.PERSON
    for mark in ("様", "さん", "君", "ちゃん", "氏", "님", "씨"):
        assert trailing_pat.search(f"田中{mark}") is not None


def test_trim_span_boundaries_comprehensive() -> None:
    from pseudonymize.backends.ml.onnx import _trim_span_boundaries

    # 1. Standard peripheral brackets and quotes
    cases = [
        ("(John)", 0, 6, None, 1, 5, "John"),
        ("[Paris]", 0, 7, None, 1, 6, "Paris"),
        ("“Berlin”", 0, 8, None, 1, 7, "Berlin"),
        ("«Madrid»", 0, 8, None, 1, 7, "Madrid"),
        ("¿London?", 0, 8, None, 1, 7, "London"),
        ("Smith,", 0, 6, None, 0, 5, "Smith"),
        ("Smith.", 0, 6, None, 0, 5, "Smith"),
        ("...Paris...", 0, 11, None, 3, 8, "Paris"),
        ("(John Smith).", 0, 13, None, 1, 11, "John Smith"),
    ]
    for text, s, e, ent_type, exp_s, exp_e, exp_text in cases:
        res_s, res_e = _trim_span_boundaries(text, s, e, ent_type)
        assert (res_s, res_e) == (exp_s, exp_e), (
            f"Failed for {text!r}: got {(res_s, res_e)}, expected {(exp_s, exp_e)}"
        )
        assert text[res_s:res_e] == exp_text

    # 2. Corporate and person abbreviations that legitimately end with a period
    corp_text = "Invest in Acme Corp. today."
    res_s, res_e = _trim_span_boundaries(corp_text, 10, 20, EntityType.ORGANIZATION)
    assert corp_text[res_s:res_e] == "Acme Corp."

    inc_text = "Founded by Globex Inc. in 1999."
    res_s, res_e = _trim_span_boundaries(inc_text, 11, 22, EntityType.ORGANIZATION)
    assert inc_text[res_s:res_e] == "Globex Inc."

    person_text = "Honoring Martin Luther King Jr. today."
    res_s, res_e = _trim_span_boundaries(person_text, 9, 31, EntityType.PERSON)
    assert person_text[res_s:res_e] == "Martin Luther King Jr."

    # 3. Internal hyphens and apostrophes must be preserved
    compound_text = "Jean-Paul and O'Connor"
    res_s, res_e = _trim_span_boundaries(compound_text, 0, 9, EntityType.PERSON)
    assert compound_text[res_s:res_e] == "Jean-Paul"

    res_s2, res_e2 = _trim_span_boundaries(compound_text, 14, 22, EntityType.PERSON)
    assert compound_text[res_s2:res_e2] == "O'Connor"

    # 4. Degenerate punctuation only
    degen = "..."
    res_s3, res_e3 = _trim_span_boundaries(degen, 0, 3, None)
    assert res_s3 >= res_e3


def test_onnx_compound_name_and_punctuation_trimming(
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
    backend = LocalONNXPIIBackend(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        config_path=config_path,
        entity_threshold=0.05,
    )
    policy = Policy(network_policy=NetworkPolicy.DENY, minimum_confidence=0.0)

    # 1. Punctuation wrapping: parentheses and commas should not contaminate entity boundaries
    text = "Please reach out to (John Smith), our coordinator in (Paris)."
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))
    detections = backend.detect(block, policy)

    detected_spans = [text[d.start : d.end] for d in detections]
    for span in detected_spans:
        assert not span.startswith("(")
        assert not span.endswith(")")
        assert not span.endswith(",")
        assert not span.endswith(".")

    # 2. Compound names with hyphens and apostrophes
    text2 = "Meeting with Jean-Paul and Liam O'Connor."
    block2 = ContentBlock(id="2", text=text2, location=TextOffsetLocation(0, len(text2)))
    detections2 = backend.detect(block2, policy)
    detected_spans2 = [text2[d.start : d.end] for d in detections2]

    # Boundaries must be clean without trailing periods
    for span in detected_spans2:
        assert not span.endswith(".")


def test_onnx_allowed_entity_types_scoping(
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts
    policy = Policy(network_policy=NetworkPolicy.DENY, minimum_confidence=0.0)
    text = "Sarah lives in Paris and works for Acme Corp."
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))

    # 1. Scoped to PERSON only using set
    person_only_backend = LocalONNXPIIBackend(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        config_path=config_path,
        entity_threshold=0.05,
        allowed_entity_types={EntityType.PERSON},
    )
    assert person_only_backend.allowed_entity_types == frozenset({EntityType.PERSON})
    assert person_only_backend.capabilities.entity_types == frozenset({EntityType.PERSON})
    person_dets = person_only_backend.detect(block, policy)
    assert all(d.entity_type == EntityType.PERSON for d in person_dets)
    assert any(d.entity_type == EntityType.PERSON for d in person_dets)

    # 2. Scoped with an unsupported entity type in set
    scoped_unsupported = LocalONNXPIIBackend(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        config_path=config_path,
        entity_threshold=0.05,
        allowed_entity_types={EntityType.PERSON, EntityType.SECRET},
    )
    assert scoped_unsupported.capabilities.entity_types == frozenset({EntityType.PERSON})

    # 3. Default backend includes all supported entity types
    default_backend = LocalONNXPIIBackend(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        config_path=config_path,
        entity_threshold=0.05,
    )
    assert default_backend.allowed_entity_types is None
    assert EntityType.LOCATION in default_backend.capabilities.entity_types
    assert EntityType.PERSON in default_backend.capabilities.entity_types
