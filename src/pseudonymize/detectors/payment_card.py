import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_CARD = re.compile(r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)")


def _valid_luhn(value: str) -> bool:
    digits = [int(character) for character in value if character.isdigit()]
    if not 13 <= len(digits) <= 19 or len(set(digits)) == 1:
        return False
    total = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


_HAS_DIGIT = re.compile(r"\d")
_TAX_CONTEXT_RX = re.compile(
    r"(?i)\b(?:tax\s*(?:id|no\.?|number|reference|code)?|tin|vat\s*(?:no\.?|number|id)?|pajak|thuế|fiscal|steuernummer|steuer-id|nif|cif|npwp|rfc|nit|rut|siren|siret|税号)\b"
)


@dataclass(frozen=True, slots=True)
class PaymentCardDetector:
    name: str = "payment_card"
    _accept_unverified: bool = False

    def detect(self, text: str) -> list[Detection]:
        if not _HAS_DIGIT.search(text):
            return []
        detections = []
        for match in _CARD.finditer(text):
            val = match.group()
            # Disambiguation: International phone numbers (often 12-16 digits with spaces/dashes)
            # frequently start with '00'. A valid PAN never starts with '00'.
            if val.startswith("00"):
                continue

            # If there's a '+' right before the match, it's definitely a phone number
            if match.start() > 0 and text[match.start() - 1] == "+":
                continue

            # Disambiguation: Preceding tax or fiscal markers explicitly identify tax/fiscal numbers
            if match.start() > 0:
                preceding = text[max(0, match.start() - 35) : match.start()]
                if _TAX_CONTEXT_RX.search(preceding):
                    continue

            if self._accept_unverified or _valid_luhn(val):
                detections.append(
                    Detection(EntityType.PAYMENT_CARD, match.start(), match.end(), 1.0, self.name)
                )
        return detections
