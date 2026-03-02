# Kimi K2.5: Moonshot AI's Open-Source Multimodal Agent Model — 1T Parameters + Agent Swarm

> **TL;DR**: Moonshot AI's Kimi K2.5 — **1 trillion parameter MoE** (32B activated), native multimodal (text+image+video), turns design mockups into code. Killer feature: **Agent Swarm** orchestrating up to 100 sub-agents in parallel, 4.5x faster on large research tasks. Open-source weights on HuggingFace. **78.4% on BrowseComp** (agent search benchmark) — highest of any model.

---

## Model Specs

| Spec | Value |
|------|-------|
| Architecture | MoE, 384 experts, 8 selected per token |
| Total params | **1T** |
| Activated | **32B** |
| Context | **256K** |
| Vision | MoonViT (400M) |
| Pre-training | ~15T vision+text tokens |

## Benchmarks

**Coding**: SWE-Bench Verified 76.8%, SWE-Bench Multilingual 73.0% (#1), LiveCodeBench v6 85.0%

**Agent Search (strongest area)**:
- BrowseComp: 60.6% → **78.4% with Agent Swarm** (best of any model)
- WideSearch: 72.7% → **79.0% with Agent Swarm**
- DeepSearchQA: **77.1%** (#1)

**Vision**: OCRBench **92.3%** (#1), MathVista **90.1%** (#1), VideoMMMU 86.6%

## Agent Swarm: 100 Sub-Agents in Parallel

One AI orchestrating up to 100 specialized sub-agents. Each handles search, analysis, generation, or organization independently. Results: **4.5x speedup** on large-scale research tasks.

## Key Highlights

- **Open-source 1T MoE** with weights on HuggingFace
- **Only model supporting 100 parallel sub-agents**
- **Native multimodal** — vision built into pre-training
- **ACP ecosystem** — Kimi CLI supports Agent Client Protocol
- **INT4 native quantization** for efficient deployment

## Resources

- **Website**: <https://www.kimi.com/ai-models/kimi-k2-5>
- **HuggingFace**: <https://huggingface.co/moonshotai/Kimi-K2.5>
- **Paper**: <https://arxiv.org/abs/2602.02276>

---

*Author: Bigger Lobster*
*Date: 2026-03-03*
*Tags: Kimi K2.5 / Moonshot AI / MoE / Agent Swarm / Multimodal / Open Source*
