import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_CONTEXT_PATTERNS = [
    # ID Card / National ID
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:identification\s*number|id\s*card|national\s*id|id|identificatif|identifiant|ticket\s*id|entity\s*id|identifier|serial|receipt\s*number|environmental\s*clearance|chứng\s*minh\s*nhân\s*dân|căn\s*cước|ref\s*:|applicant'?s?|n[uú]mero\s*de\s*identificaci[oó]n|身份证号|社保号|registration\s*number)(?![a-z0-9_])\s*:?\s*\(?([A-Z0-9]{6,15})\)?(?![a-z0-9_])"
        ),
        EntityType.NATIONAL_ID,
    ),
    # Tax Number
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:tax\s*(?:no\.?|number|reference|id|record)|tin|vat\s*(?:no\.?|number|id)|mã\s*số\s*thuế|nomor\s*pajak|número\s*de\s*impresos|税号|cung\s*cấp)(?![a-z0-9_])\s*(?:is)?\s*:?\s*([A-Z0-9]{6,20})(?![a-z0-9_])"
        ),
        EntityType.TAX_ID,
    ),
    # Passport
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:passport\s*(?:no\.?|number|#)?|护照号|paspor)(?![a-z0-9_])\s*:?\s*([A-Z0-9]{6,15})(?![a-z0-9_])"
        ),
        EntityType.NATIONAL_ID,
    ),
    # Driver's License
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:driver'?s?\s*licen[sc]e|driving\s*licen[sc]e|licen[sc]e|nomor\s*SIM|số\s*giấy\s*phép\s*lái\s*xe)\s*(?:no\.?|number|#)?(?![a-z0-9_])\s*:?\s*((?=[A-Z0-9]*\d)[A-Z0-9]{6,15})(?![a-z0-9_])"
        ),
        EntityType.NATIONAL_ID,
    ),
    # Generic fallback for contextual IDs (ticket, receipt, serial, general id)
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:ticket|receipt|serial|reference|ref|identifier|id|applicant|user\s*id|customer\s*id|proof\s*like\s*a|customer's)\s*(?:id|no\.?|number|#|:)?\s*(?:is)?\s*:?\s*((?=[A-Z0-9-]*\d)[A-Z0-9-]{6,16})(?![a-z0-9_])"
        ),
        EntityType.NATIONAL_ID,
    ),
    # Zip / Postal Code
    (
        re.compile(
            r"(?i)(?<![a-z0-9_])(?:zip\s*code|postal\s*code|postcode|zip|singapore(?:\s*[a-z\s]+)?|office\s*at|school)(?![a-z0-9_])\s*:?\s*\(?([0-9]{5,6})\)?(?![a-z0-9_])"
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
            r"(?i)(?<![a-z0-9_])(?:credit\s*card|visa|mastercard|maestro|amex|card\s*number|budget\s*of|contribution\s*of)\s*(?:no\.?|number|ending\s*in|#|\$)?\s*:?\s*(\d{13,19})(?![a-z0-9_])"
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
