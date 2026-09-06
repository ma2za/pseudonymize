import pytest
from pseudonymize.result import Detection, EntityType
from pseudonymize.engine import Pseudonymizer, Policy, _OperationStatistics
from pseudonymize.backends.base import DetectionBackend, BackendCapabilities
from pseudonymize.document import ContentBlock, TextOffsetLocation

class DummyBackend(DetectionBackend):
    def __init__(self, detections):
        self._name = "dummy"
        self._capabilities = BackendCapabilities(
            entity_types=frozenset({EntityType.PERSON, EntityType.EMAIL}),
            remote=False
        )
        self._detections = detections

    @property
    def name(self): return self._name
    @property
    def capabilities(self): return self._capabilities
    @property
    def allow_remote_processing(self): return False

    def detect(self, block, policy):
        return self._detections

def test_engine_trims_punctuation_from_person():
    text = "Hello (John Doe), and welcome!"
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))
    det = Detection(EntityType.PERSON, 6, 17, 0.9, "test")
    engine = Pseudonymizer(backends=[DummyBackend([det])], policy=Policy())
    results = engine._detect_block(block, _OperationStatistics(), False)
    assert len(results) == 1
    assert results[0].start == 7
    assert results[0].end == 15

def test_engine_does_not_trim_email():
    text = "Email: (user@example.com), please."
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))
    det = Detection(EntityType.EMAIL, 7, 25, 0.9, "test")
    engine = Pseudonymizer(backends=[DummyBackend([det])], policy=Policy())
    results = engine._detect_block(block, _OperationStatistics(), False)
    assert len(results) == 1
    assert results[0].start == 7
    assert results[0].end == 25

def test_engine_completely_trimmed_away():
    text = "(...,)"
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))
    det = Detection(EntityType.PERSON, 0, 6, 0.9, "test")
    engine = Pseudonymizer(backends=[DummyBackend([det])], policy=Policy())
    results = engine._detect_block(block, _OperationStatistics(), False)
    assert len(results) == 0

def test_engine_trims_right_but_not_left():
    text = "John Doe,"
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))
    det = Detection(EntityType.PERSON, 0, 9, 0.9, "test")
    engine = Pseudonymizer(backends=[DummyBackend([det])], policy=Policy())
    results = engine._detect_block(block, _OperationStatistics(), False)
    assert len(results) == 1
    assert results[0].start == 0
    assert results[0].end == 8
