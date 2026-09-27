from benchmarks.model_manifests import (
    CANDIDATE_REGISTRY,
    ModelCandidate,
    validate_candidate_manifests,
)


def test_candidate_registry_contains_active_candidates() -> None:
    assert "multilang-pii-ner-onnx-int8" in CANDIDATE_REGISTRY
    assert "multilang-pii-ner-onnx-fp32" in CANDIDATE_REGISTRY
    assert "deberta-v3-pii-ner" in CANDIDATE_REGISTRY
    assert "gliner-pii-spans" in CANDIDATE_REGISTRY
    assert "piiranha-v1" in CANDIDATE_REGISTRY


def test_candidate_piiranha_is_strictly_disqualified() -> None:
    piiranha = CANDIDATE_REGISTRY["piiranha-v1"]
    assert piiranha.disqualified
    assert not piiranha.commercial_use
    assert not piiranha.redistribution_allowed
    assert not piiranha.is_eligible_for_default()
    assert "Non-Commercial" in (piiranha.disqualification_reason or "")


def test_candidate_default_eligibility() -> None:
    incumbent = CANDIDATE_REGISTRY["multilang-pii-ner-onnx-int8"]
    assert not incumbent.disqualified
    assert incumbent.commercial_use
    assert incumbent.redistribution_allowed
    assert incumbent.is_eligible_for_default()


def test_validate_candidate_manifests_summary() -> None:
    summary = validate_candidate_manifests()
    assert summary["total_registered"] >= 5
    eligible_names = [c["name"] for c in summary["eligible"]]
    disqualified_names = [c["name"] for c in summary["disqualified"]]

    assert "multilang-pii-ner-onnx-int8" in eligible_names
    assert "piiranha-v1" in disqualified_names


def test_custom_candidate_validation() -> None:
    # Unverified / unknown lineage should not be eligible
    unknown = ModelCandidate(
        name="unknown-model",
        repo_id="test/unknown",
        revision="main",
        license="MIT",
        commercial_use=True,
        redistribution_allowed=True,
        disqualified=False,
        disqualification_reason=None,
        architecture="Transformer",
        quantization="int8",
        size_mb=100.0,
        training_lineage="unknown",
        supported_languages=("en",),
        max_sequence_length=512,
        label_map={},
        artifact_hashes={"model.onnx": "1234"},
    )
    assert not unknown.is_eligible_for_default()
