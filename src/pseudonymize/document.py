from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from math import isfinite
from types import MappingProxyType
from typing import TypeAlias

MetadataValue: TypeAlias = str | int | float | bool | None


def _metadata(values: Mapping[str, MetadataValue]) -> Mapping[str, MetadataValue]:
    if not isinstance(values, Mapping):
        raise TypeError("metadata must be a mapping")
    copied: dict[str, MetadataValue] = {}
    for key, value in values.items():
        if not isinstance(key, str) or not key:
            raise ValueError("metadata keys must be non-empty strings")
        if value is not None and not isinstance(value, (str, int, float, bool)):
            raise TypeError("metadata values must be JSON scalars")
        if isinstance(value, float) and not isfinite(value):
            raise ValueError("metadata numbers must be finite")
        copied[key] = value
    return MappingProxyType(copied)


@dataclass(frozen=True, slots=True)
class TextOffsetLocation:
    start: int
    end: int

    def __post_init__(self) -> None:
        if (
            not isinstance(self.start, int)
            or isinstance(self.start, bool)
            or not isinstance(self.end, int)
            or isinstance(self.end, bool)
        ):
            raise TypeError("text offsets must be integers")
        if self.start < 0 or self.end < self.start:
            raise ValueError("text offsets must describe a non-negative range")


@dataclass(frozen=True, slots=True)
class JSONPathLocation:
    path: tuple[str | int, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "path", tuple(self.path))
        if any(not isinstance(part, (str, int)) or isinstance(part, bool) for part in self.path):
            raise TypeError("JSON path parts must be strings or integers")
        if any(isinstance(part, int) and part < 0 for part in self.path):
            raise ValueError("JSON path indexes must be non-negative")


@dataclass(frozen=True, slots=True)
class CSVCellLocation:
    row: int
    column: int

    def __post_init__(self) -> None:
        if (
            not isinstance(self.row, int)
            or isinstance(self.row, bool)
            or not isinstance(self.column, int)
            or isinstance(self.column, bool)
        ):
            raise TypeError("CSV row and column indexes must be integers")
        if self.row < 0 or self.column < 0:
            raise ValueError("CSV row and column indexes must be non-negative")


SourceLocation: TypeAlias = TextOffsetLocation | JSONPathLocation | CSVCellLocation


@dataclass(frozen=True, slots=True)
class ContentBlock:
    id: str
    text: str = field(repr=False)
    location: SourceLocation
    metadata: Mapping[str, MetadataValue] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id:
            raise ValueError("block id must not be empty")
        if not isinstance(self.text, str):
            raise TypeError("block text must be a string")
        if not isinstance(self.location, (TextOffsetLocation, JSONPathLocation, CSVCellLocation)):
            raise TypeError("block location must be a supported source location")
        object.__setattr__(self, "metadata", _metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class Document:
    id: str
    blocks: tuple[ContentBlock, ...]
    metadata: Mapping[str, MetadataValue] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        if not isinstance(self.id, str) or not self.id:
            raise ValueError("document id must not be empty")
        blocks: Sequence[ContentBlock] = tuple(self.blocks)
        if any(not isinstance(block, ContentBlock) for block in blocks):
            raise TypeError("document blocks must be ContentBlock values")
        identifiers = [block.id for block in blocks]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("document block ids must be unique")
        object.__setattr__(self, "blocks", tuple(blocks))
        object.__setattr__(self, "metadata", _metadata(self.metadata))
