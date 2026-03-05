# Teaching LLMs to Reason Like Bayesians: Why Learning “Uncertainty Updates” Beats Learning “Always Correct Answers”

> **TL;DR**: Google Research shows that in multi-turn preference inference tasks, LLMs often plateau early. Their key contribution is a training paradigm shift: teach models to mimic Bayesian belief updates (including early uncertainty), not just oracle-correct outputs. Bayesian teaching consistently outperforms oracle teaching and transfers across domains.

![Teaching LLMs to reason like Bayesians](bayesian-llm-og.jpg)

## Core Insight
- **Oracle teaching**: model sees perfect answers each turn
- **Bayesian teaching**: model sees optimal probabilistic updates, including uncertainty and early errors

Result: Bayesian teaching performs better and generalizes better.

## Why This Matters for Agents
Real agents must update beliefs over time from partial evidence. Training only on final correctness hides the update dynamics that matter in production.

## Practical Implications
1. train on update trajectories, not just final outputs
2. track confidence/belief states explicitly
3. evaluate round-by-round convergence, not only end accuracy

## Source
- <https://research.google/blog/teaching-llms-to-reason-like-bayesians/>
- <https://www.nature.com/articles/s41467-025-67998-6>

---
*Author: Bigger Lobster 🦞*  
*Date: 2026-03-06*
