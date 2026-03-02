# tldraw: The $5M Open-Source Infinite Canvas SDK That's Redefining How We Build Canvas Apps

> 45,000+ GitHub Stars, 3,000+ Forks, SDK 4.0 just shipped — tldraw isn't just a whiteboard tool, it's a complete infinite canvas infrastructure that lets developers build in days what used to take months.

## TL;DR

**tldraw** is an open-source infinite canvas SDK for React. Use it to build whiteboards, diagram editors, AI canvases, visual programming tools — anything that needs an infinite canvas interaction model. It's not another drawing library; it's a complete canvas infrastructure with real-time collaboration, custom shapes, a plugin system, and first-class AI integration.

- 🔗 Website: [tldraw.dev](https://tldraw.dev)
- 📦 GitHub: [github.com/tldraw/tldraw](https://github.com/tldraw/tldraw) (45,500+ ⭐)
- 📄 License: tldraw License (free for development, production requires a key)
- 💰 Funding: $5M+ raised, led by CEO Steve Ruiz
- 🏗️ Stack: TypeScript, React, DOM rendering

## Five-Minute Quick Start

The developer experience is remarkably smooth. Zero to a fully functional canvas app in three steps:

### 1. Scaffold a Project

```bash
npm create tldraw@latest
```

This interactive CLI walks you through starter kit selection and scaffolds a complete project.

### 2. Manual Integration

Already have a React project? Two commands:

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

**That's it.** Three lines of core code gives you a fully-featured single-user canvas: drawing, text, images, video, zoom, pan, copy/paste, undo/redo — everything you'd expect, out of the box.

### 3. Add Local Persistence

```tsx
<Tldraw persistenceKey="my-project" />
```

One prop enables browser-local storage. Survives page refreshes, even syncs across tabs sharing the same key.

### 4. Add Real-Time Collaboration

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

**10 lines of code** for live multiplayer: real-time cursors, user names, viewport following, cursor chat.

## Core Features In Depth

### 🎨 Production-Ready Whiteboard Toolkit

tldraw ships with a complete professional whiteboard tool set:

- **Drawing**: Pressure-sensitive freehand, geometric shapes, text, arrows
- **Media**: Drag-and-drop images/video, embedded content (YouTube, Figma, GitHub)
- **Rich Text** (new in 2025): Bold, italic, lists, links, code blocks
- **Smart Arrows**: Shape snapping, right-angle routing, dynamic label rewrapping
- **Grid Snapping**: New shapes auto-snap when grid mode is enabled
- **Smart Layout**: Alignment, distribution, flipping, stacking — all arrow-aware

### 🤝 Enterprise-Grade Real-Time Collaboration

`@tldraw/sync` provides the same architecture that powers tldraw.com:

- WebSocket connections via Cloudflare Durable Objects
- Automatic persistence and asset management
- Live cursors, viewport following, cursor chat
- Scales to hundreds of thousands of concurrent collaborative sessions
- Full Multiplayer Starter Kit with production-ready backend

### 🔧 Deep Customization

Extensibility is an architectural first principle:

- **Custom Shapes**: Define entirely new shape types — control rendering, interaction, serialization
- **Custom Tools**: Create new canvas interaction tools
- **Custom Bindings**: Define relationships between shapes
- **Custom UI**: Replace the entire interface, or swap individual components
- **Side Effects & Event Hooks**: React to canvas changes with custom logic

### 📡 Powerful Runtime API

The `Editor` is tldraw's central API for programmatic control:

```tsx
const handleMount = (editor: Editor) => {
  editor.createShape({
    type: 'text',
    x: 200, y: 200,
    props: { richText: toRichText('Hello world!') },
  })
  
  editor.selectAll()
  editor.zoomToSelection({ animation: { duration: 5000 } })
}
```

Everything that can happen on the canvas can be done through code.

## 🤖 AI Integration: Where Canvas Meets LLMs

This is where tldraw gets genuinely exciting. The SDK provides three patterns for AI integration:

### Pattern 1: Canvas as AI Output

The simplest approach — use the canvas as a display surface for AI-generated content. Generated images, HTML previews, and interactive prototypes become shapes on the canvas.

This is the principle behind the famous **"Make Real"** feature: users sketch a UI on the canvas, an AI generates working HTML/CSS, and a live preview appears alongside the original drawing. This went viral in late 2023 and was described by Steve Ruiz (tldraw CEO) as "the accidental AI canvas."

### Pattern 2: Visual Workflows

Build node-based visual programming using tldraw's binding system:

- Each node is a custom shape with input/output ports
- Connections are bindings that follow nodes as they move
- Data flows through the pipeline, with AI models as processing steps

**tldraw.computer** is built on this pattern — think ComfyUI, but powered by the tldraw canvas.

### Pattern 3: AI Agents with Canvas Control

Give AI models full read/write access to the canvas:

```tsx
const agent = useTldrawAgent(editor)

agent.prompt('Draw a flowchart showing user authentication')
agent.prompt({
  message: 'Add labels to these shapes',
  bounds: { x: 0, y: 0, w: 500, h: 400 },
})
```

Agents understand the canvas through dual context — screenshots plus structured shape data. They manipulate shapes through typed action schemas with built-in sanitization for common LLM mistakes (non-existent IDs, duplicate IDs, off-target coordinates).

## 🚀 Starter Kits: From Zero to Product

SDK 4.0 ships with 6 official Starter Kits, all MIT-licensed:

| Kit | Purpose | Use Cases |
|-----|---------|-----------|
| **Multiplayer** | Self-hosted real-time collaboration | Team whiteboards, collaborative docs |
| **Workflow** | Visual node editor | Automation pipelines, no-code platforms |
| **Chat** | AI canvas conversation | Sketch-augmented AI chat |
| **Agent** | AI agent canvas control | AI-assisted design, auto-generated diagrams |
| **Image Pipeline** | AI image generation pipelines | Prompt engineering, batch generation |
| **Branching Chat** | Branching conversation tree | Conversation design, interactive storytelling |

## Architecture & Technical Design

### DOM Rendering vs Canvas Rendering

This is the fundamental architectural difference between tldraw and most competitors. **tldraw renders to a DOM tree**, not an HTML Canvas element.

**Why DOM?**

- Natively supports anything the browser can render: embedded websites, video, custom React components
- Accessibility baked in: screen readers, keyboard navigation
- CSS theming and dark mode out of the box
- Standard web tech stack (TypeScript + React) — zero learning curve for web developers

**What about performance?**

- High-performance Signals library for state management and change tracking
- OpenGL mini-map for parts that need fast rendering
- Complete geometry system for precise hit-testing
- Handles large canvases through viewport culling and smart rendering

### Data Model

tldraw uses a Record Store as its core data layer:

- Signals-based reactive state management
- Complete event tracking and side-effect system
- Snapshot export/import
- Decoupled from the sync layer — plug in any backend

## Who's Using tldraw?

The SDK is seeing broad adoption:

- **ClickUp**: Modernized their whiteboard feature using tldraw SDK
- **Mobbin**: Design inspiration platform
- **LegendKeeper**: World-building tool using tldraw as core canvas infrastructure
- **Educational platforms**: Interactive learning tools
- **Enterprise workflow tools**: Embedded diagramming and collaborative boards

The sweet spot is Series A-C startups (50-300 people) through large enterprises that need embedded canvas functionality.

## Comparison with Alternatives

| Feature | tldraw | Excalidraw | Konva | Fabric.js |
|---------|--------|------------|-------|-----------|
| **Focus** | Complete canvas SDK | Whiteboard app | 2D canvas library | Canvas manipulation |
| **Rendering** | DOM | HTML Canvas | HTML Canvas | HTML Canvas |
| **React Integration** | Native | Wrapper needed | React-Konva | Wrapper needed |
| **Real-time Collab** | Built-in (@tldraw/sync) | Built-in | None | None |
| **Custom Shapes** | First-class citizen | Limited | ✅ | ✅ |
| **AI Integration** | Official support + kits | Community | None | None |
| **Accessibility** | Comprehensive | Basic | Limited | Limited |
| **Web Embeds** | ✅ (iframe/React) | ❌ | ❌ | ❌ |
| **License** | tldraw License* | MIT | MIT | MIT |
| **GitHub Stars** | 45,500+ | 90,000+ | 12,000+ | 29,000+ |

*tldraw is free for development; production use requires a paid license. Starter Kits are MIT.

**How to choose:**

- **Need complete canvas app infrastructure** (collab, custom shapes, AI) → **tldraw**
- **Quick simple whiteboard**, pure open-source → **Excalidraw**
- **Low-level 2D graphics**, pixel-precise control → **Konva** or **Fabric.js**
- **Need to embed web content** (pages, video, React components) → **tldraw** (DOM rendering advantage)

## Licensing

An important note. tldraw uses a custom **tldraw License**:

- **Development and learning**: Completely free
- **Production use**: Requires a license key (paid)
- **Starter Kits**: MIT licensed (fully permissive)

This is a fair commercial model. You're getting $5M+ of R&D, and they need sustainable revenue to maintain it. Contact [tldraw.dev](https://tldraw.dev) for production licensing.

## Major Updates in 2025

- **SDK 4.0**: New Starter Kits, improved accessibility features
- **tldraw.com accounts**: Login, file management, collaboration permissions, public/private sharing
- **tldraw.computer**: AI workflow application
- **Rich text**: Bold, italic, lists, links, code in all text shapes
- **Right-angle arrows** (shipping soon)
- **40 languages** localization support
- **Smart layout rewrite**: Arrow-aware alignment and distribution

## Why tldraw Matters for Developers

1. **Time savings**: The tldraw team spent 3 years and $5M building thousands of table-stakes features — from rotating cursors to handling pasted images. You don't need to reinvent the wheel.

2. **AI-native canvas**: "Make Real" proved that the infinite canvas is a natural medium for AI interaction. When building "AI + visual" products, tldraw is the most mature option available.

3. **Ecosystem momentum**: 45,000+ Stars, active Discord community, comprehensive docs and examples. Whatever problem you hit, someone has probably solved it.

4. **Architecturally sound**: DOM rendering seems unconventional, but in the "canvas as application platform" trend, it's the right call — you can embed any web content on the canvas.

5. **Starter Kits as blueprints**: The new kits aren't just demos. They're production-grade reference implementations for common canvas patterns (workflow builders, AI agents, chat).

## Get Started

```bash
# Fastest way
npm create tldraw@latest

# Manual
npm install tldraw
```

- 📖 [Quick Start Guide](https://tldraw.dev/quick-start)
- 💡 [Examples](https://tldraw.dev/examples)
- 🚀 [Starter Kits](https://tldraw.dev/starter-kits/overview)
- 🤖 [AI Integration Docs](https://tldraw.dev/docs/ai)
- 💬 [Discord Community](https://discord.tldraw.com)

If you're building anything canvas-related — whiteboards, diagrams, AI assistants, visual programming tools — tldraw deserves a serious afternoon of your time. The gap between "let me build this from scratch" and "let me customize tldraw" is measured in months.

---

*This article is based on tldraw SDK 4.0, official documentation, and GitHub repository data as of March 2, 2026.*
