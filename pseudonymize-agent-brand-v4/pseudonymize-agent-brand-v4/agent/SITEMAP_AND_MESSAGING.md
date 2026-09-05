# pseudonymize.io — canonical pages and messaging

This is the page-level implementation contract. Use it together with `MESSAGING_SYSTEM.md` and the JSON route specs.

## Route policy

The kit defines a **recommended canonical information architecture**. Do not blindly create routes that conflict with the existing product.

When integrating into an existing repository:

1. Preserve existing working routes unless there is a strong reason to migrate them.
2. Map existing routes to the closest page specification below.
3. Create a missing marketing route only when its content can be populated truthfully.
4. Never create a Security, Pricing, SDK, or compliance page filled with invented facts.
5. Product/app routes may be renamed to match the repository conventions, but keep the screen purpose and messaging hierarchy.

---

# Public pages

## `/` — Homepage

### Job
Make a first-time visitor understand three things within the first viewport:
1. this is pseudonymization software
2. original identifiers are replaced while useful context remains
3. they can either try the product or inspect the docs

### Primary message
**H1:** `Pseudonymize sensitive data before it reaches systems that do not need the original identifiers.`

**Lead:** `Replace personal identifiers across text, structured data and files while preserving the surrounding context your workflow depends on.`

**Primary CTA:** `Pseudonymize data`

**Secondary CTA:** `View documentation`

### Hero proof
Show a real transformation, not an illustration.

Example:
`Contact alice@example.com about invoice 1842.`
→
`Contact EMAIL_01 about invoice 1842.`

The important visual fact is that `invoice 1842` and the sentence structure are unchanged.

### Section order
1. Hero
2. Supported input modes
3. Full before/after transformation proof
4. Workflow: Detect → Replace → Continue
5. Developer/API entry point, only from real repository capability
6. Verified trust facts, only if available
7. Final CTA

### Do not add
- testimonials without real testimonials
- customer logos without permission/source
- compliance badges without evidence
- fabricated usage numbers
- generic “Why us?” cards
- FAQ invented solely for SEO

---

## `/product` — Product overview

### Job
Explain the product beyond the hero. This page answers: what can I pseudonymize, what happens to it, and how does it fit into a workflow?

### H1
`One pseudonymization layer for text, structured data and files.`

### Lead
`Send supported content through one processing layer, replace detected identifiers with pseudonyms, and continue working with the surrounding context intact.`

### Sections
1. Input surfaces: Text / Structured data / Files
2. Transformation model
3. Review and processing states, if implemented
4. Mapping/consistency behavior, only if verified
5. Output and downstream workflow
6. Developer integration bridge
7. CTA

### Core message per input
**Text:** `Replace identifiers inside prose without flattening the text around them.`

**Structured data:** `Pseudonymize identifier fields while keeping rows and schemas usable.`

**Files:** `Process supported files without manually extracting their sensitive content first.`

Never promise format preservation for a file type unless verified.

---

## `/developers` — Developers / API landing

### Job
Convince a developer that pseudonymization can sit inside an existing data path without turning the page into API reference documentation.

### H1
`Put pseudonymization in the path of sensitive data.`

### Lead
`Use the API or supported integration surface to replace identifiers before content reaches downstream systems that do not require the originals.`

### Primary CTA
`Read the docs`

### Secondary CTA
Use `Pseudonymize data` or an existing API-key/signup action only if it actually exists.

### Sections
1. Minimal real request/response example
2. Authentication summary, if real
3. Supported content/input formats, sourced from code/docs
4. Error model / processing lifecycle
5. SDKs only if they exist
6. Link to reference docs

### Prohibition
Never fabricate endpoint paths, response payloads, SDK package names, rate limits, or latency claims.

---

## `/security` — Security & privacy

### Job
Let a technical buyer inspect concrete handling and security facts.

### H1
`Security claims should be inspectable.`

### Lead
`This page documents how pseudonymize.io handles data and infrastructure. Every claim shown here must be backed by an internal source or public policy.`

### Content blocks
Render only verified blocks from `security.ts` / repository sources. Preferred order:
1. Data processing
2. Retention
3. Encryption
4. Infrastructure / region
5. Access controls
6. Subprocessors
7. Security reporting/contact
8. Certifications / audits

If only two verified facts exist, show two facts. Do not pad the page.

### CTA
`View documentation` or a real `Contact` route if one exists.

---

## `/pricing` — Pricing

### Job
Explain what costs money with minimal ambiguity.

### H1
`Pricing that follows actual usage.`

Use this H1 only if the billing model is actually usage-based. Otherwise preserve or derive the real model and rewrite the H1 accordingly.

### Required content
The first pricing viewport must state:
- charging unit
- included allowance, if any
- base/subscription fee, if any
- what happens after the allowance
- whether VAT/tax is included when relevant to the business

### Plan copy
Plan names should be functional, not cute. Prefer `Free`, `Developer`, `Team`, `Enterprise` only if those plans really exist.

### CTA logic
- self-serve plan: exact signup/action label
- sales plan: `Contact sales` only if a sales path exists

Do not invent enterprise features.

---

## `/docs` — Documentation entry

If docs already use another route/domain, link there instead of duplicating.

### Job
Get a technical user to the first successful pseudonymization operation quickly.

### H1
`Documentation`

### Intro
`Integrate pseudonymization into your workflow, understand supported inputs, and handle processing results and errors.`

### First links
1. `Quickstart`
2. `Pseudonymize text`
3. `Process structured data`
4. `Upload a file`
5. `API reference`

Only show links that exist.

---

## `/about` — About, optional

Do not create solely to fill a footer.

### Job
Explain why the product exists and who is responsible for it.

### Suggested H1
`Sensitive data should not travel farther than it needs to.`

### Message
Focus on the product thesis, not startup mythology:
`Many workflows need the information around an identifier without needing the identifier itself. pseudonymize.io exists to make that separation practical.`

Use real team/company facts only.

---

# Authentication pages

## `/sign-in`

### H1
`Sign in`

### Supporting copy
Usually none. Authentication pages should be quiet.

Use provider-specific button text exactly, e.g. `Continue with Google`, only for configured providers.

Do not add fake trust copy beside the form.

## `/sign-up`

### H1
`Create your account`

### Lead
`Start pseudonymizing supported data and configure integrations available to your workspace.`

Remove the lead if the real onboarding differs.

---

# Application pages

## `/app` or `/app/new` — New processing workspace

### Job
Get input → process → inspect result with no ambiguity.

### Page title
`Pseudonymize`

### Tabs / modes
Use only implemented modes:
- `Text`
- `Data`
- `Files`

### Source panel
Title: `Source`

Text empty state:
`Paste text containing identifiers you want to replace.`

File empty state:
`Choose a supported file to process.`

### Action
`Pseudonymize`

Do not use `Secure data` or `Anonymize`.

### Result panel
Title: `Result`

Initial state:
`The pseudonymized result will appear here.`

Success status:
`Pseudonymized`

Review status:
`Review required`

### Result actions
Use only where real:
- `Copy result`
- `Download result`
- `View mappings`

---

## `/app/history` — Processing history

### H1
`Processing history`

### Empty state
`No processed items yet.`

### Table columns
Use only data actually stored. Preferred order:
- Name / input
- Type
- Status
- Processed at
- Action

Do not display original sensitive values in list views merely to make the UI informative.

---

## `/app/mappings` — Mappings, conditional

Create only if the product exposes stored/reusable mappings.

### H1
`Mappings`

### Lead
`Inspect the relationship between original identifiers and their pseudonyms.`

This page may itself contain sensitive data. Treat original values accordingly and follow actual authorization/storage behavior.

Never describe mappings as reversible unless the architecture actually supports reversal.

---

## `/app/api-keys` — API keys, conditional

### H1
`API keys`

### Lead
`Create and manage credentials used to access the pseudonymize.io API.`

### Primary CTA
`Create API key`

### Secret reveal copy
`Copy this key now. It may not be shown again.`

Use only if secret keys really have one-time visibility.

### Destructive action
`Revoke key`

---

## `/app/settings` — Settings

### H1
`Settings`

Prefer flat sections over cards.

Possible sections only if implemented:
- Workspace
- Members
- Processing defaults
- Billing
- Data handling
- API

Do not invent organization/team semantics.

---

# System pages

## 404
**H1:** `Page not found`

**Body:** `The page you requested does not exist or has moved.`

**CTA:** `Go to pseudonymize.io`

## Generic application error
**H1:** `Something failed`

**Body:** Prefer a specific error from the application. If unavailable: `The request could not be completed. Your source data was not changed by this screen.` only if that second sentence is true.

Do not make jokes in error states.

---

# Navigation contract

Marketing nav default:
- Product
- Developers
- Security
- Pricing
- Docs

Only render destinations that exist.

Right side:
- Sign in
- Pseudonymize data

Application nav should prioritize tasks rather than marketing:
- Pseudonymize
- History
- Mappings, conditional
- API keys, conditional
- Settings

---

# Cross-page messaging rules

1. Homepage says **what and why**.
2. Product says **what happens**.
3. Developers says **how it enters software**.
4. Security says **what is factually true about handling**.
5. Pricing says **what costs money**.
6. Docs says **how to perform the task**.
7. App copy says **current state and next action**.

Do not duplicate the homepage pitch verbatim across every page.
