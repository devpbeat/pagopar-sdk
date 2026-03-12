# Ejemplo de implementación en FastAPI

Este ejemplo muestra el patrón recomendado para usar `pagopar-sdk` dentro de una app FastAPI asíncrona.

Como el SDK es sincrónico (usa `httpx` internamente), cada llamada se delega a un hilo
con `asyncio.to_thread` para no bloquear el event loop.

## Instalación

```bash
pip install pagopar-sdk fastapi uvicorn
```

O con uv:

```bash
uv add pagopar-sdk fastapi uvicorn
```

## 1) Capa de servicios

Todas las llamadas a Pagopar viven en un único módulo. Cada helper es `async` y envuelve
la llamada sincrónica del SDK con `asyncio.to_thread`.

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
    """Lista todas las formas de pago disponibles para el comercio configurado."""
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
    Crea una transacción en Pagopar (Paso 1 del flujo de compra).
    Retorna {"data": "<checkout_hash>", "pedido": "<id_pedido_pagopar>"}.
    Luego redirigir al usuario a checkout_url(data["data"]).
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
    """Consulta el estado actual de un pedido Pagopar por su hash."""
    def _call():
        with _client() as c:
            data = c.commerce.get_order(hash_pedido)
        return data["resultado"][0]

    return await asyncio.to_thread(_call)


async def reversar_pedido(hash_pedido: str) -> dict:
    """Solicita una reversión/reembolso de un pedido Pagopar."""
    def _call():
        # raise_on_api_error=False para que el llamador pueda inspeccionar respuesta
        with _client(raise_on_api_error=False) as c:
            return c.commerce.reverse_order(hash_pedido)

    return await asyncio.to_thread(_call)
```

## 2) Rutas

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

## 3) Ejecutar

```bash
uvicorn app.main:app --reload
```

## Buenas prácticas

- El SDK es sincrónico — siempre envolver las llamadas con `asyncio.to_thread` para no bloquear el event loop.
- Usar `raise_on_api_error=False` cuando necesitás inspeccionar el `respuesta` crudo (por ej. reversiones) y lanzar `HTTPException` manualmente.
- Mantener las variables de entorno (`PAGOPAR_PUBLIC_KEY`, `PAGOPAR_PRIVATE_KEY`) fuera del repositorio; cargarlas con `os.getenv` o `pydantic-settings`.
- `monto_total` se envía como entero (el guaraní no tiene centavos); siempre aplicar `round()` antes de enviar.
- Tras `iniciar_transaccion`, redirigir al usuario a `checkout_url(result["data"])` para completar el pago.
