# Public repository checklist

Complete these operational steps when changing repository visibility. They are not release steps
and do not require a package publication.

## Before changing visibility

- Review the complete staged diff and confirm that every example uses synthetic data.
- Scan tracked files and Git history for credentials, private documents, and personal data.
- Confirm that release workflows contain no stored PyPI token and use Trusted Publishing.
- Confirm that the repository description, topics, licence, support policy, security policy,
  contribution guide, issue templates, and pull request template are current.
- Decide whether the historical annotated-tag email address is acceptable for public visibility.

## Immediately after changing visibility

- Enable private vulnerability reporting.
- Enable secret scanning and push protection if GitHub makes them available.
- Add a main-branch ruleset that requires pull requests, required CI checks, resolved
  conversations, and linear history, and blocks force pushes and deletion.
- Configure GitHub Pages to deploy through Actions.
- Set the repository variable `ENABLE_PAGES` to `true`.
- Verify that `https://ma2za.github.io/pseudonymize/` is live before advertising it.
- Confirm that blank issues are disabled and every issue template renders correctly.
- Confirm that the CI and licence badges render for signed-out users.
- Review a release workflow log as a signed-out user and confirm it exposes no sensitive values.

## Final public check

- Install the latest PyPI wheel into a clean environment.
- Run the README quickstart and CLI.
- Verify the PyPI provenance identity and GitHub release artifact digests.
- Open the repository in a signed-out browser and check README links, package links, security
  reporting, issue intake, and clone instructions.
