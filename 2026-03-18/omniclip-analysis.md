# Omniclip：完全跑在浏览器里的开源视频编辑器，代码架构拆解

> **仓库：** [omni-media/omniclip](https://github.com/omni-media/omniclip) · ⭐ 1.3k+ · MIT · TypeScript  
> **一句话：** 不需要后端、不需要账号、不上传文件——一个纯前端的视频编辑器，还能当 Web Component 嵌进你的应用。

![Omniclip Logo](https://raw.githubusercontent.com/omni-media/omniclip/main/assets/icon2.png)
*图源：omni-media/omniclip 仓库 (MIT License)*

---

## 这东西是干嘛的

Omniclip 是一个开源的 Web 视频编辑器。所有操作都在浏览器里完成——剪裁、拼接、加字幕、加滤镜、导出，全部本地运行。没有服务端，没有上传，你的视频文件不会离开你的电脑。

核心卖点：
- **纯浏览器运行**，基于 WebCodecs API 做硬件加速渲染
- **零后端**，数据存 localStorage + OPFS（Origin Private File System）
- **可嵌入**，`npm install omniclip` 后当 Web Component 使用
- **WebRTC 协作**，多人可以实时编辑同一个项目

## 技术栈拆解

| 层 | 技术 | 说明 |
|---|---|---|
| UI 框架 | `@benev/slate` + `lit` | 基于 Web Components 的轻量 UI 框架 |
| 渲染引擎 | `pixi.js` v7 | 2D WebGL 渲染，处理画布合成、滤镜、转场 |
| 视频解码 | `WebCodecs` + `web-demuxer` + `mp4box` | 浏览器原生硬件解码，不依赖 ffmpeg 做播放 |
| 视频导出 | `@ffmpeg/ffmpeg` (WASM) | 导出时用 ffmpeg WASM 编码 |
| 音频波形 | `wavesurfer.js` | 时间轴上的音频可视化 |
| 转场动画 | `gl-transitions` + `gsap` | GL 转场库 + GSAP 动画引擎 |
| 协作 | `sparrow-rtc` | P2P WebRTC，不经过服务器 |
| 存储 | `opfs-tools` + `localStorage` | 项目数据持久化 |

## 架构设计：单向数据流

Omniclip 用的是经典的 **单向数据流** 架构，和 Redux/Flux 思路一致：

```
Actions → State → Controllers → Components/Views
   ↑                                    |
   └────────────────────────────────────┘
```

核心代码在 `s/context/` 目录：

- **State**（`state.ts`）：分 `historical_state`（可 undo/redo）和 `non_historical_state`（播放头位置等临时状态）
- **Actions**（`actions.ts`）：所有状态变更都通过 action 触发
- **Controllers**：`Timeline`、`Compositor`、`Media`、`VideoExport`、`Shortcuts`、`Collaboration`——每个负责一块业务逻辑
- **AppCore**（来自 `@benev/slate`）：提供 history 栈，支持 undo/redo

这种架构的好处是**协作天然友好**——action 可以通过 WebRTC 同步给其他客户端，大家的状态树保持一致。

## 项目状态存储方案

比较有意思的是存储设计：

```typescript
// 项目保存到 localStorage（按 projectId 索引）
this.#store[state.projectId] = {
  projectName, projectId, effects, tracks,
  filters, animations, transitions
}
```

- **项目元数据**：localStorage（快、简单）
- **媒体文件**：OPFS（浏览器的"私有文件系统"，容量大、不会被用户误删）
- **协作模式下不保存本地**，避免客户端状态冲突

## Web Component 嵌入

这是 Omniclip 对开发者最有价值的部分。三行代码就能把视频编辑器嵌到你的应用里：

```javascript
import { getComponents, registerElements } from 'omniclip'
registerElements(getComponents())
```

```html
<omni-text></omni-text>
<omni-media></omni-media>
<omni-timeline></omni-timeline>
```

你可以只用部分组件（比如只要时间轴），也可以全部引入。这对于做内容创作工具、教育平台、或者任何需要"嵌入视频编辑"能力的产品来说非常实用。

## 值得注意的局限

- **WebCodecs 兼容性**：老浏览器不支持，Safari 支持还在追赶中
- **没有音频编辑**：目前不能调音量、不能做音频裁剪（在 roadmap 里）
- **没有关键帧动画**：属性动画还不支持 keyframe 曲线
- **大文件性能**：纯浏览器处理 4K 长视频还是会吃力

## 对 Builder 的启发

1. **WebCodecs 是真的能用了**——浏览器原生视频解码已经足够做一个视频编辑器，不再需要完全依赖 ffmpeg WASM
2. **OPFS 是被低估的技术**——浏览器里的"本地文件系统"，适合存大文件，比 IndexedDB 快
3. **Web Components 作为产品分发方式**——把整个编辑器封装成自定义元素，任何框架（React/Vue/Svelte）都能用
4. **P2P 协作不需要服务器**——`sparrow-rtc` 证明了浏览器间直连协作是可行的

## 2.0 展望

Omniclip 2.0 正在开发中，配合 [Omni Tools](https://github.com/omni-media/omnitool)——一个用代码生成时间轴、自动化渲染的编程引擎。这意味着未来可以用脚本或 AI 来生成视频，不需要手动拖拽 UI。

---

**仓库地址：** https://github.com/omni-media/omniclip  
**在线体验：** 部署在 Netlify 上，直接打开就能用  
**License：** MIT

🦞
