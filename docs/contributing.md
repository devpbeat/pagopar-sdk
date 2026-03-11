# Contributing

This project is open source and contributions are welcome.

For the full contributor guide, see [CONTRIBUTING.md](https://github.com/devpbeat/pagopar-sdk/blob/main/CONTRIBUTING.md).

## Quick contributor setup

```bash
uv sync --extra dev --extra docs
```

## Useful commands

### Lint

```bash
uv run ruff check .
```

### Tests

```bash
uv run pytest
```

### SDK syntax check

```bash
uv run python -m compileall src
```

### Build docs

```bash
uv run --extra docs mkdocs build
```

## What to update when contributing

- source code in `src/pagopar_sdk/`
- docs in `docs/`
- Spanish docs in `docs/es/` when applicable
- examples and README when public behavior changes

## Pull request expectations

- keep PRs focused
- include docs for behavior changes
- include tests when applicable
- explain the motivation clearly
