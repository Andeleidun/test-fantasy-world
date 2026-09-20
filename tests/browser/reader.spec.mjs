import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('keyboard skip link, search, filters and dictionary work at a project URL', async ({ page }) => {
  await page.goto('./');
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: 'Skip to content' })).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.locator('#main')).toBeFocused();
  await page.getByRole('link', { name: 'Search', exact: true }).click();
  await page.getByLabel('Search the lore', { exact: true }).fill('Hamarkor');
  await expect(page.locator('#results li').first()).toBeVisible();
  await page.getByLabel('Within').selectOption('language');
  await expect(page.locator('#results .eyebrow').first()).toHaveText('Language');
  await page.getByLabel('Search the lore', { exact: true }).fill('zxqvnotaword');
  await expect(page.getByRole('status')).toContainText('No results');
  await page.goto('korvar.html#dictionary-section');
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
  await page.locator('.toc').getByRole('link', { name: 'The Hamarkorar', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'The Hamarkorar', exact: true })).toBeVisible();
  await page.goto('http://127.0.0.1:4173/test-fantasy-world/merenval.html');
  await expect(page.getByRole('heading', { name: 'Merenval and its living companion', exact: true })).toBeVisible();
  await page.locator('.toc').getByRole('link', { name: 'Elven peoples and traditions', exact: true }).click();
  await expect(page.getByRole('heading', { name: 'Elven peoples and traditions', exact: true })).toBeVisible();
  await page.goto('http://127.0.0.1:4173/test-fantasy-world/korvar.html#dictionary-section');
  await expect(page.locator('#dictionary tbody tr')).toHaveCount(562);
  await context.close();
});

for (const theme of ['light', 'dark']) for (const width of [1440, 390, 320]) {
  test(`${theme} reader and accessibility at ${width}px`, async ({ page }) => {
    await page.emulateMedia({ colorScheme: theme });
    await page.setViewportSize({ width, height: 950 });
    for (const path of ['./', 'erde.html', 'dverghamar.html', 'merenval.html', 'magic.html', 'korvar.html', 'search.html', 'about.html']) {
      await page.goto(path);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
      const results = await new AxeBuilder({ page }).withTags(['wcag2a','wcag2aa','wcag21aa']).analyze();
      expect(results.violations, JSON.stringify(results.violations.map(v => ({ id: v.id, nodes: v.nodes.map(n => n.target) })))).toEqual([]);
    }
  });
}

test('theme follows the system, supports keyboard choice and persists across pages', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.goto('./');
  const toggle = page.getByRole('button', { name: 'Dark theme', exact: true });
  await expect(toggle).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('html')).toHaveCSS('color-scheme', 'dark');
  await page.emulateMedia({ colorScheme: 'light' });
  await expect(toggle).toHaveAttribute('aria-pressed', 'false');
  await toggle.focus();
  await page.keyboard.press('Space');
  await expect(toggle).toHaveAttribute('aria-pressed', 'true');
  await page.goto('erde.html');
  await expect(toggle).toHaveAttribute('aria-pressed', 'true');
  await page.reload();
  await expect(page.locator('html')).toHaveCSS('color-scheme', 'dark');
  await toggle.click();
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.reload();
  await expect(page.locator('html')).toHaveCSS('color-scheme', 'light');
  await page.emulateMedia({ media: 'print' });
  await expect(page.locator('html')).toHaveCSS('color-scheme', 'light');
});

test('dark reading works without JavaScript and the toggle tolerates blocked storage', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false, colorScheme: 'dark' });
  const page = await context.newPage();
  await page.goto('http://127.0.0.1:4173/test-fantasy-world/erde.html');
  await expect(page.locator('html')).toHaveCSS('color-scheme', 'dark');
  await expect(page.locator('#theme-toggle')).toBeHidden();
  await context.close();
  const stored = await browser.newContext({ colorScheme: 'light' });
  const screen = await stored.newPage();
  const errors = [];
  screen.on('pageerror', error => errors.push(error.message));
  await screen.addInitScript(() => {
    Object.defineProperty(window, 'localStorage', { get() { throw new DOMException('Blocked', 'SecurityError'); } });
  });
  await screen.goto('http://127.0.0.1:4173/test-fantasy-world/erde.html');
  await screen.getByRole('button', { name: 'Dark theme', exact: true }).click();
  await expect(screen.locator('html')).toHaveCSS('color-scheme', 'dark');
  expect(errors).toEqual([]);
  await screen.emulateMedia({ media: 'print' });
  await expect(screen.locator('html')).toHaveCSS('color-scheme', 'light');
  await stored.close();
});

test('search ignores stale requests, paginates and uses only public text', async ({ page }) => {
  let release;
  await page.route('**/search-index.json', async route => {
    await new Promise(resolve => { release = resolve; });
    await route.continue();
  });
  await page.goto('search.html?q=Thal');
  await expect.poll(() => Boolean(release)).toBe(true);
  await page.locator('#query').fill('zxqvnotaword');
  release();
  await expect(page.locator('#search-status')).toContainText('No results');
  await expect(page.locator('#results li')).toHaveCount(0);
  await page.locator('#query').fill('');
  await page.getByLabel('Within').selectOption('language');
  await expect(page.locator('#results li')).toHaveCount(20);
  await page.getByRole('button', { name: 'Show more results' }).click();
  await expect(page.locator('#results li')).toHaveCount(40);
  await expect(page.locator('#results li').nth(20).getByRole('link')).toBeFocused();
  await page.locator('#query').fill('supersession');
  await expect(page.locator('#search-status')).toContainText('No results');
});


test('old bookmarks reach complete guides, with inline maps and useful search destinations', async ({ page }) => {
  await page.goto('gnomes-full-reference.html#the-living-house');
  await expect(page).toHaveURL(/merenval\.html#gnomes-full-reference--the-living-house$/);
  await expect(page.locator('#gnomes-full-reference--the-living-house')).toBeInViewport();
  await expect(page.locator('#figure-gnome-living-house img')).toHaveJSProperty('complete', true);
  await page.goto('search.html?q=Alchemical&category=peoples');
  await expect(page.locator('#results')).toContainText('Goblins');
  await page.locator('#results a').first().click();
  await expect(page).toHaveURL(/erde\.html#goblins--/);
  await page.goto('erde-atlas.html#e4');
  await expect(page).toHaveURL(/erde\.html#e4$/);
  await expect(page.locator('#e4')).toBeInViewport();
  await expect(page.locator('#figure-erde-ancestry img')).toHaveJSProperty('complete', true);
});

test('mobile contents jump within a guide and close after selection', async ({ page }) => {
  await page.setViewportSize({ width:390, height:850 });
  await page.goto('dverghamar.html');
  const contents=page.locator('.mobile-toc');
  await contents.locator(':scope > summary').click();
  await contents.getByRole('link', { name:'The Jotun', exact:true }).click();
  await expect(contents).not.toHaveAttribute('open', '');
  await expect(page.locator('h2#jotuns')).toBeInViewport();
  await expect(page).toHaveURL(/dverghamar\.html#jotuns$/);
});

test('legacy links offer direct section destinations without JavaScript', async ({ browser }) => {
  const context=await browser.newContext({ javaScriptEnabled:false });
  const page=await context.newPage();
  await page.goto('http://127.0.0.1:4173/test-fantasy-world/language-grammar.html#noun-phrases-and-reference');
  await page.locator('#noun-phrases-and-reference a').click();
  await expect(page).toHaveURL(/korvar\.html#language-grammar--noun-phrases-and-reference$/);
  await expect(page.locator('#language-grammar--noun-phrases-and-reference')).toBeInViewport();
  await context.close();
});
