from itertools import pairwise

from pseudonymize import Detection, EntityType
from pseudonymize.spans import resolve_overlaps


def test_overlap_prefers_validated_entity_then_stable_order() -> None:
    phone = Detection(EntityType.PHONE, 0, 19, 0.99, "phone")
    card = Detection(EntityType.PAYMENT_CARD, 0, 19, 1.0, "card")
    email = Detection(EntityType.EMAIL, 30, 40, 0.9, "email")
    assert resolve_overlaps([phone, email, card]) == (card, email)


def test_url_credential_outranks_overlapping_email() -> None:
    # In "https://alice:s3cret@host.example" the password plus host also match
    # the email pattern; the credential span must win or "alice:" leaks.
    credential = Detection(EntityType.URL_CREDENTIAL, 8, 20, 1.0, "url")
    email = Detection(EntityType.EMAIL, 14, 32, 0.99, "email")
    assert resolve_overlaps([email, credential]) == (credential,)


def test_configured_priority_breaks_equal_rank() -> None:
    first = Detection(EntityType.SECRET, 0, 10, 0.9, "first")
    second = Detection(EntityType.SECRET, 5, 15, 0.9, "second")
    assert resolve_overlaps([first, second], ("second", "first")) == (second,)


def test_dense_overlaps_yield_disjoint_and_maximal_selection() -> None:
    detections = [
        Detection(EntityType.EMAIL, start, start + length, 0.9, f"detector-{start}-{length}")
        for start in range(0, 60, 3)
        for length in (2, 5, 9)
    ]
    result = resolve_overlaps(detections)
    assert all(left.end <= right.start for left, right in pairwise(result))
    for detection in detections:
        assert detection in result or any(
            detection.start < kept.end and kept.start < detection.end for kept in result
        )


def test_rules_outrank_ml_unless_ml_highly_confident() -> None:
    # Rule match and ML match with normal confidence -> Rule wins
    rule_normal = Detection(EntityType.PERSON, 0, 10, 1.0, "context", "local_rules")
    ml_normal = Detection(EntityType.PERSON, 0, 10, 0.85, "onnx", "local_onnx_pii")
    assert resolve_overlaps([ml_normal, rule_normal]) == (rule_normal,)

    # Rule match and ML match with > 0.95 confidence -> ML wins
    rule_overridden = Detection(EntityType.PERSON, 0, 10, 1.0, "context", "local_rules")
    ml_high = Detection(EntityType.PERSON, 0, 10, 0.96, "onnx", "local_onnx_pii")
    assert resolve_overlaps([ml_high, rule_overridden]) == (ml_high,)

def test_adjacent_same_type_spans_are_merged() -> None:
    d1 = Detection(EntityType.PERSON, 0, 10, 0.8, "onnx", "local_onnx_pii")
    d2 = Detection(EntityType.PERSON, 10, 20, 0.9, "onnx", "local_onnx_pii")
    # Gap is 0 (strictly adjacent), they should merge
    merged = resolve_overlaps([d1, d2])
    assert len(merged) == 1
    assert merged[0].start == 0
    assert merged[0].end == 20
    assert merged[0].confidence == 0.9
    assert merged[0].backend == "ensemble_merger"
    assert merged[0].detector == "ensemble"

    # Gap is > 0, they should NOT merge
    d3 = Detection(EntityType.PERSON, 0, 10, 0.8, "onnx", "local_onnx_pii")
    d4 = Detection(EntityType.PERSON, 11, 20, 0.9, "onnx", "local_onnx_pii")
    unmerged = resolve_overlaps([d3, d4])
    assert len(unmerged) == 2
