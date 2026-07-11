# 案例证据索引

本文件只记录可以公开的脱敏主张。更细的授权与脱敏依据保存在本地非公开证据账本中，不进入 Git。

| Case ID | 页面锚点 | 类型 | 非敏感证据类别 | Review status | Freshness | Responsible role | 公开边界 |
|---|---|---|---|---|---|---|---|
| `team-delivery-composite` | `engineering.html#team-case` | 历史复合案例 | 仓库规则、Git 状态、测试、review、PR/合并记录 | 已复核 | 2026-07-11 | A3 维护，A2 批准发布 | 多个可核验片段组成，不声称一次连续执行 |
| `goal-composite-excerpt` | `goal.html#real-example` | 历史复合案例 | Goal 合同、验收与恢复记录 | 已复核 | 2026-07-11 | A3 | 只摘录 Goal 阶段并回链完整案例 |
| `context-composite-excerpt` | `agents-md.html#real-example` | 历史复合案例 | AGENTS、生成上下文、dirty 状态 | 已复核 | 2026-07-11 | A3 | 不发布源会话、路径、人员或机器信息 |
| `worktree-composite-excerpt` | `subagents.html#real-example` | 历史复合案例 | Worktree 登记、写域、验证与恢复 | 已复核 | 2026-07-11 | A3 | 只摘录两层隔离阶段并回链完整案例 |
| `compound-guide-pr-1` | `compound-engineering.html#real-example` | 历史案例 | 公开计划、提交、PR #1、站点检查 | 已复核 | 2026-07-11 | A3 | 实际默认分支为 `master` |
| `compound-guide-summary` | `skills-repositories.html#compound-case` | 历史案例 | 公开计划、Git、PR 与验证 | 已复核 | 2026-07-11 | A3 | 只主张需求到 PR/合并片段 |
| `matt-context-grill` | `skills-repositories.html#matt-case` | 历史案例 | 本地 Skill 使用、仓库规则与计划 | 已复核 | 2026-07-11 | A3 | 只支持上下文准备与需求澄清 |
| `academic-research-suite-demo` | `skills-repositories.html#ars-case` | 演示场景 | 上游公开说明 | 不需历史复核 | 2026-07-11 | A3 | 没有本项目执行证据 |
| `aris-sleep-research-demo` | `skills-repositories.html#aris-case` | 演示场景 | 上游公开说明 | 不需历史复核 | 2026-07-11 | A3 | 没有本项目执行证据 |
| `skills-page-delivery` | `skills-repositories.html#real-example` | 历史案例 | 公开计划、图片、检查、提交与 PR | 已复核 | 2026-07-11 | A3 维护，A2 批准发布 | 不包含忽略的过程记录 |

## 发布规则

- `historical` 显示为“历史案例”，`composite` 显示为“历史复合案例”，`demo` 显示为“演示场景”。
- 历史案例必须说明请求、角色或边界、证据类别、重要恢复和结果；摘录还必须链接到完整案例或规范流程。
- 新证据先进入本地账本，经独立脱敏复核后才能把状态改为“已复核”。
- 无法证明来源授权、案例类型或恢复过程时，一律降级为演示场景。
