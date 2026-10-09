"""Compatibility entry point; the Python package owns the hosted service."""

from pseudonymize.service import app

__all__ = ["app"]
