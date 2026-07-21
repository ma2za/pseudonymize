from dataclasses import dataclass

from pseudonymize.result import Detection


@dataclass(frozen=True, slots=True)
class RedactTransformer:
    def transform(self, value: str, detection: Detection) -> str:
        return f"<{detection.entity_type.value}>"
