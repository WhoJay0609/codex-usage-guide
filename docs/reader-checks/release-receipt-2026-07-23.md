# 发布回执 · 2026-07-23

## Commit / URL

- Branch: `cursor/guide-gaps-implementation-0eec`
- 本地验证提交后填写公开 URL

## 自动化门

| 门 | 状态 | 说明 |
|---|---|---|
| `make check` | pass | 生成确定性、56 项 Python 单测、20 页静态契约 |
| `make test-browser` | pass | Playwright 搜索/复制/主题/响应式（部署前本地） |
| `make check-published` | fail | 2026-07-23 本地 push 后公开站尚未合并；build marker 与新增 fragment 不一致 |

## 读者检查（`docs/reader-checks/remaining-experience-script.md`）

| Reader | 查找秒数/状态 | Copy 状态 | Desktop 状态 | 备注 |
|---|---|---|---|---|
| R1 | not run | not run | not run (blocked: screenshot review pending) | 未招募代表性读者 |
| R2 | not run | not run | not run (blocked: screenshot review pending) | 未招募代表性读者 |
| R3 | not run | not run | not run (blocked: screenshot review pending) | 未招募代表性读者 |

- 查找门：`not run` — 需 3 位人工读者；自动化仅覆盖搜索控件存在性，不能替代 30 秒 median 门。
- Copy 门：`not run` — 需 3 位人工读者；Playwright 复制 smoke test 已通过，但不计入通过人数。
- Desktop 门：`not run (blocked: missing approved Desktop evidence)` — `data/screenshot-registry.json` 中五张截图均为 `pending_independent_review`，未完成独立原图隐私复核。

## 最终结论

- **blocked**
- Blocker：Desktop 截图独立复核、3 人读者研究、部署后 `make check-published`
- 解锁条件：原图级 privacy review 通过 → 更新 registry `review_status` → 跑读者脚本 → push 后 `make check-published`
