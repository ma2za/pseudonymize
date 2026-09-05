from collections.abc import Sequence

from pseudonymize.engine import Pseudonymizer
from pseudonymize.policy import Policy


def assert_no_pii(text: str, policy: Policy | None = None) -> None:
    engine = Pseudonymizer()
    if policy is not None:  # pragma: no cover
        engine.policy = policy

    result = engine.process(text)
    if result.replacements:
        types = [rep.detection.entity_type.name for rep in result.replacements]
        type_counts = {t: types.count(t) for t in set(types)}
        summary = ", ".join(f"{count}x {t}" for t, count in sorted(type_counts.items()))
        raise AssertionError(f"PII boundary violation: detected {summary} in output.")


def assert_no_values(text: str, seeded_values: Sequence[str]) -> None:
    found = sum(1 for val in seeded_values if val in text)
    if found:
        raise AssertionError(
            f"Canary boundary violation: {found} seeded values leaked into output."
        )
