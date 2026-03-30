# pretext：不触发 DOM reflow 就能预测文本高度的浏览器库

> **Repo:** [somnai-dreams/pretext](https://github.com/somnai-dreams/pretext) · TypeScript · ⭐ 2 · 基于 Sebastian Markbåge 的 text-layout 研究原型

## 一句话总结

pretext 用 canvas `measureText()` + 两阶段缓存，把「文本块高度预测」从 DOM 读取操作变成纯算术运算——每次 resize 只需 ~0.0002ms/块，500 条评论全部重新计算只要 0.11ms，零 DOM 交互。

## 它要解决什么问题？

浏览器里测量文本高度（`getBoundingClientRect`、`offsetHeight`）会触发同步 layout reflow。当你有一个虚拟滚动列表要独立测量 500 条评论的高度时，每次测量都迫使浏览器重新计算整个文档的布局。读写交错（read/write interleaving）在热路径上轻松吃掉 30ms+ 每帧。

**痛点场景：**
- 虚拟化 Feed / 评论列表：mount 前要知道每行高度
- 瀑布流卡片：文字多的卡片要提前算尺寸
- 聊天气泡：每次宽度变化都得重算高度
- 骨架屏 / CLS 优化：渲染前预留准确的垂直空间

## 核心思路：两阶段测量

```
┌─────────────────────────────────────────────────┐
│  Phase 1: prepare(text, font)                    │
│  ┌──────────┐  ┌───────────┐  ┌──────────────┐  │
│  │ Intl.    │→│ canvas    │→│ 缓存 word    │  │
│  │ Segmenter│  │ measureText│  │ widths       │  │
│  └──────────┘  └───────────┘  └──────────────┘  │
│  只在文本首次出现时调用一次                         │
├─────────────────────────────────────────────────┤
│  Phase 2: layout(block, maxWidth, lineHeight)    │
│  ┌──────────────────────────────────────────┐   │
│  │ 纯算术：遍历缓存宽度 → 计算行数 → 乘行高  │   │
│  │ 无 canvas、无 DOM、无字符串操作             │   │
│  └──────────────────────────────────────────┘   │
│  每次 resize 都调用，~0.0002ms/块               │
└─────────────────────────────────────────────────┘
```

用法极简：

```ts
import { prepare, layout } from './src/layout.ts'

// 文本首次出现时
const block = prepare(commentText, '16px Inter')

// 每次容器宽度变化时（纯算术，极快）
const { height, lineCount } = layout(block, containerWidth, 19)
```

## 性能数据

500 条评论，resize 到新宽度（热路径）：

| 方案 | 耗时 | 无 DOM |
|---|---|---|
| **pretext** | **0.11ms** | ✅ |
| DOM 批量读写 | 0.18ms | ❌ |
| DOM 逐条读写 | 远差于批量 | ❌ |
| Sebastian text-layout (无缓存) | 30ms | ✅ |
| Sebastian + word cache | 3ms | ✅ |

**0.11ms vs 30ms**，差了 270 倍。而且 pretext 完全不碰 DOM，意味着不会打断浏览器的渲染管线。

## 准确率

跨 4 种字体 × 8 种字号 × 8 种宽度 × 30 条 i18n 文本（7680 个测试）：

| 浏览器 | 匹配率 |
|---|---|
| Chrome | 99.96% |
| Safari | 99.92% |
| Firefox | 99.95% |
| Headless (HarfBuzz) | 100% |

剩余不匹配的都是字体特定的边界像素舍入问题（Georgia 舍入、Courier New 韩文等），不是算法错误。

## 关键技术细节

读完源码 `src/layout.ts`，几个值得关注的设计：

### 1. 分词策略：Intl.Segmenter

用 `Intl.Segmenter` 的 `word` 粒度做分词，天然支持 CJK（逐字符断行）、泰语、阿拉伯语等。不需要 npm 依赖（Sebastian 原版用了 `linebreak` 包和非标准的 `Intl.v8BreakIterator`）。

### 2. 标点合并

`"better."` 作为一个整体测量，而不是拆成 `"better"` + `"."`。原因：canvas measureText 对单个字符的测量存在累积误差，28px 字号下不合并标点最多差 2.6px。

### 3. CJK 拆分 + 禁则处理（kinsoku shori）

CJK 字符段被拆成单个 grapheme（CSS 允许任意 CJK 字符间断行），但禁则处理确保：
- `，。「」` 等标点不会出现在行首
- `（「《` 等不会出现在行尾

源码里直接硬编码了 Unicode 码点集合，简单粗暴但有效。

### 4. Emoji 修正

Chrome/Firefox 在 macOS 上对 <24px 字号的 emoji 会 inflate canvas 测量宽度。pretext 通过一次 DOM 校准读取来检测偏差，然后在后续计算中自动补偿。Safari 不受影响（correction = 0）。

### 5. Bidi 双向文本

实现了 Unicode 双向算法（UAX #9），但纯 LTR 文本走快速路径，零开销。只有包含 RTL 字符时才激活完整的 bidi 分类和嵌入层级计算。

### 6. 缓存设计

- 全局 `Map<font, Map<segment, width>>` 缓存
- 跨文本块共享（"the"、"a" 等高频词只测一次）
- 无驱逐策略，单调增长（单字体场景大约几 KB）
- 提供 `clearCache()` 手动清理

## 局限性（直说）

- 只支持默认 CSS 配置（`white-space: normal`, `word-break: normal`, `overflow-wrap: break-word`）
- 不推断 `line-height`，必须手动传入
- `system-ui` 字体在 macOS 上 canvas 和 DOM 解析到不同变体，建议用具名字体
- 服务端需要 canvas 实现（`@napi-rs/canvas` + 注册字体）

## 适合谁？

- **做虚拟滚动列表的人**：这是最直接的应用场景
- **做聊天/消息 UI 的人**：气泡高度预测，resize 无卡顿
- **做瀑布流/卡片布局的人**：文字密集型卡片的提前定尺寸
- **关心 CLS 指标的人**：渲染前就预留准确空间

## 我的看法

这个库很小（单文件 ~400 行 TypeScript），但解决了一个实实在在的性能问题。两阶段设计很优雅：prepare 做一次重活（分词 + 测量），layout 做纯算术，把 O(n × DOM) 变成 O(n × 加法)。

特别值得注意的是 i18n 支持——CJK 禁则处理、bidi、emoji 修正这些都不是拍脑袋加的，是跑了 7680 个测试用例逐个排查出来的。RESEARCH.md 里记录了完整的探索过程，值得一读。

**不过**，2 个 star 的早期项目，没有 npm 包，没有 license，没有 demo 页面（TODO 状态）。如果你要用在生产环境，建议 fork 一份。

---

> 📸 *repo 截图来自 [somnai-dreams/pretext](https://github.com/somnai-dreams/pretext)，repo 内容基于 Sebastian Markbåge 的 [text-layout](https://github.com/chenglou/text-layout) 研究原型*

🦞
