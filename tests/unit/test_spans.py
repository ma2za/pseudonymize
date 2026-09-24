from itertools import pairwise

from pseudonymize import Detection, EntityType
from pseudonymize.spans import DETECTOR_WEIGHTS, resolve_overlaps


def test_overlap_prefers_validated_entity_then_stable_order() -> None:
    phone = Detection(EntityType.PHONE, 0, 19, 0.99, "phone")
    card = Detection(EntityType.PAYMENT_CARD, 0, 19, 1.0, "payment_card")
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
    rule_normal = Detection(EntityType.PERSON, 0, 10, 1.0, "context_id", "local_rules")
    ml_normal = Detection(EntityType.PERSON, 0, 10, 0.85, "onnx", "local_onnx_pii")
    assert resolve_overlaps([ml_normal, rule_normal]) == (rule_normal,)

    # Rule match and ML match with > 0.95 confidence -> ML wins
    rule_overridden = Detection(EntityType.PERSON, 0, 10, 1.0, "context_id", "local_rules")
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


# ---------------------------------------------------------------------------
# 1.26.0 / 1.30.0: Reconciled Ensemble Implementation & Provenance Tests
# ---------------------------------------------------------------------------


def test_detector_weights_contract() -> None:
    """Direct assertions confirming the single source of truth for detector weights."""
    assert DETECTOR_WEIGHTS["remote_provider"] == 0.50
    assert DETECTOR_WEIGHTS["remote"] == 0.50
    assert DETECTOR_WEIGHTS["coreference"] == 0.45
    assert DETECTOR_WEIGHTS["gazetteer"] == 0.55
    assert DETECTOR_WEIGHTS["context_id"] == 0.60
    assert DETECTOR_WEIGHTS["email"] == 0.90
    assert DETECTOR_WEIGHTS["payment_card"] == 1.0
    assert DETECTOR_WEIGHTS["iban"] == 1.0
    assert DETECTOR_WEIGHTS["checksum"] == 1.0
    assert DETECTOR_WEIGHTS["tabular"] == 1.0


def test_pairwise_conflict_permutation_invariance() -> None:
    """Prove that for every pairwise conflict, input order does not change the winner."""
    backend_samples = [
        # (name, detector, backend, entity_type, confidence)
        ("rule_email", "email", "rules", EntityType.EMAIL, 0.90),
        ("rule_secret", "secret", "rules", EntityType.SECRET, 0.80),
        ("rule_context", "context_id", "rules", EntityType.NATIONAL_ID, 0.88),
        ("gazetteer", "gazetteer", "gazetteer", EntityType.LOCATION, 0.85),
        ("ml_normal", "onnx", "local_onnx_pii", EntityType.PERSON, 0.85),
        ("ml_high", "onnx", "local_onnx_pii", EntityType.PERSON, 0.98),
        ("coreference", "coreference", "coreference", EntityType.PERSON, 0.90),
        ("remote", "remote_provider", "remote", EntityType.ORGANIZATION, 0.85),
    ]

    for i, a_spec in enumerate(backend_samples):
        for b_spec in backend_samples[i + 1 :]:
            # Conflict topology 1: Same span (0, 12)
            a_same = Detection(a_spec[3], 0, 12, a_spec[4], a_spec[1], a_spec[2])
            b_same = Detection(b_spec[3], 0, 12, b_spec[4], b_spec[1], b_spec[2])
            assert resolve_overlaps([a_same, b_same]) == resolve_overlaps([b_same, a_same])

            # Conflict topology 2: Partial overlap (0, 10) vs (5, 15)
            a_part = Detection(a_spec[3], 0, 10, a_spec[4], a_spec[1], a_spec[2])
            b_part = Detection(b_spec[3], 5, 15, b_spec[4], b_spec[1], b_spec[2])
            assert resolve_overlaps([a_part, b_part]) == resolve_overlaps([b_part, a_part])

            # Conflict topology 3: Nested span (0, 20) vs (4, 14)
            a_nest = Detection(a_spec[3], 0, 20, a_spec[4], a_spec[1], a_spec[2])
            b_nest = Detection(b_spec[3], 4, 14, b_spec[4], b_spec[1], b_spec[2])
            assert resolve_overlaps([a_nest, b_nest]) == resolve_overlaps([b_nest, a_nest])


def test_pairwise_precedence_hierarchy() -> None:
    # 1. Deterministic rules outrank gazetteer
    rule_det = Detection(EntityType.EMAIL, 0, 15, 0.90, "email", "rules")
    gazetteer_det = Detection(EntityType.LOCATION, 0, 15, 0.95, "gazetteer", "gazetteer")
    assert resolve_overlaps([rule_det, gazetteer_det]) == (rule_det,)

    # 2. Gazetteer outranks coreference
    gazetteer_loc = Detection(EntityType.LOCATION, 0, 10, 0.85, "gazetteer", "gazetteer")
    coref_per = Detection(EntityType.PERSON, 0, 10, 0.95, "coreference", "coreference")
    assert resolve_overlaps([gazetteer_loc, coref_per]) == (gazetteer_loc,)

    # 3. Context ID outranks coreference
    context_det = Detection(EntityType.NATIONAL_ID, 0, 10, 0.88, "context_id", "rules")
    coref_det = Detection(EntityType.PERSON, 0, 10, 0.95, "coreference", "coreference")
    assert resolve_overlaps([context_det, coref_det]) == (context_det,)

    # 4. Remote backend (weight 0.50) outranks coreference (weight 0.45) at equal confidence
    remote_det = Detection(EntityType.ORGANIZATION, 0, 15, 0.90, "remote_provider", "remote")
    coref_det2 = Detection(EntityType.PERSON, 0, 15, 0.90, "coreference", "coreference")
    assert resolve_overlaps([remote_det, coref_det2]) == (remote_det,)

    # 5. Overwhelmingly confident ML (confidence >= 0.95) outranks remote backend
    ml_high = Detection(EntityType.PERSON, 0, 15, 0.96, "onnx", "local_onnx_pii")
    remote_det2 = Detection(EntityType.ORGANIZATION, 0, 15, 0.99, "remote_provider", "remote")
    assert resolve_overlaps([ml_high, remote_det2]) == (ml_high,)

    # 6. Checksum (weight 1.0) outranks overwhelmingly confident ML
    checksum_det = Detection(EntityType.PAYMENT_CARD, 0, 15, 1.0, "payment_card", "rules")
    assert resolve_overlaps([checksum_det, ml_high]) == (checksum_det,)

    # 7. Longer span breaks tie when resolution scores are identical
    det_short = Detection(EntityType.SECRET, 5, 10, 0.80, "secret", "rules")
    det_long = Detection(EntityType.SECRET, 0, 15, 0.80, "secret", "rules")
    assert resolve_overlaps([det_short, det_long]) == (det_long,)


def test_detector_priority_override_and_adjacency_contract() -> None:
    # Caller-specified detector_priority breaks tie when resolution scores are equal
    # Both "location" and "remote_provider" have weight 0.50
    det_a = Detection(EntityType.LOCATION, 0, 10, 0.80, "location", "rules")
    det_b = Detection(EntityType.ORGANIZATION, 0, 10, 0.80, "remote_provider", "remote")
    # By default, equal score and equal priority falls back to span length / start / detector name
    # "location" comes before "remote_provider" alphabetically when all else equal
    assert resolve_overlaps([det_a, det_b]) == (det_a,)
    # With detector_priority, remote_provider breaks the tie and wins
    assert resolve_overlaps([det_a, det_b], detector_priority=("remote_provider",)) == (det_b,)

    # Exact contiguous adjacency merges only identical entity types with 0-gap
    span1 = Detection(EntityType.PERSON, 0, 5, 0.85, "onnx", "local_onnx_pii")
    span2 = Detection(EntityType.PERSON, 5, 10, 0.90, "onnx", "local_onnx_pii")
    merged = resolve_overlaps([span1, span2])
    assert len(merged) == 1
    assert merged[0].start == 0 and merged[0].end == 10
    assert merged[0].detector == "ensemble"

    # Adjacent spans of DIFFERENT entity types must NOT merge
    span_diff = Detection(EntityType.LOCATION, 5, 10, 0.90, "gazetteer", "gazetteer")
    unmerged_diff = resolve_overlaps([span1, span_diff])
    assert len(unmerged_diff) == 2

    # Spans with gap > 0 must NOT merge
    span_gap = Detection(EntityType.PERSON, 6, 11, 0.90, "onnx", "local_onnx_pii")
    unmerged_gap = resolve_overlaps([span1, span_gap])
    assert len(unmerged_gap) == 2
