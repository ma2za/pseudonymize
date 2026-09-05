# Roadmap: pseudonymize.io to v1.0

This document outlines the 10-release strategy to take **pseudonymize.io** from initialization to a production-ready v1.0.

### Release 0.1: Foundation & Scaffolding
- **Goal:** Set up the Next.js project with App Router, TypeScript, and Tailwind CSS.
- **Features:** 
  - Monorepo/project structure initialization.
  - Setup internationalization (i18n) framework for 20 languages.
  - Setup basic theme (minimalist design system).

### Release 0.2: Better Auth Integration
- **Goal:** Implement secure user authentication.
- **Features:**
  - Setup Better Auth.
  - Google SSO integration.
  - Email/Password authentication.
  - Protected routes scaffolding.

### Release 0.3: Database & Core Models
- **Goal:** Establish the data layer for users, credits, and API keys.
- **Features:**
  - Setup ORM (e.g., Drizzle or Prisma) and PostgreSQL.
  - Models for User, API Key, and Credit Balance.
  - Initial database migrations.

### Release 0.4: Landing Page & Multi-language Structure
- **Goal:** Build the public face of the service.
- **Features:**
  - High-converting, minimal landing page.
  - Translation files stubbed for all 20 target languages.
  - Language switcher component.

### Release 0.5: Dashboard & API Key Management
- **Goal:** Allow users to manage their integration.
- **Features:**
  - Secure developer dashboard.
  - Generate, revoke, and view API keys.
  - Display current credit balance.

### Release 0.6: Monetization (Stripe Credits System)
- **Goal:** Implement the business model.
- **Features:**
  - Stripe integration (webhooks, checkout sessions).
  - Purchase flows for credit packages.
  - Update user credit balance upon successful payment.

### Release 0.7: Headless CMS Integration
- **Goal:** Lay the groundwork for content marketing.
- **Features:**
  - Connect a Headless CMS (e.g., Sanity, Strapi, or robust markdown parsing).
  - Define schema for Blog Posts (Title, Content, Meta, Slug).
  - Support content variations for the 20 languages.

### Release 0.8: Multilingual Blog & Global SEO
- **Goal:** Maximize discoverability across regions.
- **Features:**
  - Build the `/blog` frontend to fetch and render CMS content.
  - Implement hreflang tags, dynamic sitemaps, and canonical URLs.
  - Geo-optimization logic for regional rendering.

### Release 0.9: Infrastructure & CI/CD Pipeline
- **Goal:** Automate deployments to Hetzner via Coolify.
- **Features:**
  - Dockerize the Next.js application.
  - Configure Coolify deployment webhooks.
  - GitHub Actions for linting, type-checking, and auto-deploy.

### Release 1.0: Polish, Analytics & Production Launch
- **Goal:** The official launch.
- **Features:**
  - End-to-end testing of auth, billing, and localization flows.
  - Integration of privacy-friendly analytics.
  - Final UX review, ensuring the "simple, minimal, straight to the point" ethos.
  - Go live!
