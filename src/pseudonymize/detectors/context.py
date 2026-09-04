import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

# Every pattern here follows the same shape: a label that a document author
# would actually write next to an identifier, an optional separator, and a
# captured value that must contain at least one digit.
#
# The digit requirement is what keeps these from firing on ordinary prose. A
# label alone is not evidence: "identification number before Tuesday" and "the
# applicant Jonathan submitted forms" both put a plain English word where the
# identifier would go, and without the constraint both were reported as a
# national ID.
#
# Triggers must also be labels rather than coincidences. A phrase earns its
# place here only if a reader would expect an identifier immediately after it
# in any document, not because some corpus happens to pair the two.
_HAS_DIGIT = r"(?=[A-Z0-9-]*\d)"
_SEPARATOR = r"\s*[:#-]?\s*"

_CONTEXT_PATTERNS = [
    # National identity documents
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:identification\s*number|identity\s*(?:card|number)"
            r"|id\s*card|national\s*id|registration\s*number"
            r"|numéro\s*d'identification|número\s*de\s*identificación"
            r"|chứng\s*minh\s*nhân\s*dân|căn\s*cước|身份证号)"
            rf"(?![a-z0-9_]){_SEPARATOR}\(?({_HAS_DIGIT}[A-Z0-9-]{{6,15}})\)?(?![a-z0-9_])"
        ),
        EntityType.NATIONAL_ID,
    ),
    # Tax identifiers
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:tax\s*(?:no\.?|number|reference|id|record)|tin"
            r"|vat\s*(?:no\.?|number|id)|mã\s*số\s*thuế|nomor\s*pajak|税号)"
            rf"(?![a-z0-9_])\s*(?:is)?{_SEPARATOR}({_HAS_DIGIT}[A-Z0-9-]{{6,20}})(?![a-z0-9_])"
        ),
        EntityType.TAX_ID,
    ),
    # Passports
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:passport\s*(?:no\.?|number|#)?|护照号|paspor)"
            rf"(?![a-z0-9_]){_SEPARATOR}({_HAS_DIGIT}[A-Z0-9-]{{6,15}})(?![a-z0-9_])"
        ),
        EntityType.NATIONAL_ID,
    ),
    # Driving licences
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:driver'?s?\s*licen[sc]e|driving\s*licen[sc]e|nomor\s*SIM"
            r"|số\s*giấy\s*phép\s*lái\s*xe)"
            rf"\s*(?:no\.?|number|#)?(?![a-z0-9_]){_SEPARATOR}"
            rf"({_HAS_DIGIT}[A-Z0-9-]{{6,15}})(?![a-z0-9_])"
        ),
        EntityType.NATIONAL_ID,
    ),
    # Reference numbers a support or billing system prints next to a label.
    # The label must carry an explicit "number" marker, so "the serial drama"
    # and "reference the attached document" cannot match.
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:ticket|receipt|serial|reference|case|customer|user|member)"
            r"\s*(?:id|no\.?|number|#)"
            rf"(?![a-z0-9_])\s*(?:is)?{_SEPARATOR}({_HAS_DIGIT}[A-Z0-9-]{{6,16}})(?![a-z0-9_])"
        ),
        EntityType.NATIONAL_ID,
    ),
    # Postal codes
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:zip\s*code|postal\s*code|postcode|zip|cap)"
            rf"(?![a-z0-9_]){_SEPARATOR}\(?([0-9]{{5,6}})\)?(?![a-z0-9_])"
        ),
        EntityType.LOCATION,
    ),
    # Account, policy, and insurance numbers
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:account|policy|insurance)\s*(?:no\.?|number|#)"
            rf"(?![a-z0-9_]){_SEPARATOR}({_HAS_DIGIT}[A-Z0-9-]{{6,16}})(?![a-z0-9_])"
        ),
        EntityType.SECRET,
    ),
    # Payment cards that fail Luhn, which synthetic and redacted test data often
    # do. The label must name a card, never an unrelated amount.
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:credit\s*card|debit\s*card|card\s*number|visa|mastercard"
            r"|maestro|amex)"
            rf"\s*(?:no\.?|number|ending\s*in|#)?(?![a-z0-9_]){_SEPARATOR}"
            r"(\d{13,19})(?![a-z0-9_])"
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
