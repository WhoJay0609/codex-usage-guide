# 中文 Codex 实战手册

中文优先的 Codex Desktop GitHub Pages 实战手册仓库，面向两类读者：

- 初学者：想知道如何在 Codex Desktop 里打开仓库、写清楚目标、审批操作并判断结果是否真的完成。
- 进阶用户：想系统使用 Goal、subagent、`AGENTS.md`、skills、MCP 和 Desktop Automations，并把 Codex 用成可验证的工程协作者。

## 内容结构

网页已经从单页指南改为多页面实战手册。结构按“任务主线优先，概念能力补充，插件和本机实验单独说明”的顺序组织：

1. 任务页：`daily-workflow.html`、`desktop-cli.html`（Desktop 操作页，保留旧链接文件名）、`engineering.html`、`research.html`、`automation.html`、`workflows.html`。
2. 概念页：`codex.html`、`permissions.html`、`agents-md.html`、`skills.html`、`mcp.html`、`subagents.html`、`goal.html`。
3. Skills 仓库选择页：`skills-repositories.html`，比较 Compound Engineering、`mattpocock/skills`、`academic-research-skills-codex` 和 ARIS 的能力、安装路径、prompt 示例和边界。
4. 插件页：`compound-engineering.html`，说明 EveryInc Compound Engineering plugin 在 Codex Desktop 中的安装和使用方式。
5. 本机实验页：`goal-entry.html`，说明自开发 `goal-entry` 的定位、限制和效果一般的现实边界。
6. 资料页：`resources.html`，汇总 OpenAI 官方资料、开源仓库和本指南内部资料。

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

Compound Engineering plugin：

```text
https://github.com/EveryInc/compound-engineering-plugin
```

高关注 skills 仓库选择页：

```text
skills-repositories.html
```

本机自开发 `goal-entry` 示例：

```text
https://github.com/WhoJay0609/codex-goal-entry
```

## 仓库文件

- `index.html`: GitHub Pages 静态网页指南入口。
- `assets/site.css`: 全站共享视觉样式。
- `assets/site.js`: 全站共享搜索、复制、主题、导航和 Mermaid 渐进增强。
- `assets/theme.js`: 在共享 CSS 前应用有限的主题偏好，避免错误主题首屏闪烁。
- `data/site-manifest.json`: 19 个公开根页面、导航、描述和发布 URL 的唯一清单。
- `data/heading-fragments.json`: canonical 标题 fragment 与 legacy alias 的受审映射。
- `data/publication-policy.json`: 公开搜索语料的排除项和敏感内容规则。
- `scripts/check_site.py`: 发布前静态检查，覆盖 HTML 页面、站内链接、锚点和关键章节。
- `*.html`: 多页面指南，每页可直接通过 GitHub Pages 访问。
- `skills-repositories.html`: 高关注 skills 仓库选择页，包含第三方仓库边界和可复制 Codex Desktop prompts。
- `figures/*.mmd`: Mermaid 流程图源文件，可在 GitHub 上预览。
- `figures/*.md`: Mermaid 图的 Markdown 包装文件。
- `figures/*.png`: 已渲染图，用于网页展示。
- `.nojekyll`: 让 GitHub Pages 原样发布静态文件。
- `CONTEXT.md`: 指南术语表。
- `docs/adr/0001-dual-track-chinese-latex-guide.md`: 文档结构和受众决策。
- `AGENTS.md`: 给 Codex/agent 使用的仓库工作规则。

## 插件与本机 skills 备注

指南中提到的部分 skills 是插件或本机自写扩展，不等同于 OpenAI 官方内置功能。发布或迁移到其它机器时，请以对应仓库、`SKILL.md` 或插件页面为准，并把不可复现的本机路径标成 local adaptation。

当前单独说明的扩展：

- `compound-engineering`: https://github.com/EveryInc/compound-engineering-plugin
- `mattpocock/skills`: https://github.com/mattpocock/skills
- `academic-research-skills-codex`: https://github.com/Imbad0202/academic-research-skills-codex
- `ARIS`: https://github.com/wanshuiyin/auto-claude-code-research-in-sleep
- `goal-entry`: 自己开发的本机实验，效果一般，仅作参考：https://github.com/WhoJay0609/codex-goal-entry

## 发布建议

GitHub Pages 使用仓库根目录发布，`index.html` 是公开指南主入口。站点采用普通静态 HTML/CSS/JS，不需要构建步骤。不要把生成目录或本地任务过程文档发布为主内容。

发布前先跑：

```bash
make check
```

只检查生成产物和静态站点合同时运行：

```bash
make check-fast
```

需要本地浏览器回归时运行 `make test-browser`；部署完成后再运行 `make check-published`。后者会联网读取 manifest 中的全部 19 个公开页面和关键资产；部署前或网络不可用时必须记录为 `not run`，不能写成通过。

生成边界：`scripts/build_site.py` 只负责带 `guide:*` sentinel 的共享块、标题 fragment/alias、共享数据资产和受控属性归一化。正文、案例、prompt 与截图说明仍是 authored content；不要手改 sentinel 内代码，也不要让生成器用整页模板覆盖正文。真实 Desktop 截图只有在原分辨率脱敏复核完成后才能发布；当前缺失截图不得用 mock 代替。

这个检查会确认根目录 HTML 页面可解析、共享导航完整、站内链接和锚点存在，并且主要任务/资料页保留“真实实例”段落。需要 PDF 时再单独运行 `make pdf`。
