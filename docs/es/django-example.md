# Ejemplo de implementación en Django

Este ejemplo muestra una integración limpia basada en una capa de servicios con `pagopar-sdk`.

## 1) Configuración

```python
# settings.py
import os

PAGOPAR_PUBLIC_KEY = os.environ["PAGOPAR_PUBLIC_KEY"]
PAGOPAR_PRIVATE_KEY = os.environ["PAGOPAR_PRIVATE_KEY"]
PAGOPAR_BASE_URL = os.getenv("PAGOPAR_BASE_URL", "https://api.pagopar.com")
```

## 2) Capa de servicio

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

## 3) Vista para checkout

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

## 4) URLs

```python
# payments/urls.py
from django.urls import path
from .views import create_payment

urlpatterns = [
    path("payments/create/", create_payment, name="create-payment"),
]
```

## 5) Patrón recomendado para webhooks

Usar un endpoint dedicado para las notificaciones de Pagopar, validar el pedido en tu base de datos y reconciliar el estado real con `get_order`.

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

    return JsonResponse({"ok": True})
```

## Buenas prácticas

- Mantener el uso del SDK en una capa de servicios.
- Confirmar el estado del pago desde el servidor antes de entregar el producto.
- Guardar `hash_pedido` y tu ID interno para procesar webhooks de forma idempotente.
