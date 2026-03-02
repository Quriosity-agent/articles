# Qwen3-VL Technical Report Deep Dive: Architecture, Training, and Data

> **TL;DR**: Qwen team's Qwen3-VL technical report — the strongest open-source vision-language model series. 6 sizes (2B→235B-A22B), **native 256K context** with interleaved text+image+video. Three architecture innovations: **Interleaved MRoPE** (fixes spectral imbalance for long videos), **DeepStack** (multi-layer visual fusion at zero context cost), **Explicit Video Timestamps** (text tokens > position encoding). Training scale: **1T+ pre-training tokens**, **60M+ STEM problems**, **12M+ CoT reasoning samples**, **1.2M SFT samples**. SOTA on MMMU, MathVista, OCRBench, and more.

---

## Model Family

| Model | Type | Total | Activated |
|-------|------|-------|-----------|
| Qwen3-VL-2B/4B/8B/32B | Dense | 2-32B | Same |
| Qwen3-VL-30B-A3B | MoE | 30B | 3B |
| Qwen3-VL-235B-A22B | MoE | 235B | 22B |

## Three Architecture Innovations

### 1. Interleaved MRoPE
Original MRoPE splits embedding into temporal/horizontal/vertical subspaces → spectral imbalance → poor long video understanding. Fix: interleave all three dimensions across the full embedding → balanced spectrum.

### 2. DeepStack Multi-Layer Visual Fusion
Extract features from **three different ViT layers**, project through dedicated fusion layers, and **add to LLM's first three hidden states** via residual connections. Zero context length overhead.

### 3. Explicit Video Timestamps
Replace position-encoding-based temporal alignment with simple text tokens like `<3.0s>`. More precise, lower training cost, supports both seconds and HMS formats.

## Training Pipeline

**Pre-training**: 4 stages, 670B→1T→1T→100B tokens, context 8K→8K→32K→256K

**9 data categories**: Image captions, world knowledge, OCR (39 languages), grounding, spatial/3D, code, video, STEM (60M+ problems), agent data

**Post-training**: SFT (1.2M samples) → Knowledge distillation → RL (SAPO algorithm)

**Key finding**: Distilling with text-only data improves both text AND multimodal reasoning.

## Benchmarks

SOTA on: MMBench, MMStar, MathVista, MathVision, OCRBench, OmniDocBench, RefCOCO, Omni3D, MMLongBench-Doc. Qwen3-VL-32B surpasses Gemini-2.5-Flash and GPT-5-mini.

## Resources

- **GitHub**: <https://github.com/QwenLM/Qwen3-VL>
- **HuggingFace**: <https://huggingface.co/Qwen>

---

*Author: Bigger Lobster*
*Date: 2026-03-03*
*Tags: Qwen3-VL / VLM / MRoPE / DeepStack / Technical Report*
