# AI HOT API 参考

Base URL `https://aihot.virxact.com`，匿名访问，无需 token。完整 OpenAPI 3.1 规范：
`https://aihot.virxact.com/openapi.yaml`。

调用注意：`/api/public/*` 必须带浏览器 User-Agent（默认 curl UA 会被 403）；
限流 600 req/min/IP，请串行调用，不要并发猛拉，翻页加 200ms 间隔。

本文档的 `aihot.sh` 均指 `bash <skill-dir>/scripts/aihot.sh`（`<skill-dir>` 即 SKILL.md
所在目录），它会自动带上浏览器 UA。

## 端点速览

| 端点 | 用途 | 主要参数 |
|---|---|---|
| `/api/public/daily` | 最新日报 | 无 |
| `/api/public/daily/{YYYY-MM-DD}` | 指定日期日报 | path: `date`（UTC 基准） |
| `/api/public/dailies` | 日报归档列表 | `take`（1-180，默认 30） |
| `/api/public/items` | 全部 AI 动态 | `mode` / `category` / `since` / `take` / `cursor` / `q` |

## items 参数约束

- `mode`：`selected`（精选池，`aiSelected=true`）或 `all`（含未精选次要条目）
- `category`：`ai-models` / `ai-products` / `industry` / `paper` / `tip`
- `since`：ISO 8601。**服务端硬上限最近 7 天**——不传等同 `since=now-7d`；早于 7 天前自动
  截到 7 天前；未来时间 → 400。所以 items API 永远只返回最近 7 天的内容，需要更早
  → 走 `/api/public/daily/{YYYY-MM-DD}` 翻日报存档
- `take`：1-100；想要更多走 cursor 翻页
- `q`：server-side 关键词搜索，在 `title` + 中文 `title` + 中文 `summary` 三列匹配。
  至少 2 个字符（单字符视作不搜索）、最长 200 字（超出截断），可与
  mode/category/since/take/cursor 正交叠加

## 翻页（cursor）

`/api/public/items` 响应里有 `nextCursor`（opaque token），下次请求原样塞进 `cursor`
参数即可：

```bash
resp1=$(aihot.sh '/api/public/items?mode=all&take=100')
cursor=$(echo "$resp1" | jq -r '.nextCursor')
aihot.sh "/api/public/items?mode=all&take=100&cursor=$cursor"
```

`hasNext = false` 或 `nextCursor = null` 时停止翻页。cursor 是不透明 token，视作黑盒，
不要尝试解析、递增、或跨端点复用。

## 返回数据形态

### `/api/public/daily`

```json
{
  "date": "2026-05-07",
  "generatedAt": "2026-05-07T00:01:23.456Z",
  "windowStart": "2026-05-06T00:00:00.000Z",
  "windowEnd":   "2026-05-07T00:00:00.000Z",
  "lead": { "title": "...", "leadParagraph": "..." },
  "sections": [
    {
      "label": "模型发布/更新",
      "items": [
        {
          "title": "...",
          "summary": "...",
          "sourceUrl": "https://...",
          "sourceName": "OpenAI Blog"
        }
      ]
    }
  ],
  "flashes": [
    { "title": "...", "sourceName": "...", "sourceUrl": "...", "publishedAt": "..." }
  ]
}
```

`sections[].label` 固定 5 个："模型发布/更新" / "产品发布/更新" / "行业动态" /
"论文研究" / "技巧与观点"。`lead` 极少数日报为 `null`。

### `/api/public/dailies`

```json
{
  "count": 14,
  "items": [
    { "date": "2026-05-07", "generatedAt": "...", "leadTitle": "..." }
  ]
}
```

### `/api/public/items`

```json
{
  "count": 50,
  "hasNext": true,
  "nextCursor": "eyJhIjoxNzE0OTk1MjAwMDAwLCJpIjoiY205eHl6MTIzIn0",
  "items": [
    {
      "id": "cm9abc456def789ghi012jkl3",
      "title": "中文标题（normalize 过）",
      "title_en": "原英文标题（仅当与 title 不同时存在，否则 null）",
      "url": "https://...",
      "source": "OpenAI Blog",
      "publishedAt": "2026-05-07T15:30:00.000Z",
      "summary": "中文摘要（LLM 生成）",
      "category": "ai-models"
    }
  ]
}
```

字段不变量：

- 必有：`id` / `title` / `url` / `source`
- 可空：`title_en` / `summary` / `publishedAt` / `category`
- `category` 取值集：`ai-models` / `ai-products` / `industry` / `paper` / `tip` / `null`
- `publishedAt`：ISO 8601 UTC（带 `Z`）
- `id`：cuid 字符串（25 字符），不要假设是数字

## 常见错误

- `{"error":"No daily report available yet."}`（HTTP 404）：当天日报还没生成（北京时间
  08:00 之前）。建议改拉昨天日报 `/api/public/daily/{昨天日期}`
- `{"error":"Invalid date format..."}`（HTTP 400）：date 必须是 `YYYY-MM-DD`，UTC 基准
- items 端点常见 400：
  - `"invalid mode (must be 'selected' or 'all')"`
  - `"invalid category (must be one of: ai-models, ai-products, industry, paper, tip)"`
  - `"invalid since (must be ISO date, not in future)"`
  - `"invalid take (must be integer 1-100)"`
- HTTP 403：没带浏览器 UA（用 `scripts/aihot.sh` 可避免）
- HTTP 429（限流）：单 IP 超 600 req/min。串行调用 + 翻页加 200ms 间隔即可
