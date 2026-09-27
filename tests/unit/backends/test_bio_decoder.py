from pathlib import Path

import pytest

from pseudonymize.backends.ml.onnx import (
    LocalONNXPIIBackend,
    _aggregate_confidences,
)
from pseudonymize.document import ContentBlock, TextOffsetLocation
from pseudonymize.policy import Policy
from pseudonymize.result import EntityType


def test_aggregate_confidences_modes() -> None:
    confs = [0.80, 0.90, 0.70]
    assert _aggregate_confidences(confs, "max") == 0.90
    assert pytest.approx(_aggregate_confidences(confs, "mean"), abs=1e-5) == 0.80
    assert _aggregate_confidences(confs, "min") == 0.70

    # Geometric mean: (0.8 * 0.9 * 0.7) ** (1/3) = (0.504) ** (1/3) ~ 0.7958
    assert pytest.approx(_aggregate_confidences(confs, "geometric_mean"), abs=1e-3) == 0.7958

    # Degenerate empty
    assert _aggregate_confidences([], "max") == 0.0


def test_onnx_backend_decoder_validation(tmp_path: Path) -> None:
    fake_model = tmp_path / "model.onnx"
    fake_tokenizer = tmp_path / "tokenizer.json"
    fake_model.write_text("model", encoding="utf-8")
    fake_tokenizer.write_text("{}", encoding="utf-8")

    with pytest.raises(ValueError, match="Unknown decoder_mode"):
        LocalONNXPIIBackend(
            model_path=fake_model,
            tokenizer_path=fake_tokenizer,
            decoder_mode="invalid_decoder",
        )

    with pytest.raises(ValueError, match="Unknown span_aggregator"):
        LocalONNXPIIBackend(
            model_path=fake_model,
            tokenizer_path=fake_tokenizer,
            span_aggregator="invalid_aggregator",
        )

    with pytest.raises(ValueError, match="temperature must be positive"):
        LocalONNXPIIBackend(
            model_path=fake_model,
            tokenizer_path=fake_tokenizer,
            temperature=-1.0,
        )


def test_onnx_backend_constrained_bio_decoding(
    onnx_artifacts: tuple[Path, Path, Path],
) -> None:
    config_path, tokenizer_path, model_path = onnx_artifacts

    backend_legacy = LocalONNXPIIBackend(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        config_path=config_path,
        decoder_mode="legacy",
        span_aggregator="max",
    )
    backend_bio = LocalONNXPIIBackend(
        model_path=model_path,
        tokenizer_path=tokenizer_path,
        config_path=config_path,
        decoder_mode="constrained_bio",
        span_aggregator="mean",
        temperature=1.1,
    )

    assert backend_legacy.temperature == 1.0
    assert backend_legacy.decoder_mode == "legacy"
    assert backend_legacy.span_aggregator == "max"

    assert backend_bio.temperature == 1.1
    assert backend_bio.decoder_mode == "constrained_bio"
    assert backend_bio.span_aggregator == "mean"

    policy = Policy.default()
    block = ContentBlock(
        "text",
        "My name is John Smith and I live in Paris.",
        TextOffsetLocation(0, 42),
    )

    det_legacy = backend_legacy.detect(block, policy)
    det_bio = backend_bio.detect(block, policy)

    assert isinstance(det_legacy, tuple)
    assert isinstance(det_bio, tuple)

    # Both modes detect John Smith
    person_legacy = [d for d in det_legacy if d.entity_type == EntityType.PERSON]
    person_bio = [d for d in det_bio if d.entity_type == EntityType.PERSON]
    assert len(person_legacy) >= 1
    assert len(person_bio) >= 1
    assert person_bio[0].start == person_legacy[0].start
    assert person_bio[0].end == person_legacy[0].end
