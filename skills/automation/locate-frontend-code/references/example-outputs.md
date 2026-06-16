# 加速器输出参考(locate.mjs)

> 这里记录的是**可选加速器** `scripts/locate.mjs` 的原始输出,**不是** skill 的
> 最终产出。最终产出是 SKILL.md 里那份「功能地图」(结构树 + 速查表 + 数据流)。
> 脚本只负责快速收窄候选;你拿到这些 `file:line` 后,要 Read 核对再归纳成地图。

真实项目上跑出来的输出留档(`guoba-vibe/apps/qr-vault` —— React 19 +
TanStack Router + i18next,以及 qr-codes / rn-components)。下面每个代码块都是
逐字的真实 stdout,不是手写的。用它来认脚本「健康的结果长什么样」与能力边界。

怎么看输出:每次运行都打印 **① PAGE → ② MODULE → ③ CODE**。一条线索只会填上
它能到达的层——路由填 ①②;界面文字线索直接跳到 ③,再反向走回页面。

---

## 0. 最终产出长什么样(功能地图)

**这才是 skill 的交付物。** 下面是对 qr-vault「导入导出」功能产出的功能地图——
做法是:先跑加速器(见 §2 的 `/import` 原始输出)拿到候选,再逐个 `Read` 核对
行号与职责,最后归纳成下面这份(每个行号都核对过):

```
# 功能:导入导出  (/import)
把整个库导出成 JSON 快照下载,或从 JSON 文件导入覆盖本地库。

## 结构
src/app/import-export-page.tsx            页面容器:导出/导入编排、成功失败消息
├─ import-export/snapshot-card.tsx        导出卡:统计 + "导出 JSON 快照"按钮  渲染@:106
├─ import-export/import-card.tsx          导入卡:拖拽/选择文件 + 结果提示      渲染@:107
└─ import-export/stat-tile.tsx            小统计块(QR 数 / 合集数)
   ↘ 依赖 lib/storage.ts(exportVaultJson/parseVaultData)、i18n importExport.*

## 速查表
| 想改什么 | 位置 |
|---|---|
| 导出逻辑(生成 Blob 下载) | `exportVault()` @ import-export-page.tsx:34 |
| 导入逻辑(读文件→解析→落库) | `readImportFile()` @ import-export-page.tsx:44 |
| 非法 JSON 的报错文案 | `t('importExport.invalidJson')` @ page.tsx:55 |
| 导出按钮 UI/文案 | snapshot-card.tsx:28 / i18n `importExport.exportSnapshot` |
| 拖拽区交互 | `ImportDropzone` @ import-card.tsx:76 |
| 序列化/反序列化实现 | `exportVaultJson`/`parseVaultData` @ lib/storage.ts:71 / :48 |

## 数据流
- 导出:点按钮 → `exportVault()` → `exportVaultJson(data)` → Blob → 浏览器下载
- 导入:选文件 → `readImportFile()` → `parseVaultData()` → 成功 `updateVault` / 失败 `setError(invalidJson)`
```

> 注意对比:加速器只给到「§2 那批 `file:line` 原始匹配」;上面的**职责一句话、
> 数据流、速查表**是 `Read` 之后归纳的——这部分是模型干的,脚本给不了。

下面 §1–§9 是**加速器的原始输出**(归纳功能地图的原料),按线索类型分组。

---

## 1. 路由线索 → 页面 → 模块

```
$ node scripts/locate.mjs /collections --root .../apps/qr-vault

🔎 clue: "/collections"   type: route   root: .../apps/qr-vault

① PAGE — route → page component:
   /collections  →  CollectionsPage  →  src/app/collections-page.tsx

② MODULE — sub-modules ("cards") under the page + its imports:
   module folder: src/app/collections/
     - src/app/collections/collection-form-card.tsx
     - src/app/collections/collection-list-card.tsx
     - src/app/collections/collection-qr-card.tsx
   local imports in src/app/collections-page.tsx:
   src/app/collections-page.tsx:7  import { CollectionFormCard } from '@/app/collections/collection-form-card'
   src/app/collections-page.tsx:8  import { CollectionListCard } from '@/app/collections/collection-list-card'
   src/app/collections-page.tsx:9  import { CollectionQrCard } from '@/app/collections/collection-qr-card'
   src/app/collections-page.tsx:10  import { useVault } from '@/app/use-vault'
   src/app/collections-page.tsx:11  import { type Collection, deleteCollection, upsertCollection } from '@/lib/storage'
   src/app/collections-page.tsx:12  import { useDocumentTitle } from '@/lib/use-document-title'
   src/app/collections-page.tsx:13  import { getQrsForCollection } from '@/lib/vault'

③ CODE — exact locations:
   definition:
   (none)
   usages:
   src/router.tsx:12  import { CollectionsPage } from '@/app/collections-page'
   src/app/collections-page.tsx:7  import { CollectionFormCard } from '@/app/collections/collection-form-card'
   src/app/collections-page.tsx:8  import { CollectionListCard } from '@/app/collections/collection-list-card'
   src/app/collections-page.tsx:9  import { CollectionQrCard } from '@/app/collections/collection-qr-card'
```

**怎么用:** 页面文件是 `src/app/collections-page.tsx`;它的三个 card 在
`src/app/collections/` 里。路由线索下 ③ 比较吵(它在 grep 字面量)——路由
看 ① 和 ② 就够了,别看 ③。

---

## 2. 路由线索(换个页面)→ 页面 → 模块

```
$ node scripts/locate.mjs /import --root .../apps/qr-vault

🔎 clue: "/import"   type: route   root: .../apps/qr-vault

① PAGE — route → page component:
   /import  →  ImportExportPage  →  src/app/import-export-page.tsx

② MODULE — sub-modules ("cards") under the page + its imports:
   module folder: src/app/import-export/
     - src/app/import-export/import-card.tsx
     - src/app/import-export/snapshot-card.tsx
     - src/app/import-export/stat-tile.tsx
   local imports in src/app/import-export-page.tsx:
   src/app/import-export-page.tsx:5  import { ImportCard } from '@/app/import-export/import-card'
   src/app/import-export-page.tsx:6  import { SnapshotCard } from '@/app/import-export/snapshot-card'
   src/app/import-export-page.tsx:7  import { useVault } from '@/app/use-vault'
   src/app/import-export-page.tsx:8  import { Badge } from '@/components/shadcn-ui/badge'
   src/app/import-export-page.tsx:16  import { useDocumentTitle } from '@/lib/use-document-title'
```

**怎么用:** 印证约定可复现 —— `/<route>` → `src/app/<feature>-page.tsx` →
`src/app/<feature>/*` 里的 card。

---

## 3. 界面文字线索(i18n)→ 代码 → 所属页面

```
$ node scripts/locate.mjs "导出 JSON 快照" --root .../apps/qr-vault

🔎 clue: "导出 JSON 快照"   type: text   root: .../apps/qr-vault

① PAGE — (text clue: jump to CODE layer, then walk up to the page)

③ CODE — exact locations:
   i18n locale matches (value → key):
     src/i18n/locales/zh-CN.json:167  "exportSnapshot": "导出 JSON 快照",

   ↳ leaf keys used in code (grep the key to find the component):
     key "exportSnapshot":
   src/app/import-export/snapshot-card.tsx:29  <Download /> {t('importExport.exportSnapshot')}

   ↳ owning page(s):
     src/app/import-export-page.tsx

   hardcoded literal in components:
   (none)
```

**怎么用:** 可见文字是 i18n 化的,所以链路是 文字 → key `exportSnapshot` →
`snapshot-card.tsx:29` → 页面 `import-export-page.tsx`。`hardcoded literal:
(none)` 说明这段文字没有写死在任何 `.tsx` 里,只活在语言包。这也是**截图
路径**:读截图、挑一个可见文案,然后就照这样跑。

---

## 4. 组件 / 符号线索 → 定义 + 调用处 → 所属页面

```
$ node scripts/locate.mjs CollectionFormCard --root .../apps/qr-vault

🔎 clue: "CollectionFormCard"   type: symbol   root: .../apps/qr-vault

① PAGE — definition(s) by name:
   src/app/collections/collection-form-card.tsx:26  export function CollectionFormCard({

② MODULE — sub-modules ("cards") under the page + its imports:
   (no sibling module folder for src/app/collections/collection-form-card.tsx — see its imports below)
   local imports in src/app/collections/collection-form-card.tsx:
   src/app/collections/collection-form-card.tsx:5  import { FieldLabel } from '@/components/field-label'
   src/app/collections/collection-form-card.tsx:6  import { Button } from '@/components/shadcn-ui/button'
   src/app/collections/collection-form-card.tsx:7  import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/shadcn-ui/card'
   src/app/collections/collection-form-card.tsx:8  import { Input } from '@/components/shadcn-ui/input'
   src/app/collections/collection-form-card.tsx:9  import { Textarea } from '@/components/shadcn-ui/textarea'
   src/app/collections/collection-form-card.tsx:10  import type { Collection } from '@/lib/storage'
   src/app/collections/collection-form-card.tsx:11  import { cn } from '@/lib/utils'

③ CODE — exact locations:
   definition:
   src/app/collections/collection-form-card.tsx:26  export function CollectionFormCard({
   usages:
   src/app/collections-page.tsx:7  import { CollectionFormCard } from '@/app/collections/collection-form-card'
   src/app/collections-page.tsx:137  <CollectionFormCard
   src/app/collections/collection-form-card.tsx:26  export function CollectionFormCard({

   ↳ owning page(s):
     src/app/collections-page.tsx
```

**怎么用:** 定义在 `collection-form-card.tsx:26`,在
`collections-page.tsx:137` 被渲染,反向走出所属页面。"no sibling module
folder" 是预期的——线索本身*就是*一个 card,所以 ② 改为展示这个 card 自己
的 import(它依赖的 shadcn 基础组件)。

---

## 跨项目示例(不同结构,真实留档)

以上是 qr-vault(TanStack Router + i18next)。下面是另外两种结构的实跑输出,
用来看脚本在不同框架下的表现与边界。

### 5. Next.js App Router —— 路由组 `(admin)`

```
$ node scripts/locate.mjs /admin --root .../apps/qr-codes

🔎 clue: "/admin"   type: route   root: .../apps/qr-codes

① PAGE — route → page component:
   (file-based route)  src/app/(admin)/admin/page.tsx

② MODULE — sub-modules ("cards") under the page + its imports:
   (no sibling module folder for src/app/(admin)/admin/page.tsx — see its imports below)
   local imports in src/app/(admin)/admin/page.tsx:
   src/app/(admin)/admin/page.tsx:1  import { QrCard } from '@/components/qr-card'
   src/app/(admin)/admin/page.tsx:2  import { SearchBar } from '@/components/search-bar'
   src/app/(admin)/admin/page.tsx:3  import { getCollectionById } from '@/data/collections'
   src/app/(admin)/admin/page.tsx:4  import { listQrCards } from '@/data/qrs'
```

**怎么用:** `/admin` 的真实文件被路由组 `(admin)` 包着,脚本能剥掉 `(group)`
正确定位。这个项目组件平铺在 `src/components/`,没有 per-page 文件夹,所以 ②
不列文件夹、改列页面的 import —— `QrCard`/`SearchBar` 就是它拼装的模块。
(③ 对路由线索是噪音,略。)

### 6. Next.js —— 动态段 `[id]`,传实参也能命中

```
$ node scripts/locate.mjs /c/123 --root .../apps/qr-codes

🔎 clue: "/c/123"   type: route   root: .../apps/qr-codes

① PAGE — route → page component:
   (file-based route)  src/app/c/[id]/page.tsx
```

**怎么用:** 传具体值 `/c/123`,脚本能匹配到动态路由文件 `c/[id]/page.tsx`。

### 7. 传 kebab 文件名 → 自动换算成组件名

```
$ node scripts/locate.mjs qr-card --root .../apps/qr-codes

🔎 clue: "qr-card"   type: symbol   root: .../apps/qr-codes

① PAGE — definition(s) by name:
   (kebab "qr-card" → 组件名 "QrCard")
   src/components/qr-card.tsx:7  export async function QrCard({

② MODULE — sub-modules ("cards") under the page + its imports:
   (no sibling module folder for src/components/qr-card.tsx — see its imports below)
   local imports in src/components/qr-card.tsx:
   src/components/qr-card.tsx:4  import { QrCardLink } from '@/components/qr-card-link'
   src/components/qr-card.tsx:5  import { renderSvg } from '@/lib/qr'

③ CODE — exact locations:
   (kebab "qr-card" → 符号 "QrCard")
   definition:
   src/components/qr-card.tsx:7  export async function QrCard({
   usages:
   src/app/(admin)/admin/page.tsx:1  import { QrCard } from '@/components/qr-card'
   src/app/(admin)/admin/page.tsx:36  <QrCard
   src/app/c/[id]/page.tsx:5  import { QrCard } from '@/components/qr-card'
   src/app/c/[id]/page.tsx:56  <QrCard key={r.id} id={r.id} title={r.title} url={r.url} />
```

**怎么用:** 传的是文件名 `qr-card`,脚本自动换算成 `QrCard`,并且能匹配
`export async function`(早期版本这里会漏)。

### 8. 没有 i18n 的项目 → 命中硬编码文案

```
$ node scripts/locate.mjs "Sign out" --root .../apps/qr-codes

🔎 clue: "Sign out"   type: text   root: .../apps/qr-codes

① PAGE — (text clue: jump to CODE layer, then walk up to the page)

③ CODE — exact locations:

   hardcoded literal in components:
   src/app/login/page.tsx:15  You are signed in with a GitHub account that is not authorized. Sign out and try a different
   src/app/login/page.tsx:42  Sign out
```

**怎么用:** 没有语言包,i18n 那段为空,直接落到"hardcoded literal in
components",在 `login/page.tsx:42` 命中。

### 9. React Native(没有路由)→ 符号路依然精准

```
$ node scripts/locate.mjs feature-panel --root .../apps/rn-components

🔎 clue: "feature-panel"   type: symbol   root: .../apps/rn-components

① PAGE — definition(s) by name:
   (kebab "feature-panel" → 组件名 "FeaturePanel")
   src/components/index.ts:1  export { FeaturePanel } from './feature-panel'
   src/components/feature-panel.tsx:33  export function FeaturePanel({

③ CODE — exact locations:
   (kebab "feature-panel" → 符号 "FeaturePanel")
   definition:
   src/components/feature-panel.tsx:33  export function FeaturePanel({
   usages:
   src/__tests__/feature-panel.test.tsx:4  import { FeaturePanel } from '../components/feature-panel'
   src/stories/feature-panel.stories.tsx:3  import { FeaturePanel } from '../components'
   …
```

**怎么用:** RN 没有路由,page 层不适用;但**组件/符号这条路照样精准** ——
定义在 `feature-panel.tsx:33`,用法散落在 `__tests__` 和 `stories` 里。

---

## 结果不对的信号

- **每一层都是 `(none)`** → `--root` 给错了,或不是 React/Vue 项目。
- **路由线索的 ① PAGE 解析出错误组件** → 路由把 `component:` 写在了 `path:`
  *之前*,或在很深的嵌套行;手动读那段路由块(见 SKILL.md → 手动流程)。
- **界面文字命中语言包行但找不到 key 的使用处** → key 是动态拼的
  (`t(\`prefix.${x}\`)`);改成 grep 静态前缀。
