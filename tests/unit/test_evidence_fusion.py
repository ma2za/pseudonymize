from benchmarks.evidence_fusion import (
    arbitrate_conflicts,
    extract_candidate_evidence,
)

from pseudonymize.result import Detection, EntityType


def test_hard_safety_precedence_dominates_ml() -> None:
    # Mathematically validated checksum candidate with moderate confidence
    validated_det = Detection(
        entity_type=EntityType.IBAN,
        start=0,
        end=20,
        confidence=0.85,
        detector="algorithmic_checksum",
    )
    validated_evidence = extract_candidate_evidence(validated_det)
    assert validated_evidence.is_mathematically_validated is True

    # High-confidence ML detection overlapping the exact same span
    ml_det = Detection(
        entity_type=EntityType.ORGANIZATION,
        start=0,
        end=20,
        confidence=0.99,
        detector="ml_onnx",
    )
    ml_evidence = extract_candidate_evidence(ml_det)
    assert ml_evidence.is_mathematically_validated is False

    # Fused score for validated must exceed 10.0 and easily beat ML
    assert validated_evidence.compute_fused_score() > 10.0
    assert ml_evidence.compute_fused_score() < 5.0

    # Arbitration must select the validated identifier
    resolved = arbitrate_conflicts([ml_evidence, validated_evidence])
    assert len(resolved) == 1
    assert resolved[0].detection.entity_type == EntityType.IBAN
    assert resolved[0].detection.detector == "algorithmic_checksum"


def test_context_polarity_influences_score() -> None:
    det = Detection(
        entity_type=EntityType.PHONE,
        start=10,
        end=20,
        confidence=0.80,
        detector="phone",
    )

    pos_evidence = extract_candidate_evidence(det, context_polarity=1.0)
    neg_evidence = extract_candidate_evidence(det, context_polarity=-1.0)

    assert pos_evidence.compute_fused_score() > neg_evidence.compute_fused_score()


def test_arbitrate_non_overlapping_spans() -> None:
    det1 = Detection(
        entity_type=EntityType.EMAIL,
        start=0,
        end=15,
        confidence=0.95,
        detector="email",
    )
    det2 = Detection(
        entity_type=EntityType.PHONE,
        start=20,
        end=32,
        confidence=0.85,
        detector="phone",
    )

    ev1 = extract_candidate_evidence(det1)
    ev2 = extract_candidate_evidence(det2)

    resolved = arbitrate_conflicts([ev2, ev1])  # passed in reverse order
    assert len(resolved) == 2
    # Output must be ordered by start offset
    assert resolved[0].detection.start == 0
    assert resolved[1].detection.start == 20


def test_arbitrate_conflicts_empty() -> None:
    assert arbitrate_conflicts([]) == []
