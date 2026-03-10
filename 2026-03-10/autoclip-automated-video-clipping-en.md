# AutoClip: AI-Powered Video Clipping and Highlight Generation

> Repository: https://github.com/zhouxiaoka/autoclip

## What Is It?

AutoClip is an open-source AI video clipping system that automatically extracts highlights from long-form videos and generates short-form compilations. It supports downloading from YouTube and Bilibili (B站), analyzes content using large language models (Alibaba's Qwen/Tongyi Qianwen), identifies the best moments, and cuts them into standalone clips.

Think of it as: paste a 2-hour livestream URL → get a dozen polished highlight clips. Very useful for content repurposing and "secondary creation" (二创) workflows.

## Core Features

- **Multi-platform video ingestion**: YouTube, Bilibili URL parsing + download, local file upload
- **AI content analysis**: Uses Qwen (Tongyi Qianwen) LLM for video content understanding and outline extraction
- **Smart clipping**: Automatically identifies topic timestamps, scores each segment for "highlight-worthiness", generates clips
- **Collection generation**: AI-recommended video compilations with drag-and-drop reordering
- **Real-time progress**: WebSocket-based live progress updates and task monitoring
- **Bilibili upload** (in development): Planned auto-upload of clips to Bilibili
- **Subtitle editing** (in development): Visual subtitle editor with sync capabilities

## Architecture

AutoClip uses a modern decoupled frontend/backend architecture:

**Backend:**
- FastAPI (Python web framework)
- Celery + Redis (async task queue)
- SQLite (lightweight DB, upgradable to PostgreSQL)
- yt-dlp (video downloading)
- FFmpeg (video processing)
- Qwen / DashScope API (AI analysis)

**Frontend:**
- React 18 + TypeScript
- Ant Design (UI component library)
- Vite (build tool)
- Zustand (state management)

**Deployment:**
- Docker + Docker Compose for one-click setup
- Manual installation also supported (Python venv + npm)

## The Processing Pipeline

AutoClip processes videos through a multi-step pipeline:

1. **Material preparation**: Download video and subtitle files
2. **Content analysis**: AI extracts video outline and key information
3. **Timeline extraction**: Identify topic time ranges
4. **Highlight scoring**: AI scores each segment
5. **Title generation**: Generate engaging titles for highlights
6. **Collection recommendation**: AI suggests compilation groupings
7. **Video generation**: FFmpeg cuts the final clips

Each step maps to a dedicated module (`step1_outline.py`, `step2_timeline.py`, `step3_scoring.py`, `step6_video.py`). The design philosophy is clear: understand first, decide second, execute last.

## Relevance to QCut

As a project closely related to our QCut video editor, AutoClip offers several interesting parallels:

- **AI Pipeline design**: AutoClip's multi-step processing pipeline (outline → timeline → scoring → generation) mirrors QCut's native CLI pipeline approach — both decompose complex video processing into composable steps
- **LLM-driven content understanding**: AutoClip uses Qwen to analyze subtitles for content comprehension, aligning with QCut's AI-powered video analysis direction
- **Subtitles as the bridge**: Both projects recognize that subtitle/transcript text is the critical bridge between "language understanding" and "video editing"
- **Automation vs. control**: AutoClip leans fully automatic (input URL → output clips), while QCut emphasizes editor control. Both approaches have their place

**Key differences:**
- AutoClip targets content repurposing/batch workflows; QCut is a creator-facing editor
- AutoClip depends on Alibaba Cloud's Qwen API; QCut supports multiple AI backends
- AutoClip's frontend is a standalone web app; QCut is a desktop editor

## Use Cases

- Content repurposing: Extract highlights from long videos for short-form content
- Content operations: Batch process podcasts, interviews, livestream replays
- Video archiving: Auto-organize and categorize video content
- Study notes: Extract key segments from lecture recordings

## Quick Start

```bash
# One-click Docker setup
git clone https://github.com/zhouxiaoka/autoclip.git
cd autoclip
cp env.example .env
# Edit .env with your Qwen/DashScope API key
docker-compose up -d
```

Access `http://localhost:3000` after startup.

## Summary

AutoClip solves a practical problem: automated long-form video clipping. Its tech stack is modern, architecture is clean, and deployment is straightforward. While some features are still in development (Bilibili upload, subtitle editing), the core "download → analyze → clip → compile" pipeline is fully functional.

For content repurposers, it's a tool worth watching. For those of us building QCut, AutoClip's AI pipeline design and subtitle analysis approach offer valuable reference points.

---

🦞
