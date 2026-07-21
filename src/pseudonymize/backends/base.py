from collections.abc import Sequence
from typing import Protocol

from pseudonymize.result import Detection


class DetectionBackend(Protocol):
    @property
    def name(self) -> str: ...

    def detect(self, text: str) -> Sequence[Detection]: ...


EntityBackend = DetectionBackend
