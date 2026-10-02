import re

from hypothesis import given
from hypothesis import strategies as st

from pseudonymize.engine import Pseudonymizer
from pseudonymize.policy import Policy
from pseudonymize.result import EntityType


def test_intra_document_coreference() -> None:
    from pseudonymize.detectors.base import Detector
    from pseudonymize.result import Detection

    class MockDetector(Detector):
        name = "mock"

        def detect(self, text: str) -> list[Detection]:
            import re

            return [
                Detection(EntityType.PERSON, m.start(), m.end(), 0.99, self.name)
                for m in re.finditer(r"Jonathan Doe", text)
            ]

    engine = Pseudonymizer(policy=Policy.default(), detectors=[MockDetector()])

    texts = [
        "First we meet Jonathan Doe.",
        "Later, Jonathan went to the store. And Doe stayed home.",
    ]

    res = engine.process_batch(texts)

    assert "<PER_2>" in res[1].text
    assert "Jonathan" not in res[1].text
    assert "Doe" not in res[1].text


def test_ambiguous_tokens_never_propagate_in_coreference() -> None:
    from pseudonymize.detectors.base import Detector
    from pseudonymize.result import Detection

    class FullNameDetector(Detector):
        name = "full_name_mock"

        def detect(self, text: str) -> list[Detection]:
            import re

            results = [
                Detection(EntityType.PERSON, m.start(), m.end(), 0.99, self.name)
                for m in re.finditer(r"Doctor May Smith", text)
            ]
            results.extend(
                Detection(EntityType.ORGANIZATION, m.start(), m.end(), 0.99, self.name)
                for m in re.finditer(r"Global Health Agency", text)
            )
            return results

    engine = Pseudonymizer(policy=Policy.default(), detectors=[FullNameDetector()])

    texts = [
        "First we meet Doctor May Smith at Global Health Agency.",
        # Ambiguous tokens ('Doctor', 'May', 'Global', 'Agency')
        # must NOT be detected as standalone entities
        "In May, the doctor reviewed global trends and called the local health agency.",
        # Non-ambiguous unique surname ('Smith') DOES link via coreference
        "Smith confirmed the clinical trial results.",
    ]

    res = engine.process_batch(texts)

    # In text 1: Doctor May Smith was redacted
    assert "Doctor May Smith" not in res[0].text
    assert "Global Health Agency" not in res[0].text

    # In text 2: 'May', 'doctor', 'global', 'agency' are ordinary words and MUST NOT be redacted
    assert (
        "In May, the doctor reviewed global trends and called the local health agency."
        in res[1].text
    )

    # In text 3: 'Smith' was linked via coreference
    assert "Smith" not in res[2].text
    assert "<PER_1>" in res[2].text or "<PER_2>" in res[2].text or "<PER_3>" in res[2].text


def test_coreference_never_leaks_across_independent_process_calls() -> None:
    from pseudonymize.detectors.base import Detector
    from pseudonymize.result import Detection

    class InitialDetector(Detector):
        name = "initial_mock"

        def detect(self, text: str) -> list[Detection]:
            import re

            return [
                Detection(EntityType.PERSON, m.start(), m.end(), 0.99, self.name)
                for m in re.finditer(r"Alice Cooper", text)
            ]

    engine = Pseudonymizer(policy=Policy.default(), detectors=[InitialDetector()])

    # First call introduces Alice Cooper
    res1 = engine.process("Alice Cooper presented the keynote.")
    assert "Alice Cooper" not in res1.text

    # Independent second call has its own fresh scope; 'Cooper' alone must not be linked
    res2 = engine.process("Cooper was absent from the subsequent panel.")
    assert "Cooper was absent" in res2.text


def test_token_lookup_preserves_unicode_boundaries_and_case() -> None:
    from pseudonymize.coreference import CoreferenceGraph
    from pseudonymize.result import Detection

    graph = CoreferenceGraph()
    source = "Élodie Smith O\u2019Connor"
    graph.add_detections([Detection(EntityType.PERSON, 0, len(source), 0.99, "source")], source)
    text = "Élodie, Smith's Connor-Smith; smith Smithson _Smith Smith2 2Smith Élodié."
    found = graph.detect(text)
    assert [text[d.start : d.end] for d in found] == [
        "Élodie",
        "Smith",
        "Connor",
        "Smith",
        "Élodie",
    ]
    assert all(d.entity_type is EntityType.PERSON and d.confidence == 0.99 for d in found)


def test_lookup_observes_new_tokens_and_confidence_updates() -> None:
    from pseudonymize.coreference import CoreferenceGraph
    from pseudonymize.result import Detection

    graph = CoreferenceGraph()
    assert graph.detect("Smith") == []
    graph.add_detections([Detection(EntityType.PERSON, 0, 5, 0.96, "source")], "Smith")
    assert graph.detect("Smith")[0].confidence == 0.96
    graph.add_detections([Detection(EntityType.PERSON, 0, 5, 0.99, "source")], "Smith")
    assert graph.detect("Smith")[0].confidence == 0.99


@given(
    st.lists(
        st.sampled_from(
            [
                "Smith",
                "Smithson",
                "Élodie",
                "Connor",
                "smith",
                "東京",
                "_",
                "2",
                " ",
                "-",
                "'",
                "\n",
                "\u0301",
                "🙂",
            ]
        ),
        max_size=100,
    ).map("".join)
)
def test_lookup_matches_original_word_boundary_semantics(text: str) -> None:
    from pseudonymize.coreference import CoreferenceGraph
    from pseudonymize.result import Detection

    graph = CoreferenceGraph()
    source = "Smith Smithson Élodie Connor"
    graph.add_detections([Detection(EntityType.PERSON, 0, len(source), 0.99, "source")], source)
    pattern = (
        r"\b(?:" + "|".join(map(re.escape, sorted(graph.tokens, key=len, reverse=True))) + r")\b"
    )
    expected = [(m.start(), m.end()) for m in re.finditer(pattern, text)]
    assert [(d.start, d.end) for d in graph.detect(text)] == expected
