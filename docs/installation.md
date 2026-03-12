# Installation

## Requirements

- Python 3.10 or higher
- An active [Pagopar](https://www.pagopar.com/) merchant account with API credentials

---

## Install from PyPI

### pip

```bash
pip install pagopar-sdk
```

### uv

```bash
uv add pagopar-sdk
```

That's it. No extra dependencies beyond `httpx` are pulled in.

---

## Environment variables

The SDK requires two credentials issued by Pagopar in your merchant dashboard:

| Variable | Description |
|----------|-------------|
| `PAGOPAR_PUBLIC_KEY` | Your public key (used to identify the merchant) |
| `PAGOPAR_PRIVATE_KEY` | Your private key (used to sign requests) |

Store them in a `.env` file (never commit this to source control):

```
PAGOPAR_PUBLIC_KEY=your_public_key_here
PAGOPAR_PRIVATE_KEY=your_private_key_here
```

Load them in your app:

```python
import os
from pagopar_sdk import PagoparClient

client = PagoparClient(
    public_key=os.environ["PAGOPAR_PUBLIC_KEY"],
    private_key=os.environ["PAGOPAR_PRIVATE_KEY"],
)
```

Or use `python-dotenv` / `pydantic-settings` for automatic `.env` loading in
[FastAPI](fastapi-example.md) and [Django](django-example.md) projects.

---

## Basic usage

```python
from pagopar_sdk import PagoparClient

# Context manager — client is closed automatically
with PagoparClient(public_key="...", private_key="...") as client:
    methods = client.commerce.get_payment_methods()
    print(methods["resultado"])
```

Or manage lifecycle manually:

```python
client = PagoparClient(public_key="...", private_key="...")
try:
    result = client.commerce.get_payment_methods()
finally:
    client.close()
```

---

## Optional: disable automatic error raising

By default the SDK raises `PagoparBusinessError` when the API returns
`respuesta: false`. You can disable this and inspect the raw response yourself:

```python
client = PagoparClient(
    public_key="...",
    private_key="...",
    raise_on_api_error=False,
)
result = client.commerce.reverse_order("HASH_PEDIDO")
if not result.get("respuesta"):
    print("Reversal failed:", result)
```

---

## Install from source (contributors)

```bash
git clone https://github.com/devpbeat/pagopar-sdk
cd pagopar-sdk

# with pip
pip install -e ".[dev]"

# or with uv
uv sync --extra dev
```

Run tests:

```bash
pytest
```

---

## Install docs tooling

```bash
# with uv
uv sync --extra docs

# or with pip
pip install -e ".[docs]"
```

Serve locally:

```bash
mkdocs serve
```
