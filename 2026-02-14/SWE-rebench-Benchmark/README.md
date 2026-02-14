# 🏆 SWE-rebench: The Benchmark That Exposes Who's Really Winning the AI Race

**Source:** [David Ondrej on X](https://x.com/DavidOndrej1/status/2022597312024056285) | [SWE-rebench Leaderboard](https://swe-rebench.com)

**Date:** 2026-02-14

---

## TL;DR

A new benchmark called **SWE-rebench** just dropped, and it suggests many Chinese AI companies have been gaming popular benchmarks. When tested on fresh, uncontaminated coding tasks, the leaderboard looks very different.

## What is SWE-rebench?

Built by Nebius AI, SWE-rebench evaluates AI models on **real-world software engineering tasks** pulled from live GitHub repositories. Unlike static benchmarks (like the original SWE-bench), it has three key innovations:

- **Continuously updated tasks** — new problems are mined from real repos, so models can't memorize answers
- **Contamination tracking** — tasks created *after* a model's release date are flagged, exposing which models may have trained on test data
- **Standardized scaffolding** — all models get the same tools and prompts, so you're comparing the model, not the wrapper

## The Current Leaderboard (Feb 2026)

- **#1: Claude Opus 4.6** — claimed the top spot with stable, high performance
- **Claude Code** has the highest pass@5 across all models
- **gpt-5.2-codex** — extremely token-efficient, fewer tokens than any model with similar capability
- **Open-source catching up:** Kimi K2 Thinking, GLM-5, and Qwen3-Coder-Next lead open-source rankings, approaching closed-source performance
- **Qwen3-Coder-Next** — impressive with only ~3B active parameters, ranking top 2 by pass@5
- **Budget kings:** Grok Code Fast 1 and gpt-oss-120b deliver ~30% resolved rate at only $0.03-0.04 per problem

## Why This Matters

The core claim: many models that top traditional benchmarks have been **optimizing specifically for those evals** — essentially "teaching to the test." SWE-rebench's rolling dataset makes this much harder. Models highlighted in red on the leaderboard may be contaminated (tasks existed before model release).

## Key Insights

- **Reasoning mode matters hugely** — GPT-OSS-120B nearly doubled its score in high-effort reasoning mode
- **Bigger ≠ better** — Gemini 3 Flash slightly outperformed Gemini 3 Pro despite being smaller and cheaper
- **Caching is a game-changer** — Claude Sonnet 4's cost dropped from $5.29 to $0.91 per problem with proper caching
- **MiniMax M2.5** competes with top open-source models at only $0.09 per problem

## The Bottom Line

If you've been following AI benchmarks and thinking the race is neck-and-neck — SWE-rebench suggests otherwise. When you remove the possibility of benchmark contamination and test on fresh, real-world coding tasks, **the gap between leaders and followers is larger than traditional benchmarks suggest.**

🔗 Explore the full leaderboard: [swe-rebench.com](https://swe-rebench.com)
