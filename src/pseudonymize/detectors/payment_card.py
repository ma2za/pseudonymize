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


@dataclass(frozen=True, slots=True)
class PaymentCardDetector:
    name: str = "payment_card"

    def detect(self, text: str) -> list[Detection]:
        return [
            Detection(EntityType.PAYMENT_CARD, match.start(), match.end(), 1.0, self.name)
            for match in _CARD.finditer(text)
            if _valid_luhn(match.group())
        ]
