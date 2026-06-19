from __future__ import annotations


class TravelMateError(Exception):
    """Base exception for TravelMate."""


class ConfigurationError(TravelMateError):
    """Raised when required runtime configuration is missing."""


class LLMClientError(TravelMateError):
    """Raised when the OpenAI-compatible client fails."""


class ToolExecutionError(TravelMateError):
    """Raised when tool execution cannot be completed."""

