# QCut 能从 OpenReel Video 借到什么？完整代码复用分析

> OpenReel Video 是一个 130K+ 行、MIT 许可的浏览器端视频编辑器，技术栈和 QCut 高度重合（React + TypeScript + WebCodecs + WebGPU）。本文逐个功能拆解哪些代码可以直接搬、哪些需要改、哪些只能参考架构。

**仓库地址：** https://github.com/Augani/openreel-video
**许可证：** MIT（可商用）
**总代码量：** ~158K 行 TypeScript（含测试）

---

## 目录

1. [仓库结构总览](#仓库结构总览)
2. [功能文件映射表](#功能文件映射表)
3. [Tier 1：直接可复用（~天级）](#tier-1直接可复用天级)
4. [Tier 2：需要适配但逻辑可移植（~周级）](#tier-2需要适配但逻辑可移植周级)
5. [Tier 3：架构参考](#tier-3架构参考)
6. [总结](#总结)

---

## 仓库结构总览

```
openreel-video/
├── apps/
│   ├── web/                    # 主编辑器 Web 应用
│   │   └── src/
│   │       ├── bridges/        # 核心引擎 ↔ React 的桥接层
│   │       ├── components/     # UI 组件（Inspector面板、Timeline等）
│   │       ├── stores/         # Zustand 状态管理
│   │       └── services/       # 应用层服务
│   └── image/                  # 图片编辑器（独立应用）
├── packages/
│   ├── core/                   # ⭐ 核心引擎（无UI依赖！）
│   │   └── src/
│   │       ├── audio/          # 音频引擎（beat检测、降噪、闪避等）
│   │       ├── video/          # 视频引擎（WebGPU渲染、调色、关键帧等）
│   │       ├── text/           # 文字引擎（字幕、动画、卡拉OK）
│   │       ├── effects/        # 效果引擎（混合模式、粒子）
│   │       ├── export/         # 导出引擎（WebCodecs编码）
│   │       ├── animation/      # 动画系统（缓动函数、GSAP引擎）
│   │       ├── graphics/       # 图形引擎（贴纸、SVG）
│   │       ├── timeline/       # 时间线管理
│   │       ├── media/          # 媒体导入（MediaBunny）
│   │       ├── wasm/           # WASM 加速（beat检测、FFT）
│   │       └── types/          # 类型定义
│   └── ui/                     # UI 组件库（shadcn/radix）
└── package.json                # pnpm monorepo
```

**关键发现：** `packages/core` 是纯逻辑层，不依赖任何 UI 框架。QCut 可以直接 npm install 引用，或者 cherry-pick 单个文件。

---

## 功能文件映射表

| 功能 | 核心文件 | 行数 | UI组件 |
|------|---------|------|--------|
| 卡拉OK字幕 | `core/src/text/caption-animation-renderer.ts` | ~280 | `AudioTextSyncPanel.tsx` |
| Beat检测 | `core/src/audio/beat-detection-engine.ts` | ~310 | `BeatSyncSection.tsx` |
| 音频闪避 | `core/src/audio/volume-automation.ts` (AudioDucker) | ~200 | `AudioDuckingSection.tsx` |
| 噪音消除 | `core/src/audio/noise-reduction.ts` | ~310 | `NoiseReductionSection.tsx` |
| WebGPU渲染 | `core/src/video/webgpu-renderer-impl.ts` | ~1070 | `render-bridge.ts` |
| 文字动画 | `core/src/text/text-animation-presets.ts` | ~520 | `TextAnimationSection.tsx` |
| 3D LUT | `core/src/video/color-grading-engine.ts` (applyLUT) | ~50 | `LUTLoader.tsx` |
| 混合模式 | `core/src/effects/blend-modes.ts` | ~180 | `BlendingSection.tsx` |
| ProRes导出 | `core/src/export/types.ts` + `export-engine.ts` | ~1400 | `ExportDialog.tsx` |
| 调色系统 | `core/src/video/color-grading-engine.ts` | ~580 | `ColorGradingSection.tsx` |
| 关键帧系统 | `core/src/video/keyframe-engine.ts` | ~430 | `KeyframesSection.tsx` |

---

## Tier 1：直接可复用（~天级）

这些模块是纯 TypeScript 逻辑，无 UI 耦合，可以直接 copy 到 QCut。

### 1.1 混合模式引擎

**文件：** `packages/core/src/effects/blend-modes.ts`
**复用度：** ⭐⭐⭐⭐⭐ 直接可用
**集成时间：** 1 天

同时提供了 Canvas2D compositeOperation 映射和 WebGPU/WebGL shader 代码。QCut Desktop 用 Canvas 模式，Web 版用 shader。

```typescript
// 14 种混合模式 + 对应 GLSL shader
export type BlendMode =
  | "normal" | "multiply" | "screen" | "overlay"
  | "darken" | "lighten" | "color-dodge" | "color-burn"
  | "hard-light" | "soft-light" | "difference" | "exclusion"
  | "add" | "subtract";

// Canvas2D 直接映射
applyBlendMode(ctx, mode) {
  switch (mode) {
    case "multiply": ctx.globalCompositeOperation = "multiply"; break;
    case "screen": ctx.globalCompositeOperation = "screen"; break;
    // ...
  }
}

// WebGPU shader（可用于 QCut Web）
getBlendShader(mode: BlendMode): string {
  // 返回 GLSL blend 函数
  // multiply: return base * blend;
  // screen: return 1.0 - (1.0 - base) * (1.0 - blend);
}
```

**注意：** QCut Desktop 已有部分混合模式，主要价值是 shader 代码可以用于 Web 版。

### 1.2 文字动画预设

**文件：** `packages/core/src/text/text-animation-presets.ts`
**复用度：** ⭐⭐⭐⭐⭐ 直接可用
**集成时间：** 1-2 天

19 种文字动画，全部是纯数学计算，零依赖：

```typescript
const ANIMATION_MAP: Record<TextAnimationPreset, AnimationFn> = {
  none, typewriter, fade,
  "slide-left", "slide-right", "slide-up", "slide-down",
  scale, blur, bounce, rotate,
  wave, shake, pop, glitch,
  split, flip, "word-by-word", rainbow
};

// 每种动画返回 UnitAnimationState
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

**关键设计：** 动画以 character / word / line 为单位，每个单位独立计算 stagger 延迟。QCut 只需要在自己的文字渲染层调用 `calculateUnitAnimationState(ctx)` 即可。

### 1.3 卡拉OK字幕（逐字高亮）

**文件：** `packages/core/src/text/caption-animation-renderer.ts`
**复用度：** ⭐⭐⭐⭐⭐ 直接可用
**集成时间：** 1-2 天

6 种字幕动画风格：

```typescript
type CaptionAnimationStyle =
  | "none"           // 静态
  | "word-highlight" // 当前词高亮
  | "word-by-word"   // 逐字出现
  | "karaoke"        // 卡拉OK渐进填充
  | "bounce"         // 弹跳出现
  | "typewriter";    // 打字机效果

// 卡拉OK核心逻辑：基于 word timing 做渐进填充
function renderKaraoke(subtitle, currentTime) {
  segments = subtitle.words.map(word => {
    const progress = clamp(
      (currentTime - word.startTime) / (word.endTime - word.startTime), 0, 1
    );
    // 用 CSS linear-gradient 做部分填充效果
    color = `linear-gradient(90deg, 
      ${highlightColor} ${progress * 100}%, 
      ${upcomingColor} ${progress * 100}%)`;
    return { text: word.text, color, scale: isActive ? 1.05 : 1 };
  });
}
```

**前提：** 需要 word-level timestamp 数据（来自 Whisper 转录）。QCut 已经有 Whisper 集成，所以这个可以直接用。

### 1.4 缓动函数库

**文件：** `packages/core/src/animation/easing-functions.ts`
**复用度：** ⭐⭐⭐⭐⭐ 直接可用
**集成时间：** 半天

20+ 种缓动函数（easeInQuad, easeOutBounce, easeInOutElastic 等），纯数学，零依赖。

---

## Tier 2：需要适配但逻辑可移植（~周级）

### 2.1 Beat 检测引擎

**文件：**
- `packages/core/src/audio/beat-detection-engine.ts` — 核心算法
- `packages/core/src/wasm/beat-detection/` — WASM 加速
- `apps/web/src/bridges/beat-sync-bridge.ts` — 应用层集成
- `packages/core/src/text/audio-text-sync-engine.ts` — beat 同步编排

**复用度：** ⭐⭐⭐⭐ 逻辑可移植
**集成时间：** 3-5 天
**适配工作：** WASM 模块需要为 Electron 环境重新编译

核心算法流程：

```typescript
class BeatDetectionEngine {
  // 1. RMS 能量检测 → onset 事件
  detectOnsets(samples, sampleRate) {
    // 用 WASM 加速计算 RMS 能量
    wasmProcessor.computeRMSEnergies(samples, windowSize, hopSize, energies);
    // 自适应阈值（中位数 + 均值混合）
    threshold = median + (mean - median) * (1 - sensitivity);
    // 峰值检测：局部最大 + 超阈值 + 有上升沿 + 最小间距
  }

  // 2. 间隔直方图 → BPM 候选
  calculateBpm(onsets, duration) {
    // 支持半拍/双拍检测
    // 置信度 = 1 - |expectedBeats - actualBeats| / expectedBeats
  }

  // 3. 节拍网格生成
  generateBeats(bpm, duration, onsets) {
    // 对齐到最近的 onset
    // 未对齐的用 strength=0.5 标记
  }
}
```

**依赖：** WASM beat-detection 模块（`packages/core/src/wasm/beat-detection/`）。QCut Desktop 可以直接用 Node.js 的 FFT 替代，Web 版保留 WASM。

### 2.2 噪音消除（频谱减法）

**文件：**
- `packages/core/src/audio/noise-reduction.ts` — SpectralNoiseReducer
- `packages/core/src/audio/fft.ts` — 纯 JS FFT
- `packages/core/src/wasm/fft/` — WASM FFT 加速

**复用度：** ⭐⭐⭐⭐ 逻辑可移植
**集成时间：** 3-5 天

实现了完整的频谱减法降噪：

```typescript
class SpectralNoiseReducer {
  // 第一步：学习噪声特征
  learnNoiseProfile(noiseBuffer: AudioBuffer): NoiseProfile {
    // 对静音段做 FFT，统计每个频率 bin 的均值和标准差
  }

  // 第二步：逐帧处理
  processChannel(input, output) {
    for (frame of frames) {
      // 1. 加窗（Hann窗）
      // 2. FFT → 幅度+相位
      // 3. 频谱减法（过减因子 + 频谱底噪）
      // 4. IFFT 重建
      // 5. Overlap-Add 合成
    }
  }

  // 频谱减法核心
  applySpectralSubtraction(magnitudes) {
    subtracted = mag - overSubtraction * (noiseMag + noiseStd);
    floor = noiseMag * (1 - reduction) * thresholdLinear;
    return max(subtracted, floor) * (1 - smoothing) + mag * smoothing;
  }
}

// 自动噪声检测：找到音频中最安静的片段
autoLearnNoiseProfile(buffer) {
  segments = detectNoiseSegments(buffer, -50dB, 0.5s);
  // 用最长的静音段学习噪声特征
}
```

**注意：** 这是单 pass 频谱减法。README 提到"3-pass noise reduction"，但代码实际是 1 pass + 自动噪声检测。QCut 可以在此基础上做多 pass 迭代。

### 2.3 音频闪避（Audio Ducking）

**文件：**
- `packages/core/src/audio/volume-automation.ts` — `AudioDucker` 类
- `apps/web/src/components/editor/inspector/AudioDuckingSection.tsx` — UI

**复用度：** ⭐⭐⭐⭐ 逻辑可移植
**集成时间：** 2-3 天

```typescript
class AudioDucker {
  // 分析语音轨检测活跃区间
  detectActiveRegions(buffer, threshold, minDuration) → ranges[]

  // 生成闪避关键帧
  generateDuckingKeyframes(dialogBuffer, config) {
    ranges = detectActiveRegions(dialogBuffer, config.threshold);
    for (range of ranges) {
      // 在人声前 attack 时间开始降低
      // 在人声后 release 时间恢复
      keyframes.push({ time: duckStart, value: originalVolume });
      keyframes.push({ time: duckStart + attack, value: duckedVolume });
      keyframes.push({ time: range.end, value: duckedVolume });
      keyframes.push({ time: range.end + release, value: originalVolume });
    }
  }

  // 实时闪避（用于预览）
  createRealtimeDucker(dialogSource, musicGain, config) {
    // 用 AnalyserNode 实时检测 + requestAnimationFrame
  }
}
```

**预设：** Subtle / Moderate / Aggressive 三档，参数已调好。

### 2.4 调色系统（Color Wheels + Curves + HSL）

**文件：** `packages/core/src/video/color-grading-engine.ts`
**UI：** `ColorGradingSection.tsx` + `ColorWheelsControl.tsx` + `CurvesEditor.tsx` + `HSLControls.tsx`
**复用度：** ⭐⭐⭐⭐ Shader 代码可直接用
**集成时间：** 5-7 天

完整的专业调色管线：

```glsl
// Color Wheels Shader（WebGL2）
void main() {
  vec4 color = texture(u_texture, v_texCoord);
  float luma = dot(color.rgb, vec3(0.299, 0.587, 0.114));
  
  // 三区域权重
  float shadowWeight = 1.0 - smoothstep(0.0, 0.5, luma);
  float highlightWeight = smoothstep(0.5, 1.0, luma);
  float midtoneWeight = 1.0 - shadowWeight - highlightWeight;
  
  // 应用色彩偏移
  rgb += u_shadows * shadowWeight;
  rgb += u_midtones * midtoneWeight;
  rgb += u_highlights * highlightWeight;
  
  // Lift / Gamma / Gain
  rgb = rgb + u_shadowsLift * shadowWeight;
  rgb = pow(rgb, vec3(1.0 / u_midtonesGamma));
  rgb = rgb * (1.0 + (u_highlightsGain - 1.0) * highlightWeight);
}
```

**包含：**
- Color Wheels（Lift / Gamma / Gain）— WebGL2 shader
- Curves（Catmull-Rom 样条插值）— CPU 实现
- HSL 调整（8 色相范围独立调节）— WebGL2 shader + CPU fallback
- 3D LUT 加载/应用 — 三线性插值
- Waveform / Vectorscope / Histogram 示波器

### 2.5 关键帧动画系统

**文件：** `packages/core/src/video/keyframe-engine.ts`
**复用度：** ⭐⭐⭐⭐ 核心逻辑可移植
**集成时间：** 5-7 天

```typescript
class KeyframeEngine {
  // 在任意时间点获取插值后的值
  getValueAtTime(keyframes, time): {
    value,           // 插值结果
    keyframeA,       // 前一个关键帧
    keyframeB,       // 后一个关键帧
    progress,        // 线性进度
    easedProgress    // 缓动后进度
  }

  // 支持 7 种缓动 + 自定义 Bezier
  applyEasingPreset(t, preset): number
  // linear, ease-in, ease-out, ease-in-out, bounce, elastic, spring

  // 支持 Bezier 手柄编辑
  updateBezierHandles(keyframes, id, handles)

  // 运动路径可视化
  getMotionPath(clipId, keyframes, sampleCount=100): MotionPath

  // 关键帧复制/粘贴
  copyKeyframes() / pasteKeyframes()

  // 深度值插值（支持数字、对象递归）
  interpolateValue(a, b, progress)
}
```

**适配点：** QCut 已有自己的关键帧系统。价值在于 Bezier 手柄编辑、运动路径可视化、复制粘贴这些高级功能。

### 2.6 3D LUT 加载器

**文件：**
- `apps/web/src/components/editor/inspector/LUTLoader.tsx` — .cube 文件解析
- `packages/core/src/video/color-grading-engine.ts` (applyLUT) — LUT 应用

**复用度：** ⭐⭐⭐⭐ 可直接用
**集成时间：** 2-3 天

```typescript
// .cube 文件解析器
function parseCubeLUT(content: string): LUTData {
  // 解析 LUT_3D_SIZE、TITLE、DOMAIN_*
  // 解析 RGB 三元组，归一化到 0-255
  // 返回 { data: Uint8Array, size: number, intensity: number }
}

// 三线性插值应用
applyLUT(image, lut) {
  for (pixel of image) {
    // 3D 索引计算
    rIdx = r * (lutSize - 1); // 连续索引
    // 8 个邻居的三线性插值
    // intensity 混合原图
    result = mix(original, lutColor, lut.intensity);
  }
}
```

---

## Tier 3：架构参考

### 3.1 WebGPU 渲染管线

**文件：**
- `packages/core/src/video/webgpu-renderer-impl.ts` (~1070 行)
- `packages/core/src/video/webgpu-effects-processor.ts`
- `packages/core/src/video/gpu-compositor.ts`
- `packages/core/src/video/shaders/index.ts`

**复用度：** ⭐⭐⭐ 架构参考
**集成时间：** 2-4 周

WebGPU 渲染器是 OpenReel 最核心的部分，但也是最难直接搬的：

- 深度绑定了 OpenReel 的层级合成模型
- 使用了双缓冲、帧缓存、TextureCache 等基础设施
- 依赖 OpenReel 特定的 `RenderLayer` 类型系统

**QCut 可以参考：**
1. WebGPU 初始化流程（adapter → device → context → pipeline）
2. Shader 编译和管理模式
3. 纹理缓存策略（`TextureCache` 类）
4. Canvas2D fallback 模式（`canvas2d-fallback-renderer.ts`）

### 3.2 WebCodecs 导出管线 + ProRes

**文件：**
- `packages/core/src/export/export-engine.ts` (~1400 行)
- `packages/core/src/export/types.ts`
- `packages/core/src/video/video-engine.ts`

**复用度：** ⭐⭐⭐ 架构参考
**集成时间：** 2-4 周

ProRes 导出支持 6 种 profile：

```typescript
interface VideoExportSettings {
  codec: "h264" | "h265" | "vp8" | "vp9" | "av1" | "prores";
  proresProfile?: "proxy" | "lt" | "standard" | "hq" | "4444" | "4444xq";
  colorDepth?: 8 | 10 | 12;
  pixelFormat?: "yuv420" | "yuv422" | "yuv444" | "rgb";
}
```

**注意：** 实际 ProRes 编码依赖 `mediabunny` 库（OpenReel 自己的 WASM 编解码器）。QCut Desktop 可以继续用 FFmpeg，Web 版可以参考这个 WebCodecs 管线。

### 3.3 Bridge 架构模式

**文件：** `apps/web/src/bridges/` 目录

OpenReel 用 Bridge 模式把核心引擎和 React UI 解耦：

```
audio-bridge.ts          — 音频引擎 ↔ React
beat-sync-bridge.ts      — Beat同步 ↔ React
render-bridge.ts         — 渲染引擎 ↔ React
text-bridge.ts           — 文字引擎 ↔ React
media-bridge.ts          — 媒体管理 ↔ React
```

**QCut 可以学习：** 当 QCut 做 Web 版时，用类似 bridge 层把现有的 Electron native 模块和 Web API 做适配。

---

## 总结

### 优先级排序

| 优先级 | 功能 | 复用度 | 时间 | 价值 |
|--------|------|--------|------|------|
| 🔴 P0 | 文字动画 19 种 | 直接复用 | 1-2 天 | QCut 目前文字动画很少 |
| 🔴 P0 | 卡拉OK字幕 | 直接复用 | 1-2 天 | 短视频刚需 |
| 🔴 P0 | 混合模式 shader | 直接复用 | 1 天 | Web 版必需 |
| 🟡 P1 | Beat 检测 | 适配 WASM | 3-5 天 | 音乐视频刚需 |
| 🟡 P1 | 音频闪避 | 逻辑移植 | 2-3 天 | Vlog 刚需 |
| 🟡 P1 | 3D LUT 加载器 | 直接复用 | 2-3 天 | 专业调色刚需 |
| 🟡 P1 | 调色 shader | shader 移植 | 5-7 天 | 专业功能 |
| 🟢 P2 | 噪音消除 | 逻辑移植 | 3-5 天 | 有用但非刚需 |
| 🟢 P2 | 关键帧高级功能 | 选择性移植 | 5-7 天 | 增强现有系统 |
| 🔵 P3 | WebGPU 渲染器 | 架构参考 | 2-4 周 | Web 版长期规划 |
| 🔵 P3 | WebCodecs 导出 | 架构参考 | 2-4 周 | Web 版长期规划 |

### 集成策略建议

1. **先搬纯逻辑：** `text-animation-presets.ts`、`caption-animation-renderer.ts`、`blend-modes.ts` 这三个文件直接 copy，改下 import 路径就能用
2. **音频模块整包搬：** `packages/core/src/audio/` 整个目录的设计很好，但需要处理 WASM 依赖
3. **调色 shader 存起来：** 即使现在不用 WebGL，这些 shader 代码等 QCut Web 版时直接能用
4. **不要搬渲染器：** WebGPU 渲染器和 QCut 的架构差异太大，参考思路就好

### 风险提醒

- OpenReel 的 `mediabunny` 是外部依赖，编解码相关功能不能直接用
- WASM 模块需要为 Electron 环境重新编译（或者用 JS fallback）
- 部分功能（如噪音消除）在 README 宣称的能力（3-pass）和实际代码（1-pass）有差距
- ProRes 支持在浏览器端有限，QCut Desktop 继续用 FFmpeg 更靠谱

---

*分析基于 OpenReel Video 仓库 2026-03-18 版本。MIT 许可允许商用。*

🦞
