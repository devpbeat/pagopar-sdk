# Pagopar SDK Wiki

This wiki documents how to use `pagopar-sdk` in real applications and how to publish your docs as a Markdown-powered wiki.

## What you will find here

- A recommended wiki generator setup (MkDocs + Material)
- End-to-end integration examples for:
  - Django
  - FastAPI
  - Flask

## Install SDK and docs dependencies

```bash
uv sync --extra docs
```

Or with pip:

```bash
pip install -e ".[docs]"
```

## Run docs locally

```bash
mkdocs serve
```

Open: `http://127.0.0.1:8000`
