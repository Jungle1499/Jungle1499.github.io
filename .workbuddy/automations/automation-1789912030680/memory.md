# 自动化版本管理·每日漂移检测与自愈 — 执行记忆

## 2026-09-20 22:00 (触发自动化 automation-1789912030680)
- 漂移检测：`python3 scripts/check_drift.py` → 退出码 0，**0 漂移，全部一致**。
- REGISTRY 任务数=23，DB ACTIVE 数=23，两者对齐。
- 校验维度（脚本实际比对）：模型全 hy3 ✅ / 状态全 ACTIVE ✅ / prompt 文件 sha256 与 REGISTRY 记录一致 ✅ / prompt 文件 sha256 与 DB prompt 一致 ✅ / 模板钉死声明存在 ✅。
- 处置：未发现漂移 → 未触发 `sync_to_db.py --all`，**未推送飞书告警**（按规则避免打扰）。
- 注意：本任务只做"漂移检测+从文件自愈"，未改动 base 模板正文；模板版本升级需等用户明确指令。
