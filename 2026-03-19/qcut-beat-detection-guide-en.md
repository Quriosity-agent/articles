# Adding Beat Detection (Auto Beat Markers) to QCut: Reusing OpenReel Video Code

> **TL;DR:** Port the beat detection engine from OpenReel Video (MIT license) directly into QCut. Analyze audio waveforms → detect beat timestamps → render timeline markers → enable "cut on beat" workflows. Estimated effort: 1-2 days.

---

## 1. What Is Beat Detection and Why Does QCut Need It?

### Core Concept

Beat Detection = analyze audio waveform → find energy spikes (beats) → output timestamp array.

```
Audio Waveform ──→ RMS Energy Calc ──→ Adaptive Threshold ──→ Beat Timestamp Array
                    ↓                       ↓                     ↓
               [0.12, 0.08, 0.15, ...]  threshold[]         [0.5s, 1.0s, 1.5s, ...]
```

### Why QCut Needs This

| Use Case | Description |
|----------|-------------|
| **Beat-synced editing ("卡点")** | Auto-switch visuals on every music beat |
| **Short-form content** | TikTok/Reels-style rhythmic videos |
| **Montage editing** | Sports/travel/wedding compilations cut to beats |
| **Auto transitions** | Insert transition effects at beat points |
| **CLI Pipeline integration** | `qcut-pipeline autoclip` using beats as cut boundaries |

This is a core feature of CapCut/剪映. OpenReel Video has a complete implementation we can reuse.

---

## 2. OpenReel Video's Beat Detection Implementation

OpenReel Video is a 130K+ line open-source browser-based video editor (MIT license) with production-grade beat detection.

### 2.1 Key Source Files

| File Path (OpenReel repo) | Purpose | Lines | Reusability |
|--------------------------|---------|-------|-------------|
| `packages/core/src/audio/beat-detection-engine.ts` | Core algorithm engine | ~280 | ⭐⭐⭐ Direct copy |
| `packages/core/src/wasm/beat-detection/index.ts` | WASM acceleration + JS fallback | ~200 | ⭐⭐ Adapt |
| `apps/web/src/bridges/beat-sync-bridge.ts` | Bridge: engine ↔ UI state | ~250 | ⭐⭐ Reference |
| `apps/web/src/components/editor/inspector/BeatSyncSection.tsx` | React UI panel | ~200 | ⭐ Reference |

### 2.2 Algorithm Pipeline

The `BeatDetectionEngine` class implements this pipeline:

```
analyzeAudioBuffer(audioBuffer)
    ├── 1. detectOnsets(channelData, sampleRate)
    │       ├── RMS energy calculation (windowSize=2048, hopSize=512)
    │       ├── Sliding window smoothing (window=5)
    │       ├── Adaptive threshold (median + mean blend)
    │       └── Peak detection (local max + threshold + rise + min spacing)
    ├── 2. calculateBpm(onsets, duration)
    │       ├── Compute inter-onset intervals
    │       ├── BPM candidate scoring (with 2x and 0.5x harmonics)
    │       └── Confidence = actual beats vs expected beats
    ├── 3. generateBeats(bpm, duration, onsets)
    │       ├── Generate evenly-spaced BPM grid
    │       └── Snap each grid point to nearest onset
    └── 4. detectDownbeats(beats)
            └── Mark every 4th beat as downbeat (strong beat)
```

### 2.3 Key Data Structures

```typescript
// From OpenReel: packages/core/src/audio/beat-detection-engine.ts

interface Beat {
  readonly time: number;      // Beat timestamp in seconds
  readonly strength: number;  // Beat strength 0-1
  readonly index: number;     // Beat sequence number
}

interface BeatAnalysisResult {
  readonly bpm: number;          // Detected BPM
  readonly confidence: number;   // Confidence 0-1
  readonly beats: Beat[];        // All detected beats
  readonly duration: number;     // Audio total duration
  readonly downbeats: number[];  // Downbeat timestamps
}

interface BeatDetectionConfig {
  readonly minBpm: number;      // Default 60
  readonly maxBpm: number;      // Default 200
  readonly sensitivity: number; // Default 0.5 (0=strict, 1=loose)
  readonly windowSize: number;  // Default 2048
  readonly hopSize: number;     // Default 512
}
```

### 2.4 WASM Acceleration + JS Fallback

OpenReel's `BeatDetectionProcessor` implements a dual-mode pattern:

```typescript
// packages/core/src/wasm/beat-detection/index.ts

class BeatDetectionProcessor {
  computeRMSEnergies(samples, windowSize, hopSize, energies) {
    if (this.useWasm && wasmModule) {
      wasmModule.computeRMSEnergies(samples, windowSize, hopSize, energies);
    } else {
      jsComputeRMSEnergies(samples, windowSize, hopSize, energies);  // Pure JS fallback
    }
  }
  // smoothArray, calculateMedian, findPeaks, calculateMean — same pattern
}
```

**QCut strategy: Start with JS-only fallback.** WASM optimization comes later. The JS version handles 3-5 minute audio tracks with no issues.

### 2.5 Bridge Layer Pattern

OpenReel's `BeatSyncBridge` provides state management and utility methods:

```typescript
// apps/web/src/bridges/beat-sync-bridge.ts

interface BeatSyncState {
  isAnalyzing: boolean;
  progress: number;
  error: string | null;
  beatMarkers: TimelineBeatMarker[];
  beatAnalysis: TimelineBeatAnalysis;
}

// Utility methods
bridge.analyzeAudioFromBlob(blob, clipId)   // Analyze from Blob
bridge.snapTimeToNearestBeat(time)          // Snap time to nearest beat
bridge.getBeatsInRange(start, end)          // Get beats in time range
bridge.generateCutPointsForClips(clips, 4)  // Generate cut points every N beats
bridge.generateManualBeatMarkers(bpm, dur)  // Manual BPM mode
```

---

## 3. Existing QCut Infrastructure to Leverage

### 3.1 Relevant Files

| QCut File Path | Purpose | Relation to Beat Detection |
|---------------|---------|---------------------------|
| `apps/web/src/components/editor/audio-waveform.tsx` | WaveSurfer.js waveform visualization | Audio input source; extend with beat markers |
| `apps/web/src/stores/timeline/timeline-store.ts` | Core timeline store | Add beat marker state |
| `apps/web/src/stores/timeline/types.ts` | Timeline type definitions | Extend with marker types |
| `apps/web/src/stores/timeline/timeline-store-operations.ts` | Timeline operations (split, ripple) | Add beat-based split |
| `packages/editor-core/src/types/timeline.ts` | Core type definitions | Add BeatMarker types |
| `apps/web/src/components/editor/properties-panel/audio-properties.tsx` | Audio properties panel | Add "Detect Beats" button |
| `apps/web/src/lib/export-cli/sources/audio-detection.ts` | Audio source detection | Reuse audio detection logic |
| `apps/web/src/lib/ffmpeg/audio-mixer.ts` | FFmpeg audio mixing | Extract audio for beat detection |
| `electron/elevenlabs-transcribe-handler.ts` | ElevenLabs transcription | Reference for audio processing flow |
| `electron/gemini-transcribe-handler.ts` | Gemini transcription | Reference for audio processing flow |
| `apps/web/src/hooks/use-ai-pipeline.ts` | AI Pipeline hook | Reference for async task pattern |

### 3.2 QCut Timeline Type Structure

QCut's timeline currently has no "marker" concept. Element types are:
```
media | text | sticker | captions | remotion | markdown
```

Beat markers need to be an **independent overlay layer**, not timeline elements. This matches OpenReel's design approach.

---

## 4. New Files to Create

### 4.1 File List

| New File Path | Purpose | Based on OpenReel |
|--------------|---------|-------------------|
| `packages/editor-core/src/audio/beat-detection-engine.ts` | Core algorithm (pure JS) | Direct copy, simplified |
| `packages/editor-core/src/audio/beat-detection-types.ts` | Type definitions | Extracted from OpenReel |
| `packages/editor-core/src/audio/index.ts` | Audio module entry | New |
| `apps/web/src/stores/beat-detection/beat-detection-store.ts` | Zustand store | Based on BeatSyncBridge |
| `apps/web/src/stores/beat-detection/index.ts` | Store entry | New |
| `apps/web/src/components/editor/beat-detection-panel.tsx` | UI panel | Based on BeatSyncSection |
| `apps/web/src/components/editor/timeline/beat-markers-overlay.tsx` | Timeline marker rendering | New |
| `apps/web/src/hooks/use-beat-detection.ts` | React hook | New |

### 4.2 Core Algorithm Module

**File: `packages/editor-core/src/audio/beat-detection-types.ts`**

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

**File: `packages/editor-core/src/audio/beat-detection-engine.ts`**

```typescript
/**
 * Beat Detection Engine
 * Adapted from OpenReel Video (MIT License)
 * https://github.com/Augani/openreel-video
 * 
 * Pure JS implementation — no WASM dependency.
 * Works in Electron (main + renderer) and Node.js CLI.
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
   * Works in both browser (AudioBuffer.getChannelData) and Node.js (ffmpeg-extracted PCM).
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

  /** Browser-only: analyze from AudioBuffer. */
  async analyzeAudioBuffer(audioBuffer: AudioBuffer): Promise<BeatAnalysisResult> {
    const channelData = audioBuffer.getChannelData(0);
    return this.analyzeFromSamples(
      channelData,
      audioBuffer.sampleRate,
      audioBuffer.duration
    );
  }

  // --- Methods below adapted directly from OpenReel, WASM calls removed ---

  private detectOnsets(samples: Float32Array, sampleRate: number): number[] {
    const { windowSize, hopSize, sensitivity } = this.config;
    const numFrames = Math.floor((samples.length - windowSize) / hopSize);
    
    // Step 1: Compute RMS energy per frame
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

    // Step 2: Smooth energies
    const smoothed = new Float32Array(numFrames);
    const halfWin = 2;
    for (let i = 0; i < numFrames; i++) {
      let sum = 0, count = 0;
      for (let j = i - halfWin; j <= i + halfWin; j++) {
        if (j >= 0 && j < numFrames) { sum += energies[j]; count++; }
      }
      smoothed[i] = sum / count;
    }

    // Step 3: Adaptive threshold
    const threshold = this.calculateAdaptiveThreshold(
      Array.from(smoothed), sensitivity
    );

    // Step 4: Peak detection with constraints
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
    let nearest = beats[0], minDist = Math.abs(beats[0].time - time);
    for (const beat of beats) {
      const dist = Math.abs(beat.time - time);
      if (dist < minDist) { minDist = dist; nearest = beat; }
    }
    return minDist <= threshold ? nearest.time : time;
  }
}
```

### 4.3 Zustand Store

**File: `apps/web/src/stores/beat-detection/beat-detection-store.ts`**

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
  isAnalyzing: boolean;
  progress: number;
  error: string | null;
  beatMarkers: TimelineBeatMarker[];
  beatAnalysis: TimelineBeatAnalysis | null;
  config: Partial<BeatDetectionConfig>;

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
    return downbeats.filter((_, i) => i > 0 && i % beatsPerCut === 0).map(m => m.time);
  },

  snapToNearestBeat: (time, threshold = 0.1) => {
    const { beatMarkers } = get();
    if (beatMarkers.length === 0) return time;
    let nearest = beatMarkers[0], minDist = Math.abs(nearest.time - time);
    for (const m of beatMarkers) {
      const d = Math.abs(m.time - time);
      if (d < minDist) { minDist = d; nearest = m; }
    }
    return minDist <= threshold ? nearest.time : time;
  },
}));
```

### 4.4 Timeline Marker Rendering

**File: `apps/web/src/components/editor/timeline/beat-markers-overlay.tsx`**

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

  // Only render visible markers
  const startTime = scrollLeft / zoomLevel;
  const endTime = (scrollLeft + visibleWidth) / zoomLevel;
  const visible = beatMarkers.filter(
    m => m.time >= startTime - 1 && m.time <= endTime + 1
  );

  return (
    <div className="absolute inset-0 pointer-events-none z-10">
      {visible.map((marker) => {
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
                  ? 'bg-orange-400/60'   // Downbeat: orange
                  : 'bg-blue-400/30'     // Regular beat: subtle blue
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

### 4.5 Beat Detection UI Panel

**File: `apps/web/src/components/editor/beat-detection-panel.tsx`**

```tsx
/**
 * Beat Detection Panel
 * UI for triggering beat analysis and viewing results.
 * Adapted from OpenReel Video's BeatSyncSection (MIT License).
 */
import React, { useState, useCallback } from 'react';
import { Music, Zap, Loader2, Scissors, RefreshCw } from 'lucide-react';
import { useBeatDetectionStore } from '@/stores/beat-detection';

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

      {isAnalyzing ? (
        <div className="p-3 bg-background-tertiary rounded-lg">
          <div className="flex items-center gap-2 mb-2">
            <Loader2 size={14} className="animate-spin text-primary" />
            <span className="text-[10px]">Analyzing beats... {progress}%</span>
          </div>
          <div className="h-1.5 bg-background-secondary rounded-full overflow-hidden">
            <div className="h-full bg-primary transition-all" style={{ width: `${progress}%` }} />
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

      {error && (
        <p className="text-[10px] text-red-400 bg-red-400/10 p-2 rounded">{error}</p>
      )}

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

      {beatMarkers.length > 0 && (
        <div className="space-y-2">
          <button
            onClick={() => {/* TODO: wire to timeline split */}}
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
            onClick={() => generateManualBeats(manualBpm, 300)}
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

## 5. Files to Modify

### 5.1 Modification List

| Existing File | Changes | Complexity |
|--------------|---------|------------|
| `packages/editor-core/src/index.ts` | Export audio module | Low |
| `apps/web/src/stores/timeline/types.ts` | Add beat marker types to store | Low |
| `apps/web/src/components/editor/audio-waveform.tsx` | Integrate beat marker display | Medium |
| `apps/web/src/components/editor/properties-panel/audio-properties.tsx` | Add BeatDetectionPanel | Medium |
| `apps/web/src/stores/timeline/timeline-store-operations.ts` | Add splitOnBeats operation | Medium |

### 5.2 editor-core Entry Export

**Modify: `packages/editor-core/src/index.ts`**

```typescript
// Add these exports
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

### 5.3 Timeline Store Extension

**Modify: `apps/web/src/stores/timeline/timeline-store-operations.ts`**

Add beat-based split capability:

```typescript
import { useBeatDetectionStore } from '@/stores/beat-detection';

// Add to createTimelineOperations:
splitOnBeats: (trackId: string, elementId: string, beatsPerCut: number = 4) => {
  const beatStore = useBeatDetectionStore.getState();
  const cutPoints = beatStore.getCutPoints(beatsPerCut);
  const { _tracks } = get();
  
  const track = _tracks.find(t => t.id === trackId);
  const element = track?.elements.find(e => e.id === elementId);
  if (!track || !element) return;

  // Filter cut points within element bounds
  const validCuts = cutPoints.filter(
    t => t > element.startTime && t < element.startTime + element.duration
  );

  // Cut from back to front to avoid time offset issues
  for (const cutTime of validCuts.reverse()) {
    get().splitElement(trackId, elementId, cutTime);
  }
},
```

---

## 6. Step-by-Step Implementation Plan

### Phase 1: Core Algorithm (2-3 hours)

```
Step 1.1: Create packages/editor-core/src/audio/ directory
Step 1.2: Write beat-detection-types.ts
Step 1.3: Write beat-detection-engine.ts (pure JS, no WASM)
Step 1.4: Create index.ts entry
Step 1.5: Update editor-core/src/index.ts exports
Step 1.6: Write unit tests to validate algorithm
```

### Phase 2: Store + Hook (1-2 hours)

```
Step 2.1: Create stores/beat-detection/beat-detection-store.ts
Step 2.2: Create hooks/use-beat-detection.ts
Step 2.3: Verify store state transitions
```

### Phase 3: UI Integration (2-3 hours)

```
Step 3.1: Create BeatDetectionPanel component
Step 3.2: Integrate into audio-properties.tsx
Step 3.3: Create BeatMarkersOverlay
Step 3.4: Integrate into timeline rendering
```

### Phase 4: Operation Integration (1-2 hours)

```
Step 4.1: Add splitOnBeats to timeline-store-operations
Step 4.2: Add snapToNearestBeat to drag logic
Step 4.3: Wire "Auto-Cut" button to actual operations
```

### Phase 5: CLI Integration (Optional, 1 hour)

```
Step 5.1: Add --beat-sync flag to CLI pipeline
Step 5.2: Use ffmpeg to extract audio PCM data
Step 5.3: Call BeatDetectionEngine.analyzeFromSamples()
```

---

## 7. CLI Pipeline Integration

QCut's `qcut-pipeline autoclip` command can use beat detection for optimized cut points:

```typescript
// CLI usage example (Node.js, no browser AudioContext needed)
import { execSync } from 'child_process';
import { BeatDetectionEngine } from '@qcut/editor-core';

function extractPCMFromAudio(audioPath: string): { samples: Float32Array; sampleRate: number } {
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
  
  // Every 4th downbeat as a cut point
  const cutPoints = result.downbeats.filter((_, i) => i > 0 && i % 4 === 0);
  return cutPoints;
}
```

---

## 8. Complete File Change Summary

### New Files (8)

| # | File Path | Purpose |
|---|-----------|---------|
| 1 | `packages/editor-core/src/audio/beat-detection-types.ts` | Type definitions |
| 2 | `packages/editor-core/src/audio/beat-detection-engine.ts` | Core algorithm |
| 3 | `packages/editor-core/src/audio/index.ts` | Module entry |
| 4 | `apps/web/src/stores/beat-detection/beat-detection-store.ts` | Zustand store |
| 5 | `apps/web/src/stores/beat-detection/index.ts` | Store entry |
| 6 | `apps/web/src/components/editor/beat-detection-panel.tsx` | UI panel |
| 7 | `apps/web/src/components/editor/timeline/beat-markers-overlay.tsx` | Marker rendering |
| 8 | `apps/web/src/hooks/use-beat-detection.ts` | React hook |

### Modified Files (5)

| # | File Path | Changes |
|---|-----------|---------|
| 1 | `packages/editor-core/src/index.ts` | Export audio module |
| 2 | `apps/web/src/stores/timeline/types.ts` | Extend store interface |
| 3 | `apps/web/src/components/editor/properties-panel/audio-properties.tsx` | Integrate panel |
| 4 | `apps/web/src/stores/timeline/timeline-store-operations.ts` | splitOnBeats |
| 5 | `apps/web/src/components/editor/audio-waveform.tsx` | Optional: show beat markers |

### Time Estimate

| Phase | Time |
|-------|------|
| Phase 1: Core Algorithm | 2-3 hours |
| Phase 2: Store + Hook | 1-2 hours |
| Phase 3: UI Integration | 2-3 hours |
| Phase 4: Operation Integration | 1-2 hours |
| Phase 5: CLI (Optional) | 1 hour |
| **Total** | **~1-2 days** |

---

## 9. License Compliance

OpenReel Video uses the **MIT License**, which permits free use, modification, and distribution. When reusing code:

1. Add a source attribution comment in file headers:
   ```typescript
   // Adapted from OpenReel Video (MIT License)
   // https://github.com/Augani/openreel-video
   ```
2. Include attribution in your project's LICENSE or NOTICE file
3. Preserve original copyright notices

---

## Summary

Beat detection is the key feature for QCut to support "cut-on-beat" editing workflows. OpenReel Video provides a production-grade implementation — the core algorithm (~280 lines of TypeScript) can be directly reused. QCut's existing audio processing, timeline store, and WaveSurfer waveform components significantly reduce integration effort.

**Minimum viable path:** Copy `BeatDetectionEngine` → create Zustand store → add "Detect Beats" button to audio properties panel → render beat markers on timeline. One day for a basic working version.

🦞
