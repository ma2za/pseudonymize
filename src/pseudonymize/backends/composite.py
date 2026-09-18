from collections.abc import Sequence
from dataclasses import dataclass
from enum import StrEnum

from pseudonymize.backends.base import (
    BackendCapabilities,
    DetectionBackend,
    backend_capabilities,
    invoke_backend,
)
from pseudonymize.document import ContentBlock
from pseudonymize.policy import Policy
from pseudonymize.result import Detection
from pseudonymize.spans import resolve_overlaps


class EnsembleMode(StrEnum):
    UNION = "union"
    INTERSECTION = "intersection"


@dataclass(frozen=True, slots=True)
class CompositeBackend:
    backends: Sequence[DetectionBackend]
    name: str = "composite"
    allow_remote_processing: bool = False
    ensemble_mode: EnsembleMode = EnsembleMode.UNION

    def __post_init__(self) -> None:
        object.__setattr__(self, "backends", tuple(self.backends))

    @property
    def capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(
            frozenset(
                entity_type
                for backend in self.backends
                for entity_type in backend_capabilities(backend).entity_types
            ),
            any(backend_capabilities(backend).remote for backend in self.backends),
        )

    def detect(self, block: ContentBlock, policy: Policy) -> tuple[Detection, ...]:
        if self.ensemble_mode == EnsembleMode.UNION:
            candidates = (
                detection
                for backend in self.backends
                for detection in invoke_backend(backend, block, policy)
                if detection.entity_type in policy.entity_types
                and detection.confidence >= policy.minimum_confidence
            )
            return resolve_overlaps(candidates, policy.detector_priority)

        # INTERSECTION mode
        backend_detections: list[list[Detection]] = []
        for backend in self.backends:
            dets = [
                detection
                for detection in invoke_backend(backend, block, policy)
                if detection.entity_type in policy.entity_types
                and detection.confidence >= policy.minimum_confidence
            ]
            if dets:
                backend_detections.append(dets)

        candidates_list: list[Detection] = []
        if len(backend_detections) >= 2:
            for b_idx, dets in enumerate(backend_detections):
                for d in dets:
                    # Check if d overlaps with at least one detection
                    # of the same type in any other backend
                    is_confirmed = False
                    for other_idx, other_dets in enumerate(backend_detections):
                        if b_idx == other_idx:
                            continue
                        for other_d in other_dets:
                            if (
                                d.entity_type == other_d.entity_type
                                and d.start < other_d.end
                                and other_d.start < d.end
                            ):
                                is_confirmed = True
                                break
                        if is_confirmed:
                            break
                    if is_confirmed:
                        candidates_list.append(d)

        return resolve_overlaps(candidates_list, policy.detector_priority)


def leaf_backends(backends: Sequence[DetectionBackend]) -> tuple[DetectionBackend, ...]:
    leaves: list[DetectionBackend] = []
    for backend in backends:
        if isinstance(backend, CompositeBackend) and backend.ensemble_mode == EnsembleMode.UNION:
            leaves.extend(leaf_backends(backend.backends))
        else:
            leaves.append(backend)
    return tuple(leaves)
