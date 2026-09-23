import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import ClassVar

from pseudonymize.result import Detection, EntityType

# Ambiguous tokens (months, days, honorifics, corporate/institutional suffixes) that must
# never be propagated as standalone coreference links from compound entity names.
_AMBIGUOUS_COREFERENCE_TOKENS: frozenset[str] = frozenset(
    {
        # Calendar months and days
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
        # Common honorifics and titles
        "Mr",
        "Mrs",
        "Ms",
        "Miss",
        "Dr",
        "Doctor",
        "Prof",
        "Professor",
        "Sir",
        "Madam",
        "President",
        "Minister",
        "General",
        "Major",
        "Captain",
        "Senator",
        "Director",
        "Chief",
        "Officer",
        "Judge",
        "King",
        "Queen",
        "Lord",
        "Lady",
        # Generic organizational and institutional nouns
        "Company",
        "Corp",
        "Corporation",
        "Inc",
        "Incorporated",
        "Ltd",
        "Limited",
        "GmbH",
        "LLC",
        "Group",
        "Holdings",
        "Bank",
        "Agency",
        "Department",
        "Ministry",
        "Bureau",
        "Council",
        "Board",
        "Commission",
        "Foundation",
        "Institute",
        "Institution",
        "Center",
        "Centre",
        "Hospital",
        "University",
        "College",
        "School",
        "Academy",
        "Association",
        "Organization",
        "Society",
        "Federation",
        "Union",
        "Alliance",
        "Trust",
        "Fund",
        "Authority",
        "Office",
        "Service",
        "Services",
        "Network",
        "Systems",
        "Technologies",
        # General modifiers
        "International",
        "National",
        "Global",
        "Federal",
        "State",
        "Central",
        "Regional",
        "Public",
        "Special",
        "First",
        "Second",
        "Third",
        "North",
        "South",
        "East",
        "West",
        "New",
        "Old",
    }
)


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
            parts = [p for p in re.split(r"\W+", span) if p]
            for part in parts:
                if len(part) >= self._MIN_LENGTH and part.isalpha() and part.istitle():
                    # Ambiguous terms (months, honorifics, corporate suffixes) cannot stand alone
                    if part in _AMBIGUOUS_COREFERENCE_TOKENS:
                        continue

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
