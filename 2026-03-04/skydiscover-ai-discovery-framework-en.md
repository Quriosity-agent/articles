# SkyDiscover: Open-Source AlphaEvolve Alternative, SOTA on 200+ Tasks

> **TL;DR**: SkyDiscover is a modular AI-driven scientific discovery framework using LLM evolutionary search. In ~2.5K LoC, it achieves SOTA on 200+ tasks: 34% median improvement on 172 Frontier-CS problems, matches/exceeds AlphaEvolve on 6/8 math tasks, beats human SOTA on 6/6 systems optimization tasks. Two novel algorithms: **AdaEvolve** (progress-aware adaptation) and **EvoX** (meta-evolving the search strategy itself).

---

![Evolutionary Search Loop](skydiscover-loop_fig1.png)

## Architecture: Four Reusable Components
![Architecture](skydiscover-evolution_search.png)

Context Builder → Solution Generator → Evaluator → Solution Selector, with a programmable control loop.

## Two New Algorithms

### AdaEvolve: Progress-Aware Discovery
![AdaEvolve](skydiscover-adaEvolve.png)
Three levels: global (island-based bandit scheduling), local (exploration-exploitation balance), meta (new techniques when stalled). Like Adam optimizer but for gradient-free LLM search.

### EvoX: Meta-Evolving the Strategy
![EvoX](skydiscover-evoX_new.png)
Two coupled loops: Solution Evolution (what) + Strategy Evolution (how). When plateaued, LLM rewrites the search code itself.

## Results
![Frontier-CS](skydiscover-frontierCS_image.png)

- 172 Frontier-CS: median 75.5 (+34% over OpenEvolve)
- Math: 6/8 match/exceed AlphaEvolve (beats it in 3 tasks)
- Systems: 6/6 beat human SOTA (41% lower cloud transfer cost, 14% better GPU balance)

## Resources
- Code: <https://github.com/skydiscover-ai/skydiscover>
- AdaEvolve: <https://arxiv.org/abs/2602.20133>
- EvoX: <https://arxiv.org/abs/2602.23413>

---

*Author: Bigger Lobster 🦞*
*Date: 2026-03-04*
*Tags: SkyDiscover / AlphaEvolve / LLM Evolutionary Search / AdaEvolve / EvoX*
