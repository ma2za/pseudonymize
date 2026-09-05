import { test, expect } from '@playwright/test';

test.describe('Landing Page', () => {
  test('should render properly and have correct title in English', async ({ page }) => {
    await page.goto('/en');
    await expect(page).toHaveTitle(/pseudonymize.io/);
    await expect(page.getByRole('heading', { name: 'pseudonymize.io' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Get Started' })).toBeVisible();
  });

  test('should fallback or render correctly in another locale (e.g. /es)', async ({ page }) => {
    await page.goto('/es');
    await expect(page).toHaveTitle(/pseudonymize.io/);
    await expect(page.getByRole('heading', { name: 'pseudonymize.io' })).toBeVisible();
  });

  test('should redirect root to default locale (/en)', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveURL(/\/en/);
  });
});

test.describe('Login Page (Adversarial)', () => {
  test('should display validation error on malformed email', async ({ page }) => {
    await page.goto('/en/login');
    const emailInput = page.getByLabel('Email address');
    await emailInput.fill('not-an-email');
    await page.getByRole('button', { name: 'Sign in' }).click();
    
    // HTML5 validation kicks in (Playwright captures this via the input matching the pseudo-class or directly evaluating)
    const isInvalid = await emailInput.evaluate((el: HTMLInputElement) => !el.checkValidity());
    expect(isInvalid).toBe(true);
  });
});