# Releasing

Releases use locked dependencies, GitHub environments, and PyPI Trusted Publishing. Do not store a
PyPI token in repository or environment secrets.

## One-time setup

1. Create protected GitHub environments named `testpypi` and `pypi`.
2. On TestPyPI, configure a pending trusted publisher for owner `ma2za`, repository
   `pseudonymize`, workflow `release.yml`, and environment `testpypi`.
3. On PyPI, configure the same pending publisher with environment `pypi`.
4. When the repository plan supports Pages, enable Pages through GitHub Actions and
   set the repository variable `ENABLE_PAGES` to `true`. Until then, documentation
   builds remain required while deployment is skipped.
5. Protect `main`: require pull requests and CI, resolved conversations, and linear history; block
   force pushes and deletion.

Pending publishers are required for the first upload because the project does not yet exist on the
package index.

## Prepare a release

1. Create a release branch from current `main`.
2. Set the version in `pyproject.toml` and add the dated changelog entry.
3. Run:

   ```console
   uv sync --all-groups --frozen
   uv run ruff format --check .
   uv run ruff check .
   uv run mypy
   uv run pytest
   uv run mkdocs build --strict
   uv build
   uv run twine check dist/*
   uv run python scripts/verify_release.py
   ```

4. Open a pull request and merge only after every required check passes.

## TestPyPI rehearsal

Run the `Release` workflow manually from the merged commit. Manual dispatch publishes only to the
`testpypi` environment. Install from TestPyPI in a clean environment and run both entry points:

```console
python -m venv test-install
test-install/bin/python -m pip install --index-url https://test.pypi.org/simple/ pseudonymize==0.1.0a1
test-install/bin/python -c "from pseudonymize import pseudonymize; assert pseudonymize('maria@example.com') == '<EMAIL_1>'"
test-install/bin/pseudonymize keygen
```

On Windows, use `test-install\Scripts\python.exe` and `test-install\Scripts\pseudonymize.exe`.

## PyPI publication

1. Create an annotated tag whose version exactly matches `pyproject.toml`:

   ```console
   git tag -a v0.1.0a1 -m "Release 0.1.0a1"
   git push origin v0.1.0a1
   ```

2. The tag workflow reruns quality, tests, documentation, and artifact validation.
3. GitHub creates a prerelease for alpha, beta, and release-candidate versions and attaches the
   exact wheel and source distribution published to PyPI.
4. Install from PyPI in a new environment and rerun the quickstart and CLI smoke test.
5. Confirm the PyPI metadata, provenance, Python requirement, licence, project links, wheel size,
   `py.typed`, and absence of runtime dependencies.

Never reuse a published version. Fixes require a new prerelease or patch version.
