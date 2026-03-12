# Publicar en PyPI

Este proyecto está empaquetado con [pyproject.toml](https://github.com/devpbeat/pagopar-sdk/blob/main/pyproject.toml)
y se publica automáticamente en PyPI mediante GitHub Actions usando
**OIDC trusted publishing** — sin tokens de larga duración.

---

## Release automatizado (camino principal)

Hacer push de un tag de versión dispara el workflow
[publish-pypi.yml](https://github.com/devpbeat/pagopar-sdk/blob/main/.github/workflows/publish-pypi.yml),
que:

1. Construye el sdist y wheel con `uv build`
2. Valida los artefactos con `twine check`
3. Publica en PyPI vía `pypa/gh-action-pypi-publish` usando OIDC (sin token)

### Pasos de release

```bash
# 1. Bumpar versión en pyproject.toml y commitear
git add pyproject.toml
git commit -m "chore: bump version to x.y.z"

# 2. Crear tag y hacer push — esto dispara el workflow
git tag vx.y.z
git push origin main --tags
```

El workflow corre con cualquier tag que empiece con `v*`. Se puede monitorear en
`https://github.com/devpbeat/pagopar-sdk/actions`.

### Configuración en PyPI (ya realizada)

El environment `pypi` del repositorio debe tener configurado un trusted publisher
en la configuración del proyecto en PyPI:

- **Owner:** `devpbeat`
- **Repository:** `pagopar-sdk`
- **Workflow:** `publish-pypi.yml`
- **Environment:** `pypi`

---

## Release manual (alternativa)

Si se necesita publicar fuera de CI:

### 1) Construir

```bash
uv build
```

Genera `dist/*.tar.gz` y `dist/*.whl`.

### 2) Validar

```bash
uv tool run twine check dist/*
```

### 3) Publicar en TestPyPI primero (recomendado)

```bash
uv tool run twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

### 4) Publicar en PyPI

```bash
uv tool run twine upload dist/*
```

Se pedirá `__token__` como usuario y el API token de PyPI como contraseña.
En Windows PowerShell se pueden setear como variables de entorno:

```powershell
$env:TWINE_USERNAME="__token__"
$env:TWINE_PASSWORD="pypi-xxxxxxxxxxxxxxxx"
uv tool run twine upload dist/*
```

---

## Verificar el release

```bash
pip install pagopar-sdk
# o fijando versión
pip install pagopar-sdk==x.y.z
```

---

## Checklist pre-release

- [ ] Versión bumpeada en `pyproject.toml`
- [ ] Release notes actualizadas
- [ ] `README.md` al día (se usa como descripción del proyecto en PyPI)
- [ ] Todos los tests pasando en `main`
- [ ] El tag coincide con la versión (`v0.2.0` → `version = "0.2.0"`)
