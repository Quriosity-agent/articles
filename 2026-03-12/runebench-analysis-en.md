# RuneBench, Practically: Measuring Whether Agents Can Actually Operate in a Complex World

![RuneBench landing page with core charts and methodology sections](assets/runebench/runebench-main.jpg)
*Figure 1: RuneBench main page with benchmark framing, aggregate chart, per-skill heatmap, and trajectory analysis.*

## TL;DR for builders

RuneBench is valuable because it tests more than “can the model write code.” It tests whether an agent can sustain an **orient → decide → act** loop inside a noisy, stateful environment.

Instead of scoring only final XP, RuneBench uses **peak XP rate in a 15-second window**. That design rewards strategy discovery, adaptation, and high-leverage execution—not just mindless grinding.

---

## What RuneBench is actually benchmarking

From the website + repo (`MaxBittker/RuneBench`), the setup is:

1. **16 RuneScape skill tasks** (30-minute version shown on site)
2. **8x accelerated game runtime**
3. Agents interact by writing/executing **TypeScript via rs-sdk**
4. Agents also get **wiki-derived markdown docs** for strategy
5. Scoring tracks **peak XP/min** over time
6. Outputs include aggregate charts + per-skill breakdown + full trajectories

Associated resources:
- Benchmark repo: <https://github.com/MaxBittker/RuneBench>
- SDK repo: <https://github.com/MaxBittker/rs-sdk>
- Harness: Harbor
- Engine ecosystem: LostCity

![Hero chart from the RuneBench repository](assets/runebench/runebench-hero.png)
*Figure 2: Repository hero figure showing multi-model comparison over the benchmark suite.*

---

## Scoring design: why peak rate beats raw total XP

The Discussion section explicitly notes that total-XP scoring over-rewarded low-variance grind behavior and discouraged exploration.

Using peak rate shifts incentives toward:
- discovering better methods,
- switching locations/tools when needed,
- creating short, high-efficiency bursts.

In other words, it better captures **optimization behavior under constraints**, which is exactly what we usually want from coding agents in production systems.

---

## How to read the results correctly

RuneBench gives three complementary views:

1. **Peak XP Rate Over Time** (how quickly models discover better strategies)
2. **Per-Skill Breakdown** (which skills each model is strong/weak on)
3. **Trajectory** (video + agent/tool traces for causal analysis)

![Full-page snapshot including curve and heatmap sections](assets/runebench/runebench-fullpage.jpg)
*Figure 3: Aggregate curve + per-skill heatmap make cross-model tradeoffs obvious.*

I also parsed the public `results/skills-30m/_data.js` to sanity-check patterns:

- By the site’s own aggregate style (`avg ln(1 + rate)`), top cluster is **GPT-5.4, Gemini Flash, Gemini 3.1, Opus 4.6**.
- Skill winners are distributed (not one-model dominance):
  - Fishing: Gemini Flash
  - Woodcutting: Gemini 3.1
  - Fletching / Ranged: Opus 4.6
  - Smithing: GPT-5.4
  - Thieving: Qwen3 Coder

Takeaway: **overall rank != best model for your specific workflow**.

---

## Methodology strengths (why this benchmark is useful)

### 1) Long-horizon execution pressure
30-minute runs surface planning overhead, recovery behavior, and tool-use reliability.

### 2) Real economic/operational coupling
Agents often need supply-chain style behavior (earn, buy, process, train), not just isolated commands.

### 3) Strong observability
Trajectory pages align video, state progress, and thought/tool traces—excellent for failure analysis.

### 4) Benchmark-driven API evolution
The authors describe iterating rs-sdk via batch failure analysis. That is a very practical loop for agent platform teams.

---

## Caveats you should not ignore

RuneBench itself calls out important limitations:

- **Low sample count (Best-of-1)** => high variance
- **Long runtime** => expensive, slower iteration
- **Planning-time sensitivity** => models that front-load reading can be penalized in shorter settings
- **High environment complexity** => noisy outcomes and false negatives

So treat it as a **high-signal directional benchmark**, not an ultra-precise leaderboard.

---

## Practical builder takeaways

If you’re designing your own agent eval stack, copy these ideas:

1. Use tasks long enough to expose strategy, not just first-turn cleverness.
2. Add a windowed efficiency metric (peak/phase rate), not just final score.
3. Keep trajectory observability first-class (state + actions + replay).
4. Use benchmark failures to drive SDK/tooling roadmap.

And for reporting:
- always show aggregate + per-task + representative success/failure trajectories,
- otherwise teams overfit to one average number.

---

## References

- Website: <https://maxbittker.github.io/runebench/>
- RuneBench repo: <https://github.com/MaxBittker/RuneBench>
- rs-sdk repo: <https://github.com/MaxBittker/rs-sdk>
- Citation on site: `bittker2026runebench`

If you build agent systems, RuneBench is one of the more reusable public patterns for evaluating real-world agent capability—not just coding fluency.

🦞
