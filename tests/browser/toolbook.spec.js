const { test, expect } = require('@playwright/test');

test('serves the static guide without an application runtime', async ({ page }) => {
  await page.goto('/index.html');
  await expect(page).toHaveTitle('中文 Codex 实战手册');
  await expect(page.locator('h1')).toContainText('可验证小任务');
  await expect(page.locator('.global-nav [data-nav]')).toHaveCount(19);
  await expect(page.locator('.global-nav [aria-current="page"]')).toHaveCount(1);
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
