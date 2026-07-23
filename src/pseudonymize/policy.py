from collections.abc import Set
from dataclasses import dataclass
from enum import StrEnum

from pseudonymize.result import EntityType

_STRUCTURED = frozenset(
    {
        EntityType.EMAIL,
        EntityType.PHONE,
        EntityType.IP_ADDRESS,
        EntityType.IBAN,
        EntityType.PAYMENT_CARD,
    }
)
_SEMANTIC = frozenset({EntityType.PERSON, EntityType.ORGANIZATION, EntityType.LOCATION})


class NetworkPolicy(StrEnum):
    DENY = "deny"
    ALLOW_CONFIGURED = "allow_configured"
    ALLOW_ALL = "allow_all"


@dataclass(frozen=True, slots=True)
class Policy:
    entity_types: Set[EntityType] = _STRUCTURED | _SEMANTIC
    minimum_confidence: float = 0.8
    detector_priority: tuple[str, ...] = ()
    include_paths: tuple[str, ...] = ()
    exclude_paths: tuple[str, ...] = ()
    network_policy: NetworkPolicy = NetworkPolicy.DENY
    allowed_remote_backends: Set[str] = frozenset()

    def __post_init__(self) -> None:
        object.__setattr__(self, "entity_types", frozenset(self.entity_types))
        object.__setattr__(self, "detector_priority", tuple(self.detector_priority))
        object.__setattr__(self, "include_paths", tuple(self.include_paths))
        object.__setattr__(self, "exclude_paths", tuple(self.exclude_paths))
        object.__setattr__(self, "network_policy", NetworkPolicy(self.network_policy))
        object.__setattr__(self, "allowed_remote_backends", frozenset(self.allowed_remote_backends))
        if not 0 <= self.minimum_confidence <= 1:
            raise ValueError("minimum_confidence must be between 0 and 1")

    @classmethod
    def default(cls) -> "Policy":
        return cls()

    @classmethod
    def strict(cls) -> "Policy":
        return cls(entity_types=frozenset(EntityType), minimum_confidence=0.75)

    @classmethod
    def llm(
        cls,
        *,
        include_paths: tuple[str, ...] | list[str] = (),
        exclude_paths: tuple[str, ...] | list[str] = ("model", "temperature", "response_format"),
    ) -> "Policy":
        return cls(
            entity_types=frozenset(EntityType),
            include_paths=tuple(include_paths),
            exclude_paths=tuple(exclude_paths),
        )

    @classmethod
    def financial(cls) -> "Policy":
        return cls(entity_types=frozenset({EntityType.IBAN, EntityType.PAYMENT_CARD}))

    def allows_path(self, path: tuple[str, ...]) -> bool:
        if any(_path_matches(pattern, path) for pattern in self.exclude_paths):
            return False
        return not self.include_paths or any(
            _path_matches(pattern, path) for pattern in self.include_paths
        )


def _path_matches(pattern: str, path: tuple[str, ...]) -> bool:
    parts = tuple(part for part in pattern.split(".") if part)
    return len(parts) == len(path) and all(
        expected == "*" or expected == actual for expected, actual in zip(parts, path, strict=True)
    )
