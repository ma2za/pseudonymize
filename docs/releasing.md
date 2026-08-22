# Releasing

Releases use locked dependencies, GitHub environments, and PyPI Trusted Publishing. Do not store a
PyPI token in repository or environment secrets.

## One-time setup

1. Create a protected GitHub environment named `pypi`.
2. On PyPI, configure the pending publisher for owner `ma2za`, repository `pseudonymize`, and
   workflow `release.yml`. Keep the publisher's optional environment field blank. The workflow
   still uses the GitHub `pypi` environment.
3. When the repository plan supports Pages, enable Pages through GitHub Actions and
   set the repository variable `ENABLE_PAGES` to `true`. Until then, documentation
   builds remain required while deployment is skipped.
4. Protect `main`: require pull requests and CI, resolved conversations, and linear history; block
   force pushes and deletion.

After the first upload, verify that the pending publisher became an ordinary project publisher.

## Prepare a release

1. Create a release branch from current `main`.
2. Set the version in `pyproject.toml` and add the dated changelog entry.
3. Run:

   ```console
   uv sync --all-extras --all-groups --frozen
   uv run ruff format --check .
   uv run ruff check .
   uv run mypy
   uv run pytest
   uv run python -m mkdocs build --strict
   uv build
   uv run twine check dist/*
   uv run python scripts/verify_release.py
   
   # Verify the built wheel locally in an isolated environment (simulating CI)
   uv venv --python 3.14 .wheel-venv
   uv pip install --python .wheel-venv/bin/python dist/*.whl
   uv pip check --python .wheel-venv/bin/python
   .wheel-venv/bin/python -I scripts/audit_install.py
   .wheel-venv/bin/python -I scripts/smoke_wheel.py
   .wheel-venv/bin/pseudonymize detectors
   ```

4. Open a pull request and merge only after every required check passes.

## Artifact rehearsal

Run the `Package` workflow manually from the merged commit. It builds and validates the exact
artifacts without publishing them, then installs the wheel on every supported operating-system and
Python-version combination. Download the retained distributions when manual inspection is needed.

## PyPI publication

1. Create an annotated tag whose version exactly matches `pyproject.toml`:

   ```console
   git tag -a v0.1.0 -m "Release 0.1.0"
   git push origin v0.1.0
   ```

2. The tag workflow reruns quality, tests, documentation, and artifact validation.
3. GitHub creates a prerelease for alpha, beta, and release-candidate versions and attaches the
   exact wheel and source distribution published to PyPI.
4. Install from PyPI in a new environment and rerun the quickstart and CLI smoke test.
5. Confirm the PyPI metadata, provenance, Python requirement, licence, project links, wheel size,
   `py.typed`, and absence of runtime dependencies.

The production tag is the only package-publication path. Manual workflow dispatches never publish
to TestPyPI or PyPI.

Never reuse a published version. Fixes require a new prerelease or patch version.
