# pretext: Predict Text Block Heights Without Triggering DOM Reflow

> **Repo:** [somnai-dreams/pretext](https://github.com/somnai-dreams/pretext) · TypeScript · ⭐ 2 · Based on Sebastian Markbåge's text-layout research prototype

## TL;DR

pretext uses canvas `measureText()` + two-phase caching to turn "text block height prediction" from a DOM read operation into pure arithmetic — ~0.0002ms per block on resize, 0.11ms total for 500 comments, zero DOM interaction.

## The Problem

Measuring text height in the browser (`getBoundingClientRect`, `offsetHeight`) triggers synchronous layout reflow. When a virtual scrolling list needs to independently measure 500 comments, each measurement forces the browser to recompute layout for the entire document. Read/write interleaving on the resize hot path can easily cost 30ms+ per frame.

**Where it hurts:**
- Virtualized feeds / comment lists: need row heights before mount
- Masonry / card grids: text-heavy cards need upfront sizing
- Chat / messaging UIs: bubble heights must recompute on every width change
- Loading skeletons / CLS reduction: reserve accurate vertical space before render

## Core Idea: Two-Phase Measurement

```
┌───────────────────────────────────────────────────┐
│  Phase 1: prepare(text, font)                      │
│  ┌────────────┐  ┌─────────────┐  ┌────────────┐  │
│  │ Intl.      │→│ canvas      │→│ Cache word  │  │
│  │ Segmenter  │  │ measureText  │  │ widths     │  │
│  └────────────┘  └─────────────┘  └────────────┘  │
│  Called once when text first appears                │
├───────────────────────────────────────────────────┤
│  Phase 2: layout(block, maxWidth, lineHeight)      │
│  ┌────────────────────────────────────────────┐   │
│  │ Pure arithmetic: walk cached widths → count │   │
│  │ lines → multiply by lineHeight              │   │
│  │ No canvas, no DOM, no string ops            │   │
│  └────────────────────────────────────────────┘   │
│  Called on every resize, ~0.0002ms per block       │
└───────────────────────────────────────────────────┘
```

Usage is minimal:

```ts
import { prepare, layout } from './src/layout.ts'

// When text first appears
const block = prepare(commentText, '16px Inter')

// On every container width change (pure arithmetic, blazing fast)
const { height, lineCount } = layout(block, containerWidth, 19)
```

## Performance

500 comments, resize to new width (the hot path):

| Approach | Time | DOM-free |
|---|---|---|
| **pretext** | **0.11ms** | ✅ |
| DOM batch (write all, read all) | 0.18ms | ❌ |
| DOM interleaved (per-component) | Much worse in practice | ❌ |
| Sebastian's text-layout (no cache) | 30ms | ✅ |
| Sebastian's + word cache | 3ms | ✅ |

**0.11ms vs 30ms** — a 270× improvement. And because pretext never touches the DOM, it won't interrupt the browser's rendering pipeline.

## Accuracy

Tested across 4 fonts × 8 sizes × 8 widths × 30 i18n texts (7680 tests):

| Browser | Match Rate |
|---|---|
| Chrome | 99.96% |
| Safari | 99.92% |
| Firefox | 99.95% |
| Headless (HarfBuzz) | 100% |

Remaining mismatches are font-specific borderline pixel rounding issues (Georgia rounding, Courier New Korean, etc.), not algorithm errors.

## Key Technical Details

After reading the source (`src/layout.ts`), here are the designs worth noting:

### 1. Word Segmentation: Intl.Segmenter

Uses `Intl.Segmenter` with `word` granularity — natively handles CJK (per-character breaking), Thai, Arabic, and every script the browser supports. No npm dependencies (Sebastian's original used the `linebreak` package and non-standard `Intl.v8BreakIterator`).

### 2. Punctuation Merging

`"better."` is measured as one unit, not `"better"` + `"."`. Why: canvas measureText accumulates error when measuring individual characters — up to 2.6px at 28px font size without merging.

### 3. CJK Splitting + Kinsoku Shori

CJK character segments are re-split into individual graphemes (CSS allows line breaks between any CJK characters), but kinsoku shori rules ensure:
- `，。「」` etc. never start a line
- `（「《` etc. never end a line

The source hard-codes Unicode codepoint sets — simple and effective.

### 4. Emoji Correction

Chrome/Firefox on macOS inflate canvas-measured emoji widths at font sizes <24px. pretext detects this via one DOM calibration read, then auto-compensates in subsequent calculations. Safari is unaffected (correction = 0).

### 5. Bidi (Bidirectional Text)

Implements the Unicode Bidirectional Algorithm (UAX #9), but pure LTR text hits a fast path with zero overhead. Full bidi classification and embedding level computation only activate when RTL characters are present.

### 6. Cache Design

- Global `Map<font, Map<segment, width>>` cache
- Shared across text blocks ("the", "a", etc. are measured once)
- No eviction — grows monotonically (typically a few KB for single-font feeds)
- `clearCache()` available for manual eviction

## Limitations (Being Honest)

- Only supports default CSS config (`white-space: normal`, `word-break: normal`, `overflow-wrap: break-word`)
- Does not infer `line-height` — you must pass the exact value
- `system-ui` font resolves differently between canvas and DOM on macOS — use named fonts
- Server-side requires a canvas implementation (`@napi-rs/canvas` with registered fonts)

## Who Is This For?

- **Virtual scrolling list builders**: the most direct use case
- **Chat / messaging UI developers**: bubble height prediction, lag-free resize
- **Masonry / card layout builders**: upfront sizing for text-heavy cards
- **CLS-conscious developers**: reserve accurate space before render

## My Take

This library is small (~400 lines of TypeScript, single file) but solves a real performance problem. The two-phase design is elegant: prepare does the heavy lifting once (segmentation + measurement), layout does pure arithmetic, turning O(n × DOM) into O(n × addition).

The i18n support deserves special mention — CJK kinsoku shori, bidi, emoji correction weren't bolted on as afterthoughts. They emerged from running 7680 test cases and fixing edge cases one by one. RESEARCH.md documents the full exploration and is worth reading.

**However** — 2 stars, early-stage project, no npm package, no license, demo page is a TODO. If you're using this in production, fork it.

---

> 📸 *Repo screenshot from [somnai-dreams/pretext](https://github.com/somnai-dreams/pretext). Built on Sebastian Markbåge's [text-layout](https://github.com/chenglou/text-layout) research prototype.*

🦞
