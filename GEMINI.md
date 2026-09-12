# Project Instructions: pseudonymize.io

## Testing & Quality Assurance
- **Playwright E2E Mandate (STRICT):** Every single feature, view, and action MUST have an accompanying E2E Playwright test. No feature is merged without it. Tests must be adversarial (testing edge cases, malformed inputs, language switching).

## UI, UX & Styling
- **No Hardcoded Text (STRICT):** All user-facing text MUST be routed through `next-intl`. You are strictly forbidden from hardcoding readable text strings in React components. Everything must pull from `messages/[locale].json`.
- **Responsive & Zero-Scroll:** Must be 100% responsive across all screen sizes. Under any desktop viewport, strictly adhere to the global zero-scroll mandate for static card structures (login, signup, auth panels, dashboard widgets). Spacing must scale compactly.

## Infrastructure & Integrations
- **Email:** Use **Resend** for all outgoing emails (verification, password resets, notifications). This must be hooked into Better Auth.
- **Backend:** PostgreSQL + Drizzle ORM.
- **Auth:** Better Auth.
## Deployment (STRICT)
- **NO MANUAL TERMINAL COMMANDS IN PRODUCTION:** All database migrations (`drizzle-kit push` or `prisma db push`) must execute automatically during the build/deployment pipeline (e.g., via Docker `CMD` or Coolify Post-deployment hooks).
- **Strict Multi-Project Isolation:** When deploying or running locally, never interfere with other active projects, containers, or dev servers in the same workspace. If there are port conflicts (e.g., port 3000 or 5432 is occupied), select an alternative dynamic port (such as 3001, 3002 or 5434) and adjust the `.env` settings accordingly. Never shut down, stop, or delete sibling repositories' Docker containers or processes.
## Bot & LLM Automation (STRICT)
- **Frictionless Access:** The application MUST be entirely accessible to automated browsers, bots, and LLMs. Do NOT implement CAPTCHAs (e.g., Turnstile, reCAPTCHA) or arbitrary rate limits that prevent automated agent registration or credit purchasing.

## Discoverability (Global SEO & LLM Platforms)
- **Metadata (STRICT):** Every page MUST output complete `generateMetadata` including `title`, `description`, `openGraph`, `twitter`, and explicit `alternates` with `hreflang` tags for ALL 20 languages. Never output a page without proper canonicals.
- **Sitemaps & Robots:** A dynamic `sitemap.xml` detailing every supported locale path and a `robots.txt` must be maintained at the root.
- **LLM Context:** Structural semantic HTML (e.g., `<main>`, `<article>`, `<nav>`, `<h1>`-`<h6>`) must be pristine to guarantee LLM parsers (like Gemini/Claude crawlers) can accurately scrape the service purpose and API docs.
