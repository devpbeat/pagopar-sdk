# Generación de wiki

## Herramienta recomendada

Para este SDK, conviene usar **MkDocs + Material for MkDocs**.

Motivos:

- Flujo centrado en Markdown (`.md` para todo el contenido)
- Vista previa local rápida
- Publicación sencilla en GitHub Pages
- Buena navegación y búsqueda para documentación técnica

## Comandos

Instalar dependencias de documentación:

```bash
uv sync --extra docs
```

Vista previa local:

```bash
mkdocs serve
```

Generar sitio estático:

```bash
mkdocs build
```

## Opciones de publicación

### Opción A: GitHub Pages

```bash
mkdocs gh-deploy --clean
```

### Opción B: CI/CD

Ejecutar `mkdocs build` en CI y desplegar la carpeta `site/`.

## Estructura del contenido

Todo el contenido vive en `docs/` como archivos Markdown:

- `docs/index.md`
- `docs/wiki-generation.md`
- `docs/django-example.md`
- `docs/fastapi-example.md`
- `docs/flask-example.md`
- `docs/es/index.md`
- `docs/es/wiki-generation.md`
- `docs/es/django-example.md`
- `docs/es/fastapi-example.md`
- `docs/es/flask-example.md`
