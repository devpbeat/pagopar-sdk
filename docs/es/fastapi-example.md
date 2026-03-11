# Ejemplo de implementación en FastAPI

Este ejemplo usa inyección de dependencias para proveer un cliente configurado de Pagopar por request.

## 1) Configuración

```python
# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pagopar_public_key: str
    pagopar_private_key: str
    pagopar_base_url: str = "https://api.pagopar.com"


settings = Settings()
```

## 2) Proveedor de dependencias

```python
# app/deps.py
from collections.abc import Generator
from pagopar_sdk import PagoparClient
from .config import settings


def get_pagopar_client() -> Generator[PagoparClient, None, None]:
    client = PagoparClient(
        public_key=settings.pagopar_public_key,
        private_key=settings.pagopar_private_key,
        base_url=settings.pagopar_base_url,
    )
    try:
        yield client
    finally:
        client.close()
```

## 3) Rutas

```python
# app/main.py
from fastapi import Depends, FastAPI, HTTPException
from pagopar_sdk import PagoparBusinessError, PagoparClient
from .deps import get_pagopar_client

app = FastAPI(title="Pagopar Integration API")


@app.get("/payments/methods")
def payment_methods(client: PagoparClient = Depends(get_pagopar_client)):
    return client.commerce.get_payment_methods()


@app.post("/payments/transaction")
def create_transaction(payload: dict, client: PagoparClient = Depends(get_pagopar_client)):
    try:
        return client.commerce.create_transaction(payload)
    except PagoparBusinessError as exc:
        raise HTTPException(status_code=400, detail={"error": str(exc), "payload": exc.payload}) from exc


@app.post("/payments/recurrent/preauthorize")
def preauthorize(payload: dict, client: PagoparClient = Depends(get_pagopar_client)):
    return client.recurrent.preauthorize(**payload)
```

## 4) Ejecutar

```bash
uvicorn app.main:app --reload
```

## Buenas prácticas

- Mapear `PagoparBusinessError` a errores `400` y los fallos de infraestructura a `5xx`.
- Construir payloads en funciones o servicios reutilizables.
- Aplicar idempotencia en pedidos propios y webhooks.
