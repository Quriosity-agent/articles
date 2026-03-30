# pretext：不碰 DOM 就能算出文本高度的纯 JS 库

> **Repo:** [chenglou/pretext](https://github.com/chenglou/pretext) · TypeScript · npm: `@chenglou/pretext`
> **作者:** Cheng Lou（React Motion、Reason/ReScript 作者，前 Meta/Facebook）
> **Demo:** [chenglou.me/pretext](https://chenglou.me/pretext/)

## 一句话总结

pretext 用 canvas `measureText()` 做一次性预计算，之后所有布局计算都是纯算术——500 条文本的 `layout()` 只要 ~0.09ms，零 DOM 交互。支持中日韩、阿拉伯语、emoji、混合双向文本，输出可以渲染到 DOM、Canvas、SVG、WebGL。

## 它解决什么问题？

浏览器里测量文本高度（`getBoundingClientRect`、`offsetHeight`）会触发同步 layout reflow——浏览器最贵的操作之一。虚拟滚动列表要知道每行高度？聊天气泡要 resize？瀑布流卡片要定尺寸？每次测量都迫使浏览器重新计算整个文档布局。

**具体痛点：**
- **虚拟化列表**：mount 前要知道每行精确高度，目前只能靠猜（estimatedRowHeight）或者先渲染再测量
- **瀑布流/Masonry**：文字多的卡片不知道多高，布局算不准
- **布局偏移 (CLS)**：新文本加载后页面跳动，因为之前没预留准确空间
- **收缩宽度 (shrink-wrap)**：多行文本的最紧容器宽度，CSS 算不出来
- **文字环绕浮动元素**：每行宽度不同，传统测量方案彻底失效

## 核心设计：prepare + layout 两阶段

```
┌──────────────────────────────────────────────────────┐
│  Phase 1: prepare(text, font)                         │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ 空白归一化  │→│ 文本分段      │→│ canvas       │  │
│  │ + 胶水规则  │  │ (Segmenter)  │  │ measureText  │  │
│  └────────────┘  └──────────────┘  └──────────────┘  │
│  一次性调用，返回 opaque handle                        │
├──────────────────────────────────────────────────────┤
│  Phase 2: layout(prepared, maxWidth, lineHeight)      │
│  ┌──────────────────────────────────────────────┐    │
│  │ 纯算术：遍历缓存宽度 → 折行 → 算高度          │    │
│  │ 无 canvas、无 DOM、无字符串操作                 │    │
│  └──────────────────────────────────────────────┘    │
│  每次 resize 都调用，500 条 ~0.09ms                   │
└──────────────────────────────────────────────────────┘
```

关键原则：**同一段文本只 `prepare()` 一次**。窗口 resize 时只重新调用 `layout()`——这是纯算术，极快。

## 用法

### 用例 1：只要高度（最常见）

```ts
import { prepare, layout } from '@chenglou/pretext'

const prepared = prepare('AGI 春天到了. بدأت الرحلة 🚀', '16px Inter')
const { height, lineCount } = layout(prepared, containerWidth, 20)
// 纯算术，零 DOM reflow
```

需要 textarea 式的空白保留？加 `{ whiteSpace: 'pre-wrap' }`：

```ts
const prepared = prepare(textareaValue, '16px Inter', { whiteSpace: 'pre-wrap' })
const { height } = layout(prepared, textareaWidth, 20)
```

### 用例 2：需要每行的文本内容

换用 `prepareWithSegments` + `layoutWithLines`，拿到每行的文字、宽度和游标：

```ts
import { prepareWithSegments, layoutWithLines } from '@chenglou/pretext'

const prepared = prepareWithSegments('AGI 春天到了', '18px "Helvetica Neue"')
const { lines } = layoutWithLines(prepared, 320, 26)
for (let i = 0; i < lines.length; i++) {
  ctx.fillText(lines[i].text, 0, i * 26)  // 渲染到 Canvas
}
```

### 用例 3：算收缩宽度 (shrink-wrap)

`walkLineRanges` 不构建文本字符串，只回调每行宽度——适合二分搜索最优宽度：

```ts
let maxW = 0
walkLineRanges(prepared, 320, line => {
  if (line.width > maxW) maxW = line.width
})
// maxW = 最宽行的实际宽度 = 最紧的容器宽度
// 这个"多行文本 shrink-wrap"在 web 上一直缺失
```

### 用例 4：文字环绕浮动元素

`layoutNextLine` 逐行布局，每行可以用不同宽度：

```ts
let cursor = { segmentIndex: 0, graphemeIndex: 0 }
let y = 0

while (true) {
  // 图片旁边的行更窄
  const width = y < image.bottom ? columnWidth - image.width : columnWidth
  const line = layoutNextLine(prepared, cursor, width)
  if (line === null) break
  ctx.fillText(line.text, 0, y)
  cursor = line.end
  y += 26
}
```

这些 API 让你可以把文本渲染到 Canvas、SVG、WebGL——不再局限于 DOM。

## 性能数据

基于 repo 内置的 benchmark（500 条文本）：

| 阶段 | 耗时 |
|---|---|
| `prepare()` | ~19ms（一次性） |
| `layout()` | **~0.09ms**（每次 resize） |

`layout()` 是纯算术，0.09ms 处理 500 条文本意味着 resize 时的重布局基本免费。

## 语言支持

pretext 不是只做英文的库。README 的示例代码直接混了中文、阿拉伯语和 emoji：

```ts
prepare('AGI 春天到了. بدأت الرحلة 🚀', '16px Inter')
```

支持的语言特性：
- **CJK（中日韩）**：逐字符断行 + 禁则处理（kinsoku shori），`，。」` 不会出现在行首
- **双向文本 (Bidi)**：实现了 Unicode 双向算法 (UAX #9)，纯 LTR 走快速路径零开销
- **Emoji**：处理了 Chrome/Firefox macOS 上 <24px 字号的 emoji 宽度偏差
- **混合脚本**：同一段文本里混中英阿 emoji 全部正确处理
- **浏览器怪癖**：针对不同浏览器的特定行为做了适配

## API 一览

**用例 1（只要高度）：**
- `prepare(text, font, options?)` → `PreparedText`
- `layout(prepared, maxWidth, lineHeight)` → `{ height, lineCount }`

**用例 2（完整行数据）：**
- `prepareWithSegments(text, font, options?)` → `PreparedTextWithSegments`
- `layoutWithLines(prepared, maxWidth, lineHeight)` → `{ height, lineCount, lines }`
- `walkLineRanges(prepared, maxWidth, onLine)` → 逐行回调宽度和游标
- `layoutNextLine(prepared, start, maxWidth)` → 迭代器式逐行布局

**工具函数：**
- `clearCache()` — 清除内部缓存（字体/文本变体很多时有用）
- `setLocale(locale?)` — 设置 locale（同时清缓存）

## 当前限制

直说：
- 默认只支持 `white-space: normal` 和 `pre-wrap`，`word-break: normal`，`overflow-wrap: break-word`
- `line-height` 必须手动传入，不会自动推断
- macOS 上 `system-ui` 字体在 canvas 和 DOM 解析到不同变体，用具名字体更安全
- 极窄宽度下会在 grapheme 边界断词（因为 `overflow-wrap: break-word`）

## 谁应该看这个？

- **做虚拟滚动的**：终于不用猜 estimatedRowHeight 了
- **做聊天/消息 UI 的**：气泡高度预测，resize 无卡顿
- **做瀑布流的**：文字卡片提前算准高度
- **在乎 CLS 的**：渲染前预留准确空间
- **想把文本渲染到 Canvas/SVG/WebGL 的**：layoutWithLines 直接给你每行文本

## 我的看法

Cheng Lou 不是随便什么人——React Motion 证明了他对动画的理解，Reason/ReScript 证明了他对编程语言的理解。现在 pretext 证明他对文本布局的理解。

这个库的设计哲学很清晰：把一次性的重活（分词、测量）和热路径的轻活（纯算术布局）彻底分开。`prepare()` 19ms 做完所有脏活，之后 `layout()` 0.09ms 处理 500 条文本。浏览器 resize 时你的 JS 基本不花时间在文本布局上。

特别值得注意的是多语言支持不是后加的。README 的第一个示例就混了中文、阿拉伯语和 emoji。CJK 禁则处理、bidi 算法、emoji 宽度修正——这些都是从第一天就考虑的。

已经发布到 npm（`@chenglou/pretext`），有 [live demo](https://chenglou.me/pretext/)，API 分层合理（只要高度用简单 API，要行数据用高级 API）。这不是实验性质的东西，是可以直接用的。

---

> 📎 更多信息见 [chenglou/pretext](https://github.com/chenglou/pretext) · Demo: [chenglou.me/pretext](https://chenglou.me/pretext/) · npm: `@chenglou/pretext`

🦞
