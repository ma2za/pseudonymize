import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_STREET_RX = re.compile(
    r"(?i)\b\d{1,5}\s+(?:[A-Za-z]+\s*){1,3}"
    r"(?:Street|St\.?|Avenue|Ave\.?|Road|Rd\.?|Boulevard|Blvd\.?|Lane|Ln\.?|"
    r"Drive|Dr\.?|Court|Ct\.?|Plaza|Plz\.?|Square|Sq\.?|Way|Parkway|Pkwy\.?|Terrace|Ter\.?)\b"
)

_GERMANIC_STREET_RX = re.compile(
    r"(?i)\b[A-Za-z\u00C0-\u017F\-]+(?:strasse|str\.?|platz|weg|allee|damm|ring|ufer)\s+\d{1,5}[a-zA-Z]?\b"
)

_ROMANCE_STREET_RX = re.compile(
    r"(?i)\b(?:Rue|Via|Viale|Corso|Piazza|Avenida|Av\.?|Calle|Paseo|Praça|Boulevard|Blvd)\b\s+"
    r"(?:(?:de|la|del|el|los|las|da|do|dos|das|di|dell'?)\s*)*[A-Za-z\u00C0-\u017F]+\s*"
    r"(?:(?:de|la|del|el|los|las|da|do|dos|das|di|dell'?)\s*[A-Za-z\u00C0-\u017F]+\s*){0,3},?\s+\d{1,5}[a-zA-Z]?\b"
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
        for pattern in (_GERMANIC_STREET_RX, _ROMANCE_STREET_RX, _ZIPCODE_RX):
            detections.extend(
                Detection(EntityType.LOCATION, match.start(), match.end(), 0.90, self.name)
                for match in pattern.finditer(text)
            )
        return detections
