from typing import Any

import pytest

from pseudonymize import Pseudonymizer, TransformationMode
from pseudonymize.detectors.email import EmailDetector
from pseudonymize.detectors.gazetteer import GazetteerDetector
from pseudonymize.memory import MemoryBoundary
from pseudonymize.memory.dawg import DAWG


class DummyStore:
    def __init__(self) -> None:
        self.data: dict[str, Any] = {}

    def read(self, key: str) -> dict[str, Any] | str | None:
        return self.data.get(key)

    def write(self, key: str, value: dict[str, Any] | str) -> None:
        self.data[key] = value

    def delete(self, key: str) -> None:
        self.data.pop(key, None)


@pytest.mark.parametrize(
    ("detect_names", "expected"),
    [
        (False, "The user is Paolo, and his email is <EML_1>."),
        (True, "The user is <PER_1>, and his email is <EML_1>."),
    ],
)
def test_memory_boundary_write(detect_names: bool, expected: str) -> None:
    store = DummyStore()
    engine = Pseudonymizer(
        mode=TransformationMode.NUMBERED,
        detectors=(
            EmailDetector(),
            GazetteerDetector(
                person_dawg=DAWG.from_words(("Paolo",)) if detect_names else None,
                location_dawg=None,
                veto_filter=None,
            ),
        ),
    )
    boundary = MemoryBoundary(store=store, engine=engine)

    payload = {"memory": "The user is Paolo, and his email is paolo@example.com."}
    boundary.write("session_1", payload, namespace="user_A")

    saved = store.read("session_1")
    assert isinstance(saved, dict)
    assert saved["memory"] == expected

    # Check that another user namespace would generate the same numbered alias sequence locally
    # but theoretically would map to a different context.
    boundary.write("session_2", payload, namespace="user_B")
    saved2 = store.read("session_2")
    assert isinstance(saved2, dict)
    assert saved2["memory"] == expected


def test_memory_boundary_delete() -> None:
    store = DummyStore()
    boundary = MemoryBoundary(store=store)

    boundary.write("session_1", "Secret value", "ns1")
    assert store.read("session_1") is not None
    boundary.delete("session_1")
    assert store.read("session_1") is None
