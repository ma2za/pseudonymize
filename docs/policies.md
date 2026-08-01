# Policies

`Policy.default()` enables structured identifiers plus person, organization, and location entities
when a configured backend can detect them. `Policy.strict()` also enables secrets and URL
credentials with a lower threshold. `Policy.llm()` enables all available entities.
`Policy.financial()` limits detection to IBANs and payment cards.

Paths are dot-separated segments. `*` matches one segment, so `messages.*.content` matches list
indices. Exclusions win over inclusions. Dictionary keys are not transformed.

## Network policy

`NetworkPolicy.DENY` is the default and prevents every remote-capable backend invocation.
`ALLOW_CONFIGURED` permits only names copied into `allowed_remote_backends`. `ALLOW_ALL` removes
the allowlist check. Both allowing modes still require `allow_remote_processing=True` on each
remote backend:

```python
from pseudonymize import NetworkPolicy, Policy

policy = Policy(
    network_policy=NetworkPolicy.ALLOW_CONFIGURED,
    allowed_remote_backends={"company_provider"},
)
```

The base package provides no remote backend or HTTP dependency.
