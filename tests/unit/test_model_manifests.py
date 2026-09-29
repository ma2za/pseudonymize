from benchmarks.model_manifests import (
    CANDIDATE_REGISTRY,
    ModelCandidate,
    validate_candidate_manifests,
)


def test_candidate_registry_baseline_exists() -> None:
    assert "multilang-pii-ner-onnx-int8" in CANDIDATE_REGISTRY
    baseline = CANDIDATE_REGISTRY["multilang-pii-ner-onnx-int8"]
    assert baseline.is_eligible_for_default()
    assert baseline.license == "Apache-2.0"
    assert baseline.commercial_use is True
    assert baseline.redistribution_allowed is True
    assert baseline.quantization == "int8"
    assert "config.json" in baseline.artifact_hashes


def test_disqualified_candidate_rejected() -> None:
    assert "piiranha-v1" in CANDIDATE_REGISTRY
    piiranha = CANDIDATE_REGISTRY["piiranha-v1"]
    assert not piiranha.is_eligible_for_default()
    assert piiranha.disqualified is True
    assert piiranha.disqualification_reason is not None
    assert "CC-BY-NC-ND" in piiranha.disqualification_reason


def test_candidate_with_unknown_lineage_is_ineligible() -> None:
    unknown = ModelCandidate(
        name="unknown-model",
        repo_id="org/unknown",
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
        max_sequence_length=256,
        label_map={"PER": "PERSON"},
        artifact_hashes={"model.onnx": "abc"},
    )
    assert not unknown.is_eligible_for_default()


def test_candidate_without_artifact_hashes_is_ineligible() -> None:
    no_hash = ModelCandidate(
        name="no-hash-model",
        repo_id="org/no-hash",
        revision="main",
        license="Apache-2.0",
        commercial_use=True,
        redistribution_allowed=True,
        disqualified=False,
        disqualification_reason=None,
        architecture="Transformer",
        quantization="int8",
        size_mb=100.0,
        training_lineage="Independent Corpus",
        supported_languages=("en",),
        max_sequence_length=256,
        label_map={"PER": "PERSON"},
        artifact_hashes={},
    )
    assert not no_hash.is_eligible_for_default()


def test_validate_candidate_manifests() -> None:
    summary = validate_candidate_manifests()
    assert summary["total_registered"] >= 4
    assert len(summary["eligible"]) >= 3
    assert len(summary["disqualified"]) >= 1

    eligible_names = [e["name"] for e in summary["eligible"]]
    disqualified_names = [d["name"] for d in summary["disqualified"]]

    assert "multilang-pii-ner-onnx-int8" in eligible_names
    assert "piiranha-v1" in disqualified_names
