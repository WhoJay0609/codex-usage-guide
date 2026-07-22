const { test, expect } = require('@playwright/test');

test('serves the static guide without an application runtime', async ({ page }) => {
  await page.goto('/index.html');
  await expect(page).toHaveTitle('中文 Codex 实战手册');
  await expect(page.locator('h1')).toContainText('可验证的小任务');
  await expect(page.locator('.global-nav [data-nav]')).toHaveCount(20);
  await expect(page.locator('.global-nav [aria-current="page"]')).toHaveCount(1);
});

test('exposes complete social metadata from the page manifest', async ({ page }) => {
  await page.goto('/permissions.html');
  await expect(page.locator('link[rel="canonical"]')).toHaveAttribute('href', 'https://whojay0609.github.io/codex-usage-guide/permissions.html');
  await expect(page.locator('meta[name="description"]')).toHaveAttribute('content', '理解 Desktop 常见权限模式及底层 sandbox、approval、network 与 secret 边界。');
  await expect(page.locator('meta[property="og:title"]')).toHaveAttribute('content', '权限与安全');
  await expect(page.locator('meta[property="og:image"]')).toHaveAttribute('content', 'https://whojay0609.github.io/codex-usage-guide/figures/social-preview.png');
  await expect(page.locator('meta[name="twitter:card"]')).toHaveAttribute('content', 'summary_large_image');
});

test('renders manifest sources and a visible generated changelog', async ({ page }) => {
  await page.goto('/index.html');
  await expect(page.locator('.page-sources')).toContainText('OpenAI 官方');
  await expect(page.locator('.recent-updates .update-card')).toHaveCount(3);
  await expect(page.locator('.changelog-disclosure')).toContainText('查看完整更新记录');

  await page.goto('/prompt-guidance.html');
  await expect(page.locator('.page-source-link')).toHaveCount(2);
  await expect(page.locator('.page-sources')).toContainText('OpenAI 官方');
  await expect(page.locator('.page-sources')).toContainText('第三方上游');
});

test('keeps every public page usable at desktop and mobile widths', async ({ page }) => {
  await page.goto('/index.html');
  const paths = await page.evaluate(() => window.GUIDE_SITE_DATA.pages.map((item) => item.path));
  for (const viewport of [{ width: 1440, height: 900 }, { width: 390, height: 844 }]) {
    await page.setViewportSize(viewport);
    for (const path of paths) {
      await page.goto(`/${path}`);
      await expect(page.locator('main h1')).toHaveCount(1);
      const overflow = await page.evaluate(
        () => document.documentElement.scrollWidth > document.documentElement.clientWidth,
      );
      expect(overflow, `${path} overflows at ${viewport.width}px`).toBeFalsy();
    }
  }
});

test('keeps article content readable without horizontal overflow', async ({ page }) => {
  await page.goto('/permissions.html');
  await expect(page.locator('h1')).toHaveText('权限与安全');
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  expect(overflow).toBeFalsy();
});

test('renders horizontal Mermaid flows at article width without empty fixed-height cards', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  for (const path of ['install-desktop.html', 'daily-workflow.html', 'skills.html']) {
    await page.goto(`/${path}`);
    const diagram = page.locator('.mermaid').first();
    const svg = diagram.locator('svg');
    await expect(svg).toBeVisible();
    const geometry = await diagram.evaluate((element) => {
      const container = element.getBoundingClientRect();
      const rendered = element.querySelector('svg').getBoundingClientRect();
      return {
        containerWidth: container.width,
        containerHeight: container.height,
        svgWidth: rendered.width,
        svgHeight: rendered.height,
      };
    });
    expect(geometry.svgWidth, `${path} Mermaid width`).toBeGreaterThan(geometry.containerWidth * 0.8);
    expect(geometry.containerHeight - geometry.svgHeight, `${path} Mermaid empty vertical space`).toBeLessThan(90);
  }
});

test('loads every guide illustration with useful alternative text and a figure explanation', async ({ page }) => {
  for (const path of ['permissions.html', 'mcp.html', 'subagents.html', 'prompt-guidance.html']) {
    await page.goto(`/${path}`);
    const figure = page.locator('.article-illustration');
    await expect(figure).toHaveCount(1);
    await expect(figure.locator('figcaption')).toContainText('图意：');
    const image = figure.locator('img');
    await expect(image).toHaveAttribute('alt', /\S{12,}/);
    await expect.poll(() => image.evaluate((element) => element.naturalWidth)).toBe(1672);
  }
});

test('uses a compact table-of-contents above the article on desktop', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/goal.html');
  const columns = await page.locator('.toolbook-shell').evaluate((element) => getComputedStyle(element).gridTemplateColumns.split(' ').length);
  expect(columns).toBe(2);
  await expect(page.locator('.global-nav')).toBeVisible();
  await expect(page.locator('.page-toc')).toBeVisible();
  const toc = page.locator('.page-toc details');
  await expect(toc).not.toHaveAttribute('open', '');
  await expect(page.locator('.page-toc nav')).toBeHidden();
  await page.locator('.page-toc summary').click();
  await expect(page.locator('.page-toc nav')).toBeVisible();
  const positions = await page.evaluate(() => ({
    toc: document.querySelector('.page-toc').getBoundingClientRect().top,
    article: document.querySelector('.toolbook-main > main').getBoundingClientRect().top,
  }));
  expect(positions.toc).toBeLessThan(positions.article);
});

test('opens mobile navigation and keeps the page toc before the article', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/permissions.html');
  await expect(page.locator('.global-nav')).toBeHidden();
  await page.locator('.menu-toggle').click();
  await expect(page.locator('.global-nav')).toBeVisible();
  await expect(page.locator('.menu-toggle')).toHaveAttribute('aria-expanded', 'true');
  await page.keyboard.press('Escape');
  await expect(page.locator('.menu-toggle')).toBeFocused();
  const positions = await page.evaluate(() => ({
    toc: document.querySelector('.page-toc').getBoundingClientRect().top,
    article: document.querySelector('.toolbook-main > main').getBoundingClientRect().top,
  }));
  expect(positions.toc).toBeLessThan(positions.article);
});

test('keeps the home headline compact and expands individual skill repositories', async ({ page }) => {
  await page.setViewportSize({ width: 1144, height: 994 });
  await page.goto('/index.html');
  const headlineSize = await page.locator('.home-hero h1').evaluate((element) => Number.parseFloat(getComputedStyle(element).fontSize));
  expect(headlineSize).toBeLessThan(60);

  const repositoryNav = page.locator('.global-nav-disclosure');
  await expect(repositoryNav).not.toHaveAttribute('open', '');
  await repositoryNav.locator('summary').click();
  await expect(repositoryNav).toHaveAttribute('open', '');
  await expect(repositoryNav.locator('a[href="skills-repositories.html#compound-engineering"]')).toBeVisible();
  await expect(repositoryNav.locator('a[href="skills-repositories.html#mattpocock-skills"]')).toBeVisible();
  await expect(repositoryNav.locator('a[href="skills-repositories.html#academic-research-skills-codex"]')).toBeVisible();
  await expect(repositoryNav.locator('a[href="skills-repositories.html#aris-auto-claude-code-research-in-sleep"]')).toBeVisible();
});

test('keeps OpenCodex separate from native Codex and extension mechanisms', async ({ page }) => {
  await page.goto('/skills-repositories.html#opencodex');
  const section = page.locator('#opencodex-section');
  await expect(section.locator('h2')).toContainText('lidge-jun/opencodex');
  await expect(section).toContainText('第三方本地 provider proxy');
  await expect(section).toContainText('不是 Codex Skill、Plugin 或 MCP server');
  await expect(section).toContainText('127.0.0.1');
  await expect(section.locator('a[href="https://github.com/lidge-jun/opencodex"]')).toBeVisible();
});

test('keeps dot-skills as a third-party skill collection with a Codex-specific install path', async ({ page }) => {
  await page.goto('/skills-repositories.html#dot-skills');
  const section = page.locator('#dot-skills-section');
  await expect(section.locator('h2')).toContainText('pproenca/dot-skills');
  await expect(section).toContainText('第三方 Agent Skills 开放格式集合');
  await expect(section).toContainText('.codex/skills/<name>/');
  await expect(section).toContainText('不是一个 Codex Plugin 或 MCP server');
  await expect(section.locator('a[href="https://github.com/pproenca/dot-skills"]')).toBeVisible();
});

test("keeps whojay-skill evidence-first and within the user's authorization boundary", async ({ page }) => {
  await page.goto('/skills-repositories.html#whojay-skill');
  const section = page.locator('#whojay-skill-section');
  await expect(section.locator('h2')).toContainText('WhoJay0609/whojay-skill');
  await expect(section).toContainText('$colleague-whojay');
  await expect(section).toContainText('已验证');
  await expect(section).toContainText('未知或阻塞');
  await expect(section).toContainText('不会自动授权删除、远程发布、外部消息、付费调用或 GPU 运行');
  await expect(section.locator('a[href="https://github.com/WhoJay0609/whojay-skill"]')).toBeVisible();
});

test('introduces Agent Reach as a third-party capability router with explicit diagnostic and authorization boundaries', async ({ page }) => {
  await page.goto('/skills-repositories.html#agent-reach');
  const section = page.locator('#agent-reach-section');
  await expect(section.locator('h2')).toContainText('Panniantong/Agent-Reach');
  await expect(section).toContainText('$agent-reach');
  await expect(section).toContainText('第三方 CLI + Skill 互联网能力路由器');
  await expect(section).toContainText('agent-reach doctor --json');
  await expect(section).toContainText('不是原生 Codex、Plugin，也不是单一 MCP server');
  await expect(section).toContainText('外部写操作仍由用户明确授权');
  await expect(section.locator('a[href="https://github.com/Panniantong/Agent-Reach"]')).toBeVisible();
});

test('introduces Worktrees on a standalone page and keeps Subagents focused', async ({ page }) => {
  await page.goto('/worktrees.html');
  await expect(page.locator('h1')).toHaveText('Worktrees');
  await expect(page.locator('.global-nav a[href="worktrees.html"]')).toHaveAttribute('aria-current', 'page');
  await expect(page.locator('#desktop-start')).toContainText('detached HEAD');
  await expect(page.locator('#handoff')).toContainText('Hand off');
  await expect(page.locator('#safety')).toContainText('.worktreeinclude');

  await page.goto('/subagents.html');
  const relationship = page.locator('#worktree-subagent');
  await expect(relationship).toContainText('Worktree 与 Subagent 如何配合');
  await expect(relationship.locator('.mermaid')).toHaveCount(0);
  await expect(relationship.locator('a[href="worktrees.html#relationship"]')).toBeVisible();
});

test('starts the Compound Engineering core loop with Ideate', async ({ page }) => {
  await page.goto('/compound-engineering.html');
  await expect(page.locator('#loop h2')).toHaveText('核心七步怎么用#');
  const steps = page.locator('#loop .decision-row strong');
  await expect(steps).toHaveCount(7);
  await expect(steps.nth(0)).toHaveText('1. /ce-ideate');
  await expect(steps.nth(1)).toHaveText('2. /ce-brainstorm');
  await expect(steps.nth(6)).toHaveText('7. /ce-compound');
  await expect(page.locator('#核心六步怎么用')).toHaveCount(1);
});

test('searches canonical sections with an accessible modal', async ({ page }) => {
  await page.goto('/index.html');
  await expect(page.locator('script[src="assets/search-index.js"]')).toHaveCount(0);
  await page.locator('.search-trigger').click();
  await expect(page.locator('script[src="assets/search-index.js"]')).toHaveCount(1);
  await expect(page.locator('#site-search-dialog')).toBeVisible();
  await expect(page.locator('#site-search-input')).toBeFocused();
  await page.locator('#site-search-input').fill('审批决策矩阵');
  const option = page.locator('#site-search-results [role="option"]').first();
  await expect(option).toContainText('权限与安全');
  await expect(option).toContainText('审批决策矩阵');
  await expect(option.locator('mark')).toContainText('审批决策矩阵');
  await page.keyboard.press('ArrowDown');
  await expect(page.locator('#site-search-input')).toHaveAttribute('aria-activedescendant', /search-option-/);
  await page.keyboard.press('Enter');
  await expect(page).toHaveURL(/permissions\.html#%E5%AE%A1%E6%89%B9%E5%86%B3%E7%AD%96%E7%9F%A9%E9%98%B5$/);
});

test('keeps keyboard focus inside search and exposes grouped navigation', async ({ page }) => {
  await page.goto('/permissions.html');
  await expect(page.locator('.skip-link')).toHaveAttribute('href', '#main-content');
  await expect(page.locator('.breadcrumbs')).toContainText('基础概念');
  await page.locator('.search-trigger').click();
  await page.locator('.search-close').focus();
  await page.keyboard.press('Tab');
  await expect(page.locator('#site-search-input')).toBeFocused();
  await page.keyboard.press('Shift+Tab');
  await expect(page.locator('.search-close')).toBeFocused();
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

test('exposes a focusable canonical permalink for standalone reader headings', async ({ page }) => {
  await page.goto('/permissions.html');
  const headings = page.locator('main h2, main h3');
  const links = page.locator('main [data-heading-permalink]');
  await expect(links).toHaveCount(await headings.count());
  await expect(links.filter({ has: page.locator('[aria-hidden="true"]') }).first()).toBeVisible();
  await links.first().focus();
  await expect(links.first()).toBeFocused();
});

test('keeps source-card content inside its link instead of nesting links', async ({ page }) => {
  await page.goto('/index.html');
  const card = page.locator('a.source-card[href="install-desktop.html"]');
  await expect(card).toHaveCount(1);
  await expect(card.locator('h3')).toContainText('零基础：安装到第一个任务');
  await expect(card.locator('p')).toContainText('安装 Codex Desktop');
  const geometry = await card.evaluate((element) => {
    const box = element.getBoundingClientRect();
    const heading = element.querySelector('h3').getBoundingClientRect();
    const paragraph = element.querySelector('p').getBoundingClientRect();
    return { box, heading, paragraph };
  });
  expect(geometry.heading.left).toBeGreaterThanOrEqual(geometry.box.left);
  expect(geometry.heading.right).toBeLessThanOrEqual(geometry.box.right);
  expect(geometry.paragraph.left).toBeGreaterThanOrEqual(geometry.box.left);
  expect(geometry.paragraph.right).toBeLessThanOrEqual(geometry.box.right);
});

test('defaults to light, persists manual theme choices, and survives storage failure', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.goto('/index.html');
  await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
  await expect(page.locator('.theme-select')).toHaveValue('light');
  await expect(page.locator('.theme-select option')).toHaveCount(2);
  await expect(page.locator('.theme-select option[value="system"]')).toHaveCount(0);
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
  await page.goto('/resources.html');
  const external = page.locator('main a.external-link').first();
  await expect(external).toHaveAttribute('target', '_blank');
  await expect(external).toHaveAttribute('rel', 'noopener noreferrer');
  await expect(external).toHaveAttribute('referrerpolicy', 'no-referrer');
  await expect(external.locator('.external-link-indicator')).toHaveText('↗');
  await expect(page.locator('main a[href="install-desktop.html"]').first()).not.toHaveClass(/external-link/);
  await expect(page.locator('main a[href^="#"]').first()).not.toHaveClass(/external-link/);
});
