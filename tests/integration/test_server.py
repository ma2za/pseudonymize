from typing import Any, cast

import pytest

try:
    from fastapi.testclient import TestClient

    from pseudonymize.server import app
except ImportError:
    app = cast(Any, None)
    _TestClient = cast(Any, None)
else:
    _TestClient = TestClient


@pytest.fixture
def client() -> Any:
    if app is None:
        pytest.skip("fastapi is not installed")
    return _TestClient(app)


def test_pseudonymize_endpoint(client: Any) -> None:
    response = client.post("/pseudonymize", json={"text": "Contact paolo@example.com."})
    assert response.status_code == 200
    data = response.json()
    assert "<EMAIL_1>" in data["text"]
    assert len(data["replacements"]) == 1
    assert data["replacements"][0]["entity_type"] == "EMAIL"
    assert data["replacements"][0]["token"] == "<EMAIL_1>"


def test_pseudonymize_endpoint_invalid(client: Any) -> None:
    response = client.post("/pseudonymize", json={"invalid": "payload"})
    assert response.status_code == 422  # FastAPI validation error


def test_pseudonymize_endpoint_internal_error(client: Any) -> None:
    from unittest.mock import patch

    with patch("pseudonymize.server._engine.process", side_effect=ValueError("Engine failed")):
        response = client.post("/pseudonymize", json={"text": "Contact paolo@example.com."})
        assert response.status_code == 400
        assert "Engine failed" in response.json()["detail"]
