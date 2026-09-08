import re
from dataclasses import dataclass
from typing import ClassVar

from pseudonymize.memory.dawg import DAWG
from pseudonymize.result import Detection, EntityType


@dataclass(frozen=True, slots=True)
class GazetteerDetector:
    name: str = "gazetteer"

    person_dawg: DAWG | None = None
    location_dawg: DAWG | None = None

    # Fast pre-filter for capitalized words
    _CAPITALIZED_RX: ClassVar[re.Pattern[str]] = re.compile(r"\b[A-Z][a-zA-Z\u00C0-\u017F'-]+\b")

    def detect(self, text: str) -> list[Detection]:
        detections = []
        for match in self._CAPITALIZED_RX.finditer(text):
            word = match.group(0)
            if self.person_dawg is not None and word in self.person_dawg:
                detections.append(
                    Detection(EntityType.PERSON, match.start(), match.end(), 0.90, self.name)
                )
            elif self.location_dawg is not None and word in self.location_dawg:
                detections.append(
                    Detection(EntityType.LOCATION, match.start(), match.end(), 0.90, self.name)
                )
        return detections
