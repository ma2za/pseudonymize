import { test, expect } from "@playwright/test";
import { prisma } from "@/db";
import { randomUUID } from "crypto";

test.describe("Proper E2E Flow: Auth, API Keys, Settings (No Mocks)", () => {
  test.setTimeout(60000); // Increase timeout for this long journey
  
  const runId = Math.random().toString(36).slice(2, 10);
  const email = `proper-e2e-${runId}@example.com`;
  const password = "SuperSecurePassword123!";
  const name = "E2E User";

  test.afterAll(async () => {
    // Clean up test user from the live database
    try {
      const u = await prisma.user.findUnique({ where: { email } });
      if (u) {
        // Cascade deletion via Prisma
        await prisma.user.delete({ where: { id: u.id } });
      }
    } catch (error) {
      console.error("Database Cleanup failed:", error);
    }
  });

  test("should complete the 5 core platform journeys sequentially", async ({ page }) => {
    // -------------------------------------------------------------
    // 1. Registration Journey
    // -------------------------------------------------------------
    console.log("Navigating to sign-up...");
    await page.goto("/en/signup");

    console.log("Filling sign-up fields...");
    await page.locator('input[type="text"]#name-input').fill(name);
    await page.locator('input[type="email"]#email-input').fill(email);
    await page.locator('input[type="password"]#password-input').fill(password);
    
    console.log("Submitting sign-up form...");
    await page.locator('button[type="submit"]').click();

    console.log("Waiting for redirection to dashboard...");
    await page.waitForURL("**/en/dashboard", { timeout: 15000 });
    await expect(page).toHaveURL(/.*\/dashboard/);

    // Verify Dashboard UI loaded
    await expect(page.getByRole("heading", { name: /API Keys/i })).toBeVisible();

    // -------------------------------------------------------------
    // 2. API Key Journey
    // -------------------------------------------------------------
    console.log("Creating new API key...");
    const keyName = `E2E Key ${runId}`;
    
    // Fill the key name using a specific placeholder locator
    const keyInput = page.getByPlaceholder(/Name your API key/i);
    await keyInput.fill(keyName);
    await expect(keyInput).toHaveValue(keyName);
    await page.waitForTimeout(500);
    
    // Click create
    await page.getByRole("button", { name: /Create new API key/i }).click();

    // Verify key was generated
    await expect(page.getByText(/Please copy your API key now/i)).toBeVisible();
    await expect(page.getByText(/ps_live_/).first()).toBeVisible();

    // -------------------------------------------------------------
    // 3. Settings Journey
    // -------------------------------------------------------------
    console.log("Navigating to settings...");
    await page.goto("/en/dashboard/settings");

    console.log("Updating profile name...");
    const updatedName = "E2E User Updated";
    await page.locator('input[type="text"]#name').fill(updatedName);
    await page.getByRole("button", { name: /Save changes/i }).click();

    await expect(page.getByText(/Profile updated successfully/i)).toBeVisible();

    // -------------------------------------------------------------
    // 4. Session Logout & Login Journey
    // -------------------------------------------------------------
    console.log("Navigating back to dashboard and logging out...");
    await page.goto("/en/dashboard");
    await page.getByRole("button", { name: /Sign out/i }).click();
    
    // Better auth client redirect
    await page.waitForTimeout(1000);

    console.log("Navigating to login page...");
    await page.goto("/en/login");
    
    console.log("Filling login fields...");
    await page.locator('input[type="email"]#email-input').fill(email);
    await page.locator('input[type="password"]#password-input').fill(password);
    
    console.log("Submitting login form...");
    await page.getByRole("button", { name: /Sign in/i }).click();

    console.log("Waiting for redirection back to dashboard...");
    await page.waitForURL("**/en/dashboard", { timeout: 15000 });
    await expect(page).toHaveURL(/.*\/dashboard/);

    // -------------------------------------------------------------
    // 5. Account Deletion Journey
    // -------------------------------------------------------------
    console.log("Navigating to settings for account deletion...");
    await page.goto("/en/dashboard/settings");

    // Automatically accept the browser confirmation dialog
    page.on("dialog", dialog => dialog.accept());

    console.log("Clicking delete account...");
    await page.getByRole("button", { name: /Delete Account/i }).click();

    console.log("Waiting for redirection to homepage after deletion...");
    await page.waitForURL("**/en", { timeout: 15000 });
    await expect(page).toHaveURL(/.*\/en/);

    console.log("Verifying account is deleted by attempting to login again...");
    await page.context().clearCookies();
    await page.goto("/en/login");
    await page.locator('input[type="email"]#email-input').fill(email);
    await page.locator('input[type="password"]#password-input').fill(password);
    await page.getByRole("button", { name: /Sign in/i }).click();

    // Better Auth fails silently on UI by default, but URL should not change to dashboard
    await page.waitForTimeout(2000);
    await expect(page).toHaveURL(/.*\/login/);

    console.log("E2E Test Complete and Successful!");
  });
});