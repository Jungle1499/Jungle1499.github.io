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
    3) 发布：先生成 base64 payload（`python3 -c "import base64,json;c=open('<报告绝对路径>','rb').read();open('/tmp/put.json','w').write(json.dumps({'message':'deploy','content':base64.b64encode(c).decode()}))"`，更新已存在文件须先 GET 取 `sha` 并放进 payload），再执行
       `curl -s -X PUT -H "Authorization: Bearer $(cat /Users/jungle1499/.workbuddy/.gh_token)" -H "Accept: application/vnd.github+json" --data-binary @/tmp/put.json "https://api.github.com/repos/Jungle1499/Jungle1499.github.io/contents/<文件名>"`
    4) **发布后验证（交付前验证铁律）**：`curl -sL -o /tmp/v.html -w '%{http_code}' https://jungle1499.github.io/<文件名>` 必须 200，**且必须 grep 正文确认含报告真实标题关键词**——curl 200 不算数（实测 htmlpreview 等渠道会返回 200 但正文是 1269 字节加载壳、无报告内容）。首次若 404 等 30 秒重试一次（Pages 构建延迟）。
  - 部署失败降级：照发核心文字总结并在消息注明「🔗 单篇待补发」，**绝不发本地路径 / CloudStudio 沙箱 / workbuddy.link**。
- **飞书链接口径（双链接，缺一不可）**：① 🔗 单篇（免密）`https://jungle1499.github.io/<文件名>` ② 📂 报告中心 `https://jungle1499.github.io/center.html`。

【夜间·资料库发布 & 中心同步 兜底任务（每日 20:00 运行·最高优先级保障）】
目标：把当天（交易日）各篇复盘报告导入资料库、发布为单篇免密链接、刷新报告中心，并向用户发送「今日复盘汇总」（每篇单篇链接 + 中心链接）。本任务是晚间复盘自动化（19:00 完整复盘 / 19:15 最强主线 / 19:30 主线分析 / 19:45 深度复盘预判版）的兜底：若某篇因发布失败漏入库，本任务补发；同时保证中心索引最新、不漏任何一篇。

0. 时间说明：由 RRULE 每日约 20:00 触发（±10min 漂移，可能略早）。一律照常执行，不因触发略早跳过；数据基准为当日已收盘数据。
1. 交易日判断：用 westock 交易日历确认今天是否 A股交易日；非交易日（周末/法定节假日）直接结束，不发消息。
2. 取 JWT：调用 `connect_open_platform`（资料库场景）取得 op_ 令牌（不要把 token 明文写进任何文件或回复）；若失败再回退 `connect_cloud_service` 取 JWT。
3. 扫描今日报告：列出 `/Users/jungle1499/WorkBuddy/_report_hub/reports/` 下文件名含今天日期 YYYYMMDD 的 HTML；同时读取 `/Users/jungle1499/WorkBuddy/_report_hub/published.json` 已发布清单（键为文件名）。
4. 逐篇发布（仅处理未在 published.json 中出现的今日报告）：
   对每篇未发布的今日报告：
   `WB_OP_TOKEN=<op_令牌> WB_JWT=<JWT> python3 /Users/jungle1499/WorkBuddy/_report_hub/import_publish.py <绝对路径.html> --parent-id bs6jVtmeSAkRNKJQ68u1iD --title "<由文件名/内容推断的报告标题，含日期>"`
   捕获脚本打印的 `{"node_block_id":...,"publish_url":...}` 中的 publish_url（单篇免密链接 `https://workbuddy.link/p/<id>`）。
   （⚠️ 禁止使用资料库自带 import_html.py：其写接口用 X-Skill-Token 鉴权会失败；只允许用上面的 import_publish.py。）
5. 刷新中心：`WB_OP_TOKEN=<op_令牌> python3 /Users/jungle1499/WorkBuddy/_report_hub/sync_center.py`（幂等：已存在于中心的链接不会重复添加，新发布的会追加进对应日期分组并重导中心节点；中心节点保持私有）。
6. 发送「今日复盘汇总」飞书：
   - 若当日有 ≥1 篇报告：消息含一段核心文字总结（今日最强主线含阶段 / 情绪温度 / 进攻·回避·持有操作建议 / 核心风险，用真实数据），随后逐篇列出：
     🔗 单篇报告：<publish_url>
     📂 报告中心：https://www.workbuddy.cn/space/d/bs6jVtmeSAkRNKJQ68u1iD
   - 若当日无任何新报告：仅发「今日无新复盘报告」即可，不发空壳。
   - 发送命令（bot 身份，user-id `ou_fadb32ffb807b0080dfa6e5257305b3b`）：
     `python3 /Users/jungle1499/WorkBuddy/其他复盘/send_once.py send nightly-sync-YYYYMMDD <center_url> /tmp/nightly_feishu.md --user-id ou_fadb32ffb807b0080dfa6e5257305b3b`
     （send_once 幂等：今天已发过则复用，不重发。）
   发送前自检：markdown 须同时含 `🔗` 与 ≥3 个关键词（主线/风险/情绪/配置/操作/回测/催化/资金），且无 XX/X%/占位符；发送前 curl 校验 center_url 与目标单篇 publish_url 均返回 200（中心为私有页，登录态 200 即正常）。
7. 遵守全局·飞书推送铁律（带核心文字总结、禁止只发标题+URL、无占位符）。

幂等保证：已发布的篇目不重复发布；sync_center 幂等；send_once 防重发。
本任务不生成报告内容，只负责发布/同步/汇总，不写任何累积文档。

## 每日修正
<!-- 每日修正独立成块追加于此；base 结构保持不动 -->
