# pretext: Multiline Text Measurement & Layout Without DOM Reflow

> **Repo:** [chenglou/pretext](https://github.com/chenglou/pretext) · TypeScript · npm: `@chenglou/pretext`
> **Author:** Cheng Lou (creator of React Motion, Reason/ReScript, ex-Meta/Facebook)
> **Demo:** [chenglou.me/pretext](https://chenglou.me/pretext/)

## TL;DR

pretext is a pure JS/TS library that measures and lays out multiline text without touching the DOM. One-time `prepare()` does segmentation + canvas measurement; subsequent `layout()` calls are pure arithmetic — ~0.09ms for 500 texts. Supports CJK, bidi (Arabic/Hebrew), emoji, mixed scripts. Renders to DOM, Canvas, SVG, WebGL, and eventually server-side.

## The Problem

Measuring text height in the browser (`getBoundingClientRect`, `offsetHeight`) triggers synchronous layout reflow — one of the most expensive browser operations. For virtual scrolling lists, chat UIs, masonry grids, and anything that needs to know text dimensions before rendering, this is a fundamental bottleneck.

**Where it hurts:**
- **Virtualized lists**: You need exact row heights before mount, but current solutions rely on `estimatedRowHeight` or render-then-measure hacks
- **Masonry layouts**: Text-heavy cards need upfront sizing that CSS can't provide
- **Layout shift (CLS)**: New text loads and the page jumps because you couldn't reserve accurate space
- **Shrink-wrap width**: The tightest container width for multiline text — CSS simply can't compute this
- **Text flowing around floats**: Each line has a different available width, breaking traditional measurement approaches entirely

## Core Design: Two-Phase Architecture

```
┌──────────────────────────────────────────────────────┐
│  Phase 1: prepare(text, font)                         │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ Normalize  │→│ Segment text │→│ canvas       │  │
│  │ whitespace │  │ + glue rules │  │ measureText  │  │
│  └────────────┘  └──────────────┘  └──────────────┘  │
│  Called once, returns an opaque handle                 │
├──────────────────────────────────────────────────────┤
│  Phase 2: layout(prepared, maxWidth, lineHeight)      │
│  ┌──────────────────────────────────────────────┐    │
│  │ Pure arithmetic: walk cached widths → wrap    │    │
│  │ lines → compute height                        │    │
│  │ No canvas, no DOM, no string operations       │    │
│  └──────────────────────────────────────────────┘    │
│  Called on every resize, 500 texts in ~0.09ms         │
└──────────────────────────────────────────────────────┘
```

The key principle: **`prepare()` once per text, `layout()` on every resize**. The hot path is pure arithmetic.

## Usage

### Use Case 1: Height Only (Most Common)

```ts
import { prepare, layout } from '@chenglou/pretext'

const prepared = prepare('AGI 春天到了. بدأت الرحلة 🚀', '16px Inter')
const { height, lineCount } = layout(prepared, containerWidth, 20)
// Pure arithmetic. Zero DOM reflow.
```

For textarea-like whitespace preservation, pass `{ whiteSpace: 'pre-wrap' }`:

```ts
const prepared = prepare(textareaValue, '16px Inter', { whiteSpace: 'pre-wrap' })
const { height } = layout(prepared, textareaWidth, 20)
```

### Use Case 2: Full Line Data

Switch to `prepareWithSegments` + `layoutWithLines` to get each line's text, width, and cursors:

```ts
import { prepareWithSegments, layoutWithLines } from '@chenglou/pretext'

const prepared = prepareWithSegments('AGI 春天到了', '18px "Helvetica Neue"')
const { lines } = layoutWithLines(prepared, 320, 26)
for (let i = 0; i < lines.length; i++) {
  ctx.fillText(lines[i].text, 0, i * 26)  // Render to Canvas
}
```

### Use Case 3: Shrink-Wrap Width

`walkLineRanges` calls back with each line's width without building text strings — perfect for binary-searching the optimal container width:

```ts
let maxW = 0
walkLineRanges(prepared, 320, line => {
  if (line.width > maxW) maxW = line.width
})
// maxW = widest line = tightest container width that fits the text
// This multiline "shrink-wrap" has been missing from the web
```

### Use Case 4: Text Flowing Around Floats

`layoutNextLine` lays out one line at a time with a different width each time:

```ts
let cursor = { segmentIndex: 0, graphemeIndex: 0 }
let y = 0

while (true) {
  const width = y < image.bottom ? columnWidth - image.width : columnWidth
  const line = layoutNextLine(prepared, cursor, width)
  if (line === null) break
  ctx.fillText(line.text, 0, y)
  cursor = line.end
  y += 26
}
```

These APIs unlock rendering to Canvas, SVG, WebGL — no longer confined to the DOM.

## Performance

From the repo's built-in benchmark (500 texts):

| Phase | Time |
|---|---|
| `prepare()` | ~19ms (one-time) |
| `layout()` | **~0.09ms** (per resize) |

`layout()` is pure arithmetic. 0.09ms for 500 texts means resize-time re-layout is essentially free.

## Language Support

pretext isn't an English-only library. The README's very first example mixes Chinese, Arabic, and emoji:

```ts
prepare('AGI 春天到了. بدأت الرحلة 🚀', '16px Inter')
```

What's supported:
- **CJK (Chinese, Japanese, Korean)**: Per-character line breaking + kinsoku shori rules (e.g., `，。」` never start a line)
- **Bidirectional text (Bidi)**: Full Unicode Bidirectional Algorithm (UAX #9), with a fast path for pure-LTR text (zero overhead)
- **Emoji**: Handles Chrome/Firefox macOS emoji width inflation at font sizes <24px
- **Mixed scripts**: Chinese + English + Arabic + emoji in the same string — all correct
- **Browser quirks**: Specific adaptations for per-browser rendering differences

## API Overview

**Use Case 1 (height only):**
- `prepare(text, font, options?)` → `PreparedText`
- `layout(prepared, maxWidth, lineHeight)` → `{ height, lineCount }`

**Use Case 2 (full line data):**
- `prepareWithSegments(text, font, options?)` → `PreparedTextWithSegments`
- `layoutWithLines(prepared, maxWidth, lineHeight)` → `{ height, lineCount, lines }`
- `walkLineRanges(prepared, maxWidth, onLine)` → per-line callback with widths and cursors
- `layoutNextLine(prepared, start, maxWidth)` → iterator-style one-line-at-a-time layout

**Utilities:**
- `clearCache()` — clear internal measurement caches
- `setLocale(locale?)` — set locale for future prepare calls (also clears cache)

## Current Limitations

Being direct:
- Supports `white-space: normal` and `pre-wrap` only; `word-break: normal`, `overflow-wrap: break-word`
- `line-height` must be passed explicitly — no auto-inference
- `system-ui` on macOS resolves differently between canvas and DOM — use named fonts
- Very narrow widths may break inside words at grapheme boundaries (due to `overflow-wrap: break-word`)

## Who Is This For?

- **Virtual scrolling builders**: No more `estimatedRowHeight` guesswork
- **Chat / messaging UI developers**: Accurate bubble heights, lag-free resize
- **Masonry layout builders**: Upfront sizing for text-heavy cards
- **CLS-conscious developers**: Reserve exact vertical space before render
- **Canvas/SVG/WebGL renderers**: `layoutWithLines` gives you per-line text data directly

## My Take

Cheng Lou has a track record. React Motion proved he understands animation. Reason/ReScript proved he understands programming languages. Now pretext proves he understands text layout.

The design philosophy is clean: separate the one-time heavy work (segmentation, measurement) from the hot-path lightweight work (pure arithmetic layout). `prepare()` does 19ms of upfront computation, then `layout()` handles 500 texts in 0.09ms. During browser resize, your JS spends essentially zero time on text layout.

The multilingual support isn't bolted on after the fact. The very first README example mixes Chinese, Arabic, and emoji. CJK kinsoku shori, the bidi algorithm, emoji width correction — all first-class concerns from day one.

It's published on npm (`@chenglou/pretext`), has [live demos](https://chenglou.me/pretext/), and the API is well-layered (simple API for heights, advanced API for line data). This isn't experimental — it's ready to use.

---

> 📎 More at [chenglou/pretext](https://github.com/chenglou/pretext) · Demo: [chenglou.me/pretext](https://chenglou.me/pretext/) · npm: `@chenglou/pretext`

🦞
