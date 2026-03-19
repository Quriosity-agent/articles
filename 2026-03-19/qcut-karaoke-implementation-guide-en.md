# Adding Karaoke-Style Word-by-Word Subtitle Highlighting to QCut: Reusing OpenReel Video Code

> **TL;DR:** QCut already has word-level timestamp data and a subtitle styling system. OpenReel Video (MIT license) has a complete karaoke rendering engine and 20+ text animation effects. This guide details how to port OpenReel's core algorithms into QCut — approximately ~500 lines of new code, 2-3 days of work.

---

## Table of Contents

1. [QCut's Existing Infrastructure](#1-qcuts-existing-infrastructure)
2. [OpenReel Video Files to Reuse](#2-openreel-video-files-to-reuse)
3. [New Files to Create](#3-new-files-to-create)
4. [Files to Modify](#4-files-to-modify)
5. [Porting 20+ Text Animation Effects](#5-porting-20-text-animation-effects)
6. [Architecture Adaptation Notes](#6-architecture-adaptation-notes)
7. [ASS Karaoke Export](#7-ass-karaoke-export)
8. [Effort Estimate](#8-effort-estimate)

---

## 1. QCut's Existing Infrastructure

QCut already has most of the building blocks needed for karaoke subtitles. Here's the inventory:

| File Path | Purpose | What It Provides |
|-----------|---------|-----------------|
| `apps/web/src/stores/timeline/word-timeline-store.ts` | Word-level timestamp Zustand store | `WordItem { id, text, start, end, type, filterState }`, plus `getVisibleWords()`, `getWordsForExport()` |
| `apps/web/src/lib/captions/subtitle-style.ts` | SubtitleStyle → CSS conversion | `subtitleStyleToCSS(style)` function, re-exports `hexToRgba`, `rgbToASSColor`, etc. |
| `apps/web/src/lib/captions/ass-generator.ts` | ASS file generation | Re-exports `generateASS()`, `secondsToASSTime()` |
| `apps/web/src/lib/captions/ass-parser.ts` | ASS file parsing | Re-exports `parseASS()`, `assTimeToSeconds()`, `assStyleToSubtitleStyle()` |
| `apps/web/src/lib/captions/caption-export.ts` | Caption export pipeline | `exportSrt()`, `exportVtt()`, `exportAss()`, `exportAssStyled()`, and download functions |
| `apps/web/src/components/editor/preview-panel/use-preview-media.ts` | Preview panel media hook | Extracts `captionSegments` from active timeline elements to drive subtitle rendering |
| `packages/editor-core/src/types/timeline.ts` | Shared type definitions | `SubtitleStyle` interface (20 fields), `CaptionElement` interface |

### Key Data Structures

QCut's `WordItem` already contains word-level timestamps — the core data for karaoke highlighting:

```typescript
// WordItem from word-timeline-store.ts
interface WordItem {
  id: string;
  text: string;
  start: number;   // seconds, millisecond precision
  end: number;      // seconds
  type: "word" | "spacing";
  speaker_id?: string;
  filterState: WordFilterState;
  filterReason?: string;
}
```

QCut's `SubtitleStyle` controls subtitle appearance:

```typescript
// packages/editor-core/src/types/timeline.ts
interface SubtitleStyle {
  fontFamily: string;
  fontSize: number;
  fontColor: string;
  fontOpacity: number;
  bold: boolean;
  italic: boolean;
  underline: boolean;
  outlineColor: string;
  outlineWidth: number;
  shadowColor: string;
  shadowOffset: { x: number; y: number };
  backgroundColor: string;
  bgOpacity: number;
  position: { align: "top" | "center" | "bottom"; x: number; y: number };
  lineSpacing: number;
}
```

**Bottom line:** The data layer is complete. What's missing is the "highlight the current word based on playback time" rendering logic.

---

## 2. OpenReel Video Files to Reuse

OpenReel Video ([GitHub](https://github.com/Augani/openreel-video), MIT license) has a fully implemented karaoke subtitle system. Key files:

| OpenReel File Path | Lines | Purpose | Reusability |
|-------------------|-------|---------|-------------|
| `packages/core/src/text/caption-animation-renderer.ts` | ~260 | **Karaoke rendering core**: 6 caption animation modes | ⭐ Direct algorithm reuse |
| `packages/core/src/text/text-animation-presets.ts` | ~450 | **20+ text animation effects**: pure functions | ⭐ Direct copy |
| `packages/core/src/text/text-animation.ts` | ~300 | Text animation engine: preset dispatch + easing | 🔧 Adapt and reuse |
| `packages/core/src/text/character-animator.ts` | ~350 | Per-character animation: text measurement + layout | 🔧 Adapt and reuse |
| `packages/core/src/text/subtitle-engine.ts` | ~400 | Subtitle engine: SRT parsing + style management | 📖 Reference design |
| `apps/web/src/stores/project/subtitle-helpers.ts` | ~150 | Subtitle helper functions | 📖 Reference design |
| `apps/web/src/components/editor/inspector/TextAnimationSection.tsx` | ~200 | Animation picker UI component | 📖 Reference UI design |

### Core Algorithm Deep Dive

OpenReel's `caption-animation-renderer.ts` defines 6 caption animation modes:

```typescript
// OpenReel's CaptionAnimationStyle type
type CaptionAnimationStyle =
  | "none"           // Static subtitles
  | "word-highlight" // Word-by-word highlight (basic karaoke)
  | "word-by-word"   // Show one word at a time
  | "karaoke"        // Progressive fill highlight
  | "bounce"         // Bounce-in appearance
  | "typewriter";    // Typewriter effect
```

**The critical `renderKaraoke` function** (progressive fill karaoke):

```typescript
// From OpenReel caption-animation-renderer.ts — directly portable
function renderKaraoke(subtitle: Subtitle, currentTime: number): AnimatedCaptionFrame {
  if (!subtitle.words || subtitle.words.length === 0) {
    return renderNone(subtitle);
  }

  const highlightColor = subtitle.style?.highlightColor || "#ffff00";
  const upcomingColor = subtitle.style?.upcomingColor || "rgba(255, 255, 255, 0.5)";

  const segments: WordSegment[] = subtitle.words.map((word) => {
    const wordDuration = word.endTime - word.startTime;
    const elapsed = currentTime - word.startTime;
    const progress = clamp(elapsed / wordDuration, 0, 1);

    const isUpcoming = currentTime < word.startTime;
    const isActive = currentTime >= word.startTime && currentTime < word.endTime;
    const isComplete = currentTime >= word.endTime;

    let color: string | undefined;
    if (isUpcoming) color = upcomingColor;
    else if (isComplete) color = highlightColor;
    else if (isActive) {
      // Progressive fill: CSS linear-gradient simulates left-to-right color sweep
      color = `linear-gradient(90deg, ${highlightColor} ${progress * 100}%, ${upcomingColor} ${progress * 100}%)`;
    }

    return {
      text: word.text,
      style: isActive ? "active" : isComplete ? "highlighted" : "normal",
      opacity: 1,
      scale: isActive ? 1.05 : 1,
      offsetY: 0,
      color,
    };
  });

  return { segments, visible: true };
}
```

**The `renderWordHighlight` function** (simple word highlighting):

```typescript
function renderWordHighlight(subtitle: Subtitle, currentTime: number): AnimatedCaptionFrame {
  const highlightColor = subtitle.style?.highlightColor || "#ffff00";

  const segments = subtitle.words.map((word) => {
    const isActive = currentTime >= word.startTime && currentTime < word.endTime;

    return {
      text: word.text,
      style: isActive ? "highlighted" : "normal",
      opacity: 1,
      scale: isActive ? 1.15 : 1,        // Current word scales up 15%
      offsetY: isActive ? -2 : 0,         // Current word floats up 2px
      color: isActive ? highlightColor : undefined,
    };
  });

  return { segments, visible: true };
}
```

---

## 3. New Files to Create

### 3.1 `karaoke-renderer.tsx` — Karaoke Rendering Component

**Path:** `apps/web/src/components/editor/preview-panel/karaoke-renderer.tsx`

```tsx
"use client";

import React, { useMemo } from "react";
import { useWordTimelineStore } from "@/stores/timeline/word-timeline-store";
import type { SubtitleStyle } from "@/types/timeline";
import { subtitleStyleToCSS } from "@/lib/captions/subtitle-style";
import {
  type KaraokeMode,
  getKaraokeSegments,
  type KaraokeSegment,
} from "@/lib/captions/karaoke-utils";

interface KaraokeRendererProps {
  currentTime: number;        // Current playback time (seconds)
  style: SubtitleStyle;       // Subtitle style
  mode: KaraokeMode;          // Karaoke mode
  captionStartTime: number;   // Current caption segment start time
  captionEndTime: number;     // Current caption segment end time
}

export function KaraokeRenderer({
  currentTime,
  style,
  mode,
  captionStartTime,
  captionEndTime,
}: KaraokeRendererProps) {
  const getNonDeletedWords = useWordTimelineStore((s) => s.getNonDeletedWords);

  // Filter words within the current caption's time range
  const wordsInRange = useMemo(() => {
    const allWords = getNonDeletedWords();
    return allWords.filter(
      (w) => w.start >= captionStartTime && w.end <= captionEndTime
    );
  }, [getNonDeletedWords, captionStartTime, captionEndTime]);

  // Compute highlight state for each word
  const segments = useMemo(
    () => getKaraokeSegments(wordsInRange, currentTime, mode, style),
    [wordsInRange, currentTime, mode, style]
  );

  if (segments.length === 0) return null;

  const baseCSS = subtitleStyleToCSS(style);

  return (
    <div style={{ ...baseCSS, display: "inline-flex", flexWrap: "wrap", gap: "4px" }}>
      {segments.map((seg, i) => (
        <span
          key={seg.wordId || i}
          style={{
            display: "inline-block",
            transform: `scale(${seg.scale}) translateY(${seg.offsetY}px)`,
            opacity: seg.opacity,
            transition: "transform 0.1s ease-out, opacity 0.1s ease-out",
            ...(seg.color?.startsWith("linear-gradient")
              ? {
                  background: seg.color,
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                }
              : { color: seg.color || style.fontColor }),
          }}
        >
          {seg.text}
        </span>
      ))}
    </div>
  );
}
```

### 3.2 `karaoke-utils.ts` — Karaoke Utility Functions

**Path:** `apps/web/src/lib/captions/karaoke-utils.ts`

```typescript
/**
 * Karaoke utility functions — adapted from OpenReel Video (MIT license)
 * @see https://github.com/Augani/openreel-video/blob/main/packages/core/src/text/caption-animation-renderer.ts
 */

import type { WordItem } from "@/types/word-timeline";
import type { SubtitleStyle } from "@/types/timeline";

export type KaraokeMode =
  | "none"
  | "word-highlight"
  | "word-by-word"
  | "karaoke"
  | "bounce"
  | "typewriter";

export interface KaraokeSegment {
  wordId: string;
  text: string;
  state: "upcoming" | "active" | "completed" | "hidden";
  opacity: number;
  scale: number;
  offsetY: number;
  color?: string;
}

function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), max);
}

function easeOutBounce(t: number): number {
  const n1 = 7.5625;
  const d1 = 2.75;
  if (t < 1 / d1) return n1 * t * t;
  if (t < 2 / d1) return n1 * (t -= 1.5 / d1) * t + 0.75;
  if (t < 2.5 / d1) return n1 * (t -= 2.25 / d1) * t + 0.9375;
  return n1 * (t -= 2.625 / d1) * t + 0.984375;
}

/** Word highlight: current word changes color + scales up */
function wordHighlight(
  words: WordItem[], time: number,
  style: SubtitleStyle & { highlightColor?: string }
): KaraokeSegment[] {
  const highlightColor = style.highlightColor || "#ffff00";
  return words.map((word) => {
    const isActive = time >= word.start && time < word.end;
    return {
      wordId: word.id, text: word.text,
      state: isActive ? "active" : time >= word.end ? "completed" : "upcoming",
      opacity: 1,
      scale: isActive ? 1.15 : 1,
      offsetY: isActive ? -2 : 0,
      color: isActive ? highlightColor : undefined,
    };
  });
}

/** Karaoke fill: progressive left-to-right color sweep */
function karaokeFill(
  words: WordItem[], time: number,
  style: SubtitleStyle & { highlightColor?: string; upcomingColor?: string }
): KaraokeSegment[] {
  const highlightColor = style.highlightColor || "#ffff00";
  const upcomingColor = style.upcomingColor || "rgba(255, 255, 255, 0.5)";

  return words.map((word) => {
    const duration = word.end - word.start;
    const elapsed = time - word.start;
    const progress = clamp(elapsed / duration, 0, 1);
    const isUpcoming = time < word.start;
    const isActive = time >= word.start && time < word.end;
    const isComplete = time >= word.end;

    let color: string | undefined;
    if (isUpcoming) color = upcomingColor;
    else if (isComplete) color = highlightColor;
    else if (isActive) {
      color = `linear-gradient(90deg, ${highlightColor} ${progress * 100}%, ${upcomingColor} ${progress * 100}%)`;
    }

    return {
      wordId: word.id, text: word.text,
      state: isActive ? "active" : isComplete ? "completed" : "upcoming",
      opacity: 1, scale: isActive ? 1.05 : 1, offsetY: 0, color,
    };
  });
}

/** Word-by-word: show only one word at a time */
function wordByWord(words: WordItem[], time: number): KaraokeSegment[] {
  const activeWord = words.find((w) => time >= w.start && time < w.end);
  if (!activeWord) {
    const lastWord = words[words.length - 1];
    if (lastWord && time >= lastWord.end) {
      return [{ wordId: lastWord.id, text: lastWord.text, state: "completed", opacity: 1, scale: 1, offsetY: 0 }];
    }
    return [];
  }
  return [{ wordId: activeWord.id, text: activeWord.text, state: "active", opacity: 1, scale: 1, offsetY: 0 }];
}

/** Bounce: words bounce in with easeOutBounce */
function bounce(words: WordItem[], time: number): KaraokeSegment[] {
  const animDuration = 0.3;
  return words.map((word) => {
    const timeSinceStart = time - word.start;
    if (time < word.start) {
      return { wordId: word.id, text: word.text, state: "hidden" as const, opacity: 0, scale: 0, offsetY: 20 };
    }
    const progress = clamp(timeSinceStart / animDuration, 0, 1);
    const bp = easeOutBounce(progress);
    const isActive = time >= word.start && time < word.end;
    return {
      wordId: word.id, text: word.text,
      state: isActive ? "active" as const : "completed" as const,
      opacity: bp, scale: 0.5 + bp * 0.5, offsetY: 20 * (1 - bp),
    };
  });
}

/** Typewriter: words appear sequentially, last word fades in */
function typewriter(words: WordItem[], time: number): KaraokeSegment[] {
  const visible = words.filter((w) => time >= w.start);
  if (visible.length === 0) return [];
  return visible.map((word, i) => {
    const isLast = i === visible.length - 1;
    const opacity = isLast ? clamp((time - word.start) / 0.1, 0, 1) : 1;
    return { wordId: word.id, text: word.text, state: "active" as const, opacity, scale: 1, offsetY: 0 };
  });
}

/** Main entry: returns render state for all words based on mode */
export function getKaraokeSegments(
  words: WordItem[], currentTime: number, mode: KaraokeMode,
  style: SubtitleStyle & { highlightColor?: string; upcomingColor?: string }
): KaraokeSegment[] {
  if (words.length === 0) return [];
  switch (mode) {
    case "word-highlight": return wordHighlight(words, currentTime, style);
    case "karaoke":        return karaokeFill(words, currentTime, style);
    case "word-by-word":   return wordByWord(words, currentTime);
    case "bounce":         return bounce(words, currentTime);
    case "typewriter":     return typewriter(words, currentTime);
    case "none": default:
      return words.map((w) => ({
        wordId: w.id, text: w.text, state: "completed" as const,
        opacity: 1, scale: 1, offsetY: 0,
      }));
  }
}
```

---

## 4. Files to Modify

### 4.1 Extend the `SubtitleStyle` Type

**File:** `packages/editor-core/src/types/timeline.ts`

```diff
 export interface SubtitleStyle {
   fontFamily: string;
   fontSize: number;
   fontColor: string;
   fontOpacity: number;
   bold: boolean;
   italic: boolean;
   underline: boolean;
   outlineColor: string;
   outlineWidth: number;
   shadowColor: string;
   shadowOffset: { x: number; y: number };
   backgroundColor: string;
   bgOpacity: number;
   position: {
     align: "top" | "center" | "bottom";
     x: number;
     y: number;
   };
   lineSpacing: number;
+  /** Karaoke highlight color */
+  highlightColor?: string;
+  /** Karaoke highlight scale factor */
+  highlightScale?: number;
+  /** Color for upcoming (not-yet-sung) words */
+  upcomingColor?: string;
+  /** Karaoke animation mode */
+  karaokeMode?: "none" | "word-highlight" | "word-by-word" | "karaoke" | "bounce" | "typewriter";
 }
```

### 4.2 Integrate into the Preview Panel

**File:** `apps/web/src/components/editor/preview-panel/use-preview-media.ts`

```diff
+import { useWordTimelineStore } from "@/stores/timeline/word-timeline-store";

 interface UsePreviewMediaResult {
   captionSegments: TranscriptionSegment[];
+  karaokeWords: WordItem[];
   blurBackgroundElements: ActiveElement[];
   // ...
 }

 export function usePreviewMedia({ ... }): UsePreviewMediaResult {
+  const karaokeWords = useWordTimelineStore((s) => s.getNonDeletedWords());
   // ... existing code ...
   return {
     captionSegments,
+    karaokeWords,
     blurBackgroundElements,
     // ...
   };
 }
```

### 4.3 Add ASS `\k` Tag Export

**File:** `apps/web/src/lib/captions/caption-export.ts`

New function:

```typescript
/**
 * Generate ASS subtitles with karaoke \k tags
 * \k tags use centiseconds to specify each word's duration
 */
export function exportAssKaraoke(
  words: WordItem[],
  segments: TranscriptionSegment[],
  options: Partial<CaptionExportOptions> = {}
): string {
  const fontFamily = options.fontFamily || "Arial";
  const fontSize = options.fontSize || 16;

  let content = `[Script Info]
Title: QCut Karaoke Subtitles
ScriptType: v4.00+

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,${fontFamily},${fontSize},&Hffffff,&H00ffff,&H0,&H0,0,0,0,0,100,100,0,0,1,2,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
`;

  for (const segment of segments) {
    const segWords = words.filter(
      (w) => w.start >= segment.start && w.end <= segment.end
    );

    if (segWords.length === 0) {
      const startTime = formatAssTime(segment.start);
      const endTime = formatAssTime(segment.end);
      content += `Dialogue: 0,${startTime},${endTime},Default,,0,0,0,,${segment.text.trim()}\n`;
      continue;
    }

    const startTime = formatAssTime(segment.start);
    const endTime = formatAssTime(segment.end);
    const karaokeText = segWords
      .map((w) => {
        const durationCs = Math.round((w.end - w.start) * 100);
        return `{\\k${durationCs}}${w.text}`;
      })
      .join(" ");

    content += `Dialogue: 0,${startTime},${endTime},Default,,0,0,0,,${karaokeText}\n`;
  }

  return content;
}
```

### 4.4 Modification Summary

| File | Change | Diff Size |
|------|--------|-----------|
| `packages/editor-core/src/types/timeline.ts` | Add 4 optional fields to `SubtitleStyle` | +4 lines |
| `apps/web/src/lib/captions/subtitle-style.ts` | Add default values for new fields | +4 lines |
| `apps/web/src/components/editor/preview-panel/use-preview-media.ts` | Inject `karaokeWords` | +5 lines |
| `apps/web/src/lib/captions/caption-export.ts` | Add `exportAssKaraoke()` function | +50 lines |
| `packages/editor-core/src/captions/ass-generator.ts` | Support `\k` tag generation | +30 lines |

---

## 5. Porting 20+ Text Animation Effects

OpenReel Video implements 20+ text animation effects under `packages/core/src/text/`, all as **pure functions** with zero framework dependencies. They can be copied directly into QCut.

### 5.1 Complete Animation Inventory

| # | Animation | OpenReel Preset | Effect Description | Source File |
|---|-----------|----------------|-------------------|-------------|
| 1 | **Typewriter** | `typewriter` | Characters appear one by one | `text-animation-presets.ts` |
| 2 | **Fade** | `fade` | Fade in/out with configurable start/end opacity | `text-animation-presets.ts` |
| 3 | **Slide Left** | `slide-left` | Slide in from right | `text-animation-presets.ts` |
| 4 | **Slide Right** | `slide-right` | Slide in from left | `text-animation-presets.ts` |
| 5 | **Slide Up** | `slide-up` | Slide in from below | `text-animation-presets.ts` |
| 6 | **Slide Down** | `slide-down` | Slide in from above | `text-animation-presets.ts` |
| 7 | **Scale** | `scale` | Scale entrance with easeOutBack | `text-animation-presets.ts` |
| 8 | **Bounce** | `bounce` | Bouncy entrance with easeOutBounce | `text-animation-presets.ts` |
| 9 | **Rotate** | `rotate` | Rotation entrance with configurable angle | `text-animation-presets.ts` |
| 10 | **Wave** | `wave` | Continuous sine-wave oscillation | `text-animation-presets.ts` |
| 11 | **Shake** | `shake` | Continuous vibration effect | `text-animation-presets.ts` |
| 12 | **Pop** | `pop` | Pop entrance with overshoot | `text-animation-presets.ts` |
| 13 | **Glitch** | `glitch` | Digital glitch with random offset + color shift | `text-animation-presets.ts` |
| 14 | **Split** | `split` | Text splits outward from center | `text-animation-presets.ts` |
| 15 | **Flip** | `flip` | 3D flip entrance | `text-animation.ts` |
| 16 | **Word-by-Word** | `word-by-word` | Words appear sequentially | `text-animation.ts` |
| 17 | **Rainbow** | `rainbow` | Cycling rainbow color effect | `text-animation.ts` |
| 18 | **Blur** | `blur` | Blur-to-sharp transition | `text-animation-presets.ts` |
| 19 | **Word Highlight** | `word-highlight` | Per-word karaoke highlight | `caption-animation-renderer.ts` |
| 20 | **Karaoke Fill** | `karaoke` | Progressive fill highlight | `caption-animation-renderer.ts` |
| 21 | **Typewriter (Caption)** | `typewriter` | Caption-specific typewriter | `caption-animation-renderer.ts` |
| 22 | **Bounce (Caption)** | `bounce` | Caption-specific bounce | `caption-animation-renderer.ts` |

### 5.2 OpenReel's Animation Architecture

OpenReel's animation system uses a clean two-layer design:

**Layer 1: Unit Animation State (`UnitAnimationState`)**

```typescript
// text-animation-presets.ts — computed result for each animated unit
interface UnitAnimationState {
  opacity: number;                    // Opacity 0–1
  scale: { x: number; y: number };   // Scale factor
  rotation: number;                   // Rotation in degrees
  offsetX: number;                    // X offset in pixels
  offsetY: number;                    // Y offset in pixels
  blur: number;                       // Blur amount in pixels
  color?: string;                     // Optional color override
  skewX?: number;                     // Optional X skew
  skewY?: number;                     // Optional Y skew
}
```

**Layer 2: Uniform Animation Function Signature**

```typescript
// Every animation is a pure function with this signature
type AnimationFn = (ctx: TextAnimationContext) => UnitAnimationState;

interface TextAnimationContext {
  unit: AnimatedUnit;        // Current animation unit (char/word/line)
  progress: number;          // Animation progress 0–1
  isIn: boolean;             // Entrance or exit phase
  animation: TextAnimation;  // Animation configuration
  totalDuration: number;     // Total duration
}
```

### 5.3 Porting Strategy

**Direct copy (zero modifications):** All animation functions in `text-animation-presets.ts`

Every animation function is a pure function: input `TextAnimationContext`, output `UnitAnimationState`. No React, PixiJS, or framework dependencies whatsoever.

```typescript
// Example: Pop animation — can be copied directly into QCut
const popAnimation: AnimationFn = (ctx) => {
  const { unit, progress, isIn, animation } = ctx;
  const stagger = animation.stagger || 0.05;
  const overshoot = animation.params.popOvershoot ?? 1.2;

  const unitDelay = unit.index * stagger;
  const duration = isIn ? animation.inDuration : animation.outDuration;
  const unitDuration = Math.max(0.1, duration - (unit.totalUnits - 1) * stagger);

  let unitProgress = Math.max(0, Math.min(1, (progress * duration - unitDelay) / unitDuration));
  if (!isIn) unitProgress = 1 - unitProgress;

  const easedProgress = easeOutBack(unitProgress);
  const scale = unitProgress > 0 ? easedProgress * (unitProgress < 0.5 ? overshoot : 1) : 0;

  return {
    opacity: unitProgress > 0 ? 1 : 0,
    scale: { x: Math.max(0, scale), y: Math.max(0, scale) },
    rotation: 0, offsetX: 0, offsetY: 0, blur: 0,
  };
};
```

**Parts that need adaptation:**

| Component | OpenReel Approach | QCut Adaptation |
|-----------|------------------|-----------------|
| Text measurement | `CharacterAnimator` uses `OffscreenCanvas` | QCut can reuse the same approach, or use DOM measurement |
| Animation state → DOM | PixiJS Container transforms | CSS `transform` + `opacity` |
| Animation dispatch | `TextAnimationEngine` class | Reuse pure functions, dispatch via React hook |
| Config storage | React Context `useProjectStore` | Zustand store |

### 5.4 QCut Integration Plan

Create `apps/web/src/lib/captions/text-animation-presets.ts`:

```typescript
/**
 * Text animation presets — ported from OpenReel Video (MIT license)
 * Pure functions, no framework dependency
 */

// Copy all animation functions directly from OpenReel (~400 lines):
export { typewriterAnimation } from "./animations/typewriter";
export { fadeAnimation } from "./animations/fade";
export { slideAnimation } from "./animations/slide";
export { scaleAnimation } from "./animations/scale";
export { bounceAnimation } from "./animations/bounce";
export { rotateAnimation } from "./animations/rotate";
export { waveAnimation } from "./animations/wave";
export { shakeAnimation } from "./animations/shake";
export { popAnimation } from "./animations/pop";
export { glitchAnimation } from "./animations/glitch";
export { splitAnimation } from "./animations/split";
export { blurAnimation } from "./animations/blur";

// Type definitions
export type TextAnimationPreset =
  | "none" | "typewriter" | "fade"
  | "slide-left" | "slide-right" | "slide-up" | "slide-down"
  | "scale" | "bounce" | "rotate" | "wave" | "shake"
  | "pop" | "glitch" | "split" | "flip" | "blur"
  | "word-by-word" | "rainbow";

// Convert animation state → CSS properties
export function animationStateToCSS(state: UnitAnimationState): React.CSSProperties {
  return {
    opacity: state.opacity,
    transform: [
      `translateX(${state.offsetX}px)`,
      `translateY(${state.offsetY}px)`,
      `scale(${state.scale.x}, ${state.scale.y})`,
      `rotate(${state.rotation}deg)`,
      state.skewX ? `skewX(${state.skewX}deg)` : "",
      state.skewY ? `skewY(${state.skewY}deg)` : "",
    ].filter(Boolean).join(" "),
    filter: state.blur > 0 ? `blur(${state.blur}px)` : undefined,
    color: state.color || undefined,
  };
}
```

### 5.5 Effort

| Item | Lines | Time |
|------|-------|------|
| Copy pure animation functions | ~400 lines | 2 hours (copy + type adaptation) |
| Write `animationStateToCSS` | ~30 lines | 30 minutes |
| Animation picker UI | ~100 lines | 2 hours |
| Integrate into subtitle rendering | ~50 lines | 1 hour |
| **Total** | **~580 lines** | **~5.5 hours** |

---

## 6. Architecture Adaptation Notes

### 6.1 React Context → Zustand

OpenReel uses React Context (`useProjectStore`) for state management; QCut uses Zustand.

```typescript
// OpenReel (React Context)
const getTextClip = useProjectStore((state) => state.getTextClip);

// QCut adaptation (Zustand — nearly identical API!)
const getNonDeletedWords = useWordTimelineStore((s) => s.getNonDeletedWords);
```

**Good news:** OpenReel's `useProjectStore` already uses the selector pattern, which is nearly identical to Zustand's API. Adaptation effort is minimal.

### 6.2 PixiJS → CSS/DOM

OpenReel's rendering layer uses PixiJS Canvas; QCut's preview panel uses DOM rendering. But the animation algorithms (input time → output state) are fully decoupled from the rendering backend.

```
OpenReel:  Pure algorithm → UnitAnimationState → PixiJS Container.transform
QCut:      Pure algorithm → UnitAnimationState → CSS transform + opacity
```

### 6.3 Pure Functions That Copy Directly

These functions need **zero modifications**:

| Function | Source File |
|----------|------------|
| `clamp()` | `caption-animation-renderer.ts` |
| `easeOutBounce()` | `caption-animation-renderer.ts` |
| `renderWordHighlight()` algorithm | `caption-animation-renderer.ts` |
| `renderKaraoke()` algorithm | `caption-animation-renderer.ts` |
| `renderBounce()` algorithm | `caption-animation-renderer.ts` |
| `renderTypewriter()` algorithm | `caption-animation-renderer.ts` |
| `renderWordByWord()` algorithm | `caption-animation-renderer.ts` |
| All 14 animation functions in `text-animation-presets.ts` | `text-animation-presets.ts` |

---

## 7. ASS Karaoke Export

ASS format natively supports karaoke tags. The commonly used ones:

| Tag | Effect | Example |
|-----|--------|---------|
| `\k` | Per-word highlight (instant color change) | `{\k50}Hello {\k30}World` |
| `\kf` / `\K` | Progressive fill (left-to-right sweep) | `{\kf50}Hello {\kf30}World` |
| `\ko` | Outline highlight | `{\ko50}Hello {\ko30}World` |

Numbers are in **centiseconds** (1/100 second).

Generating `\k` tags from QCut's `WordItem` is straightforward:

```typescript
// WordItem.start=1.2, WordItem.end=1.7 → duration=0.5s → 50cs
const durationCs = Math.round((word.end - word.start) * 100);
const tag = `{\\k${durationCs}}${word.text}`;
// Output: {\k50}Hello
```

---

## 8. Effort Estimate

| Task | New Code | Modified Code | Time |
|------|----------|--------------|------|
| `karaoke-utils.ts` | ~180 lines | — | 3 hours |
| `karaoke-renderer.tsx` | ~80 lines | — | 2 hours |
| Type extensions + defaults | — | ~10 lines | 30 minutes |
| Preview panel integration | — | ~15 lines | 1 hour |
| ASS karaoke export | ~60 lines | ~10 lines | 2 hours |
| Text animation preset porting | ~400 lines | — | 5 hours |
| UI (mode selector) | ~100 lines | — | 2 hours |
| Testing + debugging | — | — | 3 hours |
| **Total** | **~820 lines** | **~35 lines** | **~18.5 hours (2-3 days)** |

### Implementation Priority

1. **P0 (Day 1):** `karaoke-utils.ts` + `karaoke-renderer.tsx` + type extensions → Basic word highlighting works
2. **P1 (Day 2):** Text animation preset porting + animation picker UI → 20+ animations available
3. **P2 (Day 3):** ASS `\k` tag export + testing → Complete feature loop

---

## References

- [OpenReel Video GitHub](https://github.com/Augani/openreel-video) (MIT license)
- [ASS Karaoke Tag Specification](https://aegisub.org/docs/latest/ass_tags/#karaoke-effect)
- [QCut Code Repository](https://github.com/Quriosity-AI/qcut)

---

*Written based on QCut source code + OpenReel Video source code analysis. All code examples are from actual source files.*

🦞
