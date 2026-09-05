# Accessibility requirements

- Target WCAG 2.2 AA.
- Body text >= 4.5:1 contrast. Large text >= 3:1.
- Every interactive control has a visible keyboard focus state.
- Never communicate entity/state using color alone; always include type/text/iconography.
- Respect `prefers-reduced-motion`.
- Minimum target size: 24×24 px; preferred 40–44 px for primary controls.
- Editor highlighting must preserve text legibility and selection behavior.
- Before/after panes need accessible headings and linear reading order on mobile.
- Progress/status updates should use ARIA live regions where appropriate.
- Do not expose original sensitive values to assistive-tech-only text if they are visually hidden for privacy. Hidden PII is still PII.
