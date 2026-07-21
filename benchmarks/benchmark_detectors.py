import pytest

from pseudonymize.detectors import DEFAULT_DETECTORS


@pytest.mark.parametrize("detector", DEFAULT_DETECTORS, ids=lambda detector: detector.name)
def test_detector_nonmatching_input(benchmark: object, detector: object) -> None:
    text = "A synthetic message without identifiers. " * 2_000
    benchmark(detector.detect, text)  # type: ignore[attr-defined,operator]
