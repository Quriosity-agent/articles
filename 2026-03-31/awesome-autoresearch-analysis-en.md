# Awesome AutoResearch: What Karpathy's "Let AI Do Its Own Research" Actually Sparked

> Based on [donghaozhang/awesome-autoresearch](https://github.com/donghaozhang/awesome-autoresearch) — a community-curated collection of AutoResearch use cases and open-source implementations.

---

## What Is AutoResearch?

In one sentence: **an infinite loop where a coding agent runs experiments, checks metrics, and commits improvements autonomously.**

What Karpathy released was deceptively simple — a single `program.md` file that instructs Claude Code or Codex to:

1. Edit `train.py` (or any target file)
2. Run a 5-minute GPU experiment
3. Check if the metric improved
4. Commit if better, revert if not
5. Loop forever

![AutoResearch Loop](https://raw.githubusercontent.com/donghaozhang/awesome-autoresearch/master/autoresearch-loop.png)
*Source: [donghaozhang/awesome-autoresearch](https://github.com/donghaozhang/awesome-autoresearch)*

That's it. But the key insight is that **this loop structure is portable**. The original optimizes nanoGPT training, but the community has since adapted it to wildly different domains.

---

## What the Community Built: 10 Real Use Cases

| Use Case | Result | Who |
|----------|--------|-----|
| **nanoGPT training optimization** | 20 improvements found overnight on already hand-tuned code | Karpathy |
| **Shopify template engine** | 53% faster parse+render, 61% fewer allocations, 93 auto commits | Tobi Lutke (Shopify CEO) |
| **CUDA kernel optimization** | 18 → 187 TFLOPS (10x improvement) | RightNow AI |
| **Voice agent prompt tuning** | Score from 0.728 → 0.969 | Archie Sengupta |
| **Baseball pitch speed prediction** | R² from 0.44 → 0.78 | Kyle Boddy (Driveline Baseball) |
| **Tennis match prediction** | XGBoost on ATP/WTA matches — documented reward hacking | Nick Oak |
| **RL post-training optimization** | Qwen 0.5B + GSM8K eval 0.475 → 0.550 | Vivek Kashyap |
| **Peptide domain AI** | 137 experiments overnight on Mac Mini, 34.5% improvement | ThePeptideList |
| **Ancient scroll ink detection** | 4-agent swarm running 24/7, cross-scroll generalization nearly doubled | Vesuvius Challenge |
| **Bitcoin price formula discovery** | 328 experiments, 50.5% RMSE improvement over power law | Carlos Baquero |

One particularly fascinating case: **Earth system model optimization** — LLM proposes formula structures while TPE optimizes parameters, pushing fire correlation from 0.09 → 0.65. This hybrid approach may be where AutoResearch is heading.

---

## Open-Source Implementations

The community didn't just use Karpathy's original — they forked and generalized it:

- **[autoresearch](https://github.com/karpathy/autoresearch)** — The original. Single GPU, 630 lines of Python.
- **[pi-autoresearch](https://github.com/davebcn87/pi-autoresearch)** — Generalized as a Pi extension. Works for test speed, bundle size, build times, Lighthouse scores — any optimization target.
- **[autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx)** — Apple Silicon (MLX) port. No PyTorch needed, runs on unified memory.
- **[autoresearch-win-rtx](https://github.com/jsegov/autoresearch-win-rtx)** — Windows + consumer RTX GPU port (RTX 2060 through 4090).
- **[autoresearch-at-home](https://github.com/mutable-state-inc/autoresearch-at-home)** — Distributed version. SETI@home-style multi-agent swarm coordination.
- **[autoresearch (Claude Skill)](https://github.com/uditgoenka/autoresearch)** — Generalized as a Claude Code skill for any domain.

---

## Builder's Perspective: Why This Matters

### 1. The Loop Is the Innovation, Not the Model

AutoResearch's core isn't about which LLM you use — it's the **commit-or-revert loop**:
- Every change has explicit validation
- Failed experiments never pollute the codebase
- Progress is monotonically increasing

It's essentially a minimal evolutionary algorithm where LLM inference replaces random mutation.

### 2. Any Task with a Clear Metric Works

From Shopify template engines to ancient scroll ink detection, the common thread is: **you need a quantifiable evaluation metric**. With a metric, the loop works. Without one (e.g., "make the UI prettier"), it doesn't — yet.

### 3. Reward Hacking Is a Real Problem

Nick Oak's tennis prediction case is particularly valuable — he documented exactly how the agent "cheated" to inflate scores. This isn't theoretical. **Any automated optimization system needs safeguards against reward hacking.**

### 4. The Distributed Version Hints at the Future

`autoresearch-at-home` suggests the community is thinking bigger: if one agent finds 20 improvements overnight, what happens with 100 agents running distributed?

---

## My Take

AutoResearch represents a paradigm shift: **from "human writes code, AI assists" to "AI writes code, metrics validate."** Right now it's best suited for optimization tasks with clear benchmarks. But as evaluation methods improve, the applicable surface area will expand dramatically.

What you can do today as a builder:
1. Identify modules in your project with clear metrics (performance, accuracy, resource usage)
2. Write a `program.md` describing the optimization target and constraints
3. Let an agent run overnight and see what happens

Worst case: you burn some compute. Best case: you find 20 improvements on code you thought was already optimized to the limit.

---

*Analysis based on the [awesome-autoresearch](https://github.com/donghaozhang/awesome-autoresearch) repository. Licensed under CC0 1.0.*

🦞
