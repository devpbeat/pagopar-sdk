from __future__ import annotations

import httpx
import pytest

from pagopar_sdk import PagoparBusinessError, PagoparClient


def test_get_payment_methods_uses_expected_endpoint() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/forma-pago/1.1/traer/"
        return httpx.Response(200, json={"respuesta": True, "resultado": []})

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as http_client:
        with PagoparClient(public_key="public", private_key="private", http_client=http_client) as client:
            response = client.commerce.get_payment_methods()

    assert response["respuesta"] is True
    assert response["resultado"] == []


def test_business_error_is_raised_when_respuesta_is_false() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"respuesta": False, "resultado": "failure"})

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as http_client:
        with PagoparClient(public_key="public", private_key="private", http_client=http_client) as client:
            with pytest.raises(PagoparBusinessError):
                client.commerce.get_payment_methods()
