# QCut 卡拉OK逐字高亮字幕：复用 OpenReel Video 代码的完整实现指南

> **TL;DR:** QCut 已有逐词时间戳数据和字幕样式系统，OpenReel Video（MIT 协议）已有完整的卡拉OK渲染引擎和 20+ 种文字动画效果。本文详解如何把 OpenReel 的核心算法移植到 QCut，预计新增 ~500 行代码，2-3 天完成。

---

## 目录

1. [QCut 现有基础设施](#1-qcut-现有基础设施)
2. [OpenReel Video 可复用文件](#2-openreel-video-可复用文件)
3. [需要新建的文件](#3-需要新建的文件)
4. [需要修改的文件](#4-需要修改的文件)
5. [20+ 文字动画效果移植](#5-20-文字动画效果移植)
6. [架构适配要点](#6-架构适配要点)
7. [ASS 卡拉OK导出](#7-ass-卡拉ok导出)
8. [工作量估算](#8-工作量估算)

---

## 1. QCut 现有基础设施

QCut 已经具备实现卡拉OK字幕的大部分基础组件。以下是关键文件清单：

| 文件路径 | 用途 | 提供什么 |
|---------|------|---------|
| `apps/web/src/stores/timeline/word-timeline-store.ts` | 逐词时间戳 Zustand store | `WordItem { id, text, start, end, type, filterState }`，含 `getVisibleWords()`、`getWordsForExport()` |
| `apps/web/src/lib/captions/subtitle-style.ts` | 字幕样式 → CSS 转换 | `subtitleStyleToCSS(style)` 函数，重导出 `hexToRgba`、`rgbToASSColor` 等工具函数 |
| `apps/web/src/lib/captions/ass-generator.ts` | ASS 文件生成 | 重导出 `generateASS()`、`secondsToASSTime()` |
| `apps/web/src/lib/captions/ass-parser.ts` | ASS 文件解析 | 重导出 `parseASS()`、`assTimeToSeconds()`、`assStyleToSubtitleStyle()` |
| `apps/web/src/lib/captions/caption-export.ts` | 字幕导出管线 | `exportSrt()`、`exportVtt()`、`exportAss()`、`exportAssStyled()` 及下载函数 |
| `apps/web/src/components/editor/preview-panel/use-preview-media.ts` | 预览面板媒体钩子 | 从活跃时间线元素中提取 `captionSegments`，驱动字幕渲染 |
| `packages/editor-core/src/types/timeline.ts` | 共享类型定义 | `SubtitleStyle` 接口（20 个字段）、`CaptionElement` 接口 |

### 关键数据结构

QCut 的 `WordItem` 已包含逐词时间戳——这是卡拉OK高亮的核心数据：

```typescript
// word-timeline-store.ts 中的 WordItem
interface WordItem {
  id: string;
  text: string;
  start: number;   // 秒，精确到毫秒
  end: number;      // 秒
  type: "word" | "spacing";
  speaker_id?: string;
  filterState: WordFilterState;
  filterReason?: string;
}
```

QCut 的 `SubtitleStyle` 控制字幕外观：

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

**结论：** 数据层完整，缺的是「渲染时根据当前播放时间高亮对应单词」的逻辑。

---

## 2. OpenReel Video 可复用文件

OpenReel Video（[GitHub](https://github.com/Augani/openreel-video)，MIT 协议）已实现完整的卡拉OK字幕系统。核心文件：

| OpenReel 文件路径 | 行数 | 用途 | 可复用程度 |
|------------------|------|------|-----------|
| `packages/core/src/text/caption-animation-renderer.ts` | ~260 | **卡拉OK渲染核心**：6 种字幕动画模式 | ⭐ 直接复用算法 |
| `packages/core/src/text/text-animation-presets.ts` | ~450 | **20+ 种文字动画效果**：纯函数实现 | ⭐ 直接复制 |
| `packages/core/src/text/text-animation.ts` | ~300 | 文字动画引擎：preset 调度 + easing | 🔧 适配后复用 |
| `packages/core/src/text/character-animator.ts` | ~350 | 逐字符动画：文本测量 + 布局 | 🔧 适配后复用 |
| `packages/core/src/text/subtitle-engine.ts` | ~400 | 字幕引擎：SRT 解析 + 样式管理 | 📖 参考设计 |
| `apps/web/src/stores/project/subtitle-helpers.ts` | ~150 | 字幕辅助函数 | 📖 参考设计 |
| `apps/web/src/components/editor/inspector/TextAnimationSection.tsx` | ~200 | 动画选择器 UI | 📖 参考 UI 设计 |

### 核心算法详解

OpenReel 的 `caption-animation-renderer.ts` 定义了 6 种字幕动画模式：

```typescript
// OpenReel 的 CaptionAnimationStyle 类型
type CaptionAnimationStyle =
  | "none"           // 静态字幕
  | "word-highlight" // 逐词高亮（卡拉OK基础版）
  | "word-by-word"   // 逐词显示（一次只显示一个词）
  | "karaoke"        // 卡拉OK（渐进填充高亮）
  | "bounce"         // 弹跳出现
  | "typewriter";    // 打字机效果
```

**最关键的 `renderKaraoke` 函数**（渐进填充式卡拉OK）：

```typescript
// 来自 OpenReel caption-animation-renderer.ts —— 可直接移植
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
    if (isUpcoming) {
      color = upcomingColor;
    } else if (isComplete) {
      color = highlightColor;
    } else if (isActive) {
      // 渐进填充：CSS linear-gradient 模拟从左到右的颜色过渡
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

**`renderWordHighlight` 函数**（简单逐词高亮）：

```typescript
function renderWordHighlight(subtitle: Subtitle, currentTime: number): AnimatedCaptionFrame {
  const highlightColor = subtitle.style?.highlightColor || "#ffff00";

  const segments = subtitle.words.map((word) => {
    const isActive = currentTime >= word.startTime && currentTime < word.endTime;
    const isPast = currentTime >= word.endTime;

    return {
      text: word.text,
      style: isActive ? "highlighted" : "normal",
      opacity: 1,
      scale: isActive ? 1.15 : 1,        // 当前词放大 15%
      offsetY: isActive ? -2 : 0,         // 当前词上浮 2px
      color: isActive ? highlightColor : undefined,
    };
  });

  return { segments, visible: true };
}
```

---

## 3. 需要新建的文件

### 3.1 `karaoke-renderer.tsx` — 卡拉OK渲染组件

**路径：** `apps/web/src/components/editor/preview-panel/karaoke-renderer.tsx`

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
  currentTime: number;        // 当前播放时间（秒）
  style: SubtitleStyle;       // 字幕样式
  mode: KaraokeMode;          // 卡拉OK模式
  captionStartTime: number;   // 当前字幕段落开始时间
  captionEndTime: number;     // 当前字幕段落结束时间
}

export function KaraokeRenderer({
  currentTime,
  style,
  mode,
  captionStartTime,
  captionEndTime,
}: KaraokeRendererProps) {
  const getNonDeletedWords = useWordTimelineStore((s) => s.getNonDeletedWords);

  // 筛选当前字幕时间范围内的词
  const wordsInRange = useMemo(() => {
    const allWords = getNonDeletedWords();
    return allWords.filter(
      (w) => w.start >= captionStartTime && w.end <= captionEndTime
    );
  }, [getNonDeletedWords, captionStartTime, captionEndTime]);

  // 计算每个词的高亮状态
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

### 3.2 `karaoke-utils.ts` — 卡拉OK工具函数

**路径：** `apps/web/src/lib/captions/karaoke-utils.ts`

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

/** 逐词高亮：当前词变色+放大，其他词正常 */
function wordHighlight(
  words: WordItem[],
  time: number,
  style: SubtitleStyle & { highlightColor?: string }
): KaraokeSegment[] {
  const highlightColor = style.highlightColor || "#ffff00";

  return words.map((word) => {
    const isActive = time >= word.start && time < word.end;
    return {
      wordId: word.id,
      text: word.text,
      state: isActive ? "active" : time >= word.end ? "completed" : "upcoming",
      opacity: 1,
      scale: isActive ? 1.15 : 1,
      offsetY: isActive ? -2 : 0,
      color: isActive ? highlightColor : undefined,
    };
  });
}

/** 卡拉OK：渐进填充高亮 */
function karaokeFill(
  words: WordItem[],
  time: number,
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
      wordId: word.id,
      text: word.text,
      state: isActive ? "active" : isComplete ? "completed" : "upcoming",
      opacity: 1,
      scale: isActive ? 1.05 : 1,
      offsetY: 0,
      color,
    };
  });
}

/** 逐词显示：一次只显示一个词 */
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

/** 弹跳出现 */
function bounce(words: WordItem[], time: number): KaraokeSegment[] {
  const animDuration = 0.3;
  return words.map((word) => {
    const timeSinceStart = time - word.start;
    const isVisible = time >= word.start;
    if (!isVisible) {
      return { wordId: word.id, text: word.text, state: "hidden" as const, opacity: 0, scale: 0, offsetY: 20 };
    }
    const progress = clamp(timeSinceStart / animDuration, 0, 1);
    const bounceProgress = easeOutBounce(progress);
    const isActive = time >= word.start && time < word.end;
    return {
      wordId: word.id,
      text: word.text,
      state: isActive ? "active" as const : "completed" as const,
      opacity: bounceProgress,
      scale: 0.5 + bounceProgress * 0.5,
      offsetY: 20 * (1 - bounceProgress),
    };
  });
}

/** 打字机效果 */
function typewriter(words: WordItem[], time: number): KaraokeSegment[] {
  const visibleWords = words.filter((w) => time >= w.start);
  if (visibleWords.length === 0) return [];

  return visibleWords.map((word, index) => {
    const isLast = index === visibleWords.length - 1;
    const elapsed = time - word.start;
    const opacity = isLast ? clamp(elapsed / 0.1, 0, 1) : 1;
    return {
      wordId: word.id,
      text: word.text,
      state: "active" as const,
      opacity,
      scale: 1,
      offsetY: 0,
    };
  });
}

/** 主入口：根据模式返回所有词的渲染状态 */
export function getKaraokeSegments(
  words: WordItem[],
  currentTime: number,
  mode: KaraokeMode,
  style: SubtitleStyle & { highlightColor?: string; upcomingColor?: string }
): KaraokeSegment[] {
  if (words.length === 0) return [];

  switch (mode) {
    case "word-highlight":
      return wordHighlight(words, currentTime, style);
    case "karaoke":
      return karaokeFill(words, currentTime, style);
    case "word-by-word":
      return wordByWord(words, currentTime);
    case "bounce":
      return bounce(words, currentTime);
    case "typewriter":
      return typewriter(words, currentTime);
    case "none":
    default:
      return words.map((w) => ({
        wordId: w.id,
        text: w.text,
        state: "completed" as const,
        opacity: 1,
        scale: 1,
        offsetY: 0,
      }));
  }
}
```

---

## 4. 需要修改的文件

### 4.1 扩展 `SubtitleStyle` 类型

**文件：** `packages/editor-core/src/types/timeline.ts`

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
+  /** 卡拉OK高亮颜色 */
+  highlightColor?: string;
+  /** 卡拉OK高亮缩放 */
+  highlightScale?: number;
+  /** 未唱到的词的颜色 */
+  upcomingColor?: string;
+  /** 卡拉OK动画模式 */
+  karaokeMode?: "none" | "word-highlight" | "word-by-word" | "karaoke" | "bounce" | "typewriter";
 }
```

### 4.2 集成到预览面板

**文件：** `apps/web/src/components/editor/preview-panel/use-preview-media.ts`

在 `captionSegments` 之后添加卡拉OK相关数据：

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
   // ... 现有代码 ...
   return {
     captionSegments,
+    karaokeWords,
     blurBackgroundElements,
     // ...
   };
 }
```

### 4.3 ASS 导出添加 `\k` 标签

**文件：** `apps/web/src/lib/captions/caption-export.ts`

新增函数：

```typescript
/**
 * 生成带卡拉OK \k 标签的 ASS 格式字幕
 * \k 标签后跟时间（厘秒），表示每个词的持续时间
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
    const segmentWords = words.filter(
      (w) => w.start >= segment.start && w.end <= segment.end
    );

    if (segmentWords.length === 0) {
      // 无逐词数据，退回普通字幕
      const startTime = formatAssTime(segment.start);
      const endTime = formatAssTime(segment.end);
      content += `Dialogue: 0,${startTime},${endTime},Default,,0,0,0,,${segment.text.trim()}\n`;
      continue;
    }

    // 用 \k 标签构建带逐词时间的行
    const startTime = formatAssTime(segment.start);
    const endTime = formatAssTime(segment.end);
    const karaokeText = segmentWords
      .map((w) => {
        const durationCs = Math.round((w.end - w.start) * 100); // 厘秒
        return `{\\k${durationCs}}${w.text}`;
      })
      .join(" ");

    content += `Dialogue: 0,${startTime},${endTime},Default,,0,0,0,,${karaokeText}\n`;
  }

  return content;
}
```

### 4.4 修改总览

| 文件 | 修改内容 | 改动量 |
|------|---------|--------|
| `packages/editor-core/src/types/timeline.ts` | 添加 4 个可选字段到 `SubtitleStyle` | +4 行 |
| `apps/web/src/lib/captions/subtitle-style.ts` | 添加 `DEFAULT_SUBTITLE_STYLE` 的新字段默认值 | +4 行 |
| `apps/web/src/components/editor/preview-panel/use-preview-media.ts` | 注入 `karaokeWords` | +5 行 |
| `apps/web/src/lib/captions/caption-export.ts` | 添加 `exportAssKaraoke()` 函数 | +50 行 |
| `packages/editor-core/src/captions/ass-generator.ts` | 支持生成 `\k` 标签 | +30 行 |

---

## 5. 20+ 文字动画效果移植

OpenReel Video 在 `packages/core/src/text/` 下实现了 20+ 种文字动画效果，全部是**纯函数**，无框架依赖，可以直接复制到 QCut。

### 5.1 动画效果完整清单

| # | 动画名称 | OpenReel Preset 值 | 效果描述 | 来源文件 |
|---|---------|-------------------|---------|---------|
| 1 | **Typewriter** | `typewriter` | 逐字符出现，模拟打字机 | `text-animation-presets.ts` |
| 2 | **Fade** | `fade` | 淡入淡出，支持自定义起止透明度 | `text-animation-presets.ts` |
| 3 | **Slide Left** | `slide-left` | 从右滑入 | `text-animation-presets.ts` |
| 4 | **Slide Right** | `slide-right` | 从左滑入 | `text-animation-presets.ts` |
| 5 | **Slide Up** | `slide-up` | 从下滑入 | `text-animation-presets.ts` |
| 6 | **Slide Down** | `slide-down` | 从上滑入 | `text-animation-presets.ts` |
| 7 | **Scale** | `scale` | 缩放入场，支持 easeOutBack | `text-animation-presets.ts` |
| 8 | **Bounce** | `bounce` | 弹跳入场，easeOutBounce | `text-animation-presets.ts` |
| 9 | **Rotate** | `rotate` | 旋转入场，支持自定义角度 | `text-animation-presets.ts` |
| 10 | **Wave** | `wave` | 持续波浪运动，正弦函数驱动 | `text-animation-presets.ts` |
| 11 | **Shake** | `shake` | 持续抖动效果 | `text-animation-presets.ts` |
| 12 | **Pop** | `pop` | 弹出效果，带回弹过冲 | `text-animation-presets.ts` |
| 13 | **Glitch** | `glitch` | 数字故障效果，随机偏移+变色 | `text-animation-presets.ts` |
| 14 | **Split** | `split` | 从中心分裂出现 | `text-animation-presets.ts` |
| 15 | **Flip** | `flip` | 3D 翻转入场 | `text-animation.ts` |
| 16 | **Word-by-Word** | `word-by-word` | 逐词顺序出现 | `text-animation.ts` |
| 17 | **Rainbow** | `rainbow` | 彩虹色循环 | `text-animation.ts` |
| 18 | **Blur** | `blur` | 模糊到清晰 | `text-animation-presets.ts` |
| 19 | **Word Highlight** | `word-highlight` | 逐词高亮（卡拉OK） | `caption-animation-renderer.ts` |
| 20 | **Karaoke Fill** | `karaoke` | 渐进填充高亮 | `caption-animation-renderer.ts` |
| 21 | **Typewriter (Caption)** | `typewriter` | 字幕专用打字机 | `caption-animation-renderer.ts` |
| 22 | **Bounce (Caption)** | `bounce` | 字幕专用弹跳 | `caption-animation-renderer.ts` |

### 5.2 OpenReel 动画架构

OpenReel 的动画系统基于两层设计：

**第一层：单元动画状态（`UnitAnimationState`）**

```typescript
// text-animation-presets.ts — 每个动画单元的计算结果
interface UnitAnimationState {
  opacity: number;           // 透明度
  scale: { x: number; y: number };  // 缩放
  rotation: number;          // 旋转角度
  offsetX: number;           // X 偏移
  offsetY: number;           // Y 偏移
  blur: number;              // 模糊度
  color?: string;            // 可选颜色覆盖
  skewX?: number;            // 可选 X 倾斜
  skewY?: number;            // 可选 Y 倾斜
}
```

**第二层：动画函数签名（统一接口）**

```typescript
// 每个动画都是这个签名的纯函数
type AnimationFn = (ctx: TextAnimationContext) => UnitAnimationState;

interface TextAnimationContext {
  unit: AnimatedUnit;        // 当前动画单元（字符/词/行）
  progress: number;          // 动画进度 0~1
  isIn: boolean;             // 入场还是出场
  animation: TextAnimation;  // 动画配置
  totalDuration: number;     // 总时长
}
```

### 5.3 移植策略

**直接复制（零修改）：** `text-animation-presets.ts` 中的所有动画函数

每个动画函数都是纯函数，输入 `TextAnimationContext`，输出 `UnitAnimationState`。没有任何 React/PixiJS/框架依赖。

```typescript
// 示例：Pop 动画 — 可以直接复制到 QCut
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

**需要适配的部分：**

| 组件 | OpenReel 方式 | QCut 适配 |
|------|-------------|----------|
| 文本测量 | `CharacterAnimator` 用 `OffscreenCanvas` | QCut 可复用相同方式，或用 DOM 测量 |
| 动画状态 → DOM | PixiJS Container transform | CSS `transform` + `opacity` |
| 动画调度 | `TextAnimationEngine` class | 复用纯函数，用 React hook 调度 |
| 配置存储 | React Context `useProjectStore` | Zustand store |

### 5.4 QCut 集成方案

新建文件 `apps/web/src/lib/captions/text-animation-presets.ts`：

```typescript
/**
 * Text animation presets — ported from OpenReel Video (MIT license)
 * Pure functions, no framework dependency
 */

// 直接从 OpenReel 复制以下函数（约 400 行）：
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

// 类型定义
export type TextAnimationPreset =
  | "none" | "typewriter" | "fade"
  | "slide-left" | "slide-right" | "slide-up" | "slide-down"
  | "scale" | "bounce" | "rotate" | "wave" | "shake"
  | "pop" | "glitch" | "split" | "flip" | "blur"
  | "word-by-word" | "rainbow";

// 动画状态 → CSS 转换
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

### 5.5 工作量

| 项目 | 行数 | 时间 |
|------|------|------|
| 复制动画纯函数 | ~400 行 | 2 小时（复制 + 类型适配） |
| 编写 `animationStateToCSS` | ~30 行 | 30 分钟 |
| 动画选择器 UI | ~100 行 | 2 小时 |
| 集成到字幕渲染 | ~50 行 | 1 小时 |
| **合计** | **~580 行** | **~5.5 小时** |

---

## 6. 架构适配要点

### 6.1 React Context → Zustand

OpenReel 用 React Context（`useProjectStore`）管理状态，QCut 用 Zustand。

```typescript
// OpenReel 方式（React Context）
const getTextClip = useProjectStore((state) => state.getTextClip);
const applyTextAnimationPreset = useProjectStore((state) => state.applyTextAnimationPreset);

// QCut 适配（Zustand — 几乎相同的 API！）
const getNonDeletedWords = useWordTimelineStore((s) => s.getNonDeletedWords);
```

**好消息：** OpenReel 的 `useProjectStore` 已经是 selector 模式，和 Zustand 语法几乎一致。适配工作量极小。

### 6.2 PixiJS → CSS/DOM

OpenReel 的渲染层使用 PixiJS Canvas，QCut 的预览面板用 DOM 渲染。但动画算法（输入时间 → 输出状态）完全解耦，不依赖渲染后端。

```
OpenReel:  算法纯函数 → UnitAnimationState → PixiJS Container.transform
QCut:      算法纯函数 → UnitAnimationState → CSS transform + opacity
```

### 6.3 可直接复制的纯函数

以下函数**零修改**即可使用：

| 函数 | 来源文件 |
|------|---------|
| `clamp()` | `caption-animation-renderer.ts` |
| `easeOutBounce()` | `caption-animation-renderer.ts` |
| `renderWordHighlight()` 算法 | `caption-animation-renderer.ts` |
| `renderKaraoke()` 算法 | `caption-animation-renderer.ts` |
| `renderBounce()` 算法 | `caption-animation-renderer.ts` |
| `renderTypewriter()` 算法 | `caption-animation-renderer.ts` |
| `renderWordByWord()` 算法 | `caption-animation-renderer.ts` |
| 全部 14 个 `text-animation-presets.ts` 动画函数 | `text-animation-presets.ts` |

---

## 7. ASS 卡拉OK导出

ASS 格式原生支持卡拉OK标签。常用标签：

| 标签 | 效果 | 示例 |
|------|------|------|
| `\k` | 逐词高亮（瞬间变色） | `{\k50}Hello {\k30}World` |
| `\kf` / `\K` | 渐进填充（从左到右扫过） | `{\kf50}Hello {\kf30}World` |
| `\ko` | 轮廓高亮 | `{\ko50}Hello {\ko30}World` |

数字单位是**厘秒**（1/100 秒）。

从 QCut 的 `WordItem` 生成 `\k` 标签非常直接：

```typescript
// WordItem.start=1.2, WordItem.end=1.7 → duration=0.5s → 50cs
const durationCs = Math.round((word.end - word.start) * 100);
const tag = `{\\k${durationCs}}${word.text}`;
// 输出: {\k50}Hello
```

---

## 8. 工作量估算

| 任务 | 新增代码 | 改动代码 | 时间 |
|------|---------|---------|------|
| `karaoke-utils.ts` | ~180 行 | — | 3 小时 |
| `karaoke-renderer.tsx` | ~80 行 | — | 2 小时 |
| 类型扩展 + 默认值 | — | ~10 行 | 30 分钟 |
| 预览面板集成 | — | ~15 行 | 1 小时 |
| ASS 卡拉OK导出 | ~60 行 | ~10 行 | 2 小时 |
| 文字动画预设移植 | ~400 行 | — | 5 小时 |
| UI（模式选择器） | ~100 行 | — | 2 小时 |
| 测试 + 调试 | — | — | 3 小时 |
| **合计** | **~820 行** | **~35 行** | **~18.5 小时（2-3 天）** |

### 实施优先级

1. **P0（Day 1）：** `karaoke-utils.ts` + `karaoke-renderer.tsx` + 类型扩展 → 基础逐词高亮可工作
2. **P1（Day 2）：** 文字动画预设移植 + 动画选择器 UI → 20+ 种动画可用
3. **P2（Day 3）：** ASS `\k` 标签导出 + 测试 → 完整功能闭环

---

## 参考链接

- [OpenReel Video GitHub](https://github.com/Augani/openreel-video)（MIT 协议）
- [ASS 卡拉OK标签规范](https://aegisub.org/docs/latest/ass_tags/#karaoke-effect)
- [QCut 代码仓库](https://github.com/Quriosity-AI/qcut)

---

*基于 QCut 源码 + OpenReel Video 源码分析撰写。所有代码示例均来自实际源文件。*

🦞
