from typing import Protocol

from pseudonymize.result import Detection


class Detector(Protocol):
    @property
    def name(self) -> str: ...

    def detect(self, text: str) -> list[Detection]: ...
