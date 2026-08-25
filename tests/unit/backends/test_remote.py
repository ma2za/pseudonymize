import json
from unittest import mock

import httpx
import pytest

from pseudonymize.backends.remote import HTTPRemoteBackend
from pseudonymize.document import ContentBlock, TextOffsetLocation
from pseudonymize.exceptions import BackendExecutionError
from pseudonymize.policy import Policy
from pseudonymize.result import Detection, EntityType


@pytest.fixture
def mock_httpx() -> mock.MagicMock:
    with mock.patch("httpx.Client") as mock_client:
        yield mock_client


def test_http_remote_backend_initialization() -> None:
    backend = HTTPRemoteBackend(
        name="test_remote",
        endpoint="https://api.example.com/detect",
        entity_types=frozenset({EntityType.PERSON, EntityType.EMAIL}),
        auth_token="secret",
    )
    assert backend.name == "test_remote"
    assert backend.capabilities.remote is True
    assert backend.allow_remote_processing is True
    assert EntityType.PERSON in backend.capabilities.entity_types


def test_http_remote_backend_detect_success(mock_httpx: mock.MagicMock) -> None:
    backend = HTTPRemoteBackend(
        name="remote_llm",
        endpoint="https://api.example.com",
        entity_types=frozenset({EntityType.PERSON, EntityType.EMAIL}),
    )
    block = ContentBlock("id1", "Call Maria at maria@example.com", TextOffsetLocation(0, 31))
    
    mock_response = mock.MagicMock()
    mock_response.json.return_value = {
        "detections": [
            {"entity_type": "PERSON", "start": 5, "end": 10, "confidence": 0.9},
            {"entity_type": "EMAIL", "start": 14, "end": 31, "confidence": 1.0},
        ]
    }
    
    mock_client_instance = mock_httpx.return_value.__enter__.return_value
    mock_client_instance.post.return_value = mock_response
    
    detections = backend.detect(block, Policy.default())
    
    assert len(detections) == 2
    assert detections[0].entity_type is EntityType.PERSON
    assert detections[0].start == 5
    assert detections[0].end == 10
    assert detections[0].detector == "remote_llm"
    
    mock_client_instance.post.assert_called_once()
    args, kwargs = mock_client_instance.post.call_args
    assert kwargs["json"]["text"] == "Call Maria at maria@example.com"
    assert "PERSON" in kwargs["json"]["entity_types"]


def test_http_remote_backend_detect_auth(mock_httpx: mock.MagicMock) -> None:
    backend = HTTPRemoteBackend(
        name="remote_llm",
        endpoint="https://api.example.com",
        entity_types=frozenset({EntityType.PERSON}),
        auth_token="mytoken123"
    )
    block = ContentBlock("id1", "hello", TextOffsetLocation(0, 5))
    
    mock_response = mock.MagicMock()
    mock_response.json.return_value = {"detections": []}
    
    mock_client_instance = mock_httpx.return_value.__enter__.return_value
    mock_client_instance.post.return_value = mock_response
    
    backend.detect(block, Policy.default())
    
    args, kwargs = mock_client_instance.post.call_args
    assert kwargs["headers"]["Authorization"] == "Bearer mytoken123"


def test_http_remote_backend_http_error(mock_httpx: mock.MagicMock) -> None:
    backend = HTTPRemoteBackend("remote", "http://x", frozenset({EntityType.PERSON}))
    block = ContentBlock("id1", "hello", TextOffsetLocation(0, 5))
    
    mock_client_instance = mock_httpx.return_value.__enter__.return_value
    mock_client_instance.post.side_effect = httpx.RequestError("Connection failed")
    
    with pytest.raises(BackendExecutionError, match="HTTP request failed"):
        backend.detect(block, Policy.default())


def test_http_remote_backend_invalid_json(mock_httpx: mock.MagicMock) -> None:
    backend = HTTPRemoteBackend("remote", "http://x", frozenset({EntityType.PERSON}))
    block = ContentBlock("id1", "hello", TextOffsetLocation(0, 5))
    
    mock_response = mock.MagicMock()
    mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)
    
    mock_client_instance = mock_httpx.return_value.__enter__.return_value
    mock_client_instance.post.return_value = mock_response
    
    with pytest.raises(BackendExecutionError, match="Invalid JSON response"):
        backend.detect(block, Policy.default())


def test_http_remote_backend_handles_malformed_detections(mock_httpx: mock.MagicMock) -> None:
    backend = HTTPRemoteBackend("remote", "http://x", frozenset({EntityType.PERSON}))
    block = ContentBlock("id1", "hello", TextOffsetLocation(0, 5))
    
    mock_response = mock.MagicMock()
    mock_response.json.return_value = {
        "detections": [
            "not a dict",
            {"entity_type": "person", "start": "bad", "end": 10},
            {"entity_type": "unknown_type", "start": 0, "end": 5},
        ]
    }
    
    mock_client_instance = mock_httpx.return_value.__enter__.return_value
    mock_client_instance.post.return_value = mock_response
    
    detections = backend.detect(block, Policy.default())
    # Should safely skip the malformed ones and return empty list
    assert len(detections) == 0