"""Authentication and signature helpers for Pagopar APIs."""

from __future__ import annotations

import hashlib
from decimal import Decimal, InvalidOperation

NumberLike = int | float | Decimal | str


def sha1_hex(raw: str) -> str:
    """Return SHA1 hex digest for a string payload."""

    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def build_token(private_key: str, suffix: str) -> str:
    """Build token using Pagopar's SHA1(private_key + suffix) scheme."""

    return sha1_hex(f"{private_key}{suffix}")


def normalize_amount_for_signature(amount: NumberLike) -> str:
    """Normalize amount to match Postman parseFloat(...).toString() behavior."""

    try:
        decimal_amount = Decimal(str(amount))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"Invalid amount for signature: {amount!r}") from exc

    normalized = format(decimal_amount, "f")
    if "." in normalized:
        normalized = normalized.rstrip("0").rstrip(".")

    return normalized or "0"


def build_start_transaction_token(
    private_key: str,
    id_pedido_comercio: str,
    monto_total: NumberLike,
) -> str:
    """Build token for `/api/comercios/2.0/iniciar-transaccion`."""

    normalized_amount = normalize_amount_for_signature(monto_total)
    return sha1_hex(f"{private_key}{id_pedido_comercio}{normalized_amount}")
