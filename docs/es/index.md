# Wiki de Pagopar SDK

Esta wiki documenta cómo usar `pagopar-sdk` en aplicaciones reales y cómo publicar la documentación como una wiki basada en Markdown.

## Qué incluye

- Una configuración recomendada para generar la wiki (MkDocs + Material)
- Ejemplos de integración completos para:
  - Django
  - FastAPI
  - Flask

## Instalar dependencias del SDK y de la documentación

```bash
uv sync --extra docs
```

O con pip:

```bash
pip install -e ".[docs]"
```

## Ejecutar la documentación localmente

```bash
mkdocs serve
```

Abrir: `http://127.0.0.1:8000`
