# 每日修正 · 宏观日历月度补录

本目录存放该任务**每日独立修正块**，base 模板（prompt.md）保持不动。

## 用法
每天你给的修正，写成独立文件：`automation-1788963671627/YYYY-MM-DD.md`

示例（automation-1788963671627/2026-09-20.md）：
```markdown
## 每日修正 2026-09-20
- 农业/种植 由 P1 升 P2（连板确认）
- 贵金属/有色 维持回避
- 次日仓位上限由 7 成调到 6 成
```

并入方式：将当日修正追加进 `automations/automation-1788963671627/prompt.md` 的 `## 每日修正` 段（sync_to_db 前），再 git commit。
