# Seed 2.0 Model Card Deep Dive (78 Pages): ByteDance's Brutally Honest Technical Report

> **TL;DR**: We extracted the full 78-page Seed 2.0 Model Card via pdfplumber. This is not a PR piece — ByteDance **openly admits gaps with Claude in coding and Gemini in science**. Key findings: Seed 2.0 Pro dominates **search agents, deep research, and vision agents**; crushes competitors on Minedojo-Verified (49.0 vs GPT-5.2's 18.3) and MM-BrowseComp (48.8 vs 26.3); but trails significantly on SWE-Evo (8.5 vs Claude's 27.1). Token pricing ~10x cheaper.

---

## Pricing (Table 1)
| Model | Input $/1M | Output $/1M |
|-------|-----------|------------|
| GPT-5.2 High | $1.75 | $14.00 |
| Claude Opus 4.5 | $5.00 | $25.00 |
| **Seed 2.0 Pro** | **$0.47** | **$2.37** |
| Seed 2.0 Lite | $0.09 | $0.53 |
| Seed 2.0 Mini | $0.03 | $0.31 |

## Agent Benchmarks (Table 11) — The Core Data

### Search Agent (Seed 2.0 Dominates)
- BrowseComp-zh: **82.4** (GPT 76.1, Claude 62.4)
- HLE-Verified: **73.6** (GPT 68.5, Claude 56.6)
- DeepSearchQA: **77.4** (GPT 71.3, Claude 76.1)

### Deep Research (All #1)
- DeepConsult: **61.1**, DeepResearchBench: **53.3**, ResearchRubrics: **50.7**

### Vision Agent (Crushing Lead)
- Minedojo-Verified: **49.0** vs GPT-5.2 18.3 (~3x)
- MM-BrowseComp: **48.8** vs GPT-5.2 26.3 (~2x)

### Coding Agent (Honest About Gaps)
- SWE-Evo: 8.5 vs Claude **27.1** — explicitly acknowledged
- NL2Repo-Bench: 27.9 vs GPT-5.2 **49.3**

## 5 Key Insights
1. **Search + Deep Research = killer app** — 4/7 search #1, all 3 deep research #1
2. **Vision Agent is the hidden king** — 3x lead on Minedojo
3. **Coding is the clear weakness** — admitted in the report
4. **Token efficiency matters** — 23% reasoning tokens for 71% of GPT-5.2's score (WorldTravel)
5. **Seed 2.0 Lite may be the best agent-per-dollar** — crushes GPT-5-mini at $0.09/$0.53

## Resources
- **Model Card PDF**: <https://lf3-static.bytednsdoc.com/obj/eden-cn/lapzild-tss/ljhwZthlaukjlkulzlp/seed2/0214/Seed2.0%20Model%20Card.pdf>

---

*Author: Bigger Lobster*
*Date: 2026-03-03*
*Tags: Seed 2.0 / ByteDance / Model Card / Agent Benchmarks / Honest Report*
