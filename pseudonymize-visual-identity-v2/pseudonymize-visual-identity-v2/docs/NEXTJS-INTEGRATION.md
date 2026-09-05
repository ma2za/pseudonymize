# Next.js integration

## 1. Assets
Copy the contents of `favicons/` and desired `logo/` files into `public/`. Do not copy font files from this package; none are bundled.

## 2. Tokens
Import `tokens/tokens.css` in `app/globals.css` or translate `tokens/design-tokens.json` into your existing design system. A Tailwind-ready object is included as `tokens/tailwind-theme.ts`.

## 3. Fonts
Use `next/font/google` for Inter and IBM Plex Mono if your deployment policy permits fetching them at build time, or self-host them under your own licensing/deployment setup.

```tsx
import { Inter, IBM_Plex_Mono } from 'next/font/google'

export const inter = Inter({ subsets: ['latin'], variable: '--font-sans' })
export const plexMono = IBM_Plex_Mono({ weight: ['400','500','600'], subsets: ['latin'], variable: '--font-mono' })
```

## 4. Metadata

```tsx
export const metadata = {
  title: 'pseudonymize.io — Keep the structure. Lose the identity.',
  description: 'Pseudonymize sensitive data, text and files without destroying their usefulness.',
  icons: { icon: '/favicon.ico', apple: '/apple-touch-icon.png' },
  openGraph: { images: ['/og-default.png'] },
}
```

## 5. Accessibility
Preserve the visible focus ring, reduced-motion media query, textual status labels, and linear mobile order of before/after content.

## 6. Trust section
Do not ship the placeholder security facts from the prototype. Replace them with verified processing, retention, cryptography and assurance details before publishing.
