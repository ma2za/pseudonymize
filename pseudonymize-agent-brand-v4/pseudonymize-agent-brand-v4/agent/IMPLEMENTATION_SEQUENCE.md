# Implementation sequence

## Pass 1 — inventory
- framework / router
- CSS / Tailwind / component system
- current favicon/logo/metadata
- existing product surfaces
- actual API schema
- verified security/privacy facts

## Pass 2 — foundations
- map `tokens.css`
- install/confirm fonts only if the repo already has a font strategy; otherwise use fallbacks
- integrate logo assets
- wire metadata/favicon

## Pass 3 — semantic primitives
- pseudonym token
- sensitive-identifier highlight
- status badge
- transformation/mapping row
- processor frame
- buttons

## Pass 4 — product
Implement working product surfaces before polishing marketing screenshots. Real product UI is part of the identity.

## Pass 5 — marketing
Implement the homepage spec using actual product semantics/examples.

## Pass 6 — docs/email where present
Do not create unused surfaces just because the kit contains a spec.

## Pass 7 — verification
- tests / typecheck / build
- brand lint
- visual QA
- security-claims QA
- responsive keyboard check


## Content pass
For every implemented route, map it to `agent/SITEMAP_AND_MESSAGING.md`, load the matching page/app JSON spec, then wire copy from `src/brand/copy.ts`. Do not create unsupported proof, pricing, API, or trust content.
