import { test, expect } from '@playwright/test';

test.describe('Blog Subsystem & Markdown Rendering', () => {

  test('Blog index should render properly with correct SEO headers', async ({ page }) => {
    await page.goto('/en/blog');
    
    // Verify title and standard blog strings
    await expect(page).toHaveTitle(/Our Blog/i);
    await expect(page.getByRole('heading', { name: /Our Blog/i, level: 1 })).toBeVisible();

    // Verify at least one blog post is loaded from the markdown folder
    await expect(page.getByRole('heading', { name: 'The Future of PII Management', level: 3 })).toBeVisible();
    await expect(page.getByText('Why modern enterprises are shifting towards deterministic pseudonymization')).toBeVisible();
  });

  test('Blog article should render parsed HTML from Markdown', async ({ page }) => {
    await page.goto('/en/blog/the-future-of-pii-management');

    // Title should dynamically pull from the post
    await expect(page).toHaveTitle(/The Future of PII Management/);
    await expect(page.getByRole('heading', { name: 'The Future of PII Management', level: 1 })).toBeVisible();

    // Verify markdown headers compiled correctly into HTML
    const mdHeader = page.getByRole('heading', { name: 'The Shift in Data Privacy', level: 1 });
    await expect(mdHeader).toBeVisible();

    // Verify markdown bold and text blocks parsed correctly
    await expect(page.getByText('Random anonymization destroys the relational integrity')).toBeVisible();
  });

  test('Blog article should return a 404/not found gracefully for bad slugs', async ({ page }) => {
    const response = await page.goto('/en/blog/does-not-exist');
    expect(response?.status()).toBe(404);
  });
});