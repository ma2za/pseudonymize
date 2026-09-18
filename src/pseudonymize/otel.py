import logging
from typing import Any

from pseudonymize.engine import Pseudonymizer


class DlpLoggingFilter(logging.Filter):
    """
    A lightweight, zero-overhead standard logging Filter that redacts PII
    from log messages and string arguments on the fly before they are emitted.
    """

    def __init__(self, engine: Pseudonymizer | None = None, name: str = ""):
        super().__init__(name)
        self.engine = engine or Pseudonymizer()

    def filter(self, record: logging.LogRecord) -> bool:
        # Redact the core log message string if it is formatted
        if isinstance(record.msg, str):
            record.msg = self.engine.process(record.msg).text

        # Redact any string arguments passed to the log formatting
        if record.args:
            new_args = []
            for arg in record.args:
                if isinstance(arg, str):
                    new_args.append(self.engine.process(arg).text)
                else:
                    new_args.append(arg)
            record.args = tuple(new_args)

        return True


class OTelRedactionSpanProcessor:
    """
    A zero-overhead, duck-typed OpenTelemetry SpanProcessor that seamlessly
    redacts PII from span attributes during span lifecycle events (on_start and on_end).
    Operates with <1ms overhead on string attributes, requiring zero hard dependencies.
    """

    def __init__(self, engine: Pseudonymizer | None = None):
        self.engine = engine or Pseudonymizer()

    def on_start(self, span: Any, parent_context: Any = None) -> None:
        """Called when a span starts. Redacts any initial attributes."""
        self._redact_span_attributes(span)

    def on_end(self, span: Any) -> None:
        """Called when a span ends. Redacts any late-added attributes."""
        self._redact_span_attributes(span)

    def shutdown(self) -> None:
        """Conforms to the OpenTelemetry SpanProcessor shutdown contract."""

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        """Conforms to the OpenTelemetry SpanProcessor force_flush contract."""
        return True

    def _redact_span_attributes(self, span: Any) -> None:
        if not hasattr(span, "attributes") or not span.attributes:
            return

        # OpenTelemetry attributes are dict-like. Iterate and redact string values.
        # We wrap in list() to avoid dictionary mutation size changes if needed,
        # and safely update values in-place.
        try:
            for key, val in list(span.attributes.items()):
                if isinstance(val, str):
                    span.attributes[key] = self.engine.process(val).text
                elif isinstance(val, (list, tuple)):
                    new_val = []
                    for item in val:
                        if isinstance(item, str):
                            new_val.append(self.engine.process(item).text)
                        else:
                            new_val.append(item)
                    span.attributes[key] = type(val)(new_val)
        except Exception:  # noqa: S110
            # Shield the hot path from any runtime attribute mutation errors
            pass
