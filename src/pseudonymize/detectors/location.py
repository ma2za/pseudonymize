import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_STREET_RX = re.compile(
    r"(?i)\b\d{1,5}\s+(?:[A-Za-z]+\s*){1,3}"
    r"(?:Street|St\.?|Avenue|Ave\.?|Road|Rd\.?|Boulevard|Blvd\.?|Lane|Ln\.?|"
    r"Drive|Dr\.?|Court|Ct\.?|Plaza|Plz\.?|Square|Sq\.?|Way|Parkway|Pkwy\.?|Terrace|Ter\.?)\b"
)

_ZIPCODE_RX = re.compile(r"(?i)\b(?:[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}|\d{5}(?:-\d{4})?)\b")


@dataclass(frozen=True, slots=True)
class LocationDetector:
    name: str = "location"

    def detect(self, text: str) -> list[Detection]:
        detections = [
            Detection(EntityType.LOCATION, match.start(), match.end(), 0.90, self.name)
            for match in _STREET_RX.finditer(text)
        ]
        detections.extend(
            Detection(EntityType.LOCATION, match.start(), match.end(), 0.90, self.name)
            for match in _ZIPCODE_RX.finditer(text)
        )
        return detections
