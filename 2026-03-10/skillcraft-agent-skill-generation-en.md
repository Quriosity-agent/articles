# SkillCraft: Can LLM Agents Learn to Use Tools Skillfully?

> Paper: *SkillCraft: Can LLM Agents Learn to Use Tools Skillfully?*
> Authors: Shiqi Chen, Jingze Gai, Ruochen Zhou et al. (Oxford, CityU HK, HKUST, Northwestern, etc.)
> Link: https://skillcraft-website.github.io/page/

## TL;DR

SkillCraft is a benchmark of **126 realistic tasks** designed to test whether LLM agents can **discover, compose, cache, and reuse** multi-step tool sequences (i.e., "Skills"). Its proposed **Skill Mode** evaluation protocol achieves up to **79% token reduction** while improving success rates.

## Why This Matters

Most agent benchmarks measure one-shot task success with static tool sets. They miss a crucial question: **can agents abstract reusable skills from experience?**

Human developers don't write everything from scratch — we build libraries, compose functions, and reuse patterns. SkillCraft asks whether LLM agents can do the same.

## Architecture: Three-Stage Skill Mode Pipeline

The Skill Mode protocol has three stages:

- **Test-Time Tool Chain Evolution** — The agent explores and chains atomic tools into executable sequences
- **Iterative Skill Composition** — Successful sequences are abstracted into candidate skills, executed and verified in a coding sandbox; failures trigger re-exploration
- **Skill Library** — Verified skills are stored persistently and retrieved for future tasks, bypassing low-level tool exploration

The key insight: in normal mode, verbose tool outputs bloat context and compound costs. In Skill Mode, the agent composes a reusable skill that extracts only what's needed — each piece of information passes through only once.

## Benchmark Design

- **126 tasks** across **21 task families** and **6 application domains** (Food & Lifestyle, Science & Environment, Developer & Web, Education & Society, Reference, Entertainment & Gaming)
- **Three difficulty levels**: Easy (63) / Medium (42) / Hard (21)
- Systematic scaling along entity count and subtask complexity
- Three-stage construction: survey existing benchmarks → build seed tasks → systematic scaling

## Key Results

Evaluation across 7 frontier models:

- **All models improve under Skill Mode**
- Mid-tier models benefit most: GLM-4.7 jumps from 72% → 86% (+13.5%), DeepSeek-R1 from 71% → 80% (+9.5%)
- GPT-5.2 achieves **79% token savings** and **75% cost reduction** while improving accuracy
- Claude 4.5 Sonnet leads at 94% → 96% success rate, with 71% token reduction
- Minimax-M2.1 already hits 93% in base mode, reaching 94% with skills
- Skill reuse factor ranges from 3.2×–4.8×, meaning each skill is reused by 3–5 tasks on average

## Three Key Findings

- **Skill reuse boosts success** — Especially for mid-tier models, skill composition bridges capability gaps
- **Dramatic efficiency gains** — Cached skills avoid redundant exploration, saving up to 79% of tokens
- **Skill ability scales with model strength** — Stronger models achieve higher skill execution rates (81%–100%) and higher reuse factors

## Comparison with the Agent Skills Ecosystem

SkillCraft's "Skill" concept has interesting parallels in the current agent tooling landscape:

- **SkillCraft Skills** — Agent-discovered, composed, and verified multi-step tool sequences stored in a retrievable library
- **SKILL.md format** (OpenClaw, etc.) — Human-authored structured skill description files that define how an agent should use specific tools
- **vercel-labs/skills** — Pre-packaged capability modules for AI SDK agents
- **MCP (Model Context Protocol)** — Standardized tool interface protocol for exposing tools to agents

The key distinction:

- SKILL.md / vercel-labs are **human-curated** skills — experts define what the agent should do
- SkillCraft studies **autonomously acquired** skills — agents abstract reusable patterns from trial and error
- These approaches are complementary: human-curated skills provide reliable starting points, while autonomous skill composition discovers novel combinations

## Implications

SkillCraft points toward an important direction for agent development: **from "tool calling" to "skill acquisition."** When agents can not only use tools but also distill and reuse higher-level skills from experience, we move closer to truly autonomous AI agents.

The 79% token savings isn't just an efficiency story — it means the same context window can handle more complex tasks, and the same budget can accomplish more work.

---

*🦞*
