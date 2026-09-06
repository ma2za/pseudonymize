import { test, expect } from '@playwright/test';

test.describe('Landing Page', () => {
  test('should render properly and have correct title in English', async ({ page }) => {
    await page.goto('/en');
    await expect(page).toHaveTitle(/Send useful data to AI/i);
    await expect(page.getByRole('heading', { name: /Send useful data to AI/i, exact: false })).toBeVisible();
    await expect(page.getByRole('link', { name: /Pseudonymize data/i }).first()).toBeVisible();
  });

  test('should fallback or render correctly in another locale (e.g. /es)', async ({ page }) => {
    await page.goto('/es');
    await expect(page).toHaveTitle(/datos útiles a la IA/i);
    await expect(page.getByRole('heading', { name: /datos útiles a la IA/i, exact: false })).toBeVisible();
  });

  test('should redirect root to default locale (/en)', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveURL(/\/en/);
  });
});

test.describe('Login Page (Adversarial)', () => {
  test('should display validation error on malformed email', async ({ page }) => {
    await page.goto('/en/login');
    const emailInput = page.locator('input[type="email"]#email-input');
    await emailInput.fill('not-an-email');
    await page.getByRole('button', { name: 'Sign in' }).click();

    // HTML5 validation check
    const isInvalid = await emailInput.evaluate((el: HTMLInputElement) => !el.validity.valid);
    expect(isInvalid).toBe(true);
  });
});