# Contributing to pagopar-sdk

Thanks for contributing to `pagopar-sdk`.

This project aims to provide a clean, well-documented Python SDK for Pagopar, including:

- commerce / checkout integrations
- recurrent payments
- framework examples
- bilingual documentation (`EN` / `ES`)

## Ways to contribute

Contributions are welcome in several forms:

- bug reports
- bug fixes
- documentation improvements
- new examples
- tests
- type-safety improvements
- API ergonomics improvements
- Spanish/English documentation translations

## Before you start

Please try to keep contributions:

- focused
- documented
- typed when possible
- consistent with the existing SDK structure

For larger changes, open an issue first so the direction can be discussed before implementation.

## Development setup

This repository uses `uv`.

### 1) Clone the repository

```bash
git clone https://github.com/devpbeat/pagopar-sdk.git
cd pagopar-sdk
```

### 2) Install dependencies

```bash
uv sync --extra dev --extra docs
```

### 3) Activate the virtual environment (Windows PowerShell)

```powershell
& .venv\Scripts\Activate.ps1
```

## Common commands

### Run quick syntax validation

```bash
uv run python -m compileall src
```

### Run tests

```bash
uv run pytest
```

### Run lint checks

```bash
uv run ruff check .
```

### Build the documentation wiki

```bash
uv run --extra docs mkdocs build
```

### Preview the documentation wiki locally

```bash
uv run --extra docs mkdocs serve
```

## Project structure

- `src/pagopar_sdk/`: SDK source code
- `docs/`: documentation wiki in Markdown
- `docs/es/`: Spanish documentation pages
- `README.md`: main project overview
- `CONTRIBUTING.md`: contributor guide

## Contribution workflow

1. Create a branch from `main`
2. Make your changes
3. Update docs/examples if behavior changes
4. Add or update tests when applicable
5. Run the local checks
6. Open a pull request

## Pull request guidelines

Please include:

- a clear summary of the change
- why the change is needed
- any API changes
- any docs updates included
- sample request/response context if relevant

Small, focused pull requests are preferred over large multi-topic ones.

## Code guidelines

### Python

- Keep code typed where practical
- Prefer small, explicit methods
- Reuse the existing client/model/error structure
- Avoid breaking public APIs unless clearly necessary

### Documentation

- Use Markdown only for docs pages
- Keep examples runnable and realistic
- If you add wiki pages, consider whether both `EN` and `ES` versions are needed

### Examples

- Prefer production-like examples over toy snippets
- Show error handling where useful
- Keep secrets out of examples

## Reporting bugs

When opening a bug report, include:

- what you expected
- what happened instead
- steps to reproduce
- relevant payload or endpoint
- Python version
- package version

## Suggesting features

Feature requests are welcome. Please describe:

- the use case
- the current limitation
- the proposed API or workflow

## Release-related changes

If your contribution affects packaging or releases, please mention it explicitly in the pull request.

Examples:

- `pyproject.toml` metadata changes
- new docs dependencies
- publishing workflow changes
- versioning impact

## Community expectations

Be respectful, constructive, and specific.

The goal is to keep the project approachable for merchants, integrators, and open-source contributors.
