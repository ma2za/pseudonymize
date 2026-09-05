import { test, expect } from '@playwright/test';

test.describe('Password Recovery Subsystem', () => {

  test('Forgot Password view renders correctly and respects i18n', async ({ page }) => {
    await page.goto('/en/forgot-password');

    // Title and description
    await expect(page.getByRole('heading', { name: /Reset your password/i })).toBeVisible();
    await expect(page.getByText(/Enter your email address and we will send you a link/i)).toBeVisible();

    // Form elements
    await expect(page.locator('input[type="email"]#email-input')).toBeVisible();
    await expect(page.getByRole('button', { name: /Send reset link/i })).toBeVisible();

    // Backlink
    const loginLink = page.getByRole('link', { name: /Back to login/i });
    await expect(loginLink).toBeVisible();
    await expect(loginLink).toHaveAttribute('href', '/en/login');
  });

  test('Reset Password view renders correctly', async ({ page }) => {
    // Navigating directly without a token to ensure the UI renders (Better Auth will fail the API call later)
    await page.goto('/en/reset-password');

    // Title
    await expect(page.getByRole('heading', { name: /Set new password/i })).toBeVisible();

    // Form elements
    await expect(page.locator('input[type="password"]#password-input')).toBeVisible();
    await expect(page.getByRole('button', { name: /Reset password/i })).toBeVisible();
  });
});
