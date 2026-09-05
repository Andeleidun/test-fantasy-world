import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('keyboard skip link, search, filters and dictionary work at a project URL', async ({ page }) => {
  await page.goto('./');
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: 'Skip to content' })).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.locator('#main')).toBeFocused();
  await page.getByRole('link', { name: 'Search the lore', exact: true }).click();
  await page.getByLabel('Search the lore', { exact: true }).fill('Hamarkor');
  await expect(page.locator('#results li').first()).toBeVisible();
  await page.getByLabel('Within').selectOption('language');
  await expect(page.locator('#results .eyebrow').first()).toHaveText('language');
  await page.getByLabel('Search the lore', { exact: true }).fill('zxqvnotaword');
  await expect(page.getByRole('status')).toContainText('No results');
  await page.goto('dictionary.html');
  await page.getByLabel('Find a word or meaning').fill('rakkor');
  await expect(page.locator('#dictionary tbody tr:visible')).toHaveCount(1);
  await expect(page.locator('#dictionary tbody tr:visible')).toContainText('regional');
});

test('search recovers after a failed index request', async ({ page }) => {
  let attempts = 0;
  await page.route('**/search-index.json', route => ++attempts === 1 ? route.abort() : route.continue());
  await page.goto('search.html?q=Thal');
  await expect(page.getByRole('status')).toContainText('Search could not load');
  await page.getByRole('button', { name: 'Search', exact: true }).click();
  await expect(page.locator('#results li').first()).toBeVisible();
});

test('worlds and dictionary remain readable without JavaScript', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto('http://127.0.0.1:4173/test-fantasy-world/dverghamar.html');
  await expect(page.getByRole('heading', { name: 'Dverghamar', exact: true })).toBeVisible();
  await page.getByRole('link', { name: 'Meet the Hamarkorar' }).click();
  await expect(page.getByRole('heading', { name: 'The Hamarkorar', exact: true })).toBeVisible();
  await page.goto('http://127.0.0.1:4173/test-fantasy-world/dictionary.html');
  await expect(page.locator('#dictionary tbody tr')).toHaveCount(571);
  await context.close();
});

for (const width of [1440, 390, 320]) {
  test(`responsive reader and accessibility at ${width}px`, async ({ page }) => {
    await page.setViewportSize({ width, height: 950 });
    for (const path of ['./', 'dverghamar.html', 'language-grammar.html', 'dverghamar-atlas.html', 'search.html', 'dictionary.html']) {
      await page.goto(path);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
      const results = await new AxeBuilder({ page }).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
      expect(results.violations, JSON.stringify(results.violations.map(v => ({ id: v.id, nodes: v.nodes.map(n => n.target) })))).toEqual([]);
    }
  });
}
