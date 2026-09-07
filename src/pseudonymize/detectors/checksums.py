import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

# Broad numerical shape extractors targeting formats that frequently contain checksums
# (e.g. 9-digit SSN-like, 11-digit CPF-like, 13-15 digit French NIR, etc.)
# We extract shapes, strip non-digits, and then apply strict mathematical validators.

_SHAPE_RX = re.compile(
    r"(?<!\d)"
    r"(?:"
    r"\d{9}"  # 9 digits (e.g., Mod-11/Luhn variants)
    r"|\d{11}"  # 11 digits (e.g., CPF, Mod-11 x2)
    r"|\d{14}"  # 14 digits (e.g., CNPJ)
    r"|\d{15}"  # 15 digits (e.g., IMEI Luhn)
    r"|\d{13,15}"  # French NIR is 13 or 15 (Mod 97)
    r"|\d{2}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}[-.\s]?\d{2}"  # CNPJ formatted
    r"|\d{3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{2}"  # CPF formatted
    r"|\d[A-Z0-9]{5,10}\d"  # Alphanumeric IDs
    r")"
    r"(?!\d)"
)

# We can also capture specific Tax ID formats. But wait, for v1.11.0, the prompt said:


# Let's start with a general Luhn (Mod-10) for 15-digit IMEI and 9-digit SIN.
def _valid_luhn(value: str) -> bool:
    digits = [int(character) for character in value if character.isdigit()]
    if len(set(digits)) == 1:
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


def _valid_mod11(value: str) -> bool:
    # Basic Mod 11: right-to-left weights 2,3,4,5,6,7,2,3...
    digits = [int(character) for character in value if character.isdigit()]
    if len(digits) < 2 or len(set(digits)) == 1:
        return False

    total = 0
    weight = 2
    for digit in reversed(digits[:-1]):
        total += digit * weight
        weight = weight + 1 if weight < 7 else 2

    rem = total % 11
    check = 11 - rem if rem > 1 else 0
    return check == digits[-1]


def _valid_verhoeff(value: str) -> bool:
    # Verhoeff algorithm for 12-digit Aadhaar
    digits = [int(c) for c in value if c.isdigit()]
    if len(digits) != 12 or len(set(digits)) == 1:
        return False

    d = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (1, 2, 3, 4, 0, 6, 7, 8, 9, 5),
        (2, 3, 4, 0, 1, 7, 8, 9, 5, 6),
        (3, 4, 0, 1, 2, 8, 9, 5, 6, 7),
        (4, 0, 1, 2, 3, 9, 5, 6, 7, 8),
        (5, 9, 8, 7, 6, 0, 4, 3, 2, 1),
        (6, 5, 9, 8, 7, 1, 0, 4, 3, 2),
        (7, 6, 5, 9, 8, 2, 1, 0, 4, 3),
        (8, 7, 6, 5, 9, 3, 2, 1, 0, 4),
        (9, 8, 7, 6, 5, 4, 3, 2, 1, 0),
    )
    p = (
        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9),
        (1, 5, 7, 6, 2, 8, 3, 0, 9, 4),
        (5, 8, 0, 3, 7, 9, 6, 1, 4, 2),
        (8, 9, 1, 6, 0, 4, 3, 5, 2, 7),
        (9, 4, 5, 3, 1, 2, 6, 8, 7, 0),
        (4, 2, 8, 6, 5, 7, 3, 9, 0, 1),
        (2, 7, 9, 3, 8, 0, 6, 4, 1, 5),
        (7, 0, 4, 6, 9, 1, 3, 2, 5, 8),
    )

    c = 0
    for i, num in enumerate(reversed(digits)):
        c = d[c][p[i % 8][num]]
    return c == 0


# Chinese Resident Identity Card (18 digits, Mod 11-2 variant)
def _valid_gb11643(value: str) -> bool:
    if len(value) != 18:
        return False
    weights = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    chars = "10X98765432"
    total = 0
    for i in range(17):
        if not value[i].isdigit():
            return False
        total += int(value[i]) * weights[i]
    return chars[total % 11] == value[17].upper()


_AADHAAR_RX = re.compile(r"(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}(?!\d)")
_CHINESE_ID_RX = re.compile(r"(?<!\d)\d{17}[\dX](?!\d)", re.I)
_GENERIC_9_11_RX = re.compile(r"(?<!\d)\d{3}[\s-]?\d{2,3}[\s-]?\d{3,4}(?!\d)")
_FRENCH_NIR_RX = re.compile(
    r"(?<!\d)[12]\s?\d{2}\s?(?:0[1-9]|1[0-2]|[23]\d)\s?(?:0[1-9]|[1-8]\d|9[0-5]|2[AB])\s?\d{3}\s?\d{3}\s?(?:\d{2})?(?!\d)",
    re.I,
)


def _valid_french_nir(value: str) -> bool:
    clean = "".join(c for c in value if c.isalnum()).upper()
    if len(clean) not in (13, 15):
        return False
    # Handle Corse 2A/2B
    base = clean[:13].replace("2A", "19").replace("2B", "18")
    if not base.isdigit():
        return False

    if len(clean) == 15:
        key = int(clean[13:])
        return key == (97 - (int(base) % 97))
    # If 13 digits, it's just the shape, maybe not verified, but we can accept it if we want.
    # Actually, French NIR always has the 2 digit key if it's full.
    return False


@dataclass(frozen=True, slots=True)
class AlgorithmicChecksumDetector:
    name: str = "checksum"

    def detect(self, text: str) -> list[Detection]:
        detections = [
            Detection(EntityType.NATIONAL_ID, match.start(), match.end(), 1.0, self.name)
            for match in _AADHAAR_RX.finditer(text)
            if _valid_verhoeff(match.group())
        ]
        detections.extend(
            Detection(EntityType.NATIONAL_ID, match.start(), match.end(), 1.0, self.name)
            for match in _CHINESE_ID_RX.finditer(text)
            if _valid_gb11643(match.group())
        )
        for match in _GENERIC_9_11_RX.finditer(text):
            val = match.group()
            clean = "".join(c for c in val if c.isdigit())
            if len(clean) == 9:
                if _valid_luhn(clean):
                    detections.append(
                        Detection(
                            EntityType.NATIONAL_ID, match.start(), match.end(), 1.0, self.name
                        )
                    )
                elif _valid_mod11(clean):
                    detections.append(
                        Detection(EntityType.TAX_ID, match.start(), match.end(), 1.0, self.name)
                    )
            elif len(clean) == 11 and _valid_mod11(clean):
                detections.append(
                    Detection(EntityType.TAX_ID, match.start(), match.end(), 1.0, self.name)
                )

        detections.extend(
            Detection(EntityType.NATIONAL_ID, match.start(), match.end(), 1.0, self.name)
            for match in _FRENCH_NIR_RX.finditer(text)
            if _valid_french_nir(match.group())
        )
        return detections
