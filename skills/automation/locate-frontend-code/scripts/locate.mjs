#!/usr/bin/env node
// locate.mjs —— 分层前端代码定位器:page -> module -> code。
//
// 给一条线索(路由 / 一段界面文字 / 符号或组件名),它会按人读前端仓库的
// 顺序跑一串 grep:
//   1. PAGE   —— 把路由/页面名解析到页面组件文件。
//   2. MODULE —— 列出页面隔壁的模块/"card"文件夹 + 它的 import。
//   3. CODE   —— 钉到具体的符号 / i18n key / 字面字符串。
//
// 它是约定驱动的,不锁死框架。认得常见的 React/Vue 形态(TanStack Router、
// React Router <Route path=>、Next.js app 目录、Vue Router)和 i18next 风格的
// 语言包 JSON。线索匹配不上已知形态时,退回普通 ripgrep,保证仍有命中。
//
// 用法:
//   node locate.mjs "<线索>" [--root <目录>] [--type route|text|symbol|auto]
//
// 示例:
//   node locate.mjs /collections
//   node locate.mjs "导出 JSON 快照"
//   node locate.mjs CollectionFormCard
//
// 输出按 PAGE / MODULE / CODE 分组,带可点击的 file:line 引用。

import { execFileSync } from 'node:child_process'
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs'
import { basename, dirname, isAbsolute, join, relative, resolve as resolvePath } from 'node:path'

const args = process.argv.slice(2)
let root = process.cwd()
let type = 'auto'
const positional = []
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--root') root = args[++i]
  else if (args[i] === '--type') type = args[++i]
  else positional.push(args[i])
}
const clue = positional.join(' ').trim()

if (!clue) {
  console.error('usage: node locate.mjs "<clue>" [--root <dir>] [--type route|text|symbol|auto]')
  process.exit(2)
}

// 优先用 ripgrep;没有 rg 就退回 git grep。
function hasRg() {
  try {
    execFileSync('rg', ['--version'], { stdio: 'ignore' })
    return true
  } catch {
    return false
  }
}
const RG = hasRg()

// 跑一次定值或正则搜索,返回 [{file, line, text}]。
function search(pattern, { fixed = false, glob = null, max = 60 } = {}) {
  try {
    let out
    if (RG) {
      const a = ['--line-number', '--no-heading', '--color', 'never']
      if (fixed) a.push('--fixed-strings')
      if (glob) a.push('--glob', glob)
      a.push('--max-count', String(max), pattern, root)
      out = execFileSync('rg', a, { encoding: 'utf8', maxBuffer: 1 << 24 })
    } else {
      // git grep 兜底。用 -P(Perl)让 ripgrep 那套正则(`(?:…)`、`\b`、
      // `{n}`、`?`)也能用;-F 走定值字符串。cwd=root,所以不带路径参数。
      // 只搜被 git 跟踪的文件 —— 作为兜底够用。
      const a = ['grep', '-nI', '--color=never']
      a.push(fixed ? '-F' : '-P')
      a.push('-e', pattern)
      out = execFileSync('git', a, { encoding: 'utf8', maxBuffer: 1 << 24, cwd: root })
    }
    return out
      .split('\n')
      .filter(Boolean)
      .map((l) => {
        const m = l.match(/^(.*?):(\d+):(.*)$/)
        if (!m) return null
        // ripgrep 打印绝对路径(我们传了绝对 root);git grep 打印相对 cwd
        // (=root)的路径。统一归一化成绝对路径。
        const file = isAbsolute(m[1]) ? m[1] : join(root, m[1])
        return { file, line: Number(m[2]), text: m[3].trim() }
      })
      .filter(Boolean)
      .filter((h) => !/node_modules|\/dist\/|\/build\/|\.min\./.test(h.file))
  } catch {
    return []
  }
}

const rel = (f) => relative(root, f) || f
function printHits(hits, { limit = 12 } = {}) {
  if (!hits.length) {
    console.log('   (none)')
    return
  }
  for (const h of hits.slice(0, limit)) {
    console.log(`   ${rel(h.file)}:${h.line}  ${h.text.slice(0, 100)}`)
  }
  if (hits.length > limit) console.log(`   … +${hits.length - limit} more`)
}

function detectType(c) {
  if (c.startsWith('/')) return 'route'
  // 驼峰 / 带连字符 / 无空格 -> 很可能是符号、组件名或文件名
  if (!/\s/.test(c) && /[A-Za-z]/.test(c) && !/[一-鿿]/.test(c)) return 'symbol'
  return 'text'
}
const kind = type === 'auto' ? detectType(clue) : type

console.log(`\n🔎 clue: ${JSON.stringify(clue)}   type: ${kind}   root: ${rel(root)}\n`)

// --- PAGE 层:把路由/页面名解析到页面组件文件。 ---
function resolvePageComponent(componentName) {
  // 找到定义 `export ... componentName` 或默认导出的那个文件。
  // 允许 `export default`、`export async function`、`export default async function`。
  const defs = search(
    `(export\\s+(default\\s+)?(async\\s+)?(function|const|class)\\s+${componentName}\\b|export\\s+\\{[^}]*\\b${componentName}\\b)`,
    { glob: '*.{tsx,jsx,ts,js,vue}' },
  )
  return defs
}

// kebab-case -> PascalCase(qr-card -> QrCard),给"传了文件名当符号"的情况兜底。
function kebabToPascal(s) {
  return s.split(/[-_]/).filter(Boolean).map((w) => w[0].toUpperCase() + w.slice(1)).join('')
}

// 递归列出某个 app-router 根目录下的所有 page 文件,并算出它对应的路由。
// 路由组 `(group)` 段会被剥掉,动态段 `[id]` 保留。
function walkAppPages(appRoot) {
  const out = []
  if (!existsSync(appRoot)) return out
  const walk = (dir) => {
    let entries
    try {
      entries = readdirSync(dir, { withFileTypes: true })
    } catch {
      return
    }
    for (const e of entries) {
      const full = join(dir, e.name)
      if (e.isDirectory()) {
        if (e.name === 'node_modules' || e.name.startsWith('.')) continue
        walk(full)
      } else if (/^page\.(tsx|jsx|ts|js)$/.test(e.name)) {
        const routeSegs = relative(appRoot, dir)
          .split('/')
          .filter((s) => s && !/^\(.*\)$/.test(s)) // 去掉路由组 (xxx)
        out.push({ file: full, segs: routeSegs })
      }
    }
  }
  walk(appRoot)
  return out
}

// 路由段匹配:长度一致,且每段相等或文件路由那段是动态段 `[x]`。
function routeSegsMatch(fileSegs, querySegs) {
  if (fileSegs.length !== querySegs.length) return false
  return fileSegs.every((fs, i) => fs === querySegs[i] || /^\[.*\]$/.test(fs))
}

// 把 import 说明符(在 `fromFile` 里)解析到磁盘上的具体文件。
// 处理 `@/` -> src/ 别名(Vite/Next 默认)以及相对路径。
function resolveSpecifier(spec, fromFile) {
  let base
  if (spec.startsWith('@/')) base = join(root, 'src', spec.slice(2))
  else if (spec.startsWith('.')) base = resolvePath(dirname(fromFile), spec)
  else return null
  for (const ext of ['', '.tsx', '.jsx', '.ts', '.js', '.vue', '/index.tsx', '/index.ts']) {
    if (existsSync(base + ext) && statSync(base + ext).isFile()) return base + ext
  }
  return null
}

// 在 router/源码文件里找到 componentName 是从哪 import 的,并解析出文件。
function fileForComponent(componentName, routerFiles) {
  for (const rf of routerFiles) {
    if (!existsSync(rf)) continue
    const src = readFileSync(rf, 'utf8')
    const m = src.match(
      new RegExp(`import\\s+(?:\\{[^}]*\\b${componentName}\\b[^}]*\\}|${componentName})\\s+from\\s+['"\`]([^'"\`]+)['"\`]`),
    )
    if (m) {
      const f = resolveSpecifier(m[1], rf)
      if (f) return f
    }
  }
  // 兜底:在整棵树里按名字找定义。
  const defs = resolvePageComponent(componentName)
  return defs.length ? defs[0].file : null
}

// 从深层文件反向往上走到拥有它的页面。约定:
// src/app/<feature>/anything.tsx  ->  src/app/<feature>-page.tsx
function owningPage(file) {
  const r = rel(file)
  const m = r.match(/(.*\/app)\/([^/]+)\/.+\.(tsx|jsx|ts|js|vue)$/)
  if (!m) return null
  for (const ext of ['tsx', 'jsx', 'vue', 'ts', 'js']) {
    const p = join(root, `${m[1]}/${m[2]}-page.${ext}`)
    if (existsSync(p)) return p
  }
  return null
}
function printOwningPages(files) {
  const pages = [...new Set(files.map(owningPage).filter(Boolean))]
  if (pages.length) {
    console.log('\n   ↳ owning page(s):')
    for (const p of pages) console.log(`     ${rel(p)}`)
  }
}

function pageLayer() {
  if (kind === 'route') {
    console.log('① PAGE — route → page component:')
    // 1) 文件路由(Next.js app/pages 目录)。走递归扫描,能处理路由组
    //    `(admin)` 和动态段 `[id]`(实参 /c/123 也能匹配到 c/[id])。
    const seg = clue.replace(/^\/+|\/+$/g, '')
    const querySegs = seg ? seg.split('/') : []
    const fileRouted = []
    for (const appRoot of [join(root, 'src/app'), join(root, 'app')]) {
      for (const pg of walkAppPages(appRoot)) {
        if (routeSegsMatch(pg.segs, querySegs)) fileRouted.push(pg.file)
      }
    }
    // pages-router 兜底:pages/<seg>.tsx 或 pages/<seg>/index.tsx
    for (const p of [
      join(root, 'src/pages', `${seg || 'index'}.tsx`),
      join(root, 'pages', `${seg || 'index'}.tsx`),
      join(root, 'src/pages', seg, 'index.tsx'),
      join(root, 'pages', seg, 'index.tsx'),
    ]) {
      if (existsSync(p)) fileRouted.push(p)
    }
    if (fileRouted.length) {
      for (const p of [...new Set(fileRouted)]) console.log(`   (file-based route)  ${rel(p)}`)
      return [...new Set(fileRouted)]
    }
    // 2) 配置式路由(TanStack/React Router)。先找到 path 字面量,
    //    再扫它所在的 createRoute/<Route> 块,取组件名。
    const pathHits = search(`path:\\s*['"\`]${clue}['"\`]|path=['"\`]${clue}['"\`]`)
    const routerFiles = [...new Set(pathHits.map((h) => h.file))]
    if (!pathHits.length) console.log('   (no `path:` literal found — falling back to raw matches)')
    const comps = new Set()
    for (const h of pathHits) {
      const lines = readFileSync(h.file, 'utf8').split('\n')
      // 同一个路由块里 `component:` 在 `path:` 之后,所以从 path 行往下扫,
      // 到块边界停(下一个路由的 `path:`/`createRoute`,或闭合的 `})`)。
      // 这样避免串到上一个路由的组件。
      for (let i = h.line - 1; i < Math.min(lines.length, h.line + 12); i++) {
        if (i > h.line - 1 && /createRoute|getParentRoute|^\s*const\s|path:\s*['"`]/.test(lines[i])) break
        const cm =
          lines[i].match(/component:\s*([A-Z][A-Za-z0-9_]+)/) ||
          lines[i].match(/element=\{?\s*<([A-Z][A-Za-z0-9_]+)/) ||
          lines[i].match(/Component=\{([A-Z][A-Za-z0-9_]+)\}/)
        if (cm) {
          comps.add(cm[1])
          break
        }
        if (/^\s*\}\)/.test(lines[i]) && i > h.line - 1) break
      }
    }
    const pageFiles = []
    for (const c of comps) {
      const f = fileForComponent(c, routerFiles)
      console.log(`   ${clue}  →  ${c}  →  ${f ? rel(f) : '(file not resolved)'}`)
      if (f) pageFiles.push(f)
    }
    if (!comps.size) {
      console.log('   route lines:')
      printHits(pathHits.length ? pathHits : search(clue, { fixed: true }))
    }
    return pageFiles
  }
  // 直接给的是页面名 / 符号名
  console.log('① PAGE — definition(s) by name:')
  let defs = resolvePageComponent(clue)
  // 兜底:传的是 kebab 文件名(qr-card)而组件其实叫 PascalCase(QrCard)。
  if (!defs.length && /[-_]/.test(clue)) {
    const pascal = kebabToPascal(clue)
    defs = resolvePageComponent(pascal)
    if (defs.length) console.log(`   (kebab "${clue}" → 组件名 "${pascal}")`)
  }
  printHits(defs)
  return defs.map((d) => d.file)
}

// --- MODULE 层:页面隔壁的 "card"/模块文件夹 + 它的 import。 ---
function moduleLayer(pageFiles) {
  console.log('\n② MODULE — sub-modules ("cards") under the page + its imports:')
  if (!pageFiles || !pageFiles.length) {
    console.log('   (resolve a page first; re-run with the page name as the clue)')
    return
  }
  for (const pf of pageFiles.slice(0, 3)) {
    const file = typeof pf === 'string' ? pf : pf.file
    if (!existsSync(file)) continue
    const dir = dirname(file)
    // 约定:src/app/<feature>-page.tsx -> src/app/<feature>/*
    const base = basename(file).replace(/-page\.(tsx|jsx|ts|js|vue)$/, '').replace(/\.(tsx|jsx|ts|js|vue)$/, '')
    const candidates = [join(dir, base), join(dir, basename(file).replace(/\.[^.]+$/, ''))]
    let listed = false
    for (const folder of candidates) {
      if (existsSync(folder) && statSync(folder).isDirectory()) {
        console.log(`   module folder: ${rel(folder)}/`)
        for (const f of readdirSync(folder).filter((n) => /\.(tsx|jsx|ts|js|vue)$/.test(n))) {
          console.log(`     - ${rel(join(folder, f))}`)
        }
        listed = true
      }
    }
    if (!listed) console.log(`   (no sibling module folder for ${rel(file)} — see its imports below)`)
    // 页面文件里的本地 import = 它拼装的模块。
    const imports = search(`import .* from '(\\.|@/)`, { glob: rel(file) }).filter((h) =>
      h.file === file,
    )
    if (imports.length) {
      console.log(`   local imports in ${rel(file)}:`)
      printHits(imports, { limit: 20 })
    }
  }
}

// --- CODE 层:钉到具体的符号 / i18n key / 字面文字。 ---
function codeLayer() {
  console.log('\n③ CODE — exact locations:')
  if (kind === 'text') {
    // i18next 反查:在语言包 JSON 里找到字符串值,推出 key。
    const locHits = search(clue, { fixed: true, glob: '*.json' }).filter((h) =>
      /locale|i18n|lang|messages|translation/i.test(h.file),
    )
    if (locHits.length) {
      console.log('   i18n locale matches (value → key):')
      const keys = new Set()
      for (const h of locHits) {
        const m = h.text.match(/^"([^"]+)"\s*:/)
        if (m) keys.add(m[1])
        console.log(`     ${rel(h.file)}:${h.line}  ${h.text.slice(0, 90)}`)
      }
      if (keys.size) {
        console.log('\n   ↳ leaf keys used in code (grep the key to find the component):')
        for (const k of keys) {
          const usages = search(`['"\`][^'"\`]*${k}['"\`]`, { glob: '*.{tsx,jsx,ts,js,vue}' }).filter(
            (h) => !/locale|i18n\/locales/i.test(h.file),
          )
          if (usages.length) {
            console.log(`     key "${k}":`)
            printHits(usages, { limit: 8 })
            printOwningPages(usages.map((u) => u.file))
          }
        }
      }
    }
    // 另外:这段字面文字也可能是直接硬编码在组件里的。
    const lit = search(clue, { fixed: true, glob: '*.{tsx,jsx,vue}' })
    console.log('\n   hardcoded literal in components:')
    printHits(lit)
    return
  }
  // 符号/路由的兜底:定义 + 调用处。
  // 传的若是 kebab 文件名(qr-card)而组件叫 PascalCase(QrCard),自动换算。
  let name = clue
  if (/[-_]/.test(clue) && !search(`(function|const|class) ${clue}\\b`, { glob: '*.{tsx,jsx,ts,js,vue}', max: 1 }).length) {
    name = kebabToPascal(clue)
    if (name !== clue) console.log(`   (kebab "${clue}" → 符号 "${name}")`)
  }
  const defs = search(`(async )?(function|const|class) ${name}\\b`, { glob: '*.{tsx,jsx,ts,js,vue}' })
  console.log('   definition:')
  printHits(defs)
  const usages = search(`\\b${name}\\b`, { glob: '*.{tsx,jsx,ts,js,vue}' })
  console.log('   usages:')
  printHits(usages, { limit: 10 })
  printOwningPages([...defs.map((d) => d.file), ...usages.map((u) => u.file)])
}

// --- 依次驱动三层 ---
let pageFiles = []
if (kind === 'route' || kind === 'symbol') pageFiles = pageLayer()
else console.log('① PAGE — (text clue: jump to CODE layer, then walk up to the page)')
if (kind !== 'text') moduleLayer(pageFiles)
codeLayer()
console.log('')
