import ipaddress
import re
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_IP_CANDIDATE = re.compile(
    r"(?<![\w:.])(?:\d{1,3}(?:\.\d{1,3}){3}|[0-9A-Fa-f]{0,4}:[0-9A-Fa-f:]+)(?![\w:.])"
)


@dataclass(frozen=True, slots=True)
class IpAddressDetector:
    name: str = "ip_address"

    def detect(self, text: str) -> list[Detection]:
        detections: list[Detection] = []
        for match in _IP_CANDIDATE.finditer(text):
            try:
                ipaddress.ip_address(match.group())
            except ValueError:
                continue
            detections.append(
                Detection(EntityType.IP_ADDRESS, match.start(), match.end(), 0.99, self.name)
            )
        return detections
