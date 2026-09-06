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
