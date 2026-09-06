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
            entity_types=frozenset(
                {EntityType.LOCATION, EntityType.ORGANIZATION, EntityType.PERSON}
            ),
            remote=False,
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


def test_engine_pass2_crops_leading_and_trailing_function_words() -> None:
    # "John is in Seattle and" -> indices 12 to 34 is "in Seattle and" (originally proposed)
    # Pass 2 should crop "in" (leading) and "and" (trailing) to isolate "Seattle"
    text = "John is currently in Seattle and his sister is there."
    # "in Seattle and" starts at 18, ends at 32
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))
    det = Detection(EntityType.LOCATION, 18, 32, 0.9, "test")
    engine = Pseudonymizer(backends=[DummyBackend([det])], policy=Policy())
    results = engine._detect_block(block, _OperationStatistics(), False)

    assert len(results) == 1
    assert text[results[0].start : results[0].end] == "Seattle"


def test_engine_pass2_crops_the_from_organization() -> None:
    text = "He works at the Microsoft corporation."
    # "the Microsoft corporation" starts at 12, ends at 37
    block = ContentBlock(id="1", text=text, location=TextOffsetLocation(0, len(text)))
    det = Detection(EntityType.ORGANIZATION, 12, 37, 0.9, "test")
    engine = Pseudonymizer(backends=[DummyBackend([det])], policy=Policy())
    results = engine._detect_block(block, _OperationStatistics(), False)

    assert len(results) == 1
    assert text[results[0].start : results[0].end] == "Microsoft corporation"
