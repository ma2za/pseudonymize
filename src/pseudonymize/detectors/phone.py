import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_PHONE = re.compile(r"(?<![\w+])(?:\+\d{1,3}[ .()-]*)?(?:\d[ .()-]*){6,14}\d(?!\w)")


def _credible_phone(value: str) -> bool:
    digits = "".join(character for character in value if character.isdigit())
    if not 7 <= len(digits) <= 15 or len(set(digits)) == 1:
        return False
    separators = sum(character in " .()-" for character in value)
    return value.startswith("+") or separators >= 2


@dataclass(frozen=True, slots=True)
class PhoneDetector:
    name: str = "phone"

    def detect(self, text: str) -> list[Detection]:
        return [
            Detection(EntityType.PHONE, match.start(), match.end(), 0.86, self.name)
            for match in _PHONE.finditer(text)
            if _credible_phone(match.group())
        ]
