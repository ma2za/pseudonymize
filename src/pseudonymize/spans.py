import bisect
from collections.abc import Iterable

from pseudonymize.result import Detection, EntityType

_ENTITY_PRIORITY = {
    EntityType.PAYMENT_CARD: 70,
    EntityType.IBAN: 70,
    EntityType.NATIONAL_ID: 70,
    EntityType.TAX_ID: 70,
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
    # Priority:
    # 3 if ML >= 0.95
    # 2 if local_rules
    # 1 otherwise

    ranked = sorted(
        detections,
        key=lambda detection: (
            -_ENTITY_PRIORITY[detection.entity_type],
            -configured.get(detection.detector, 0),
            -3 if (detection.backend == "local_onnx_pii" and detection.confidence >= 0.95)
            else -2 if detection.backend == "local_rules"
            else -1,
            -(detection.end - detection.start),
            -detection.confidence,
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

    sorted_selected = sorted(selected, key=lambda detection: (detection.start, detection.end))
    
    # Merge adjacent spans of the same entity type to prevent fragmentation.
    # Allow merging if the gap is just structural/whitespace (<= 2 chars).
    merged: list[Detection] = []
    for det in sorted_selected:
        if not merged:
            merged.append(det)
            continue
            
        last = merged[-1]
        
        # If same type, and strictly adjacent
        if last.entity_type == det.entity_type and det.start == last.end:
            merged[-1] = Detection(
                entity_type=last.entity_type,
                start=last.start,
                end=det.end,
                # Take highest confidence
                confidence=max(last.confidence, det.confidence),
                # Record as an ensemble merge
                detector="ensemble",
                backend="ensemble_merger"
            )
        else:
            merged.append(det)

    return tuple(merged)
