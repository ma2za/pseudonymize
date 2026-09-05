# Roadmap: pseudonymize.io (v1.1 to v2.0)

With v1.0 successfully launched, this roadmap outlines the next 10 releases aimed at improving user acquisition, account management, and platform maturity.

### Release 1.1: Global Layouts & Navigation
- **Goal:** Unify the brand experience across all public pages.
- **Features:**
  - Implement a global, responsive Header (Logo, Blog, Auth links).
  - Implement a minimal Footer (Copyright, social links, legal placeholders).

### Release 1.2: User Registration Flow
- **Goal:** Allow frictionless onboarding.
- **Features:**
  - Dedicated `/signup` page.
  - Native Email/Password registration bridging with Better Auth.
  - Seamless redirect to the dashboard upon successful registration.

### Release 1.3: Password Recovery 
- **Goal:** Prevent user lockouts.
- **Features:**
  - `/forgot-password` flow to trigger Resend recovery emails.
  - `/reset-password` page to securely set a new password via token.

### Release 1.4: Profile Settings & Account Deletion
- **Goal:** Give users control over their data (GDPR compliance).
- **Features:**
  - Add a "Settings" tab in the dashboard.
  - Allow users to update their name/email.
  - 1-click account deletion and data wipe.

### Release 1.5: Interactive API Documentation
- **Goal:** Developer enablement.
- **Features:**
  - Add a `/docs` sub-route powered by our Markdown CMS.
  - Code snippets in Python, Node.js, and Go.
  - Live interactive payload playground.

### Release 1.6: Usage Analytics Dashboard
- **Goal:** Transparency in billing.
- **Features:**
  - Track API usage in the backend (using a Redis or fast Postgres table).
  - Display a usage graph/chart on the user dashboard.

### Release 1.7: Subscription & Auto-Reload
- **Goal:** Advanced monetization.
- **Features:**
  - Integrate Stripe Billing Portal.
  - Option to auto-reload credits when balance falls below a threshold.

### Release 1.8: Organization & Team Support
- **Goal:** B2B capabilities.
- **Features:**
  - Allow users to create "Organizations".
  - Invite team members via email.
  - Shared credit pools and API keys.

### Release 1.9: Multi-Region API Routing
- **Goal:** Latency optimization for enterprise.
- **Features:**
  - Allow users to select API processing regions (EU vs US) for strict compliance.

### Release 2.0: Platform Marketplace
- **Goal:** Extend pseudonymization logic.
- **Features:**
  - Custom data masking rules (e.g., regex patterns, specific NLP models).
  - Open the platform for community-contributed masking strategies.
