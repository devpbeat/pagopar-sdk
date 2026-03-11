# Contribuir

Este proyecto es open source y acepta contribuciones.

Para la guía completa, ver [CONTRIBUTING.md](https://github.com/devpbeat/pagopar-sdk/blob/main/CONTRIBUTING.md).

## Setup rápido para contribuir

```bash
uv sync --extra dev --extra docs
```

## Comandos útiles

### Lint

```bash
uv run ruff check .
```

### Tests

```bash
uv run pytest
```

### Validación rápida del SDK

```bash
uv run python -m compileall src
```

### Build de documentación

```bash
uv run --extra docs mkdocs build
```

## Qué conviene actualizar al contribuir

- código fuente en `src/pagopar_sdk/`
- documentación en `docs/`
- documentación en español en `docs/es/` cuando aplique
- ejemplos y README si cambia el comportamiento público

## Qué se espera en un pull request

- que sea enfocado
- que incluya documentación si cambia el comportamiento
- que incluya tests cuando corresponda
- que explique claramente la motivación
