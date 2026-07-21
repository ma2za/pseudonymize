# Contributing

Install uv, fork the repository, and run:

```console
uv sync --all-groups
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
uv run mkdocs build --strict
```

Add positive, negative, boundary, Unicode, and adversarial tests with detector changes. Use only
synthetic values in issues, tests, benchmarks, and commits. Public API changes require an ADR.
