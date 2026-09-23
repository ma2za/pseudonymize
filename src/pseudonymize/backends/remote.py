import json
from collections.abc import Sequence
from urllib.parse import urlsplit

import httpx

from pseudonymize.backends.base import BackendCapabilities, DetectionBackend
from pseudonymize.document import ContentBlock
from pseudonymize.exceptions import BackendExecutionError
from pseudonymize.policy import Policy
from pseudonymize.result import Detection, EntityType


class HTTPRemoteBackend(DetectionBackend):
    """Optional HTTP-based remote detection backend.

    Sends configured content blocks and requested entity types to a caller-selected
    HTTPS endpoint. Redirects are not followed, transport errors are sanitized to
    prevent secret or plaintext leakage, and invocation requires explicit dual consent
    via NetworkPolicy and allow_remote_processing=True.

    Callers and applications are responsible for bounding content block sizes and
    configuring transport timeouts appropriate for the chosen provider.
    """

    def __init__(
        self,
        name: str,
        endpoint: str,
        entity_types: frozenset[EntityType],
        auth_token: str | None = None,
        timeout: float = 5.0,
        max_retries: int = 2,
    ) -> None:
        """Initialize the HTTP remote backend.

        Args:
            name: Identifier for this backend instance in reports.
            endpoint: Remote HTTPS endpoint URL.
            entity_types: Supported entity types declared by this backend.
            auth_token: Optional Bearer token for HTTP Authorization header.
            timeout: Request timeout in seconds (must be positive).
            max_retries: Maximum number of transport retry attempts (must not be negative).
        """
        parsed_endpoint = urlsplit(endpoint)
        if parsed_endpoint.scheme != "https" or not parsed_endpoint.netloc:
            raise ValueError("remote endpoint must be an HTTPS URL")
        if timeout <= 0:
            raise ValueError("remote timeout must be positive")
        if max_retries < 0:
            raise ValueError("remote retries must not be negative")
        self._name = name
        self._endpoint = endpoint
        self._capabilities = BackendCapabilities(entity_types, remote=True)
        self._auth_token = auth_token
        self._timeout = timeout
        self._max_retries = max_retries

    @property
    def name(self) -> str:
        return self._name

    @property
    def capabilities(self) -> BackendCapabilities:
        return self._capabilities

    @property
    def allow_remote_processing(self) -> bool:
        return True

    def detect(self, block: ContentBlock, policy: Policy) -> Sequence[Detection]:
        headers = {"Content-Type": "application/json"}
        if self._auth_token:
            headers["Authorization"] = f"Bearer {self._auth_token}"

        payload = {
            "text": block.text,
            "entity_types": [
                e.value for e in (policy.entity_types & self._capabilities.entity_types)
            ],
        }

        transport = httpx.HTTPTransport(retries=self._max_retries)
        with httpx.Client(
            transport=transport, timeout=self._timeout, follow_redirects=False
        ) as client:
            try:
                response = client.post(self._endpoint, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
            except httpx.RequestError as e:
                raise BackendExecutionError("remote request failed") from e
            except httpx.HTTPStatusError as e:
                raise BackendExecutionError("remote response was unsuccessful") from e
            except json.JSONDecodeError as e:
                raise BackendExecutionError("remote response was not valid JSON") from e

        detections: list[Detection] = []
        if not isinstance(data, dict) or "detections" not in data:
            return detections

        for item in data["detections"]:
            if not isinstance(item, dict):
                continue
            try:
                entity_type = EntityType(item["entity_type"])
                start = int(item["start"])
                end = int(item["end"])
                confidence = float(item.get("confidence", 1.0))

                detections.append(
                    Detection(
                        entity_type=entity_type,
                        start=start,
                        end=end,
                        confidence=confidence,
                        detector=self._name,
                    )
                )
            except (ValueError, KeyError, TypeError):
                continue

        return detections
