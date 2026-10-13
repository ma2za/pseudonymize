# Codex Cloud handover

This public repository contains the Python engine, CLI, optional hosted HTTP service,
tests, benchmark tooling and results, release procedures, and maintainer commands.
The hosted Next.js gateway lives in the separate `ma2za/pseudonymize.io` repository.
Preserve the current repository visibility. Follow `INSTRUCTIONS.md` for engineering
and benchmark integrity; no external instruction file or sibling checkout is needed.

## Environment setup

Use `uv` and Python 3.13 for the full development environment. Configure the cloud
environment's install script as:

```bash
bash scripts/codex-cloud-setup.sh
```

The script installs the frozen optional dependencies and development groups, then
installs the existing pre-commit hooks. Python 3.13 is selected because the benchmark
group pins PyArrow 19; the library's supported Python versions remain 3.11 through 3.14.
Linux OCR checks additionally need the `tesseract-ocr` system package. The existing
`scripts/install_tesseract.py` installs it through sudo/apt on supported Linux hosts.

```bash
uv run --frozen ruff format --check .
uv run --frozen ruff check .
uv run --frozen mypy
uv run --frozen pytest
uv run --frozen python -m mkdocs build --strict
uv build
uv run --frozen twine check dist/*
uv run --frozen python scripts/verify_release.py
```

The ONNX tests use a real quantized model. Their fixture downloads model files into
an ignored cache and verifies fixed SHA-256 hashes. Allow network access for initial
dependency and model downloads. Model caches, datasets, training outputs, virtual
environments, and debug logs stay outside Git. No production credentials are needed
for library development or tests.

Optional gazetteer word lists are loaded from `data/gazetteer` when present. They
are ignored local inputs and can change default rule detections. The memory-store
tests explicitly exercise both absent and configured name dictionaries so checks
do not depend on a workstation's word lists. Existing local data is retained;
it is not silently uploaded or discarded by this handover.

The default library remains dependency-free. The `service` extra is optional and
does not import or initialize the hosted service through a base library import.
See `deployment/README.md` for verified service/model assets and gateway authentication.
Gateway deployment, AWS authentication, PyPI publishing, and GitHub releases are
separate actions; this setup script performs none of them. See `docs/releasing.md`
for the release gates. A merge repair is not a release and does not establish a new
benchmark score.

## Preserved merge work

The October 13, 2026 repair completes the pending merge of the local history and the
incoming history. Both parents remain reachable from the merge commit. It retains
the local public interfaces, tests and historical benchmark documentation, the
newer ONNX/coreference/Bloom and release-evidence fixes, and both agent command
directories. The project keeps the incoming development version `1.37.0`;
no published tag or release is replaced. `uv` validates the lock against the combined
project metadata. The duplicate historical benchmark block is retained once.

A verified local snapshot of the pre-resolution working tree, merge index, and
Git histories is retained outside this checkout. Local ignored files and caches
are kept intact. They are not required by the clean checkout and are not uploaded
as raw document or model archives. Never inspect held-out validation rows to tune
detectors; use the training split and follow the repository's benchmark rules.
