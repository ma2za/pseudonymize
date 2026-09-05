---
title: "Privacy Policy"
lastUpdated: "2026-09-05"
---

# Privacy Policy

**Effective Date:** September 5, 2026

At pseudonymize.io, we are committed to providing a secure, minimal, and transparent service. We believe in strict data minimization.

## 1. What Data We Collect
We collect the minimum amount of data required to operate our service:
*   **Account Information:** Your name and email address provided during registration (via Google SSO or direct email signup).
*   **Payment Information:** Handled securely by Stripe. We only store a reference to your customer ID and your purchased credit balance.
*   **API Usage:** We track the volume of API requests to decrement your credit balance. 

## 2. What Data We DO NOT Collect
*   **API Payloads:** We **do not log, store, or persist** the data payloads you transmit to our API for pseudonymization. The process happens entirely in memory, and the original data is discarded immediately after the HTTP response is sent.

## 3. Third-Party Integrations
We use the following secure third parties to run our infrastructure:
*   **Hetzner/Coolify:** For self-hosted, sovereign European server infrastructure.
*   **Stripe:** For billing and subscription processing.
*   **Resend:** For transactional emails (password resets and verification).
*   **Google:** For optional Single Sign-On (SSO).

## 4. Your Rights
Under GDPR and CCPA, you have the right to request the deletion of your account and all associated data. You will find a 1-click account deletion tool inside your dashboard settings (coming in Release 1.4).

If you have any questions, please check our open-source repository on GitHub.
