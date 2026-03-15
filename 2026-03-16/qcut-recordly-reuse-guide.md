# QCut 如何复用 Recordly 的屏幕录制增强代码：实战集成指南

> Recordly 是一个 MIT 开源的 Electron + TypeScript 屏幕录制器，拥有光标动画、自动缩放、背景美化等 Screen Studio 级别的功能。QCut 是同技术栈的视频编辑器，自带基础屏录但缺少"抛光层"。本文是一份实战指南：从 Recordly 仓库里挑哪些代码、怎么搬、搬完怎么接。

**仓库：** https://github.com/webadderall/Recordly  
**协议：** MIT  
**技术栈：** Electron + React + TypeScript + PixiJS  

---

## 1. QCut 缺什么 vs Recordly 有什么

| 功能 | QCut 现状 | Recordly 实现 |
|------|----------|---------------|
| 光标渲染 | 无 — 录屏只录原生系统光标 | PixiJS 渲染管线：平滑、运动模糊、点击弹跳、macOS 风格光标素材 |
| 自动缩放 | 无 | 基于光标活动的自动缩放建议 + 手动缩放区域 + 平滑 pan 过渡 |
| 背景美化 | 无 | 23+ 内置壁纸、渐变、纯色、模糊、圆角、阴影、padding |
| 光标坐标采集 | 无 | uiohook-napi 原生模块实时采集坐标 + 光标类型 |
| 缩放合成导出 | 无 | 导出管线内置缩放变换合成 |

**一句话：** QCut 录的是"原始素材"，Recordly 录的是"成品演示视频"。差距就在这五块。

---

## 2. Recordly 仓库结构地图

```
Recordly/
├── electron/
│   ├── native/              # 原生采集层
│   │   ├── macos/           # ScreenCaptureKit (macOS 12.3+)
│   │   └── windows/         # WGC 屏幕采集 + WASAPI 音频
│   ├── ipc/                 # Electron IPC 通道定义
│   ├── uiohook-napi.d.ts    # uiohook 光标坐标采集类型声明
│   ├── main.ts              # 主进程入口
│   ├── preload.ts           # 预加载脚本
│   └── windows.ts           # 窗口管理
│
├── src/
│   ├── components/video-editor/
│   │   ├── videoPlayback/        # ⭐ 核心：光标渲染管线
│   │   │   ├── cursorRenderer.ts      # 光标渲染器（PixiJS Sprite + 阴影 + 点击动画）
│   │   │   ├── motionSmoothing.ts     # 弹簧物理平滑（spring dynamics）
│   │   │   ├── zoomRegionUtils.ts     # 缩放区域强度计算 + 过渡
│   │   │   ├── zoomTransform.ts       # 缩放矩阵变换
│   │   │   ├── focusUtils.ts          # 焦点区域约束
│   │   │   ├── mathUtils.ts           # 缓动曲线（cubic-bezier, easeOut）
│   │   │   ├── layoutUtils.ts         # 视口布局
│   │   │   ├── overlayUtils.ts        # 覆盖层工具
│   │   │   ├── uploadedCursorAssets.ts # macOS 风格光标 SVG 素材
│   │   │   ├── cursorLoopTelemetry.ts # 光标循环回位
│   │   │   ├── videoEventHandlers.ts  # 视频事件处理
│   │   │   └── constants.ts           # 常量定义
│   │   │
│   │   └── timeline/             # 时间线 UI
│   │       ├── ZoomSpan/         # 缩放区间轨道
│   │       └── SpeedRegion/      # 变速区间轨道
│   │
│   ├── lib/
│   │   ├── wallpapers.ts         # ⭐ 23+ 内置壁纸预设
│   │   ├── exporter/             # ⭐ 导出管线（含缩放合成）
│   │   ├── assetPath.ts          # 资源路径解析
│   │   ├── customFonts.ts        # 自定义字体
│   │   ├── shortcuts.ts          # 快捷键
│   │   └── utils.ts              # 通用工具函数
│   │
│   └── utils/
│       └── aspectRatioUtils.ts   # 宽高比计算
```

### 关键文件速览

**`cursorRenderer.ts`** — 光标渲染的核心引擎：

```typescript
// Recordly 的光标渲染配置
export interface CursorRenderConfig {
  dotRadius: number;       // 光标基础大小（参考 1920px 宽度）
  dotColor: number;        // 光标颜色（hex）
  dotAlpha: number;        // 光标透明度
  smoothingFactor: number; // 平滑因子（0-1，越低越平滑）
  motionBlur: number;      // 方向运动模糊
  clickBounce: number;     // 点击弹跳倍率
}

export const DEFAULT_CURSOR_CONFIG: CursorRenderConfig = {
  dotRadius: 28,
  dotColor: 0xffffff,
  dotAlpha: 0.95,
  smoothingFactor: 0.18,
  motionBlur: 0,
  clickBounce: 1,
};
```

**`motionSmoothing.ts`** — 弹簧物理模型：

```typescript
// 弹簧状态
export interface SpringState {
  value: number;
  velocity: number;
  initialized: boolean;
}

// 弹簧配置 — 控制光标平滑手感
export interface SpringConfig {
  stiffness: number;  // 刚度：越高越"硬"
  damping: number;    // 阻尼：越高越快停
  mass: number;       // 质量：越重越慢
}

// 根据 smoothingFactor 计算弹簧参数
export function getCursorSpringConfig(smoothingFactor: number): SpringConfig {
  // smoothingFactor 0 → 几乎无平滑 (stiffness=1000)
  // smoothingFactor 0.5 → 中等平滑 (stiffness=340)
  // smoothingFactor 2.0 → 极致丝滑 (stiffness=160)
}
```

**`wallpapers.ts`** — 壁纸预设（纯数据，直接可搬）：

```typescript
export interface BuiltInWallpaper {
  id: string;
  label: string;
  relativePath: string;
  publicPath: string;
}

export const BUILT_IN_WALLPAPERS: BuiltInWallpaper[] = [
  { id: 'wallpaper-1', label: 'Wallpaper 1', relativePath: 'wallpapers/wallpaper1.jpg', ... },
  { id: 'cityscape', label: 'Cityscape', relativePath: 'wallpapers/cityscape.jpg', ... },
  // 共 23+ 个预设
];
```

---

## 3. 复用优先级分层

### Tier 1 — 直接可搬（~3 天）

| 模块 | 文件 | 搬法 |
|------|------|------|
| 光标渲染管线 | `videoPlayback/cursorRenderer.ts` + `motionSmoothing.ts` + `mathUtils.ts` | 整目录拷贝，改 import 路径，接 QCut 的 PixiJS 实例 |
| 光标坐标采集 | `electron/uiohook-napi.d.ts` + 主进程 uiohook 监听 | npm install uiohook-napi，在 QCut 录屏进程里加监听 |
| 壁纸预设 | `src/lib/wallpapers.ts` + `public/wallpapers/` | 直接拷贝文件 + 图片资源 |
| 光标素材 | `videoPlayback/uploadedCursorAssets.ts` | 拷贝 SVG data URL 素材 |

### Tier 2 — 需要适配（~3-4 天）

| 模块 | 文件 | 适配点 |
|------|------|--------|
| 自动缩放建议 | `zoomRegionUtils.ts` + `focusUtils.ts` | 算法可直接用，但 ZoomRegion 类型要映射到 QCut 的 track 数据结构 |
| 缩放合成导出 | `src/lib/exporter/` + `zoomTransform.ts` | QCut 导出管线是 FFmpeg CLI，Recordly 是 PixiJS 帧渲染 + 编码，需要把缩放变换注入 QCut 的导出流程 |
| 宽高比工具 | `utils/aspectRatioUtils.ts` | 小改：QCut 已有部分比例逻辑，合并不替换 |

### Tier 3 — 仅供参考

| 模块 | 原因 |
|------|------|
| Timeline UI（ZoomSpan / SpeedRegion） | QCut 有完整的多轨时间线，Recordly 的是单一录屏时间线，架构不同 |
| 状态管理 | Recordly 用 React Context，QCut 用 Zustand，不能直接搬 |
| 原生采集层 | QCut 已有自己的采集管线（`editor:screen-recording:*`），不需要替换 |

---

## 4. 分步集成计划

### Step 1：录屏时采集光标坐标（1 天）

**目标：** 在 QCut 屏幕录制过程中，同步录制光标坐标数据。

```bash
# 安装 uiohook-napi
npm install uiohook-napi
```

在 QCut 的 Electron 主进程中添加：

```typescript
// qcut/electron/services/cursorTelemetry.ts
import { uIOhook, UiohookMouseEvent } from 'uiohook-napi';

interface CursorTelemetryPoint {
  timestamp: number;   // 相对于录制开始的毫秒数
  x: number;           // 屏幕坐标
  y: number;
  pressed: boolean;    // 是否按下
  cursorType?: string; // 'arrow' | 'text' | 'pointer' | ...
}

export class CursorTelemetryRecorder {
  private points: CursorTelemetryPoint[] = [];
  private startTime = 0;
  private recording = false;

  start() {
    this.points = [];
    this.startTime = Date.now();
    this.recording = true;

    uIOhook.on('mousemove', (e: UiohookMouseEvent) => {
      if (!this.recording) return;
      this.points.push({
        timestamp: Date.now() - this.startTime,
        x: e.x,
        y: e.y,
        pressed: false,
      });
    });

    uIOhook.on('mousedown', (e: UiohookMouseEvent) => {
      if (!this.recording) return;
      this.points.push({
        timestamp: Date.now() - this.startTime,
        x: e.x,
        y: e.y,
        pressed: true,
      });
    });

    uIOhook.start();
  }

  stop(): CursorTelemetryPoint[] {
    this.recording = false;
    uIOhook.stop();
    return this.points;
  }
}
```

通过 IPC 暴露给渲染进程：

```typescript
// qcut/electron/preload 补充
ipcMain.handle('cursor-telemetry:start', () => recorder.start());
ipcMain.handle('cursor-telemetry:stop', () => recorder.stop());
```

### Step 2：移植光标平滑 + 运动模糊渲染器（1 天）

**目标：** 在 QCut 的视频预览画布上渲染平滑的动画光标。

从 Recordly 拷贝以下文件到 QCut：

```
src/components/video-editor/videoPlayback/
├── cursorRenderer.ts
├── motionSmoothing.ts
├── mathUtils.ts
└── uploadedCursorAssets.ts
```

在 QCut 的预览组件中集成：

```typescript
// qcut/src/components/preview/CursorOverlay.tsx
import { CursorRenderer } from './cursor/cursorRenderer';
import { DEFAULT_CURSOR_CONFIG } from './cursor/cursorRenderer';

// QCut 用 Zustand，所以状态层要重写
import { useScreenRecordingStore } from '@/stores/screenRecording';

export function CursorOverlay({ pixiApp }: { pixiApp: Application }) {
  const cursorData = useScreenRecordingStore(s => s.cursorTelemetry);
  const config = useScreenRecordingStore(s => s.cursorConfig);

  useEffect(() => {
    // 初始化 Recordly 的光标渲染器
    const renderer = new CursorRenderer(pixiApp.stage, {
      ...DEFAULT_CURSOR_CONFIG,
      ...config,
    });

    return () => renderer.destroy();
  }, [pixiApp, config]);
}
```

**关键适配：** Recordly 的 `cursorRenderer.ts` 依赖 `pixi.js` 和 `pixi-filters/motion-blur`。QCut 如果还没用 PixiJS，需要添加依赖：

```bash
npm install pixi.js @pixi/filter-motion-blur
```

### Step 3：添加背景美化选项（0.5 天）

**目标：** 录屏回放时可以选择壁纸背景、渐变、圆角等。

直接拷贝 `src/lib/wallpapers.ts` 和 `public/wallpapers/` 图片目录。

在 QCut 的属性面板加一个背景设置区：

```typescript
// qcut/src/stores/screenRecording.ts — Zustand store 补充
interface ScreenRecordingState {
  // ... 已有字段
  background: {
    type: 'none' | 'wallpaper' | 'gradient' | 'solid';
    wallpaperId?: string;
    gradientColors?: [string, string];
    solidColor?: string;
    padding: number;       // 画面内边距
    borderRadius: number;  // 圆角半径
    shadow: boolean;       // 投影开关
    blur: number;          // 背景模糊
  };
}

// 壁纸列表直接从 Recordly 搬来
import { BUILT_IN_WALLPAPERS } from '@/lib/wallpapers';
```

### Step 4：实现自动缩放建议（2 天）

**目标：** 根据光标活动自动生成缩放区域建议。

从 Recordly 拷贝核心算法：

```
videoPlayback/
├── zoomRegionUtils.ts   # 缩放区域强度计算
├── zoomTransform.ts     # 缩放矩阵变换
├── focusUtils.ts        # 焦点约束
└── constants.ts         # 过渡时间常量
```

**核心算法逻辑（来自 `zoomRegionUtils.ts`）：**

```typescript
// Recordly 的缩放强度计算 — Screen Studio 风格的缓动
export function computeRegionStrength(region: ZoomRegion, timeMs: number) {
  const zoomInEnd = region.startMs + ZOOM_IN_OVERLAP_MS;  // 500ms
  const leadInStart = zoomInEnd - ZOOM_IN_TRANSITION_WINDOW_MS;
  const leadOutEnd = region.endMs + TRANSITION_WINDOW_MS;

  if (timeMs < leadInStart || timeMs > leadOutEnd) return 0;
  if (timeMs < zoomInEnd) {
    const progress = (timeMs - leadInStart) / ZOOM_IN_TRANSITION_WINDOW_MS;
    return easeOutScreenStudio(progress);  // Screen Studio 特有的缓动曲线
  }
  if (timeMs <= region.endMs) return 1;
  // 淡出
  const progress = clamp01((timeMs - region.endMs) / TRANSITION_WINDOW_MS);
  return 1 - easeOutScreenStudio(progress);
}
```

**适配到 QCut 的关键点：** QCut 的时间线是多轨结构（视频轨、音频轨、字幕轨等），缩放建议需要映射到 QCut 的 track 系统：

```typescript
// qcut 侧的适配层
interface QCutZoomSuggestion {
  trackId: string;          // QCut track ID
  startFrame: number;       // QCut 用帧数
  endFrame: number;
  zoomLevel: number;        // 1.0 = 无缩放, 2.0 = 2x
  focusX: number;           // 0-1 归一化坐标
  focusY: number;
}

function recordlyRegionToQCutSuggestion(
  region: ZoomRegion,
  fps: number,
): QCutZoomSuggestion {
  return {
    trackId: 'screen-recording-zoom',
    startFrame: Math.round((region.startMs / 1000) * fps),
    endFrame: Math.round((region.endMs / 1000) * fps),
    zoomLevel: ZOOM_DEPTH_SCALES[region.depth] ?? 1.5,
    focusX: region.focus.cx,
    focusY: region.focus.cy,
  };
}
```

### Step 5：缩放合成集成到 QCut 导出管线（1.5 天）

**目标：** 导出视频时把缩放动画"烘焙"进最终画面。

Recordly 的导出流程是：PixiJS 逐帧渲染 → 编码。QCut 用的是 FFmpeg 导出。

**方案A（推荐）：** 在 QCut 的预览帧回调里注入缩放变换

```typescript
// qcut 导出管线扩展
import { computeRegionStrength } from './zoom/zoomRegionUtils';
import { interpolateZoomTransform } from './zoom/zoomTransform';

function applyZoomToExportFrame(
  frame: CanvasRenderingContext2D,
  timeMs: number,
  zoomRegions: ZoomRegion[],
  sourceWidth: number,
  sourceHeight: number,
) {
  // 计算当前时间点的缩放状态
  let maxStrength = 0;
  let activeRegion: ZoomRegion | null = null;

  for (const region of zoomRegions) {
    const strength = computeRegionStrength(region, timeMs);
    if (strength > maxStrength) {
      maxStrength = strength;
      activeRegion = region;
    }
  }

  if (!activeRegion || maxStrength <= 0) return;

  // 应用缩放变换
  const scale = 1 + (activeRegion.depth - 1) * maxStrength;
  const focusX = activeRegion.focus.cx * sourceWidth;
  const focusY = activeRegion.focus.cy * sourceHeight;

  frame.save();
  frame.translate(focusX, focusY);
  frame.scale(scale, scale);
  frame.translate(-focusX, -focusY);
  // 渲染缩放后的帧内容
  frame.restore();
}
```

**方案B：** 用 FFmpeg filter 实现（性能好，但缩放动画不够平滑）

```bash
# FFmpeg 的 zoompan filter — 简单但没有 Recordly 的弹簧动画效果
ffmpeg -i input.mp4 -vf "zoompan=z='if(between(t,2,5),1.5,1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1" output.mp4
```

---

## 5. 踩坑指南

### 状态管理不兼容

```
Recordly: React Context + useReducer
QCut:     Zustand store
```

**解决方法：** 不搬 Recordly 的 Context Provider，把光标配置、缩放区域等状态直接加到 QCut 的 Zustand store 里。Recordly 的渲染函数是纯函数（接收参数，返回结果），状态层只是"喂数据"，所以核心算法不受影响。

### 时间线架构差异

```
Recordly: 单一录屏时间线（一条视频 + 缩放/变速标记）
QCut:     多轨时间线（视频轨 + 音频轨 + 字幕轨 + 效果轨...）
```

**原则：不替换，扩展。** 在 QCut 的时间线上新增 "Zoom Track" 轨道类型，用来放 Recordly 的缩放区域数据。

### uiohook-napi 原生依赖

```bash
# uiohook-napi 需要在 Electron 的 electron-builder 配置里声明
# package.json
{
  "build": {
    "extraResources": [],
    "nativeRebuilder": "sequential"
  }
}

# 还需要 rebuild
npx electron-rebuild -f -w uiohook-napi
```

**注意：** macOS 上需要辅助功能权限（Accessibility），Windows 上开箱即用。

### PixiJS 版本对齐

Recordly 用 PixiJS v8+。如果 QCut 还没用 PixiJS，需要加：

```bash
npm install pixi.js@^8.0.0 pixi-filters
```

如果 QCut 已有其他 Canvas 渲染方案（比如 Fabric.js），光标渲染层可以作为独立的 PixiJS overlay，不需要替换现有渲染层。

### 光标坐标系转换

Recordly 的光标坐标是屏幕绝对坐标，需要转换到录制区域的相对坐标：

```typescript
function screenToRelative(
  screenX: number, screenY: number,
  captureRect: { x: number; y: number; width: number; height: number },
): { rx: number; ry: number } {
  return {
    rx: (screenX - captureRect.x) / captureRect.width,
    ry: (screenY - captureRect.y) / captureRect.height,
  };
}
```

---

## 6. 时间线估算

| 阶段 | 时间 | 内容 |
|------|------|------|
| Step 1 | 1 天 | uiohook-napi 集成 + 光标坐标采集 |
| Step 2 | 1 天 | 光标渲染管线移植 + PixiJS 集成 |
| Step 3 | 0.5 天 | 壁纸/背景美化 |
| Step 4 | 2 天 | 自动缩放建议算法 + QCut track 适配 |
| Step 5 | 1.5 天 | 导出管线缩放合成 |
| 测试 + 调优 | 1-2 天 | 端到端测试，调参 |
| **合计** | **~7-8 天（1-1.5 周）** | |

---

## 7. 总结

Recordly 对 QCut 的价值不在于"拿一个完整功能来用"，而在于**它把 Screen Studio 的核心体验拆解成了可复用的独立模块**：

1. **光标渲染管线**（cursorRenderer + motionSmoothing）是最值得搬的 — 弹簧物理模型、运动模糊、点击弹跳，这些手写很耗时
2. **缩放区域算法**（zoomRegionUtils + zoomTransform）是第二优先 — Screen Studio 风格的缓动曲线和过渡逻辑
3. **壁纸/背景**是送分题 — 纯数据 + 图片，拷贝即可

Recordly 的代码质量不错，类型定义完整，函数基本是纯函数，这让移植变得相对容易。最大的工作量在"胶水层"：把 Recordly 的数据结构映射到 QCut 的 store 和 track 系统。

🦞
