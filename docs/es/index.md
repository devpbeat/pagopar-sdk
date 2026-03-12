# Wiki de Pagopar SDK

`pagopar-sdk` es una biblioteca Python tipada y liviana para integrar con
[Pagopar](https://www.pagopar.com/) — la pasarela de pagos online en Paraguay.

Cubre ambas APIs que ofrece Pagopar:

| API | Qué hace |
|-----|----------|
| **Commerce** (`client.commerce`) | Iniciar transacciones, listar formas de pago, consultar pedidos, solicitar reversiones |
| **Recurrente / Preautorización** (`client.recurrent`) | Registrar clientes y tarjetas, listar/confirmar/eliminar tarjetas, cobrar con tarjeta guardada, preautorizar y confirmar/cancelar montos |

La implementación sigue la
[colección Postman oficial de Pagopar](https://www.postman.com/pagopar/workspace/pagopar/overview?)
— cada endpoint, algoritmo de generación de token y esquema de firma fue derivado
directamente de la colección provista por la pasarela de pagos.

---

## Qué incluye esta wiki

- [Instalación](installation.md) — pip, uv, variables de entorno y setup desde fuente
- [Integración con FastAPI](fastapi-example.md) — patrón de capa de servicios asíncrona con `asyncio.to_thread`
- [Integración con Django](django-example.md) — clase de servicio + vistas + patrón de webhook
- [Integración con Flask](flask-example.md) — patrón app factory + blueprint
- [Contribuir](contributing.md) — cómo contribuir al SDK
- [Publicación en PyPI](pypi-publishing.md) — cómo se publican los releases
- [Generación de Wiki](wiki-generation.md) — cómo se construye este sitio con MkDocs

---

## Inicio rápido

```bash
pip install pagopar-sdk
# o
uv add pagopar-sdk
```

```python
from pagopar_sdk import PagoparClient

with PagoparClient(public_key="TU_PUBLIC_KEY", private_key="TU_PRIVATE_KEY") as client:
    formas = client.commerce.get_payment_methods()
    print(formas["resultado"])
```

Ver la [guía de instalación](installation.md) para el setup completo incluyendo variables de entorno.

---

## SDK de un vistazo

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

## Ejecutar la documentación localmente

```bash
uv sync --extra docs
mkdocs serve
```

Abrir: `http://127.0.0.1:8000`
