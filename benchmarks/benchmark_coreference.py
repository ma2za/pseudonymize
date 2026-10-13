"""Compare scope lookup costs without changing detector or model quality."""

import re

import pytest

from pseudonymize.coreference import CoreferenceGraph
from pseudonymize.result import Detection, EntityType


def _suffix(value: int) -> str:
    result = ""
    while True:
        result += chr(97 + value % 26)
        value //= 26
        if not value:
            return result


def _alternation_reference(graph: CoreferenceGraph, text: str) -> list[Detection]:
    words = sorted(graph.tokens, key=len, reverse=True)
    pattern = r"\b(?:" + "|".join(map(re.escape, words)) + r")\b"
    results = []
    for match in re.finditer(pattern, text):
        entity_type, confidence = graph.tokens[match.group()]
        results.append(
            Detection(entity_type, match.start(), match.end(), confidence, "coreference")
        )
    return results


@pytest.mark.parametrize("size", [100, 1_000, 10_000])
@pytest.mark.parametrize("implementation", ["alternation", "lookup"])
def test_coreference_scope_lookup(benchmark: object, size: int, implementation: str) -> None:
    graph = CoreferenceGraph()
    for index in range(size):
        word = "Person" + _suffix(index)
        graph.add_detections([Detection(EntityType.PERSON, 0, len(word), 0.99, "source")], word)
    text = "Ordinary unrelated words. " * 40 + "Persona Personb."
    expected = _alternation_reference(graph, text)
    assert graph.detect(text) == expected  # noqa: S101
    if implementation == "alternation":
        result = benchmark(_alternation_reference, graph, text)  # type: ignore[operator]
    else:
        result = benchmark(graph.detect, text)  # type: ignore[operator]
    assert result == expected  # noqa: S101
