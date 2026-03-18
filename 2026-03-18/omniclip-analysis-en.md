# Omniclip: A Fully Browser-Based Open Source Video Editor — Architecture Deep Dive

> **Repo:** [omni-media/omniclip](https://github.com/omni-media/omniclip) · ⭐ 1.3k+ · MIT · TypeScript  
> **TL;DR:** No backend, no accounts, no file uploads — a pure client-side video editor that also ships as embeddable Web Components.

![Omniclip Logo](https://raw.githubusercontent.com/omni-media/omniclip/main/assets/icon2.png)
*Source: omni-media/omniclip repository (MIT License)*

---

## What It Does

Omniclip is an open source web video editor. Trimming, splitting, text overlays, filters, transitions, export — all running locally in your browser. No server, no uploads, your media never leaves your machine.

Key selling points:
- **Runs entirely in-browser**, leveraging the WebCodecs API for hardware-accelerated decode/encode
- **Zero backend** — project data stored in localStorage + OPFS (Origin Private File System)
- **Embeddable** — `npm install omniclip`, register the custom elements, done
- **Real-time collaboration** via WebRTC (peer-to-peer, no relay server)

## Tech Stack Breakdown

| Layer | Technology | Purpose |
|---|---|---|
| UI Framework | `@benev/slate` + `lit` | Lightweight Web Components UI layer |
| Rendering | `pixi.js` v7 | 2D WebGL canvas — compositing, filters, transitions |
| Video Decode | `WebCodecs` + `web-demuxer` + `mp4box` | Native browser hardware decoding (no WASM for playback) |
| Video Export | `@ffmpeg/ffmpeg` (WASM) | Encoding via ffmpeg compiled to WebAssembly |
| Audio Waveform | `wavesurfer.js` | Timeline audio visualization |
| Transitions | `gl-transitions` + `gsap` | GL-based transition shaders + GSAP animation engine |
| Collaboration | `sparrow-rtc` | P2P WebRTC — no server relay needed |
| Storage | `opfs-tools` + `localStorage` | Project persistence without a backend |

## Architecture: Unidirectional Data Flow

Omniclip follows a classic **unidirectional data flow** pattern (think Redux/Flux):

```
Actions → State → Controllers → Components/Views
   ↑                                    |
   └────────────────────────────────────┘
```

The core lives in `s/context/`:

- **State** (`state.ts`): Split into `historical_state` (undo/redo-capable) and `non_historical_state` (ephemeral things like playhead position)
- **Actions** (`actions.ts`): All mutations go through typed actions
- **Controllers**: `Timeline`, `Compositor`, `Media`, `VideoExport`, `Shortcuts`, `Collaboration` — each owns a domain
- **AppCore** (from `@benev/slate`): Provides the history stack for undo/redo

This architecture is **collaboration-friendly by design** — actions can be serialized and broadcast via WebRTC, keeping state trees in sync across peers.

## Storage Design

The persistence strategy is worth noting:

```typescript
// Projects saved to localStorage, indexed by projectId
this.#store[state.projectId] = {
  projectName, projectId, effects, tracks,
  filters, animations, transitions
}
```

- **Project metadata**: localStorage (fast, simple)
- **Media files**: OPFS (browser's private filesystem — large capacity, not user-accessible)
- **Collaboration mode skips local saves** to avoid state conflicts between peers

## Web Component Embedding

This is where Omniclip becomes most interesting for product builders. Three lines to embed a video editor in any web app:

```javascript
import { getComponents, registerElements } from 'omniclip'
registerElements(getComponents())
```

```html
<omni-text></omni-text>
<omni-media></omni-media>
<omni-timeline></omni-timeline>
```

You can use individual components (just the timeline, for example) or all of them. This is immediately useful for content creation platforms, education tools, or any product that needs "embed video editing" capabilities.

## Notable Limitations

- **WebCodecs compatibility**: Older browsers won't work; Safari support is still catching up
- **No audio editing**: Volume control and audio trimming are still on the roadmap
- **No keyframe animation**: Property animations don't support keyframe curves yet
- **Large file performance**: Pure browser-based processing of 4K long-form video will struggle

## Takeaways for Builders

1. **WebCodecs is production-ready** — Browser-native video decoding is now sufficient for a video editor; you don't need to lean entirely on ffmpeg WASM
2. **OPFS is underrated** — The browser's "local filesystem" handles large files better than IndexedDB, and most developers haven't heard of it
3. **Web Components as a distribution model** — Packaging an entire editor as custom elements means any framework (React/Vue/Svelte/vanilla) can consume it
4. **P2P collaboration without infrastructure** — `sparrow-rtc` proves that browser-to-browser real-time editing is viable without relay servers

## What's Coming in 2.0

Omniclip 2.0 is in active development, paired with [Omni Tools](https://github.com/omni-media/omnitool) — a programmatic engine for building timelines from code, automating renders, and integrating with AI/scripting workflows. This opens the door to script-generated or AI-driven video production without touching a GUI.

---

**Repository:** https://github.com/omni-media/omniclip  
**Live Demo:** Deployed on Netlify — open and start editing  
**License:** MIT

🦞
