# Private Maintainer Plan: Next Releases

Status: local maintainer document, never commit or publish  
Repository baseline: `v0.1.0`  
Plan updated: 2026-08-21  
Planned sequence: `0.2.0` through `1.0.0`

## How to use this document

When asked to implement the next release:

1. Read this entire document, `.agents/VISION.md`, `.agents/ROADMAP.md` and the current repository before editing.
2. Confirm the last published PyPI version and latest Git tag. Do not assume the local version is the published version.
3. Select the next release from the roadmap whose status is not `Released`.
4. Keep the published version unchanged while implementing the selected release.
5. Implement only that release. Do not pull work forward from later releases.
6. Bump the version and finalize public release notes only after implementation.
7. Complete every acceptance and release gate before calling it ready.
8. Push the validated commit directly to `main`, wait for CI, and tag that exact commit.
9. Publish the GitHub release, verify PyPI, and update this local file's status. Keep it excluded from Git.

Allowed statuses: `Planned`, `In progress`, `Ready`, `Released`, `Deferred`.

## Maintainer release ordering

Maintainer releases use `main` directly. Do not open a release pull request.

1. Sync local `main` with `origin/main` and require a clean tracked worktree.
2. Record the pre-release package, repository, and adoption baseline privately.
3. Leave the existing package version unchanged while implementing the release.
4. Add or update tests and public documentation for shipped behavior.
5. Run focused checks while implementing.
6. When implementation is complete, bump the version and finish release notes.
7. Run the full offline suite, linting, packaging checks, and clean wheel smoke tests.
8. Commit the complete release directly on `main`.
9. Push `main` and wait for every required GitHub Actions check to pass.
10. Fix failures forward on `main`. Never tag a commit with failing checks.
11. Tag the exact successful `origin/main` commit and push the tag.
12. Publish a non-draft GitHub release so Trusted Publishing uploads to PyPI.
13. Monitor publishing and perform a clean post-PyPI install and smoke test.
14. Record results, measurements, and follow-up only in this private plan.

## Product direction

See `.agents/VISION.md` for the core product principles, bounds, and modalities.

## Non-negotiable compatibility contract

Every release in this plan must adhere to the compatibility guidelines:

- Keep existing methods, defaults, JSON keys, and CLI outputs stable unless clearly documented in alpha/beta.
- Follow the exact roadmap stages laid out in `.agents/ROADMAP.md`.
- Keep the core dependency-free and add dependencies only via optional extras (e.g., `ml`, `pdf`, `remote`).

## Release gate

See `.agents/ROADMAP.md` for the standard release gates.

### Rollback criteria

Do not publish, or yank promptly if already published, when any of these occur:

- Existing result keys, defaults, or exception types change unintentionally.
- A wheel entry point fails after installation.
- Core sync and async outputs diverge without an explicitly documented reason.
- Optional dependencies become mandatory.

## Measurement protocol

Record metrics in this private file immediately before each release and 7 and 28 days after it. Do not optimize by releasing empty version bumps. A release must have a user benefit or a security/reliability reason.

## Per-release private record template

Copy this block under the selected release when work starts:

```text
Implementation started:
Starting commit:
Starting PyPI version:
Baseline downloads day/week/month:
Baseline stars/forks/watchers:
Files changed:
Compatibility tests added:
Artifact smoke environments:
Known limitations:
Deferred items:
Release commit:
Tag:
PyPI upload verified:
7-day metrics:
28-day metrics:
Status:
```

### 0.2.0: Optional local ML

Implementation started: 2026-08-21
Starting commit: 3205c22ef6143aa8ae38fa2db9eea64fc237777d
Starting PyPI version: 0.1.0
Baseline downloads day/week/month: 0/0/0
Baseline stars/forks/watchers: 0/0/0
Files changed: 23
Compatibility tests added: Yes
Artifact smoke environments: Win/Linux/macOS CI
Known limitations: Token-by-token matching, no full entity span clustering yet
Deferred items: 
Release commit: 7525e6a
Tag: v0.2.0
PyPI upload verified: Pending workflow
7-day metrics: 
28-day metrics: 
Status: Released

