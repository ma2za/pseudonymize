import { test, expect } from '@playwright/test';

test.describe('Documentation & Proof Pages', () => {

  test('Docs: Main API documentation page renders correctly from Markdown', async ({ page }) => {
    await page.goto('/en/docs');
    
    // Verify the Markdown content is injected correctly
    await expect(page.getByRole('heading', { name: /pseudonymize.io API/i })).toBeVisible();
    await expect(page.getByRole('heading', { name: /Authentication/i })).toBeVisible();
    await expect(page.getByText(/curl -X POST https:\/\/api.pseudonymize.io\/v1\/text/i)).toBeVisible();
  });

  test('Docs: Concepts (Pseudonyms) page renders correctly from Markdown', async ({ page }) => {
    await page.goto('/en/docs/concepts/pseudonyms');
    
    // Verify the concept content is visible
    await expect(page.getByRole('heading', { name: /Pseudonyms/i })).toBeVisible();
    await expect(page.getByRole('heading', { name: /What it means/i })).toBeVisible();
    await expect(page.getByText(/A pseudonym is a structured alias/i)).toBeVisible();
  });

  test('Docs: Concepts (Determinism) page renders correctly from Markdown', async ({ page }) => {
    await page.goto('/en/docs/concepts/determinism');
    
    // Verify the concept content is visible
    await expect(page.getByRole('heading', { name: /Determinism/i })).toBeVisible();
    await expect(page.getByRole('heading', { name: /Security Properties/i })).toBeVisible();
  });

  test('Proof: Security architecture page renders correctly from Markdown', async ({ page }) => {
    await page.goto('/en/security');
    
    // Verify the security architecture content is visible
    await expect(page.getByRole('heading', { name: /Security Architecture/i })).toBeVisible();
    await expect(page.getByRole('heading', { name: /Threat Model/i })).toBeVisible();
    await expect(page.getByText(/Pseudonymization reduces exposure/i)).toBeVisible();
  });

  test('Proof: Benchmarks page renders correctly from Markdown', async ({ page }) => {
    await page.goto('/en/benchmarks');
    
    // Verify the benchmarks content is visible
    await expect(page.getByRole('heading', { name: /Detection Benchmarks/i })).toBeVisible();
    
    // Check that the precision/recall metrics are present
    await expect(page.getByText('Precision').first()).toBeVisible();
    await expect(page.getByText('Recall').first()).toBeVisible();
  });

});
