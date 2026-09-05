import { test, expect, devices } from '@playwright/test';

test.use({
  ...devices['Pixel 5'],
});

test.describe('Mobile Viewport Responsiveness', () => {

  test('header collapses navigation and renders without scrollbars on mobile', async ({ page }) => {
    await page.goto('/en');
    
    // Logo should be visible
    await expect(page.getByRole('link', { name: /pseudonymize\.io/i })).toBeVisible();

    // The desktop "Sign Up" button and "Open Source" links should be hidden by Tailwind `hidden sm:block`
    const signUpBtn = page.getByRole('link', { name: /Sign Up/i });
    await expect(signUpBtn).toBeHidden();

    const openSourceLink = page.getByRole('link', { name: /Open Source/i });
    await expect(openSourceLink).toBeHidden();

    // The "Sign In" button and "Blog" should still be visible (or in a hamburger menu, if implemented)
    const signInBtn = page.getByRole('link', { name: /Sign In/i });
    await expect(signInBtn).toBeVisible();

    // Check for horizontal scrollbars by executing client-side JS
    const hasHorizontalScrollbar = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    });
    expect(hasHorizontalScrollbar).toBe(false);
  });

  test('login page scales properly on mobile', async ({ page }) => {
    await page.goto('/en/login');
    
    // Check for horizontal scrollbars by executing client-side JS
    const hasHorizontalScrollbar = await page.evaluate(() => {
      return document.documentElement.scrollWidth > document.documentElement.clientWidth;
    });
    expect(hasHorizontalScrollbar).toBe(false);

    // Inputs should still be fully visible
    await expect(page.locator('input[type="email"]#email-input')).toBeInViewport();
  });
});