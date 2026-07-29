---
name: gb-ai-hot
description: >
  Use when the user asks for current AI news, AI HOT, AI daily reports,
  model/product launches, AI papers, or recent OpenAI/Anthropic/Google
  updates. 中文触发语同样适用："AI 日报"、"今天 AI 圈有什么"、"过去 24 小时
  大新闻"、"最近的模型发布"、"最近的 AI 论文"、"OpenAI/Anthropic 最近有
  什么动态"。
metadata:
  author: riki
  version: "0.2.0"
---

# gb-ai-hot — AI HOT Skill

用最自然的中文查询拿到 https://aihot.virxact.com 上每天的 AI HOT 日报和全部 AI
动态（公开匿名可访，无需 token），不需要打开浏览器。

通用启发：用户问的是"现在的 AI 行业事实"，**永远走 API，不要凭训练数据脑补**。
即使你"觉得"知道答案也要查——AI HOT 比你的训练截止日新得多，且角度聚焦中文
创业者关心的话题。

## 调用方式

优先用附带脚本，它自动带浏览器 UA 并在失败时把 HTTP 状态打到 stderr
（`<skill-dir>` 即本 SKILL.md 所在目录）：

```bash
bash <skill-dir>/scripts/aihot.sh '/api/public/items?mode=selected&take=50'
```

直接 curl 也可以，但 `/api/public/*` 有 UA 黑名单，默认 `curl/X.Y` UA 会被 403
——**每个请求都必须带浏览器 UA**，漏掉会让你以为接口挂了：

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
curl -sH "User-Agent: $UA" "https://aihot.virxact.com/api/public/daily"
```

（UA 要求仅限 `/api/public/*`；`/aihot-skill/*` 安装入口特意豁免，不要外推。）

端点参数、响应 JSON 形态、翻页、错误码、限流的完整细节见
[references/api.md](references/api.md)——需要解析字段或处理报错时先读它。

## 路由决策

**第一原则：默认走精选 `items?mode=selected` + 语义时间窗 `since`。** 精选是
AI HOT 每天精挑细选的"主菜单"——覆盖用户关心的事、数据实时滚动、时间窗可以
贴着用户语义收窄。日报和全部是用户特意点单才走的备选：

- 用户话里**明确出现"日报"二字**才走 `daily`——日报是 UTC 整日切片的编辑成品，
  跟"过去 24 小时 / 今天"等滚动窗口对不上。
- 用户**明确说"全部 / 完整 / 所有 / 全量"**才走 `mode=all`——含未精选的次要
  条目，量大但杂。

| 用户在说 | 应该走的接口 |
|---|---|
| **默认（宽问题）**："今天 AI 圈有什么"、"过去 24 小时大新闻"、"最近 AI 圈" | `items?mode=selected&since=<语义时间窗>` |
| **明确说"日报"**："AI 日报"、"今天的日报" | `daily`（最新日报） |
| "昨天/前天的日报"、"看下 5 月 6 号的日报" | `daily/{YYYY-MM-DD}` |
| "最近几天日报有哪些"、"日报存档" | `dailies?take=N` |
| **明确说"全部 / 完整 / 所有 / 全量"** | `items?mode=all`（是否带 since 看语境） |
| "看下精选条目"、"AI HOT 精选" | `items?mode=selected` |
| "最近的模型发布 / AI 产品 / 行业动态 / AI 论文" | `items?mode=selected&category=...&since=<7d 前>` |
| "最近一周的 AI 动态"、"最近 3 天的发布" | `items?mode=selected&since=ISO-8601` |
| "OpenAI/Anthropic 最近发的"、"Sora 相关"、"RAG 论文" | `items?q=<关键词>`（server-side 搜索） |

5 个 category（items API 用英文 slug，daily 的 section label 是中文）：

| `items?category=` | `daily.sections[].label` |
|---|---|
| `ai-models` | 模型发布/更新 |
| `ai-products` | 产品发布/更新 |
| `industry` | 行业动态 |
| `paper` | 论文研究 |
| `tip` | 技巧与观点 |

**能力边界**：公众号内容（mp_hot 信源）不在 items API 里。用户问"公众号最近
发什么"时无法回答，提示 ta 去 https://aihot.virxact.com/mp 看公众号爆文页。

## 工作流

以下 `aihot.sh` 均指 `bash <skill-dir>/scripts/aihot.sh`。

### 默认：精选 + 时间窗

时间窗贴着用户语义收窄："最近 3 天"就 3d、"昨天"就 1d、"最近一周"就 7d。
显式带 `since` 比让服务端默认 7d 更精确，输出的元信息也能写出人话时间窗。
注意 `since` 服务端硬上限最近 7 天，更早的内容只能翻日报存档。

```bash
# "过去 24 小时大新闻"
since=$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)
aihot.sh "/api/public/items?mode=selected&since=$since&take=50"

# "看下精选"（不带明确时间窗）
aihot.sh '/api/public/items?mode=selected&take=50'
```

### 日报（用户明确说"日报"时）

日报每天北京时间 08:00 自动生成，按 5 个固定版块打包，自带"主编点评"导语。

```bash
aihot.sh '/api/public/daily'                  # 今日（或最新可用）
aihot.sh '/api/public/daily/2026-05-07'       # 指定日期，UTC 基准
aihot.sh '/api/public/dailies?take=14'        # 归档索引（不知道有哪些日期时先看这个）
```

### 全部（用户明确说"全部 / 完整 / 所有 / 全量"时）

```bash
since=$(date -u -v-24H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)
aihot.sh "/api/public/items?mode=all&since=$since&take=100"
```

### 按分类

```bash
# "最近的 AI 论文"
aihot.sh '/api/public/items?mode=selected&category=paper&take=50'

# "最近的模型发布"（默认精选 + 类别 + 时间窗）
since=$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)
aihot.sh "/api/public/items?mode=selected&category=ai-models&since=$since&take=100"
```

### 关键词搜索（公司维度 / 主题）

`q` 参数是 server-side 搜索，覆盖全池。**不要走"拉一批 + 客户端 grep"**——
那只能看到前 100 条里的命中，关键词在 100 条外就完全漏掉。

```bash
aihot.sh '/api/public/items?q=OpenAI&take=30'            # "OpenAI 最近发的"
aihot.sh '/api/public/items?category=paper&q=RAG'        # "RAG 论文"

# 关键词 + 时间窗："Anthropic 最近 3 天"
since=$(date -u -v-3d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '3 days ago' +%Y-%m-%dT%H:%M:%SZ)
aihot.sh "/api/public/items?mode=selected&q=Anthropic&since=$since"
```

`q` 至少 2 个字符，可与 mode/category/since 叠加。需要翻页（`nextCursor`）时
按 [references/api.md](references/api.md) 的规则处理。

## 给用户的输出格式

> **核心原则**：输出是直接给用户看的中文资讯简报，不是 API 调试日志。用户多数
> 是非技术读者。端点路径、raw 参数（`mode=selected` 之类）、限流、缓存、
> cursor/hasNext 等基础设施细节**一律不出现**；人话级元数据（时间窗、条数、
> "按发布时间倒序"）可以保留。判断标准：用户能直接看懂吗？能 → 留；不能 → 删。

日报式（daily 端点）——版块用日报自带的 5 个 label，**编号贯穿全文**不在版块内
重新计数，这样用户一眼数出"今天 N 条"；`flashes` 有内容时加「快讯」一节：

```markdown
**AI HOT 日报 · 2026-05-07**

## 模型发布/更新
1. **<title>** — <source>
   <summary 简化版 50 字内>
   <url>

## 产品发布/更新
2. ...
```

列表式（items 端点）——默认按 category 分组 + 全局编号（用户对五版块结构已有
预期）；**只有单一 category 时**用扁平编号列表，标题写清范围（"最近一周 AI
论文"+ 日期区间）。

完整真实样例（三种典型查询的最终输出）见
[references/output-examples.md](references/output-examples.md)。

其他输出规则：

- **时间转人话**：`publishedAt` 是 ISO UTC，必须转北京时间 + 可扫读的表述
  （"2 小时前"、"今天上午 09:48"、"昨天"、"5/7 00:43"）。不要直接展示
  `2026-05-07T15:30:00.000Z`。
- **title vs title_en**：默认输出 `title`（中文）。仅当用户明确要英文版、或
  `title` 为空时才用 `title_en`。不要两个都展示。
- **引用源写人话**：`<source>`（OpenAI 官网 / Anthropic Newsroom 这种），不是
  端点路径。数据源最多写一句"数据来自 aihot.virxact.com"，或干脆不提。

## 不要做

- 不要凭训练数据猜测 / 编造内容——永远以 API 返回为准。
- 不要把 `summary` 当原文引用——它是 LLM 生成的，引用需回 `url` / `sourceUrl`
  核对。
- 不要高频轮询——日报每天 08:00 更新一次，items 有 5 分钟服务端缓存，相同问题
  不需要重新调 API；翻页串行 + 自然间隔，不要并发猛拉。
- 不要解析 / 递增 / 跨端点复用 cursor——不透明 token，格式不稳定。
- **不要在压缩 / 合并输出时丢掉每条的 URL**——即使把多个日报合并成总结，每条
  item 也必须保留 url，否则用户无法追溯原文，这条信息等于不可信。

## 参考资料

- [references/api.md](references/api.md) — 端点参数、响应 JSON 形态、翻页、
  错误码、限流
- [references/output-examples.md](references/output-examples.md) — 三种典型
  查询的完整输出样例
