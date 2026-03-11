from __future__ import annotations

import hashlib

from pagopar_sdk.auth import build_start_transaction_token, build_token, normalize_amount_for_signature


def test_build_token_matches_sha1_scheme() -> None:
    expected = hashlib.sha1("secretPAGO-RECURRENTE".encode("utf-8")).hexdigest()
    assert build_token("secret", "PAGO-RECURRENTE") == expected


def test_normalize_amount_for_signature_matches_postman_behavior() -> None:
    assert normalize_amount_for_signature("1000.00") == "1000"
    assert normalize_amount_for_signature("1000.50") == "1000.5"
    assert normalize_amount_for_signature(0) == "0"


def test_start_transaction_token_normalizes_amount_before_hashing() -> None:
    token_a = build_start_transaction_token("secret", "2017", "1000.00")
    token_b = build_start_transaction_token("secret", "2017", 1000)
    assert token_a == token_b
