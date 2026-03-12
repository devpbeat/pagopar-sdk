# Publishing to PyPI

This project is packaged with [pyproject.toml](https://github.com/devpbeat/pagopar-sdk/blob/main/pyproject.toml)
and publishes automatically to PyPI via GitHub Actions using
**OIDC trusted publishing** — no long-lived API tokens needed.

---

## Automated release (primary path)

Pushing a version tag triggers the
[publish-pypi.yml](https://github.com/devpbeat/pagopar-sdk/blob/main/.github/workflows/publish-pypi.yml)
workflow, which:

1. Builds the sdist and wheel with `uv build`
2. Validates artifacts with `twine check`
3. Publishes to PyPI via `pypa/gh-action-pypi-publish` using OIDC (no token required)

### Release steps

```bash
# 1. Bump version in pyproject.toml, commit
git add pyproject.toml
git commit -m "chore: bump version to x.y.z"

# 2. Tag and push — this triggers the workflow
git tag vx.y.z
git push origin main --tags
```

The workflow runs on any tag matching `v*`. Monitor it at
`https://github.com/devpbeat/pagopar-sdk/actions`.

### One-time PyPI setup (already done)

The repository's `pypi` environment must be configured with a trusted publisher
in your PyPI project settings:

- **Owner:** `devpbeat`
- **Repository:** `pagopar-sdk`
- **Workflow:** `publish-pypi.yml`
- **Environment:** `pypi`

---

## Manual release (fallback)

If you need to publish outside of CI:

### 1) Build

```bash
uv build
```

Generates `dist/*.tar.gz` and `dist/*.whl`.

### 2) Validate

```bash
uv tool run twine check dist/*
```

### 3) Publish to TestPyPI first (recommended)

```bash
uv tool run twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

### 4) Publish to PyPI

```bash
uv tool run twine upload dist/*
```

You will be prompted for `__token__` as username and your PyPI API token as password.
On Windows PowerShell you can set them as env vars to avoid the prompt:

```powershell
$env:TWINE_USERNAME="__token__"
$env:TWINE_PASSWORD="pypi-xxxxxxxxxxxxxxxx"
uv tool run twine upload dist/*
```

---

## Verify the release

```bash
pip install pagopar-sdk
# or pin a specific version
pip install pagopar-sdk==x.y.z
```

---

## Pre-release checklist

- [ ] Version bumped in `pyproject.toml`
- [ ] `CHANGELOG` / release notes updated
- [ ] `README.md` accurate (it becomes the PyPI project description)
- [ ] All tests passing on `main`
- [ ] Tag matches version (`v0.2.0` → `version = "0.2.0"`)
