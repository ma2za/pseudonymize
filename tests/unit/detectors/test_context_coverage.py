from pseudonymize.detectors.context import ContextualIdDetector


def test_context_detector_skips_unknown_punctuation() -> None:
    assert ContextualIdDetector().detect("Passport No $ X1234567 was issued.")


def test_context_detector_dependency_links_and_exhaustion() -> None:
    # Cover exhaustion (inner loop finishes): no candidate found in window
    assert (
        ContextualIdDetector().detect(
            "Passport No: and then nothing happens for sixty characters or more so it just exhausts"
        )
        == []
    )

    # Cover candidate failing regex: breaks out of loop (value too short)
    assert ContextualIdDetector().detect("Passport No: X123") == []

    # Cover candidate with no digits
    assert ContextualIdDetector().detect("Passport No: XXXXXXXXX") == []


def test_context_detector_payment_card_length_boundary() -> None:
    # Too short digits for payment card (e.g. 10 digits)
    assert ContextualIdDetector().detect("Credit card number 1234567890 on file.") == []
    # Too many digits for payment card (e.g. 21 digits)
    assert ContextualIdDetector().detect("Credit card number 123456789012345678901 on file.") == []


def test_context_detector_negative_context_score_decay() -> None:
    # A candidate token whose window contains negative indicators (e.g. 'version', 'port')
    # drops score below threshold, suppressing detection
    assert ContextualIdDetector().detect("Passport No: X1234567 in build version 4.") == []


def test_context_detector_hash_separator() -> None:
    # Separator # boost
    detections = ContextualIdDetector().detect("Passport No # X1234567")
    assert len(detections) == 1
    assert detections[0].confidence >= 0.88
