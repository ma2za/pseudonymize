from dataclasses import dataclass

from pseudonymize.resolution import ResolvedEntity
from pseudonymize.transforms.alias import Alias


@dataclass(frozen=True, slots=True)
class RedactTransformer:
    typed: bool = False

    def render(self, entity: ResolvedEntity, alias: Alias) -> str:
        suffix = f"_{entity.detection.entity_type.value}" if self.typed else ""
        return f"[REDACTED{suffix}]"
