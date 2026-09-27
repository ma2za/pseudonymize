from pseudonymize.detectors.location import LocationDetector


def test_location_detector_multilingual() -> None:
    detector = LocationDetector()
    texts = [
        "Hauptstrasse 15",
        "Kurfürstendamm 12",
        "Karl-Marx-Allee 12",
        "Rue de la Paix 2",
        "Via Roma 10",
        "Avenida Paulista 2000",
        "Calle de los Milagros 45",
        "Via dell'Indipendenza 123",
    ]

    for t in texts:
        full_text = f"My address is {t}."
        detections = detector.detect(full_text)
        assert len(detections) > 0
        matches = [full_text[det.start : det.end] for det in detections]
        assert any(t in match for match in matches)


def test_location_detector_international_postal_codes() -> None:
    detector = LocationDetector()
    codes = [
        "SW1A 1AA",  # UK
        "K1A 0B1",  # Canada
        "1012 JS",  # Netherlands
        "00-001",  # Poland
        "90210",  # US
        "75001",  # France
    ]
    for code in codes:
        full_text = f"Send mail to {code}."
        detections = detector.detect(full_text)
        assert len(detections) > 0
        matches = [full_text[det.start : det.end] for det in detections]
        assert any(code in match for match in matches)
