from typing import Protocol

from pseudonymize.resolution import ResolvedEntity
from pseudonymize.transforms.alias import Alias


class Transformer(Protocol):
    def render(self, entity: ResolvedEntity, alias: Alias) -> str: ...
