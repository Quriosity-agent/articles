# What QCut Can Borrow from OpenReel Video: A Complete Code Reuse Analysis

> OpenReel Video is a 130K+ line, MIT-licensed, browser-based video editor with near-identical tech stack to QCut (React + TypeScript + WebCodecs + WebGPU). This article maps every reusable feature — exact file paths, integration effort, and gotchas.

**Repository:** https://github.com/Augani/openreel-video
**License:** MIT (commercial use OK)
**Total codebase:** ~158K lines of TypeScript (including tests)

---

## Table of Contents

1. [Repository Structure](#repository-structure)
2. [Feature-to-File Mapping](#feature-to-file-mapping)
3. [Tier 1: Directly Reusable (~days)](#tier-1-directly-reusable-days)
4. [Tier 2: Needs Adaptation (~1 week)](#tier-2-needs-adaptation-1-week)
5. [Tier 3: Architecture Reference Only](#tier-3-architecture-reference-only)
6. [Summary & Integration Strategy](#summary--integration-strategy)

---

## Repository Structure

```
openreel-video/
├── apps/
│   ├── web/                    # Main editor web app
│   │   └── src/
│   │       ├── bridges/        # Core engine ↔ React bridge layer
│   │       ├── components/     # UI (Inspector panels, Timeline, etc.)
│   │       ├── stores/         # Zustand state management
│   │       └── services/       # App-level services
│   └── image/                  # Standalone image editor
├── packages/
│   ├── core/                   # ⭐ Core engine (zero UI dependencies!)
│   │   └── src/
│   │       ├── audio/          # Audio engine (beat detection, noise reduction, ducking)
│   │       ├── video/          # Video engine (WebGPU rendering, color grading, keyframes)
│   │       ├── text/           # Text engine (subtitles, animations, karaoke)
│   │       ├── effects/        # Effects engine (blend modes, particles)
│   │       ├── export/         # Export engine (WebCodecs encoding)
│   │       ├── animation/      # Animation system (easing functions, GSAP engine)
│   │       ├── graphics/       # Graphics engine (stickers, SVG)
│   │       ├── timeline/       # Timeline management
│   │       ├── media/          # Media import (MediaBunny)
│   │       ├── wasm/           # WASM acceleration (beat detection, FFT)
│   │       └── types/          # Type definitions
│   └── ui/                     # UI component library (shadcn/radix)
└── package.json                # pnpm monorepo
```

**Key finding:** `packages/core` is a pure logic layer with zero UI framework dependencies. QCut can either npm install it directly or cherry-pick individual files.

---

## Feature-to-File Mapping

| Feature | Core Files | Lines | UI Component |
|---------|-----------|-------|-------------|
| Karaoke subtitles | `core/src/text/caption-animation-renderer.ts` | ~280 | `AudioTextSyncPanel.tsx` |
| Beat detection | `core/src/audio/beat-detection-engine.ts` | ~310 | `BeatSyncSection.tsx` |
| Audio ducking | `core/src/audio/volume-automation.ts` (AudioDucker) | ~200 | `AudioDuckingSection.tsx` |
| Noise reduction | `core/src/audio/noise-reduction.ts` | ~310 | `NoiseReductionSection.tsx` |
| WebGPU rendering | `core/src/video/webgpu-renderer-impl.ts` | ~1070 | `render-bridge.ts` |
| Text animations | `core/src/text/text-animation-presets.ts` | ~520 | `TextAnimationSection.tsx` |
| 3D LUT support | `core/src/video/color-grading-engine.ts` (applyLUT) | ~50 | `LUTLoader.tsx` |
| Blend modes | `core/src/effects/blend-modes.ts` | ~180 | `BlendingSection.tsx` |
| ProRes export | `core/src/export/types.ts` + `export-engine.ts` | ~1400 | `ExportDialog.tsx` |
| Color grading | `core/src/video/color-grading-engine.ts` | ~580 | `ColorGradingSection.tsx` |
| Keyframe system | `core/src/video/keyframe-engine.ts` | ~430 | `KeyframesSection.tsx` |

---

## Tier 1: Directly Reusable (~days)

These modules are pure TypeScript logic with zero UI coupling — copy and use.

### 1.1 Blend Mode Engine

**File:** `packages/core/src/effects/blend-modes.ts`
**Reusability:** ⭐⭐⭐⭐⭐ Drop-in
**Integration time:** 1 day

Provides both Canvas2D compositeOperation mapping AND WebGPU/WebGL GLSL shaders for 14 blend modes:

```typescript
export type BlendMode =
  | "normal" | "multiply" | "screen" | "overlay"
  | "darken" | "lighten" | "color-dodge" | "color-burn"
  | "hard-light" | "soft-light" | "difference" | "exclusion"
  | "add" | "subtract";

// Canvas2D path (QCut Desktop)
applyBlendMode(ctx, mode) {
  ctx.globalCompositeOperation = "multiply"; // etc.
}

// WebGL/WebGPU shader path (QCut Web)
getBlendShader(mode: BlendMode): string {
  // Returns GLSL blend function per mode
  // multiply: return base * blend;
  // screen: return 1.0 - (1.0 - base) * (1.0 - blend);
}
```

### 1.2 Text Animation Presets (19 types)

**File:** `packages/core/src/text/text-animation-presets.ts`
**Reusability:** ⭐⭐⭐⭐⭐ Drop-in
**Integration time:** 1-2 days

19 text animation types, all pure math, zero dependencies:

```typescript
const ANIMATION_MAP = {
  none, typewriter, fade,
  "slide-left", "slide-right", "slide-up", "slide-down",
  scale, blur, bounce, rotate,
  wave, shake, pop, glitch,
  split, flip, "word-by-word", rainbow
};

// Each animation returns per-unit state
interface UnitAnimationState {
  opacity: number;
  scale: { x: number; y: number };
  rotation: number;
  offsetX: number;
  offsetY: number;
  blur: number;
  color?: string;
  skewX?: number;
}
```

**Key design:** Animations operate on character/word/line units with independent stagger delays. QCut just needs to call `calculateUnitAnimationState(ctx)` from its text renderer.

### 1.3 Karaoke-Style Subtitles (Word-by-Word Highlighting)

**File:** `packages/core/src/text/caption-animation-renderer.ts`
**Reusability:** ⭐⭐⭐⭐⭐ Drop-in
**Integration time:** 1-2 days

6 caption animation styles:

```typescript
type CaptionAnimationStyle =
  | "none"           // Static text
  | "word-highlight" // Current word highlighted
  | "word-by-word"   // Words appear one at a time
  | "karaoke"        // Progressive fill (like karaoke)
  | "bounce"         // Bounce in
  | "typewriter";    // Typewriter effect

// Karaoke core: progressive gradient fill based on word timing
function renderKaraoke(subtitle, currentTime) {
  segments = subtitle.words.map(word => {
    const progress = clamp(
      (currentTime - word.startTime) / (word.endTime - word.startTime), 0, 1
    );
    color = `linear-gradient(90deg, 
      ${highlightColor} ${progress * 100}%, 
      ${upcomingColor} ${progress * 100}%)`;
    return { text: word.text, color, scale: isActive ? 1.05 : 1 };
  });
}
```

**Prerequisite:** Requires word-level timestamps (from Whisper transcription). QCut already has Whisper integration, so this drops right in.

### 1.4 Easing Functions Library

**File:** `packages/core/src/animation/easing-functions.ts`
**Reusability:** ⭐⭐⭐⭐⭐ Drop-in
**Integration time:** Half a day

20+ easing functions (easeInQuad, easeOutBounce, easeInOutElastic, etc.), pure math, zero deps.

---

## Tier 2: Needs Adaptation (~1 week)

### 2.1 Beat Detection Engine

**Files:**
- `packages/core/src/audio/beat-detection-engine.ts` — Core algorithm
- `packages/core/src/wasm/beat-detection/` — WASM acceleration
- `apps/web/src/bridges/beat-sync-bridge.ts` — App integration
- `packages/core/src/text/audio-text-sync-engine.ts` — Beat sync choreography

**Reusability:** ⭐⭐⭐⭐ Logic portable
**Integration time:** 3-5 days
**Adaptation:** WASM module needs recompilation for Electron; or use JS fallback

Algorithm pipeline:

```typescript
class BeatDetectionEngine {
  // 1. RMS energy analysis → onset detection
  detectOnsets(samples, sampleRate) {
    // WASM-accelerated RMS energy computation
    wasmProcessor.computeRMSEnergies(samples, windowSize, hopSize, energies);
    // Adaptive threshold: median + mean hybrid
    threshold = median + (mean - median) * (1 - sensitivity);
    // Peak detection: local max + above threshold + rising edge + min spacing
  }

  // 2. Interval histogram → BPM candidates
  calculateBpm(onsets, duration) {
    // Supports half-time and double-time detection
    // Confidence = 1 - |expectedBeats - actualBeats| / expectedBeats
  }

  // 3. Beat grid generation aligned to onsets
  generateBeats(bpm, duration, onsets) {
    // Snap to nearest onset within tolerance
    // Unaligned beats get strength=0.5
  }
}
```

### 2.2 Spectral Noise Reduction

**Files:**
- `packages/core/src/audio/noise-reduction.ts` — SpectralNoiseReducer
- `packages/core/src/audio/fft.ts` — Pure JS FFT
- `packages/core/src/wasm/fft/` — WASM FFT acceleration

**Reusability:** ⭐⭐⭐⭐ Logic portable
**Integration time:** 3-5 days

Full spectral subtraction pipeline:

```typescript
class SpectralNoiseReducer {
  // Step 1: Learn noise profile from quiet segment
  learnNoiseProfile(noiseBuffer: AudioBuffer): NoiseProfile {
    // FFT each frame, compute mean + stddev per frequency bin
  }

  // Step 2: Process audio frame-by-frame
  processChannel(input, output) {
    for (frame of frames) {
      // 1. Window (Hann)
      // 2. FFT → magnitude + phase
      // 3. Spectral subtraction (over-subtraction + spectral floor)
      // 4. IFFT reconstruction
      // 5. Overlap-Add synthesis
    }
  }
}

// Auto noise detection: find quietest segment in audio
autoLearnNoiseProfile(buffer) {
  segments = detectNoiseSegments(buffer, -50dB, 0.5s);
  // Use longest quiet segment as noise reference
}
```

**Note:** The README claims "3-pass noise reduction" but the code implements 1-pass spectral subtraction + auto noise detection. QCut can iterate multiple passes on top of this.

### 2.3 Audio Ducking

**Files:**
- `packages/core/src/audio/volume-automation.ts` — `AudioDucker` class
- `apps/web/src/components/editor/inspector/AudioDuckingSection.tsx` — UI

**Reusability:** ⭐⭐⭐⭐ Logic portable
**Integration time:** 2-3 days

```typescript
class AudioDucker {
  // Analyze speech track for active regions
  detectActiveRegions(buffer, threshold, minDuration) → ranges[]

  // Generate ducking keyframes
  generateDuckingKeyframes(dialogBuffer, config: DuckingConfig) {
    ranges = detectActiveRegions(dialogBuffer, config.threshold);
    for (range of ranges) {
      // Ramp down before speech (attack)
      // Hold during speech
      // Ramp back up after speech (release)
    }
  }

  // Real-time ducking for preview
  createRealtimeDucker(dialogSource, musicGain, config) {
    // AnalyserNode + requestAnimationFrame
  }
}
```

**Built-in presets:** Subtle / Moderate / Aggressive with pre-tuned parameters.

### 2.4 Color Grading System (Wheels + Curves + HSL)

**File:** `packages/core/src/video/color-grading-engine.ts`
**UI:** `ColorGradingSection.tsx` + `ColorWheelsControl.tsx` + `CurvesEditor.tsx` + `HSLControls.tsx`
**Reusability:** ⭐⭐⭐⭐ Shaders directly reusable
**Integration time:** 5-7 days

Professional color grading pipeline with WebGL2 shaders:

```glsl
// Color Wheels Shader
void main() {
  vec4 color = texture(u_texture, v_texCoord);
  float luma = dot(color.rgb, vec3(0.299, 0.587, 0.114));
  
  // Three-zone weighting
  float shadowWeight = 1.0 - smoothstep(0.0, 0.5, luma);
  float highlightWeight = smoothstep(0.5, 1.0, luma);
  float midtoneWeight = 1.0 - shadowWeight - highlightWeight;
  
  // Apply per-zone color shift + Lift/Gamma/Gain
  rgb += u_shadows * shadowWeight + u_midtones * midtoneWeight 
       + u_highlights * highlightWeight;
  rgb = pow(rgb + u_shadowsLift * shadowWeight, vec3(1.0 / u_midtonesGamma));
  rgb *= (1.0 + (u_highlightsGain - 1.0) * highlightWeight);
}
```

**Includes:**
- Color Wheels (Lift / Gamma / Gain) — WebGL2 shader
- Curves (Catmull-Rom spline interpolation) — CPU
- HSL adjustments (8 hue ranges, independent control) — WebGL2 + CPU fallback
- 3D LUT load/apply — Trilinear interpolation
- Waveform / Vectorscope / Histogram scopes

### 2.5 Keyframe Animation System

**File:** `packages/core/src/video/keyframe-engine.ts`
**Reusability:** ⭐⭐⭐⭐ Core logic portable
**Integration time:** 5-7 days

```typescript
class KeyframeEngine {
  // Interpolated value at any point in time
  getValueAtTime(keyframes, time) → { value, keyframeA, keyframeB, progress }

  // 7 easing presets + custom Bezier
  applyEasingPreset(t, preset) // linear, ease-in/out, bounce, elastic, spring

  // Bezier handle editing
  updateBezierHandles(keyframes, id, handles)

  // Motion path visualization (sampled at N points)
  getMotionPath(clipId, keyframes, sampleCount=100)

  // Copy/paste keyframes across clips
  copyKeyframes() / pasteKeyframes()

  // Deep value interpolation (numbers + nested objects)
  interpolateValue(a, b, progress)
}
```

**Value for QCut:** Bezier handle editing, motion path visualization, and copy/paste features that go beyond QCut's current keyframe system.

### 2.6 3D LUT Loader

**Files:**
- `apps/web/src/components/editor/inspector/LUTLoader.tsx` — .cube file parser
- `packages/core/src/video/color-grading-engine.ts` (applyLUT) — LUT application

**Reusability:** ⭐⭐⭐⭐ Drop-in
**Integration time:** 2-3 days

```typescript
// .cube file parser
function parseCubeLUT(content: string): LUTData {
  // Parse LUT_3D_SIZE, TITLE, DOMAIN_*
  // Parse RGB triplets, normalize to 0-255
  // Returns { data: Uint8Array, size: number, intensity: number }
}

// Trilinear interpolation LUT application
applyLUT(image, lut) {
  for (pixel of image) {
    // 3D index computation → 8-neighbor trilinear interpolation
    result = mix(original, lutColor, lut.intensity);
  }
}
```

---

## Tier 3: Architecture Reference Only

### 3.1 WebGPU Rendering Pipeline

**Files:**
- `packages/core/src/video/webgpu-renderer-impl.ts` (~1070 lines)
- `packages/core/src/video/webgpu-effects-processor.ts`
- `packages/core/src/video/gpu-compositor.ts`
- `packages/core/src/video/shaders/index.ts`

**Reusability:** ⭐⭐⭐ Architecture reference
**Integration time:** 2-4 weeks

The WebGPU renderer is OpenReel's most complex subsystem and too deeply coupled to its layer composition model for direct reuse. However, QCut can reference:
1. WebGPU initialization flow (adapter → device → context → pipeline)
2. Shader compilation and management patterns
3. Texture caching strategy (`TextureCache` class)
4. Canvas2D fallback architecture (`canvas2d-fallback-renderer.ts`)

### 3.2 WebCodecs Export Pipeline + ProRes

**Files:**
- `packages/core/src/export/export-engine.ts` (~1400 lines)
- `packages/core/src/export/types.ts`

**Reusability:** ⭐⭐⭐ Architecture reference
**Integration time:** 2-4 weeks

ProRes support with 6 profiles:

```typescript
interface VideoExportSettings {
  codec: "h264" | "h265" | "vp8" | "vp9" | "av1" | "prores";
  proresProfile?: "proxy" | "lt" | "standard" | "hq" | "4444" | "4444xq";
  colorDepth?: 8 | 10 | 12;
  pixelFormat?: "yuv420" | "yuv422" | "yuv444" | "rgb";
}
```

**Caveat:** Actual ProRes encoding relies on `mediabunny` (OpenReel's custom WASM codec library). QCut Desktop should continue using FFmpeg. QCut Web can reference the WebCodecs pipeline architecture.

### 3.3 Bridge Architecture Pattern

**Directory:** `apps/web/src/bridges/`

OpenReel uses a Bridge pattern to decouple core engines from React:

```
audio-bridge.ts          — Audio engine ↔ React
beat-sync-bridge.ts      — Beat sync ↔ React
render-bridge.ts         — Render engine ↔ React
text-bridge.ts           — Text engine ↔ React
media-bridge.ts          — Media management ↔ React
```

**Value for QCut:** When building the Web version, use a similar bridge layer to adapt existing Electron native modules to Web APIs.

---

## Summary & Integration Strategy

### Priority Matrix

| Priority | Feature | Reusability | Time | Value |
|----------|---------|------------|------|-------|
| 🔴 P0 | 19 text animations | Drop-in | 1-2 days | QCut currently has few text animations |
| 🔴 P0 | Karaoke subtitles | Drop-in | 1-2 days | Short-form video essential |
| 🔴 P0 | Blend mode shaders | Drop-in | 1 day | Required for Web version |
| 🟡 P1 | Beat detection | Adapt WASM | 3-5 days | Music video essential |
| 🟡 P1 | Audio ducking | Port logic | 2-3 days | Vlog essential |
| 🟡 P1 | 3D LUT loader | Drop-in | 2-3 days | Professional color grading |
| 🟡 P1 | Color grading shaders | Port shaders | 5-7 days | Professional feature |
| 🟢 P2 | Noise reduction | Port logic | 3-5 days | Useful but not critical |
| 🟢 P2 | Advanced keyframes | Selective port | 5-7 days | Enhances existing system |
| 🔵 P3 | WebGPU renderer | Arch reference | 2-4 weeks | Long-term Web version |
| 🔵 P3 | WebCodecs export | Arch reference | 2-4 weeks | Long-term Web version |

### Recommended Integration Order

1. **Start with pure logic files:** Copy `text-animation-presets.ts`, `caption-animation-renderer.ts`, and `blend-modes.ts` directly — just fix import paths
2. **Port audio modules as a package:** The entire `packages/core/src/audio/` directory is well-designed, but handle WASM dependencies (JS fallback for Electron, keep WASM for Web)
3. **Bank the color grading shaders:** Even if not needed now, these WebGL2 shaders are ready for QCut Web
4. **Don't port the renderer:** The WebGPU renderer is too tightly coupled to OpenReel's architecture — reference the patterns only

### Risk Notes

- OpenReel's `mediabunny` is an external dependency — codec-related features can't be used directly
- WASM modules need recompilation for Electron (or use JS fallbacks)
- Some features (e.g., noise reduction) have gaps between README claims (3-pass) and actual implementation (1-pass)
- ProRes in browser is limited — QCut Desktop should stick with FFmpeg

---

*Analysis based on OpenReel Video repository as of 2026-03-18. MIT license permits commercial use.*

🦞
