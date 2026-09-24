import logging
from typing import Any

from pseudonymize.engine import Pseudonymizer


class DlpLoggingFilter(logging.Filter):
    """A standard logging Filter that redacts PII from log records.

    Redacts the primary log message string and string values in arguments
    (tuples, lists, dicts, and nested collections) before records are emitted.
    Preserves non-string arguments and numerical values untouched.
    """

    def __init__(self, engine: Pseudonymizer | None = None, name: str = ""):
        super().__init__(name)
        self.engine = engine or Pseudonymizer()

    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = self.engine.process(record.msg).text

        if record.args:
            if isinstance(record.args, dict):
                record.args = {k: self._redact_value(v) for k, v in record.args.items()}
            elif isinstance(record.args, (list, tuple)):
                record.args = tuple(self._redact_value(arg) for arg in record.args)

        return True

    def _redact_value(self, val: Any) -> Any:
        if isinstance(val, str):
            return self.engine.process(val).text
        if isinstance(val, (list, tuple)):
            return type(val)(self._redact_value(item) for item in val)
        if isinstance(val, dict):
            return {k: self._redact_value(v) for k, v in val.items()}
        return val


class OTelRedactionSpanProcessor:
    """A duck-typed OpenTelemetry SpanProcessor that redacts PII from span attributes.

    Sanitizes string attributes and collections (lists, tuples, nested mappings)
    during span lifecycle events (on_start and on_end) without requiring OpenTelemetry
    packages to be installed at base import.

    If an attribute container is immutable or rejects in-place item assignment,
    the processor attempts to reassign the attributes mapping. If mutation is
    impossible, it fails closed by raising a RuntimeError rather than silently
    leaking unsanitized attributes.
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

    def _redact_value(self, val: Any) -> Any:
        if isinstance(val, str):
            return self.engine.process(val).text
        if isinstance(val, (list, tuple)):
            return type(val)(self._redact_value(item) for item in val)
        if isinstance(val, dict):
            return {k: self._redact_value(v) for k, v in val.items()}
        return val

    def _redact_span_attributes(self, span: Any) -> None:
        if not hasattr(span, "attributes") or not span.attributes:
            return

        try:
            for key, val in list(span.attributes.items()):
                new_val = self._redact_value(val)
                if new_val is not val:
                    span.attributes[key] = new_val
        except (TypeError, AttributeError):
            # Attribute container is immutable; attempt to replace mapping on span
            try:
                new_attrs = {k: self._redact_value(v) for k, v in span.attributes.items()}
                span.attributes = new_attrs
            except Exception as exc:
                raise RuntimeError("Failed to redact immutable span attributes safely") from exc
