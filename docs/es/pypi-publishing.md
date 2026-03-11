# Publicar en PyPI

Este proyecto ya está empaquetado con [pyproject.toml](https://github.com/devpbeat/pagopar-sdk/blob/main/pyproject.toml), así que publicarlo en PyPI es bastante directo.

## Antes de publicar

Conviene revisar esto primero:

1. Confirmar que el nombre del paquete esté disponible en PyPI.
2. Incrementar la versión en [pyproject.toml](https://github.com/devpbeat/pagopar-sdk/blob/main/pyproject.toml).
3. Verificar que [README.md](https://github.com/devpbeat/pagopar-sdk/blob/main/README.md) esté listo, porque se usa como descripción del proyecto en PyPI.

## 1) Construir el paquete

Desde la raíz del proyecto:

```bash
uv build
```

Esto genera:

- `dist/*.tar.gz`
- `dist/*.whl`

## 2) Validar los artefactos

```bash
uv tool run twine check dist/*
```

## 3) Crear un token API de PyPI

En PyPI:

- Crear una cuenta
- Generar un API token
- Guardarlo en un lugar seguro

## 4) Publicar manualmente desde Windows PowerShell

```powershell
$env:TWINE_USERNAME="__token__"
$env:TWINE_PASSWORD="pypi-xxxxxxxxxxxxxxxx"
uv tool run twine upload dist/*
```

## 5) Opcional: publicar primero en TestPyPI

```powershell
$env:TWINE_USERNAME="__token__"
$env:TWINE_PASSWORD="pypi-xxxxxxxxxxxxxxxx"
uv tool run twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

## 6) Verificar instalación

```bash
pip install pagopar-sdk
```

O fijando versión:

```bash
pip install pagopar-sdk==0.1.0
```

## Flujo recomendado de release

1. Actualizar la versión en [pyproject.toml](https://github.com/devpbeat/pagopar-sdk/blob/main/pyproject.toml)
2. Hacer commit y tag del release
3. Ejecutar `uv build`
4. Ejecutar `uv tool run twine check dist/*`
5. Subir a TestPyPI o PyPI

## Mejoras recomendadas de metadata

Para una mejor página en PyPI, conviene agregar estos campos en [pyproject.toml](https://github.com/devpbeat/pagopar-sdk/blob/main/pyproject.toml):

- `authors`
- `license`
- `classifiers`
- `keywords`
- `project.urls`

## Siguiente mejora opcional: trusted publishing

La mejor configuración a largo plazo es publicar desde CI con trusted publishing de PyPI, en lugar de subir manualmente con token.
