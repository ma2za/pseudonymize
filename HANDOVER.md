# Engineering handover

Read this file and `ROADMAP.md` before changing the project. The recovery roadmap in
`ROADMAP.md` is authoritative when it conflicts with an older changelog claim or aspirational
release name.

## Non-negotiable standard

Do not manufacture progress.

- Do not call a test, benchmark, release, PyPI upload, CI job, or documentation build successful
  unless its command completed successfully in the current worktree and its result was observed.
- Do not convert an unverified assertion into a roadmap “Completed” item. State what was run, what
  was not run, and the remaining evidence required.
- Do not claim an F1 improvement without the same immutable dataset revision, split, seed, scoring
  mode, supported-label set, model hashes, policy, and per-entity counts as the comparison run.
- Do not weaken checksum validation, network consent, or value-safe diagnostics for a benchmark or
  convenience path. Test/benchmark accommodations must be explicit and inaccessible through normal
  public processing configuration.
- Do not commit or discard another person's work. `AGENTS.md` is currently a user-owned local
  deletion and must remain out of commits unless the user explicitly asks otherwise.

## Current release state

`1.26.0` is in development. It is a contract-and-evidence release, not an enterprise DLP broker.
`1.27.0` may not become the active release until `1.26.0` exit criteria are evidenced.

Completed and already pushed before this handover:

- `8ec7e11 chore: restore dependency-free base release contract`
- `27e2be8 fix: harden optional remote and benchmark paths`

Uncommitted work at handover time must be reviewed, tested, then committed as a coherent change:

- Release metadata guard: current-version changelog entries cannot be marked published without a
  matching tag; tagged releases require a matching dated changelog entry.
- Evaluator reproducibility: remote datasets require `--dataset-revision`; `--output` writes a JSON
  record with configuration, counts, metrics, local-corpus hash, and ML artifact hashes.
- Evaluator CLI fixture coverage in `tests/unit/test_quality_evaluator.py`.

Always run `git status --short` first. Treat this section as a starting clue, not a substitute for
the actual worktree.

## Work completed in `1.26.0` and `1.27.0` (active uncommitted worktree)

- The base wheel has no runtime dependencies. `scripts/verify_release.py` and
  `scripts/audit_install.py` enforce that exact contract.
- Clean-wheel tests cover base install and every documented extra (`html`, `ml`, `ocr`, `office`,
  `pdf`, `remote`) independently via `scripts/audit_extras.py` and `scripts/audit_install.py --extra`.
- `scripts/verify_release.py` verifies wheel `Provides-Extra` matches the documented extras exactly.
- `HTTPRemoteBackend` is optional, requires HTTPS, does not follow redirects, retains explicit
  timeout/retry settings, and sanitizes request, status, and JSON errors.
- Active documentation across `README.md`, `docs/deployment.md`, `docs/limitations.md`,
  `docs/threat-model.md`, `docs/policies.md`, and `HTTPRemoteBackend` docstrings reconciled:
  callers/applications are explicitly responsible for bounding content block sizes and setting
  timeouts.
- `SYNTHETIC_BENCHMARK` no longer changes library behavior. Synthetic checksum accommodation is
  private to benchmark tooling and explicitly flagged in the evaluator.
- Evaluator reproducibility complete: remote datasets require `--dataset-revision` (pinned in docs
  to `a785eb528e28be2693c3718a27e066970de5dadb`), `--output` writes JSON with package version,
  git commit, policy configuration, counts, metrics, local-corpus hash, and ML artifact hashes.
- CI-safe deterministic evaluator fixture coverage in `tests/unit/test_quality_evaluator.py`.
- Scheduled/manual trusted full-benchmark workflow in `.github/workflows/quality-benchmark.yml`.
- Security regression corpus established in `tests/integration/test_security_regression_corpus.py`
  covering Unicode controls & zero-width characters (ZWNJ, soft hyphen, ZWSP, word joiners, bidi
  overrides/isolates), deeply nested payloads, streaming chunk splits, JSON/CSV boundary escapes and
  formula injections, document metadata isolation, and hostile remote responses.
- Policy defaults and network egress isolation audit complete in `tests/unit/test_policy_defaults_audit.py`,
  verifying all 12 entity types under default/strict policies, and proving denied remote paths never
  touch socket creation or DNS resolution.

## Remaining work, in strict order

1. Audit held-out benchmark and baseline measurements.
   - Run a clean baseline record of `1.27.0` against the pinned immutable dataset revision.
2. Only then consider `1.28.0` detector changes. Each rule needs locale scope, positive and
   negative cases, false-positive rationale, and held-out evidence.

## Required verification before any commit

Run the narrow tests for changed modules first, then run all applicable gates:

```console
uv run pre-commit run --all-files
uv run mypy
uv run python -m pytest
uv run python -m mkdocs build --strict
uv build
uv run python scripts/verify_release.py
```

If a command is blocked by the environment, report that exact limitation. Do not write “passed”
based on an absent terminal summary. Remove generated `dist` artifacts and `.coverage` after
verification unless they are intentionally retained as a user-approved release artifact.

## Commit and release discipline

- Stage files by name; never use a broad stage command while unrelated work exists.
- A normal commit must use hooks. If a hook is broken by the local environment, run its equivalent
  explicitly, record the exact failure, and use `--no-verify` only with the user's authorization.
- Push only when explicitly requested.
- A version is published only after its matching tag, successful release workflow, PyPI artifact,
  and GitHub release exist. Until then, keep changes under `[Unreleased]`.
