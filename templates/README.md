# 模板钉死机制（templates）

本目录记录「每种报告类型对应哪个权威规范」，让任务 prompt 永不漂移。
REGISTRY.json 中每个任务的 `template_ref` 指向下表中的规范/脚本。

## 报告类型 → 钉死规范映射
| 报告类型 | template_ref（权威源） | 正确生成脚本/入口 |
|---|---|---|
| 完整版复盘 / 完整复盘 / 预判版 | `新交易体系/报告结构规范.md` | `_report_hub/gen_20260917.py`（**六节正确版**，禁止用五节简版） |
| 深度复盘·跟随版 | `大盘复盘/每日深度复盘_V55_结构规范.md` | 跟随版专用生成器 |
| 主线分析 | `skills/zhuxian-gold-template/SKILL.md` | 主线分析生成器 |
| 盘前策略 | `skills/fupan-rules/SKILL.md` | 盘前生成器（新 gold 10节版） |
| 竞价快报 | `skills/fupan-rules/SKILL.md` + `大盘复盘/jingjia_pipeline/v23/run_live_v24.py` | 竞价 pipeline |
| 盘中速览 / 午盘 | `skills/fupan-rules/SKILL.md` | 盘中生成器 |
| 行业催化早报 | `skills/industry-panorama-research/SKILL.md` | 行业全景生成器 |
| 行业新闻日报 | `skills/fupan-rules/SKILL.md` | — |
| 各类回测（收盘/整体/周度） | `skills/fupan-rules/SKILL.md` | 回测生成器 |
| 潜伏主题扫描 | `skills/fupan-rules/SKILL.md` | Discovery Gate |
| 周末新闻搜集/回测 | `skills/us-china-tech-restriction-tracking/SKILL.md` | — |
| 宏观日历 | `skills/fupan-rules/SKILL.md` | — |
| 自愈看门狗 / 发布兜底 / 每日查漏 | 运维脚本（巡检/发布） | — |

## 钉死规则
1. `template_version` 当前统一为 `pinned-2026-09-20`。
2. **任何任务运行时只能引用上表钉死版本**，不得"自动用最新"。
3. 升级模板：先在对应规范里改定，再改本表 + REGISTRY 的 `template_version`，commit + sync。
4. 事故警示（2026-09-17）：曾误用 `gen_full_fupan_20260917.py` 五节简版顶"完整版"标题发出——
   根因就是**没钉死生成脚本**。钉死后 check_drift 会检测 prompt 是否声明了正确模板版本。
