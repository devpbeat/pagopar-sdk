# Publishing to PyPI

This project is already packaged with [pyproject.toml](https://github.com/devpbeat/pagopar-sdk/blob/main/pyproject.toml), so publishing to PyPI is straightforward.

## Before publishing

Check these items first:

1. Confirm the package name is available on PyPI.
2. Bump the version in [pyproject.toml](https://github.com/devpbeat/pagopar-sdk/blob/main/pyproject.toml).
3. Make sure [README.md](https://github.com/devpbeat/pagopar-sdk/blob/main/README.md) is ready, since it becomes the project description on PyPI.

## 1) Build the package

From the project root:

```bash
uv build
```

This generates:

- `dist/*.tar.gz`
- `dist/*.whl`

## 2) Validate the artifacts

```bash
uv tool run twine check dist/*
```

## 3) Create a PyPI API token

In PyPI:

- Create an account
- Generate an API token
- Keep the token somewhere safe

## 4) Publish manually from Windows PowerShell

```powershell
$env:TWINE_USERNAME="__token__"
$env:TWINE_PASSWORD="pypi-xxxxxxxxxxxxxxxx"
uv tool run twine upload dist/*
```

## 5) Optional: publish to TestPyPI first

```powershell
$env:TWINE_USERNAME="__token__"
$env:TWINE_PASSWORD="pypi-xxxxxxxxxxxxxxxx"
uv tool run twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

## 6) Verify installation

```bash
pip install pagopar-sdk
```

Or pin a version:

```bash
pip install pagopar-sdk==0.1.0
```

## Recommended release flow

1. Update version in [pyproject.toml](https://github.com/devpbeat/pagopar-sdk/blob/main/pyproject.toml)
2. Commit changes and tag the release
3. Run `uv build`
4. Run `uv tool run twine check dist/*`
5. Upload to TestPyPI or PyPI

## Recommended metadata improvements

For a better PyPI page, consider adding these fields to [pyproject.toml](https://github.com/devpbeat/pagopar-sdk/blob/main/pyproject.toml):

- `authors`
- `license`
- `classifiers`
- `keywords`
- `project.urls`

## Optional next step: trusted publishing

The best long-term setup is publishing from CI with PyPI trusted publishing instead of uploading manually with a token.
