---
name: locate-frontend-code
description: >
  探索某个前端功能的代码,产出一份「功能地图」(结构树 + 速查表 + 数据流),
  帮你快速了解它的代码位置和结构。仅在以下显式触发时调用:
  `/locate-frontend-code`、"定位前端代码"、"这个功能的代码在哪/结构是什么"、
  "给我一份功能地图"、"map this feature"。
metadata:
  author: riki
  version: "0.2.0"
---

# 前端功能地图

给一个功能(页面名 / 路由 / 界面文字 / 截图 / 一句话描述),**你(模型)自己
去仓库里探索**,把它的代码摸清楚,然后产出一份**简洁易读的功能地图**:按
page → module → code 组织的结构树 + 「想改什么去哪」速查表 + 数据流。

这不是"跑个脚本打印一堆匹配"。脚本只是可选加速器;**真正的产出是你读完代码后
归纳出的那份地图**——路径真实、行号核对过、职责一句话说清。

## 产出模板(这是最终交付物)

严格按这个结构输出,内容换成真实代码。三块:结构树、速查表、数据流。

```
# 功能:<功能名>  (<入口路由,如有>)
<一句话:这个功能干什么>

## 结构
<page 文件>                     页面容器 / 负责什么
├─ <module 文件>               这个模块负责什么
├─ <module 文件>               …
└─ <module 文件>               …
   ↘ 依赖 <lib/服务文件>, <…>   (页面/模块依赖的非 UI 代码)

## 速查表
| 想改什么 | 位置 |
|---|---|
| <常见修改点> | <file:line 或 i18n key> |
| … | … |

## 数据流
<用户操作 → 调用的函数 → 状态/存储 → 重渲染,一行说清>
```

### 真实样例(qr-vault 的「合集」功能,已逐项核对代码)

```
# 功能:合集管理  (/collections)
管理 QR 合集:新建/编辑/删除合集,查看合集内的 QR。

## 结构
src/app/collections-page.tsx              页面容器:路由参数解析、状态、增删改编排
├─ collections/collection-list-card.tsx   左侧合集列表(选中/删除)        渲染@:129
├─ collections/collection-form-card.tsx   新建·编辑表单(标题/描述/保存)  渲染@:137
└─ collections/collection-qr-card.tsx     选中合集后展示合集内 QR          渲染@:149
   ↘ 依赖 lib/storage.ts(增删改)、lib/vault.ts(查询)、i18n collections.*

## 速查表
| 想改什么 | 位置 |
|---|---|
| 保存合集的逻辑 | `saveCollection()` @ collections-page.tsx:61 |
| 删除(二次确认)逻辑 | `handleDelete()` @ collections-page.tsx:80 |
| 新建按钮行为 | `startNewCollection()` @ collections-page.tsx:72 |
| 表单 UI/字段 | collection-form-card.tsx:26 |
| 列表 UI | collection-list-card.tsx:18 |
| 增删改的底层实现 | `upsertCollection`/`deleteCollection` @ lib/storage.ts:131 / :123 |
| 界面文案 | i18n key `collections.*` @ i18n/locales/zh-CN.json |

## 数据流
点保存 → `saveCollection()` → `updateVault(upsertCollection(...))` → 写入 storage → 重渲染列表
```

更多真实样例(工作区 / QR 详情 / 分享页)见
[`references/feature-map-samples.md`](references/feature-map-samples.md)。

## 探索流程(你怎么把上面填出来)

用你自己的工具(Grep / Glob / Read)按层探,**每写进地图的行号都要 Read 核对**,
不要凭匹配猜:

1. **入口(page)**:把线索落到页面文件。
   - 路由 → 在 router 配置 grep `path:`,或 Next.js 看 `app/<route>/page.tsx`。
   - 界面文字 → 先 i18n 反查(语言包 JSON 里搜文案 → key → 用到 key 的组件),
     没有 i18n 就直接搜硬编码字面量。
   - 截图 → 先读图,挑一段稳定可见文字,再走"界面文字"。
   - 一句话描述/页面名 → grep 组件定义或目录名。
2. **模块(module/card)**:读页面文件的 import + 看它隔壁的同名文件夹
   (`src/app/<feature>/`)。**逐个打开模块文件,用一句话概括它干什么**——
   这步是地图的灵魂,不能省。
3. **代码(code)**:对每个"常见修改点",Read 到具体函数/JSX,记下 `file:line`。
4. **数据流**:顺着事件处理函数(onClick/onSubmit)追到它调用的服务/存储函数,
   串成一行。

## 可选加速器:locate.mjs

大仓库里想先快速收窄候选,可以先跑脚本拿一批 `file:line`,**再人工核对、归纳成
地图**(脚本不产出地图,只给原始线索):

```bash
node <skill-dir>/scripts/locate.mjs "<线索>" --root <前端项目目录>
```

它会按 ① PAGE / ② MODULE / ③ CODE 打印匹配。脚本的能力边界、各框架下的真实
输出、以及踩过的坑,见
[`references/example-outputs.md`](references/example-outputs.md)。

## 质量要求(产出前自检)

- [ ] 结构树里**每个文件路径都真实存在**,没有编造。
- [ ] 速查表里**每个行号都 Read 核对过**,不是 grep 的近似匹配。
- [ ] 每个模块都有**一句话职责**,而不是只列文件名。
- [ ] 数据流串得通(事件 → 函数 → 存储 → 渲染),不是空话。
- [ ] 整体能让人**两分钟看懂这个功能的代码长怎样、改东西去哪**。

## 适配不同项目

- 页面/模块约定常见为 `src/app/<feature>-page.tsx` + `src/app/<feature>/*`;
  Next.js 是 `app/<route>/page.tsx` + 平铺的 `src/components/`(此时"模块"看
  页面的 import)。
- 没有路由的项目(React Native、组件库):没有"入口路由",结构树以**组件**
  为根,照样给依赖和速查表。
- 约定对不上时别硬套模板的结构树——以"能让人快速看懂"为准,该简化就简化。
