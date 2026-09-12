# 中文 Codex 实战手册

这是一个中文优先的 Codex Desktop GitHub Pages 实战手册，面向两类读者；[在线手册入口](https://whojay0609.github.io/codex-usage-guide/) 是公开阅读的 canonical 页面：

- 初学者：想知道如何在 Codex Desktop 里打开仓库、写清楚目标、审批操作并判断结果是否真的完成。
- 进阶用户：想系统使用 Goal、subagent、`AGENTS.md`、skills、MCP 和 Scheduled tasks（定时任务），并把 Codex 用成可验证的工程协作者。

## 按任务直达

不确定从哪页开始时，先按任务选择入口；链接直接落到对应页面的章节锚点。

| 你要做什么 | 直接入口 |
| --- | --- |
| 第一次安装、打开仓库并完成只读任务 | [安装到第一个任务](https://whojay0609.github.io/codex-usage-guide/install-desktop.html#安装到第一个任务) |
| 读代码、修测试、改文档或审查 diff | [日常任务的最小可靠闭环](https://whojay0609.github.io/codex-usage-guide/daily-workflow.html#日常任务的最小可靠闭环) |
| 拆分复杂工程任务并组织并行工作 | [从 Idea 到 task receipt](https://whojay0609.github.io/codex-usage-guide/engineering.html#从-idea-到-task-receipt) |
| 从研究问题走到可审查证据 | [从 Idea 到可审查证据](https://whojay0609.github.io/codex-usage-guide/research.html#从-idea-到可审查证据) |
| 写 Goal、使用 Subagents 或选择 Skills | [先选工作面，再写任务](https://whojay0609.github.io/codex-usage-guide/workflows.html#先选工作面-再写任务) |
| 使用 Git、Worktree、Hand off 或安全清理 | [保留 Local，创建 clean Worktree，再交付](https://whojay0609.github.io/codex-usage-guide/git.html#git-worktree-workflow) |
| 判断定时任务和无人值守是否合适 | [自动化前置条件](https://whojay0609.github.io/codex-usage-guide/automation.html#自动化前置条件) |
| 比较第三方 Skills、插件和辅助仓库 | [30 秒选择表](https://whojay0609.github.io/codex-usage-guide/skills-repositories.html#30-秒选择表) |

## 内容结构

网页已从单页指南改成多页面实战手册，结构按“任务主线优先，概念能力补充，插件和提示词实践单独说明”的顺序组织：

1. 任务页：`daily-workflow.html`、`desktop-cli.html`（Desktop 操作页，保留旧链接文件名）、`engineering.html`、`research.html`、`automation.html`、`workflows.html`。
2. 概念页：`codex.html`、`git.html`、`permissions.html`、`agents-md.html`、`skills.html`、`mcp.html`、`subagents.html`、`goal.html`。
3. Skills 仓库选择页：`skills-repositories.html`，先看 Codex CLI 生态 Top 10，再比较 Compound Engineering、`mattpocock/skills`、`academic-research-skills-codex`、ARIS、`leonxlnx/taste-skill`、`helloianneo/ian-xiaohei-illustrations` 和 `plexpt/awesome-chatgpt-prompts-zh` 的能力、安装路径、prompt 示例和边界。
4. 插件页：`compound-engineering.html`，说明 EveryInc Compound Engineering plugin 在 Codex Desktop 中的安装和使用方式。
5. 提示词页：`prompt-guidance.html`，解读 OpenAI GPT-5.6 prompting guidance，并介绍第三方 `refine-user-prompt` skill。
6. 资料页：`resources.html`，汇总 OpenAI 官方资料、开源仓库和本指南内部资料。

## 在线阅读与本地预览

公开入口：[whojay0609.github.io/codex-usage-guide](https://whojay0609.github.io/codex-usage-guide/)。源码仓库：[WhoJay0609/codex-usage-guide](https://github.com/WhoJay0609/codex-usage-guide)。

本项目是根目录发布的静态 HTML，不需要先安装前端依赖即可预览；本地预览需要 Python 3：

```bash
git clone https://github.com/WhoJay0609/codex-usage-guide.git
cd codex-usage-guide
python3 -m http.server 8000
```

然后打开 <http://127.0.0.1:8000/>。本次本地预览验证中，`GET /` 返回 HTTP 200，响应以 `<!doctype html>` 开头。提交修改前运行 `make check`；只检查生成产物和静态站点合同时可运行 `make check-fast`。

本次维护的最小验证结果：

```console
$ make check
Site check passed: 21 HTML pages, local links, anchors, and required sections are valid.
```

## 仓库文件

- `index.html`: GitHub Pages 静态网页指南入口。
- `assets/site.css`: 全站共享视觉样式。
- `assets/site.js`: 全站共享搜索、复制、主题、导航和 Mermaid 渐进增强。
- `assets/theme.js`: 在共享 CSS 前应用有限的主题偏好，避免错误主题首屏闪烁。
- `data/site-manifest.json`: 21 个公开根页面、导航、描述、发布 URL 和逐页资料依据的唯一清单。
- `data/changelog.json`: 首页“最近更新”和完整更新记录的唯一数据源。
- `data/heading-fragments.json`: canonical 标题 fragment 与 legacy alias 的受审映射。
- `data/publication-policy.json`: 公开搜索语料的排除项、敏感内容规则和本地发布边界（`doc/` 不进入公开页面链接）。
- `scripts/check_site.py`: 发布前静态检查，覆盖 HTML 页面、站内链接、锚点、关键章节、公开边界和搜索索引覆盖。
- `*.html`: 多页面指南，每页可直接通过 GitHub Pages 访问。
- `skills-repositories.html`: Codex 相关高 stars 开源仓库选择页，包含 skills、MCP、其他辅助工具、第三方仓库边界和可复制 Codex Desktop prompts。
- `figures/*.mmd`: Mermaid 流程图源文件，可在 GitHub 上预览。
- `figures/*.md`: Mermaid 图的 Markdown 包装文件。
- `figures/*.png`: 已渲染图，用于网页展示。
- `.nojekyll`: 让 GitHub Pages 原样发布静态文件。
- `CONTEXT.md`: 指南术语表。
- `docs/adr/0001-dual-track-chinese-latex-guide.md`: 文档结构和受众决策。
- `AGENTS.md`: 给 Codex/agent 使用的仓库工作规则。

## 插件、第三方 skills 与辅助工具备注

指南中提到的部分 skills 是插件或第三方扩展，不等同于 OpenAI 官方内置功能。发布或迁移到其它机器时，请以对应仓库、`SKILL.md` 或插件页面为准。

当前单独说明的扩展：

- `compound-engineering`: https://github.com/EveryInc/compound-engineering-plugin
- `mattpocock/skills`（Codex 的安装路径和 plugin 状态以其当前 README 与 `skills.sh` 页面为准）: https://github.com/mattpocock/skills
- `academic-research-skills-codex`: https://github.com/Imbad0202/academic-research-skills-codex
- `ARIS`: https://github.com/wanshuiyin/auto-claude-code-research-in-sleep
- `awesome-chatgpt-prompts-zh`: https://github.com/plexpt/awesome-chatgpt-prompts-zh
- `refine-user-prompt`: 基于 GPT-5.6 prompting guidance 的第三方 skill：https://github.com/WhoJay0609/refine-user-prompt

## 范围、边界与反馈

本仓库只维护中文优先的 Codex Desktop 实战指南；它不是 OpenAI 官方文档，也不是 Codex API、CLI 或第三方扩展的完整参考。产品行为和第三方仓库会变化，遇到版本差异时以页面列出的官方资料、上游 README 或 `SKILL.md` 为准。指南列出的 skills、plugins 和辅助工具不自动获得官方背书或兼容性保证。

发现失效链接、错误锚点、事实更新或读者卡点时，请提交 [Issue](https://github.com/WhoJay0609/codex-usage-guide/issues)，附上页面 URL、fragment、当前行为和期望行为。贡献页面内容前先读 [`AGENTS.md`](AGENTS.md)；不要把本地任务记录、个人凭据或未经脱敏的 Desktop 截图放进公开内容。

## 维护者与 Agent 快速入口

- 公开主入口是 [`index.html`](index.html)；页面清单、导航和资料依据以 [`data/site-manifest.json`](data/site-manifest.json) 为准。
- 文章正文和案例是 authored content；共享导航、标题 fragment、元数据和搜索资产由生成器维护。修改生成内容时运行 `make generate`，不要手改 `guide:*` sentinel 块。
- 最小回归命令是 `make check`。部署后再运行 `make check-published`；部署前或公网不可用时记录为 `not run`。

## 发布建议

GitHub Pages 使用仓库根目录发布，`index.html` 是公开指南主入口。站点采用普通静态 HTML/CSS/JS，不需要构建步骤。`data/site-manifest.json` 列出公开根页面；`doc/` 只保存本地执行记录，不能从公开页面链接进入，也不要把它发布为主内容。

发布前先运行：

```bash
make check
```

只检查生成产物和静态站点合同时运行：

```bash
make check-fast
```

需要本地浏览器回归时运行 `make test-browser`；部署完成后再运行 `make check-published`。后者会联网读取 manifest 中的全部 21 个公开页面和关键资产；部署前或网络不可用时必须记录为 `not run`，不能写成通过。

生成边界：`scripts/build_site.py` 只负责带 `guide:*` sentinel 的共享块、标题 fragment/alias、共享数据资产和受控属性归一化。正文、案例、prompt 与截图说明仍是 authored content；不要手改 sentinel 内代码，也不要让生成器用整页模板覆盖正文。真实 Desktop 截图只有在原分辨率脱敏复核完成后才能发布；当前缺失截图不得用 mock 代替。

这个检查会确认根目录 HTML 页面可解析、共享导航完整、站内链接和锚点存在，并且主要任务/资料页保留“真实实例”段落。需要 PDF 时再单独运行 `make pdf`。

`src/main.tex` 是独立维护的长文源，不会随 canonical HTML 页面或站点生成器自动同步。修改网页内容时不要假设 PDF 已同步；只有任务明确要求 PDF，并人工核对两套内容边界后，才运行 PDF 构建。

## 许可证

本项目采用 [MIT License](LICENSE)。
