# Policies

`Policy.default()` enables structured identifiers plus person, organization, and location entities
when a configured backend can detect them. `Policy.strict()` also enables secrets and URL
credentials with a lower threshold. `Policy.llm()` enables all available entities.
`Policy.financial()` limits detection to IBANs and payment cards.

Paths are dot-separated segments. `*` matches one segment, so `messages.*.content` matches list
indices. Exclusions win over inclusions. Dictionary keys are not transformed.
