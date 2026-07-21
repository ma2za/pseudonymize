from collections.abc import Sequence
from dataclasses import dataclass

from pseudonymize.detectors import DEFAULT_DETECTORS, Detector
from pseudonymize.result import Detection


@dataclass(frozen=True, slots=True)
class RulesBackend:
    detectors: Sequence[Detector] = DEFAULT_DETECTORS
    name: str = "rules"

    def __post_init__(self) -> None:
        object.__setattr__(self, "detectors", tuple(self.detectors))

    def detect(self, text: str) -> tuple[Detection, ...]:
        return tuple(
            detection for detector in self.detectors for detection in detector.detect(text)
        )
