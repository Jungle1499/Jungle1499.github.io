# 自动化版本管理约定（CONVENTIONS）

> 本仓库是「自动化任务」的**单一事实源**。数据库 `workbuddy.db` 里的 prompt 只是**部署产物**。
> 所有改动从文件发起，经 git 留痕，再同步到 DB。不允许直接在 DB 里手改后不回写文件。

## 0. 核心铁律（不可违反）
1. **全部固定自动化模型 = `hy3`（混元3付费版）**。任何任务 `model_id != 'hy3'` 即漂移，check_drift 会报红。
2. **base 模板稳定**：每个任务的 `automations/<id>/prompt.md` 正文是稳定基线，**不每天改正文**。
3. **每日修正单独成块**：你每天发我的修正，落进 `corrections/<id>/YYYY-MM-DD.md`，再并入 prompt.md 的 `## 每日修正` 段（见下），base 结构不动。
4. **改必有痕**：每次改动 = 改文件 → `git commit` → `sync_to_db.py` →（可选）`git push`。
5. **每周打基线 tag**：`git tag baseline-YYYY-MM-DD`，日常碎改不盖掉稳定线。

## 1. 目录结构
```
automation_registry/
├── REGISTRY.json            # 任务元数据清单（模型/模板版本/规范引用/脚本/状态）
├── CONVENTIONS.md           # 本文件
├── automations/<id>/prompt.md   # 每个任务的「单一事实源」prompt（base 稳定）
├── templates/README.md      # 模板钉死机制说明（各报告类型对应哪个权威规范）
├── corrections/<id>/README.md   # 该任务每日修正存放处（独立块）
└── scripts/
    ├── check_drift.py       # 漂移检测：DB vs REGISTRY vs 文件
    ├── sync_to_db.py        # 文件 → DB（发布改动）
    └── sync_from_db.py      # DB → 文件（拉取线上真实状态比对）
```

## 2. 每日修正怎么存（不污染 base）
你每天发我的修正，按以下格式建文件：
```
corrections/<id>/2026-09-20.md
```
内容示例：
```markdown
## 每日修正 2026-09-20
- 农业/种植 由 P1 升 P2（连板确认）
- 贵金属/有色 维持回避
- 次日仓位上限由 7 成调到 6 成
```
并入 prompt.md：把当天修正**追加**进 prompt.md 末尾的 `## 每日修正` 段（若该段不存在则新建），不改动前面的 base 结构。

## 3. 模板钉死（防「停一天后面跑的不一样」）
- REGISTRY.json 里每个任务有 `template_version`（当前 `pinned-2026-09-20`）和 `template_ref`（指向权威规范/脚本）。
- prompt.md 头部有一行钉死声明（由 sync_to_db 注入），模型读到后**只按钉死版本生成**，禁止引用"最新"或未钉版本模板。
- 要升级模板：先在 templates/ 下确认新规范，改 `template_version` + `template_ref`，commit，再 sync。

## 4. 连续性断链守卫（补你这次的坑）
- 链首/链中任务跑前，检查「前一日同任务快照/送达文件」是否存在。
- 不存在 → 飞书摘要显式写 `N/A（前日未跑，链条断裂）` 并告警，绝不默默生成一篇"看起来正常但已脱轨"的报告。
- 修复后补跑，回填对应锚点文件，链条续上。

## 5. 日常操作速查
| 你想做的事 | 操作 |
|---|---|
| 看现在跑的是哪版 | `python3 scripts/check_drift.py` |
| 改某个任务的指令 | 编辑 `automations/<id>/prompt.md` → commit → `python3 scripts/sync_to_db.py <id>` |
| 每天发来的修正 | 写 `corrections/<id>/日期.md` → 并入 prompt.md `## 每日修正` → commit → sync |
| 拉线上真实状态比对 | `python3 scripts/sync_from_db.py`（仅写本地文件，不覆盖 DB） |
| 回滚到某基线 | `git checkout baseline-YYYY-MM-DD` → `sync_to_db.py --all` |
| 备份到 GitHub | `git remote add origin <url>`（一次性）→ 之后 `git push` |
