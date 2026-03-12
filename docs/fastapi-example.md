# FastAPI example implementation

This example shows the recommended pattern for using `pagopar-sdk` inside an async FastAPI app.

Because the SDK is synchronous (backed by `httpx`), each call is offloaded to a thread
with `asyncio.to_thread` so it never blocks the event loop.

## Installation

```bash
pip install pagopar-sdk fastapi uvicorn
```

Or with uv:

```bash
uv add pagopar-sdk fastapi uvicorn
```

## 1) Service layer

All Pagopar calls live in a single module. Each helper is `async` and wraps the
sync SDK call with `asyncio.to_thread`.

```python
# app/pagopar.py
import asyncio
import os
from datetime import datetime, timedelta

from pagopar_sdk import PagoparClient

PAGOPAR_CHECKOUT_BASE = "https://www.pagopar.com/pagos"

PUBLIC_KEY: str = os.getenv("PAGOPAR_PUBLIC_KEY", "")
PRIVATE_KEY: str = os.getenv("PAGOPAR_PRIVATE_KEY", "")


def _client(*, raise_on_api_error: bool = True) -> PagoparClient:
    return PagoparClient(
        public_key=PUBLIC_KEY,
        private_key=PRIVATE_KEY,
        raise_on_api_error=raise_on_api_error,
    )


def checkout_url(data_hash: str) -> str:
    return f"{PAGOPAR_CHECKOUT_BASE}/{data_hash}"


async def get_formas_pago() -> list[dict]:
    """List all available payment methods for the configured merchant."""
    def _call():
        with _client() as c:
            data = c.commerce.get_payment_methods()
        return data["resultado"]

    return await asyncio.to_thread(_call)


async def iniciar_transaccion(
    id_pedido_comercio: str,
    monto_total: float,
    comprador: dict,
    compras_items: list[dict],
    forma_pago: int | None = None,
    descripcion_resumen: str = "",
    fecha_maxima_pago: str | None = None,
) -> dict:
    """
    Create a transaction at Pagopar (Step 1 of the purchase flow).
    Returns {"data": "<checkout_hash>", "pedido": "<pagopar_order_id>"}.
    After this, redirect the user to checkout_url(data["data"]).
    """
    if not fecha_maxima_pago:
        fecha_maxima_pago = (datetime.utcnow() + timedelta(hours=24)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    payload: dict = {
        "id_pedido_comercio": id_pedido_comercio,
        "monto_total": round(monto_total),
        "tipo_pedido": "VENTA-COMERCIO",
        "comprador": comprador,
        "compras_items": compras_items,
        "fecha_maxima_pago": fecha_maxima_pago,
        "descripcion_resumen": descripcion_resumen,
    }
    if forma_pago is not None:
        payload["forma_pago"] = forma_pago

    def _call():
        with _client() as c:
            data = c.commerce.create_transaction(payload)
        return data["resultado"][0]

    return await asyncio.to_thread(_call)


async def consultar_pedido(hash_pedido: str) -> dict:
    """Query the current status of a Pagopar order by its hash."""
    def _call():
        with _client() as c:
            data = c.commerce.get_order(hash_pedido)
        return data["resultado"][0]

    return await asyncio.to_thread(_call)


async def reversar_pedido(hash_pedido: str) -> dict:
    """Request a reversal/refund for a Pagopar order."""
    def _call():
        # raise_on_api_error=False so callers can inspect respuesta themselves
        with _client(raise_on_api_error=False) as c:
            return c.commerce.reverse_order(hash_pedido)

    return await asyncio.to_thread(_call)
```

## 2) Routes

```python
# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from . import pagopar

app = FastAPI(title="Pagopar Integration API")


@app.get("/payments/methods")
async def payment_methods():
    return await pagopar.get_formas_pago()


class TransactionRequest(BaseModel):
    id_pedido_comercio: str
    monto_total: float
    comprador: dict
    compras_items: list[dict]
    forma_pago: int | None = None
    descripcion_resumen: str = ""
    fecha_maxima_pago: str | None = None


@app.post("/payments/transaction")
async def create_transaction(body: TransactionRequest):
    result = await pagopar.iniciar_transaccion(**body.model_dump())
    return {
        "checkout_url": pagopar.checkout_url(result["data"]),
        "pedido": result["pedido"],
    }


@app.get("/payments/order/{hash_pedido}")
async def get_order(hash_pedido: str):
    return await pagopar.consultar_pedido(hash_pedido)


@app.post("/payments/order/{hash_pedido}/reverse")
async def reverse_order(hash_pedido: str):
    result = await pagopar.reversar_pedido(hash_pedido)
    if not result.get("respuesta"):
        raise HTTPException(status_code=400, detail=result)
    return result
```

## 3) Run

```bash
uvicorn app.main:app --reload
```

## Good practices

- The SDK is synchronous — always wrap calls with `asyncio.to_thread` to avoid blocking the event loop.
- Use `raise_on_api_error=False` when you need to inspect the raw `respuesta` (e.g. reversals), and raise `HTTPException` manually.
- Keep environment variables (`PAGOPAR_PUBLIC_KEY`, `PAGOPAR_PRIVATE_KEY`) out of source control; load them with `os.getenv` or `pydantic-settings`.
- `monto_total` is sent as an integer (guaraníes have no cents); always `round()` before sending.
- After `iniciar_transaccion`, redirect the user to `checkout_url(result["data"])` to complete payment.
