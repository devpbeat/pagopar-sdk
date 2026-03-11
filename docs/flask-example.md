# Flask example implementation

This example uses the app factory pattern and a small integration helper.

## 1) App factory configuration

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

## 2) Integration helper

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

## 3) Blueprint routes

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

## 4) Run

```bash
flask --app app:create_app run --debug
```

## Good practices

- Build and close the SDK client per request unless you manage a global lifecycle explicitly.
- Keep webhook endpoints separate from checkout creation endpoints.
- Confirm final payment state with Pagopar before fulfillment.
