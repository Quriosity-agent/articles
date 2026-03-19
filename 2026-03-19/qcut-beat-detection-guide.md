# QCut 实现 Beat Detection（自动节拍标记）：复用 OpenReel Video 代码的完整实施指南

> **TL;DR:** 从 OpenReel Video（MIT 协议）直接移植 beat detection 引擎到 QCut，实现音频节拍自动检测 → 时间线标记 → "卡点剪辑" 工作流。预估工作量 1-2 天。

---

## 1. Beat Detection 是什么？QCut 为什么需要它？

### 核心概念

Beat Detection（节拍检测）= 分析音频波形 → 找到能量峰值（节拍点）→ 输出时间戳数组。

```
音频波形 ──→ RMS 能量计算 ──→ 自适应阈值 ──→ 节拍时间戳数组
              ↓                    ↓                ↓
          [0.12, 0.08, 0.15, ...]  threshold[]    [0.5s, 1.0s, 1.5s, ...]
```

### 为什么 QCut 需要这个功能？

| 使用场景 | 具体需求 |
|---------|---------|
| **卡点剪辑（"卡点"）** | 音乐视频自动在节拍处切换画面 |
| **短视频制作** | 抖音/快手风格的节奏感视频 |
| **Montage 蒙太奇** | 运动/旅行/婚礼集锦按节拍切换 |
| **自动转场** | 在节拍点自动插入转场效果 |
| **CLI Pipeline 集成** | `qcut-pipeline autoclip` 命令使用节拍作为切割点 |

这是剪映（CapCut）的核心功能之一，OpenReel Video 已经实现了完整版本，QCut 可以直接复用。

---

## 2. OpenReel Video 的 Beat Detection 实现

OpenReel Video 是一个 130K+ 行代码的开源浏览器端视频编辑器（MIT 协议），其 beat detection 实现非常完整。

### 2.1 核心文件清单

| 文件路径（OpenReel 仓库） | 功能 | 行数 | 可复用性 |
|--------------------------|------|------|---------|
| `packages/core/src/audio/beat-detection-engine.ts` | 核心算法引擎 | ~280 行 | ⭐⭐⭐ 直接复用 |
| `packages/core/src/wasm/beat-detection/index.ts` | WASM 加速层 + JS fallback | ~200 行 | ⭐⭐ 需适配 |
| `apps/web/src/bridges/beat-sync-bridge.ts` | 桥接层：引擎 ↔ UI 状态 | ~250 行 | ⭐⭐ 参考结构 |
| `apps/web/src/components/editor/inspector/BeatSyncSection.tsx` | React UI 面板 | ~200 行 | ⭐ 参考 UI |

### 2.2 算法流程

`BeatDetectionEngine` 是核心类，算法流程如下：

```
analyzeAudioBuffer(audioBuffer)
    ├── 1. detectOnsets(channelData, sampleRate)
    │       ├── RMS 能量计算（windowSize=2048, hopSize=512）
    │       ├── 滑动窗口平滑（窗口大小 5）
    │       ├── 自适应阈值计算（median + mean 混合）
    │       └── 峰值检测（局部最大值 + 阈值 + 上升幅度 + 最小间距）
    ├── 2. calculateBpm(onsets, duration)
    │       ├── 计算相邻 onset 间隔
    │       ├── BPM 候选打分（含 2x 和 0.5x harmonic）
    │       └── 置信度 = actual beats vs expected beats
    ├── 3. generateBeats(bpm, duration, onsets)
    │       ├── 用 BPM 生成等间距网格
    │       └── 每个网格点 snap 到最近的 onset
    └── 4. detectDownbeats(beats)
            └── 每 4 拍标记一个 downbeat（强拍）
```

### 2.3 关键数据结构

```typescript
// 来自 OpenReel: packages/core/src/audio/beat-detection-engine.ts

interface Beat {
  readonly time: number;      // 节拍时间戳（秒）
  readonly strength: number;  // 节拍强度 0-1
  readonly index: number;     // 节拍序号
}

interface BeatAnalysisResult {
  readonly bpm: number;          // 检测到的 BPM
  readonly confidence: number;   // 置信度 0-1
  readonly beats: Beat[];        // 所有节拍
  readonly duration: number;     // 音频总时长
  readonly downbeats: number[];  // 强拍时间戳
}

interface BeatDetectionConfig {
  readonly minBpm: number;      // 默认 60
  readonly maxBpm: number;      // 默认 200
  readonly sensitivity: number; // 默认 0.5（0=严格，1=宽松）
  readonly windowSize: number;  // 默认 2048
  readonly hopSize: number;     // 默认 512
}
```

### 2.4 WASM 加速 + JS Fallback

OpenReel 的 `BeatDetectionProcessor` 类实现了双轨模式：

```typescript
// packages/core/src/wasm/beat-detection/index.ts

class BeatDetectionProcessor {
  computeRMSEnergies(samples, windowSize, hopSize, energies) {
    if (this.useWasm && wasmModule) {
      wasmModule.computeRMSEnergies(samples, windowSize, hopSize, energies);
    } else {
      jsComputeRMSEnergies(samples, windowSize, hopSize, energies);  // 纯 JS fallback
    }
  }
  // smoothArray, calculateMedian, findPeaks, calculateMean 同理
}
```

**QCut 策略：先只用 JS fallback 版本**，WASM 作为后续优化。JS 版本对 3-5 分钟的音频完全够用。

### 2.5 桥接层模式

OpenReel 的 `BeatSyncBridge` 提供了状态管理和实用方法：

```typescript
// apps/web/src/bridges/beat-sync-bridge.ts

interface BeatSyncState {
  isAnalyzing: boolean;         // 正在分析中
  progress: number;             // 进度 0-100
  error: string | null;         // 错误信息
  beatMarkers: TimelineBeatMarker[];  // 节拍标记
  beatAnalysis: TimelineBeatAnalysis; // 分析结果
}

// 实用方法
bridge.analyzeAudioFromBlob(blob, clipId)   // 从 Blob 分析
bridge.snapTimeToNearestBeat(time)          // 时间吸附到最近节拍
bridge.getBeatsInRange(start, end)          // 获取范围内节拍
bridge.generateCutPointsForClips(clips, 4)  // 每 4 拍生成切割点
bridge.generateManualBeatMarkers(bpm, dur)  // 手动 BPM 模式
```

---

## 3. QCut 现有可复用的基础设施

### 3.1 相关文件清单

| QCut 文件路径 | 功能 | 与 Beat Detection 的关系 |
|--------------|------|-------------------------|
| `apps/web/src/components/editor/audio-waveform.tsx` | WaveSurfer.js 波形可视化 | 音频输入源，可扩展显示节拍标记 |
| `apps/web/src/stores/timeline/timeline-store.ts` | 时间线核心 store | 需要添加 beat marker 状态 |
| `apps/web/src/stores/timeline/types.ts` | 时间线类型定义 | 需要扩展 marker 类型 |
| `apps/web/src/stores/timeline/timeline-store-operations.ts` | 时间线操作（split、ripple 等） | 添加 beat-based split |
| `packages/editor-core/src/types/timeline.ts` | 核心类型定义 | 添加 BeatMarker 类型 |
| `apps/web/src/components/editor/properties-panel/audio-properties.tsx` | 音频属性面板 | 添加 "Detect Beats" 按钮 |
| `apps/web/src/lib/export-cli/sources/audio-detection.ts` | 音频源检测 | 复用音频检测逻辑 |
| `apps/web/src/lib/ffmpeg/audio-mixer.ts` | FFmpeg 音频混合 | 可提取音频给 beat detection |
| `electron/elevenlabs-transcribe-handler.ts` | ElevenLabs 转录 | 参考音频处理流程 |
| `electron/gemini-transcribe-handler.ts` | Gemini 转录 | 参考音频处理流程 |
| `apps/web/src/hooks/use-ai-pipeline.ts` | AI Pipeline hook | 参考异步任务模式 |

### 3.2 QCut 时间线类型结构

QCut 的时间线目前没有 "marker" 概念，元素类型包括：
```
media | text | sticker | captions | remotion | markdown
```

Beat marker 需要作为**独立的叠加层**（overlay），不是时间线元素。这与 OpenReel 的设计一致。

---

## 4. 需要创建的新文件

### 4.1 文件清单

| 新文件路径 | 功能 | 基于 OpenReel |
|-----------|------|-------------|
| `packages/editor-core/src/audio/beat-detection-engine.ts` | 核心算法（纯 JS） | 直接复制并简化 |
| `packages/editor-core/src/audio/beat-detection-types.ts` | 类型定义 | 提取自 OpenReel |
| `packages/editor-core/src/audio/index.ts` | Audio 模块入口 | 新建 |
| `apps/web/src/stores/beat-detection/beat-detection-store.ts` | Zustand store | 基于 BeatSyncBridge |
| `apps/web/src/stores/beat-detection/index.ts` | Store 入口 | 新建 |
| `apps/web/src/components/editor/beat-detection-panel.tsx` | UI 面板 | 基于 BeatSyncSection |
| `apps/web/src/components/editor/timeline/beat-markers-overlay.tsx` | 时间线节拍标记渲染 | 新建 |
| `apps/web/src/hooks/use-beat-detection.ts` | React hook | 新建 |

### 4.2 核心算法模块

**文件：`packages/editor-core/src/audio/beat-detection-types.ts`**

```typescript
/**
 * Beat Detection Types
 * Adapted from OpenReel Video (MIT License)
 * https://github.com/Augani/openreel-video
 */

export interface Beat {
  readonly time: number;
  readonly strength: number;
  readonly index: number;
}

export interface BeatAnalysisResult {
  readonly bpm: number;
  readonly confidence: number;
  readonly beats: Beat[];
  readonly duration: number;
  readonly downbeats: number[];
}

export interface BeatDetectionConfig {
  readonly minBpm: number;
  readonly maxBpm: number;
  readonly sensitivity: number;
  readonly windowSize: number;
  readonly hopSize: number;
}

export const DEFAULT_BEAT_DETECTION_CONFIG: BeatDetectionConfig = {
  minBpm: 60,
  maxBpm: 200,
  sensitivity: 0.5,
  windowSize: 2048,
  hopSize: 512,
};

export interface TimelineBeatMarker {
  time: number;
  strength: number;
  index: number;
  isDownbeat: boolean;
}

export interface TimelineBeatAnalysis {
  bpm: number;
  confidence: number;
  sourceClipId?: string;
  analyzedAt: number;
}
```

**文件：`packages/editor-core/src/audio/beat-detection-engine.ts`**

```typescript
/**
 * Beat Detection Engine
 * Adapted from OpenReel Video (MIT License)
 * https://github.com/Augani/openreel-video
 * 
 * Pure JS implementation - no WASM dependency.
 * Suitable for Electron (main + renderer) and Node.js CLI.
 */

import {
  type Beat,
  type BeatAnalysisResult,
  type BeatDetectionConfig,
  DEFAULT_BEAT_DETECTION_CONFIG,
} from './beat-detection-types';

export class BeatDetectionEngine {
  private config: BeatDetectionConfig;

  constructor(config: Partial<BeatDetectionConfig> = {}) {
    this.config = { ...DEFAULT_BEAT_DETECTION_CONFIG, ...config };
  }

  /**
   * Analyze audio from raw PCM samples.
   * Works in both browser (AudioBuffer.getChannelData) and Node.js (ffmpeg extracted PCM).
   */
  analyzeFromSamples(
    samples: Float32Array,
    sampleRate: number,
    duration: number
  ): BeatAnalysisResult {
    const onsets = this.detectOnsets(samples, sampleRate);
    const { bpm, confidence } = this.calculateBpm(onsets, duration);
    const beats = this.generateBeats(bpm, duration, onsets);
    const downbeats = this.detectDownbeats(beats);

    return { bpm, confidence, beats, duration, downbeats };
  }

  /**
   * Browser-only: analyze from AudioBuffer.
   */
  async analyzeAudioBuffer(audioBuffer: AudioBuffer): Promise<BeatAnalysisResult> {
    const channelData = audioBuffer.getChannelData(0);
    return this.analyzeFromSamples(
      channelData,
      audioBuffer.sampleRate,
      audioBuffer.duration
    );
  }

  // --- 以下方法直接复制自 OpenReel，移除 WASM 调用 ---

  private detectOnsets(samples: Float32Array, sampleRate: number): number[] {
    const { windowSize, hopSize, sensitivity } = this.config;
    const numFrames = Math.floor((samples.length - windowSize) / hopSize);
    
    // Step 1: 计算 RMS 能量
    const energies = new Float32Array(numFrames);
    for (let frame = 0; frame < numFrames; frame++) {
      const start = frame * hopSize;
      let sum = 0.0;
      for (let i = 0; i < windowSize && start + i < samples.length; i++) {
        const s = samples[start + i];
        sum += s * s;
      }
      energies[frame] = Math.sqrt(sum / windowSize);
    }

    // Step 2: 平滑
    const smoothed = new Float32Array(numFrames);
    const halfWin = 2;
    for (let i = 0; i < numFrames; i++) {
      let sum = 0;
      let count = 0;
      for (let j = i - halfWin; j <= i + halfWin; j++) {
        if (j >= 0 && j < numFrames) { sum += energies[j]; count++; }
      }
      smoothed[i] = sum / count;
    }

    // Step 3: 自适应阈值
    const threshold = this.calculateAdaptiveThreshold(
      Array.from(smoothed), sensitivity
    );

    // Step 4: 峰值检测
    const onsets: number[] = [];
    let lastOnsetFrame = -10;
    const minFramesBetween = Math.floor((sampleRate / hopSize) * 0.1);

    for (let i = 1; i < smoothed.length - 1; i++) {
      const current = smoothed[i];
      const prev = smoothed[i - 1];
      const isLocalMax = current > smoothed[i - 1] && current >= smoothed[i + 1];
      const isAboveThreshold = current > threshold[i];
      const hasRise = current - prev > threshold[i] * 0.3;
      const notTooClose = i - lastOnsetFrame >= minFramesBetween;

      if (isLocalMax && isAboveThreshold && hasRise && notTooClose) {
        onsets.push((i * hopSize) / sampleRate);
        lastOnsetFrame = i;
      }
    }

    return onsets;
  }

  private calculateAdaptiveThreshold(
    energies: number[],
    sensitivity: number
  ): number[] {
    const windowSize = 50;
    return energies.map((_, i) => {
      const start = Math.max(0, i - windowSize);
      const end = Math.min(energies.length, i + windowSize);
      const window = energies.slice(start, end);
      
      const sorted = [...window].sort((a, b) => a - b);
      const median = sorted[Math.floor(sorted.length / 2)];
      const mean = window.reduce((a, b) => a + b, 0) / window.length;
      
      const base = median + (mean - median) * (1 - sensitivity);
      return base * (1.5 - sensitivity * 0.5);
    });
  }

  private calculateBpm(
    onsets: number[],
    duration: number
  ): { bpm: number; confidence: number } {
    if (onsets.length < 4) return { bpm: 120, confidence: 0 };

    const { minBpm, maxBpm } = this.config;
    const intervals = [];
    for (let i = 1; i < onsets.length; i++) {
      intervals.push(onsets[i] - onsets[i - 1]);
    }

    const candidates = new Map<number, number>();
    for (const interval of intervals) {
      const bpm = Math.round(60 / interval);
      if (bpm >= minBpm && bpm <= maxBpm) {
        candidates.set(bpm, (candidates.get(bpm) || 0) + 1);
      }
      // Harmonic consideration
      const double = Math.round(120 / interval);
      if (double >= minBpm && double <= maxBpm) {
        candidates.set(double, (candidates.get(double) || 0) + 0.5);
      }
    }

    let bestBpm = 120, bestScore = 0;
    for (const [bpm, score] of candidates) {
      if (score > bestScore) { bestScore = score; bestBpm = bpm; }
    }

    const expected = (duration * bestBpm) / 60;
    const confidence = Math.min(1, Math.max(0, 1 - Math.abs(expected - onsets.length) / expected));
    return { bpm: bestBpm, confidence };
  }

  private generateBeats(bpm: number, duration: number, onsets: number[]): Beat[] {
    const interval = 60 / bpm;
    const beats: Beat[] = [];
    
    let firstBeatTime = 0;
    if (onsets.length > 0) {
      const offset = Math.round(onsets[0] / interval);
      firstBeatTime = onsets[0] - offset * interval;
      while (firstBeatTime < 0) firstBeatTime += interval;
    }

    let idx = 0;
    for (let time = firstBeatTime; time < duration; time += interval) {
      const nearest = this.findNearestOnset(time, onsets, interval * 0.3);
      beats.push({
        time: nearest !== null ? nearest : time,
        strength: nearest !== null ? 1 : 0.5,
        index: idx++,
      });
    }
    return beats;
  }

  private findNearestOnset(time: number, onsets: number[], tolerance: number): number | null {
    let nearest: number | null = null;
    let minDist = tolerance;
    for (const onset of onsets) {
      const dist = Math.abs(onset - time);
      if (dist < minDist) { minDist = dist; nearest = onset; }
    }
    return nearest;
  }

  private detectDownbeats(beats: Beat[]): number[] {
    const strong = beats.filter(b => b.strength > 0.7);
    if (strong.length > 0) {
      const firstIdx = beats.findIndex(b => b.time === strong[0].time);
      const result: number[] = [];
      for (let i = firstIdx; i < beats.length; i += 4) {
        result.push(beats[i].time);
      }
      return result;
    }
    return beats.filter((_, i) => i % 4 === 0).map(b => b.time);
  }

  snapToNearestBeat(time: number, beats: Beat[], threshold = 0.1): number {
    if (beats.length === 0) return time;
    let nearest = beats[0];
    let minDist = Math.abs(beats[0].time - time);
    for (const beat of beats) {
      const dist = Math.abs(beat.time - time);
      if (dist < minDist) { minDist = dist; nearest = beat; }
    }
    return minDist <= threshold ? nearest.time : time;
  }
}
```

### 4.3 Zustand Store

**文件：`apps/web/src/stores/beat-detection/beat-detection-store.ts`**

```typescript
/**
 * Beat Detection Store
 * Manages beat analysis state for the timeline.
 */
import { create } from 'zustand';
import { BeatDetectionEngine } from '@qcut/editor-core/audio/beat-detection-engine';
import type {
  TimelineBeatMarker,
  TimelineBeatAnalysis,
  BeatDetectionConfig,
} from '@qcut/editor-core/audio/beat-detection-types';

interface BeatDetectionState {
  // State
  isAnalyzing: boolean;
  progress: number;
  error: string | null;
  beatMarkers: TimelineBeatMarker[];
  beatAnalysis: TimelineBeatAnalysis | null;
  config: Partial<BeatDetectionConfig>;

  // Actions
  analyzeAudioBuffer: (buffer: AudioBuffer, clipId?: string) => Promise<void>;
  generateManualBeats: (bpm: number, duration: number, offset?: number) => void;
  clearBeats: () => void;
  setConfig: (config: Partial<BeatDetectionConfig>) => void;
  getCutPoints: (beatsPerCut?: number) => number[];
  snapToNearestBeat: (time: number, threshold?: number) => number;
}

const engine = new BeatDetectionEngine();

export const useBeatDetectionStore = create<BeatDetectionState>((set, get) => ({
  isAnalyzing: false,
  progress: 0,
  error: null,
  beatMarkers: [],
  beatAnalysis: null,
  config: {},

  analyzeAudioBuffer: async (buffer, clipId) => {
    set({ isAnalyzing: true, progress: 10, error: null });
    try {
      const result = await engine.analyzeAudioBuffer(buffer);
      const downbeatSet = new Set(result.downbeats);
      const markers: TimelineBeatMarker[] = result.beats.map(beat => ({
        time: beat.time,
        strength: beat.strength,
        index: beat.index,
        isDownbeat: downbeatSet.has(beat.time) || beat.index % 4 === 0,
      }));

      set({
        isAnalyzing: false,
        progress: 100,
        beatMarkers: markers,
        beatAnalysis: {
          bpm: result.bpm,
          confidence: result.confidence,
          sourceClipId: clipId,
          analyzedAt: Date.now(),
        },
      });
    } catch (err) {
      set({
        isAnalyzing: false,
        progress: 0,
        error: err instanceof Error ? err.message : 'Beat detection failed',
      });
    }
  },

  generateManualBeats: (bpm, duration, offset = 0) => {
    const interval = 60 / bpm;
    const markers: TimelineBeatMarker[] = [];
    let idx = 0;
    for (let time = offset; time < duration; time += interval) {
      markers.push({
        time,
        strength: idx % 4 === 0 ? 1 : 0.7,
        index: idx,
        isDownbeat: idx % 4 === 0,
      });
      idx++;
    }
    set({
      beatMarkers: markers,
      beatAnalysis: { bpm, confidence: 1, analyzedAt: Date.now() },
    });
  },

  clearBeats: () => set({ beatMarkers: [], beatAnalysis: null, error: null }),

  setConfig: (config) => set({ config }),

  getCutPoints: (beatsPerCut = 4) => {
    const { beatMarkers } = get();
    const downbeats = beatMarkers.filter(m => m.isDownbeat);
    return downbeats
      .filter((_, i) => i > 0 && i % beatsPerCut === 0)
      .map(m => m.time);
  },

  snapToNearestBeat: (time, threshold = 0.1) => {
    const { beatMarkers } = get();
    if (beatMarkers.length === 0) return time;
    let nearest = beatMarkers[0];
    let minDist = Math.abs(nearest.time - time);
    for (const m of beatMarkers) {
      const d = Math.abs(m.time - time);
      if (d < minDist) { minDist = d; nearest = m; }
    }
    return minDist <= threshold ? nearest.time : time;
  },
}));
```

### 4.4 时间线标记渲染

**文件：`apps/web/src/components/editor/timeline/beat-markers-overlay.tsx`**

```tsx
/**
 * Beat Markers Overlay
 * Renders beat detection markers on the timeline ruler area.
 */
import React from 'react';
import { useBeatDetectionStore } from '@/stores/beat-detection';

interface BeatMarkersOverlayProps {
  zoomLevel: number;
  scrollLeft: number;
  visibleWidth: number;
}

export const BeatMarkersOverlay: React.FC<BeatMarkersOverlayProps> = ({
  zoomLevel,
  scrollLeft,
  visibleWidth,
}) => {
  const { beatMarkers } = useBeatDetectionStore();

  if (beatMarkers.length === 0) return null;

  // 只渲染可见范围内的标记
  const startTime = scrollLeft / zoomLevel;
  const endTime = (scrollLeft + visibleWidth) / zoomLevel;

  const visibleMarkers = beatMarkers.filter(
    m => m.time >= startTime - 1 && m.time <= endTime + 1
  );

  return (
    <div className="absolute inset-0 pointer-events-none z-10">
      {visibleMarkers.map((marker) => {
        const x = marker.time * zoomLevel - scrollLeft;
        return (
          <div
            key={marker.index}
            className="absolute top-0 bottom-0"
            style={{ left: `${x}px` }}
          >
            <div
              className={`w-px h-full ${
                marker.isDownbeat
                  ? 'bg-orange-400/60'   // 强拍：橙色
                  : 'bg-blue-400/30'     // 弱拍：蓝色淡
              }`}
            />
            {marker.isDownbeat && (
              <div className="absolute -top-1 -translate-x-1/2">
                <div className="w-2 h-2 rounded-full bg-orange-400" />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};
```

### 4.5 Beat Detection UI 面板

**文件：`apps/web/src/components/editor/beat-detection-panel.tsx`**

```tsx
/**
 * Beat Detection Panel
 * UI for triggering beat analysis and viewing results.
 * Adapted from OpenReel Video's BeatSyncSection (MIT License).
 */
import React, { useState, useCallback } from 'react';
import { Music, Zap, Loader2, Scissors, RefreshCw } from 'lucide-react';
import { useBeatDetectionStore } from '@/stores/beat-detection';
import { useTimelineStore } from '@/stores/timeline';

interface BeatDetectionPanelProps {
  audioBuffer: AudioBuffer | null;
  clipId?: string;
}

export const BeatDetectionPanel: React.FC<BeatDetectionPanelProps> = ({
  audioBuffer,
  clipId,
}) => {
  const {
    isAnalyzing, progress, error, beatAnalysis, beatMarkers,
    analyzeAudioBuffer, generateManualBeats, clearBeats,
  } = useBeatDetectionStore();
  
  const [manualBpm, setManualBpm] = useState(120);
  const [showManual, setShowManual] = useState(false);

  const handleAnalyze = useCallback(async () => {
    if (!audioBuffer) return;
    await analyzeAudioBuffer(audioBuffer, clipId);
  }, [audioBuffer, clipId, analyzeAudioBuffer]);

  return (
    <div className="space-y-3 p-3">
      <div className="flex items-center gap-2">
        <Music size={14} className="text-primary" />
        <span className="text-xs font-medium">Beat Detection</span>
      </div>

      {/* 分析按钮 */}
      {isAnalyzing ? (
        <div className="p-3 bg-background-tertiary rounded-lg">
          <div className="flex items-center gap-2 mb-2">
            <Loader2 size={14} className="animate-spin text-primary" />
            <span className="text-[10px]">Analyzing beats... {progress}%</span>
          </div>
          <div className="h-1.5 bg-background-secondary rounded-full overflow-hidden">
            <div
              className="h-full bg-primary transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      ) : (
        <button
          onClick={handleAnalyze}
          disabled={!audioBuffer}
          className="w-full py-2.5 bg-primary/10 hover:bg-primary/20 border border-primary/30 rounded-lg text-[11px] font-medium text-primary flex items-center justify-center gap-2 disabled:opacity-50"
        >
          <Zap size={14} />
          Detect Beats from Audio
        </button>
      )}

      {/* 错误提示 */}
      {error && (
        <p className="text-[10px] text-red-400 bg-red-400/10 p-2 rounded">{error}</p>
      )}

      {/* 分析结果 */}
      {beatAnalysis && (
        <div className="p-3 bg-green-500/10 border border-green-500/30 rounded-lg space-y-1">
          <div className="flex justify-between">
            <span className="text-[10px] text-text-secondary">BPM</span>
            <span className="text-sm font-bold text-green-400">{beatAnalysis.bpm}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-[10px] text-text-secondary">Confidence</span>
            <span className="text-[10px]">{Math.round(beatAnalysis.confidence * 100)}%</span>
          </div>
          <div className="flex justify-between">
            <span className="text-[10px] text-text-secondary">Markers</span>
            <span className="text-[10px]">{beatMarkers.length}</span>
          </div>
        </div>
      )}

      {/* 操作按钮 */}
      {beatMarkers.length > 0 && (
        <div className="space-y-2">
          <button
            onClick={() => {/* TODO: 调用 timeline split */}}
            className="w-full py-2 bg-background-tertiary hover:bg-background-secondary rounded-lg text-[10px] flex items-center justify-center gap-2"
          >
            <Scissors size={12} /> Auto-Cut on Every 4 Beats
          </button>
          <button
            onClick={clearBeats}
            className="w-full py-2 bg-background-tertiary hover:bg-red-500/10 rounded-lg text-[10px] text-text-secondary hover:text-red-400 flex items-center justify-center gap-2"
          >
            <RefreshCw size={12} /> Clear Beat Markers
          </button>
        </div>
      )}

      {/* 手动 BPM */}
      <button
        onClick={() => setShowManual(!showManual)}
        className="w-full py-1.5 text-[10px] text-text-muted hover:text-text-secondary"
      >
        {showManual ? 'Hide' : 'Show'} Manual BPM Settings
      </button>
      {showManual && (
        <div className="p-3 bg-background-tertiary rounded-lg flex items-center gap-2">
          <input
            type="number" value={manualBpm}
            onChange={e => setManualBpm(parseInt(e.target.value) || 120)}
            min={60} max={200}
            className="w-16 px-2 py-1 bg-background-secondary rounded text-[10px]"
          />
          <span className="text-[10px]">BPM</span>
          <button
            onClick={() => generateManualBeats(manualBpm, 300)} // TODO: 用实际时长
            className="px-3 py-1 bg-primary/20 rounded text-[10px] text-primary"
          >
            Generate
          </button>
        </div>
      )}
    </div>
  );
};
```

---

## 5. 需要修改的现有文件

### 5.1 修改清单

| 现有文件 | 修改内容 | 复杂度 |
|---------|---------|--------|
| `packages/editor-core/src/index.ts` | 导出 audio 模块 | 低 |
| `apps/web/src/stores/timeline/types.ts` | 添加 beat marker 相关类型到 store | 低 |
| `apps/web/src/components/editor/audio-waveform.tsx` | 集成 beat markers 显示 | 中 |
| `apps/web/src/components/editor/properties-panel/audio-properties.tsx` | 添加 BeatDetectionPanel | 中 |
| `apps/web/src/stores/timeline/timeline-store-operations.ts` | 添加 splitOnBeats 操作 | 中 |

### 5.2 editor-core 入口导出

**修改：`packages/editor-core/src/index.ts`**

```typescript
// 添加以下导出
export { BeatDetectionEngine } from './audio/beat-detection-engine';
export type {
  Beat,
  BeatAnalysisResult,
  BeatDetectionConfig,
  TimelineBeatMarker,
  TimelineBeatAnalysis,
} from './audio/beat-detection-types';
export { DEFAULT_BEAT_DETECTION_CONFIG } from './audio/beat-detection-types';
```

### 5.3 时间线 Store 扩展

**修改：`apps/web/src/stores/timeline/timeline-store-operations.ts`**

添加基于节拍的分割功能：

```typescript
import { useBeatDetectionStore } from '@/stores/beat-detection';

// 在 createTimelineOperations 中添加：
splitOnBeats: (trackId: string, elementId: string, beatsPerCut: number = 4) => {
  const beatStore = useBeatDetectionStore.getState();
  const cutPoints = beatStore.getCutPoints(beatsPerCut);
  const { _tracks } = get();
  
  const track = _tracks.find(t => t.id === trackId);
  const element = track?.elements.find(e => e.id === elementId);
  if (!track || !element) return;

  // 过滤出元素范围内的切割点
  const validCuts = cutPoints.filter(
    t => t > element.startTime && t < element.startTime + element.duration
  );

  // 从后往前切割（避免时间偏移）
  for (const cutTime of validCuts.reverse()) {
    // 调用现有的 split 逻辑
    get().splitElement(trackId, elementId, cutTime);
  }
},
```

---

## 6. 分步实施计划

### Phase 1: 核心算法（2-3 小时）

```
Step 1.1: 创建 packages/editor-core/src/audio/ 目录
Step 1.2: 复制 beat-detection-types.ts
Step 1.3: 复制 beat-detection-engine.ts（移除 WASM 依赖，纯 JS）
Step 1.4: 创建 index.ts 入口
Step 1.5: 更新 editor-core/src/index.ts 导出
Step 1.6: 写单元测试验证算法
```

### Phase 2: Store + Hook（1-2 小时）

```
Step 2.1: 创建 stores/beat-detection/beat-detection-store.ts
Step 2.2: 创建 hooks/use-beat-detection.ts
Step 2.3: 验证 store 状态流转
```

### Phase 3: UI 集成（2-3 小时）

```
Step 3.1: 创建 BeatDetectionPanel 组件
Step 3.2: 集成到 audio-properties.tsx
Step 3.3: 创建 BeatMarkersOverlay
Step 3.4: 集成到时间线渲染
```

### Phase 4: 操作集成（1-2 小时）

```
Step 4.1: 添加 splitOnBeats 到 timeline-store-operations
Step 4.2: 添加 snapToNearestBeat 到拖拽逻辑
Step 4.3: 连接 "Auto-Cut" 按钮到实际操作
```

### Phase 5: CLI 集成（可选，1 小时）

```
Step 5.1: 在 CLI pipeline 中添加 --beat-sync 选项
Step 5.2: 使用 ffmpeg 提取音频 PCM 数据
Step 5.3: 调用 BeatDetectionEngine.analyzeFromSamples()
```

---

## 7. CLI Pipeline 集成方案

QCut 的 `qcut-pipeline autoclip` 命令可以使用 beat detection 来优化剪辑点：

```typescript
// CLI 端使用示例（Node.js，不需要浏览器 AudioContext）
import { execSync } from 'child_process';
import { BeatDetectionEngine } from '@qcut/editor-core';

function extractPCMFromAudio(audioPath: string): { samples: Float32Array; sampleRate: number } {
  // 使用 ffmpeg 提取原始 PCM 数据
  const buffer = execSync(
    `ffmpeg -i "${audioPath}" -f f32le -acodec pcm_f32le -ac 1 -ar 44100 -`
  );
  return {
    samples: new Float32Array(buffer.buffer),
    sampleRate: 44100,
  };
}

async function autoclipWithBeats(audioPath: string, duration: number) {
  const engine = new BeatDetectionEngine({ sensitivity: 0.6 });
  const { samples, sampleRate } = extractPCMFromAudio(audioPath);
  
  const result = engine.analyzeFromSamples(samples, sampleRate, duration);
  
  console.log(`Detected BPM: ${result.bpm} (confidence: ${Math.round(result.confidence * 100)}%)`);
  console.log(`Found ${result.beats.length} beats, ${result.downbeats.length} downbeats`);
  
  // 每 4 个强拍作为一个切割点
  const cutPoints = result.downbeats.filter((_, i) => i > 0 && i % 4 === 0);
  return cutPoints;
}
```

---

## 8. 文件变更总览

### 新建文件（8 个）

| # | 文件路径 | 用途 |
|---|---------|------|
| 1 | `packages/editor-core/src/audio/beat-detection-types.ts` | 类型定义 |
| 2 | `packages/editor-core/src/audio/beat-detection-engine.ts` | 核心算法 |
| 3 | `packages/editor-core/src/audio/index.ts` | 模块入口 |
| 4 | `apps/web/src/stores/beat-detection/beat-detection-store.ts` | Zustand store |
| 5 | `apps/web/src/stores/beat-detection/index.ts` | Store 入口 |
| 6 | `apps/web/src/components/editor/beat-detection-panel.tsx` | UI 面板 |
| 7 | `apps/web/src/components/editor/timeline/beat-markers-overlay.tsx` | 标记渲染 |
| 8 | `apps/web/src/hooks/use-beat-detection.ts` | React hook |

### 修改文件（5 个）

| # | 文件路径 | 修改内容 |
|---|---------|---------|
| 1 | `packages/editor-core/src/index.ts` | 导出 audio 模块 |
| 2 | `apps/web/src/stores/timeline/types.ts` | 扩展 store 接口 |
| 3 | `apps/web/src/components/editor/properties-panel/audio-properties.tsx` | 集成面板 |
| 4 | `apps/web/src/stores/timeline/timeline-store-operations.ts` | splitOnBeats |
| 5 | `apps/web/src/components/editor/audio-waveform.tsx` | 可选：显示 beat 标记 |

### 估时

| 阶段 | 时间 |
|------|------|
| Phase 1: 核心算法 | 2-3 小时 |
| Phase 2: Store + Hook | 1-2 小时 |
| Phase 3: UI 集成 | 2-3 小时 |
| Phase 4: 操作集成 | 1-2 小时 |
| Phase 5: CLI（可选） | 1 小时 |
| **总计** | **~1-2 天** |

---

## 9. OpenReel 代码的许可证

OpenReel Video 采用 **MIT 协议**，允许自由使用、修改和分发。在复用代码时，建议：

1. 在文件头部注释标注来源：
   ```typescript
   // Adapted from OpenReel Video (MIT License)
   // https://github.com/Augani/openreel-video
   ```
2. 在项目 LICENSE 或 NOTICE 文件中声明
3. 保留原始版权声明

---

## 总结

Beat Detection 是 QCut 走向"卡点剪辑"的关键功能。OpenReel Video 提供了一个生产级的实现，核心算法（~280 行 TypeScript）可以直接复用。QCut 已有的音频处理、时间线 store、WaveSurfer 波形组件等基础设施大幅降低了集成成本。

**最小可行路径：** 复制 `BeatDetectionEngine` → 创建 Zustand store → 在音频属性面板添加 "Detect Beats" 按钮 → 在时间线渲染 beat markers。一天内可完成基础版本。

🦞
