# Jellyfish: An Open-Source AI Short Drama Factory — From Script to Final Cut

> Repo: [donghaozhang/Jellyfish](https://github.com/donghaozhang/Jellyfish) · License: Apache-2.0 · Stack: React 18 + TypeScript + Vite + Multi-model API

## What Is It

Jellyfish is a **one-stop AI short drama production tool** (vertical/micro short dramas). It tackles the biggest pain point in AI video generation: **character and scene drift** — where the same character looks different across shots.

The complete pipeline:

```
Script Input → Smart Storyboarding → Character/Scene/Prop Consistency Management → AI Video Generation → Post-Production Editing → One-Click Export
```

![Jellyfish Project Overview](https://raw.githubusercontent.com/donghaozhang/Jellyfish/main/docs/img/project.png)
*Image source: [donghaozhang/Jellyfish](https://github.com/donghaozhang/Jellyfish) project screenshot*

## Why It Matters

### 1. Consistency Is the Core Value Proposition

AI video generation's #1 problem is consistency. Jellyfish attacks it with three mechanisms:

- **Global seed anti-drift**: Project-level seed locking, all storyboard shots inherit the same style
- **Dual-layer asset system**: Project assets + global assets — full lifecycle management for characters, scenes, props, costumes
- **Cross-shot reference**: Reference images can be reused across storyboard shots, ControlNet skeleton/depth for action control

### 2. Industrial Production Pipeline

This isn't a toy — it's designed as a production line:

| Module | What It Does |
|--------|-------------|
| **Chapter Shooting Workbench** | Script → smart condensation → storyboard extraction → editing → video gen → preview |
| **Fine-Grained Shot Control** | Shot size/angle/camera movement/mood/duration/atmosphere, independent prompts for first/last/key frames |
| **Advanced Generation Control** | ControlNet skeleton/depth, smart lip-sync, multi-model switching |
| **Video Post-Production** | Timeline editing, multi-track, asset library drag-and-drop, final export |
| **Agent Workflow** | Dify-like node-based orchestration — plot extraction, character extraction, storyboard suggestions |
| **Model Management** | OpenAI/Claude/Tongyi/Hunyuan/Midjourney/Runway/Kling/Luma multi-vendor |

### 3. Agent Workflow Editor

The most interesting part. Jellyfish includes a **Dify-like node-based workflow editor** (built on React Flow) where you can customize Agents for:

- Automatic plot extraction
- Character identification and description generation
- Storyboard suggestions and prompt auto-fill

This means you can orchestrate the entire short drama production pipeline into an automated workflow.

## Architecture Breakdown

```
Frontend: React 18 + TypeScript + Vite
├── UI: Ant Design + Tailwind CSS
├── State: Redux Toolkit / Zustand
├── Workflow: React Flow (node-based orchestration)
├── Player: Video.js / Plyr
└── Editor: Monaco Editor / React Quill

Backend (optional): Node.js / NestJS / FastAPI / Spring Boot
├── OpenAPI auto-generates frontend request code
└── pnpm run openapi:update for one-click sync

AI Layer: Multi-model API integration
├── Text: OpenAI / Anthropic / Tongyi / Hunyuan
├── Image: Midjourney / DALL-E
└── Video: Runway / Kling / Luma
```

Notable: frontend request functions and type definitions are **auto-generated** from the backend OpenAPI spec (`front/src/services/generated/`). Good practice — prevents frontend-backend interface drift.

## Development Status

The project is under active development. Completed so far:

- ✅ Model management (multi-vendor, multi-type, default configuration)
- ✅ Project management (CRUD, global style and seed)
- ✅ Project workbench and chapter shooting workbench interaction layer

In progress:

- 🚧 Complete storyboard editing + video generation + preview pipeline
- 🚧 Advanced prompt templates with smart fill

## Builder's Perspective: What Can You Take Away

**If you're building AI video products**, Jellyfish's architecture is worth studying:

1. **Asset consistency approach**: Global seed + dual-layer asset library addresses the hardest problem in AI-generated content
2. **Agent workflow**: Decomposing video production into orchestratable nodes — this pattern applies to any AI content production scenario
3. **Multi-model switching layer**: Managing 6+ video/image/text models simultaneously is a non-trivial architecture challenge with reusable patterns
4. **OpenAPI frontend-backend sync**: Auto-generating frontend types and request code prevents interface drift

**Best suited for:**
- Short drama / micro-drama batch production
- AI film studios
- Educational / training video creation
- Brand / e-commerce product promotional clips

## Comparison with Similar Projects

Compared to projects we've previously analyzed:

- **vs Omniclip**: Omniclip is a general-purpose browser-based video editor; Jellyfish focuses on the AI short drama production pipeline
- **vs LTX-Desktop**: LTX is a desktop AI video generator; Jellyfish adds the complete script → storyboard → editing chain
- **vs FunCineForge**: FunCineForge does AI movie dubbing; Jellyfish does end-to-end AI short drama production

Jellyfish's differentiation: **vertically deep in the short drama vertical**, especially consistency management and industrial pipeline design.

## Bottom Line

Jellyfish tackles AI video generation's hardest problem — consistency — while building an industrial production pipeline for short dramas. Though still in early development, the architecture is well-thought-out. The combination of asset management + Agent workflows + multi-model switching has serious potential.

For builders working on AI video products, this project's architectural patterns are more valuable than the code itself.

🦞
