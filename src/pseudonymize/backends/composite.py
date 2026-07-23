from collections.abc import Sequence
from dataclasses import dataclass

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


@dataclass(frozen=True, slots=True)
class CompositeBackend:
    backends: Sequence[DetectionBackend]
    name: str = "composite"
    allow_remote_processing: bool = False

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
        candidates = (
            detection
            for backend in self.backends
            for detection in invoke_backend(backend, block, policy)
            if detection.entity_type in policy.entity_types
            and detection.confidence >= policy.minimum_confidence
        )
        return resolve_overlaps(candidates, policy.detector_priority)


def leaf_backends(backends: Sequence[DetectionBackend]) -> tuple[DetectionBackend, ...]:
    leaves: list[DetectionBackend] = []
    for backend in backends:
        if isinstance(backend, CompositeBackend):
            leaves.extend(leaf_backends(backend.backends))
        else:
            leaves.append(backend)
    return tuple(leaves)
