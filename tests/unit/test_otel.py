import logging
from typing import Any

from pseudonymize import DlpLoggingFilter, OTelRedactionSpanProcessor


def test_dlp_logging_filter() -> None:
    # Set up standard logger
    logger = logging.getLogger("test_dlp_logger")
    logger.setLevel(logging.INFO)

    # Capture log outputs
    from io import StringIO

    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)

    # Add our DLP filter
    dlp_filter = DlpLoggingFilter()
    logger.addFilter(dlp_filter)

    try:
        # Log a message containing PII
        logger.info("My email is john.smith@example.com and phone is +39 333 123 4567.")
        log_output = log_stream.getvalue().strip()

        # Verify that PII is successfully redacted in the printed log!
        assert "john.smith@example.com" not in log_output
        assert "+39 333 123 4567" not in log_output
        assert "My email is" in log_output
    finally:
        logger.removeFilter(dlp_filter)
        logger.removeHandler(handler)


def test_otel_redaction_span_processor() -> None:
    class MockSpan:
        def __init__(self, attributes: dict[str, Any]):
            self.attributes = attributes

    # A mock span with initial PII attributes
    span = MockSpan(
        attributes={
            "user.email": "john.smith@example.com",
            "db.query": "SELECT * FROM users WHERE email = 'john.smith@example.com'",
            "server.port": 8080,  # non-string must be preserved untouched
            "user.roles": ["admin", "john.smith@example.com"],  # list of strings
        }
    )

    processor = OTelRedactionSpanProcessor()

    # Process span lifecycle events
    processor.on_start(span)
    processor.on_end(span)

    # Verify that PII is redacted from attributes
    assert span.attributes["user.email"] != "john.smith@example.com"
    assert "john.smith@example.com" not in span.attributes["db.query"]
    assert span.attributes["server.port"] == 8080  # preserved
    assert span.attributes["user.roles"][0] == "admin"
    assert span.attributes["user.roles"][1] != "john.smith@example.com"
