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

    # Fast pre-filter for capitalized words (can optionally grab adjacent capitalized words up to 3)
    _CAPITALIZED_RX: ClassVar[re.Pattern[str]] = re.compile(
        r"\b[A-Z][a-zA-Z\u00C0-\u017F'-]+(?:[ ]+[A-Z][a-zA-Z\u00C0-\u017F'-]+){0,2}\b"
    )

    def detect(self, text: str) -> list[Detection]:
        detections = []
        for match in self._CAPITALIZED_RX.finditer(text):
            word = match.group(0)

            # We can also check individual parts if the whole compound word isn't found
            parts = word.split()

            # 1. Try the full compound string (e.g. "Toa Payoh", "New York")
            if self.location_dawg is not None and word in self.location_dawg:
                detections.append(
                    Detection(EntityType.LOCATION, match.start(), match.end(), 0.90, self.name)
                )
                continue  # if full match found, don't over-segment
            if self.person_dawg is not None and word in self.person_dawg:
                detections.append(
                    Detection(EntityType.PERSON, match.start(), match.end(), 0.90, self.name)
                )
                continue

            # 2. If compound fails, check individual parts (e.g. "John Smith")
            if len(parts) > 1:
                current_start = match.start()
                for p in parts:
                    p_start = text.find(p, current_start)
                    p_end = p_start + len(p)
                    current_start = p_end

                    if self.veto_filter is not None and p.lower() in self.veto_filter:
                        continue

                    if self.location_dawg is not None and p in self.location_dawg:
                        detections.append(
                            Detection(EntityType.LOCATION, p_start, p_end, 0.90, self.name)
                        )
                    elif self.person_dawg is not None and p in self.person_dawg:
                        detections.append(
                            Detection(EntityType.PERSON, p_start, p_end, 0.90, self.name)
                        )
            else:
                if self.veto_filter is not None and word.lower() in self.veto_filter:
                    continue
                if self.location_dawg is not None and word in self.location_dawg:
                    detections.append(
                        Detection(EntityType.LOCATION, match.start(), match.end(), 0.90, self.name)
                    )
                elif self.person_dawg is not None and word in self.person_dawg:
                    detections.append(
                        Detection(EntityType.PERSON, match.start(), match.end(), 0.90, self.name)
                    )

        return detections
