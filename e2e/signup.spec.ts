import { test, expect } from '@playwright/test';

test.describe('User Registration (Signup) Flow', () => {

  test('signup page should render all interactive elements', async ({ page }) => {
    await page.goto('/en/signup');

    // Title
    await expect(page.getByRole('heading', { name: /Create your account/i })).toBeVisible();

    // Inputs
    await expect(page.locator('input[type="text"]#name-input')).toBeVisible();
    await expect(page.locator('input[type="email"]#email-input')).toBeVisible();
    await expect(page.locator('input[type="password"]#password-input')).toBeVisible();

    // Buttons
    await expect(page.getByRole('button', { name: /Sign up/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /Google/i })).toBeVisible();
    
    // Links
    const loginLink = page.getByRole('link', { name: /Already have an account\? Sign in/i });
    await expect(loginLink).toBeVisible();
    await expect(loginLink).toHaveAttribute('href', '/en/login');
  });

  test('signup form should enforce HTML5 validation on email and password', async ({ page }) => {
    await page.goto('/en/signup');
    
    const emailInput = page.locator('input[type="email"]#email-input');
    const submitBtn = page.getByRole('button', { name: /Sign up/i });

    // Test malformed email
    await emailInput.fill('invalid-email-no-domain');
    
    // Evaluate HTML5 validity
    const isEmailInvalid = await emailInput.evaluate((el: HTMLInputElement) => !el.checkValidity());
    expect(isEmailInvalid).toBe(true);

    // Verify fields are required
    const nameInput = page.locator('input[type="text"]#name-input');
    const isNameRequired = await nameInput.evaluate((el: HTMLInputElement) => el.required);
    expect(isNameRequired).toBe(true);
  });
});
