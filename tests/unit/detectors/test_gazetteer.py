from pseudonymize.detectors.gazetteer import GazetteerDetector
from pseudonymize.memory.dawg import DAWG


def test_gazetteer_detector_matches() -> None:
    # Setup DAWGs
    person_dawg = DAWG.from_words(["Jonathan", "Doe", "Alice", "Bob"])
    location_dawg = DAWG.from_words(["London", "Paris", "Berlin", "Rome"])

    detector = GazetteerDetector(person_dawg=person_dawg, location_dawg=location_dawg)

    text = "Alice and Bob traveled to Paris and Berlin to meet Jonathan Doe."

    detections = detector.detect(text)

    assert len(detections) == 6

    # Check types
    person_matches = [d for d in detections if d.entity_type.name == "PERSON"]
    location_matches = [d for d in detections if d.entity_type.name == "LOCATION"]

    assert len(person_matches) == 4
    assert len(location_matches) == 2


def test_gazetteer_detector_ignores_lowercase() -> None:
    person_dawg = DAWG.from_words(["hope", "mark", "will"])
    detector = GazetteerDetector(person_dawg=person_dawg)

    # Should not match because the regex requires capital letters
    text = "I hope that mark will do well."

    detections = detector.detect(text)

    assert len(detections) == 0


def test_gazetteer_detector_handles_empty() -> None:
    detector = GazetteerDetector(person_dawg=None, location_dawg=None)
    detections = detector.detect("Hello World")
    assert len(detections) == 0
