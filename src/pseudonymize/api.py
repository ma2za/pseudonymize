from pseudonymize.detectors import DEFAULT_DETECTORS
from pseudonymize.engine import Pseudonymizer
from pseudonymize.policy import Policy
from pseudonymize.transforms import RedactTransformer, generate_key


def pseudonymize(
    text: str, *, key: bytes, namespace: str = "default", policy: Policy | None = None
) -> str:
    return Pseudonymizer(key=key, namespace=namespace, policy=policy).process(text).text


def redact(text: str, *, policy: Policy | None = None) -> str:
    return (
        Pseudonymizer(
            key=b"\0" * 32,
            policy=policy,
            detectors=DEFAULT_DETECTORS,
            transformer=RedactTransformer(),
        )
        .process(text)
        .text
    )


__all__ = ["generate_key", "pseudonymize", "redact"]
