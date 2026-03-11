"""Main SDK client implementations for Pagopar APIs."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

import httpx

from .auth import build_start_transaction_token, build_token
from .exceptions import (
    PagoparBusinessError,
    PagoparConnectionError,
    PagoparHTTPError,
    PagoparResponseError,
)
from .models import StartTransactionRequest


class _HTTPTransport:
    """Internal HTTP transport with shared error handling and auth context."""

    def __init__(
        self,
        public_key: str,
        private_key: str,
        *,
        base_url: str,
        timeout: float,
        raise_on_api_error: bool,
        http_client: httpx.Client | None,
    ) -> None:
        self.public_key = public_key
        self.private_key = private_key
        self.base_url = base_url.rstrip("/")
        self.raise_on_api_error = raise_on_api_error
        self._owns_client = http_client is None
        self._client = http_client or httpx.Client(timeout=timeout)

    def close(self) -> None:
        """Close underlying HTTP resources if owned by this SDK instance."""

        if self._owns_client:
            self._client.close()

    def post(self, path: str, payload: Mapping[str, Any]) -> dict[str, Any]:
        """POST JSON payload to a Pagopar endpoint and return parsed JSON."""

        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            response = self._client.post(
                url,
                json=payload,
                headers={"Accept": "application/json", "Content-Type": "application/json"},
            )
        except httpx.HTTPError as exc:
            raise PagoparConnectionError(f"Unable to connect to Pagopar: {exc}") from exc

        if response.status_code >= 400:
            raise PagoparHTTPError(
                status_code=response.status_code,
                message=f"Pagopar returned HTTP {response.status_code}.",
                response_text=response.text,
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise PagoparResponseError("Pagopar response is not valid JSON.") from exc

        if not isinstance(data, dict):
            raise PagoparResponseError("Pagopar response JSON is not an object.")

        if self.raise_on_api_error and data.get("respuesta") is False:
            message = str(data.get("resultado", "Pagopar business error."))
            raise PagoparBusinessError(message=message, payload=data)

        return data


class CommerceAPI:
    """Client for standard commerce endpoints (checkout flow)."""

    def __init__(self, transport: _HTTPTransport) -> None:
        self._transport = transport

    def create_transaction(
        self,
        request: StartTransactionRequest | Mapping[str, Any],
    ) -> dict[str, Any]:
        """Create a transaction with `/api/comercios/2.0/iniciar-transaccion`."""

        if isinstance(request, StartTransactionRequest):
            payload = request.to_payload(public_key=self._transport.public_key)
        else:
            payload = deepcopy(dict(request))
            payload.setdefault("public_key", self._transport.public_key)

            if isinstance(payload.get("compras_items"), list):
                for item in payload["compras_items"]:
                    if isinstance(item, dict):
                        item.setdefault("public_key", self._transport.public_key)

        order_id = str(payload["id_pedido_comercio"])
        amount = payload["monto_total"]
        payload["token"] = build_start_transaction_token(
            private_key=self._transport.private_key,
            id_pedido_comercio=order_id,
            monto_total=amount,
        )

        return self._transport.post("/api/comercios/2.0/iniciar-transaccion", payload)

    def get_payment_methods(self) -> dict[str, Any]:
        """Fetch payment methods from `/api/forma-pago/1.1/traer/`."""

        payload = {
            "token": build_token(self._transport.private_key, "FORMA-PAGO"),
            "token_publico": self._transport.public_key,
        }
        return self._transport.post("/api/forma-pago/1.1/traer/", payload)

    def get_order(self, hash_pedido: str) -> dict[str, Any]:
        """Fetch order details from `/api/pedidos/1.1/traer`."""

        payload = {
            "token": build_token(self._transport.private_key, "CONSULTA"),
            "token_publico": self._transport.public_key,
            "hash_pedido": hash_pedido,
        }
        return self._transport.post("/api/pedidos/1.1/traer", payload)

    def reverse_order(self, hash_pedido: str) -> dict[str, Any]:
        """Reverse order with `/api/pedidos/1.1/reversar`."""

        payload = {
            "token": build_token(self._transport.private_key, "PEDIDO-REVERSAR"),
            "token_publico": self._transport.public_key,
            "hash_pedido": hash_pedido,
        }
        return self._transport.post("/api/pedidos/1.1/reversar", payload)


class RecurrentAPI:
    """Client for recurrent payment endpoints (`/api/pago-recurrente/3.0/*`)."""

    def __init__(self, transport: _HTTPTransport) -> None:
        self._transport = transport

    def _base_payload(self) -> dict[str, str]:
        return {
            "token": build_token(self._transport.private_key, "PAGO-RECURRENTE"),
            "token_publico": self._transport.public_key,
        }

    def add_customer(
        self,
        *,
        identificador: int | str,
        nombre_apellido: str,
        email: str,
        celular: str,
    ) -> dict[str, Any]:
        """Create recurrent customer with `/agregar-cliente/`."""

        payload = self._base_payload() | {
            "identificador": identificador,
            "nombre_apellido": nombre_apellido,
            "email": email,
            "celular": celular,
        }
        return self._transport.post("/api/pago-recurrente/3.0/agregar-cliente/", payload)

    def add_card(
        self,
        *,
        identificador: int | str,
        url: str,
        proveedor: str = "Bancard",
    ) -> dict[str, Any]:
        """Start card registration flow with `/agregar-tarjeta/`."""

        payload = self._base_payload() | {
            "url": url,
            "proveedor": proveedor,
            "identificador": identificador,
        }
        return self._transport.post("/api/pago-recurrente/3.0/agregar-tarjeta/", payload)

    def list_cards(self, *, identificador: int | str) -> dict[str, Any]:
        """List cards from `/listar-tarjeta/`."""

        payload = self._base_payload() | {"identificador": identificador}
        return self._transport.post("/api/pago-recurrente/3.0/listar-tarjeta/", payload)

    def confirm_card(self, *, identificador: int | str, url: str) -> dict[str, Any]:
        """Confirm card registration with `/confirmar-tarjeta/`."""

        payload = self._base_payload() | {"url": url, "identificador": identificador}
        return self._transport.post("/api/pago-recurrente/3.0/confirmar-tarjeta/", payload)

    def delete_card(self, *, identificador: int | str, tarjeta: str) -> dict[str, Any]:
        """Delete a stored card with `/eliminar-tarjeta/`."""

        payload = self._base_payload() | {"tarjeta": tarjeta, "identificador": identificador}
        return self._transport.post("/api/pago-recurrente/3.0/eliminar-tarjeta/", payload)

    def pay(self, *, identificador: int | str, tarjeta: str, hash_pedido: str) -> dict[str, Any]:
        """Pay with stored card using `/pagar/`."""

        payload = self._base_payload() | {
            "hash_pedido": hash_pedido,
            "tarjeta": tarjeta,
            "identificador": identificador,
        }
        return self._transport.post("/api/pago-recurrente/3.0/pagar/", payload)

    def preauthorize(
        self,
        *,
        identificador: int | str,
        tarjeta: int | str,
        monto: int | float,
        descripcion: str,
        id_transaccion: int | str,
    ) -> dict[str, Any]:
        """Create preauthorization with `/preautorizar/`."""

        payload = self._base_payload() | {
            "tarjeta": tarjeta,
            "monto": monto,
            "descripcion": descripcion,
            "id_transaccion": id_transaccion,
            "identificador": identificador,
        }
        return self._transport.post("/api/pago-recurrente/3.0/preautorizar/", payload)

    def confirm_preauthorization(
        self,
        *,
        identificador: int | str,
        transaccion: int | str,
        id_transaccion: int | str,
        hash_pedido: str,
    ) -> dict[str, Any]:
        """Confirm preauthorization with `/confirmar-preautorizacion/`."""

        payload = self._base_payload() | {
            "hash_pedido": hash_pedido,
            "transaccion": transaccion,
            "id_transaccion": id_transaccion,
            "identificador": identificador,
        }
        return self._transport.post("/api/pago-recurrente/3.0/confirmar-preautorizacion/", payload)

    def cancel_preauthorization(
        self,
        *,
        identificador: int | str,
        transaccion: int | str,
        id_transaccion: int | str,
    ) -> dict[str, Any]:
        """Cancel preauthorization with `/cancelar-preautorizacion/`."""

        payload = self._base_payload() | {
            "transaccion": transaccion,
            "id_transaccion": id_transaccion,
            "identificador": identificador,
        }
        return self._transport.post("/api/pago-recurrente/3.0/cancelar-preautorizacion/", payload)


class PagoparClient:
    """Top-level Pagopar SDK client.

    Example:
        >>> from pagopar_sdk import PagoparClient
        >>> client = PagoparClient(public_key="...", private_key="...")
        >>> methods = client.commerce.get_payment_methods()
        >>> client.close()
    """

    def __init__(
        self,
        *,
        public_key: str,
        private_key: str,
        base_url: str = "https://api.pagopar.com",
        timeout: float = 20.0,
        raise_on_api_error: bool = True,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._transport = _HTTPTransport(
            public_key=public_key,
            private_key=private_key,
            base_url=base_url,
            timeout=timeout,
            raise_on_api_error=raise_on_api_error,
            http_client=http_client,
        )
        self.commerce = CommerceAPI(self._transport)
        self.recurrent = RecurrentAPI(self._transport)

    def close(self) -> None:
        """Release resources used by the underlying HTTP client."""

        self._transport.close()

    def __enter__(self) -> "PagoparClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
