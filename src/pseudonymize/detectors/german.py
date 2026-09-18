import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

# Matches 11-digit German Tax ID, e.g. 12 345 678 901 or 12345678901
_GERMAN_TIN_RX = re.compile(
    r"(?<![0-9])([1-9][0-9]{10}|[1-9][0-9]{1}[ ]?[0-9]{3}[ ]?[0-9]{3}[ ]?[0-9]{3})(?![0-9])"
)


def _valid_german_tin(tin_raw: str) -> bool:
    tin = tin_raw.replace(" ", "").replace("-", "")
    if len(tin) != 11 or not tin.isdigit() or tin[0] == "0":
        return False

    # Check digit constraints for the first 10 digits:
    # Under German central tax law, exactly one digit must occur 2 or 3 times,
    # or multiple duplicates under specific transition scenarios.
    first_10 = tin[:10]
    counts = [first_10.count(str(d)) for d in range(10)]
    if not any(c in (2, 3) for c in counts):
        return False

    # ISO 7064 Mod 11,10 custom German tax checksum
    product = 10
    for char in first_10:
        digit = int(char)
        sum_val = (digit + product) % 10
        if sum_val == 0:
            sum_val = 10
        product = (sum_val * 2) % 11

    checksum = 11 - product
    if checksum == 10:
        checksum = 0
    return checksum == int(tin[10])


@dataclass(frozen=True, slots=True)
class GermanTINDetector:
    name: str = "german_tin"

    def detect(self, text: str) -> list[Detection]:
        return [
            Detection(EntityType.TAX_ID, match.start(), match.end(), 1.0, self.name)
            for match in _GERMAN_TIN_RX.finditer(text)
            if _valid_german_tin(match.group())
        ]
