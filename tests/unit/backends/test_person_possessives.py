from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import pytest

from pseudonymize import Pseudonymizer
from pseudonymize.backends.base import BackendCapabilities
from pseudonymize.backends.ml.onnx import LocalONNXPIIBackend
from pseudonymize.document import ContentBlock
from pseudonymize.policy import Policy
from pseudonymize.result import Detection, EntityType


@dataclass
class FixedBackend:
    detections: Sequence[Detection]
    name: str = "fixed"
    allow_remote_processing: bool = False

    @property
    def capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(frozenset({EntityType.PERSON, EntityType.ORGANIZATION}))

    def detect(self, block: ContentBlock, policy: Policy) -> Sequence[Detection]:
        return self.detections


@pytest.mark.parametrize("name", ["Paolo", "\u00c9lodie", "O'Connor"])
@pytest.mark.parametrize("suffix", ["'s", "'S", "\u2019s", "\u2019S"])
@pytest.mark.parametrize("include_suffix", [False, True])
def test_detected_possessives_share_alias_and_are_fully_replaced(
    name: str, suffix: str, include_suffix: bool
) -> None:
    lower_name = name.casefold()
    text = f"{name} arrived. {lower_name}{suffix} car remained."
    start = text.index(lower_name, len(name))
    backend = FixedBackend(
        [
            Detection(EntityType.PERSON, 0, len(name), 0.99, "fixed"),
            Detection(
                EntityType.PERSON,
                start,
                start + len(lower_name) + (len(suffix) if include_suffix else 0),
                0.99,
                "fixed",
            ),
        ]
    )
    result = Pseudonymizer(backends=[backend], enable_coreference=False).process(text)
    assert result.text == "<PER_1> arrived. <PER_1> car remained."
    assert result.replacements[1].detection.end == start + len(lower_name) + len(suffix)
    assert result.text[result.replacements[1].output_start : result.replacements[1].output_end] == (
        result.replacements[1].token
    )
    assert Pseudonymizer(backends=[backend], mode="redacted").process(text).text == (
        "[REDACTED] arrived. [REDACTED] car remained."
    )


@pytest.mark.parametrize("tail", ["'soup", "\u2019soup", "'smith"])
def test_suffix_must_be_a_complete_possessive(tail: str) -> None:
    text = f"Paolo{tail}"
    backend = FixedBackend([Detection(EntityType.PERSON, 0, 5, 0.99, "fixed")])
    assert Pseudonymizer(backends=[backend]).process(text).text == f"<PER_1>{tail}"


def test_organization_possessive_is_not_consumed() -> None:
    text = "Acme's office"
    backend = FixedBackend([Detection(EntityType.ORGANIZATION, 0, 4, 0.99, "fixed")])
    assert Pseudonymizer(backends=[backend]).process(text).text == "<ORG_1>'s office"


@pytest.mark.parametrize("decoder", ["legacy", "constrained_bio"])
def test_onnx_name_mentions_across_sentence_boundary(
    onnx_artifacts: tuple[Path, Path, Path], decoder: str
) -> None:
    config, tokenizer, model = onnx_artifacts
    backend = LocalONNXPIIBackend(model, tokenizer, config, decoder_mode=decoder)
    text = "Alice emailed Bob and Paolo. Paolo's car is outside."
    result = Pseudonymizer(backends=[backend], enable_coreference=False).process(text)
    assert result.text == "<PER_1> emailed <PER_2> and <PER_3>. <PER_3> car is outside."
    assert len(result.replacements) == 4
    assert all(r.detection.backend == backend.name for r in result.replacements)
    assert all(r.detection.detector == "onnx" for r in result.replacements)
