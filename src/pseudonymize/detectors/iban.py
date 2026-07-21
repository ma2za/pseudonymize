import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_IBAN = re.compile(r"(?<![A-Z0-9])[A-Z]{2}\d{2}(?:[ ]?[A-Z0-9]){11,30}(?![A-Z0-9])", re.I)


def _valid_mod97(value: str) -> bool:
    compact = "".join(value.split()).upper()
    if not 15 <= len(compact) <= 34:
        return False
    rearranged = compact[4:] + compact[:4]
    remainder = 0
    for character in rearranged:
        digits = str(ord(character) - 55) if character.isalpha() else character
        for digit in digits:
            remainder = (remainder * 10 + int(digit)) % 97
    return remainder == 1


@dataclass(frozen=True, slots=True)
class IbanDetector:
    name: str = "iban"

    def detect(self, text: str) -> list[Detection]:
        return [
            Detection(EntityType.IBAN, match.start(), match.end(), 1.0, self.name)
            for match in _IBAN.finditer(text)
            if _valid_mod97(match.group())
        ]
