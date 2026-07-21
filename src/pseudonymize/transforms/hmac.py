import secrets

_MINIMUM_KEY_BYTES = 32


def generate_key() -> bytes:
    return secrets.token_bytes(_MINIMUM_KEY_BYTES)
