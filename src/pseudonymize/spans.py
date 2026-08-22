import bisect
from collections.abc import Iterable

from pseudonymize.result import Detection, EntityType

_ENTITY_PRIORITY = {
    EntityType.PAYMENT_CARD: 70,
    EntityType.IBAN: 70,
    EntityType.EMAIL: 60,
    EntityType.IP_ADDRESS: 60,
    EntityType.URL_CREDENTIAL: 50,
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
    # Accepted spans are kept sorted and non-overlapping, so a candidate can
    # only collide with the span immediately before its insertion point.
    starts: list[int] = []
    ends: list[int] = []
    selected: list[Detection] = []
    for detection in ranked:
        index = bisect.bisect_left(starts, detection.end)
        if index and ends[index - 1] > detection.start:
            continue
        starts.insert(index, detection.start)
        ends.insert(index, detection.end)
        selected.append(detection)
    return tuple(sorted(selected, key=lambda detection: (detection.start, detection.end)))
