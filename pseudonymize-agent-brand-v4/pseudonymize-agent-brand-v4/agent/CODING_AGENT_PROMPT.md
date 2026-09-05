Read `AGENTS.md` before editing code. Treat it as the authoritative visual implementation contract.

Then inspect the existing repository. Determine its framework, routing, styling system, component library, existing product behavior, and verified security/privacy facts.

Integrate the pseudonymize.io brand system rather than rebuilding unrelated application logic. Use the semantic tokens and components supplied here, adapt them to the repository's conventions where appropriate, and implement the relevant JSON page specs.

Critical requirements:
- preserve all product behavior and accessibility
- use the mapped-identity visual grammar
- keep Cipher Green semantic and scarce
- sensitive identifiers use amber, not error red
- never fabricate API endpoints, capabilities, certifications or security/privacy claims
- do not introduce generic cybersecurity imagery
- use real product UI/examples wherever possible
- run the repository's lint/typecheck/tests/build
- run `node scripts/brand-lint.mjs <repo-root>`
- complete both supplied QA checklists before stopping

Do not ask for trivial aesthetic choices. Make the implementation decisions implied by this system.

## Page and messaging requirements
Before editing a route, read:
- `agent/MESSAGING_SYSTEM.md`
- `agent/SITEMAP_AND_MESSAGING.md`
- the matching route spec in `agent/specs/pages/` or `agent/specs/app/`
- `src/brand/copy.ts`

Treat the supplied page copy as the default source of truth. Replace or extend it only when repository facts make more specific wording necessary. Never invent product formats, SDKs, endpoints, pricing, customer proof, security claims, data handling, or compliance facts to fill a page. Omit unsupported sections instead.
