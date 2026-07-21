import re
import urllib.parse
from dataclasses import dataclass

from pseudonymize.result import Detection, EntityType

_URL = re.compile(r"https?://[^\s<>\"']+", re.I)
_SENSITIVE_QUERY_NAMES = frozenset(
    {"access_token", "api_key", "apikey", "auth", "key", "password", "secret", "token"}
)


@dataclass(frozen=True, slots=True)
class UrlDetector:
    name: str = "url"

    def detect(self, text: str) -> list[Detection]:
        detections: list[Detection] = []
        for match in _URL.finditer(text):
            url = match.group().rstrip(".,;:!?)]}")
            parsed = urllib.parse.urlsplit(url)
            if parsed.username is not None or parsed.password is not None:
                authority_start = url.find("//") + 2
                at = url.find("@", authority_start)
                detections.append(
                    Detection(
                        EntityType.URL_CREDENTIAL,
                        match.start() + authority_start,
                        match.start() + at,
                        1.0,
                        self.name,
                    )
                )
            query_start = url.find("?") + 1
            if query_start == 0:
                continue
            cursor = query_start
            for item in url[query_start:].split("&"):
                name, separator, value = item.partition("=")
                if separator and urllib.parse.unquote_plus(name).lower() in _SENSITIVE_QUERY_NAMES:
                    value_start = cursor + len(name) + 1
                    if value:
                        detections.append(
                            Detection(
                                EntityType.URL_CREDENTIAL,
                                match.start() + value_start,
                                match.start() + value_start + len(value),
                                0.98,
                                self.name,
                            )
                        )
                cursor += len(item) + 1
        return detections
