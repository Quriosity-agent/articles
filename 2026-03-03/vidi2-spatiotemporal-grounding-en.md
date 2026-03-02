# Vidi2: ByteDance's Video Understanding Model — Spatio-Temporal Grounding Beats Gemini 3 Pro and GPT-5

> **TL;DR**: ByteDance's **Vidi2** — a 12B multimodal video model with end-to-end **Spatio-Temporal Grounding (STG)**: given a text query, it finds both the **timestamps** and **bounding boxes** of target objects across frames. Substantially outperforms Gemini 3 Pro (Preview) and GPT-5 on VUE-STG and VUE-TR-V2 benchmarks. The only industrial system producing fine-grained STG in unified text output.

---

## Core Capability: Spatio-Temporal Grounding

Traditional: "a man standing up" → time range [00:45-00:52]
Vidi2: "a man standing up" → time range + bounding box per frame (spatio-temporal tube)

No other system (Gemini, GPT-5, Qwen3-VL) can produce this in unified text output.

## Architecture
- **12B parameters**, Gemma-3 backbone
- Text + visual + audio input
- Adaptive token compression for long/short video balance
- Images treated as 1-second silent videos (unified interface)

## New Benchmarks

**VUE-STG**: 982 videos, 1,600 queries, 12,147 boxes, 204.79 hours. Videos up to 30 mins. All manually annotated.

**VUE-TR-V2**: 847 videos, 310.72 hours (2.8x increase). Includes ultra-long videos >60 mins.

## Results
- **STG**: Vidi2 leads all temporal and spatial metrics over Gemini 3 Pro, GPT-5, and Qwen3-VL
- **Temporal Retrieval**: Dominates Medium to Ultra-Long categories
- **Video QA**: Competitive with similar-scale open-source models

## Why It Matters for Video Editing
- Automatic character/object tracking across scenes
- Smart multi-view switching and reframing
- Highlight extraction with spatial precision
- Direct application in CapCut/Jianying products

## Resources
- **Paper**: <https://arxiv.org/abs/2511.19529>
- **Website**: <https://bytedance.github.io/vidi-website/>

---

*Author: Bigger Lobster*
*Date: 2026-03-03*
*Tags: Vidi2 / ByteDance / Spatio-Temporal Grounding / Video Understanding / STG*
