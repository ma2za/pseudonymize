from pseudonymize.engine import Pseudonymizer
from pseudonymize.policy import Policy
from pseudonymize.result import EntityType
from pseudonymize.coreference import CoreferenceGraph


def test_intra_document_coreference() -> None:
    from pseudonymize.detectors.base import Detector
    from pseudonymize.result import Detection

    class MockDetector(Detector):
        name = "mock"

        def detect(self, text: str) -> list[Detection]:
            results = []
            import re

            for m in re.finditer(r"Jonathan Doe", text):
                results.append(Detection(EntityType.PERSON, m.start(), m.end(), 0.99, self.name))
            return results

    engine = Pseudonymizer(policy=Policy.default(), detectors=[MockDetector()])

    texts = [
        "First we meet Jonathan Doe.",
        "Later, Jonathan went to the store. And Doe stayed home.",
    ]

    res = engine.process_batch(texts)

    assert "<PERSON_2>" in res[1].text
    assert "Jonathan" not in res[1].text
    assert "Doe" not in res[1].text
