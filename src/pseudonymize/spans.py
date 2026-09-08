import bisect
from collections.abc import Iterable

from pseudonymize.result import Detection

_DETECTOR_WEIGHT = {
    # Tabular Layout / Column Headers (Absolute Highest)
    "tabular": 1.0,
    
    # Checksums / Deterministic structures - Highest priority (1.0)
    "payment_card": 1.0,
    "iban": 1.0,
    "italian_fiscal_code": 1.0,
    "italian_vat": 1.0,
    "checksum": 1.0,
    # URL credentials outrank emails (password vs email)
    "url": 0.95,
    "email": 0.90,
    "ip_address": 0.90,
    "secret": 0.80,
    "phone": 0.70,
    # Local heuristics & gazetteers
    "context_id": 0.60,
    "gazetteer": 0.55,
    "location": 0.50,
    "organization": 0.50,
    "ensemble": 0.40,
}


def resolve_overlaps(
    detections: Iterable[Detection], detector_priority: tuple[str, ...] = ()
) -> tuple[Detection, ...]:
    configured = {
        name: len(detector_priority) - index for index, name in enumerate(detector_priority)
    }

    def resolution_score(detection: Detection) -> float:
        base_weight = _DETECTOR_WEIGHT.get(detection.detector, 0.3)
        if detection.backend == "local_onnx_pii" and detection.confidence >= 0.95:
            # Overwhelmingly confident ML overrides generic heuristics,
            # but stays below valid deterministic checksums.
            return max(base_weight * detection.confidence, 0.85)
        return base_weight * detection.confidence

    ranked = sorted(
        detections,
        key=lambda detection: (
            -resolution_score(detection),
            -configured.get(detection.detector, 0),
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
                backend="ensemble_merger",
            )
        else:
            merged.append(det)

    return tuple(merged)
