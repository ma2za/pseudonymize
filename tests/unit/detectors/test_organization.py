from pseudonymize.detectors.organization import OrganizationDetector


def test_organization_detector_matches() -> None:
    detector = OrganizationDetector()

    texts = [
        "Acme Corp",
        "Globex Inc.",
        "Wayne Enterprises LLC",
        "Stark Industries, Inc.",
        "Initech SpA",
        "Massive Dynamic GmbH",
        "Smith & Wesson Corp.",
        "ACME LLC",
    ]

    for t in texts:
        detections = detector.detect(t)
        assert len(detections) == 1
        assert t[detections[0].start : detections[0].end] == t


def test_organization_detector_ignores_lowercased() -> None:
    detector = OrganizationDetector()

    texts = ["hello world llc", "acme corp", "wayne enterprises inc."]

    for t in texts:
        detections = detector.detect(t)
        assert len(detections) == 0


def test_organization_detector_with_surrounding_text() -> None:
    detector = OrganizationDetector()

    text = "We recently signed a contract with Stark Industries, Inc. for the new project."
    detections = detector.detect(text)

    assert len(detections) == 1
    assert text[detections[0].start : detections[0].end] == "Stark Industries, Inc."
