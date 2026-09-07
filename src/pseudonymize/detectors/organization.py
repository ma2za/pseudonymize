import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_CORP_RX = re.compile(
    r"\b(?:[A-Z][a-zA-Z0-9&'-]*|&)"
    r"(?:[\s,]+(?:[A-Z][a-zA-Z0-9&'-]*|&)){0,4}"
    r"[\s,]+(?:Inc|LLC|L\.?L\.?C\.?|Corp|Corporation|GmbH|S\.?A\.?|N\.?V\.?|S\.?p\.?A\.?|Pty|Ltd|Limited)\b\.?"
)


@dataclass(frozen=True, slots=True)
class OrganizationDetector:
    name: str = "organization"

    def detect(self, text: str) -> list[Detection]:
        return [
            Detection(EntityType.ORGANIZATION, match.start(), match.end(), 0.90, self.name)
            for match in _CORP_RX.finditer(text)
        ]
