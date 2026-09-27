"""Evidence fusion and arbitration for 1.33.0 model bake-off.

Extracts candidate evidence features and arbitrates detection conflicts
while preserving hard safety precedence for mathematically validated identifiers.
"""

from __future__ import annotations

from dataclasses import dataclass

from pseudonymize.result import Detection

# Provenance weights for evidence fusion
PROVENANCE_WEIGHTS: dict[str, float] = {
    "checksum": 1.0,
    "credentials": 0.95,
    "email": 0.90,
    "ip": 0.90,
    "ml_onnx": 0.85,
    "secret": 0.80,
    "phone": 0.70,
    "context": 0.60,
    "gazetteer": 0.55,
    "heuristics": 0.50,
    "coreference": 0.45,
}

MATHEMATICALLY_VALIDATED_DETECTORS = frozenset(
    {"iban", "payment_card", "algorithmic_checksum", "italian_code", "german_id"}
)


@dataclass(frozen=True)
class CandidateEvidence:
    """Feature vector representing detection evidence for multi-backend arbitration."""

    detection: Detection
    is_mathematically_validated: bool
    provenance_weight: float
    context_polarity: float  # +1.0 for positive context, -1.0 for negative, 0.0 neutral
    span_length: int
    backend_agreement_count: int

    def compute_fused_score(
        self,
        w_prob: float = 0.50,
        w_prov: float = 0.30,
        w_ctx: float = 0.15,
        w_agree: float = 0.05,
    ) -> float:
        """Compute inspectable linear evidence score."""
        # Hard Safety Precedence: mathematically validated checksums cannot be overridden
        if self.is_mathematically_validated:
            return 10.0 + self.detection.confidence

        score = (
            w_prob * self.detection.confidence
            + w_prov * self.provenance_weight
            + w_ctx * self.context_polarity
            + w_agree * min(self.backend_agreement_count, 3)
        )
        return float(score)


def extract_candidate_evidence(
    detection: Detection,
    context_polarity: float = 0.0,
    agreement_count: int = 1,
) -> CandidateEvidence:
    """Extract evidence features for a detection candidate."""
    det_name = detection.detector.lower()
    is_validated = det_name in MATHEMATICALLY_VALIDATED_DETECTORS

    # Determine provenance weight
    prov_weight = 0.50
    for key, weight in PROVENANCE_WEIGHTS.items():
        if key in det_name or (detection.backend and key in detection.backend.lower()):
            prov_weight = weight
            break

    span_len = max(0, detection.end - detection.start)

    return CandidateEvidence(
        detection=detection,
        is_mathematically_validated=is_validated,
        provenance_weight=prov_weight,
        context_polarity=context_polarity,
        span_length=span_len,
        backend_agreement_count=agreement_count,
    )


def arbitrate_conflicts(
    candidates: list[CandidateEvidence],
) -> list[CandidateEvidence]:
    """Arbitrate overlapping candidate detections using evidence fusion.

    Enforces:
    1. Mathematically validated identifiers (e.g. Luhn, Verhoeff, IBAN Mod97) always win.
    2. Higher fused evidence score wins among overlapping spans.
    3. Deterministic tie-breaking by start position and entity type.
    """
    if not candidates:
        return []

    # Sort candidates by fused score descending
    scored = sorted(
        candidates,
        key=lambda c: (
            c.compute_fused_score(),
            -c.detection.start,
            -(c.detection.end - c.detection.start),
        ),
        reverse=True,
    )

    selected: list[CandidateEvidence] = []
    occupied_intervals: list[tuple[int, int]] = []

    for cand in scored:
        c_start = cand.detection.start
        c_end = cand.detection.end

        # Check overlap
        overlaps = False
        for o_start, o_end in occupied_intervals:
            if max(c_start, o_start) < min(c_end, o_end):
                overlaps = True
                break

        if not overlaps:
            selected.append(cand)
            occupied_intervals.append((c_start, c_end))

    # Return in document start order
    return sorted(selected, key=lambda c: (c.detection.start, c.detection.end))
