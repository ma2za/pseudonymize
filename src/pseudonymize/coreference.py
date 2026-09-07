import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import ClassVar

from pseudonymize.result import Detection, EntityType


@dataclass
class CoreferenceGraph:
    # Map from exact token to (EntityType, confidence)
    tokens: dict[str, tuple[EntityType, float]] = field(default_factory=dict)

    _MIN_LENGTH: ClassVar[int] = 3

    def add_detections(self, detections: Iterable[Detection], text: str) -> None:
        for det in detections:
            if det.entity_type not in {EntityType.PERSON, EntityType.ORGANIZATION}:
                continue
            if det.confidence < 0.95:
                continue

            span = text[det.start : det.end]
            # Split by non-word chars to get constituent tokens (e.g. 'Jonathan', 'Doe')
            parts = re.split(r"\W+", span)
            for part in parts:
                if len(part) >= self._MIN_LENGTH and part.isalpha() and part.istitle():
                    # Keep exact case to avoid overly broad matching
                    existing = self.tokens.get(part)
                    if not existing or det.confidence > existing[1]:
                        self.tokens[part] = (det.entity_type, det.confidence)

    def detect(self, text: str) -> list[Detection]:
        if not self.tokens:
            return []

        results = []
        # Sort by length descending to match longest first (though they are words)
        words = sorted(self.tokens.keys(), key=len, reverse=True)
        pattern = r"\b(?:" + "|".join(map(re.escape, words)) + r")\b"

        for match in re.finditer(pattern, text):
            token = match.group(0)
            ent_type, conf = self.tokens[token]
            results.append(Detection(ent_type, match.start(), match.end(), conf, "coreference"))

        return results
