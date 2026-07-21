from collections.abc import Sequence

from pseudonymize.backends import DetectionBackend
from pseudonymize.engine import Pseudonymizer
from pseudonymize.policy import Policy
from pseudonymize.transforms import TransformationMode, generate_key


def pseudonymize(
    text: str,
    *,
    mode: TransformationMode | str = TransformationMode.NUMBERED,
    key: bytes | None = None,
    namespace: str = "default",
    policy: Policy | None = None,
    backends: Sequence[DetectionBackend] | None = None,
) -> str:
    return (
        Pseudonymizer(
            mode=mode,
            key=key,
            namespace=namespace,
            policy=policy,
            backends=backends,
        )
        .process(text)
        .text
    )


def redact(
    text: str,
    *,
    typed: bool = False,
    policy: Policy | None = None,
    backends: Sequence[DetectionBackend] | None = None,
) -> str:
    return (
        Pseudonymizer(
            mode=TransformationMode.REDACTED,
            policy=policy,
            backends=backends,
            typed_redaction=typed,
        )
        .process(text)
        .text
    )


__all__ = ["generate_key", "pseudonymize", "redact"]
