"""Custom exception hierarchy for Pagopar SDK."""

from __future__ import annotations

from typing import Any


class PagoparError(Exception):
    """Base class for all SDK-related exceptions."""


class PagoparConnectionError(PagoparError):
    """Raised when the SDK cannot reach Pagopar servers."""


class PagoparHTTPError(PagoparError):
    """Raised when Pagopar responds with a non-success HTTP status code."""

    def __init__(self, status_code: int, message: str, response_text: str | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class PagoparResponseError(PagoparError):
    """Raised when Pagopar responds with an invalid or unexpected payload."""


class PagoparBusinessError(PagoparError):
    """Raised when Pagopar returns a processed request with `respuesta=false`."""

    def __init__(self, message: str, payload: dict[str, Any]) -> None:
        super().__init__(message)
        self.payload = payload
