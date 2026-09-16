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

  test('should successfully sign out an authenticated user without 404', async ({ page }) => {
    // 1. Sign up a new user to get a valid session
    await page.goto('/en/signup');
    const email = `test.signout.${Date.now()}@example.com`;
    const password = 'Password123!';
    
    await page.locator('#name-input').fill('Test Signout User');
    await page.locator('#email-input').fill(email);
    await page.locator('#password-input').fill(password);
    
    await page.getByRole('button', { name: 'Sign up' }).click();

    // The sign up creates the user but better-auth might require login depending on config, OR it directly logs in. Let's explicitly log in if we aren't redirected.
    // Wait for URL to change to dashboard
    await expect(page).toHaveURL(/.*\/dashboard/, { timeout: 10000 });

    // 3. Click the Sign Out button
    // The text might be localized, so we use a robust selector or text matching.
    // 'Sign out' is the default English text for the button we modified.
    await page.getByRole('button', { name: 'Sign out' }).click();

    // 4. Verify we are redirected to the homepage, NOT a 404 page
    // The signout success callback uses `window.location.href = \`/${locale}\`;`
    await expect(page).toHaveURL(/\/en$/); // Should end up at /en (homepage)
    
    // 5. Verify the login button is visible again, confirming signed-out state
    await expect(page.getByRole('link', { name: 'Sign in' })).toBeVisible();
  });
});
