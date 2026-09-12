import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

from pseudonymize.memory.bloom import BloomFilter
from pseudonymize.memory.dawg import DAWG
from pseudonymize.result import Detection, EntityType


def _load_dawg(filename: str) -> DAWG | None:
    path = Path(f"data/gazetteer/{filename}")
    if not path.exists():
        return None
    try:
        with open(path, encoding="utf-8") as f:
            words = (line.strip() for line in f if line.strip())
            return DAWG.from_words(words)
    except Exception:
        return None


def _load_bloom(filename: str) -> BloomFilter | None:
    path = Path(f"data/gazetteer/{filename}")
    if not path.exists():
        return None
    try:
        with open(path, encoding="utf-8") as f:
            words = [line.strip().lower() for line in f if line.strip()]
            return BloomFilter.from_words(words)
    except Exception:
        return None


@dataclass(frozen=True, slots=True)
class GazetteerDetector:
    name: str = "gazetteer"

    person_dawg: DAWG | None = field(default_factory=lambda: _load_dawg("names.txt"))
    location_dawg: DAWG | None = field(default_factory=lambda: _load_dawg("locations.txt"))
    veto_filter: BloomFilter | None = field(default_factory=lambda: _load_bloom("common_words.txt"))

    # Fast pre-filter for capitalized words
    _CAPITALIZED_RX: ClassVar[re.Pattern[str]] = re.compile(r"\b[A-Z][a-zA-Z\u00C0-\u017F'-]+\b")

    def detect(self, text: str) -> list[Detection]:
        detections = []
        for match in self._CAPITALIZED_RX.finditer(text):
            word = match.group(0)

            if self.veto_filter is not None and word.lower() in self.veto_filter:
                continue

            if self.person_dawg is not None and word in self.person_dawg:
                detections.append(
                    Detection(EntityType.PERSON, match.start(), match.end(), 0.90, self.name)
                )
            elif self.location_dawg is not None and word in self.location_dawg:
                detections.append(
                    Detection(EntityType.LOCATION, match.start(), match.end(), 0.90, self.name)
                )
        return detections
