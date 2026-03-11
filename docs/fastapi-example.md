# FastAPI example implementation

This example uses dependency injection to provide a configured Pagopar client per request.

## 1) Configuration

```python
# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pagopar_public_key: str
    pagopar_private_key: str
    pagopar_base_url: str = "https://api.pagopar.com"


settings = Settings()
```

## 2) Dependency provider

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

## 3) Routes

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

## 4) Run

```bash
uvicorn app.main:app --reload
```

## Good practices

- Map `PagoparBusinessError` to `400`-style API errors and infrastructure errors to `5xx`.
- Keep outgoing payload construction in dedicated service functions for reuse and validation.
- Add idempotency in your own order handling, especially for retries and webhooks.
