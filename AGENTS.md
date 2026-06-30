# AGENTS.md

## Repository Purpose

This repository contains a Chinese-first GitHub Pages guide for using Codex.
The web page is the canonical public artifact.

## Editing Rules

- Keep the guide useful for both beginners and advanced Codex users.
- Preserve exact English identifiers such as `Goal`, `subagent`, `AGENTS.md`,
  `goal-entry`, `SKILL.md`, and command names.
- Keep generic Goal/Subagent guidance before scenario-specific skills.
- Keep local `goal-entry` implementation details only in the final mapping
  section of the guide.
- Do not publish internal task process docs under `doc/`; they are local
  execution records.
- Do not make PDF generation part of the default completion contract unless the
  user explicitly asks for a PDF.

## Build And Verification

- Before claiming completion, verify:
  - `index.html` contains the requested Chinese content and links.
  - Important anchors referenced by the sidebar exist.
  - GitHub Pages has been pushed and, when network access is available,
    the published page returns the updated HTML.

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

- Generated: 2026-06-30T11:14:38Z
- Max depth: 4
- Max items per section: 40

### Start Here

- `.` - requested target path
- `AGENTS.md` - agent instructions for this scope
- `README.md` - project overview and setup notes
- `Makefile` - project manifest or command/dependency entry

### AGENTS Files

- `AGENTS.md` - agent instructions for this scope

### Workspace Units

- `.` - workspace unit containing Makefile

### Commands And Manifests

- `Makefile` - project manifest or command/dependency entry

### Source Roots

- `assets` - contains source/config files

### Docs

- `README.md` - project overview and setup notes
- `doc` - harness task workspace and durable task notes
- `doc/findings.md` - harness task workspace and durable task notes
- `doc/lessons.md` - harness task workspace and durable task notes
- `doc/progress.md` - harness task workspace and durable task notes
- `doc/task_issue.md` - harness task workspace and durable task notes
- `doc/task_plan.md` - harness task workspace and durable task notes
- `docs` - project documentation
- `docs/adr` - project documentation
- `docs/adr/0001-dual-track-chinese-latex-guide.md` - project documentation

### Task Docs

- `doc/task_plan.md` - required task process doc
- `doc/progress.md` - required task process doc
- `doc/findings.md` - required task process doc
- `doc/task_issue.md` - required task process doc
- `doc/lessons.md` - required task process doc

<!-- goal-context:path-index:end -->
