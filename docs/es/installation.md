# Instalación

## Requisitos

- Python 3.10 o superior
- Una cuenta de comercio activa en [Pagopar](https://www.pagopar.com/) con credenciales de API

---

## Instalar desde PyPI

### pip

```bash
pip install pagopar-sdk
```

### uv

```bash
uv add pagopar-sdk
```

No se requieren dependencias adicionales más allá de `httpx`.

---

## Variables de entorno

El SDK requiere dos credenciales emitidas por Pagopar desde el panel de comercio:

| Variable | Descripción |
|----------|-------------|
| `PAGOPAR_PUBLIC_KEY` | Tu clave pública (identifica al comercio) |
| `PAGOPAR_PRIVATE_KEY` | Tu clave privada (firma las solicitudes) |

Guardarlas en un archivo `.env` (nunca commitear al repositorio):

```
PAGOPAR_PUBLIC_KEY=tu_clave_publica
PAGOPAR_PRIVATE_KEY=tu_clave_privada
```

Cargarlas en tu aplicación:

```python
import os
from pagopar_sdk import PagoparClient

client = PagoparClient(
    public_key=os.environ["PAGOPAR_PUBLIC_KEY"],
    private_key=os.environ["PAGOPAR_PRIVATE_KEY"],
)
```

O usar `python-dotenv` / `pydantic-settings` para carga automática del `.env` en
proyectos con [FastAPI](fastapi-example.md) y [Django](django-example.md).

---

## Uso básico

```python
from pagopar_sdk import PagoparClient

# Context manager — el cliente se cierra automáticamente
with PagoparClient(public_key="...", private_key="...") as client:
    formas = client.commerce.get_payment_methods()
    print(formas["resultado"])
```

O manejar el ciclo de vida manualmente:

```python
client = PagoparClient(public_key="...", private_key="...")
try:
    resultado = client.commerce.get_payment_methods()
finally:
    client.close()
```

---

## Opcional: deshabilitar el lanzamiento automático de errores

Por defecto el SDK lanza `PagoparBusinessError` cuando la API devuelve
`respuesta: false`. Se puede deshabilitar para inspeccionar la respuesta cruda:

```python
client = PagoparClient(
    public_key="...",
    private_key="...",
    raise_on_api_error=False,
)
resultado = client.commerce.reverse_order("HASH_PEDIDO")
if not resultado.get("respuesta"):
    print("Reversión fallida:", resultado)
```

---

## Instalar desde fuente (contribuidores)

```bash
git clone https://github.com/devpbeat/pagopar-sdk
cd pagopar-sdk

# con pip
pip install -e ".[dev]"

# o con uv
uv sync --extra dev
```

Ejecutar tests:

```bash
pytest
```

---

## Instalar dependencias de documentación

```bash
# con uv
uv sync --extra docs

# o con pip
pip install -e ".[docs]"
```

Servir localmente:

```bash
mkdocs serve
```
