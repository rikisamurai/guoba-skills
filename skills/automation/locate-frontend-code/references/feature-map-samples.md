# 功能地图样例集

skill 的最终交付物长这样。以下都是对 qr-vault 真实功能产出的功能地图,**每个
路径/行号都经过 `Read` 核对**。把它们当"好产出"的标杆——风格统一:结构树 +
速查表 + 数据流。

> 另外两个样例在别处:**合集管理**见 `SKILL.md`(模板教学样例);**导入导出**
> 见 `example-outputs.md` §0(演示"加速器原始输出 → 归纳成地图")。

---

## 工作区(首页)  /

```
# 功能:工作区(QR 总览)  (/)
库的主界面:搜索/筛选所有 QR,选中后在右侧查看与操作。

## 结构
src/app/workspace-page.tsx                页面容器:搜索/筛选/选中/删除状态编排
├─ workspace/workspace-header.tsx         顶部:搜索框 + 筛选 + 新建入口   渲染@:158
├─ workspace/qr-list.tsx                  中部:QR 列表(按筛选/搜索结果)  渲染@:168
│  └─ workspace/qr-row-actions.tsx        单行操作:复制 URL/分享/删除
│     └─ workspace/action-tooltip.tsx     操作按钮的 tooltip 封装
├─ workspace/qr-inspector.tsx             右侧:选中 QR 的预览与操作(含空态) 渲染@:184
└─ workspace/types.ts                     ActiveFilter / WorkspaceQr 类型
   ↘ 依赖 lib/vault.ts(搜索/排序/分组)、lib/storage.ts(deleteQr)、
          lib/qr.ts(下载)、lib/url.ts(分享链接)

## 速查表
| 想改什么 | 位置 |
|---|---|
| 删除 QR 逻辑 | `handleDelete()` @ workspace-page.tsx:71 |
| 搜索/筛选/排序算法 | `searchQrs`/`sortQrsByRecent`/`getQrsForCollection` @ lib/vault.ts |
| 列表行的复制/分享/删除按钮 | qr-row-actions.tsx:16 |
| 右侧预览面板 / 空态文案 | qr-inspector.tsx:24 / i18n `workspace.emptyVault` |
| 顶部搜索框与筛选 | workspace-header.tsx |

## 数据流
输入搜索/切筛选 → `searchQrs`/`sortQrsByRecent` 过滤 → `QrList` 渲染 →
点某行 → `selectedId` → `QrInspector` 展示;点删除 → `handleDelete()` →
`deleteQr` → 写 storage → 重渲染。
```

---

## QR 详情 / 新建  /q/$qrId  ·  /new

```
# 功能:QR 详情与编辑  (/q/$qrId、/new)
新建或编辑单个 QR:填标题/描述/URL/所属合集,实时预览,生成分享链接。

## 结构
src/app/qr-detail-page.tsx                页面容器:表单状态、保存/另存、URL 解析
├─ qr-detail/qr-detail-form-card.tsx      主表单:标题/描述/URL/合集        渲染@:156
├─ qr-detail/preview-panel.tsx            实时预览 + 下载 PNG               渲染@:176
├─ qr-detail/url-utilities-panel.tsx      URL 解析详情(parsedUrl)         渲染@:186
├─ qr-detail/share-utility-panel.tsx      分享链接生成/复制                 渲染@:187
├─ qr-detail/mobile-url-preview.tsx       移动端 URL 预览
└─ qr-detail/not-found-card.tsx           查无此 QR 时的占位               渲染@:138
   ↘ 依赖 lib/storage.ts(upsertQr)、lib/url.ts(parseDeepLink/buildShareUrl)

## 速查表
| 想改什么 | 位置 |
|---|---|
| 保存逻辑 | `saveQr()` @ qr-detail-page.tsx:80 |
| 另存为新 QR | `saveAsNew()` @ qr-detail-page.tsx:93 |
| URL 解析 / 分享链接拼装 | `parseDeepLink`/`buildShareUrl` @ page.tsx:47/:48 (lib/url.ts) |
| 表单字段 UI | qr-detail-form-card.tsx |
| 预览/下载 PNG | preview-panel.tsx:19 |
| 查无此 QR 的展示 | not-found-card.tsx(渲染@page.tsx:138) |

## 数据流
编辑表单 → `saveQr()` → `upsertQr(...)` → 写 storage → `navigate('/q/$qrId')`;
URL 变化 → `parseDeepLink(url)` → 驱动预览/解析/分享三块。
```

---

## 分享页(只读落地页)  /share

```
# 功能:分享落地页  (/share?url=...&title=...)
通过分享链接打开的独立页面(不在主 shell 内):展示对方分享的 QR,可保存到自己的库。

## 结构
src/app/share-page.tsx                    页面容器:解析 search 参数、保存到库
├─ share/share-header.tsx                 顶部品牌/导航                    渲染@:85
├─ share/share-hero.tsx                   主视觉:大 QR + 复制分享链接      渲染@:88
├─ share/share-qr-details.tsx             标题/URL 详情(生成 dataUrl)     渲染@:95
├─ share/share-actions.tsx                操作区:原始 URL 展示 + 按钮       渲染@:96
└─ share/share-footer.tsx                 页脚                            渲染@:108
   ↘ 依赖 lib/url.ts(parseDeepLink)、lib/storage.ts(upsertQr)、
          lib/qr.ts(下载)、lib/ids.ts(nanoid8)

## 速查表
| 想改什么 | 位置 |
|---|---|
| 解析分享链接参数 | `parseDeepLink(url)` @ share-page.tsx:30 |
| "保存到我的库" | `upsertQr` + `navigate('/q/$qrId')` @ share-page.tsx:42/:50 |
| 大图 QR / 复制按钮 | share-hero.tsx:14 / i18n `common.copyShareUrl` |
| 原始 URL 展示 | share-actions.tsx:17 / i18n `share.rawUrl` |

## 数据流
打开 `/share?url=...` → `parseDeepLink` 解析 → Hero/Details/Actions 展示 →
点"保存" → `upsertQr` → 写 storage → `navigate('/q/$qrId')` 进入详情。
```

---

## 这些样例的共性(产出时照着抄)

- **结构树**用缩进体现"页面 → 模块 → 子模块",右侧对齐一句话职责;非 UI 依赖
  用 `↘ 依赖` 收尾,不混进树里。
- **速查表**只放"最常被改的点",每行给到 `file:line` 或 i18n key,不堆砌。
- **数据流**一两行串起"事件 → 函数 → 存储 → 渲染/跳转",让人看懂闭环。
- 行号都核对过;模块职责来自实际读文件(标题文案/aria-label/CardTitle),不靠猜。
