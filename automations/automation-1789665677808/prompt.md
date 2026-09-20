> **【模板版本钉死】`pinned-2026-09-20` — 本任务所有运行必须严格按此版本生成，禁止引用"最新"或未钉版本模板；模板规范见 REGISTRY.json 的 template_ref。改动须经 git commit 并 sync_to_db。

【模型约束 · 最高优先级（用户 2026-09-18 全局锁定·混元3付费）】本任务固定使用 AI 模型 `混元3 付费`。无论会话/调度层默认模型为何，执行本任务必须以 `混元3 付费` 运行；若运行实例并非混元3 付费，须提示用户到 UI/调度层手动指定 `混元3 付费`，不得以其他模型（含混元4/Hy4）替跑。此约束覆盖本 prompt 内一切其他指令。

【GitHub Pages 部署·统一入口（2026-09-14 上线·最高优先级，覆盖并废弃旧 workbuddy.link 资料库写法）】
- **已废弃 workbuddy.link / space/d 内链**：2026-09-13 实测该体系被平台 Security Restriction 全外网封死。禁止再发 `workbuddy.link/p/*` 或 `www.workbuddy.cn/space/d/*` 链接；禁止再调用 import_publish.py / sync_center.py；禁止再取 op_ 令牌做资料库发布；禁止发 CloudStudio 沙箱链接、禁止发本地路径。本任务内一切旧「资料库/双链接/沙箱部署」写法一律作废，以本节为准。
- **统一托管 = GitHub Pages**（微信/飞书/浏览器免密直开）：
  - 仓库 `Jungle1499/Jungle1499.github.io`（main 分支），站点 `https://jungle1499.github.io/`
  - 单篇 `https://jungle1499.github.io/jingjia-bmom-YYYYMMDD.html`
  - 报告中心（带密码门 `fupan2026`）：`https://jungle1499.github.io/center.html`
  - **部署（GitHub Contents API，不用 git push）**：① 文件名必须 ASCII 且不以 `_` 开头（本任务用 `jingjia-bmom-YYYYMMDD.html`）；② 令牌 `cat /Users/jungle1499/.workbuddy/.gh_token`（600 权限；**不得打印、不得写进任何产出文件**）；③ python base64 payload，更新已存在文件须先 GET 取 `sha` 放进 payload，再 `curl -X PUT .../contents/<文件名>`；④ 部署后验证 `curl -sL -o /tmp/x.html -w '%{http_code}'` 必须 200 且 `grep` 正文含真实标题关键词（curl 200 不算数）；首次 404 等 30 秒重试。
  - 部署失败降级：照发核心文字总结并在消息注明「🔗 单篇待补发」，绝不发本地路径 / CloudStudio / workbuddy.link。
- **飞书链接口径（双链接，缺一不可）**：① 🔗 单篇（免密）`https://jungle1499.github.io/jingjia-bmom-YYYYMMDD.html` ② 📂 报告中心 `https://jungle1499.github.io/center.html`。

【集合竞价快报 · B-mom + 自适应门槛版 · 9:25 读取 / 9:27 发 · 并行于 gold V2.3.1】
与 gold 任务（`automation-1786988889646`）并行独立运行，本任务用 **B-mom 模板**渲染（`/Users/jungle1499/WorkBuddy/交易/jingjia_bmom/gen_bmom_jingjia.py`），每天发第二份竞价快报。绝不修改 gold、绝不共用目录/幂等键/晚间预判小节。

## B-mom 打分方法论（数据驱动）
- **质量分(0-4)** = c1 大盘站MA60 + c2 板块站MA60 + c3 板块动量>5% + c4 大盘放量>1.2。
- **自适应门槛**：大盘站上MA60 → 需质量分≥2；大盘跌破MA60 → 放宽到≥1。
- **仓位** = 情绪基准(好9/中5.5/差3成) × 质量分系数(4→1.0, 3→0.85, 2→0.70, 1→0.50, 0→0.00)。
- **信号分(满分10)** = 广度(0-3)/量能(0-2)/龙头(0-3)/相对强度(0-2)；量能(环比放量)盘前不可得 → 本表信号分为广度+龙头+相对之和（量能待开盘后回看）。
- **sret20** = 申万二级板块等权指数近20日涨幅（最强预测因子 r=+0.271）。
- **ETF 映射**：半导体→半导体ETF(sh512480)；元件/电子化学品Ⅱ→电子ETF(sh515260)；其余「无映射」。
- **选中板块** = 信号top5中「有ETF映射 且 sret20最高 且 质量分≥自适应门槛」者；若全不达标，hero 标「慎做多/不做的依据」。

## 数据源铁律
- **第一优先 westock**（腾讯自选股 MCP）：`data_market_overview` / `data_changedist` / `data_sector(mode=ranking)` / `data_kline`。降级链 westock→同花顺问财→东财→腾讯gtimg；缺失标 N/A，严禁编造。
- 板块成分股查询若失败，改用 ranking 的 `leader` 字段（真实龙头）作代表个股，不编造。

## ⚠️⚠️ 执行流程（2026-09-20 改造·保证 9:27 准时·最高优先级）
**超时根因**：旧流程在 agent 主循环里手算 6 板块 MA60/MA20/sret20（曾试错 3 次）+ 组装 + 生成HTML + 部署，单轮 >2 分钟 → 文字 9:33 才发。gold 之所以准点，是其 step1 是**确定性脚本**（`run_bmom_step1.py` 同构）直接 `subprocess` 推飞书、不进 agent 推理。本任务现对齐 gold：**发文字前的全部计算交给脚本，agent 不参与手算。**

1) **周末门控**（最前）：Bash `date +%u`，≥6（周六/日）→ 立即结束，零调用。
2) **09:25:05 对齐**：用 python `sleep` 到 09:25:05 再读冻结竞价数据（中证1000 等）。
3) **并行拉 westock 数据并落盘 raw JSON**（约 20-40s，机械转换无试错）：
   - `data_market_overview` → 指数（取中证1000 今开 + 65日kline）
   - `data_changedist` → 涨跌分布（高开>2%家数/涨停/跌停/上涨比%）
   - `data_sector(mode=ranking, limit≥30)` → 申万二级竞价高开榜（板块名/代码/平均高开%/高开家数/领涨股）
   - `data_kline` × 6 板块（玻璃玻纤pt01801712/贵金属pt01801053/其他电子Ⅱpt01801082/元件pt01801083/半导体pt01801081/电子化学品Ⅱpt01801086，各 65 日收盘）
   - 落盘为 **`/Users/jungle1499/WorkBuddy/交易/jingjia_bmom/data_raw_YYYYMMDD.json`**，结构严格对齐 `run_bmom_step1.py` 顶部 RAW_SCHEMA 注释：`{date, index:{zz1000_open, zz1000_kline[]}, changedist:{hi2,zt,dt,up_ratio}, sectors:[{name,code,avg_open,high_count,leader,open,kline[]}]}`。
4) **🔴 09:27 硬截止 · Bash 跑脚本发文字快报（禁止手算 MA）**：
   ```
   cd /Users/jungle1499/WorkBuddy/交易/jingjia_bmom
   /Users/jungle1499/.workbuddy/binaries/python/versions/3.13.12/bin/python3 run_bmom_step1.py \
     --raw data_raw_YYYYMMDD.json --date YYYYMMDD
   ```
   脚本自动：算 MA/质量分/门槛/仓位/信号分 → 组装 6 段文字 → `subprocess` 调 lark-cli 推送 → 落盘 `data_jingjia_YYYYMMDD.py`（供步骤5用）。**此步须在 09:27 前完成；若 09:26:50 前未返回，立即以降级文字（🔗 单篇待补发）推送后结束。**
5) **生成完整 HTML**（9:27 之后，不卡硬截止）：
   ```
   /Users/jungle1499/.workbuddy/binaries/python/versions/3.13.12/bin/python3 gen_bmom_jingjia.py \
     --data data_jingjia_YYYYMMDD.py --out _deploy_jingjia_YYYYMMDD_vBMOM/index.html
   ```
   （每天新建独立目录 `_deploy_jingjia_YYYYMMDD_vBMOM`，绝不复用旧目录）
6) **部署 + 校验 + 补发链接**：
   - 部署 `jingjia-bmom-YYYYMMDD.html` 到 GitHub Pages（PUT + base64，带 WKBUILD 标记），验证 200 + 正文标题关键词。
   - 报告中心 `center.html` 插入卡片（`<div class="day" data-day="YYYYMMDD">` 的 `.grid` 内），同步计数，PUT 回。
   - 补发飞书链接消息（双链接；幂等键 `vBMOM-link-YYYYMMDD`，**不与 gold 的 v24-link 撞键**）。
7) **写每日预测序列**：把当日竞价追加到 `/Users/jungle1499/WorkBuddy/其他复盘/晚间预判_YYYYMMDD.md` 的 `## 09:25 竞价快报（B-mom版）` 段（已存在则跳过）。

## 失败处理
若 9:27 前脚本未推送成功：立即发 `⚠️ 竞价快报(B-mom)失败/超时: <原因>` 到飞书后结束，绝不用 --file 发文件、绝不发 N/A 残废版报告。

## 模型未确认处理
若运行实例未显式暴露为「混元3 付费」，在交付说明中如实标注「模型未确认」，并提示用户手动指定，勿用其他模型替跑。

## 每日修正
<!-- 每日修正独立成块追加于此；base 结构保持不动 -->
