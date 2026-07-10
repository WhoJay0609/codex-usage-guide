# 0001: Dual-Track Chinese LaTeX Guide

## Status

Accepted

## Context

The guide must serve two reader groups selected during the initial grilling flow:

- general beginner users who need a practical entry point;
- advanced automation and Agent developers who need rules for skills, MCP tools, permissions, and workflow design.

The requested artifact is a LaTeX usage guide, and the surrounding workflow is Chinese-first. The repository should also be publishable as a GitHub usage-guide project, not just as a private generated PDF.

## Decision

Write the guide as a Chinese-first LaTeX document with general material first
and scenario-specific skills later:

1. General Front Half: Codex work model, Goal objective writing, subagent usage, Goal/Subagent combination patterns, `AGENTS.md`, task phrasing, permissions, and verification.
2. Engineering Scenario Track: mainly grounded in the installed Matt Pocock skills flow behind `ask-matt`, `grill-me`, and `grill-with-docs`.
3. Academic Scenario Track: grounded in installed research skills such as `academic-research-suite`, `ask-research`, and `research-grill-me`.
4. Extension Track: explain portable plugins such as Compound Engineering separately from self-developed local adaptations.
5. Local Goal Implementation Track: keep `goal-entry` as a clearly labeled self-developed, average-effectiveness local experiment only after the generic Goal/Subagent concepts are established.
5. Official Context: include Codex app background from official OpenAI documentation.
6. Beginner Visual Aids: include Mermaid source files and rendered figures so zero-background readers can see the Codex task loop and the Goal/Subagent lifecycle before reading detailed prose.
7. Local Skill Boundary: explicitly note which mentioned skills are local, self-written, or locally maintained extensions rather than OpenAI official built-ins.
8. GitHub Publication Boundary: make `README.md` the landing page, keep LaTeX source canonical, ignore local task-process docs, and publish generated PDFs through releases or CI artifacts rather than committing build output.

Keep exact English identifiers for commands, file names, tool names, API names, and skill names.

## Consequences

- General readers can stop after the first half with reusable Goal/Subagent/AGENTS guidance.
- Engineering readers get a maintainable reference for the Matt Pocock-style flow.
- Research readers get a maintainable reference for local academic automation skills.
- Advanced readers can distinguish ordinary subagent delegation from goal-bound harness work.
- Project maintainers get a concrete `AGENTS.md` template instead of generic advice.
- GitHub readers can understand audience, contents, build command, and artifact policy from the repository landing page.
- Beginner readers get a diagram-assisted quickstart before the heavier Goal/Subagent material.
- Mermaid sources remain editable and reviewable while checked-in PNG renders keep the PDF build reproducible without requiring Mermaid CLI.
- The guide needs periodic refresh because Codex tools, local skills, and MCP surfaces can change.
