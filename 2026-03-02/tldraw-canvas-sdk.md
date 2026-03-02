# tldraw：价值 500 万美元的开源无限画布 SDK，正在重新定义 Canvas 应用开发

> 45,000+ GitHub Stars、3,000+ Forks、SDK 4.0 全新发布——tldraw 不只是一个白板工具，它是一个完整的无限画布基础设施，让开发者在数天内构建出过去需要数月才能完成的画布应用。

## 一句话概括

**tldraw** 是一个基于 React 的开源无限画布 SDK。你可以用它构建白板、流程图编辑器、AI 画布、可视化编程工具——任何需要"无限画布"交互的应用。它不是又一个画图库，而是一套完整的画布基础设施，包含实时协作、自定义形状、插件系统和 AI 集成。

- 🔗 官网：[tldraw.dev](https://tldraw.dev)
- 📦 GitHub：[github.com/tldraw/tldraw](https://github.com/tldraw/tldraw)（45,500+ ⭐）
- 📄 许可证：tldraw License（开发免费，生产环境需要授权）
- 💰 融资：超过 500 万美元，由 CEO Steve Ruiz 领导

## 五分钟快速上手

tldraw 的开发者体验极其丝滑。从零到一个完整的画布应用，只需三步：

### 1. 创建项目

```bash
npm create tldraw@latest
```

这一条命令会引导你选择 starter kit 并搭建完整项目。

### 2. 手动集成

如果你已有 React 项目：

```bash
npm install tldraw
```

```tsx
import { Tldraw } from 'tldraw'
import 'tldraw/tldraw.css'

export default function App() {
  return (
    <div style={{ position: 'fixed', inset: 0 }}>
      <Tldraw />
    </div>
  )
}
```

**就这样。** 三行核心代码，你就拥有了一个功能完整的单用户画布：绘图、文本、图片、视频、缩放、平移、复制粘贴、撤销重做——所有你期望的画布功能都开箱即用。

### 3. 添加本地持久化

```tsx
<Tldraw persistenceKey="my-project" />
```

一个 prop 搞定浏览器本地存储，刷新页面不丢数据，甚至能跨标签页同步。

### 4. 添加实时协作

```bash
npm install @tldraw/sync
```

```tsx
import { useSyncDemo } from '@tldraw/sync'

export default function App() {
  const store = useSyncDemo({ roomId: 'my-room' })
  return (
    <div style={{ position: 'fixed', inset: 0 }}>
      <Tldraw store={store} />
    </div>
  )
}
```

**10 行代码**，实时多人协作：实时光标、用户名、视角跟随、光标聊天。

## 核心功能深度解析

### 🎨 完整的白板工具集

tldraw 内置了一整套专业级白板工具：

- **绘图工具**：压感绘图、几何形状、文本、箭头
- **图片和视频**：拖拽上传、嵌入外部内容（YouTube、Figma、GitHub）
- **富文本**（2025 新增）：粗体、斜体、列表、链接、代码
- **智能箭头**：自动吸附、直角箭头、动态标签重排
- **网格对齐**：新建形状自动对齐网格
- **智能布局**：对齐、分布、翻转、堆叠，自动处理箭头连接

### 🤝 企业级实时协作

`@tldraw/sync` 提供了与 tldraw.com 相同架构的自托管协作方案：

- 基于 Cloudflare Durable Objects 的 WebSocket 连接
- 自动持久化和资产管理
- 实时光标、视角跟随、光标聊天
- 支持数十万并发协作会话

Multiplayer Starter Kit 提供了完整的生产级后端实现。

### 🔧 深度可定制

tldraw 的架构设计核心是可扩展性：

- **自定义形状**（Custom Shapes）：定义全新的形状类型，控制渲染、交互、序列化
- **自定义工具**（Custom Tools）：创建新的画布交互工具
- **自定义绑定**（Custom Bindings）：定义形状之间的关系
- **自定义 UI**：替换整个用户界面，或只修改特定组件
- **副作用和事件钩子**：监听画布变化，执行自定义逻辑

### 📡 强大的运行时 API

`Editor` 是 tldraw 的核心 API，提供完整的程序化控制：

```tsx
const handleMount = (editor: Editor) => {
  // 创建形状
  editor.createShape({
    type: 'text',
    x: 200, y: 200,
    props: { richText: toRichText('Hello world!') },
  })
  
  // 全选并缩放
  editor.selectAll()
  editor.zoomToSelection({ animation: { duration: 5000 } })
}
```

画布上发生的一切，都可以通过代码实现。

## 🤖 AI 集成：画布遇上大模型

这是 tldraw 最令人兴奋的部分。SDK 提供了三种 AI 集成模式：

### 模式一：画布作为 AI 输出

最简单的集成——把画布当作 AI 生成内容的展示面板。生成的图片、HTML 预览、交互式原型都可以作为形状放在画布上。

这就是著名的 **"Make Real"** 背后的原理：用户在画布上画一个 UI 草图，AI 生成可运行的 HTML/CSS 代码，实时预览在草图旁边。这个功能在 2023 年底一炮而红，被 Steve Ruiz（tldraw CEO）称为"意外的 AI 画布"。

### 模式二：可视化工作流

利用 tldraw 的绑定系统构建节点式可视化编程：

- 每个节点是一个自定义形状，有输入/输出端口
- 连接线是绑定关系，跟随节点移动
- 数据在节点间流动，AI 模型作为流水线的一环

**tldraw.computer** 就是基于这个模式构建的 AI 工作流应用——类似 ComfyUI，但以 tldraw 画布为基础。

### 模式三：AI Agent 画布操控

给 AI 模型完整的画布读写权限：

```tsx
const agent = useTldrawAgent(editor)

// AI 根据指令操作画布
agent.prompt('画一个用户认证流程图')
agent.prompt({
  message: '给这些形状添加标签',
  bounds: { x: 0, y: 0, w: 500, h: 400 },
})
```

Agent 通过截图 + 结构化形状数据双重方式理解画布状态，通过类型化动作 Schema 操作画布，内置对 LLM 常见错误的清洗和修正。

## 🚀 Starter Kits：从零到产品的加速器

SDK 4.0 推出了 6 个官方 Starter Kit，每个都是 MIT 许可：

| Kit | 用途 | 适用场景 |
|-----|------|---------|
| **Multiplayer** | 自托管实时协作 | 团队白板、协作文档 |
| **Workflow** | 可视化节点编辑器 | 自动化流水线、低代码平台 |
| **Chat** | AI 画布对话 | 带画图能力的 AI 聊天 |
| **Agent** | AI Agent 画布控制 | AI 辅助设计、自动生成图表 |
| **Image Pipeline** | AI 图片生成流水线 | Prompt 工程、批量生成 |
| **Branching Chat** | 分支对话树 | 对话设计、互动叙事 |

## 架构与技术设计

### DOM 渲染 vs Canvas 渲染

这是 tldraw 与许多竞品的根本区别。**tldraw 使用 DOM 树渲染**，而非 HTML Canvas。

**为什么选择 DOM？**

- 天然支持浏览器能渲染的一切：嵌入网页、视频、自定义 React 组件
- 无障碍访问：屏幕阅读器支持、键盘导航
- CSS 主题和暗色模式开箱即用
- 标准 Web 技术栈（TypeScript + React），开发者上手零门槛

**性能如何保证？**

- 高性能 Signals 库管理状态和变更
- OpenGL mini-map 处理需要高性能渲染的部分
- 完整的几何系统支持精确的碰撞检测

### 数据模型

tldraw 使用 Record Store（记录存储）作为核心数据层：

- 基于 Signals 的响应式状态管理
- 完整的事件跟踪和副作用系统
- 支持快照导出/导入
- 与 sync 层解耦，可以对接任意后端

## 谁在用 tldraw？

tldraw 的 SDK 已经被广泛采用：

- **ClickUp**：用 tldraw SDK 重构了其白板功能
- **Mobbin**：设计灵感平台
- **LegendKeeper**：世界构建工具
- **教育平台**：互动学习工具
- **企业工作流**：内嵌流程图和协作看板

从 50-300 人的 Series A-C 初创公司到大型企业，tldraw 正在成为"画布基础设施"的事实标准。

## 与竞品的对比

| 特性 | tldraw | Excalidraw | Konva | Fabric.js |
|------|--------|------------|-------|-----------|
| **定位** | 完整画布 SDK | 白板应用 | 2D Canvas 库 | Canvas 操作库 |
| **渲染方式** | DOM | HTML Canvas | HTML Canvas | HTML Canvas |
| **React 集成** | 原生 | 需包装 | React-Konva | 需包装 |
| **实时协作** | 内置 (@tldraw/sync) | 内置 | 无 | 无 |
| **自定义形状** | ✅ 一等公民 | 有限 | ✅ | ✅ |
| **AI 集成** | 官方支持+Starter Kit | 社区方案 | 无 | 无 |
| **无障碍** | 完整支持 | 基础 | 有限 | 有限 |
| **嵌入网页** | ✅ (iframe/React) | ❌ | ❌ | ❌ |
| **许可证** | tldraw License* | MIT | MIT | MIT |
| **GitHub Stars** | 45,500+ | 90,000+ | 12,000+ | 29,000+ |

*tldraw 开发免费，生产环境需付费许可。Starter Kits 为 MIT。

**怎么选？**

- **需要完整的画布应用基础设施**（协作、自定义形状、AI）→ **tldraw**
- **快速搭建一个简单白板**，纯开源 → **Excalidraw**
- **底层 2D 图形操作**，精确像素控制 → **Konva** 或 **Fabric.js**
- **需要嵌入浏览器内容**（网页、视频、React 组件）→ **tldraw**（DOM 渲染的优势）

## 许可证说明

这一点需要特别注意。tldraw 使用自定义的 **tldraw License**：

- **开发和学习**：完全免费
- **生产环境**：需要购买 license key
- **Starter Kits**：MIT 许可（完全自由）

这意味着如果你在商业产品中使用 tldraw SDK，需要联系他们获取商业许可。这是一个合理的商业模式——你获得了价值 500 万美元的研发成果，他们需要可持续的收入来持续维护。

## 2025 年的重大更新

- **SDK 4.0**：全新 Starter Kits、改进的无障碍功能
- **tldraw.com 账户系统**：登录、文件管理、协作权限控制
- **tldraw.computer**：AI 工作流应用
- **富文本支持**：粗体、斜体、列表、链接、代码
- **直角箭头**（即将发布）
- **40 种语言**本地化支持
- **智能布局**重写：自动处理箭头连接关系

## 为什么 tldraw 对开发者重要

1. **省时间**：tldraw 团队花了 3 年、500 万美元构建了数千个基础功能——从旋转光标到处理粘贴图片。你不需要重新发明轮子。

2. **AI 时代的画布**："Make Real" 证明了无限画布是 AI 交互的天然载体。当你需要构建"AI + 视觉"的产品时，tldraw 是目前最成熟的选择。

3. **生态效应**：45,000+ Stars、活跃的 Discord 社区、完善的文档和示例。你遇到的问题，大概率有人已经解决过。

4. **架构正确**：DOM 渲染的选择看似非主流，但在"画布即应用平台"的趋势下是明智的——你可以在画布上嵌入任何 Web 内容。

## 开始动手

```bash
# 最快的方式
npm create tldraw@latest

# 或者手动
npm install tldraw
```

- 📖 [快速上手指南](https://tldraw.dev/quick-start)
- 💡 [示例代码](https://tldraw.dev/examples)
- 🚀 [Starter Kits](https://tldraw.dev/starter-kits/overview)
- 🤖 [AI 集成文档](https://tldraw.dev/docs/ai)
- 💬 [Discord 社区](https://discord.tldraw.com)

如果你正在构建任何与"画布"相关的应用——无论是白板、流程图、AI 助手还是可视化编程工具——tldraw 值得你花一个下午认真了解。

---

*本文基于 tldraw SDK 4.0、官方文档和 GitHub 仓库信息撰写，数据截至 2026 年 3 月 2 日。*
