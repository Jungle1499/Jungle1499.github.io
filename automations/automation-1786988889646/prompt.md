> **【模板版本钉死】`pinned-2026-09-20` — 本任务所有运行必须严格按此版本生成，禁止引用"最新"或未钉版本模板；模板规范见 REGISTRY.json 的 template_ref。改动须经 git commit 并 sync_to_db。

【模型约束 · 最高优先级（用户 2026-09-18 全局锁定·混元3付费）】本任务固定使用 AI 模型 `混元3 付费`。无论会话/调度层默认模型为何，执行本任务必须以 `混元3 付费` 运行；若运行实例并非混元3 付费，须提示用户到 UI/调度层手动指定 `混元3 付费`，不得以其他模型（含混元4/Hy4）替跑。此约束覆盖本 prompt 内一切其他指令。

【GitHub Pages 部署·统一入口（2026-09-14 上线·最高优先级，覆盖并废弃旧 workbuddy.link 资料库写法）】
- **已废弃 workbuddy.link / space/d 内链**：2026-09-13 实测该体系被平台 Security Restriction 全外网封死（连飞书都打不开）。**禁止再发 `workbuddy.link/p/*` 或 `www.workbuddy.cn/space/d/*` 链接；禁止再调用 import_publish.py / sync_center.py；禁止再取 op_ 令牌做资料库发布；禁止发 CloudStudio 沙箱链接、禁止发本地路径**。本任务内一切旧「资料库/双链接/沙箱部署」写法一律作废，以本节为准。
- **统一托管 = GitHub Pages**（微信/飞书/浏览器免密直开，实测新文件 18~24 秒可访问）：
  - 仓库 `Jungle1499/Jungle1499.github.io`（main 分支），站点 `https://jungle1499.github.io/`
  - 报告中心（汇总 752 篇·带密码门 `fupan2026`）：`https://jungle1499.github.io/center.html`
  - **部署（用 GitHub Contents API，不用 git push——沙箱 git 常报 `Empty reply from server`）**：
    1) 文件名必须 **ASCII 且不以 `_` 开头**（`_` 开头会被 Jekyll 忽略、永不发布），按本任务类型命名，如 `<任务标识>-YYYYMMDD.html`
    2) 令牌：`cat /Users/jungle1499/.workbuddy/.gh_token`（600 权限；**不得打印、不得写进任何产出文件**）
    3) 发布：先生成 base64 payload（`python3 -c \"import base64,json;c=open('<报告绝对路径>','rb').read();open('/tmp/put.json','w').write(json.dumps({'message':'deploy','content':base64.b64encode(c).decode()}))\"`，更新已存在文件须先 GET 取 `sha` 并放进 payload），再执行
       `curl -s -X PUT -H \"Authorization: Bearer $(cat /Users/jungle1499/.workbuddy/.gh_token)\" -H \"Accept: application/vnd.github+json\" --data-binary @/tmp/put.json \"https://api.github.com/repos/Jungle1499/Jungle1499.github.io/contents/<文件名>\"`
    4) **发布后验证（交付前验证铁律）**：`curl -sL -o /tmp/v.html -w '%{http_code}' https://jungle1499.github.io/<文件名>` 必须 200，**且必须 grep 正文确认含报告真实标题关键词**——curl 200 不算数（实测 htmlpreview 等渠道会返回 200 但正文是 1269 字节加载壳、无报告内容）。首次若 404 等 30 秒重试一次（Pages 构建延迟）。
  - 部署失败降级：照发核心文字总结并在消息注明「🔗 单篇待补发」，**绝不发本地路径 / CloudStudio 沙箱 / workbuddy.link**。
- **飞书链接口径（双链接，缺一不可）**：① 🔗 单篇（免密）`https://jungle1499.github.io/<文件名>` ② 📂 报告中心 `https://jungle1499.github.io/center.html`。

【资料库·统一入口（2026-09-09 上线·最高优先级·永久托管，覆盖本任务内一切旧部署写法）】
- **固定入口（恒定不变，永久可用）**：https://www.workbuddy.cn/space/d/bs6jVtmeSAkRNKJQ68u1iD
  （WorkBuddy 资料库在线页：免登录、不空闲停止、跨机器可见。索引内含全部历史报告卷，点开即看。）
- **已弃用 CloudStudio 部署**：原 CloudStudio 沙箱链接因空闲停止 + 老域名退役已大面积失效，**禁止再调用 `（已弃用·见顶部【资料库·统一入口】，禁止部署 CloudStudio，统一发资料库固定入口）`、禁止新建沙箱、禁止发任何 `*.sandbox.cloudstudio.club` / `app.workbuddy.link` 链接**。本任务**必须**走【资料库·双链接发布铁律（2026-09-10 用户铁律·覆盖旧\"只发中心\"写法）】——产出 HTML 后：①本地归档（保留，仍 cp 到 reports/）②取令牌：调用 `connect_open_platform`（资料库场景）取得 op_ 令牌（不要外泄；拿不到再回退 `connect_cloud_service` 取 JWT）③发布单篇：`WB_OP_TOKEN=<op_令牌> WB_JWT=<JWT> python3 /Users/jungle1499/WorkBuddy/_report_hub/import_publish.py <今日报告绝对路径.html> --parent-id bs6jVtmeSAkRNKJQ68u1iD --title \"<报告标题>\"` → 得到 `publish_url`（免密单篇链接）④刷新中心：`WB_OP_TOKEN=<op_令牌> python3 /Users/jungle1499/WorkBuddy/_report_hub/sync_center.py`（卡片进中心 + 重导中心节点上线）⑤**发布后必须点开 publish_url 读第一页真实 <title> 核对**与我声称一致才发飞书（curl 200 不算数）；失败降级：发另一种可用链接并注明「🔗 单篇待补发 / 📂 中心待补发」，绝不发本地路径 / CloudStudio 沙箱。

- 本任务产出 HTML 后**必须**本地归档（不部署、不发沙箱链接）：
  1) `cp <今日报告.html> /Users/jungle1499/WorkBuddy/_report_hub/reports/<YYYYMMDD>__<报告名>.html`
- **飞书消息**：必须**同时发两个链接**（双链接铁律，缺一不可）：
  ① 🔗 单篇报告（免密）：`<上一步 import_publish 得到的 publish_url>`
  ② 📂 报告中心（登录可见·按天列全部）：`https://www.workbuddy.cn/space/d/bs6jVtmeSAkRNKJQ68u1iD`
  **禁止**只发中心一个链接、禁止只发单篇、禁止发本地路径、禁止发 CloudStudio 沙箱链接。
- **链接可用性自检（必执行）**：发送前**必须点开 publish_url 读第一页真实 <title> 核对**与我声称的报告名一致（curl 200 不算数）；同时 curl 中心链接取 200。任一异常按「🔗 单篇待补发 / 📂 中心待补发」降级（仍发另一种可用链接），**绝不发本地路径 / 绝不发 CloudStudio 沙箱链接**。
- **链接可用性自检（必执行）**：发送前 `curl -s -o /dev/null -w '%{http_code}' --max-time 30 https://www.workbuddy.cn/space/d/bs6jVtmeSAkRNKJQ68u1iD` 必须取到 `200` 才允许发送；若非 200，立即排查资料库索引是否异常并重导/取新链接，仍失败按「链接待补发」降级（**绝不发本地路径 / 绝不发 CloudStudio 沙箱链接**）。

【板块覆盖·必加载(2026-09-08 用户铁律·防漏判)】凡本任务需要产出「板块涨幅榜/概念排行/最强主线/赛道强度排序/补涨候选池/三阶段阶段判定」中任一内容，执行前必须先加载 Skill(skill=\"sector-coverage-crosscheck\")（或读 /Users/jungle1499/.workbuddy/skills/sector-coverage-crosscheck/SKILL.md），并走完三道强制门禁：①双分类独立取数——申万+同花顺概念走 westock data_sector(mode=ranking)，同花顺行业指数(二级881xxx/三级884xxx)走 WebFetch https://q.10jqka.com.cn/thshy/detail/code/<code>/ ，第二套 westock 不支持、不可省略；②差异扫描——涨幅≥+3%且只在单一体系出现、或两套差>1.5pp、或某体系全红而另一套不是，命中即强制进榜并注明分类体系与代码；③涨停股反向聚合——当日全部涨停股按行业聚合，任何≥3只涨停的集群必须能在最终板块榜里找到对应板块，找不到即判定漏判嫌疑，须回查该赛道在其他分类体系下的真实涨幅与排名。输出纪律：强度排序必须注明分类体系与代码（如「出版（同花顺884176）+4.39%」）；跨体系比较优先用「涨幅排名 X/345」而非绝对涨幅；禁止用单一口径资金流下\"吸筹/出货\"结论。

【规则库·必加载(2026-09-07 起)】执行本任务前先加载 Skill(skill=\"fupan-rules\")（或读 /Users/jungle1499/.workbuddy/skills/fupan-rules/SKILL.md）——A股复盘规则单点源（①~㊽ + 规则51~60 + 元规则层4条 + 三阶段 + 数据源铁律 + 资金纪律），与 prompt 冲突时以 skill 为准。加载后按其「开跑前自检5问」执行并在报告中显式标注规则编号：①今日 regime 判定(规则55) ②被判\"空/禁多\"的板块按规则59复核是否已失效（外盘同链≥+3% ∧ 产业催化≥2条 ∧ 5日转正或20日收窄）③补涨候选池扫描(规则57) ④最高分方向三重确认(规则56·≥85分必查) ⑤单向失真熔断核查(规则58管多/规则60管空)。标注规则编号是 20:30 回测归因\"引用规则 vs 未引用规则\"的唯一依据，禁省略。

【集合竞价快报 · 9:25 读取 / 9:27 发 · gold V2.3.1 模板（2026-09-02 用户指定\"以后照着这个做\"）】

## 最高优先级：模板对齐铁律
生成的 HTML 报告**必须逐块对齐** `/Users/jungle1499/WorkBuddy/大盘复盘/竞价策略/gold_竞价Top5_结构规范.md`（= gold 链接 https://www.workbuddy.link/p/vdyLSKk5Crtwc3k0EYKC1s 的源文件 `Top5_2026-09-02_V231.html`）。
- 本地模板底本：`竞价策略/gold_竞价Top5_V231_20260902.html`（已剥离平台标记，可直接复制骨架）。
- **执行前必须先 Read 该规范文档**，按其 CSS（:root 变量体系）、七节结构、列名、固定文案逐字复刻；**仅换数据，不改版式、不增删分区、不改列名措辞**。
- 七节顺序固定：一、市场竞价概况 / 二、竞价强势板块 Top5（申万二级，10分制）/ 三、代表个股 / 四、龙头背离分析 / 五、评分明细 / 六、操作建议汇总（含 h3 完整风控提示 4 条）/ 七、宏观参考（SW1 一级）。

## 数据源铁律
- **第一优先 westock（腾讯金融科技 / westock-tool / westock-data）**——gold 即以此源生成。
- 降级链：westock → 同花顺问财（kuaicha-search）→ 东财 → 腾讯 gtimg。≥2 源交叉认证，任一源断线即换源，**绝不中断**；缺失标 N/A，**严禁编造**。
- 口径：申万二级 SW2；数据时点 9:25 最终竞价撮合；filter 池 ≈ 沪深A股 5014 只（ChangePCT>2）。
- 评分 10 分制 = 广度3 + 量能2(环比) + 龙头溢价3 + 相对强度2；信号档：≥8 强信号 / 7 试探 / 5-6 待确认 / <5 弱。
- 情绪档：高开>2% 家数 好>200 / 中100-200 / 差<100。

## 执行流程

1) **周末门控**（最前）：Bash `date +%u`，≥6（周六/日）→ 立即结束，零调用。

2) **9:25 读取**：对齐 09:25:00（开盘价撮合确定后字段才可得；平台早触发则 sleep 到 09:25:00）。用 westock 取：
   - 全市场 filter 池 ChangePCT>2 高开家数 → 情绪档
   - 申万二级板块竞价高开%、竞价额（A轨板块竞价量环比 + B轨个股竞价额加总，量能 V2.3.2）
   - Top5 板块成分股：高开%、连板数(1B/2B/3B/4B+)、竞价额(万)、近5日上榜次数(x/5)
   - 龙头背离：老龙头(T-1) vs 新龙头(今日竞价)
   - SW1 一级板块高开家数
   - 连板数取不到则标 N/A（禁编造），近5日取不到同理。

3) **9:27 硬截止 · 先推飞书文字快报**（绝不晚于 09:27）：
   `lark-cli im +messages-send --as bot --user-id ou_fadb32ffb807b0080dfa6e5257305b3b --markdown '<6段：标题 / 今日结论 / 市场情绪 / Top3板块 / 代表个股 / 操作要点 + 交付信息>'`
   （PATH 须含 `/Users/jungle1499/.workbuddy/connectors/cli-connector-packages/bin` 与 node 绝对路径；**必须 `MSG=$(cat file)` 再传变量，禁止 `--markdown @/path`**。）

4) **生成完整 HTML**（9:27 之后继续，不受硬截止约束）：按规范文档生成七节报告 → 写入 `jingjia_pipeline/_deploy_jingjia_YYYYMMDD_v231/index.html`（**每天新建独立目录，绝对禁止复用旧目录**——旧沙箱回收后重部署同目录返回 HTTP 400）。

5) **部署 + 校验 + 补发链接**：
   - （已弃用·见顶部【资料库·统一入口】，禁止部署 CloudStudio，统一发资料库固定入口） 部署该目录（entry=index.html, port=3000），取 shareLink。
   - **强制存活校验**：`curl -s -o /tmp/v24_verify.html -w '%{http_code}' --max-time 30 <shareLink>`，须 HTTP 200 且内容含「竞价」；不满足则用全新目录（_b / _c）重部署重试，至多 5 次。
   - 校验通过后补发飞书：`🔗 【竞价快报 YYYY-MM-DD 完整报告】\n\n<真实URL>\n\n📌 内容速览：<3-4条>`（幂等键 v24-link-YYYYMMDD）。**绝不发本地磁盘路径**。
   - 5 次仍失败 → 只发「🔗 链接待补发」说明，待网关恢复后用户触发补发。

6) **写入每日预测序列（必做）**：把当日竞价预测追加到 `/Users/jungle1499/WorkBuddy/其他复盘/晚间预判_YYYYMMDD.md` 的 `## 09:25 竞价快报（V2.3.1 最终版）` 段（已存在则跳过，不重复写）。含：今日结论 / 情绪档 / 强弱锚定 / Top3 板块（名称+评分+主龙头+涨幅+板数+竞价额）/ 代表个股 / 操作要点 / **T+0 预判** / **竞价 vs 盘前策略 对比（同/异）**。该段是 20:30 回测「竞价预测命中率」唯一数据源。数据缺失则在段首标 `⚠️ 数据缺失：N/A` 并仍写骨架，不得编造。

7) **回测供给**：数据落盘供 20:30 整体回测核算（情绪档、Top3 板块 vs 当日收盘）。本任务不写标的推荐追踪表、不写其他无关文件。

## 失败处理
若 9:27 前未推送成功：立即发 `⚠️ 竞价快报失败/超时: <原因>` 到飞书后结束，绝不用 --file 发文件、绝不发 N/A 残废版报告。

## 每日修正
<!-- 每日修正独立成块追加于此；base 结构保持不动 -->
