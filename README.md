# Codex Usage Guide

中文优先的 Codex 使用指南仓库，面向两类读者：

- 初学者：想知道如何把任务交给 Codex、如何写清楚目标、如何判断结果是否真的完成。
- 进阶用户：想系统使用 Goal、subagent、`AGENTS.md`、本地 skills，并把 Codex 用成可验证的工程协作者。

## 内容结构

PDF 按“通用方法优先，场景 skills 其次，最后映射本机实现”的顺序组织：

1. Codex app 与本地工作区的基本工作模型。
2. Goal 怎么写，包括目标、范围、验收、验证、约束和停止条件。
3. Subagent 怎么用，包括拆分、输出合同、并行边界和整合责任。
4. `AGENTS.md` 怎么设置，让项目规则可复用。
5. 日常任务请求、权限判断和完成证据。
6. 零基础 quickstart 和 Mermaid 流程图，帮助读者先跑通最小闭环。
7. 工程场景下的 Matt Pocock skills 流程。
8. 学术场景下的 research skills 与 `research-pipeline` 全流程。
9. 最后一节说明本机 `goal-entry` 如何实现前面的通用模型，并链接独立公开仓库。

## 快速开始

构建 PDF：

```bash
make pdf
```

生成文件位于：

```text
build/codex-usage-guide.pdf
```

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

## 环境要求

构建依赖 XeLaTeX 和中文字体支持。当前 LaTeX 源使用：

- `ctexart`
- `Noto Serif CJK SC`
- `Noto Sans CJK SC`
- `Noto Sans Mono CJK SC`

在多数 TeX Live 环境中，需要安装 `ctex`、`fontspec`、`xeCJK` 和 Noto CJK 字体。

## 仓库文件

- `src/main.tex`: 主 LaTeX 文档。
- `figures/*.mmd`: Mermaid 流程图源文件，可在 GitHub 上预览。
- `figures/*.md`: Mermaid 图的 Markdown 包装文件。
- `figures/*.png`: 已渲染图，用于离线构建 PDF。
- `index.html`: GitHub Pages 静态网页指南入口。
- `.nojekyll`: 让 GitHub Pages 原样发布静态文件。
- `Makefile`: PDF 构建入口。
- `CONTEXT.md`: 指南术语表。
- `docs/adr/0001-dual-track-chinese-latex-guide.md`: 文档结构和受众决策。
- `AGENTS.md`: 给 Codex/agent 使用的仓库工作规则。

## 本机 skills 备注

指南中提到的部分 skills 是本机自写或本地维护扩展，不等同于 OpenAI 官方内置功能。发布或迁移到其它机器时，请以对应 `SKILL.md` 为准，并把不可复现的本机路径标成 local adaptation。

当前已单独公开的本机扩展示例：

- `goal-entry`: https://github.com/WhoJay0609/codex-goal-entry

## 发布建议

GitHub 仓库建议发布源文件，不提交 `build/` 目录。PDF 可以通过 GitHub Releases 或 CI artifact 发布。这样仓库保持轻量，读者仍然可以本地复现构建。
