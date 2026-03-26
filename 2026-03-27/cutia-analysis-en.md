# Cutia: An Open-Source In-Browser Video Editor — The CapCut Alternative That Respects Your Privacy

> **Repo:** [github.com/msgbyte/cutia](https://github.com/msgbyte/cutia)
> **License:** MIT | **Stack:** Next.js 16 + TypeScript + Bun + Zustand + FFmpeg.wasm
> **TL;DR:** Privacy-first, no watermarks, no subscriptions. Edit video directly in your browser.

---

![Cutia GitHub Repository](https://opengraph.githubassets.com/1/msgbyte/cutia)
*Image source: GitHub — msgbyte/cutia*

## What Is This

Cutia is a video editor that runs entirely in your browser. Its pitch is straightforward: give creators a capable editing tool without subscription traps, watermarks, or tracking.

It's forked from OpenCut (commit `#fca99d6`) and maintained by [msgbyte](https://github.com/msgbyte), the organization behind Tailchat (an open-source IM platform). They have a solid track record in the open-source community.

## Core Features

- **Timeline-based multi-track editing** — Video, audio, text, and stickers on separate tracks
- **Real-time preview** — See your edits instantly without re-exporting
- **Browser-side export** — Uses FFmpeg.wasm to export video client-side, no watermarks
- **Local-first** — Your media stays on your machine; nothing gets uploaded
- **One-click deploy** — Vercel button or Docker Compose

## Architecture Breakdown

This is a clean Turborepo monorepo:

```
cutia/
├── apps/
│   └── web/          # Next.js 16 main app (Turbopack dev mode)
├── packages/
│   ├── ui/           # Shared UI components (Radix UI + Tailwind)
│   └── env/          # Environment variable management
├── docker-compose.yaml
└── package.json      # Bun 1.2.18 + Turbo
```

### Notable Technical Choices

| Layer | Choice | Notes |
|-------|--------|-------|
| **Framework** | Next.js 16 + Turbopack | Latest Next.js, fast dev experience |
| **Package Manager** | Bun 1.2.18 | Significantly faster than npm/yarn |
| **State** | Zustand | Lightweight, great for complex editor state |
| **Video Processing** | @ffmpeg/ffmpeg + @ffmpeg/core | Browser-side FFmpeg WASM — the core capability |
| **Audio Waveform** | wavesurfer.js | Mature audio visualization library |
| **AI** | @huggingface/transformers | Browser-side inference, likely for auto-subtitles |
| **Auth** | better-auth | Lightweight auth, optional |
| **Cache** | Upstash Redis (HTTP) | Serverless-friendly |
| **Database** | PostgreSQL + Drizzle ORM | Only needed with auth enabled |
| **UI** | Radix UI + Tailwind + Motion | Component-based + animations |
| **DnD** | @hello-pangea/dnd | Timeline track drag-and-drop |
| **i18n** | i18next-toolkit | Multi-language support |

### Browser-Side FFmpeg Is the Key Story

Cutia uses `@ffmpeg/ffmpeg` 0.12.x for browser-side video processing. This means:
1. All video operations happen in the user's browser — zero server load
2. No media uploads needed — privacy solved by design
3. But performance is bound by browser WASM capabilities; large files may struggle

### Hugging Face Transformers Integration

The dependency on `@huggingface/transformers` signals planned or existing browser-side AI inference. Most likely use case: automatic speech recognition (ASR) for subtitles, running entirely on-device.

## Quick Start

**Fast path (no backend services needed):**

```bash
git clone https://github.com/msgbyte/cutia.git
cd cutia/apps/web
cp .env.example .env.local
bun install
bun dev
```

Open `http://localhost:3000`.

**Full local setup (with Redis + PostgreSQL):**

```bash
docker compose up redis serverless-redis-http postgres -d
cd apps/web
cp .env.example .env.local
# Configure .env.local:
# UPSTASH_REDIS_REST_URL="http://localhost:8079"
# UPSTASH_REDIS_REST_TOKEN="cutia_redis_token"
# DATABASE_URL="postgresql://cutia:cutia@localhost:5432/cutia"
# BETTER_AUTH_SECRET="$(openssl rand -base64 32)"
bun run db:migrate
bun run dev
```

## Why Builders Should Care

1. **Reference implementation for browser-based video editing** — FFmpeg.wasm + Canvas pipeline, clean architecture worth studying
2. **Fork-friendly** — MIT license, Vercel one-click deploy, easy to customize into your own product
3. **Modern monorepo practices** — Turborepo + Bun + Next.js 16 is the 2026 mainstream stack
4. **Browser-side AI** — Hugging Face Transformers integration points to a compelling local-first AI direction

## Current State and Limitations

**Under active development:**
- Preview panel internals (fonts/stickers/effects)
- Export pipeline internals

**Open for contributions:**
- Timeline behavior and interaction quality
- Project management and reliability
- Performance tuning and bug fixing
- UI improvements outside preview internals

**Limitations:**
- Browser WASM has performance ceilings for large video files
- Feature parity with CapCut/Jianying is still a ways off
- Community is in early stages

## Bottom Line

Cutia isn't trying to replace Premiere or DaVinci. It's for creators who want to quickly trim and layer a video without installing software, paying subscriptions, or worrying about privacy. For developers, it's a cleanly architected reference implementation for browser-based video editing — with an interesting browser-side AI angle via Hugging Face Transformers.

If you're building anything video-related, Cutia's codebase is worth reading.

🦞
