from benchmarks.evidence_fusion import (
    arbitrate_conflicts,
    extract_candidate_evidence,
)

from pseudonymize.result import Detection, EntityType


def test_mathematically_validated_identifier_has_hard_safety_precedence() -> None:
    # A payment card validated by Luhn checksum
    card_det = Detection(
        EntityType.PAYMENT_CARD, 0, 16, 0.85, "payment_card", "algorithmic_checksum"
    )
    # An overlapping ML detection with higher raw confidence
    ml_det = Detection(EntityType.PERSON, 0, 16, 0.99, "onnx", "local_onnx_pii")

    ev_card = extract_candidate_evidence(card_det)
    ev_ml = extract_candidate_evidence(ml_det)

    assert ev_card.is_mathematically_validated
    assert not ev_ml.is_mathematically_validated

    # Card score exceeds 10.0 due to hard safety invariant
    assert ev_card.compute_fused_score() > 10.0
    assert ev_ml.compute_fused_score() < 2.0

    # Arbitration must select card over ML
    arbitrated = arbitrate_conflicts([ev_ml, ev_card])
    assert len(arbitrated) == 1
    assert arbitrated[0].detection.entity_type == EntityType.PAYMENT_CARD


def test_arbitrate_conflicts_prefers_higher_fused_evidence() -> None:
    d1 = Detection(EntityType.EMAIL, 10, 25, 0.95, "email", "rules")
    d2 = Detection(EntityType.PERSON, 10, 25, 0.60, "heuristic", "rules")

    ev1 = extract_candidate_evidence(d1, context_polarity=1.0, agreement_count=2)
    ev2 = extract_candidate_evidence(d2, context_polarity=-1.0, agreement_count=1)

    arbitrated = arbitrate_conflicts([ev2, ev1])
    assert len(arbitrated) == 1
    assert arbitrated[0].detection.entity_type == EntityType.EMAIL


def test_arbitrate_conflicts_preserves_disjoint_spans() -> None:
    d1 = Detection(EntityType.PERSON, 0, 10, 0.90, "onnx", "local_onnx_pii")
    d2 = Detection(EntityType.LOCATION, 20, 30, 0.85, "onnx", "local_onnx_pii")

    ev1 = extract_candidate_evidence(d1)
    ev2 = extract_candidate_evidence(d2)

    arbitrated = arbitrate_conflicts([ev1, ev2])
    assert len(arbitrated) == 2
    assert arbitrated[0].detection.start == 0
    assert arbitrated[1].detection.start == 20


def test_arbitrate_conflicts_empty() -> None:
    assert arbitrate_conflicts([]) == []
