from typing import Any, Protocol, cast, runtime_checkable

from pseudonymize.engine import Pseudonymizer


@runtime_checkable
class MemoryStore(Protocol):
    def read(self, key: str) -> Any: ...
    def write(self, key: str, value: Any) -> None: ...
    def delete(self, key: str) -> None: ...


class MemoryBoundary:
    """A privacy boundary sitting between an agent and its persistent memory store."""

    def __init__(self, store: MemoryStore, engine: Pseudonymizer | None = None) -> None:
        self._store = store
        self._engine = engine or Pseudonymizer()

    def write(self, key: str, value: dict[str, Any] | str, namespace: str) -> None:
        """Pseudonymize a record before writing it to the underlying store."""
        scope = self._engine.new_scope()

        safe_value = scope.process_data(value)
        self._store.write(key, safe_value)

    def read(self, key: str, restore: bool = False) -> dict[str, Any] | str | None:
        """Read a record."""
        return cast(dict[str, Any] | str | None, self._store.read(key))  # pragma: no cover

    def delete(self, key: str) -> None:
        """Erasure request for a specific record."""
        self._store.delete(key)
