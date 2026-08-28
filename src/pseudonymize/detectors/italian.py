import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_OMOCODIA_DIGITS = str.maketrans("LMNPQRSTUV", "0123456789")
_FISCAL_CODE = re.compile(
    r"(?<![A-Z0-9])"
    r"[A-Z]{6}[0-9LMNPQRSTUV]{2}[ABCDEHLMPRST][0-9LMNPQRSTUV]{2}"
    r"[A-Z][0-9LMNPQRSTUV]{3}[A-Z]"
    r"(?![A-Z0-9])",
    re.I,
)
_ODD_VALUES = dict(
    zip(
        "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        (
            1,
            0,
            5,
            7,
            9,
            13,
            15,
            17,
            19,
            21,
            1,
            0,
            5,
            7,
            9,
            13,
            15,
            17,
            19,
            21,
            2,
            4,
            18,
            20,
            11,
            3,
            6,
            8,
            12,
            14,
            16,
            10,
            22,
            25,
            24,
            23,
        ),
        strict=True,
    )
)
_EVEN_VALUES = {
    **{character: value for value, character in enumerate("0123456789")},
    **{character: value for value, character in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")},
}
_VAT_WITH_COUNTRY = re.compile(
    r"(?<![A-Z0-9])(?P<value>IT[ ]?(?:\d[ ]?){10}\d)(?![A-Z0-9])",
    re.I,
)
_VAT_WITH_LABEL = re.compile(
    r"(?<![a-z0-9_])(?:partita[ ]+iva|p[ .]*iva|p[ .]*i[ .]*|vat(?:[ ]+id)?)"
    r"\s*[:=]?\s*(?P<value>(?:IT[ ]?)?(?:\d[ ]?){10}\d)(?!\d)",
    re.I,
)


def _valid_fiscal_code(value: str) -> bool:
    compact = value.upper()
    day_text = compact[9:11].translate(_OMOCODIA_DIGITS)
    day = int(day_text)
    if not (1 <= day <= 31 or 41 <= day <= 71):
        return False
    total = sum(
        (_ODD_VALUES if index % 2 == 0 else _EVEN_VALUES)[character]
        for index, character in enumerate(compact[:15])
    )
    return compact[-1] == chr(ord("A") + total % 26)


def _valid_vat(value: str) -> bool:
    compact = "".join(character for character in value if character.isdigit())
    if len(compact) != 11 or len(set(compact)) == 1:
        return False
    total = sum(int(character) for character in compact[:10:2])
    for character in compact[1:10:2]:
        doubled = int(character) * 2
        total += doubled - 9 if doubled > 9 else doubled
    return (10 - total % 10) % 10 == int(compact[-1])


@dataclass(frozen=True, slots=True)
class ItalianFiscalCodeDetector:
    name: str = "italian_fiscal_code"

    def detect(self, text: str) -> list[Detection]:
        return [
            Detection(EntityType.NATIONAL_ID, match.start(), match.end(), 1.0, self.name)
            for match in _FISCAL_CODE.finditer(text)
            if _valid_fiscal_code(match.group())
        ]


@dataclass(frozen=True, slots=True)
class ItalianVATDetector:
    name: str = "italian_vat"

    def detect(self, text: str) -> list[Detection]:
        spans = {
            match.span("value")
            for pattern in (_VAT_WITH_COUNTRY, _VAT_WITH_LABEL)
            for match in pattern.finditer(text)
            if _valid_vat(match.group("value"))
        }
        return [
            Detection(EntityType.TAX_ID, start, end, 1.0, self.name) for start, end in sorted(spans)
        ]
