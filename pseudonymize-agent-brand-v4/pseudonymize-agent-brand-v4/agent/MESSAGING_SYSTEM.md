# pseudonymize.io — messaging system

This file is the canonical messaging contract for marketing, product UI, docs, and transactional copy.

## 1. Category

**Pseudonymization infrastructure**

Do not reposition pseudonymize.io as generic cybersecurity, anonymization software, DLP, a compliance consultancy, or an "AI privacy" product unless the repository clearly establishes those capabilities.

## 2. Core promise

**Keep the context. Replace the identifiers.**

Supporting idea:

> Pseudonymize sensitive identifiers before data reaches systems that do not need the originals, while preserving the surrounding context and structure the workflow still needs.

The product value is not "make data safe." That is too broad. The value is **reduce unnecessary exposure of original identifiers without destroying useful context**.

## 3. Messaging hierarchy

Use this hierarchy consistently.

### Level 1 — category + outcome
Explain what the product does in plain language.

Preferred:
- `Pseudonymize sensitive data before it reaches systems that do not need the original identifiers.`
- `Keep sensitive identifiers out of downstream systems without stripping away useful context.`

Avoid:
- `Protect your data with next-generation privacy.`
- `Enterprise-grade AI security.`
- `Make your data completely safe.`

### Level 2 — mechanism
Explain how the operation works.

Preferred concepts:
- detect identifiers
- replace identifiers with pseudonyms
- preserve surrounding text / rows / files
- maintain consistent mappings when the product actually supports consistency
- review uncertain detections when the product actually exposes review

Do not claim reversible, deterministic, format-preserving, local, or stateless behavior unless verified in code/product configuration.

### Level 3 — workflow fit
Explain why a team uses it.

Preferred:
- before analytics
- before testing
- before sharing
- before sending data into downstream tools or models
- before giving data to systems that do not require direct identifiers

Only mention a workflow when the product actually supports the input/output path involved.

### Level 4 — trust
Trust messaging must be factual and inspectable.

Every security or privacy claim needs evidence. If evidence is absent, omit the claim rather than replacing it with vague reassurance.

## 4. Primary audience language

Default audience: developers, data teams, and technical operators moving sensitive information through software workflows.

Write for an informed technical buyer without sounding like documentation on the homepage.

Use:
- `API`
- `structured data`
- `identifiers`
- `processing`
- `mapping`
- `workflow`

Avoid unexplained regulatory or cryptographic jargon in primary marketing copy.

## 5. Canonical vocabulary

### Prefer
- pseudonymize
- pseudonymized
- pseudonym
- original identifier
- sensitive identifier
- detected identifier
- replacement
- mapping
- processing
- review required
- source
- result
- input
- output

### Conditional terminology
Use only when technically true in the repository:
- consistent pseudonym
- stable mapping
- reversible mapping
- deterministic mapping
- format preserving
- encrypted mapping
- local processing
- zero retention
- EU processing
- self-hosted
- model / AI detection

### Avoid by default
- anonymized
- anonymous
- de-identified as a legal/compliance conclusion
- sanitized
- safe data
- secure data
- privacy magic
- military-grade
- bulletproof
- zero-risk
- unhackable
- compliant with X as a blanket promise

## 6. Voice

Calm. Exact. Short. Technical when useful. Never theatrical.

A good pseudonymize.io sentence normally contains a concrete noun and a concrete verb.

Good:
`Replace detected email addresses with pseudonyms before the text leaves your workflow.`

Bad:
`Unlock a new era of trusted privacy-first innovation.`

## 7. Sentence rules

- Prefer active voice.
- Prefer one idea per sentence.
- Headings should usually be 3–10 words.
- Leads should usually be 18–34 words.
- Buttons should normally be 1–4 words.
- Do not repeat `secure`, `privacy`, or `sensitive` in every section.
- Do not make fear the primary conversion mechanism.
- Do not attack competitors.
- Do not describe pseudonymization as deletion.

## 8. CTA system

Primary marketing CTA:
`Pseudonymize data`

Primary developer CTA:
`Read the docs`

Secondary marketing CTA:
`View documentation`

Authentication CTA:
`Sign in`

Do not use vague CTAs such as:
- Get started
- Learn more
- Discover
- Explore

unless the destination cannot be stated more precisely.

## 9. Status language

Use exactly where possible:
- `Not processed`
- `Processing`
- `Pseudonymized`
- `Review required`
- `Failed`

Never use `Secure` as a processing status.

## 10. Error language

Errors should explain:
1. what failed
2. whether user data was changed
3. the next action

Example:
`Processing failed. The source file was not changed. Try again or upload a different file.`

Do not write:
`Oops! Something went wrong.`

## 11. Empty-state language

Empty states should tell the user what can happen next. No mascots or motivational copy.

Example:
`Paste text or upload a supported file to identify and replace sensitive identifiers.`

## 12. Security-page language

The security page exists to expose facts, not produce feelings.

Preferred headings:
- `How data is processed`
- `Data retention`
- `Encryption`
- `Infrastructure`
- `Subprocessors`
- `Security reporting`

Only render headings for which the repository/company has an actual answer.

Do not create an empty section with a comforting paragraph when a fact is unknown.

## 13. Pricing language

Pricing copy should explain the charging unit in the first visible pricing section.

Examples depending on the actual product:
- `Pay for processed characters.`
- `Pay for processed records.`
- `Pay for processed files.`

Never invent the billing unit. If it cannot be discovered from the repository/config, preserve existing pricing copy and flag the missing fact in implementation notes.

## 14. Documentation language

Docs optimize for precision, not branding.

Documentation page titles should be task-oriented:
- `Pseudonymize text`
- `Upload a file`
- `Process structured data`
- `Authentication`
- `Errors`

Avoid marketing headings inside API/reference documentation.

## 15. Product UI microcopy

### Input
- `Source`
- `Paste text`
- `Upload file`
- `Choose file`
- `Process`

### Output
- `Result`
- `Pseudonymized`
- `Copy result`
- `Download result`

### Review
- `Review required`
- `Detected identifier`
- `Original identifier`
- `Pseudonym`

### History
- `Processing history`
- `No processed items yet`

### API keys
- `API keys`
- `Create API key`
- `Revoke`
- `Last used`

Do not expose an API-key page if the product does not have API authentication.

## 16. SEO / metadata

Default title:
`pseudonymize.io — Pseudonymization for text, data and files`

Default description:
`Replace sensitive identifiers with pseudonyms while preserving the context and structure your workflows still need.`

Do not mention unverified certifications or deployment properties in metadata.

## 17. One test for every sentence

Before shipping copy, ask:

**Does this sentence describe a real capability, a real outcome, or a real next action?**

If not, delete it.
