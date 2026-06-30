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
