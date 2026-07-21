import base64
import hashlib
import hmac
import secrets
from dataclasses import dataclass, field

from pseudonymize.exceptions import InvalidKeyError
from pseudonymize.normalization import normalize
from pseudonymize.result import Detection

_MINIMUM_KEY_BYTES = 32


def generate_key() -> bytes:
    return secrets.token_bytes(_MINIMUM_KEY_BYTES)


@dataclass(frozen=True, slots=True)
class HmacTransformer:
    key: bytes = field(repr=False)
    namespace: str = "default"

    def __post_init__(self) -> None:
        if len(self.key) < _MINIMUM_KEY_BYTES:
            raise InvalidKeyError("key must contain at least 32 bytes")
        if "\0" in self.namespace:
            raise ValueError("namespace must not contain NUL characters")

    def transform(self, value: str, detection: Detection) -> str:
        normalized = normalize(value, detection.entity_type)
        payload = b"\x00".join(
            (
                b"PZ1",
                self.namespace.encode("utf-8"),
                detection.entity_type.value.encode("ascii"),
                normalized.encode("utf-8"),
            )
        )
        digest = hmac.new(self.key, payload, hashlib.sha256).digest()
        alias = base64.b32encode(digest).decode("ascii")[:16]
        return f"<PZ1:{detection.entity_type.value}:{alias}>"
