from typing import Protocol

from pseudonymize.result import Detection


class Transformer(Protocol):
    def transform(self, value: str, detection: Detection) -> str: ...
