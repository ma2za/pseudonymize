# Component visual specification

## Buttons
- Height: 42 px default, 34 px compact, 48 px large.
- Radius: 8 px.
- Primary: Cipher Green on Ink. Use once per decision area.
- Secondary: transparent + 1 px neutral border.
- Destructive: neutral by default, Danger only on confirmation.

## Inputs
- 42 px min height; 10 px radius; 1 px border.
- Focus ring: 3 px `rgba(72,214,176,.35)` with 2 px offset.
- Technical values may use mono; labels stay sans.

## Token / entity chips
- Pseudonym token: mono, Cipher Green text, low-opacity Cipher background.
- Original sensitive value: do **not** use screaming red; use a quiet rose underline/background only when comparison requires it.
- Entity type is uppercase mono: `PERSON`, `EMAIL`, `PHONE`, `CITY`.

## Cards
- Radius 12–14 px; 1 px border.
- Borders before shadows.
- Never put every section inside a card.

## Tables
- 44 px rows minimum.
- Sticky header permitted.
- Pseudonymized values use mono.
- Original PII should not be visible by default after processing.

## Status
`Pseudonymized` / `Processing` / `Review required` / `Failed` / `Not processed`.
Do not use `Secure` as a job status.

## Empty state
One sentence explaining what goes here + one action. No cute illustrations.

## Dialogs
Use only for actions requiring interruption. Deletion/export of mappings require explicit confirmation and scope.
