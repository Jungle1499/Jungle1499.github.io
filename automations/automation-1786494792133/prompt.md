【三阶段理论 v3.0 · 全局口径覆盖（2026-09-21 用户拍板·最高优先级，覆盖并废弃本 prompt 内一切旧三阶段写法；不影响周末/时间/幂等门控，门控照常优先）】
凡本任务涉及三阶段 / P1/P2/P3 阶段判定，一律按**三阶段理论 v3.0**（原 v4.17.0 状态机）执行，**两层结构**：
① **第一层·板块筛**：板块进全市场涨幅前三 → 列为 P1 候选（**只筛选，不定级**）。
② **第二层·Pair 定级**（阶段判定唯一依据）：板块内取龙头/补涨 Pair，按 v3.0 状态机判定 —— P1 触发 = 任一只当日涨幅 **≥5%**；确认走 **D0/D1/D2 三天观察窗四路径**，并按 D0~D2 累计涨幅最高者**定死 leader**；P2/P3 用**回溯前两日 2-of-3**（最快 T+1，允许中间插一天）；中断**仅 P1/P2 阶段且只看龙头单日跌 ≥6%**（补涨跌不算）；**P3 确认 = 持有**（非清仓），龙头开跌或双双跌才 W 结束；状态可回退（P3 中补涨强→回 P2，P2 中龙头强→回 P1）。
⚠️ 本 prompt 内原有的「连 2 天跑赢」「板块进涨幅前三 = P1 预警」「P3 确认即清仓」「7 状态」等旧口径一律作废，以本节为准。

> **【模板版本钉死】`pinned-2026-09-20` — 本任务所有运行必须严格按此版本生成，禁止引用"最新"或未钉版本模板；模板规范见 REGISTRY.json 的 template_ref。改动须经 git commit 并 sync_to_db。

【模型约束 · 最高优先级（用户 2026-09-18 全局锁定·混元3付费）】本任务固定使用 AI 模型 `混元3 付费`。无论会话/调度层默认模型为何，执行本任务必须以 `混元3 付费` 运行；若运行实例并非混元3 付费，须提示用户到 UI/调度层手动指定 `混元3 付费`，不得以其他模型（含混元4/Hy4）替跑。此约束覆盖本 prompt 内一切其他指令。
【GitHub Pages 部署·统一入口（最高优先级）】
- 统一托管 = GitHub Pages：仓库 `Jungle1499/Jungle1499.github.io`（main 分支），站点 `https://jungle1499.github.io/`。
- 报告中心：`https://jungle1499.github.io/center.html`。
- 部署（GitHub Contents API，不用 git push）：
  1) 文件名必须 ASCII 且不以 `_` 开头，命名如 `panqian-YYYYMMDD.html`；
  2) 令牌：`cat /Users/jungle1499/.workbuddy/.gh_token`（**不得打印、不得写进任何产出文件**）；
  3) 发布：先生成 base64 payload（更新已存在文件须先 GET 取 `sha` 并放进 payload），再 `curl -s -X PUT -H "Authorization: Bearer $(cat /Users/jungle1499/.workbuddy/.gh_token)" -H "Accept: application/vnd.github+json" --data-binary @/tmp/put.json "https://api.github.com/repos/Jungle1499/Jungle1499.github.io/contents/<文件名>"`；
  4) 发布后验证：`curl -sL -o /tmp/v.html -w '%{http_code}' https://jungle1499.github.io/<文件名>` 必须 200 且 grep 正文确认含报告真实标题关键词（curl 200 不算数）；首次 404 等 30 秒重试一次。
- 飞书链接口径（双链接，缺一不可）：① 🔗 单篇 `https://jungle1499.github.io/panqian-YYYYMMDD.html` ② 📂 报告中心 `https://jungle1499.github.io/center.html`。
- 部署失败降级：照发核心文字总结并注明「🔗 单篇待补发」，绝不发本地路径 / CloudStudio 沙箱 / workbuddy.link。

【板块覆盖·必加载】产出板块涨幅榜/概念排行/最强主线/方向表前，先加载 Skill(skill="sector-coverage-crosscheck")，走完三道强制门禁：①双分类独立取数（申万+同花顺概念走 westock data_sector ranking；同花顺行业指数881/884走 WebFetch q.10jqka.com.cn/thshy/detail/code/<code>/）；②差异扫描；③涨停股反向聚合。强度排序注明分类体系与代码。

【底层技能·必加载】执行任何分析/判断/生成前，先应用 pua-agent-enhancer：三红线质量门、压力升级 L0-L4、5-Why、资金/主力语境强制对抗自检。

# ⚠️ 周末零调用硬门控（最前）
先用 Bash 运行 `date +%u`（1=周一…7=周日）。若 6 或 7，立即输出"非交易日，跳过"并结束，不读数据、不部署、不推送。

【框架标准·复盘学习积累（必读）】生成前先读取 /Users/jungle1499/WorkBuddy/复盘学习积累.md（基线：框架 v2.8·报告 v3.3·随机基准命中率47.5%），把"已固化规则清单"应用到今日盘前判断。强制应用三阶段理论（P1/P2/P3/退潮）给全局与板块定档；退潮期方向表整体降权（多≤2~3 板块）。

【生成当日《盘前策略》网页，并发送到飞书个人账号】

【执行前置条件】（全满足才继续；否则结束，不生成不发送）
0. 时间说明：RRULE 每日约 07:00 触发（±10min 漂移照常执行）。数据基准严格 = T-1 收盘 + 隔夜外盘。
1. 交易日判断：westock 交易日历确认今天是否 A股 交易日；非交易日直接结束。
2. 幂等防重：检查 /Users/jungle1499/WorkBuddy/大盘复盘/ 是否已存在 panqian-YYYYMMDD.html（YYYYMMDD=今天）；已存在则结束。

【gold 基准（2026-09-14 用户指定对齐）】
- 权威参考来源（用户指定的对齐基准，已抓取干净 HTML 为模板）：`https://www.workbuddy.link/p/CaqbK72cAwzUGWD5kG4bNK`（标题「每日盘前策略 - 2026年9月14日」）。
- 本地 gold 模板：`/Users/jungle1499/WorkBuddy/大盘复盘/盘前策略_模板.html`（10 节卡片式版式，已存）。
- 结构规范：`/Users/jungle1499/WorkBuddy/大盘复盘/盘前策略_结构规范.md`（10 节逐列名+CSS+分析思路）。
- 生成前先 Read 模板 HTML + 结构规范，严格逐块对齐，仅换当日真实数据，不改版式、不增删分区、不改列名措辞、不更换配色。

【10 节固定顺序（缺一节即判失败）】
① 标题区（紫色渐变 header：📊 每日盘前策略 + 日期「YYYY年M月D日 · 周X · HH:MM 盘前」+ 🎵 song 金句）。
② 📌 核心摘要：5 个 summary-box（承接昨日交易日志 / 核心利好 / 两重压制 / 情绪周期定位 / 今日展望）+ 末尾关键词 tag。
③ 🔗 决策逻辑链：5 个 logic-item（①数据→分析 ②数据→分析 ③数据→分析 ④判断 ⑤行动）。
④ ⚡ 盘前30秒速览：key-value 表约 10 行（支撑压力/成交警戒/主力资金/美股/油价/美债/加息概率/解禁/仓位/事件日历）。
⑤ 🌍 隔夜外盘：单表（分类/品种/收盘/涨跌/解读）+ 末尾「📡 关键信号解读」box；取最近一个美股交易日收盘并标日期。
⑥ 📊 市场全景：3 子表（四大指数 / 涨跌分布 / 板块排行·主线轮动）+ 「主线轮动轨迹」box。
⑦ ⭐ 板块共识度与方向表：7 列固定 = 板块|评分|共识度|操作判断|建议仓位|核心策略|核心个股建议；评分 0~100 胶囊，共识度 极强/强/中/弱，操作判断内嵌 P2持有加仓/P1试错买入/回避；末尾「⚠️ 回避板块」box。板块条目由当日真实盘面扫描决定，严禁沿用旧列表当起点。
⑧ ⚠️ 风险点 + 催化日历 + 止盈止损纪律：3 盒 = risk-box（🚨风险点按重要性<ul>）+ calendar-box（📅催化日历<table>）+ discipline-box（🛡止盈止损纪律<ul>，含铁律A/B+个股止损锚）。
⑨ 📚 信源引用：单表（类型/信源/关键引用），覆盖 westock-data/盘前纪要/纪要研报中心/调研纪要/证券时报·CNBC·CME。
⑩ footer：生成说明+数据基准日+免责声明+版本号。

【分析思路（"这个思路"——必须按此产出）】
- 情绪周期定位：P0→P1冰点后修复 / P1试错 / P2持有加仓 / P3退潮 给全局与板块定档；退潮期方向表整体降权。
- 板块共识度评分表：每方向板块给 评分+共识度+操作判断+建议仓位%+核心策略+2~3 核心个股（带代码与逻辑）。
- 决策逻辑链：5 步 data→analysis→judgment→action，讲透"为什么是这条主线"。
- 政策催化驱动：国常会/产业验证（业绩/订单）/商品涨价（MLCC/光纤等）作为主线三重共振证据。
- 主线判定：优先算力硬件（光通信/CPO/PCB覆铜板/MLCC/光纤）+ 地缘窗口（油气/油运）+ 防御底仓（银行红利）；加息敏感型（半导体设备/医药/白酒）回避。
- 铁律A/B：占风险点清单第1、2条，数值用当日真实数据填充。

【数据采集（多源交叉，≥2 源一致才采用）】
- T-1 四大指数收盘+北证50+沪深300（价/涨跌幅/成交额/技术状态）：同花顺问财 → westock → 东财 → Wind 交叉。
- 市场广度 T-1：涨停/跌停/涨跌家数/涨跌比/成交额/主力净流入/北向估算。
- 板块双向榜单 T-1：涨幅TOP6 + 资金流入榜 + 流出/跌幅榜。
- 隔夜外盘：美股（道/标普/纳/费半+个股异动）、亚太、美债2Y/10Y、商品（WTI/布油）、COMEX黄金、美元指数；附信号解读。
- 催化日历：未来2周重点事件（CPI/PM/非农/FOMC/新品/行业大会）。
- 风险素材：铁律A/B状态、流动性、地缘尾部、个股止损锚、连板退潮、减持。
- R-Judge 双轨：预判层/修正层兑现率门槛（预判≥60%/修正≥85%）。

6. 生成 HTML：严格照搬模板 `盘前策略_模板.html` 的 CSS 与全部卡片结构，逐字一致、一模一样；仅替换当日真实数据。文件名 `panqian-YYYYMMDD.html`，保存到 /Users/jungle1499/WorkBuddy/大盘复盘/。

7. 部署：用上方 GitHub Pages 步骤部署，取得公开 URL；并更新 center.html（在 `<div id="list">` 后插入当日卡片：`<div class="day" data-day="YYYYMMDD">…<a class="r" href="https://jungle1499.github.io/panqian-YYYYMMDD.html"…>盘前策略 / 每日盘前策略 - YYYY年M月D日 / NN KB · panqian-YYYYMMDD.html</a>…</div>`，并 +1 总份数/日期数计数器），重部署 center.html。

8. 发飞书：lark-cli（PATH 含 /Users/jungle1499/.workbuddy/binaries/node/cli-connector-packages/bin 与 /Users/jungle1499/.workbuddy/binaries/node/versions/22.22.2/bin），命令 `lark-cli im +messages-send --as bot --user-id ou_fadb32ffb807b0080dfa6e5257305b3b --markdown '…核心文字总结 + 《核心看好标的追踪表》 + 🔗URL…' --idempotency-key panqian-YYYYMMDD`。摘要必须含核心文字总结（指数/情绪/量能+最强主线含阶段+催化+操作建议+风险）+《核心看好标的追踪表》+🔗URL，禁止只发标题+URL，无占位符。

8b. 同步结构化推荐：将本次核心看多标的与板块写成 JSON 覆盖写入 /Users/jungle1499/WorkBuddy/大盘复盘/jingjia_pipeline/preopen_reco.json（结构 {"date","sectors":[],"stocks":[{"name","code","stage","reason"}],"note"}）。

9. 任务输出末尾简要说明：基准日、数据交叉认证结果、云端 URL、飞书发送状态（message_id）、情绪周期定位与主线结论。

【硬性要求】
- 数据基准 = T-1 收盘 + 隔夜外盘，绝不用盘中实时价。
- 一天只跑一次（幂等门控）。
- 方向表必须 stage-aware：未做 P1/P2/P3/退潮 阶段判定不得给"多"。

【全局·预测-回测连续铁律】本任务方向/预判/标的必须纳入全天跨时点连续链。预测产出写入 /Users/jungle1499/WorkBuddy/其他复盘/预测快照_YYYYMMDD.md 的 `## 08:00 盘前策略` 段（字段：大势+板块Top N多空中性+主线），只追加自己段、不改他人段。

【全局·飞书推送铁律】每条飞书消息必须"带核心文字总结"，字段覆盖 ①指数/情绪/量能 ②最强主线(含阶段) ③关键变化/催化 ④进攻/回避/持有建议 ⑤核心风险；markdown 须同时含"🔗"与≥3 个总结关键词；禁止任何未替换占位符。

【全局·核心看好标的追踪表】飞书消息在核心文字总结之后、🔗 之前，必须追加《核心看好标的追踪表》（飞书 markdown，列：| 标的(名称+代码) | 阶段 | 推荐原因 | 近期走势 |，上限10只），并同步以 `### YYYY-MM-DD HH:MM 盘前策略` 小标题追加写入 /Users/jungle1499/WorkBuddy/标的推荐追踪表.md（只追加不覆盖）。

【🔒 发送防重复铁律】每交易日仅推送 1 次。lark-cli 必须含 `--idempotency-key panqian-$(date +%Y%m%d)`；发送前检查 /Users/jungle1499/WorkBuddy/大盘复盘/jingjia_pipeline/.panqian_sent_$(date +%Y%m%d) 是否存在，存在则跳过发送直接结束，不存在则发送成功后 touch。两道闸门任一缺失即判失败。

## 每日修正
<!-- 每日修正独立成块追加于此；base 结构保持不动 -->