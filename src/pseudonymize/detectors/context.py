import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_CONTEXT_PATTERNS = [
    # Passport
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:passport\s*(?:no\.?|number|#)?)(?![a-z0-9_])\s*:?\s*([A-Z0-9]{6,15})(?![a-z0-9_])"
        ),
        EntityType.NATIONAL_ID,
    ),
    # Driver's License
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:driver'?s?\s*licen[sc]e|driving\s*licen[sc]e)\s*(?:no\.?|number|#)?(?![a-z0-9_])\s*:?\s*([A-Z0-9]{6,15})(?![a-z0-9_])"
        ),
        EntityType.NATIONAL_ID,
    ),
    # ID Card / National ID
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:identification\s*number|id\s*card|national\s*id|id\s*(?:no\.?|number|#)|identificatif|identifiant)(?![a-z0-9_])\s*:?\s*([A-Z0-9]{6,15})(?![a-z0-9_])"
        ),
        EntityType.NATIONAL_ID,
    ),
    # Tax Number
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:tax\s*(?:no\.?|number|reference|id)|tin|vat\s*(?:no\.?|number|id))(?![a-z0-9_])\s*:?\s*([A-Z0-9]{6,15})(?![a-z0-9_])"
        ),
        EntityType.TAX_ID,
    ),
    # Zip / Postal Code
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:zip\s*code|postal\s*code|postcode|zip)(?![a-z0-9_])\s*:?\s*([A-Z0-9-]{4,10})(?![a-z0-9_])"
        ),
        EntityType.LOCATION,
    ),
    # Generic Account / Policy / Insurance
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:account|policy|insurance)\s*(?:no\.?|number|#)(?![a-z0-9_])\s*:?\s*([A-Z0-9-]{6,16})(?![a-z0-9_])"
        ),
        EntityType.SECRET,
    ),
    # Credit Card Context Fallback (catches synthetic ones failing Luhn)
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:credit\s*card|visa|mastercard|maestro|amex|card\s*number)\s*(?:no\.?|number|ending\s*in|#)?(?![a-z0-9_])\s*:?\s*(\d{13,19})(?![a-z0-9_])"
        ),
        EntityType.PAYMENT_CARD,
    ),
]


@dataclass(frozen=True, slots=True)
class ContextualIdDetector:
    name: str = "context_id"

    def detect(self, text: str) -> list[Detection]:
        detections = []
        for pattern, entity_type in _CONTEXT_PATTERNS:
            for match in pattern.finditer(text):
                # We map the span of the CAPTURE GROUP, not the whole regex
                # so we don't redact the keyword itself.
                start, end = match.span(1)
                detections.append(Detection(entity_type, start, end, 0.90, self.name))
        return detections
