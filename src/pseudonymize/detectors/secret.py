import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_SECRET_PATTERNS = (
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,255}\b"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(
        r"(?i)\b(?:api[_-]?key|client[_-]?secret|password|secret|token)\b\s*[:=]\s*"
        r"(?P<value>['\"]?[A-Za-z0-9_./+=-]{8,}['\"]?)"
    ),
)


@dataclass(frozen=True, slots=True)
class SecretDetector:
    name: str = "secret"

    def detect(self, text: str) -> list[Detection]:
        detections: list[Detection] = []
        for pattern in _SECRET_PATTERNS:
            for match in pattern.finditer(text):
                start, end = match.span("value") if "value" in pattern.groupindex else match.span()
                if text[start : start + 1] in {'"', "'"}:
                    start += 1
                if text[end - 1 : end] in {'"', "'"}:
                    end -= 1
                detections.append(Detection(EntityType.SECRET, start, end, 0.96, self.name))
        return detections
