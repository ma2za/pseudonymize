import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_EMAIL = re.compile(
    r"(?<![\w.+-])[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}(?![\w-])"
)


@dataclass(frozen=True, slots=True)
class EmailDetector:
    name: str = "email"

    def detect(self, text: str) -> list[Detection]:
        return [
            Detection(EntityType.EMAIL, match.start(), match.end(), 0.99, self.name)
            for match in _EMAIL.finditer(text)
            if len(match.group().partition("@")[0]) <= 64 and len(match.group()) <= 254
        ]
