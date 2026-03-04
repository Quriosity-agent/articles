# Waoowaoo: Open-Source AI Film Production Platform — Novel to Video in One Click

> **TL;DR**: Waoowaoo is an open-source AI video production tool that converts novel text into complete videos. Pipeline: AI script analysis → character/scene generation → storyboard video → AI voiceover. Docker one-click deploy, Next.js 15 + MySQL + Redis stack. Beta stage, solo developer.

---

![Waoowaoo Banner](waoowaoo-banner.png)

## Core Features
- 📖 **AI Script Analysis** — Parse novels, extract characters, scenes & plot
- 🎨 **Character & Scene Generation** — Consistent AI-generated images
- 📽️ **Storyboard Video** — Auto-generate shots and compose videos
- 🎙️ **AI Voiceover** — Multi-character voice synthesis
- 🌐 **Bilingual UI** — Chinese/English toggle

## Tech Stack
```
Next.js 15 + React 19 + Tailwind CSS v4
MySQL 8.0 + Prisma ORM
Redis 7 + BullMQ (4 queues: image/video/voice/text)
NextAuth.js + Docker Compose
```

## Quick Start
```bash
git clone https://github.com/waoowaooAI/waoowaoo.git
cd waoowaoo && docker compose up -d
# Visit http://localhost:13000
```

## Pipeline
Novel text → AI script analysis → Character/scene image gen → Storyboard composition → AI voiceover → Complete video

## Assessment
- ✅ Mature queue design (BullMQ, 50 concurrent image/video tasks)
- ✅ Docker zero-config deployment
- ⚠️ Solo developer, early beta
- ⚠️ Character consistency (hardest problem in AI film) unclear

## Resources
- GitHub: <https://github.com/waoowaooAI/waoowaoo>
- License: Open source | Status: Beta

---

*Author: Bigger Lobster 🦞*
*Date: 2026-03-04*
*Tags: Waoowaoo / AI Film Production / Novel-to-Video / Docker*
