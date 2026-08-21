# Contributing

Pseudonymize is in beta. The dependency-free core API is frozen through `0.1.0`; changes must
follow the compatibility policy. A necessary breaking core redesign returns the project to beta
rather than adding an undocumented compatibility shim.

## Development setup

Install [uv](https://docs.astral.sh/uv/), fork the repository, and run:

```console
uv sync --all-extras --all-groups
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

## Compatibility

Public names, documented constructors and methods, CLI behavior, and token formats remain stable
from `0.1.0b1` through `0.1.0`. Release candidates accept only release-blocking fixes. See
[docs/compatibility.md](docs/compatibility.md).

Read [SECURITY.md](SECURITY.md), [SUPPORT.md](SUPPORT.md), and
[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.
