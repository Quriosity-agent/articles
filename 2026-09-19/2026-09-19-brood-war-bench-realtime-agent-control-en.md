---
title: "Brood War Bench Deep Dive: 171 StarCraft Matches Expose Agent Latency and Coordination Gaps"
date: 2026-09-19
source: "https://bw.swerdlow.dev/report"
canonical: "https://bw.swerdlow.dev/report"
tags:
  - Brood War Bench
  - Realtime Agents
  - Agent Evaluation
  - Codex
  - Claude
  - Grok
  - Multi-Agent Systems
  - Inference Latency
---

# Brood War Bench Deep Dive: 171 StarCraft Matches Expose Agent Latency and Coordination Gaps

> **TL;DR:** Ben Swerdlow ran a complete 171-match round robin among 19 model-and-reasoning-effort configurations in StarCraft: Brood War. Codex Astra / xhigh finished 18–0, Claude Fable went 15–3, and Grok plus Claude Haiku occupied the bottom of the table. The lasting value of the report is not the winner. It puts agents inside a world that does not pause while they think: inference latency becomes lost game time, subagents without a shared plan send units to die one by one, and higher reasoning effort does not reliably produce a higher win rate or a lower total match cost. This is an evaluation of closed-loop control, not merely static-answer accuracy.

- **Author:** [Ben Swerdlow](https://twitter.com/benswerd)
- **Report:** [Brood War Bench](https://bw.swerdlow.dev/report)
- **Scale:** 19 configurations, 171 completed matches, 342 player-runs
- **Saved evidence:** game-engine recordings, both agent-harness logs, match replays, and 30-second trend data
- **Published:** September 19, 2026 (the report page has no visible date; this follows its first public index record)
- **Checked:** September 23, 2026

![Official Brood War Bench artwork](imgs/brood-war-bench-realtime-agent-control/01-brood-war-bench-hero.webp)

## The short answer

Brood War Bench does not primarily test how much StarCraft knowledge a language model can recite. It tests whether the model can survive a continuous loop of **observe, reason, act, and observe again**.

A conventional benchmark can let a model think for minutes and score only the final answer. StarCraft keeps running. Every additional second of reasoning gives the opponent another second to mine, produce a unit, or destroy the base. Inference latency stops being a hidden serving metric and becomes damage inside the environment.

That explains the report's apparently contradictory result. Astra / xhigh was undefeated, yet higher effort was not consistently better within every model family. Older systems in particular behaved as if the real-time strategy game were turn-based and died while thinking. Capability, reasoning depth, action cadence, and the environment clock have to be evaluated together.

## How the 171 matches were formed

Each of the 19 model-and-effort configurations played every other configuration once:

`19 × 18 ÷ 2 = 171`

Each match ran on a Freestyle VM. A local player CLI and opponent CLI exchanged observations and commands with the same game. The benchmark saved both harness logs and the game-engine recording, then exposed replays. Trend data sampled workers, army, structures, minerals, gas, supply, and technology every 30 seconds.

The design has three useful properties:

1. **A shared opponent pool:** every configuration faced the same other 18 entries.
2. **Observable process:** the report includes economic, military, technology, and action-rate trajectories rather than only wins.
3. **Replayable failures:** G043, G005, G009, G007, G027, and G036 link behavior claims to specific replay windows.

It is still not a model-only comparison. Codex, Claude Code, and Grok run through different agent harnesses. Tool protocols, context handling, and command execution can all affect the result. The evaluated object is a model-runtime system.

## The ranking is clear, but absolute skill remains low

| Rank | Configuration | Record | Win rate | APM | Cost/game |
|---:|---|---:|---:|---:|---:|
| 1 | Codex Astra / xhigh | 18–0 | 100.0% | 12.6 | $10.54 |
| 2 | Codex Astra / medium | 16–2 | 88.9% | 17.2 | $15.11 |
| 3 | Claude Fable | 15–3 | 83.3% | 12.6 | $12.24 |
| 4 | Codex Astra / low | 14–4 | 77.8% | 25.7 | $21.07 |
| 5 | Codex 5.6 Sol / medium | 13–5 | 72.2% | 10.1 | $5.12 |
| 6 | Codex 5.6 Sol / low | 12–6 | 66.7% | 18.1 | $9.23 |
| 7 | Claude Opus 5 | 12–6 | 66.7% | 10.5 | $20.78 |
| 8 | Codex 5.6 Sol / xhigh | 11–7 | 61.1% | 8.0 | $3.23 |
| 9 | Codex 5.6 Luna / low | 9–9 | 50.0% | 23.8 | $0.42 |
| 10 | Codex 5.6 Terra / xhigh | 9–9 | 50.0% | 15.8 | $2.10 |

Astra / xhigh's 18–0 establishes a large advantage over this field. It does not establish competent StarCraft play. The author explicitly says that none of the models played beyond beginner level and that a beginner photon-cannon rush could likely beat all of them.

Two statements are therefore true at once: **Astra was the strongest configuration in the benchmark, and every configuration remained far from stable human play.** A relative leaderboard cannot replace an absolute baseline.

## Why more effort is not always better

The three Codex families show three different relationships between effort, results, and cost:

| Family | Best win-rate setting | Lowest-cost setting | Pattern |
|---|---|---|---|
| Astra | xhigh: 100% | xhigh: $10.54 | deeper reasoning aligns with results |
| Sol | medium: 72.2% | xhigh: $3.23 | medium wins more |
| Luna | low: 50.0% | xhigh: $0.16 | low effort wins more |

This does not justify a general claim that low effort is better for games. Performance is more plausibly a joint product of decision quality, inference latency, command-batch size, and match duration.

Cost is not simply model price multiplied by one call. A match that ends early may be cheaper overall. A low-token-price agent that fails to conclude a game can continue consuming resources for much longer. The Codex and Sonnet figures are token-based estimates, so the dollar values are best read as relative costs for these runs, not precise procurement prices.

![Agent win rate versus average cost per game on a logarithmic x-axis](imgs/brood-war-bench-realtime-agent-control/02-win-rate-vs-cost.webp)

## APM is not a monotonic quality metric

Terra / low reached 48.3 APM but won 44.4% of its games. Astra / xhigh used 12.6 APM and won every match. Grok / xhigh fell to 2.8 APM and barely produced effective control.

The report's APM should be understood as action frequency through the agent control interface, not as a direct equivalent of a professional player's mouse-and-keyboard APM. One high-level command may control multiple units; repeated, stale, or conflicting commands can also inflate activity without improving play.

The better metric is effective closed-loop frequency: how often the agent refreshes world state, how quickly it corrects deviation, and whether each command batch is stale before execution. Twelve coherent actions can outperform 48 actions that do not share a plan.

## Codex delegated work without maintaining shared state

The report observed Codex creating separate subagents for economy, production, and army control. That resembles a sensible multi-agent architecture, but the matches exposed a communication gap. The production agent did not know that the army was meant to assemble; the control agent sent each new unit into combat immediately. Units arrived one at a time and died against prepared defenses.

The missing component was not the ability to call a subagent. It was a shared operational state that every role obeyed:

- whether the current phase was harassment, defense, assembly, or attack;
- rally points, force thresholds, and earliest departure time;
- ownership of each unit group;
- the timestamp of the latest observation and whether commands were still fresh;
- events allowed to interrupt the long-term plan.

Human guidance improved planning and timing. That suggests the models possessed some strategic knowledge but struggled to turn it into synchronized execution in a changing environment.

## Why harassment beat macro play

Codex's most effective recurring idea was not a mature economy. It sent one or more Probes across the map early to disrupt the opponent. The opponent could then spend tens of seconds rethinking, turning real-time latency into an exploitable weakness.

This is a recognizable form of benchmark adaptation. The agent may not discover the best StarCraft strategy; it discovers the strategy that attacks the current opponent runtime. The target is not only the opponent's units. It is the opponent's control loop.

Most systems were still poor at sustained production, technology timing, and force assembly. Claude Fable showed comparatively richer development: in G007 it reached Lair, Spire, and Mutalisks; in G027 it built a Robotics Facility, Citadel, Observatory, and Templar Archives. Reaching advanced technology, however, is not the same as coordinating economy, composition, and engagement timing into a repeatable win condition.

Grok demonstrates the latency failure in its most extreme form. In G043, Grok / xhigh produced 11,138 reasoning tokens but issued only six command batches over 43 minutes and never built a combat unit. In a static setting that may look like extensive reasoning. In a real-time system it is functionally close to no action.

## What the five-minute snapshot reveals

After pooling effort settings by model family, the report gives these means for player-runs still represented at minute five:

| Metric | Codex Astra | Claude Fable | Grok 4.6 |
|---|---:|---:|---:|
| Workers | 14.7 | 16.7 | 7.4 |
| Army | 8.3 | 7.6 | 2.0 |
| Structures | 6.2 | 7.4 | 4.5 |
| Technology | 0.3 | 0.2 | 0.0 |
| Supply used | 26.5 | 26.6 | 11.3 |
| Banked minerals | 240.6 | 248.6 | 536.6 |

Grok's larger mineral bank is not evidence of a stronger economy. The resources were not converted into workers, structures, or army. The table also has an important caveat: completed games drop out of later time points, and the model-level view pools effort settings. It is not a fixed-cohort causal comparison.

## Six direct lessons for real-time agent design

1. **Separate fast control from slow planning.** A reactive controller handles survival, worker production, and sudden attacks while a slower planner sets technology, composition, and phase goals.
2. **Give reasoning a deadline.** Each loop needs a latency budget. On timeout, the system should take a reversible fallback action rather than freeze the world under an old plan.
3. **Observe and execute asynchronously.** Long reasoning should not block telemetry or basic control. Fresh observations must be able to cancel stale plans.
4. **Share state, not just messages.** Subagents need structured world state, budgets, unit ownership, and an operational phase instead of relying on scattered natural-language updates.
5. **Measure outcomes rather than activity.** APM, token count, and subagent count are intermediate signals. Resource conversion, state freshness, command failure, and plan completion are closer to operational quality.
6. **Preserve replayable evidence.** The strongest part of Brood War Bench is the combination of game recordings, agent logs, and time series, which lets a failure be traced to observation, reasoning, decision, or execution.

## What this benchmark does not establish

This is an informative researcher-run experiment, not a final model ranking:

- each configuration pair played only once, without repeated seeds, confidence intervals, or significance tests;
- the report page does not fully publish system prompts, tool schemas, race/map assignment, command budgets, and timeout rules;
- provider-specific harnesses confound model capability with runtime capability;
- head-to-head results can be sensitive to matchup style and early harassment, so a stable transitive ordering is not guaranteed;
- APM is interface activity rather than a same-scale measurement of human control;
- some costs are estimates and all are affected by match duration;
- there is no systematic human or conventional game-bot baseline beyond the author's qualitative beginner-level judgment.

The precise claim is that Astra / xhigh defeated the other 18 configurations under this harness, rule set, and single-round-robin schedule. It is not evidence that AI has mastered Brood War.

## Conclusion

Brood War Bench makes a usually hidden problem visible: **an agent's answer can be correct, yet arrive after the world has already changed.**

Astra's lead suggests newer systems are becoming more aware that thinking has a cost. Fable demonstrates comparatively coherent economy and technology. Grok's long reasoning and sparse action show that more reasoning tokens do not automatically create real-time control. Deeper reasoning becomes useful only when embedded in fast perception, deadlines, interruptible execution, and shared state.

That lesson extends well beyond games. Software, browsers, markets, robots, and multi-user workflows do not wait forever. Future agent evaluations should ask not only whether the final answer was correct, but how long action took, whether its state was still fresh, whether multiple executors shared one plan, and whether a failure can be reconstructed from complete evidence.

## Sources

1. Ben Swerdlow, “Brood War Bench”
   https://bw.swerdlow.dev/report

2. Machine-readable benchmark results
   https://bw.swerdlow.dev/benchmark/report.json

3. Aggregated 30-second trend data
   https://bw.swerdlow.dev/benchmark/trends.json

4. G043 replay example
   https://bw.swerdlow.dev/benchmark/replay.html?game=G043&start=210&duration=120&seat=0&focus=guest-base
