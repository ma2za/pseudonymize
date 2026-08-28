from collections.abc import Sequence
from dataclasses import dataclass

from pseudonymize.backends.base import BackendCapabilities
from pseudonymize.detectors import DEFAULT_DETECTORS, Detector
from pseudonymize.document import ContentBlock
from pseudonymize.policy import Policy
from pseudonymize.result import Detection, EntityType

_RULE_ENTITY_TYPES = frozenset(
    {
        EntityType.EMAIL,
        EntityType.PHONE,
        EntityType.IP_ADDRESS,
        EntityType.IBAN,
        EntityType.PAYMENT_CARD,
        EntityType.NATIONAL_ID,
        EntityType.TAX_ID,
        EntityType.URL_CREDENTIAL,
        EntityType.SECRET,
        EntityType.LOCATION,
    }
)


@dataclass(frozen=True, slots=True)
class RulesBackend:
    detectors: Sequence[Detector] = DEFAULT_DETECTORS
    name: str = "rules"
    allow_remote_processing: bool = False

    def __post_init__(self) -> None:
        object.__setattr__(self, "detectors", tuple(self.detectors))

    @property
    def capabilities(self) -> BackendCapabilities:
        return BackendCapabilities(_RULE_ENTITY_TYPES)

    def detect(self, block: ContentBlock, policy: Policy) -> tuple[Detection, ...]:
        return tuple(
            detection
            for detector in self.detectors
            for detection in detector.detect(block.text)
            if detection.entity_type in policy.entity_types
            and detection.confidence >= policy.minimum_confidence
        )
