# pseudonymize.io agent brand kit v3

Implementation package for coding agents. This is not a presentation deck and contains no generated mockup imagery.

## Start here
1. Copy this package into the target repository.
2. Tell the coding agent: **Read `AGENTS.md` and implement the relevant page spec.**
3. The agent should integrate with the existing stack rather than blindly replacing it.

## What changed from v2
- replaced the slash-through-P logo with a mapped-identity symbol that does not read as “disabled P”
- changed the core line from `Lose the identity` to the technically safer `Replace the identifiers`
- separated **sensitive** (amber) from **error** (red)
- reduced decorative green usage
- tightened radii, spacing, and product density
- made the rail/mapping relationship the core layout pattern
- made verified security claims a typed/evidence-backed contract
- removed static preview imagery from the deliverable
- added code-level brand linting and clearer implementation rules

## Core files
- `AGENTS.md` — authoritative coding-agent instructions
- `agent/specs/*.json` — page contracts
- `src/brand/tokens.css` — semantic CSS variables
- `src/brand/components.css` — reference primitive styles
- `src/brand/components/*` — React/Next primitives
- `public/brand/*` — SVG logo assets
- `scripts/brand-lint.mjs` — guardrails against common drift

## Additional machine-readable contracts
- `agent/specs/logo.json`
- `agent/specs/components.json`
- `agent/specs/iconography.json`
- `agent/specs/motion.json`
- `agent/specs/accessibility.json`

The kit intentionally ships no static preview mockups. A coding agent should apply the system to the real product, not copy pixels from a screenshot.
