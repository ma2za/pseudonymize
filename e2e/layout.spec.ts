import { test, expect } from '@playwright/test';

test.describe('Global Layout Components', () => {
  
  test('Header renders correctly across languages and contains proper navigation', async ({ page }) => {
    await page.goto('/en');
    
    // Logo Link
    const logoLink = page.getByRole('link', { name: /pseudonymize\.io/i });
    await expect(logoLink).toBeVisible();
    await expect(logoLink).toHaveAttribute('href', '/en');

    // Auth links (desktop)
    const signInLink = page.getByRole('link', { name: /Sign In/i });
    await expect(signInLink).toBeVisible();
    await expect(signInLink).toHaveAttribute('href', '/en/login');

    const signUpLink = page.getByRole('link', { name: /Sign Up/i });
    await expect(signUpLink).toBeVisible();
    await expect(signUpLink).toHaveAttribute('href', '/en/signup');

    // Marketing Links
    const blogLink = page.getByRole('link', { name: /Blog/i }).first(); // Could be in footer too
    await expect(blogLink).toBeVisible();
    await expect(blogLink).toHaveAttribute('href', '/en/blog');
  });

  test('Footer renders correctly with legal strings', async ({ page }) => {
    await page.goto('/en');

    // Legal strings
    await expect(page.getByText(/© 2026 pseudonymize\.io\. All rights reserved\./i)).toBeVisible();

    // Footer Links
    const privacyLink = page.getByRole('link', { name: /Privacy Policy/i });
    await expect(privacyLink).toBeVisible();

    const termsLink = page.getByRole('link', { name: /Terms of Service/i });
    await expect(termsLink).toBeVisible();
  });
});