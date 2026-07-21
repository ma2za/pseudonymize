from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Protocol

from pseudonymize.normalization import normalize
from pseudonymize.result import Detection


@dataclass(frozen=True, slots=True)
class ResolvedEntity:
    detection: Detection
    normalized_value: str = field(repr=False)


class EntityResolver(Protocol):
    def resolve(self, text: str, detections: Sequence[Detection]) -> tuple[ResolvedEntity, ...]: ...


@dataclass(frozen=True, slots=True)
class ExactEntityResolver:
    def resolve(self, text: str, detections: Sequence[Detection]) -> tuple[ResolvedEntity, ...]:
        return tuple(
            ResolvedEntity(
                detection,
                normalize(text[detection.start : detection.end], detection.entity_type),
            )
            for detection in detections
        )
