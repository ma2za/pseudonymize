from collections.abc import Sequence
from dataclasses import dataclass

from pseudonymize.backends.base import DetectionBackend
from pseudonymize.result import Detection


@dataclass(frozen=True, slots=True)
class CompositeBackend:
    backends: Sequence[DetectionBackend]
    name: str = "composite"

    def __post_init__(self) -> None:
        object.__setattr__(self, "backends", tuple(self.backends))

    def detect(self, text: str) -> tuple[Detection, ...]:
        return tuple(detection for backend in self.backends for detection in backend.detect(text))
