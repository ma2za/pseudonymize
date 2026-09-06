from collections.abc import Sequence

from pseudonymize.backends.base import BackendCapabilities, DetectionBackend
from pseudonymize.document import ContentBlock, TextOffsetLocation
from pseudonymize.engine import Pseudonymizer, _OperationStatistics
from pseudonymize.policy import Policy
from pseudonymize.result import Detection, EntityType


class DummyBackend(DetectionBackend):
    def __init__(self, detections: Sequence[Detection]) -> None:
        self._name = "dummy"
        self._capabilities = BackendCapabilities(
            entity_types=frozenset({EntityType.LOCATION}), remote=False
        )
        self._detections = detections

    @property
    def name(self) -> str:
        return self._name

    @property
    def capabilities(self) -> BackendCapabilities:
        return self._capabilities

    @property
    def allow_remote_processing(self) -> bool:
        return False

    def detect(self, block: ContentBlock, policy: Policy) -> Sequence[Detection]:
        return self._detections


def test_engine_segments_nested_location_address() -> None:
    # "123 Main St, Springfield, 12345" (index 0 to 31)
    # Under standard ML, this might match as one massive LOCATION detection.
    # Our geographic segmentation splits it:
    # - "123 Main St" (STREET)
    # - "Springfield" (CITY -> gap text)
    # - "12345" (ZIPCODE)
    text = "123 Main St, Springfield, 12345"
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))
    det = Detection(EntityType.LOCATION, 0, 31, 0.9, "test")
    engine = Pseudonymizer(backends=[DummyBackend([det])], policy=Policy())
    results = engine._detect_block(block, _OperationStatistics(), False)

    assert len(results) == 3
    assert results[0].start == 0
    assert results[0].end == 11
    assert text[results[0].start : results[0].end] == "123 Main St"

    assert results[1].start == 13
    assert results[1].end == 24
    assert text[results[1].start : results[1].end] == "Springfield"

    assert results[2].start == 26
    assert results[2].end == 31
    assert text[results[2].start : results[2].end] == "12345"


def test_engine_segments_location_with_trailing_gap() -> None:
    # "123 Main St, Springfield"
    text = "123 Main St, Springfield"
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))
    det = Detection(EntityType.LOCATION, 0, 24, 0.9, "test")
    engine = Pseudonymizer(backends=[DummyBackend([det])], policy=Policy())
    results = engine._detect_block(block, _OperationStatistics(), False)

    assert len(results) == 2
    assert text[results[0].start : results[0].end] == "123 Main St"
    assert text[results[1].start : results[1].end] == "Springfield"
