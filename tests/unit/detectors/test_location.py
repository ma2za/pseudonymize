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
