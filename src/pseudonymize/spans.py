from collections.abc import Iterable

from pseudonymize.result import Detection, EntityType

_ENTITY_PRIORITY = {
    EntityType.PAYMENT_CARD: 70,
    EntityType.IBAN: 70,
    # URL credentials outrank emails: a password such as "s3cret" followed by
    # "@host" also matches the email pattern, and letting the email span win
    # would leave the "user:" part of the userinfo unmasked.
    EntityType.URL_CREDENTIAL: 65,
    EntityType.EMAIL: 60,
    EntityType.IP_ADDRESS: 60,
    EntityType.SECRET: 50,
    EntityType.PHONE: 40,
    EntityType.PERSON: 30,
    EntityType.ORGANIZATION: 30,
    EntityType.LOCATION: 30,
}


def resolve_overlaps(
    detections: Iterable[Detection], detector_priority: tuple[str, ...] = ()
) -> tuple[Detection, ...]:
    configured = {
        name: len(detector_priority) - index for index, name in enumerate(detector_priority)
    }
    ranked = sorted(
        detections,
        key=lambda detection: (
            -_ENTITY_PRIORITY[detection.entity_type],
            -detection.confidence,
            -configured.get(detection.detector, 0),
            -(detection.end - detection.start),
            detection.start,
            detection.end,
            detection.detector,
            detection.backend,
        ),
    )
    selected: list[Detection] = []
    for detection in ranked:
        if any(
            detection.start < existing.end and existing.start < detection.end
            for existing in selected
        ):
            continue
        selected.append(detection)
    return tuple(sorted(selected, key=lambda detection: (detection.start, detection.end)))
