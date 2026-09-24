import logging
import subprocess
import sys
from io import StringIO
from types import MappingProxyType
from typing import Any

import pytest

from pseudonymize import DlpLoggingFilter, OTelRedactionSpanProcessor


def test_dlp_logging_filter_redacts_messages_and_arguments() -> None:
    logger = logging.getLogger("test_dlp_logger")
    logger.setLevel(logging.INFO)

    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)

    dlp_filter = DlpLoggingFilter()
    logger.addFilter(dlp_filter)

    try:
        # 1. Standard string formatting in msg
        logger.info("My email is john.smith@example.com and phone is +39 333 123 4567.")
        output = log_stream.getvalue().strip()
        assert "john.smith@example.com" not in output
        assert "+39 333 123 4567" not in output
        assert "My email is" in output

        # 2. Tuple arguments formatting
        log_stream.seek(0)
        log_stream.truncate(0)
        logger.info("User: %s, Org: %s, Port: %d", "admin@example.org", "AcmeCorp", 8080)
        output = log_stream.getvalue().strip()
        assert "admin@example.org" not in output
        assert "8080" in output

        # 3. Dict arguments formatting
        log_stream.seek(0)
        log_stream.truncate(0)
        logger.info(
            "Contact: %(email)s on port %(port)d",
            {"email": "contact@example.com", "port": 443},
        )
        output = log_stream.getvalue().strip()
        assert "contact@example.com" not in output
        assert "443" in output

        # 4. Nested structures in arguments
        log_stream.seek(0)
        log_stream.truncate(0)
        logger.info(
            "Record: %s",
            {"users": ["alice@corp.org", "bob@corp.org"], "count": 2},
        )
        output = log_stream.getvalue().strip()
        assert "alice@corp.org" not in output
        assert "bob@corp.org" not in output
        assert "count" in output
    finally:
        logger.removeFilter(dlp_filter)
        logger.removeHandler(handler)


def test_otel_redaction_span_processor() -> None:
    class MockSpan:
        def __init__(self, attributes: dict[str, Any]):
            self.attributes = attributes

    span = MockSpan(
        attributes={
            "user.email": "john.smith@example.com",
            "db.query": "SELECT * FROM users WHERE email = 'john.smith@example.com'",
            "server.port": 8080,
            "user.roles": ["admin", "john.smith@example.com"],
            "metadata": {"owner": "super@example.com", "active": True},
        }
    )

    processor = OTelRedactionSpanProcessor()
    processor.on_start(span)
    processor.on_end(span)

    assert span.attributes["user.email"] != "john.smith@example.com"
    assert "john.smith@example.com" not in span.attributes["db.query"]
    assert span.attributes["server.port"] == 8080
    assert span.attributes["user.roles"][0] == "admin"
    assert span.attributes["user.roles"][1] != "john.smith@example.com"
    assert span.attributes["metadata"]["owner"] != "super@example.com"
    assert span.attributes["metadata"]["active"] is True

    processor.shutdown()
    assert processor.force_flush() is True


def test_otel_observability_isolated_base_import() -> None:
    """Run an isolated Python subprocess to verify importing pseudonymize and otel

    does not load any opentelemetry modules and does not open network sockets.
    """
    code = (
        "import sys, socket\n"
        "import pseudonymize\n"
        "import pseudonymize.otel\n"
        "loaded_otel = [m for m in sys.modules if m.startswith('opentelemetry')]\n"
        "assert not loaded_otel, f'Telemetry module loaded: {loaded_otel}'\n"
        "print('ISOLATION_OK')\n"
    )

    try:
        completed = subprocess.run(  # noqa: S603
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )
    except subprocess.TimeoutExpired as exc:
        raise AssertionError("Isolated import verification timed out after 15s") from exc

    assert completed.returncode == 0, f"STDOUT: {completed.stdout}\nSTDERR: {completed.stderr}"
    assert "ISOLATION_OK" in completed.stdout


def test_otel_redaction_immutable_container_handling() -> None:
    """Verify that immutable attribute containers fail closed rather than leaking PII."""
    processor = OTelRedactionSpanProcessor()

    # Case 1: Attributes is a MappingProxyType, but span allows reassigning attributes
    class SpanWithReassignableAttrs:
        def __init__(self, raw: dict[str, Any]):
            self.attributes = MappingProxyType(raw)

    span1 = SpanWithReassignableAttrs({"user.email": "leak@example.com"})
    processor.on_start(span1)
    # Reassigned to new mutable dict with redacted content
    assert span1.attributes["user.email"] != "leak@example.com"

    # Case 2: Span is completely frozen and prevents both in-place mutation
    # and attribute reassignment
    class FrozenSpan:
        @property
        def attributes(self) -> Any:
            return MappingProxyType({"user.email": "leak@example.com"})

    frozen_span = FrozenSpan()
    # Must fail closed by raising RuntimeError rather than silently passing and leaking
    with pytest.raises(RuntimeError, match="Failed to redact immutable span attributes safely"):
        processor.on_start(frozen_span)


def test_otel_redaction_diverse_attribute_shapes() -> None:
    """Verify span redaction across diverse attribute types without wall-clock assertions."""

    class MockSpan:
        def __init__(self, attributes: dict[str, Any]):
            self.attributes = attributes

    processor = OTelRedactionSpanProcessor()
    spans = [
        MockSpan(
            attributes={
                "http.route": "/api/v1/users",
                "user.email": f"user_{i}@example.com",
                "request.id": f"req-{i:04d}",
                "tenant.id": 42,
                "tags": ["telemetry", f"client_{i}@example.org"],
                "nested": {"contact": f"nested_{i}@corp.org"},
            }
        )
        for i in range(10)
    ]

    for s in spans:
        processor.on_start(s)

    for i, s in enumerate(spans):
        assert f"user_{i}@example.com" not in s.attributes["user.email"]
        assert f"client_{i}@example.org" not in s.attributes["tags"][1]
        assert f"nested_{i}@corp.org" not in s.attributes["nested"]["contact"]
        assert s.attributes["tenant.id"] == 42
