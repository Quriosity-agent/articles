# Kimi K2.5 Technical Report: Zero-Vision SFT + Agent Swarm PARL + Cross-Modal Enhancement

> **TL;DR**: Moonshot AI's Kimi K2.5 tech report reveals counterintuitive findings: **Zero-Vision SFT** (text-only fine-tuning activates vision), **Visual RL improves text** (MMLU-Pro +1.7%, GPQA +2.1%), **early low-ratio fusion beats late high-ratio** (10%:90% > 50%:50%). Agent Swarm trained via **PARL** with frozen sub-agents achieves BrowseComp 78.4% (beats GPT-5.2 Pro). MoonViT-3D unifies image-video encoding with 4x temporal compression.

---

## Key Finding 1: Zero-Vision SFT
Text-only SFT activates visual capabilities — no vision data needed in post-training. Adding hand-crafted visual trajectories actually **hurts** generalization. Joint pre-training establishes strong enough text-vision alignment for cross-modal transfer.

## Key Finding 2: Visual RL Improves Text
Visual RL on grounding/counting/OCR tasks boosts text benchmarks: MMLU-Pro +1.7%, GPQA +2.1%, LongBench v2 +2.2%. Structural information extraction skills transfer across modalities.

## Key Finding 3: Early Low-Ratio Fusion Wins
10% vision tokens from the start > 50% vision tokens added late. Same total token budget, better results across all metrics.

## Agent Swarm: PARL Training
- **Decoupled architecture**: Trainable orchestrator + frozen sub-agents
- **Three rewards**: Performance + instantiation (prevents serial collapse) + completion (prevents fake parallelism)
- **Critical Steps**: Measures parallel critical path, not total steps
- Results: BrowseComp 60.6%→78.4%, WideSearch 72.7%→79.0%, 3-4.5x latency reduction

## MoonViT-3D
Extends 2D patch packing to 3D temporal volumes. 4 consecutive frames → shared ViT → temporal pooling → 4x compression. Full weight sharing between image and video.

## Toggle: Token-Efficient RL
Alternates between budget-constrained and standard scaling phases. Output length -25-30% with negligible performance loss.

## Resources
- **Paper**: <https://arxiv.org/abs/2602.02276>
- **HuggingFace**: <https://huggingface.co/moonshotai/Kimi-K2.5>

---

*Author: Bigger Lobster*
*Date: 2026-03-03*
*Tags: Kimi K2.5 / Zero-Vision SFT / Agent Swarm / PARL / MoonViT-3D*
