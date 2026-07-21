from dataclasses import dataclass

from pseudonymize.resolution import ResolvedEntity
from pseudonymize.transforms.alias import Alias


@dataclass(frozen=True, slots=True)
class PlaceholderTransformer:
    def render(self, entity: ResolvedEntity, alias: Alias) -> str:
        suffix = f"_{alias.identifier}" if alias.identifier is not None else ""
        return f"<{alias.entity_type.value}{suffix}>"
