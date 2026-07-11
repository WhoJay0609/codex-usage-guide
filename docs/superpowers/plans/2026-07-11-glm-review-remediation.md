# GLM Review Remediation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct the guide’s product terminology and technical boundaries, distinguish native features from recommended practices, and close the highest-value content, accessibility, and maintainability gaps identified by the GLM review.

**Architecture:** Keep article prose as authored HTML, keep navigation/headings/search payloads generator-owned, and encode high-risk product facts as regression-tested semantic contracts. Resolve review claims against current OpenAI documentation instead of applying the report mechanically; record claims that are obsolete or contradicted by current official docs in a disposition matrix.

**Tech Stack:** Static HTML, CSS, browser JavaScript, Python site generator/validator, `unittest`, Playwright.

---

## File map

- `docs/reviews/2026-07-11-glm-review-disposition.md`: one-row-per-issue evidence and disposition matrix.
- `data/site-manifest.json`: canonical page titles, navigation labels, descriptions, and verification dates.
- `scripts/build_site.py`: generated header, grouped breadcrumbs, skip link, lazy search-index hook, and uniform page sequence.
- `scripts/check_site.py`: site-wide terminology and product-boundary release gates.
- `tests/test_build_site.py`, `tests/test_check_site.py`: generator and semantic regression tests.
- `tests/browser/toolbook.spec.js`: search dialog keyboard/focus behavior and lazy-loading checks.
- `assets/site.js`: lazy search loading, highlighted matches, focus trap, and Escape priority.
- `assets/site.css`: section comments, focus/skip-link styles, `<mark>` styles, and dead-rule cleanup.
- `index.html`, `codex.html`, `install-desktop.html`, `desktop-cli.html`, `permissions.html`, `agents-md.html`, `skills.html`, `mcp.html`, `subagents.html`, `goal.html`: official product boundary and beginner-path corrections.
- `automation.html`, `workflows.html`, `daily-workflow.html`, `engineering.html`, `research.html`, `compound-engineering.html`, `skills-repositories.html`, `goal-entry.html`, `resources.html`: terminology, recommended-practice labels, safety warnings, CLI/Desktop boundaries, and glossary/resource corrections.
- `404.html`, `robots.txt`, `sitemap.xml`: static failure and discovery artifacts, registered in the publication model where applicable.

### Task 1: Lock the evidence boundary and failing semantic tests

**Files:**
- Create: `docs/reviews/2026-07-11-glm-review-disposition.md`
- Modify: `scripts/check_site.py`
- Modify: `tests/test_check_site.py`

- [ ] **Step 1: Write failing tests for the high-risk contracts**

Add tests that construct minimal page maps and assert errors for obsolete UI terms, bracketed skill invocations, missing native/recommended labels, missing Desktop/CLI boundary text, and a permission page without the four current desktop modes:

```python
def test_product_accuracy_contract_rejects_obsolete_desktop_terms(self) -> None:
    pages = {
        "permissions.html": parse("<main>Read-only Workspace-write Auto Danger</main>"),
        "automation.html": parse("<main>Automations Triage inbox</main>"),
        "skills.html": parse("<main><code>[$grill-with-docs]</code></main>"),
    }
    errors = validate_product_accuracy_contracts(pages)
    self.assertTrue(any("permission modes" in error for error in errors), errors)
    self.assertTrue(any("obsolete Scheduled tasks terminology" in error for error in errors), errors)
    self.assertTrue(any("invalid skill mention syntax" in error for error in errors), errors)
```

- [ ] **Step 2: Run the narrow test and confirm it fails**

Run: `python3 -m unittest tests.test_check_site.SemanticContractTests.test_product_accuracy_contract_rejects_obsolete_desktop_terms -v`

Expected: `FAIL` because `validate_product_accuracy_contracts` does not yet exist.

- [ ] **Step 3: Implement the validator with explicit page-scoped requirements**

Define `validate_product_accuracy_contracts(pages)` and call it from the normal site check. Require `Ask for approval`, `Approve for me`, `Full access`, `Custom (config.toml)` on `permissions.html`; reject visible `Triage inbox`, bracketed `$skill` calls, and unqualified native-sounding claims for `receipt`, `grant`, or the role framework.

- [ ] **Step 4: Create the disposition matrix**

Record every T/A/C/R/D numbered item and every “重要功能遗漏” row with status `fix`, `partial`, `no-change`, or `defer`, current evidence, affected source-of-truth files, and a reason. Explicitly record that current official documentation confirms “Integrated terminal” and `--dangerously-bypass-approvals-and-sandbox`, so those two report claims must not be implemented as mechanical replacements.

- [ ] **Step 5: Run the contract tests**

Run: `python3 -m unittest tests.test_check_site -v`

Expected: all tests pass.

### Task 2: Correct native product facts and beginner onboarding

**Files:**
- Modify: `data/site-manifest.json`
- Modify: `permissions.html`
- Modify: `agents-md.html`
- Modify: `mcp.html`
- Modify: `subagents.html`
- Modify: `goal.html`
- Modify: `install-desktop.html`
- Modify: `codex.html`
- Modify: `desktop-cli.html`

- [ ] **Step 1: Replace the desktop permission model**

Replace the five CLI-derived cards with four current desktop modes and a separate CLI/config note:

```html
<article class="card span-6"><h3>Ask for approval</h3><p>工作区内可读写并运行常规命令；联网或越过工作区边界前询问用户。</p></article>
<article class="card span-6"><h3>Approve for me</h3><p>设置中称 Auto-review；额外权限请求由自动审阅器判断，仍可能出错。</p></article>
<article class="card span-6"><h3>Full access</h3><p>可访问整台电脑并联网执行命令，无逐次审批；仅用于可信环境。</p></article>
<article class="card span-6"><h3>Custom (config.toml)</h3><p>通过 Codex 配置组合沙箱、审批和网络边界。</p></article>
```

- [ ] **Step 2: Add the complete AGENTS.md discovery chain**

Explain `CODEX_HOME`, global `AGENTS.override.md`/`AGENTS.md`, project-root-to-CWD traversal, per-directory override priority, fallback filenames, and the default 32 KiB combined limit. Keep `apply_patch` only as an optional implementation detail, not a desktop control the reader must find.

- [ ] **Step 3: Add actionable MCP setup and safety boundaries**

Document Model Context Protocol, desktop Settings > MCP servers, STDIO vs Streamable HTTP, shared `~/.codex/config.toml`, a minimal TOML example, plugin/MCP relationship, and untrusted server instructions/tool output as prompt-injection input that must not override user intent.

- [ ] **Step 4: Explain subagent context and Goal behavior**

State that subagents receive the task context supplied by the orchestrating thread rather than an assumed full private conversation copy; each agent performs its own model/tool work and returns activity/results to the main task. Label the six-field Goal block as this guide’s recommended prompt contract, provide a minimal first-use version, describe progress checks, and contrast temporary Goal contracts with persistent `AGENTS.md` rules.

- [ ] **Step 5: Make installation useful and clarify naming**

Use “ChatGPT desktop app（本指南简称桌面版）中的 Codex” at first mention; add official download, Apple Silicon/Windows availability language, sign-in, selecting Codex, selecting a project, permission choice, and a first read-only task. Avoid fabricating a version number; show an official-facts verification date and “UI labels may change” note.

- [ ] **Step 6: Generate and run targeted checks**

Run: `make generate && python3 -m unittest tests.test_build_site tests.test_check_site -v`

Expected: generated assets update deterministically and all unit tests pass.

### Task 3: Normalize terminology and separate native features from guide practices

**Files:**
- Modify: `index.html`
- Modify: `automation.html`
- Modify: `skills.html`
- Modify: `skills-repositories.html`
- Modify: `goal-entry.html`
- Modify: `compound-engineering.html`
- Modify: `engineering.html`
- Modify: `workflows.html`
- Modify: `daily-workflow.html`
- Modify: `research.html`
- Modify: `resources.html`
- Modify: `README.md`
- Modify: `CONTEXT.md`

- [ ] **Step 1: Normalize current UI terms and skill syntax**

Use “Scheduled tasks（定时任务）” and “Scheduled 视图”; use `$skill-name`, `$ce-brainstorm`, and `$ce-plan` for Codex skill mentions. Preserve slash commands only when the upstream plugin actually defines slash commands and label them as plugin-specific.

- [ ] **Step 2: Add a native-versus-recommended boundary banner**

On the home page and affected workflow pages, distinguish native features (`Goal`, subagent, Worktree, MCP, `AGENTS.md`, skills, Scheduled tasks, Browser) from this guide’s practices (`receipt`, `grant`, role labels, five-stage loop, prompt ladder, claim ledger, six-field Goal template).

- [ ] **Step 3: Rename the role framework and unify closeout**

Replace A2/A3/A4 display labels with “用户 / 编排线程 / 执行线程”; label the mapping as a guide-specific teaching model. Use one Chinese-first completion receipt schema in `workflows.html` and `daily-workflow.html`.

- [ ] **Step 4: Add safety and installation prerequisites**

Warn against unattended Scheduled tasks that auto-commit/push/open PRs or run `/lfg`; recommend protected branches and human review. Mark `grant` as a prompt-level agreement that cannot expand product permissions. Mark Compound Engineering/ARS/ARIS installation surfaces as plugin or CLI-specific, with exact environment labels and upstream links.

- [ ] **Step 5: Add a Chinese-first glossary and current resource links**

Explain sandbox, approval, worktree, receipt, closeout, checkpoint, diff, commit, push, merge, PR, CI, Objective, Scope, Acceptance, Validation, prompt ladder, grant, disposition, and lane. Replace redirected `developers.openai.com/codex/...` links with their canonical `learn.chatgpt.com/docs/...` targets and add CLI, IDE, cloud, changelog, model/modes, Record & Replay, Memories, Chronicle, and config resources without pretending each is a desktop-only feature.

- [ ] **Step 6: Run negative searches and the full static check**

Run: `rg -n 'Triage inbox|\[\$[A-Za-z0-9_-]+\]|Codex Desktop Automations' -- *.html README.md CONTEXT.md`

Expected: no matches.

Run: `make check-fast`

Expected: pass.

### Task 4: Improve search, keyboard access, and generated page consistency

**Files:**
- Modify: `scripts/build_site.py`
- Modify: `assets/site.js`
- Modify: `assets/site.css`
- Modify: `tests/test_build_site.py`
- Modify: `tests/browser/toolbook.spec.js`

- [ ] **Step 1: Test lazy loading and keyboard containment**

Update generator tests to require `site-data.js` in the initial document and forbid `search-index.js` there. Add a browser test that opens search, waits for the index, tabs through controls without leaving the modal, closes with Escape, and verifies focus returns to the search trigger.

- [ ] **Step 2: Lazy-load the generated search index**

Remove the synchronous search-index script from the generated header. Add `loadSearchIndex()` that creates one deferred script element on first search activation, resolves when `GUIDE_SEARCH_INDEX` exists, reports loading/failure states, and reuses the same promise.

- [ ] **Step 3: Highlight matches without injecting HTML**

Build title/section/snippet content with text nodes and `<mark>` elements derived from normalized string ranges; never assign report/search content to `innerHTML`.

- [ ] **Step 4: Add focus trap and Escape priority**

Handle Tab/Shift+Tab inside the modal’s focusable controls. The dialog `cancel` handler owns Escape while open; the global navigation handler must return early when the search dialog is open.

- [ ] **Step 5: Generate a skip link and grouped breadcrumbs**

Add `<a class="skip-link" href="#main-content">跳到正文</a>`, ensure `<main id="main-content">`, and render `首页 / 分组 / 当前页` from the manifest navigation group.

- [ ] **Step 6: Run browser and generator checks**

Run: `make generate && python3 -m unittest tests.test_build_site -v && npm test`

Expected: all checks pass; initial pages do not request `assets/search-index.js` until search opens.

### Task 5: Close maintainability and publication gaps, then audit the whole report

**Files:**
- Modify: `assets/site.css`
- Modify: `README.md`
- Create: `404.html`
- Create: `robots.txt`
- Create: `sitemap.xml`
- Modify: `data/site-manifest.json`
- Modify: `tests/test_check_site.py`
- Modify: `docs/reviews/2026-07-11-glm-review-disposition.md`

- [ ] **Step 1: Remove confirmed dead CSS and consolidate dark variables**

Use repository-wide searches to prove `.nav`, `.side-nav`, and `.reveal-word` are unused before removal. Add short section comments for tokens, layout, components, accessibility, themes, and responsive rules. Keep one `:root[data-theme="dark"]` variable block.

- [ ] **Step 2: Document intentional formatting and source synchronization**

Explain in `README.md` that generator-owned sentinel blocks are intentionally compact and should not be hand-formatted, and that `src/main.tex` is a separate long-form source rather than an automatically synchronized mirror of every HTML edit.

- [ ] **Step 3: Add static fallback/discovery artifacts**

Create a branded 404 page using the shared assets, a `robots.txt` that points to the sitemap, and a sitemap containing manifest-scoped public pages. Add tests that ensure every sitemap HTML URL corresponds to the manifest.

- [ ] **Step 4: Finalize the issue matrix**

For each review item, link the proving diff/test/source. Mark image conversion, wholesale historical-case rewriting, broad HTML reformatting, or other deferred work explicitly with rationale instead of implying completion.

- [ ] **Step 5: Run full local release gates**

Run: `make generate && make check && make test-browser && make check-release-local`

Expected: all local automated gates pass. `make check-published` remains not run until changes are deployed.

- [ ] **Step 6: Review the final diff and scope**

Run: `git diff --check && git status --short && git diff --stat`

Expected: no whitespace errors; only planned sources, generated outputs, tests, and review/plan artifacts changed; no user work is discarded.
