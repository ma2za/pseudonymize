from enum import StrEnum


class TransformationMode(StrEnum):
    NUMBERED = "numbered"
    GENERIC = "generic"
    DETERMINISTIC = "deterministic"
    REDACTED = "redacted"
