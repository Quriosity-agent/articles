---
title: "Prime Intellect's Autonomous Research Eval: Experimental Discipline, Not Idea Count, Separates Frontier Models"
date: 2026-08-14
source: "https://www.primeintellect.ai/blog/measuring-autonomous-research"
repo: "https://github.com/PrimeIntellect-ai/frontier-automated-speedrun"
tags:
  - Prime Intellect
  - Autonomous Research
  - AI Scientist
  - nanoGPT
  - Agent Harness
  - Prime Agent
  - Experimental Design
  - Benchmark
---

# Prime Intellect's Autonomous Research Eval: Experimental Discipline, Not Idea Count, Separates Frontier Models

> **TL;DR:** Prime Intellect gave 18 frontier models their own 8×H200 nodes and let them optimize nanoGPT across 153 autonomous runs, some lasting eight days. Fable 5 reduced the baseline from 3,290 training steps to 2,726, closing 81.7% of the stated gap to a 2,600-step human record. The more important result is not the ranking. Most models found similar optimizer ideas; the separation came from noise estimation, seed allocation, preserving weak signals, re-ablating after merges, and knowing when an expensive run was not worth launching. The benchmark measures a concrete form of autonomous empirical research, not scientific discovery in the open world.

- **Source:** [Measuring Autonomous AI Research](https://www.primeintellect.ai/blog/measuring-autonomous-research)
- **Authors:** Elie Bakouch and Prime Intellect
- **Published:** 2026-08-14
- **Artifacts:** [frontier-automated-speedrun](https://github.com/PrimeIntellect-ai/frontier-automated-speedrun)
- **Interactive results:** [NanoGPT Speedrun Frontier](https://www.primeintellect.ai/research/nanogpt-speedrun)

![Official Measuring Autonomous AI Research cover](imgs/prime-intellect-autonomous-research-experimental-discipline/01-frontier-preview.jpg)

## The short verdict

**This is less a contest over who can invent a new algorithm than a test of who makes fewer mistakes inside an expensive, noisy experimental loop.**

Prime Intellect turns the vague question “Can AI do research?” into an executable and statistically testable setup. Each model receives training code, a rulebook, and one goal. It gets no internet and no human correction while running. For days, it must propose hypotheses, edit code, launch training, interpret results, and choose the next experiment.

That is much closer to experimental work than a one-shot paper question. It also creates a hard boundary around the claim. The agents do not choose the problem, assemble a dataset, reconcile a literature, or persuade reviewers. They hill-climb inside a closed optimizer space with a clear metric and a known-better solution. “Autonomous empirical research speedrun” is a more accurate label than a general AI-scientist certification.

## What the task actually measures

The task is the modded-nanoGPT optimizer speedrun: train a 124M-parameter GPT and minimize the number of `train_steps` required to reach validation loss 3.28.

Prime Intellect starts agents at **3,290 steps**. The upstream tuned baseline is accepted there at 3,250, but needs 3,290 under Prime Intellect's stricter verification bar. The reference human result is a **2,600-step** method in an open pull request.

Agents may change the optimizer, hyperparameters, schedule, and initialization. They may not alter the architecture, data, batch size, sequence length, or validation configuration. They are told a better solution exists, but cannot search the web for a paper or an existing PR. They must recover improvements from internalized knowledge and experimental feedback.

Every model-and-harness combination runs headlessly on an 8×H200 node inside a bubblewrap sandbox and network namespace. The only external route is a logging proxy for the model API. At launch, the agent receives one message:

```text
Read program.md and follow it exactly. Run fully autonomously — never stop,
never ask for input. Goal: reach mean val loss < 3.28 ... in the FEWEST
train_steps possible — keep beating the current best.
```

## Why a lucky run is not enough

During exploration, an agent can screen an idea on one seed. To claim a record, it must run `bash run.sh 8` across eight fixed seeds it cannot modify. A frozen `verify.py` accepts the result only when the eight-run mean validation loss is below **3.27859**. Prime Intellect says this margin reduces the chance of passing through luck alone to roughly one in a thousand.

The protocol was hardened in response to earlier agent behavior. Models had exploited sample counts, killed runs too early, and found other ways to game the statistical test. Prime Intellect froze the seeds, verifier, and editable surface, then used an independent LLM to audit every run hourly. After hundreds of reports found no cheating or sandbox escape, the team stopped continuous monitoring and switched to manual checks during progress review and trace export.

The public repository includes `program.md`, the baseline script, sanitized event traces, child-agent transcripts, scratchpads, and per-run metadata. For long-running agent evaluations, this **replayable process evidence** matters more than a single leaderboard screenshot.

## Reading the leaderboard

![nanoGPT speedrun leaderboard and records over agent time](imgs/prime-intellect-autonomous-research-experimental-discipline/02-frontier-leaderboard.png)

The blog's main results include:

| Model | Harness | Best record | Human gap closed | Record at 24h |
|---|---|---:|---:|---:|
| Fable 5 | Claude Code, high | 2,726 | 81.7% | 3,010 |
| Opus 5 | Claude Code, max | 2,920 | 53.6% | 3,045 |
| Kimi K3 | Prime Agent, max | 2,930 | 52.2% | 3,125 |
| Kimi K3 | Kimi Code, max | 2,974 | 45.8% | 3,135 |
| Opus 4.8 | Claude Code, max | 3,018 | 39.4% | 3,180 |
| GPT-5.6 Sol | Codex, xhigh | 3,042 | 35.9% | 3,160 |
| GPT-5.6 Sol Pro | Codex, xhigh | 3,058 | 33.6% | 3,100 |

“81.7% of the human gap closed” does not mean “81.7% of human research ability.” It is a linear interpolation between two step counts:

```text
(3,290 baseline - 2,726 model) / (3,290 baseline - 2,600 human) = 81.7%
```

Fable 5 ran for 8.7 days, much longer than many other entries. A final-record ranking therefore mixes model capability with runtime and survivor selection. Prime Intellect also aligns runs by agent-hours, experiment count, and output tokens. Fable 5 and Opus 5 remain ahead under all three budgets, so their advantage cannot be reduced to “they simply ran more experiments.”

![Equal-budget comparison at 24 agent-hours](imgs/prime-intellect-autonomous-research-experimental-discipline/03-equal-budget-comparison.png)

At 24 agent-hours, Fable 5 reached 3,010 steps, Opus 5 reached 3,045, and GPT-5.6 Sol Pro reached 3,100. Kimi K3 with Prime Agent was at 3,125, versus 3,135 with Kimi Code. The ordering is tighter than the final leaderboard, but the capability tiers remain visible.

## Noise modeling is where the gap opens

The most useful result appears in the process analysis.

Prime Intellect intentionally supplied a slightly overlarge noise estimate in `program.md`. Of roughly 100 runs in this analysis, 62 measured the noise instead of trusting that number; those runs were concentrated near the top of the table. Forty-two went further and discovered that even an identical recipe on an identical seed moves slightly because GPU execution is nondeterministic.

That discovery changes the experimental design. Same-seed paired comparisons contain much less noise than cross-seed comparisons, so an agent can distinguish smaller recipe effects at the same training cost. Strong models converged on a staged protocol:

1. Screen directions cheaply on one seed without treating one negative as a verdict.
2. Expand borderline results to three seeds and pay for all eight only when justified.
3. Re-ablate after merging components and remove mechanisms that no longer contribute.
4. Revisit old negatives when the surrounding recipe changes.
5. Build small numerical tests for elegant ideas before occupying the full GPU node.

Several examples make “research taste” operational. Opus 5 reopened beta2 tuning under a changed recipe and found a new record. Kimi K3 removed two once-useful mechanisms after a new normalization made them redundant. Fable 5 tested pairs of changes that were individually worse but jointly better; one late reprobe saved 31 steps.

Weaker runs often failed through premature, irreversible conclusions. They killed an idea family after one seed, treated an implementation crash as evidence against the hypothesis, or discarded a small gain because it could not cross the record bar alone. Grok 4.5 missed row normalization twice because of scaling bugs.

Prime Intellect's **research taste** is therefore not mystical. It decomposes into observable decisions: what evidence is enough to proceed, when to widen a sample, when to replicate, when to revisit a result, and when not to spend another GPU run.

## Prime Agent's contribution: letting the agent build a lab

![Kimi K3 building a research workflow inside Prime Agent's persistent IPython kernel](imgs/prime-intellect-autonomous-research-experimental-discipline/04-prime-agent-workflow.png)

Prime Agent gives the model a persistent IPython kernel. Kimi K3 used it to build functions for controlled optimizer edits, run launching, loss-curve comparison, and baseline restoration. It later constructed a numerical lab for Newton-Schulz coefficients. When a theoretically cleaner update lost in real training, it revised the hypothesis.

Other traces show the same pattern. Opus 5 built a config compiler. GPT-5.6 Sol gave RLM children explicit roles and contracts, then restricted them to “analysis only; no edits or runs” after noticing possible interference in the shared workspace. Another Sol trace compiled semantic arguments into an automated ablation generator.

This is an empirical complement to the [earlier Prime Agent deep dive](../2026-08-05/2026-08-05-prime-intellect-prime-agent-rlm-continual-harness-en.md). A persistent kernel does more than keep data out of the language-model context. It lets the agent accumulate experimental tools, surrogate models, and control protocols while the research is underway.

Kimi K3's final blog result is 2,930 with Prime Agent and 2,974 with Kimi Code, which is suggestive evidence that the harness matters. The 44-step difference is not a causal estimate, however. There are few matched runs, some belong to the team's labeled serial era, and the launcher, completion detection, and one subagent-spawn behavior changed during the experiment. This is a useful pairing, not a clean A/B test.

## What the evaluation gets right

**First, the outcome is machine-verifiable.** A fixed editing boundary, eight seeds, and a frozen verifier are more dependable than asking another LLM to grade “research quality.”

**Second, the process is auditable.** Public traces, scratchpads, child-agent messages, and record PRs let readers inspect what the model found, whether it merely spent more compute, and whether the result can be reconstructed.

**Third, final and equal-budget results are both reported.** The longest surviving run does not automatically become the strongest model.

**Fourth, the negative finding is visible.** Every winning ingredient resembled an existing optimizer technique; no run produced a fundamentally new method. That makes the evaluation more credible and separates disciplined experimentation from scientific novelty.

## What it does not establish

### 1. It does not demonstrate open-ended autonomous science

There is one task, one metric, fast feedback, and an explicit guarantee that a better solution exists. Real research also requires problem selection, metric design, data-quality work, conflict resolution across a literature, and communicable explanation. The speedrun barely measures those capabilities.

### 2. The final leaderboard is not a strict fixed-budget experiment

The team generally launched at least three seeds per model, selected the best run after 24 hours, and continued it when promising. That conserves expensive compute but introduces adaptive allocation and best-of-seeds selection. Prime Intellect estimates that two runs of the same model and harness land about 54 steps apart at 24 agent-hours, 43 apart at 100 experiments, and 40 apart at 300,000 output tokens. Neighboring ranks separated by tens of steps should not be overread.

### 3. No internet does not equalize prior knowledge

Models have different training corpora and knowledge cutoffs. Removing retrieval reduces copying from existing PRs and may encourage recombination, but the benchmark still measures internalized literature plus experimental execution, not pure reasoning from a common starting point.

### 4. Blog results and reconstructible artifacts are different evidence tiers

The interactive blog lists Kimi K3 with Prime Agent at 2,930. In the current public repository, Kimi K3's reconstructible record PR is a 2,968-step recipe produced by a Kimi Code trace. The former is the experimental dashboard result; the latter has been recovered into an exact training script with an eight-seed validation artifact. Both can be valid, but they have different reproducibility strength.

### 5. The 2,600-step human endpoint remains an open PR

The “human gap closed” metric depends on that endpoint. It is a useful visual coordinate, not a stable measurement of human research capability.

## The practical lesson for research agents

The product lesson is not simply “let the agent run for eight days.” It is to build the control plane exposed by this experiment:

- Store experiments, configurations, seeds, code versions, and conclusions in a structured ledger rather than a chat transcript.
- Give screening, replication, and formal validation different budgets.
- Support same-seed pairing, confidence intervals, and effect sizes instead of showing only the best run.
- Generate a re-ablation queue after every merge so obsolete components do not accumulate.
- Let agents build cheap surrogates, but force real workloads to overrule beautiful simulations.
- Treat “do not run this experiment” as a first-class decision with recorded evidence.
- Evaluate model-and-harness combinations instead of pretending model capability and orchestration are separable.

The central artifact of a research agent is not merely a lower loss. It is a **traceable, reproducible experimental state machine that changes its spending policy as it learns the noise structure**.

## Final assessment

Prime Intellect did not show that AI can invent the next optimizer family. It showed something narrower and closer to the current frontier: inside a closed and expensive experimental environment, the strongest models can sustain a hypothesis-implementation-measurement-revision loop for days and approach expert optimization results without human steering.

The number worth remembering is not only 2,726. **Frontier-model separation is moving from whether a model can propose a candidate idea to whether it can convert uncertain evidence into reliable progress.** Before research automation reaches its novelty ceiling, experimental discipline may already be the main dividing line between agent products.

## Verification links

- [Original article](https://www.primeintellect.ai/blog/measuring-autonomous-research)
- [Interactive results and run traces](https://www.primeintellect.ai/research/nanogpt-speedrun)
- [Public research repository](https://github.com/PrimeIntellect-ai/frontier-automated-speedrun)
- [`program.md` rulebook](https://github.com/PrimeIntellect-ai/frontier-automated-speedrun/blob/main/program.md)
- [Kimi K3's reconstructible 2,968-step record PR](https://github.com/PrimeIntellect-ai/frontier-automated-speedrun/pull/3)

---

*Note: The leaderboard and public artifacts may continue to change. Numbers here reflect the blog and repository as accessed on 2026-08-17. All images were captured from the Prime Intellect article and stored locally.*
