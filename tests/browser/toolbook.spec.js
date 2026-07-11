const { test, expect } = require('@playwright/test');

test('serves the static guide without an application runtime', async ({ page }) => {
  await page.goto('/index.html');
  await expect(page).toHaveTitle('中文 Codex 实战手册');
  await expect(page.locator('h1')).toContainText('可验证小任务');
  await expect(page.locator('.global-nav [data-nav]')).toHaveCount(19);
  await expect(page.locator('.global-nav [aria-current="page"]')).toHaveCount(1);
});

test('exposes complete social metadata from the page manifest', async ({ page }) => {
  await page.goto('/permissions.html');
  await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', 'https://whojay0609.github.io/codex-usage-guide/permissions.html');
  await expect(page.locator('meta[name="description"]')).toHaveAttribute('content', '理解 sandbox、approval、network 与 secret 边界。');
  await expect(page.locator('meta[property="og:title"]')).toHaveAttribute('content', '权限与安全');
  await expect(page.locator('meta[property="og:image"]')).toHaveAttribute('content', 'https://whojay0609.github.io/codex-usage-guide/figures/social-preview.png');
  await expect(page.locator('meta[name="twitter:card"]')).toHaveAttribute('content', 'summary_large_image');
});

test('keeps article content readable without horizontal overflow', async ({ page }) => {
  await page.goto('/permissions.html');
  await expect(page.locator('h1')).toHaveText('权限与安全');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  expect(overflow).toBeFalsy();
});

test('uses three columns on desktop', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/goal.html');
  const columns = await page.locator('.toolbook-shell').evaluate((element) => getComputedStyle(element).gridTemplateColumns.split(' ').length);
  expect(columns).toBe(3);
  await expect(page.locator('.global-nav')).toBeVisible();
  await expect(page.locator('.page-toc')).toBeVisible();
});

test('opens mobile navigation and places the page toc before the article', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/permissions.html');
  await expect(page.locator('.global-nav')).toBeHidden();
  await page.locator('.menu-toggle').click();
  await expect(page.locator('.global-nav')).toBeVisible();
  await expect(page.locator('.menu-toggle')).toHaveAttribute('aria-expanded', 'true');
  await page.keyboard.press('Escape');
  await expect(page.locator('.menu-toggle')).toBeFocused();
  const positions = await page.evaluate(() => ({ toc: document.querySelector('.page-toc').getBoundingClientRect().top, article: document.querySelector('.toolbook-main').getBoundingClientRect().top }));
  expect(positions.toc).toBeLessThan(positions.article);
});

test('searches canonical sections with an accessible modal', async ({ page }) => {
  await page.goto('/index.html');
  await page.locator('.search-trigger').click();
  await expect(page.locator('#site-search-dialog')).toBeVisible();
  await expect(page.locator('#site-search-input')).toBeFocused();
  await page.locator('#site-search-input').fill('审批决策矩阵');
  const option = page.locator('#site-search-results [role="option"]').first();
  await expect(option).toContainText('权限与安全');
  await expect(option).toContainText('审批决策矩阵');
  await page.keyboard.press('ArrowDown');
  await expect(page.locator('#site-search-input')).toHaveAttribute('aria-activedescendant', /search-option-/);
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/permissions\.html#%E5%AE%A1%E6%89%B9%E5%86%B3%E7%AD%96%E7%9F%A9%E9%98%B5$/);
});

test('closes search with Escape and restores trigger focus', async ({ page }) => {
  await page.goto('/permissions.html');
  await page.locator('.search-trigger').click();
  await page.keyboard.press('Escape');
  await expect(page.locator('#site-search-dialog')).toBeHidden();
  await expect(page.locator('.search-trigger')).toBeFocused();
});

test('copies exact prompt text and reports clipboard failure truthfully', async ({ page, context }) => {
  await context.grantPermissions(['clipboard-read', 'clipboard-write']);
  await page.goto('/permissions.html');
  const block = page.locator('.copy-block').first();
  const expected = await block.locator('pre > code').textContent();
  await block.locator('.copy-button').click();
  await expect(block.locator('.copy-status')).toContainText('已复制');
  expect(await page.evaluate(() => navigator.clipboard.readText())).toBe(expected);

  await page.evaluate(() => {
    Object.defineProperty(navigator, 'clipboard', { configurable: true, value: undefined });
  });
  await block.locator('.copy-button').click();
  await expect(block.locator('.copy-status')).toContainText('复制失败');
  await expect(block.locator('.copy-button')).toHaveText('复制');
});

test('exposes a focusable canonical permalink for every reader heading', async ({ page }) => {
  await page.goto('/permissions.html');
  const headings = page.locator('main h2, main h3');
  const links = page.locator('main [data-heading-permalink]');
  await expect(links).toHaveCount(await headings.count());
  await expect(links.filter({ has: page.locator('[aria-hidden="true"]') }).first()).toBeVisible();
  await links.first().focus();
  await expect(links.first()).toBeFocused();
});

test('persists manual theme choices and survives storage failure', async ({ page }) => {
  await page.goto('/index.html');
  await page.locator('.theme-select').selectOption('dark');
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
  await page.reload();
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
  await page.evaluate(() => {
    Object.defineProperty(window, 'localStorage', { configurable: true, get() { throw new Error('denied'); } });
  });
  await page.locator('.theme-select').selectOption('light');
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
  await expect(page.locator('.theme-status')).toContainText('未保存');
});

test('marks only cross-origin HTTP links as external', async ({ page }) => {
  await page.goto('/permissions.html');
  const external = page.locator('main a.external-link').first();
  await expect(external).toHaveAttribute('target', '_blank');
  await expect(external).toHaveAttribute('rel', 'noopener noreferrer');
  await expect(external).toHaveAttribute('referrerpolicy', 'no-referrer');
  await expect(external.locator('.external-link-indicator')).toHaveText('↗');
  await expect(page.locator('a[href^="mailto:"]')).not.toHaveClass(/external-link/);
});
