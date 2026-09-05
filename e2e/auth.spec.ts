import { test, expect } from '@playwright/test';

test.describe('Authentication & Protected Routes', () => {

  test('should redirect unauthenticated users from dashboard to login', async ({ page }) => {
    // Attempt to access dashboard directly
    await page.goto('/en/dashboard');
    
    // Should be redirected to login page
    await expect(page).toHaveURL(/.*\/login/);
    
    // Verify login page elements are visible
    await expect(page.locator('h2')).toContainText(/Sign in to your account/i);
  });

  test('login page should have all required interactive elements', async ({ page }) => {
    await page.goto('/en/login');

    // Email input
    const emailInput = page.locator('input[type="email"]');
    await expect(emailInput).toBeVisible();
    await expect(emailInput).toHaveAttribute('required', '');

    // Password input
    const passwordInput = page.locator('input[type="password"]');
    await expect(passwordInput).toBeVisible();
    await expect(passwordInput).toHaveAttribute('required', '');

    // Submit button (should be disabled initially or enabled depending on Turnstile mock, 
    // but we can check if it exists)
    const submitBtn = page.getByRole('button', { name: /Sign in/i });
    await expect(submitBtn).toBeVisible();

    // Google Login button
    const googleBtn = page.getByRole('button', { name: /Google/i });
    await expect(googleBtn).toBeVisible();
  });

  test('login form should enforce email HTML5 validation', async ({ page }) => {
    await page.goto('/en/login');
    const emailInput = page.locator('input[type="email"]');
    const submitBtn = page.getByRole('button', { name: /Sign in/i });

    await emailInput.fill('invalid-email-format');
    
    // Turnstile might block the click if we use disabled={!token}, but let's check the DOM validity state
    const isInvalid = await emailInput.evaluate((el: HTMLInputElement) => !el.checkValidity());
    expect(isInvalid).toBe(true);
  });
});
