# Qwen3-VL: Alibaba's Most Powerful Open-Source Vision-Language Model

**Source: qwen.ai | September 22, 2025**

---

## TL;DR

Alibaba's Qwen team releases Qwen3-VL — the most powerful vision-language model in the Qwen family. The flagship 235B-A22B is fully open-sourced. The Instruct version matches or exceeds Gemini 2.5 Pro and GPT-5 on most visual benchmarks. The Thinking version sets SOTA on multiple multimodal reasoning tasks. Native 256K context, expandable to 1M tokens (~2 hours of video).

---

## 12 Core Capabilities

| # | Capability | Highlight |
|---|-----------|-----------|
| 1 | **Visual Agent** | Operates phones/computers — opens apps, clicks buttons, fills forms. Top on OS World |
| 2 | **Think with Images** | Combines visual details + tools for complex reasoning |
| 3 | **Visual Coding** | Sketch → HTML/CSS/JS, design mockup → code. WYSIWYG programming |
| 4 | **Spatial Understanding** | 2D grounding (relative coords) + 3D bounding boxes. Foundation for robotics |
| 5 | **Long Context** | Native 256K, expandable to **1M tokens** (~2hr video). 99.5% accuracy at 1M |
| 6 | **Multimodal Reasoning** | STEM deep reasoning. HMMT Feb 25: 98.0 (vs Gemini 3 Pro 97.5) |
| 7 | **Universal Recognition** | Celebrities, anime characters, products, landmarks, animals, plants |
| 8 | **32-Language OCR** | Up from 10 languages. Works in poor lighting, blur, tilted text |
| 9 | **Creative Writing** | Image/video → stories, social media copy, scripts |
| 10 | **Complex Instruction Following** | Multi-step, conditional, structured instructions |
| 11 | **Multi-Image Dialogue** | Compare, connect, maintain context across turns |
| 12 | **Video Understanding** | Precise temporal grounding, 1.5+ hour videos, gameplay → code |

---

## Benchmark Highlights

| Benchmark | Qwen3-VL-Thinking | GPT-5.2-Thinking | Gemini 3 Pro | Claude-Opus-4.5 |
|-----------|-------------------|------------------|-------------|-----------------|
| HMMT Feb 25 | **98.0** | 99.4 | 97.5 | — |
| C-Eval | **93.7** | 90.5 | 93.4 | 92.2 |
| Arena-Hard v2 | **90.2** | 80.6 | 81.7 | 76.7 |
| MultiChallenge | **63.3** | 57.9 | 64.2 | 54.2 |
| HLE (w/ tools) | **49.8** | 45.5 | 45.8 | 43.2 |
| LiveCodeBench v6 | 85.9 | 87.7 | **90.7** | 84.8 |
| SWE Verified | 75.3 | 80.0 | 76.2 | **80.9** |

Outperforms closed-source flagships on multiple dimensions — especially in instruction following (Arena-Hard v2: 90.2) and agentic search (HLE w/ tools: 49.8).

---

## Architecture Innovations

### 1. Interleaved-MRoPE
Original MRoPE concentrated temporal information in high-frequency dimensions. Qwen3-VL interleaves time/height/width across all frequency bands — dramatically improving long video comprehension.

### 2. DeepStack
Instead of injecting visual tokens into a single LLM layer, Qwen3-VL injects them across **multiple layers**. Visual features from different ViT layers are tokenized separately, preserving low-to-high level visual information.

### 3. Text-Timestamp Alignment
Interleaved "timestamp-video frame" input format enables fine-grained alignment between temporal information and visual content. Native support for both seconds and HMS time formats.

---

## Claude Code Compatible!

Qwen3-VL's API supports the Anthropic protocol, meaning you can drive Claude Code directly:

```bash
npm install -g @anthropic-ai/claude-code
export ANTHROPIC_MODEL="qwen3-max-2026-01-23"
export ANTHROPIC_BASE_URL=https://dashscope.aliyuncs.com/apps/anthropic
export ANTHROPIC_AUTH_TOKEN=your-api-key
claude
```

---

## Open-Source Model Lineup

| Model | Type | Context |
|-------|------|---------|
| Qwen3-VL-235B-A22B-Instruct | Non-reasoning | 256K (expandable to 1M) |
| Qwen3-VL-235B-A22B-Thinking | Reasoning | 256K (expandable to 1M) |

Both available on Hugging Face, ModelScope, and via Alibaba Cloud API.

---

## Why This Matters

1. **Open-source matching closed-source** — 235B beats Gemini 2.5 Pro and GPT-5 on many benchmarks
2. **True multimodal** — Not just "seeing" but understanding, reasoning, acting, and coding
3. **1M context** — Feed 2 hours of video at once, 99.5% accuracy
4. **32-language OCR** — Practical global utility
5. **Visual Agent** — Operating phones and computers autonomously
6. **Text parity** — Language performance matches Qwen3-235B (text-only flagship)

This is arguably the most capable open-source multimodal model available today.

---

*Original: <https://qwen.ai/blog?id=99f0335c4ad9ff6153e517418d48535ab6d8afef>*
*Article compiled from Qwen official blog.*
