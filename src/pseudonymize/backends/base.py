from collections.abc import Sequence
from dataclasses import dataclass, replace
from typing import Protocol

from pseudonymize.document import ContentBlock
from pseudonymize.exceptions import (
    BackendContractError,
    BackendExecutionError,
    InvalidDetectionError,
    NetworkPolicyError,
)
from pseudonymize.policy import NetworkPolicy, Policy
from pseudonymize.result import Detection, EntityType


@dataclass(frozen=True, slots=True)
class BackendCapabilities:
    entity_types: frozenset[EntityType]
    remote: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "entity_types", frozenset(self.entity_types))
        if any(not isinstance(entity_type, EntityType) for entity_type in self.entity_types):
            raise TypeError("backend entity types must be EntityType values")
        if not isinstance(self.remote, bool):
            raise TypeError("backend remote capability must be a boolean")


class DetectionBackend(Protocol):
    @property
    def name(self) -> str: ...

    @property
    def capabilities(self) -> BackendCapabilities: ...

    @property
    def allow_remote_processing(self) -> bool: ...

    def detect(self, block: ContentBlock, policy: Policy) -> Sequence[Detection]: ...


def backend_capabilities(backend: DetectionBackend) -> BackendCapabilities:
    try:
        capabilities = backend.capabilities
        allow_remote_processing = backend.allow_remote_processing
        name = backend.name
    except Exception:
        raise BackendContractError(
            "backend does not declare the required block-aware contract"
        ) from None
    if not isinstance(capabilities, BackendCapabilities):
        raise BackendContractError("backend capabilities are invalid")
    if not isinstance(allow_remote_processing, bool):
        raise BackendContractError("backend remote consent must be a boolean")
    if not isinstance(name, str) or not name:
        raise BackendContractError("backend name must be a non-empty string")
    return capabilities


def invoke_backend(
    backend: DetectionBackend, block: ContentBlock, policy: Policy
) -> tuple[Detection, ...]:
    capabilities = backend_capabilities(backend)
    name = backend.name
    if capabilities.remote:
        if policy.network_policy is NetworkPolicy.DENY:
            raise NetworkPolicyError("network policy denies remote processing")
        if not backend.allow_remote_processing:
            raise NetworkPolicyError("remote backend lacks explicit consent")
        if (
            policy.network_policy is NetworkPolicy.ALLOW_CONFIGURED
            and name not in policy.allowed_remote_backends
        ):
            raise NetworkPolicyError("remote backend is not allowlisted")
    try:
        candidates = tuple(backend.detect(block, policy))
    except TypeError:
        raise BackendContractError("backend does not implement block-aware detection") from None
    except Exception as e:
        raise BackendExecutionError("backend failed during detection") from e
    detections: list[Detection] = []
    for detection in candidates:
        if not isinstance(detection, Detection):
            raise BackendContractError("backend returned a value that is not a Detection")
        if detection.entity_type not in capabilities.entity_types:
            raise BackendContractError(
                f"backend {backend.name} returned an undeclared entity type {detection.entity_type}"
            )
        if detection.end > len(block.text):
            raise InvalidDetectionError("backend returned offsets outside the content block")
        detections.append(detection if detection.backend else replace(detection, backend=name))
    return tuple(detections)


def invoke_backend_batch(
    backend: DetectionBackend, blocks: Sequence[ContentBlock], policy: Policy
) -> tuple[tuple[Detection, ...], ...]:
    if not blocks:
        return ()

    capabilities = backend_capabilities(backend)
    name = backend.name
    if capabilities.remote:
        if policy.network_policy is NetworkPolicy.DENY:
            raise NetworkPolicyError("network policy denies remote processing")
        if not backend.allow_remote_processing:
            raise NetworkPolicyError("remote backend lacks explicit consent")
        if (
            policy.network_policy is NetworkPolicy.ALLOW_CONFIGURED
            and name not in policy.allowed_remote_backends
        ):
            raise NetworkPolicyError("remote backend is not allowlisted")

    detect_batch_fn = getattr(backend, "detect_batch", None)
    if callable(detect_batch_fn):
        try:
            batch_candidates = tuple(detect_batch_fn(blocks, policy))
        except TypeError:
            raise BackendContractError(
                "backend does not implement block-aware batch detection"
            ) from None
        except Exception as e:
            raise BackendExecutionError("backend failed during batch detection") from e

        if len(batch_candidates) != len(blocks):
            raise BackendContractError(
                f"backend {backend.name} returned {len(batch_candidates)} "
                f"results for {len(blocks)} blocks"
            )

        all_results: list[tuple[Detection, ...]] = []
        for block, candidates in zip(blocks, batch_candidates, strict=True):
            detections: list[Detection] = []
            for detection in candidates:
                if not isinstance(detection, Detection):
                    raise BackendContractError("backend returned a value that is not a Detection")
                if detection.entity_type not in capabilities.entity_types:
                    raise BackendContractError(
                        f"backend {backend.name} returned an undeclared entity type "
                        f"{detection.entity_type}"
                    )
                if detection.end > len(block.text):
                    raise InvalidDetectionError(
                        "backend returned offsets outside the content block"
                    )
                detections.append(
                    detection if detection.backend else replace(detection, backend=name)
                )
            all_results.append(tuple(detections))
        return tuple(all_results)

    return tuple(invoke_backend(backend, block, policy) for block in blocks)
