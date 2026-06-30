# AGENTS.md

## Repository Purpose

This repository contains a Chinese-first LaTeX guide for using Codex. The guide
must work as a GitHub-publishable usage-guide repository and as a local PDF
source project.

## Editing Rules

- Keep the guide useful for both beginners and advanced Codex users.
- Preserve exact English identifiers such as `Goal`, `subagent`, `AGENTS.md`,
  `goal-entry`, `SKILL.md`, and command names.
- Keep generic Goal/Subagent guidance before scenario-specific skills.
- Keep local `goal-entry` implementation details only in the final mapping
  section of the guide.
- Do not publish internal task process docs under `doc/`; they are local
  execution records.

## Build And Verification

- Build with `make pdf`.
- The generated PDF is `build/codex-usage-guide.pdf`.
- Before claiming completion, verify:
  - `make pdf` succeeds.
  - CJK fonts in the PDF have Unicode maps, for example with `pdffonts`.
  - Chinese text can be extracted, for example with `pdftotext`.
  - Important section placement still matches the intended reading flow.

## Documentation Boundaries

- `README.md` is the GitHub landing page.
- `CONTEXT.md` is the domain glossary.
- `docs/adr/` stores durable documentation decisions.
- `src/main.tex` is the canonical guide content.

## Path Index

Update this section manually or with the local goal-context tooling if project
structure changes materially.
