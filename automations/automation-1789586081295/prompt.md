> **【模板版本钉死】`pinned-2026-09-20` — 本任务所有运行必须严格按此版本生成，禁止引用"最新"或未钉版本模板；模板规范见 REGISTRY.json 的 template_ref。改动须经 git commit 并 sync_to_db。

【模型约束 · 最高优先级（用户 2026-09-18 全局锁定·混元3付费）】本任务固定使用 AI 模型 `混元3 付费`。无论会话/调度层默认模型为何，执行本任务必须以 `混元3 付费` 运行；若运行实例并非混元3 付费，须提示用户到 UI/调度层手动指定 `混元3 付费`，不得以其他模型（含混元4/Hy4）替跑。此约束覆盖本 prompt 内一切其他指令。
运行每日查漏脚本，把已发布到 GitHub Pages（Jungle1499.github.io）但漏加进报告中心 center.html 的「当日与前一日」报告卡片自动补齐。\n\n执行命令（用绝对路径，managed python）：\n/Users/jungle1499/.workbuddy/binaries/python/versions/3.13.12/bin/python3 /Users/jungle1499/WorkBuddy/_report_hub/gap_check.py --apply\n\n运行后必须如实汇报：①扫描到几个候选、几个漏项；②按同日期+标题去重跳过了几个重复旧文件；③实际新增几张卡；④L2 验证结果（新卡是否全部在位、center.html 卡片总数）。\n\n脚本已内置：仓库文件 vs 中心卡片差集检测、标题归一化去重（避免 pankx/dp1000 这类旧命名重复卡）、PUT 前实时取 sha + 409 重试（防多自动化并发写竞态）、结构化断言与 L2 验证。\n\n若脚本报错、网络超时、或 L2 验证「新卡全部在位=False」，必须如实报告具体错误，绝对不要声称"已补齐/成功"。如 dry-run（不加 --apply）显示无漏项，也如实说明"今日无漏项"。\n\n注意：令牌在 /Users/jungle1499/.workbuddy/.gh_token，脚本内已读取，禁止打印或写进任何产出文件。

## 每日修正
<!-- 每日修正独立成块追加于此；base 结构保持不动 -->
