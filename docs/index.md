# Pagopar SDK Wiki

`pagopar-sdk` is a typed, lightweight Python library for integrating with
[Pagopar](https://www.pagopar.com/) — Paraguay's online payment gateway.

It covers both APIs offered by Pagopar:

| API | What it does |
|-----|--------------|
| **Commerce** (`client.commerce`) | Initiate transactions, list payment methods, query orders, request reversals |
| **Recurrent / Preauthorization** (`client.recurrent`) | Register customers and cards, list/confirm/delete cards, charge saved cards, preauthorize and confirm/cancel amounts |

The implementation follows the official
[Pagopar Postman collection](https://www.postman.com/pagopar/workspace/pagopar/overview?)
— every endpoint, token-generation algorithm, and signature scheme was derived directly
from the collection provided by the payment gateway.

---

## What you will find here

- [Installation](installation.md) — pip, uv, environment variables, and source setup
- [FastAPI integration](fastapi-example.md) — async service-layer pattern with `asyncio.to_thread`
- [Django integration](django-example.md) — service class + views + webhook pattern
- [Flask integration](flask-example.md) — app factory + blueprint pattern
- [Contributing](contributing.md) — how to contribute to the SDK
- [PyPI Publishing](pypi-publishing.md) — how releases are published
- [Wiki Generator](wiki-generation.md) — how this site is built with MkDocs

---

## Quick start

```bash
pip install pagopar-sdk
# or
uv add pagopar-sdk
```

```python
from pagopar_sdk import PagoparClient

with PagoparClient(public_key="YOUR_PUBLIC_KEY", private_key="YOUR_PRIVATE_KEY") as client:
    methods = client.commerce.get_payment_methods()
    print(methods["resultado"])
```

See the [Installation guide](installation.md) for full setup including environment variables.

---

## SDK at a glance

```
PagoparClient
├── .commerce
│   ├── get_payment_methods()
│   ├── create_transaction(payload)
│   ├── get_order(hash_pedido)
│   └── reverse_order(hash_pedido)
└── .recurrent
    ├── add_customer(...)
    ├── add_card(...)
    ├── list_cards(...)
    ├── confirm_card(...)
    ├── delete_card(...)
    ├── pay(...)
    ├── preauthorize(...)
    ├── confirm_preauthorization(...)
    └── cancel_preauthorization(...)
```

---

## Run docs locally

```bash
uv sync --extra docs
mkdocs serve
```

Open: `http://127.0.0.1:8000`
