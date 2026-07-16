# AGENTS.md

## Repository Purpose

This repository contains a Chinese-first GitHub Pages guide for using Codex.
The web page is the canonical public artifact.

## Editing Rules

- Keep the guide useful for both beginners and advanced Codex users.
- Preserve exact English identifiers such as `Goal`, `subagent`, `AGENTS.md`,
  `refine-user-prompt`, `Compound Engineering`, `SKILL.md`, and command names.
- Keep generic Goal/Subagent guidance before scenario-specific skills.
- Keep the GPT-5.6 prompt-guidance interpretation grounded in the linked OpenAI
  source, and label `refine-user-prompt` as a third-party skill.
- Do not publish internal task process docs under `doc/`; they are local
  execution records.
- Do not make PDF generation part of the default completion contract unless the
  user explicitly asks for a PDF.

## Build And Verification

- Before claiming completion, verify:
  - `make check` passes for local HTML links, anchors, shared navigation, and
    required real-example coverage.
  - `index.html` contains the requested Chinese content and links.
  - Important anchors referenced by the sidebar exist.
  - GitHub Pages has been pushed and, when network access is available,
    the published page returns the updated HTML.

### Maintainer Commands

- `make generate` updates sentinel-owned root-page blocks and generated assets.
- `make check-fast` checks deterministic generation plus the manifest-scoped 20-page static contract.
- `make check` adds the Python unit suite.
- `make test-browser` runs Playwright interaction and responsive checks.
- `make check-release-local` runs local automated release gates; it does not satisfy human privacy or reader checks.
- `make check-published` is post-deployment and network-dependent. Record `not run` before deployment or when the public site is unavailable; never convert that state to pass.

### Generated And Authored Boundaries

- `data/site-manifest.json`, `data/changelog.json`, `data/heading-fragments.json`, and `data/publication-policy.json` are reviewed sources of truth.
- `assets/site-data.js`, `assets/search-index.js`, root-page `guide:*` blocks, canonical heading IDs, legacy alias elements, permalink controls, and normalized external-link attributes are generated. Change their source and run `make generate`; do not hand-edit them.
- Article prose, prompts, case evidence, captions, and narrowly scoped evidence sections outside generated blocks are authored content. Generator changes must preserve those bytes except for the explicitly registered narrow transformations above.
- Real Desktop screenshots remain an external-input gate. Do not create an approval record, claim privacy sign-off, or publish substitutes until the exact committed derivative has received independent original-resolution review.

## Documentation Boundaries

- `index.html` is the GitHub Pages guide and canonical public artifact.
- `README.md` is the repository landing page.
- `CONTEXT.md` is the domain glossary.
- `docs/adr/` stores durable documentation decisions.

## Path Index

Update this section manually or with the local goal-context tooling if project
structure changes materially.

<!-- goal-context:path-index:start -->
## Path Index

- Generated: 2026-07-11T13:00:09Z
- Max depth: 4
- Max items per section: 40

### Start Here

- `.` - requested target path
- `AGENTS.md` - agent instructions for this scope
- `README.md` - project overview and setup notes
- `Makefile` - project manifest or command/dependency entry
- `package.json` - project manifest or command/dependency entry

### AGENTS Files

- `AGENTS.md` - agent instructions for this scope

### Workspace Units

- `.` - workspace unit containing Makefile

### Commands And Manifests

- `Makefile` - project manifest or command/dependency entry
- `package.json` - project manifest or command/dependency entry

### Source Roots

- `.` - contains source/config files
- `assets` - contains source/config files
- `scripts` - contains source/config files
- `tests` - contains source/config files
- `tests/browser` - contains source/config files

### Tests

- `tests` - test directory
- `tests/test_build_site.py` - test file
- `tests/test_check_site.py` - test file
- `tests/test_published_site.py` - test file
- `tests/browser/toolbook.spec.js` - test file

### Docs

- `README.md` - project overview and setup notes
- `doc` - harness task workspace and durable task notes
- `doc/findings.md` - harness task workspace and durable task notes
- `doc/lessons.md` - harness task workspace and durable task notes
- `doc/progress.md` - harness task workspace and durable task notes
- `doc/task_issue.md` - harness task workspace and durable task notes
- `doc/task_plan.md` - harness task workspace and durable task notes
- `docs` - project documentation
- `docs/case-evidence-index.md` - project documentation
- `docs/adr` - project documentation
- `docs/adr/0001-dual-track-chinese-latex-guide.md` - project documentation
- `docs/ideation` - project documentation
- `docs/ideation/2026-07-10-codex-desktop-guide-effectiveness-ideation.html` - project documentation
- `docs/plans` - project documentation
- `docs/plans/2026-07-07-001-docs-high-stars-skills-repos-plan.md` - project documentation
- `docs/plans/2026-07-10-002-docs-evidence-task-loop-worktree-subagents-plan.md` - project documentation
- `docs/plans/2026-07-11-003-docs-guide-toolbook-upgrade-plan.md` - project documentation
- `docs/plans/2026-07-11-004-docs-guide-remaining-experience-gaps-plan.md` - project documentation
- `docs/reader-checks` - project documentation
- `docs/reader-checks/remaining-experience-script.md` - project documentation

### Task Docs

- `doc/task_plan.md` - required task process doc
- `doc/progress.md` - required task process doc
- `doc/findings.md` - required task process doc
- `doc/task_issue.md` - required task process doc
- `doc/lessons.md` - required task process doc

<!-- goal-context:path-index:end -->
