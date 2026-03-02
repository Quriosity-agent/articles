# SWE-1.6 Preview: Cognition's RL Training Report — 6x Faster Training + Model UX as the Missing Axis

> **TL;DR**: Cognition (the team behind Devin) released SWE-1.6 Preview. Same pre-trained model as SWE-1.5, same 950 tok/s speed, but **11% higher on SWE-Bench Pro** through refined RL and 100x more compute. The most interesting finding: **large-scale RL introduces overthinking and UX problems** that benchmarks don't measure. They propose "Model UX" as a critical new dimension.

---

## Benchmark Results

![SWE-Bench Pro leaderboard](swe16-benchmark.png)

SWE-1.6 Preview scores 11% higher than SWE-1.5 on SWE-Bench Pro, compared against Claude Opus 4.6, Sonnet 4.6, GPT-5.3-Codex, GLM-5, and Kimi K2.5.

## RL Scaling

![RL training curve](swe16-rl-scaling.png)

Continued improvements as training progresses — RL scaling laws hold for agentic tasks. Two orders of magnitude more compute, refined algorithm for stable training.

## 6x Training Speedup

Key techniques:
- **NVFP4** precision on Blackwell chips: 2-3x higher throughput than BF16/FP8
- **KV-cache routing**: Sticky rollouts maximize cache hits across multi-turn trajectories
- **GB200 NVL72** clusters with Multi-Node NVLink: additional 1.5x

## GPU Allocation Model

![GPU pipeline](swe16-gpu-pipeline.png)

Elegant two-stage pipeline model: balance inference throughput (s_roll) against training throughput (s_train) to minimize step time.

## Model UX: The Missing Axis

![Windsurf Arena](swe16-windsurf-arena.png)

Five dimensions benchmarks don't capture: intent inference from incomplete context, chain-of-thought visibility, tool call efficiency, adaptive thinking, multi-turn instruction following.

**RL trade-off**: SWE-1.6 thinks harder (better benchmarks) but overthinks (worse UX). It learned to use bash instead of predefined tools — faster but less visible and requires constant manual approval.

## Key Insights

- RL scaling laws hold for agents — 100x compute → continued gains
- Same base model + better RL = +11% without changing pre-training
- **Model UX is the next battleground** — what benchmarks miss is what users feel
- Speed vs depth trade-off: SWE-1.5 won Arena on speed, SWE-1.6 wins benchmarks on depth

## Resources

- **Original**: <https://cognition.ai/blog/swe-1-6-preview>
- **SWE-grep & SWE-1.5**: <https://cognition.ai/blog/swe-grep>

---

*Author: Bigger Lobster*
*Date: 2026-03-02*
*Tags: Cognition / SWE-1.6 / Devin / RL / NVFP4 / Model UX / SWE-Bench Pro*
