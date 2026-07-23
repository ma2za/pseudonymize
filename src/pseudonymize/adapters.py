from pathlib import Path
from typing import Protocol, TypeVar

from pseudonymize.document import Document

SourceT = TypeVar("SourceT", contravariant=True)


class InputAdapter(Protocol[SourceT]):
    def extract(self, source: SourceT) -> Document: ...


class OutputAdapter(Protocol):
    def render(self, document: Document) -> bytes: ...


FileInputAdapter = InputAdapter[Path]
