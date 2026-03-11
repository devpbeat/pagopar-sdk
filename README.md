# Pagopar Python SDK

Typed, lightweight Python SDK for the Pagopar APIs covered by your Postman collections:

- **Integración de medios de pagos** (checkout / commerce flow)
- **Catastro de tarjetas - Pagos recurrentes - Preautorización**

## Features

- Typed models for `iniciar-transaccion`
- Automatic token/signature generation matching Postman scripts
- Structured client split by domain: `commerce` and `recurrent`
- Safe error hierarchy for HTTP, connection, payload, and business errors
- Context-manager friendly (`with PagoparClient(...) as client`)

## Installation

```bash
pip install -e .
```

Or with uv:

```bash
uv pip install -e .
```

## Wiki and framework examples

This repository now includes a Markdown-based wiki under `docs/` powered by MkDocs.

It can now be built in **English and Spanish**.

- Wiki home: `docs/index.md`
- Spanish wiki home: `docs/es/index.md`
- Contributing guide: `CONTRIBUTING.md`
- Wiki contributing guide: `docs/contributing.md`
- Spanish wiki contributing guide: `docs/es/contributing.md`
- PyPI publishing guide: `docs/pypi-publishing.md`
- Spanish PyPI publishing guide: `docs/es/pypi-publishing.md`
- Django implementation: `docs/django-example.md`
- Spanish Django implementation: `docs/es/django-example.md`
- FastAPI implementation: `docs/fastapi-example.md`
- Spanish FastAPI implementation: `docs/es/fastapi-example.md`
- Flask implementation: `docs/flask-example.md`
- Spanish Flask implementation: `docs/es/flask-example.md`
- Wiki generation guide: `docs/wiki-generation.md`
- Spanish wiki generation guide: `docs/es/wiki-generation.md`

Install docs tooling:

```bash
uv sync --extra docs
```

Serve docs locally:

```bash
mkdocs serve
```

Build static docs:

```bash
mkdocs build
```

The generated site includes both locales.

## Quick start

```python
from pagopar_sdk import PagoparClient

with PagoparClient(public_key="YOUR_PUBLIC_KEY", private_key="YOUR_PRIVATE_KEY") as client:
	payment_methods = client.commerce.get_payment_methods()
	print(payment_methods)
```

## SDK structure

- `PagoparClient`: top-level client
  - `client.commerce`: checkout/commerce APIs
  - `client.recurrent`: recurrent card/payment APIs

## Commerce API (Integración de medios de pagos)

### 1) Iniciar transacción

Use typed models:

```python
from pagopar_sdk import Buyer, PagoparClient, PurchaseItem, StartTransactionRequest

request = StartTransactionRequest(
	id_pedido_comercio="2017",
	monto_total=1000,
	tipo_pedido="VENTA-COMERCIO",
	forma_pago=26,
	fecha_maxima_pago="2026-12-31 20:00:00",
	descripcion_resumen="Pago de ejemplo",
	comprador=Buyer(
		nombre="Rudolph Goetz",
		email="fernandogoetz@gmail.com",
		documento="4247903",
		telefono="0972200046",
		ruc="4247903-7",
		tipo_documento="CI",
	),
	compras_items=[
		PurchaseItem(
			id_producto=895,
			nombre="Pago ejemplo",
			descripcion="Descripción del pago",
			cantidad=1,
			precio_total=1000,
			categoria="909",
			ciudad="1",
			url_imagen="https://example.com/item.png",
		)
	],
)

with PagoparClient(public_key="YOUR_PUBLIC_KEY", private_key="YOUR_PRIVATE_KEY") as client:
	response = client.commerce.create_transaction(request)
	print(response)
```

You can also pass a `dict` payload directly to `create_transaction(...)`.

### 2) Traer formas de pago

```python
response = client.commerce.get_payment_methods()
```

### 3) Consultar pedido

```python
response = client.commerce.get_order(hash_pedido="HASH_PEDIDO")
```

### 4) Reversar pedido

```python
response = client.commerce.reverse_order(hash_pedido="HASH_PEDIDO")
```

## Recurrent API (Catastro / pagos recurrentes / preautorización)

### Cliente

```python
from pagopar_sdk import PagoparClient

client = PagoparClient(public_key="YOUR_PUBLIC_KEY", private_key="YOUR_PRIVATE_KEY")
```

### Endpoints disponibles

```python
# 1) Agregar cliente
client.recurrent.add_customer(
	identificador=1,
	nombre_apellido="Mikhail Szwako",
	email="mihares@gmail.com",
	celular="0981252238",
)

# 2) Agregar tarjeta
client.recurrent.add_card(
	identificador=1,
	url="https://www.tusitio.com/checkout",
	proveedor="Bancard",  # o "uPay" según tu configuración
)

# 3) Listar tarjetas
client.recurrent.list_cards(identificador=1)

# 4) Confirmar tarjeta
client.recurrent.confirm_card(identificador=1, url="https://www.tusitio.com/checkout")

# 5) Eliminar tarjeta
client.recurrent.delete_card(identificador=1, tarjeta="TOKEN_TARJETA")

# 6) Pagar con tarjeta guardada
client.recurrent.pay(
	identificador=1,
	tarjeta="TOKEN_TARJETA",
	hash_pedido="HASH_PEDIDO",
)

# 7) Preautorizar
client.recurrent.preauthorize(
	identificador=1,
	tarjeta=77,
	monto=1000,
	descripcion="Monto ejemplo",
	id_transaccion=17,
)

# 8) Confirmar preautorización
client.recurrent.confirm_preauthorization(
	identificador=1,
	transaccion=8330907,
	id_transaccion=16,
	hash_pedido="HASH_PEDIDO",
)

# 9) Cancelar preautorización
client.recurrent.cancel_preauthorization(
	identificador=1,
	transaccion=8330993,
	id_transaccion=17,
)
```

When finished:

```python
client.close()
```

## Error handling

```python
from pagopar_sdk import (
	PagoparBusinessError,
	PagoparConnectionError,
	PagoparHTTPError,
	PagoparResponseError,
)

try:
	with PagoparClient(public_key="...", private_key="...") as client:
		client.commerce.get_payment_methods()
except PagoparBusinessError as exc:
	print("API respondió con error de negocio:", exc)
except PagoparHTTPError as exc:
	print("Error HTTP:", exc.status_code)
except PagoparConnectionError:
	print("No se pudo conectar a Pagopar")
except PagoparResponseError:
	print("Respuesta inválida")
```

## Token/signature helpers

The SDK exposes helpers if you need manual integration:

```python
from pagopar_sdk import build_start_transaction_token, build_token

recurrent_token = build_token("PRIVATE_KEY", "PAGO-RECURRENTE")
tx_token = build_start_transaction_token("PRIVATE_KEY", "2017", 1000)
```

## Notes

- Base URL defaults to `https://api.pagopar.com`.
- SDK raises business exceptions by default when `respuesta == false`.
- You can disable that behavior with `PagoparClient(..., raise_on_api_error=False)`.

