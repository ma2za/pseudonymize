# pseudonymize.io — coding-agent visual contract

This is the **source of truth** for visual implementation. Read it before touching UI.

## 0. Objective
Build a privacy/data-infrastructure product that feels precise, calm, inspectable, and trustworthy. Do not style it like generic “cybersecurity”.

The brand is based on one literal operation:

`ORIGINAL IDENTIFIER  ⇄  PSEUDONYM`

while the surrounding structure remains intact.

**Brand line:** `Keep the context. Replace the identifiers.`

That wording is intentional. Do not casually change it to “lose identity” or “anonymize”: pseudonymization and anonymization are not the same claim.

## 1. Visual concept: preserved frame / mapped identity
The logo is no longer a slash-through-P. The symbol contains:
- outer brackets = structure/context is preserved
- open circle = original identifier
- compact square token = pseudonym
- short cipher bond = stable relationship/mapping

Never reinterpret the symbol as a shield, lock, delete icon, or disabled state.

## 2. Priority
1. Product behavior and accessibility
2. Verified privacy/security facts
3. These brand rules
4. Existing styling

Do not change backend/security behavior to satisfy the design.

## 3. Mandatory files
Read:
- `src/brand/brand.config.ts`
- `src/brand/tokens.css`
- `src/brand/components.css`
- `agent/specs/tokens.json`
- relevant page spec under `agent/specs/`
- `agent/checklists/visual-qa.md`
- `agent/checklists/security-claims.md`

## 4. Semantic color grammar
Do not treat the palette as decoration.

### Cipher `#5BD6AE`
Use for:
- pseudonyms / transformed identifiers
- mapping bond
- primary CTA
- completed pseudonymization state

Do **not** use it for every icon, border, heading or background.

### Sensitive `#E7B35A`
Use for an original identifier that requires attention/review. Sensitive is not an error.

### Danger `#E97474`
Failures and destructive actions only.

### Neutral
Everything else. Secure products should not look like a traffic light exploded inside them.

## 5. Typography
- Sans: Inter/system sans
- Mono: IBM Plex Mono/system mono
- Mono is semantic, not aesthetic. Use it for pseudonyms, hashes, IDs, code, file metadata, entity labels.
- Do not typeset long paragraphs in mono.
- Headings use normal text color. No green gradient headlines.

## 6. Geometry
- 4 / 6 / 8 / 12 px radii only for ordinary UI
- controls are normally 40px high
- borders before shadows
- shadows only for overlays/floating surfaces
- no 24–32px “friendly SaaS” card radii
- keep product density tighter than marketing density

## 7. Layout grammar
The recurring motif is a **rail**: original value on one side, pseudonym on the other, connected by a restrained bond. Use this in demos, mapping views and explanations.

Do not make every section a grid of floating cards. Prefer:
- rails
- split panes
- rows
- bordered sections
- tables
- code/data surfaces

## 8. Logo usage
Assets: `/public/brand`.
- dark surfaces: `lockup-dark.svg`, `mark-dark.svg`
- light surfaces: `lockup-light.svg`, `mark-light.svg`
- single-color contexts: `mark-mono.svg`
- favicon: `favicon.svg`

Do not redraw, animate, rotate, glow, outline, or put the mark inside another shield/container. The dark/light mark already contains its app-tile background.

For navbars, use the `Logo` component rather than reimplementing asset logic.

## 9. Security/privacy claims
**Never infer trust facts from the category of the product.** Do not invent:
- SOC 2 / ISO 27001 / HIPAA
- GDPR “compliant” guarantees
- data residency
- EU-only processing
- zero retention
- local-only processing
- end-to-end encryption
- encryption algorithms
- DPA availability
- penetration testing
- subprocessor claims
- “military-grade”, “unhackable”, “zero-risk”, “bulletproof”

A rendered trust claim requires `label`, `value`, `source`, and `verifiedAt` in `src/brand/security.ts` or an equivalent repository source.

If none exist, omit the trust-facts section in production.

## 10. Copy rules
Prefer exact operational language:
- `Pseudonymized`
- `Original identifier`
- `Sensitive identifier`
- `Review required`
- `Processing`
- `Failed`

Avoid calling an output `Safe`, `Anonymous`, or `Secure` unless that is technically established in context.

Homepage source copy lives in `src/brand/copy.ts`.

## 11. Marketing page
Implement `agent/specs/homepage.json`.

The hero must show the operation, not a decorative illustration. A visitor should understand within seconds that surrounding context remains while the identifier changes.

The page should feel mostly neutral/dark. Cipher green should be scarce enough that pseudonyms immediately attract attention.

## 12. Product UI
Implement `agent/specs/product.json`.

Desktop workspace default:
- source on left
- result on right
- shared toolbar
- visible processing status

Raw/sensitive is not a red error state. Use amber only around the exact identifier. Pseudonymized tokens are mono + cipher.

Never label completion merely `Secure`.

## 13. Docs
Docs are light by default for reading comfort. Code/data blocks can be dark. Do not turn documentation into the marketing homepage.

## 14. Accessibility
- WCAG AA contrast for body/UI text
- visible keyboard focus
- never use color alone for status
- respect reduced motion
- 44px minimum touch target on touch-first surfaces when practical
- do not make pseudonym tokens unreadably tiny

## 15. Forbidden tropes
No decorative:
- shields / padlocks / fingerprints
- matrix rain / hacker silhouettes
- neon cyan-purple gradients
- glassmorphism
- glossy 3D blobs
- AI sparkles / robots
- fake certifications
- random green checkmarks
- giant gradient text
- stock photos of server racks

## 16. Implementation sequence
1. inspect repository framework and existing UI primitives
2. map/import `tokens.css`
3. import `components.css` or port its rules into the existing design system
4. wire logo assets + metadata/favicon
5. port semantic primitives (`PseudonymToken`, `EntityHighlight`, `StatusBadge`, `ProcessorFrame`)
6. implement product surface first if product exists; marketing second
7. populate trust claims only from evidence
8. run tests/build
9. run `node scripts/brand-lint.mjs <repo-root>`
10. execute checklists

## 17. Definition of done
Not “it compiles”. Done means:
- the original→pseudonym relationship is obvious
- the surrounding structure is visually preserved
- color semantics are correct
- no fake security claim exists
- no generic cyber clichés exist
- mobile remains legible and linear
- focus/reduced-motion behavior works
- logo use is consistent
- no random off-palette hardcoded colors were introduced

## 18. Agent autonomy
Do not ask the user to choose trivial visual variants. Follow this system. Surface only genuine product/security ambiguities that cannot be resolved from the repository.
