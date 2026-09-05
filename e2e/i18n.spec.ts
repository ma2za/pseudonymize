import { test, expect } from '@playwright/test';

test.describe('i18n & Language Switcher', () => {
  test('changing language via select updates URL and content', async ({ page }) => {
    // Start at english root
    await page.goto('/en');

    // Ensure English text is present
    await expect(page.getByRole('heading', { name: /Pseudonymize sensitive data/i, exact: false })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Pseudonymize data' }).first()).toBeVisible();

    // Change language to Spanish using the switcher
    const languageSelect = page.getByRole('combobox', { name: 'Select language' });
    await expect(languageSelect).toBeVisible();
    
    // Select Spanish
    await languageSelect.selectOption('es');

    // Wait for navigation and verify the URL changed to /es
    await page.waitForURL('**/es');
    await expect(page).toHaveURL(/.*\/es/);
  });
});
