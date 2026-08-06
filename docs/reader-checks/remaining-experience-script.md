# 剩余体验读者检查脚本

本脚本记录产品发布门，不替代自动化检查。至少招募 3 位代表性读者：能阅读中文、使用过代码或研究资料，但不要求熟悉本指南。主持人只读题，不提示页面位置、搜索词改写或 Desktop 操作步骤。

## 前置条件

- 记录被测提交、站点 URL、日期、浏览器和设备宽度。
- 先运行 `make check` 和 `make test-browser`；未运行或失败要照实记录。
- Desktop 首任务只有在真实、已脱敏且已独立复核的截图齐备后执行。U3 证据缺失时，该项必须记为 `not run (blocked: missing approved Desktop evidence)`。
- 不收集账号、仓库名、本地路径、任务正文或屏幕录制；记录任务结果和用时即可。

## 每位读者的任务

1. **已知项查找：**“找到审批决策矩阵，并说明它位于哪个页面和章节。”从读题结束开始计时，到读者到达正确 fragment 停止。记录秒数、是否使用搜索、是否需要主持人提示。
2. **Prompt 复用：**在当前或相邻页面找到一个可复用 prompt，只使用页面复制控件放入临时空白文本框。核对首尾行和换行完整；随后立即清空文本框。记录成功、失败反馈是否真实、是否发生手工选择。
3. **第一个 Desktop 任务：**按安装/Desktop 路径完成一个预先准备的只读仓库任务；读者需要指出打开仓库、审批边界、diff/review 或浏览器反馈证据。主持人不得补充界面步骤。缺少任何已批准关键截图时不执行。

## 判定

- 已知项查找：3 人中位数不超过 30 秒，且无人依赖主持人定位。
- Prompt 复用：3 人均无需手工选中文字，复制内容完整，失败状态不虚报成功。
- Desktop 首任务：至少 2/3 人无需主持人界面指导完成，并能指出可观察验证证据。
- 任一任务只有 `pass`、`fail`、`not run` 三种状态；`not run` 必须附 blocker，不能计入通过人数。

## 记录表

| Reader | 查找秒数/状态 | Copy 状态 | Desktop 状态 | 主持人提示 | 观察备注 |
|---|---|---|---|---|---|
| R1 | not run | not run | not run (blocked: screenshot review pending) | — | 2026-07-23：五张 Desktop 截图待独立复核 |
| R2 | not run | not run | not run (blocked: screenshot review pending) | — | — |
| R3 | not run | not run | not run (blocked: screenshot review pending) | — | — |

## 发布回执

- Commit / URL：见 `docs/reader-checks/release-receipt-2026-07-23.md`
- 自动化门：`pass / fail / not run`（附命令与原因）
- 查找门：`not run`（需 3 人人工；Playwright 搜索 smoke 已通过但不计入）
- Copy 门：`not run`（需 3 人人工；Playwright 复制 smoke 已通过但不计入）
- Desktop 门：`not run (blocked: missing approved Desktop evidence)`（registry 五图均为 pending_independent_review）
- Published-site 门：`not run`（仅部署后运行）
- 最终结论：`blocked`
- Blocker 与解锁条件：独立原图复核 → 读者三项 → push 后 check-published
