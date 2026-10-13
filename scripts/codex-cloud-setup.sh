#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
uv sync --python 3.13 --all-extras --all-groups --frozen
uv run --frozen pre-commit install
