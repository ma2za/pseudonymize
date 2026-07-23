# Contributing

Pseudonymize is in active alpha development. Clean API changes are welcome even when they are
breaking. Do not add compatibility aliases, deprecation layers, or migration shims unless the
current roadmap milestone explicitly requires them.

## Development setup

Install [uv](https://docs.astral.sh/uv/), fork the repository, and run:

```console
uv sync --all-groups
uv run ruff format --check .
uv run ruff check .
uv run mypy
uv run pytest
uv run mkdocs build --strict
```

## Pull requests

- Keep each change focused and explain its privacy and security impact.
- Add positive, negative, boundary, Unicode, and adversarial tests where relevant.
- Prefer behavior and invariant tests over implementation-shaped coverage.
- Update public documentation and the changelog when behavior changes.
- Add or update an ADR when a change alters a durable architecture boundary.
- Keep the base package dependency-free.
- Do not introduce network access, model downloads, telemetry, or optional imports into the core.

## Test data

Use only synthetic values in issues, tests, benchmarks, commits, screenshots, and logs. Never paste
real personal data, credentials, access tokens, production payloads, or private documents.

## Alpha compatibility

Until `0.1.0`, contributors should remove obsolete alpha contracts instead of maintaining parallel
old and new APIs. Release notes document material breaks. The stable compatibility policy will be
defined before the first stable release.

Read [SECURITY.md](SECURITY.md), [SUPPORT.md](SUPPORT.md), and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.
