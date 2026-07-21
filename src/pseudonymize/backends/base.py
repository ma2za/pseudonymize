from typing import Protocol

from pseudonymize.result import Detection


class EntityBackend(Protocol):
    @property
    def name(self) -> str: ...

    def load(self) -> None: ...

    def detect(self, text: str) -> list[Detection]: ...
