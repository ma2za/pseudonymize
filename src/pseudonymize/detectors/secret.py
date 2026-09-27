import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_SECRET_PATTERNS = (
    re.compile(r"(?<![A-Za-z0-9_])AKIA[0-9A-Z]{16}(?![A-Za-z0-9_])"),
    re.compile(r"(?<![A-Za-z0-9_])gh[pousr]_[A-Za-z0-9]{36,255}(?![A-Za-z0-9_])"),
    re.compile(r"(?<![A-Za-z0-9_])sk-[A-Za-z0-9_-]{20,}(?![A-Za-z0-9_])"),
    re.compile(
        r"(?i)(?<![a-z0-9_])(?:api[_-]?key|client[_-]?secret|password|secret|token)(?![a-z0-9_])\s*[:=]\s*"
        r"(?P<value>['\"]?[A-Za-z0-9_./+=-]{8,}['\"]?)"
    ),
)


@dataclass(frozen=True, slots=True)
class SecretDetector:
    name: str = "secret"

    def detect(self, text: str) -> list[Detection]:
        detections: list[Detection] = []
        if "AKIA" in text:
            detections.extend(
                Detection(EntityType.SECRET, match.start(), match.end(), 0.96, self.name)
                for match in _SECRET_PATTERNS[0].finditer(text)
            )
        if "gh" in text:
            detections.extend(
                Detection(EntityType.SECRET, match.start(), match.end(), 0.96, self.name)
                for match in _SECRET_PATTERNS[1].finditer(text)
            )
        if "sk-" in text:
            detections.extend(
                Detection(EntityType.SECRET, match.start(), match.end(), 0.96, self.name)
                for match in _SECRET_PATTERNS[2].finditer(text)
            )
        if ":" in text or "=" in text:
            for match in _SECRET_PATTERNS[3].finditer(text):
                start, end = match.span("value")
                if text[start : start + 1] in {'"', "'"}:
                    start += 1
                if text[end - 1 : end] in {'"', "'"}:
                    end -= 1
                detections.append(Detection(EntityType.SECRET, start, end, 0.96, self.name))
        return detections
