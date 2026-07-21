import base64
import hashlib
import hmac
from collections.abc import MutableMapping
from dataclasses import dataclass, field
from typing import Protocol

from pseudonymize.exceptions import InvalidKeyError
from pseudonymize.resolution import ResolvedEntity
from pseudonymize.result import EntityType

_MINIMUM_KEY_BYTES = 32


@dataclass(frozen=True, slots=True)
class Alias:
    entity_type: EntityType
    identifier: str | None


@dataclass(slots=True, repr=False)
class AliasContext:
    aliases: MutableMapping[tuple[EntityType, str], Alias] = field(default_factory=dict)
    counters: MutableMapping[EntityType, int] = field(default_factory=dict)


class AliasAssigner(Protocol):
    def assign(self, entity: ResolvedEntity, context: AliasContext) -> Alias: ...


@dataclass(frozen=True, slots=True)
class NumberedAliasAssigner:
    def assign(self, entity: ResolvedEntity, context: AliasContext) -> Alias:
        key = (entity.detection.entity_type, entity.normalized_value)
        existing = context.aliases.get(key)
        if existing is not None:
            return existing
        entity_type = entity.detection.entity_type
        identifier = context.counters.get(entity_type, 0) + 1
        context.counters[entity_type] = identifier
        alias = Alias(entity_type, str(identifier))
        context.aliases[key] = alias
        return alias


@dataclass(frozen=True, slots=True)
class GenericAliasAssigner:
    def assign(self, entity: ResolvedEntity, context: AliasContext) -> Alias:
        return Alias(entity.detection.entity_type, None)


@dataclass(frozen=True, slots=True)
class DeterministicAliasAssigner:
    key: bytes = field(repr=False)
    namespace: str = "default"

    def __post_init__(self) -> None:
        if len(self.key) < _MINIMUM_KEY_BYTES:
            raise InvalidKeyError("key must contain at least 32 bytes")
        if "\0" in self.namespace:
            raise ValueError("namespace must not contain NUL characters")

    def assign(self, entity: ResolvedEntity, context: AliasContext) -> Alias:
        payload = b"\0".join(
            (
                b"PZ2",
                self.namespace.encode("utf-8"),
                entity.detection.entity_type.value.encode("ascii"),
                entity.normalized_value.encode("utf-8"),
            )
        )
        digest = hmac.new(self.key, payload, hashlib.sha256).digest()
        identifier = base64.b32encode(digest).decode("ascii")[:12]
        return Alias(entity.detection.entity_type, identifier)
