# Handover Status: pseudonymize.io

**Date:** September 12, 2026
**Current Branch:** `main`

## Current State of the Project
The application is a Next.js (App Router) monolith providing API pseudonymization services with a unified dashboard and billing portal.

### Recently Completed (This Session)
1. **Layout & Transparency Fixes:**
   - Stripped broken dark mode overrides (`--pz-ink`) and hardcoded backdrop-blurs in `globals.css` that were rendering the mobile menu and header transparent. The navbar is now solidly opaque.
2. **Strict Validation Suite Enforcement:**
   - Addressed 102 ESLint errors across the codebase.
   - Refactored and stabilized the Playwright E2E suite (`npx playwright test`). Extended test timeouts to 60s for massive sequential journeys (`core-journeys.spec.ts`).
   - Re-wrote strict locator queries in Playwright to properly handle responsive DOM (targeting `.last()` for mobile "Sign In" vs. desktop).
   - Injected `dotenv` into `playwright.config.ts` to ensure it reads `.env.local` for the `DATABASE_URL` correctly in isolated testing environments.
3. **Release 1.6 - Usage Analytics:**
   - **Database:** Added the `ApiUsage` model to `prisma/schema.prisma` and applied the migration via `npx prisma db push`.
   - **Backend:** Implemented `src/app/actions/usage.ts` to aggregate the last 30 days of API usage into a Recharts-compatible format.
   - **Frontend:** Implemented `src/components/UsageChart.tsx` (using `recharts` with SSR hydration safeguards) and wired it into `src/app/[locale]/dashboard/page.tsx`.
   - **Testing:** Provided a hidden route at `POST /api/v1/mock-usage` to easily seed synthetic chart data.

## Next Steps / Roadmap
The next immediate priorities from the `ROADMAP.md` are:

- **Release 1.7: Subscription & Auto-Reload**
  - Integrate Stripe Billing Portal directly into the credit logic.
  - Options for automated credit auto-reloads when balances dip below a set threshold.
- **Release 1.8: Organization & Team Support**
  - Schema updates for cross-user Organizations.
  - Shared API keys and credit pools across invited team members.

## Notes for the Next Agent / Developer
- **Port Conflicts:** If `localhost:3000` is bound, use `$env:BASE_URL="http://localhost:3001"; npx playwright test` to execute E2E tests against an alternative port.
- **Validation Mandate:** The user mandates a strict "Zero Breakage" policy. Never commit or push without running `npm run lint` and `npx playwright test`. If a PR breaks, you must backtrack.
- **Database:** Prisma is using standard PostgreSQL. When migrating or testing, ensure Docker is running `docker run -d --name pseudonymize_db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=pseudonymize -p 5432:5432 postgres:15-alpine` if no DB is available.
- **UI Constraints:** Standardized components are driven by `src/brand/tokens.css` (do not hardcode hex values or Tailwind colors unless they map to a `--pz-*` token). Under any viewport, scrolling on static panels should be avoided.

---
*Ready for handover. The workspace is clean and committed.*