# Ejemplo de implementación en Flask

Este ejemplo usa el patrón app factory y un helper pequeño para la integración.

## Instalación

```bash
pip install pagopar-sdk flask
```

O con uv:

```bash
uv add pagopar-sdk flask
```

## 1) Configuración en app factory

```python
# app/__init__.py
import os
from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.update(
        PAGOPAR_PUBLIC_KEY=os.environ["PAGOPAR_PUBLIC_KEY"],
        PAGOPAR_PRIVATE_KEY=os.environ["PAGOPAR_PRIVATE_KEY"],
        PAGOPAR_BASE_URL=os.getenv("PAGOPAR_BASE_URL", "https://api.pagopar.com"),
    )

    from .payments import bp as payments_bp
    app.register_blueprint(payments_bp, url_prefix="/payments")
    return app
```

## 2) Helper de integración

```python
# app/pagopar_integration.py
from flask import current_app
from pagopar_sdk import PagoparClient


def build_pagopar_client() -> PagoparClient:
    return PagoparClient(
        public_key=current_app.config["PAGOPAR_PUBLIC_KEY"],
        private_key=current_app.config["PAGOPAR_PRIVATE_KEY"],
        base_url=current_app.config["PAGOPAR_BASE_URL"],
    )
```

## 3) Rutas con blueprint

```python
# app/payments.py
from flask import Blueprint, jsonify, request
from pagopar_sdk import PagoparBusinessError
from .pagopar_integration import build_pagopar_client

bp = Blueprint("payments", __name__)


@bp.get("/methods")
def methods():
    client = build_pagopar_client()
    try:
        return jsonify(client.commerce.get_payment_methods())
    finally:
        client.close()


@bp.post("/transaction")
def transaction():
    payload = request.get_json(force=True)
    client = build_pagopar_client()
    try:
        response = client.commerce.create_transaction(payload)
        return jsonify(response)
    except PagoparBusinessError as exc:
        return jsonify({"error": str(exc), "payload": exc.payload}), 400
    finally:
        client.close()
```

## 4) Ejecutar

```bash
flask --app app:create_app run --debug
```

## Buenas prácticas

- Crear y cerrar el cliente del SDK por request salvo que se gestione un ciclo de vida global.
- Separar endpoints de checkout y de webhook.
- Confirmar el estado real del pago con Pagopar antes de entregar el producto.
