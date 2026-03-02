# Qwen3-VL Explicit Video Timestamps: Why Text Tokens Beat Position Encoding for Temporal Alignment

> **TL;DR**: Qwen3-VL replaces Qwen2.5-VL's position-encoding-based temporal alignment with **plain text timestamp tokens** like `<3.0s>`. Trades a small context length increase for dramatically better long video temporal grounding. Core insight: **LLMs are best at text — so encode time as text.**

---

## The Problem with Position-Encoding Time

Qwen2.5-VL used **Temporal-Synchronized MRoPE**: position IDs directly bound to absolute time. Two issues:

**1. Long video position ID explosion**: A 2-hour video needs IDs up to 720,000 — far beyond training distribution, causing poor extrapolation.

**2. Training data cost**: Need uniform sampling across multiple frame rates to cover all time-position mappings.

## The Fix: Just Write the Time

```
Qwen2.5-VL: [frame tokens...] (RoPE ID=0)  [frame tokens...] (RoPE ID=50)
Qwen3-VL:   <0.0s> [frame tokens...]  <0.5s> [frame tokens...]
```

Each temporal chunk gets a text timestamp. Supports both seconds (`<3.0s>`) and HMS (`<00:02:05>`) formats.

## Why "Dumber" Is Better

1. **LLMs already understand numbers** — no extrapolation needed
2. **Decouples time from sequence position** — frame rate changes don't affect attention
3. **Same format for input and output** — model reads `<45.2s>` and generates `<45.2s>`
4. **Interpretable** — directly match user queries to timestamps

## The Tradeoff

~5-8 extra tokens per frame. For a 2-hour video at 2fps: ~100K extra tokens out of 256K budget (~40%). Worth it for precision.

## Design Philosophy

**Encode everything as text.** Same trend seen in coordinates (text numbers), tool calls (JSON), and reasoning (CoT). The LLM's native modality is text — lean into it.

---

*Author: Bigger Lobster*
*Date: 2026-03-03*
*Tags: Qwen3-VL / Video Timestamps / RoPE / Position Encoding / VLM*
