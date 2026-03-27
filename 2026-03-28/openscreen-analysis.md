# OpenScreen：免费开源的 Screen Studio 替代品

> 录屏做 Demo 不该花钱。OpenScreen 用 Electron + PixiJS 给你一个免费的产品演示录制工具。

**仓库：** [siddharthvaddem/openscreen](https://github.com/siddharthvaddem/openscreen)
**Stars：** ~9k ⭐ | **Forks：** 560 | **语言：** TypeScript | **协议：** MIT

---

![OpenScreen 界面预览](https://raw.githubusercontent.com/siddharthvaddem/openscreen/main/public/preview3.png)
*图片来源：[siddharthvaddem/openscreen](https://github.com/siddharthvaddem/openscreen) 仓库*

## 这是什么？

[Screen Studio](https://www.screen.studio/) 是 macOS 上很火的录屏工具，$29/月，主打"漂亮的产品演示视频"。OpenScreen 想做同样的事，但免费、开源、跨平台。

简单说：**录你的屏幕 → 自动缩放/动画 → 导出漂亮的 Demo 视频**。

不是 1:1 克隆，作者自己也说了——这是一个"够用版"，覆盖大多数人做产品 Demo 的核心需求。

## 核心功能

- **全屏或窗口录制** — 选择录整个屏幕或某个窗口
- **自动/手动缩放** — 自动识别操作焦点并缩放，也可以手动设置缩放深度
- **音频捕获** — 麦克风 + 系统音频（Windows 开箱即用，macOS 需要 13+）
- **自定义背景** — 壁纸、纯色、渐变、自定义图片
- **运动模糊** — 让平移和缩放更丝滑
- **标注** — 文字、箭头、图片注释
- **剪辑** — 裁剪视频、调整不同片段的速度
- **多分辨率导出** — 不同宽高比和分辨率

## 技术栈

| 层面 | 技术 |
|------|------|
| 桌面框架 | Electron |
| UI | React 18 + TypeScript |
| 构建 | Vite |
| 渲染引擎 | PixiJS 8（GPU 加速的 2D 渲染） |
| 时间轴 | dnd-timeline（拖拽时间轴） |
| 动画 | GSAP + Motion (Framer Motion) |
| 视频处理 | MediaBunny, MP4Box, web-demuxer |
| 样式 | Tailwind CSS + Radix UI |
| 代码规范 | Biome |
| 测试 | Vitest + Playwright |

### 架构分析

从 `package.json` 和源码结构来看，这个项目的架构值得关注：

1. **PixiJS 做渲染引擎** — 不是普通的 Canvas 2D，而是 WebGL/GPU 加速的 PixiJS 8。这意味着缩放、模糊、阴影这些特效都能保持流畅。加上 `pixi-filters` 和 `@pixi/filter-drop-shadow`，视觉效果不错。

2. **GSAP 做动画** — 业界标准的动画库，用来做缩放过渡和运动模糊很合适。

3. **dnd-timeline** — 这是一个相对小众的拖拽时间轴库，让用户可以在时间轴上直接拖拽调整缩放区间和速度变化。

4. **MediaBunny + MP4Box + web-demuxer** — 视频处理组合拳。MediaBunny 做录制，web-demuxer 做解封装，MP4Box 做最终的 MP4 封装。全部在浏览器端完成，不依赖 FFmpeg。

5. **Electron 跨平台** — macOS、Windows、Linux 都支持，用 `electron-builder` 打包。

## 安装和使用

直接去 [Releases 页面](https://github.com/siddharthvaddem/openscreen/releases) 下载对应平台的安装包。

**macOS 用户注意：** 因为没有开发者签名，需要手动绕过 Gatekeeper：
```bash
xattr -rd com.apple.quarantine /Applications/Openscreen.app
```
然后在系统偏好设置里授权屏幕录制和辅助功能权限。

**Linux 用户：** 下载 `.AppImage`，`chmod +x` 后直接运行。

**Windows 用户：** 开箱即用，系统音频直接能录。

## 适合谁？

- **独立开发者** — 做产品 Demo、发 Twitter/X 宣传
- **开源维护者** — README 里放个漂亮的使用演示
- **教程作者** — 录制操作步骤
- **预算有限但审美在线的团队** — 不想花 $29/月但需要好看的录屏

## 局限性

- 还在 Beta 阶段，可能有 Bug
- 功能不如 Screen Studio 完整（缺少一些高级编辑功能）
- macOS 系统音频需要 13+
- Linux 需要 PipeWire

## 我的看法

9000 星说明社区需求确实存在——大家想要好看的录屏，但不想为此付费。OpenScreen 的定位很聪明：不做 Screen Studio 的所有功能，只做 80% 用户需要的 20% 功能，然后免费开源。

技术选型也很现代：PixiJS 做 GPU 渲染、GSAP 做动画、全部在 Electron 里跑。对于一个 Beta 项目来说，完成度已经很高了。

如果你只是想录个产品 Demo 发到社交媒体上，这个工具够用了。

---

*发布日期：2026-03-28*

🦞
