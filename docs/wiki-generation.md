# Wiki generation

## Recommended tool

For this SDK, use **MkDocs + Material for MkDocs**.

Why this is a good fit:

- Markdown-first workflow (`.md` files only for content)
- Fast local preview
- Easy publish to GitHub Pages
- Good navigation/search for technical docs

## Commands

Install docs dependencies:

```bash
uv sync --extra docs
```

Local preview:

```bash
mkdocs serve
```

Build static site:

```bash
mkdocs build
```

## Publish options

### Option A: GitHub Pages (quickest)

```bash
mkdocs gh-deploy --clean
```

This creates/updates the `gh-pages` branch with the generated site.

### Option B: CI/CD pipeline

Run `mkdocs build` in CI and deploy the generated `site/` folder to your hosting platform.

## Content structure

All documentation content is under `docs/` and stored as Markdown files:

- `docs/index.md`
- `docs/wiki-generation.md`
- `docs/django-example.md`
- `docs/fastapi-example.md`
- `docs/flask-example.md`
