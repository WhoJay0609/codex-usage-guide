# Codex Usage Guide

中文优先的 Codex GitHub Pages 使用指南仓库，面向两类读者：

- 初学者：想知道如何把任务交给 Codex、如何写清楚目标、如何判断结果是否真的完成。
- 进阶用户：想系统使用 Goal、subagent、`AGENTS.md`、本地 skills，并把 Codex 用成可验证的工程协作者。

## 内容结构

网页已经从单页指南改为多页面文档站。结构按“概念先行，任务后置，本机扩展单独说明”的顺序组织：

1. 概念页：`codex.html`、`permissions.html`、`agents-md.html`、`skills.html`、`mcp.html`、`subagents.html`、`goal.html`。
2. 任务页：`desktop-cli.html`、`daily-workflow.html`、`engineering.html`、`research.html`、`automation.html`、`workflows.html`。
3. 本机扩展页：`goal-entry.html`，说明本机 `goal-entry` 的架构、流程、目标能力和独立仓库链接。
4. 资料页：`resources.html`，汇总 OpenAI 官方资料、开源仓库和本指南内部资料。

## 快速开始

网页指南入口：

```text
index.html
```

如果 GitHub Pages 以仓库根目录发布，访问地址通常是：

```text
https://whojay0609.github.io/codex-usage-guide/
```

远程仓库：

```text
https://github.com/WhoJay0609/codex-usage-guide
```

`goal-entry` 独立仓库：

```text
https://github.com/WhoJay0609/codex-goal-entry
```

## 仓库文件

- `index.html`: GitHub Pages 静态网页指南入口。
- `assets/site.css`: 全站共享视觉样式。
- `assets/site.js`: 全站共享导航高亮和渐进式动画。
- `*.html`: 多页面指南，每页可直接通过 GitHub Pages 访问。
- `figures/*.mmd`: Mermaid 流程图源文件，可在 GitHub 上预览。
- `figures/*.md`: Mermaid 图的 Markdown 包装文件。
- `figures/*.png`: 已渲染图，用于网页展示。
- `.nojekyll`: 让 GitHub Pages 原样发布静态文件。
- `CONTEXT.md`: 指南术语表。
- `docs/adr/0001-dual-track-chinese-latex-guide.md`: 文档结构和受众决策。
- `AGENTS.md`: 给 Codex/agent 使用的仓库工作规则。

## 本机 skills 备注

指南中提到的部分 skills 是本机自写或本地维护扩展，不等同于 OpenAI 官方内置功能。发布或迁移到其它机器时，请以对应 `SKILL.md` 为准，并把不可复现的本机路径标成 local adaptation。

当前已单独公开的本机扩展示例：

- `goal-entry`: https://github.com/WhoJay0609/codex-goal-entry

## 发布建议

GitHub Pages 使用仓库根目录发布，`index.html` 是公开指南主入口。站点采用普通静态 HTML/CSS/JS，不需要构建步骤。不要把生成目录或本地任务过程文档发布为主内容。
