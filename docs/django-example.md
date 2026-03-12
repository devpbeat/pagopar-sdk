# Django example implementation

This example shows a clean service-oriented integration with `pagopar-sdk`.

## Installation

```bash
pip install pagopar-sdk django
```

Or with uv:

```bash
uv add pagopar-sdk django
```

## 1) Settings

```python
# settings.py
import os

PAGOPAR_PUBLIC_KEY = os.environ["PAGOPAR_PUBLIC_KEY"]
PAGOPAR_PRIVATE_KEY = os.environ["PAGOPAR_PRIVATE_KEY"]
PAGOPAR_BASE_URL = os.getenv("PAGOPAR_BASE_URL", "https://api.pagopar.com")
```

## 2) Service layer

```python
# payments/services/pagopar_service.py
from __future__ import annotations

from django.conf import settings
from pagopar_sdk import PagoparBusinessError, PagoparClient


class PagoparService:
    def __init__(self) -> None:
        self.client = PagoparClient(
            public_key=settings.PAGOPAR_PUBLIC_KEY,
            private_key=settings.PAGOPAR_PRIVATE_KEY,
            base_url=settings.PAGOPAR_BASE_URL,
        )

    def create_transaction(self, payload: dict) -> dict:
        return self.client.commerce.create_transaction(payload)

    def get_order(self, hash_pedido: str) -> dict:
        return self.client.commerce.get_order(hash_pedido=hash_pedido)

    def close(self) -> None:
        self.client.close()


def start_checkout(payload: dict) -> dict:
    service = PagoparService()
    try:
        return service.create_transaction(payload)
    except PagoparBusinessError as exc:
        return {"respuesta": False, "resultado": str(exc), "detalle": exc.payload}
    finally:
        service.close()
```

## 3) API view for checkout

```python
# payments/views.py
from __future__ import annotations

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .services.pagopar_service import start_checkout


@require_POST
def create_payment(request):
    payload = json.loads(request.body)
    response = start_checkout(payload)
    return JsonResponse(response, status=200)
```

## 4) URL mapping

```python
# payments/urls.py
from django.urls import path
from .views import create_payment

urlpatterns = [
    path("payments/create/", create_payment, name="create-payment"),
]
```

## 5) Webhook callback pattern (recommended)

Use a dedicated endpoint for Pagopar notifications, verify your order in DB, and confirm current state with `get_order`.

```python
# payments/views.py
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@require_POST
def pagopar_webhook(request):
    event = json.loads(request.body)
    hash_pedido = event.get("hash_pedido")
    if not hash_pedido:
        return JsonResponse({"ok": False, "error": "missing hash_pedido"}, status=400)

    # Reconcile status against Pagopar before marking the order as paid.
    # status = service.get_order(hash_pedido)
    return JsonResponse({"ok": True})
```

## Good practices

- Keep SDK usage in a service layer, not spread across views.
- Always reconcile payment state server-to-server (`get_order`) before fulfillment.
- Store `hash_pedido` and your internal order ID for idempotent webhook processing.
