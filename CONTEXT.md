# Context

## Glossary

- **Codex**: the coding agent used through the local workspace to read files, edit code, run commands, and report verified outcomes.
- **Codex App**: the desktop Codex surface used for parallel threads, project work, review, local terminal actions, worktrees, automations, skills, plugins, and browser/computer-use workflows.
- **Workspace**: the filesystem scope shared by the user and Codex for a task.
- **Repository**: a Git-controlled project directory with its own source, docs, task rules, and verification surface.
- **Guide Reader**: a person using this guide to operate Codex. The guide supports both beginner readers and advanced automation or Agent developers.
- **Beginner Track**: the path that explains basic Codex usage, task phrasing, file changes, command execution, and verification.
- **Beginner Quickstart Loop**: the smallest reliable Codex loop for zero-background users: open project, write a four-part request, let Codex read context, execute narrowly, verify, and review evidence.
- **Advanced Track**: the path that emphasizes Goal design, subagent delegation contracts, `AGENTS.md` reuse, skills, and evidence-based closeout.
- **GitHub Publication Boundary**: the repository stance that source files and documentation are published while generated build artifacts are ignored or released separately.
- **Web-First Guide**: the current publication stance that `index.html` on GitHub Pages is the canonical public guide, while PDF generation is not part of the default workflow.
- **Engineering Advanced Track**: the path grounded in the Matt Pocock skills flow: `ask-matt`, `grill-me`, `grill-with-docs`, `to-prd`, `to-issues`, `implement`, and review.
- **Academic Automation Track**: the path grounded in installed research skills: `academic-research-suite`, `ask-research`, and `research-grill-me`.
- **Skill**: a local instruction package with a `SKILL.md` entry point that changes how Codex should approach a class of tasks.
- **AGENTS.md**: repository or directory-level operating rules that Codex must read and obey when working in that scope.
- **Instruction Chain**: the ordered set of global, project, and nested instruction files Codex reads before work; nearer path-level files override broader guidance.
- **Subagent Mode**: delegation mode where isolated agents receive narrow task context, scoped write boundaries, expected outputs, and later integration by the main thread.
- **Goal Mode**: generic goal-bound workflow with readiness checks, context resolution, delegation contracts, artifact tracking, validation, and closeout.
- **Goal Objective**: the compact execution contract passed to goal creation; it must include scope, success criteria, acceptance criteria, constraints, validation, artifacts, and stop conditions.
- **General Guidance Front Half**: the report structure that places reusable Codex work-model, Goal, subagent, `AGENTS.md`, and validation guidance before scenario-specific skill chapters.
- **Scenario Skills Chapters**: the later report chapters that explain how engineering and academic skills apply after the generic method is understood.
- **Local Goal Implementation Mapping**: the final report section that maps the generic Goal/Subagent model to the installed `goal-entry` router and its child skills.
- **Standalone Goal Entry Repository**: the public `codex-goal-entry` repository that packages `goal-entry`, its resolver, architecture note, and standalone validator.
- **Self-Written Skill Note**: the explicit warning that some mentioned skills are local, self-written, or locally maintained extensions rather than OpenAI official built-ins.
- **Mermaid Figure Source**: the `figures/*.mmd` source files used to create visual flow diagrams for GitHub preview and web rendering.
- **Matt Pocock Skills Flow**: engineering flow for idea sharpening, PRD/issue decomposition, implementation, and review.
- **Research Pipeline**: end-to-end academic automation skill family for idea discovery, implementation, experiment deployment, auto-review-loop, narrative handoff, and optional paper writing.
- **Research Dossier**: durable research-state document maintained by research workflows such as `research-grill-me`.
- **Approval**: a user decision that permits an operation outside the current sandbox or normal write boundary.
- **Verification**: the concrete checks Codex runs or reports before declaring a task complete.
