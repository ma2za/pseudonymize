import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum


class EntityType(StrEnum):
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    IP_ADDRESS = "IP_ADDRESS"
    IBAN = "IBAN"
    PAYMENT_CARD = "PAYMENT_CARD"
    URL_CREDENTIAL = "URL_CREDENTIAL"
    SECRET = "SECRET"  # noqa: S105


@dataclass(frozen=True, slots=True)
class Detection:
    entity_type: EntityType
    start: int
    end: int
    confidence: float
    detector: str
    backend: str = ""

    def __post_init__(self) -> None:
        if self.start < 0 or self.end <= self.start:
            raise ValueError("detection offsets must describe a non-empty span")
        if not 0 <= self.confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True, slots=True)
class Replacement:
    detection: Detection
    output_start: int
    output_end: int
    token: str


@dataclass(frozen=True, slots=True)
class Result:
    text: str
    replacements: tuple[Replacement, ...]
    mapping: Mapping[str, str] | None = field(default=None, repr=False, compare=False)

    def restore(self, text: str) -> str:
        mapping = self.mapping
        if mapping is None:
            raise ValueError("restoration requires include_mapping=True during processing")
        if not mapping:
            return text
        placeholders = sorted(mapping, key=len, reverse=True)
        pattern = re.compile("|".join(re.escape(placeholder) for placeholder in placeholders))
        return pattern.sub(lambda match: mapping[match.group()], text)
