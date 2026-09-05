import { test, expect } from '@playwright/test';

test.describe('Mocked Authentication Journeys', () => {

  test('successful login redirects to dashboard (Mocked Network)', async ({ page }) => {
    // Intercept the Next.js / Better Auth fetch request
    await page.route('**/api/auth/sign-in/email', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          user: { id: 'mock-123', email: 'test@example.com' },
          session: { id: 'sess-123' }
        })
      });
    });

    await page.goto('/en/login');

    await page.locator('input[type="email"]#email-input').fill('test@example.com');
    await page.locator('input[type="password"]#password-input').fill('SuperSecret123!');
    
    // Submit the form
    await page.getByRole('button', { name: /Sign in/i }).click();

    // Verify it pushed the router to dashboard
    await page.waitForURL('**/dashboard');
    await expect(page).toHaveURL(/.*\/dashboard/);
  });

  test('successful signup redirects to dashboard (Mocked Network)', async ({ page }) => {
    await page.route('**/api/auth/sign-up/email', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          user: { id: 'mock-456', email: 'new@example.com' },
          session: { id: 'sess-456' }
        })
      });
    });

    await page.goto('/en/signup');

    await page.locator('input[type="text"]#name-input').fill('Test User');
    await page.locator('input[type="email"]#email-input').fill('new@example.com');
    await page.locator('input[type="password"]#password-input').fill('SuperSecret123!');
    
    // Submit the form
    await page.getByRole('button', { name: /Sign up/i }).click();

    // Verify it pushed the router to dashboard
    await page.waitForURL('**/dashboard');
    await expect(page).toHaveURL(/.*\/dashboard/);
  });

  test('successful forgot password shows success message (Mocked Network)', async ({ page }) => {
    await page.route('**/api/auth/forget-password', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ status: true })
      });
    });

    await page.goto('/en/forgot-password');

    await page.locator('input[type="email"]#email-input').fill('test@example.com');
    await page.getByRole('button', { name: /Send reset link/i }).click();

    // Verify the success state renders locally without navigating
    await expect(page.getByText(/Check your email for the reset link!/i)).toBeVisible();
  });
});
