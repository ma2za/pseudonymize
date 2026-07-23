from dataclasses import dataclass
from typing import Generic, TypeVar

from pseudonymize.document import SourceLocation
from pseudonymize.result import EntityType

OutputT = TypeVar("OutputT")


@dataclass(frozen=True, slots=True)
class DetectionReport:
    entity_type: EntityType
    block_id: str
    location: SourceLocation
    start: int
    end: int
    confidence: float
    backend: str
    detector: str
    token: str | None = None


@dataclass(frozen=True, slots=True)
class ProcessingStatistics:
    blocks_processed: int = 0
    detections_found: int = 0
    replacements_applied: int = 0
    backend_invocations: int = 0
    local_block_calls: int = 0
    remote_block_calls: int = 0


@dataclass(frozen=True, slots=True)
class ProcessingWarning:
    code: str
    message: str
    block_id: str | None = None


@dataclass(frozen=True, slots=True)
class ProcessingResult(Generic[OutputT]):
    output: OutputT
    detections: tuple[DetectionReport, ...]
    statistics: ProcessingStatistics
    warnings: tuple[ProcessingWarning, ...] = ()
