# Policies

`Policy.default()` enables structured identifiers. `Policy.strict()` also enables secrets and URL
credentials with a lower threshold. `Policy.llm()` enables all bundled entities. `Policy.financial()`
limits detection to IBANs and payment cards.

Paths are dot-separated segments. `*` matches one segment, so `messages.*.content` matches list
indices. Exclusions win over inclusions. Dictionary keys are not transformed.
