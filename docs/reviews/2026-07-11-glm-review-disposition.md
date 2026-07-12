# GLM 网页审阅问题处置矩阵

日期：2026-07-12

状态含义：`fix` 已在本轮落实；`partial` 已解决高风险部分但仍有后续空间；`no-change` 经核验不按报告建议修改；`defer` 不属于本轮 P0/P1 范围或需要独立重构。这里记录的是处置结论，不以“未发现问题”替代验证；最终构建与站点检查由主执行线程统一完成。

## 术语与命名（T1–T8）

| ID | 状态 | 证据 / 理由 |
|---|---|---|
| T1 | fix | `automation.html`、`index.html`、`codex.html`、`desktop-cli.html`、`workflows.html`、`resources.html`、`README.md`、`data/site-manifest.json` 统一使用 Scheduled tasks（定时任务）与 Scheduled 视图；`scripts/check_site.py` 拒绝旧产品名。官方 URL 中 `/automations` 保留。 |
| T2 | fix | `skills.html`、`skills-repositories.html`、`goal-entry.html` 的通用 skill 示例使用 `$skill-name`；静态合同拒绝可见 `[$skill-name]`。 |
| T3 | fix | `index.html`、`codex.html` 澄清本指南的“Codex Desktop”是 ChatGPT desktop app 中 Codex 工作面的简称。 |
| T4 | no-change | Browser 的共享视图、视觉评论和页面交互是官方能力；`codex.html` 与 `desktop-cli.html` 保留该能力并收紧描述，不按“只能由 Codex 调用、不能评论”改写。 |
| T5 | no-change | Integrated terminal 是当前官方功能名；保留英文 UI 名，并在首页首次出现处补“集成终端”中文释义。 |
| T6 | fix | `data/site-manifest.json` 将 Scheduled tasks、Compound Engineering plugin、Skills 仓库等标题与页面主标题方向对齐；生成块由 `make generate` 统一刷新。 |
| T7 | fix | `resources.html` 增加 sandbox、approval、worktree、receipt、closeout、checkpoint、diff、commit、push、merge、PR、CI、Objective、Scope、Acceptance、Validation、prompt ladder、grant、disposition、lane 对照表。 |
| T8 | partial | 首页高频入口已用中文内联简释，术语表规定“中文首次解释、英文保留给 UI/命令”；全站历史案例的中英措辞不做批量文风重写。 |

## 技术准确性（A1–A15）

| ID | 状态 | 证据 / 理由 |
|---|---|---|
| A1 | fix | `permissions.html` 按 Ask for approval、Approve for me / Auto-review、Full access、Custom (config.toml) 四种 Desktop 选择重写，并把 sandbox / approval 作为底层概念解释。`dangerously-bypass-approvals-and-sandbox` 作为仍有效的兼容别名不删除，但不作为推荐入口。 |
| A2 | fix | `skills-repositories.html` 明确 Desktop 首选 Plugins / Marketplace；`npx`、Python skill-installer、shell installer 均标为 Codex CLI / 本地文件系统路径，且不会自动出现在未安装插件面板。 |
| A3 | fix | `agents-md.html` 已补全全局层、项目层、override、`CODEX_HOME`、大小限制与 fallback 配置边界。 |
| A4 | fix | `subagents.html` 已补显式上下文传递、窄写域、父任务整合与安全限制。 |
| A5 | fix | `goal.html` 将六字段模板明确标为本指南推荐提示词结构，并补原生 Goal 执行状态与进度行为。 |
| A6 | fix | `mcp.html` 已补 Model Context Protocol 全称、CLI / Desktop 配置路径、tools 与 resources 区分及 prompt injection / secret 风险。 |
| A7 | fix | `automation.html` 与 `compound-engineering.html` 明令禁止无人值守 Scheduled tasks 运行 `/lfg` 或自动 commit / push / PR / 修 CI 的 skill，并要求 protected branch、最小权限、人工 review / merge。 |
| A8 | fix | `engineering.html` 与 `index.html` 明确 grant 是提示词层面的授权约定，不是 Codex 权限机制。报告中重复出现的两条 A8 合并处置。 |
| A9 | partial | 各页提供 `facts_verified` 日期并以 Changelog 为时效入口；不硬编码无法稳定核验、且可能快速变化的客户端版本号。 |
| A10 | fix | `worktrees.html` 已将 Handoff / Create branch 写成按实际版本核对的操作，并说明 Local / Worktree 状态与交接边界。 |
| A11 | fix | `resources.html` 改用已确认的 `https://learn.chatgpt.com/docs/...` canonical 链接。 |
| A12 | fix | `engineering.html` 已说明 CE 命令需要先安装 Compound Engineering plugin，并链接安装页。 |
| A13 | fix | `engineering.html` 已将独立 reviewer 限定为辅助视角，关键变更仍需人类审查。 |
| A14 | fix | `skills-repositories.html` 给出 ARS 的完整 skill-installer 命令，并明确是 Codex CLI / 本地文件系统安装路径。 |
| A15 | partial | `compound-engineering.html` 覆盖核心七步与常见额外命令，并指向上游仓库；不复制可能快速漂移的近 20 项完整清单。 |

## 概念边界（C1–C4）

| ID | 状态 | 证据 / 理由 |
|---|---|---|
| C1 | fix | `index.html` 显著区分原生 Goal / Subagent / Worktree / MCP / AGENTS.md / Skills / Scheduled tasks / Browser 与指南推荐 receipt / grant / A2-A4 / 五阶段 / prompt ladder / claim ledger / 六字段 Goal 模板。 |
| C2 | fix | `engineering.html` 把 A2/A3/A4 解释为用户、编排线程、执行线程的教学映射，不暗示三个同权原生角色。 |
| C3 | fix | `workflows.html` 明示 receipt 是本指南推荐的任务收口实践，不是原生 UI。 |
| C4 | fix | `daily-workflow.html` 的 closeout 与 `workflows.html` receipt 统一为 changed scope、behavior_changed、validation evidence、risk-or-blocker、next step。 |

## 阅读体验与内容（R1–R16）

| ID | 状态 | 证据 / 理由 |
|---|---|---|
| R1 | fix | `install-desktop.html` 已补下载、平台/系统要求、登录、首次打开、Codex 工作面与第一个只读任务步骤。 |
| R2 | partial | `index.html` 强化路线入口与原生/推荐边界；本轮不进行与报告无关的首页整页重设计。 |
| R3 | partial | `data/site-manifest.json` 继续作为统一导航源，首页路线按同一任务主线组织；不新增导航层级重构。 |
| R4 | partial | 首页明确零基础、日常、进阶入口；不对每个历史章节逐一增加读者 badge。 |
| R5 | fix | `index.html` 的 30 秒入口为 Browser、Integrated terminal、diff、Goal、subagent、skills、validation、closeout、worktree 增加中文内联简释。 |
| R6 | defer | 全站“真实实例”批量替换需要逐案例证据重建，属于 wholesale 案例重写，低于本轮 P0/P1，另立内容项目处理。 |
| R7 | partial | 通过概念页交叉引用与任务页边界减少重复；不做全站大规模合并。 |
| R8 | fix | `resources.html` 新增统一术语对照，首页高频概念首次出现加中文释义。 |
| R9 | fix | 生成器按 manifest 导航组生成“首页 / 分组 / 当前页”三级面包屑，无需逐页维护。 |
| R10 | partial | `automation.html` 三个提示词标题中文化；全站所有代码块补语言 class 需要生成器级迁移，另行处理。 |
| R11 | fix | `automation.html` 补 Desktop / Web 的 Scheduled 入口、工作描述、schedule/cadence、上下文、Local/worktree、模型/推理、sandbox、普通任务预跑、前几次运行审查及 Scheduled 视图。 |
| R12 | fix | `goal.html` 已提供最小 Goal 起步版本与完整推荐模板的层次。 |
| R13 | fix | `resources.html` 增加 app、Permissions、Scheduled tasks、Browser、Integrated terminal、Skills & Plugins、AGENTS、Subagents、MCP、Worktrees、CLI、IDE、Cloud、Changelog、Record & Replay。未确认 canonical 路径不加入。 |
| R14 | fix | `index.html` 主标题修为“从一个可验证的小任务开始使用 Codex”。 |
| R15 | partial | 共享页脚继续由当前页面结构管理；不做与准确性无关的全站视觉统一。 |
| R16 | fix | `data/site-manifest.json` 将本轮相关页面更新与事实核验日期设为 2026-07-12；生成后同步到页面。 |

## 代码与工程质量（D1–D11）

| ID | 状态 | 证据 / 理由 |
|---|---|---|
| D1 | fix | `assets/site.css` 增加键盘导航组件注释，并删除经全仓引用检查确认未使用的 `.nav`、`.side-nav`、`.reveal-word` 规则。 |
| D2 | fix | 暗色模式重复变量已合并到共享选择器，相关样式检查由站点测试覆盖。 |
| D3 | defer | 全站 HTML 格式化会制造巨量无语义 diff，低于 P0/P1 且与本轮内容准确性无关，另行处理。 |
| D4 | fix | 页面首屏不再同步引入 `search-index.js`；首次打开搜索时按需加载，结果标题、章节和摘要使用安全 DOM `<mark>` 高亮。 |
| D5 | fix | `assets/site.js` 已统一 dialog focus trap 与 Escape 优先级，浏览器测试覆盖键盘路径。 |
| D6 | partial | favicon 已补齐并进入生成 metadata；skip-to-content 已处理。404、robots.txt、sitemap.xml 属于独立发布增强，未在本轮声称完成。 |
| D7 | defer | 三张图片批量转 WebP 需要视觉质量与引用迁移复核，低于本轮 P0/P1，另行处理。 |
| D8 | defer | `var` 到 `const` / `let` 的 wholesale JS 风格迁移不改变本轮产品准确性。 |
| D9 | no-change | `AGENTS.md` 明确 `doc/` 是本地执行记录且不作为公开主内容；`docs/` 存 durable 文档，两者用途不同，不构成冲突。 |
| D10 | fix | `README.md` 已说明 Web-first：HTML 是 canonical，PDF / LaTeX 不属于默认完成合同。 |
| D11 | partial | 轻微项逐项按风险处理；`lang="zh-CN"`、外链安全属性和页脚链接由生成/静态检查覆盖，IntersectionObserver 边界留给独立浏览器体验回归。 |

## 报告中的“重要功能遗漏”

| 功能 | 状态 | 证据 / 理由 |
|---|---|---|
| Codex Cloud | fix | `resources.html` 增加 Cloud canonical 入口；本指南仍以 Desktop 主线为主。 |
| IDE 扩展 | fix | `resources.html` 增加 IDE canonical 入口。 |
| 模型选择与推理强度 | fix | `automation.html` 的 Scheduled tasks 配置步骤与模板包含模型和推理强度。 |
| Plan 模式 | partial | 属于协作模式说明，暂不扩写为新章节；避免在未核对版本 UI 时给固定行为承诺。 |
| `/init` | defer | 未确认本轮 canonical 资料路径，不添加可能漂移的命令说明。 |
| `/review` | partial | 站点已有 review 工作流；内置命令的版本行为不在本轮扩写。 |
| `codex resume` | defer | CLI 会话恢复不属于 Desktop 主线，后续 CLI 专章处理。 |
| Record & Replay | fix | `resources.html` 增加 canonical 入口。 |
| Chronicle | defer | 未确认稳定 canonical 文档和当前可用范围，不臆造。 |
| Memories | defer | ChatGPT 通用能力与 Codex 项目上下文边界需单独核验，不在本轮混写。 |
| `config.toml` | fix | `permissions.html` 和相关概念页说明 Custom (config.toml)；MCP / skills 页面区分本地配置路径。 |
| `requirements.toml` 组织策略 | partial | 权限页说明组织策略可能限制模式；企业管理细节需依据组织文档另行扩展。 |
| Skill vs Plugin | fix | `skills.html`、`skills-repositories.html`、`index.html` 区分 skill mention、插件安装包和 Marketplace。 |
| Desktop skill 管理 | fix | `skills-repositories.html` 明确 Desktop 首选 Plugins / Marketplace，通用 skill 使用 `$` mention。 |
| `codex --search` | defer | CLI 可选参数不属于 Desktop 主线，且本轮不增加未核对路径。 |
| `codex --image` | defer | CLI 可选参数不属于 Desktop 主线，且本轮不增加未核对路径。 |

## 明确延期项

- 全站历史案例 wholesale 重写：需要逐案例重新建立来源与执行证据，另立内容审计任务。
- 图片 WebP 迁移：需要视觉质量、尺寸、缓存与引用回归，另立性能任务。
- 全 HTML 格式化：会产生大规模无语义 diff，应配合 formatter 与生成器契约单独实施。
