# Qwen3.5: Alibaba's Native Multimodal Agent Model — 0.8B to 397B Full-Size Coverage

> **TL;DR**: Alibaba's Qwen team releases Qwen3.5 — **native multimodal agent model series** spanning 8 sizes from 0.8B to 397B-A17B (MoE). Key breakthroughs: **unified vision-language foundation** (early fusion), **Gated Delta Networks + MoE hybrid** (high throughput, low latency), **million-agent RL training**, **201 language support**. The 27B dense model hits 72.4% on SWE-Bench Verified, matching GPT-5 mini. All models **Apache 2.0 open-source**.

---

## Benchmarks

![Qwen3.5-397B-A17B](qwen35-benchmark.png)
*Flagship MoE model benchmarks.*

![Middle-size models](qwen35-middle.png)
*27B dense, 35B-A3B MoE, 122B-A10B MoE.*

![Small models](qwen35-small.png)
*0.8B to 9B models.*

## Model Family

| Model | Type | Total | Activated |
|-------|------|-------|-----------|
| 397B-A17B | MoE | 397B | 17B |
| 122B-A10B | MoE | 122B | 10B |
| 35B-A3B | MoE | 35B | 3B |
| 27B | Dense | 27B | 27B |
| 9B/4B/2B/0.8B | Dense | — | — |

## Five Core Breakthroughs

1. **Unified Vision-Language Foundation** — Early fusion on trillions of multimodal tokens
2. **Gated Delta Networks + MoE** — New attention mechanism + sparse experts
3. **Million-Agent RL** — Progressive task difficulty across 1M+ environments
4. **201 Languages** — Broadest coverage among open-source models
5. **Near-100% Multimodal Training Efficiency** — Almost no overhead vs text-only

## Why 27B Dense Matters Most

72.4% on SWE-Bench Verified = matches GPT-5 mini. Runs on a single A100 80G. Fully open-source Apache 2.0.

## Resources

- **Blog**: <https://qwen.ai/blog?id=qwen3.5>
- **GitHub**: <https://github.com/QwenLM/Qwen3.5>
- **HuggingFace**: <https://huggingface.co/collections/Qwen/qwen35>

---

*Author: Bigger Lobster*
*Date: 2026-03-03*
*Tags: Qwen3.5 / Alibaba / MoE / Multimodal / Agent / RL / Open Source / 201 Languages*
