import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_SPANISH_NIF_RX = re.compile(
    r"(?<![A-Z0-9])([XYZKLM]?[0-9]{7,8})[- ]?([A-Z])(?![A-Z0-9])",
    re.I,
)

_SPANISH_CIF_RX = re.compile(
    r"(?<![A-Z0-9])([ABCDEFGHJNPQRSUVW])[- ]?([0-9]{7})[- ]?([A-Z0-9])(?![A-Z0-9])",
    re.I,
)


def _valid_spanish_nif(digits_str: str, letter: str) -> bool:
    digits_str = digits_str.upper()
    letter = letter.upper()
    first_char = digits_str[0]

    if first_char.isdigit():
        digits = digits_str
    elif first_char in "XYZ":
        nie_prefix = {"X": "0", "Y": "1", "Z": "2"}[first_char]
        digits = nie_prefix + digits_str[1:]
    elif first_char in "KLM":
        digits = digits_str[1:]
    else:
        return False

    if not digits.isdigit():
        return False

    num = int(digits)
    expected_letter = "TRWAGMYFPDXBNJZSQVHLCKE"[num % 23]
    return letter == expected_letter


def _valid_spanish_cif(first_char: str, digits: str, control: str) -> bool:
    first_char = first_char.upper()
    control = control.upper()
    if not digits.isdigit():
        return False

    even_sum = 0
    odd_sum = 0
    for i, d_char in enumerate(digits):
        d = int(d_char)
        if i % 2 == 1:
            even_sum += d
        else:
            prod = d * 2
            odd_sum += prod // 10 + prod % 10

    total_sum = even_sum + odd_sum
    last_digit = total_sum % 10
    control_digit = (10 - last_digit) % 10

    letter_map = "JABCDEFGHI"
    expected_letter = letter_map[control_digit]

    return control == str(control_digit) or control == expected_letter


@dataclass(frozen=True, slots=True)
class SpanishNIFDetector:
    name: str = "spanish_nif"

    def detect(self, text: str) -> list[Detection]:
        detections = []
        for match in _SPANISH_NIF_RX.finditer(text):
            digits, letter = match.groups()
            if _valid_spanish_nif(digits, letter):
                detections.append(
                    Detection(EntityType.NATIONAL_ID, match.start(), match.end(), 1.0, self.name)
                )
        for match in _SPANISH_CIF_RX.finditer(text):
            prefix, digits, control = match.groups()
            if _valid_spanish_cif(prefix, digits, control):
                detections.append(
                    Detection(EntityType.TAX_ID, match.start(), match.end(), 1.0, self.name)
                )
        return sorted(detections, key=lambda d: d.start)
