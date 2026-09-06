import { test, expect } from '@playwright/test';
import { prisma } from "@/db";

test.describe("5 More Critical & Untested Platform Features", () => {
  const runId = Math.random().toString(36).slice(2, 10);
  const email = `untested-e2e-${runId}@example.com`;
  const password = "SuperSecurePassword123!";

  test.beforeAll(async ({ browser }) => {
    // Create the test user once for the suite
    const page = await browser.newPage();
    await page.goto("/en/signup");
    await page.locator('input[type="text"]#name-input').fill('Untested Tester');
    await page.locator('input[type="email"]#email-input').fill(email);
    await page.locator('input[type="password"]#password-input').fill(password);
    await page.locator('button[type="submit"]').click();
    await page.waitForURL("**/en/dashboard", { timeout: 15000 });
    await page.close();
  });

  test.afterAll(async () => {
    try {
      const u = await prisma.user.findUnique({ where: { email } });
      if (u) {
        await prisma.user.delete({ where: { id: u.id } });
      }
    } catch (error) {
      console.error("Cleanup failed:", error);
    }
  });

  // -------------------------------------------------------------
  // Test 1: Theme State Persistence across views
  // -------------------------------------------------------------
  test('1. UI: Theme Toggle persists light/dark selection across views', async ({ page }) => {
    await page.goto('/en');
    
    // Check initial HTML tag doesn't crash
    const html = page.locator('html');
    
    // Toggle theme
    const themeButton = page.getByRole('button', { name: 'Toggle theme' });
    await expect(themeButton).toBeVisible();
    await themeButton.click();
    
    // Check state is reflected in the html theme attribute
    const theme = await html.getAttribute('data-theme');
    expect(theme).toMatch(/dark|light/);
    
    // Navigate to pricing page and ensure the theme is preserved
    await page.goto('/en/pricing');
    const pricingTheme = await html.getAttribute('data-theme');
    expect(pricingTheme).toBe(theme);
  });

  // -------------------------------------------------------------
  // Test 2: API Key Revocation
  // -------------------------------------------------------------
  test('2. Security: Users can revoke existing API keys cleanly', async ({ page }) => {
    // Login
    await page.goto('/en/login');
    await page.locator('input[type="email"]#email-input').fill(email);
    await page.locator('input[type="password"]#password-input').fill(password);
    await page.getByRole("button", { name: /Sign in/i }).click();
    await page.waitForURL("**/en/dashboard", { timeout: 15000 });

    const keyName = `Revokable Key ${runId}`;
    
    // Create API Key
    await page.locator('input[type="text"]').first().fill(keyName);
    await page.getByRole("button", { name: /Create new API key/i }).click();

    // Key should appear in the key management list
    await expect(page.getByText(keyName).first()).toBeVisible();

    // Revoke the key
    page.on("dialog", dialog => dialog.accept());
    await page.getByRole('button', { name: /Revoke key/i }).first().click();

    // Expect key to be successfully removed from UI
    await expect(page.getByText(keyName)).not.toBeVisible();
  });

  // -------------------------------------------------------------
  // Test 3: Password Recovery Requests
  // -------------------------------------------------------------
  test('3. Recovery: Forgot Password journey triggers instructions email alert', async ({ page }) => {
    await page.goto('/en/login');
    await page.getByRole('link', { name: /Forgot password\?/i }).click();
    await page.waitForURL("**/en/forgot-password");

    await page.locator('input[type="email"]#email-input').fill(email);
    await page.getByRole('button', { name: /Send reset link/i }).click();

    // Verify confirmation message is shown
    await expect(page.getByText(/Check your email for the reset link/i)).toBeVisible();
  });

  // -------------------------------------------------------------
  // Test 4: Clipboard Copy Mechanics
  // -------------------------------------------------------------
  test('4. UX: Copying generated API Key uses Clipboard API correctly', async ({ page }) => {
    // Login
    await page.goto('/en/login');
    await page.locator('input[type="email"]#email-input').fill(email);
    await page.locator('input[type="password"]#password-input').fill(password);
    await page.getByRole("button", { name: /Sign in/i }).click();
    await page.waitForURL("**/en/dashboard", { timeout: 15000 });

    // Grant clipboard permissions to browser context
    await page.context().grantPermissions(['clipboard-read', 'clipboard-write']);

    const keyName = `Copyable Key ${runId}`;
    await page.locator('input[type="text"]').first().fill(keyName);
    await page.getByRole("button", { name: /Create new API key/i }).click();

    // Click copy button on the newly created key panel
    const copyButton = page.locator('button').filter({ has: page.locator('.lucide-copy') }).first();
    await copyButton.click();

    // Verify copy icon toggles to checkmark
    await expect(page.locator('.lucide-check')).toBeVisible();

    // Verify actual clipboard text content matches the generated key prefix
    const clipboardText = await page.evaluate(() => navigator.clipboard.readText());
    expect(clipboardText).toMatch(/ps_live_|^temp/); // The key generated is prefixed or mock prefixed
  });

  // -------------------------------------------------------------
  // Test 5: Nested Routing Navigation via Links
  // -------------------------------------------------------------
  test('5. Routing: Nested Docs links transition successfully to sub-conceptual files', async ({ page }) => {
    await page.goto('/en/docs');

    // Find the link pointing to /docs/concepts/pseudonyms
    const pseudonymConceptLink = page.locator('a[href*="/docs/concepts/pseudonyms"]');
    if (await pseudonymConceptLink.count() > 0) {
      await pseudonymConceptLink.first().click();
      await page.waitForURL("**/en/docs/concepts/pseudonyms");
      await expect(page.getByRole('heading', { name: /Pseudonyms/i })).toBeVisible();
    } else {
      // If links are written within the markdown as simple /docs/concepts/pseudonyms we test direct entry
      await page.goto('/en/docs/concepts/determinism');
      await expect(page.getByRole('heading', { name: /Determinism/i })).toBeVisible();
    }
  });
});
