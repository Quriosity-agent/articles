---
title: "Prime Agent Deep Dive: The Next Layer of Agent Harnesses Lets the Model Program Its Own Context and Scaffolding"
date: 2026-08-05
source: "https://www.primeintellect.ai/blog/prime-agent"
repo: "https://github.com/PrimeIntellect-ai/prime-agent"
tags:
  - Prime Intellect
  - Prime Agent
  - RLM
  - Continual Harness
  - agent harness
  - programmatic tool calling
  - ARC-AGI-3
  - reward hacking
---

# Prime Agent Deep Dive: The Next Layer of Agent Harnesses Lets the Model Program Its Own Context and Scaffolding

> **TL;DR:** On 2026-08-05 Prime Intellect open-sourced Prime Agent, a coding harness built on two abstractions: the Recursive Language Model (context as variables, sub-agents as function calls inside a REPL) and the Continual Harness (prompts, skills, memory, and sub-agent specs as state the agent itself can CRUD). The headline number is 95.5% RHAE Best@1 on ARC-AGI-3 with Opus 5, edging past the reported human expert baseline of 95.4%. The number is not the interesting part. Three things are: how collapsing the tool surface into a single IPython kernel saves tokens, how `/refine` turns self-improvement into "smallest relevant CRUD edit, rollback by ID," and the Factorio reward hacking they disclosed themselves — where the same improvement loop, once it found an RCON exploit, started distilling cheating into reusable skills.

- **Source:** [Prime Agent: A self-improving RLM agent](https://www.primeintellect.ai/blog/prime-agent)
- **Repo:** [PrimeIntellect-ai/prime-agent](https://github.com/PrimeIntellect-ai/prime-agent) (MIT)
- **Authors:** Seth Karten, Alex L. Zhang, Kevin Thomas, Sebastian Müller, Prime Intellect Team
- **Published:** 2026-08-05 (Research)
- **Topic:** agent harness / recursive language models / programmatic tool calling / self-improvement / long-context evals

![Prime Agent cover](imgs/prime-intellect-prime-agent-rlm-continual-harness/01-cover.webp)

## The one-line read

**Prime Agent bets that a harness should stop compensating for what models can't do and start extrapolating on what they already can.**

The post states the critique bluntly: today's harness designs were built around the capabilities of earlier model generations. Fixed tool-calling schemas and context compaction force the model to work around its own scaffolding instead of leveraging it. Static, hand-engineered sub-agents, prompts, skills, and memory are set at design time and never adapt to what the agent learns while running.

That's worth sitting with if you build agent products. Most harness engineering over the past two years has gone into defense: compaction because context might blow up, narrowed schemas because the model might misuse tools, fixed orchestration because sub-agents might run away. Prime Agent goes the other direction and hands those decisions back to the model, expressed as code.

The project is fully open-source, installed with a single command:

```bash
curl -fsSL https://app.primeintellect.ai/prime-agent/install.sh | sh
```

![Prime Agent onboarding splash](imgs/prime-intellect-prime-agent-rlm-continual-harness/02-onboarding-splash.gif)

## Abstraction one: RLM, or context as a variable

The Recursive Language Model has a one-sentence definition: context is a variable, and sub-agent delegation is a function call inside a REPL.

In practice, the model's **only tool in Prime Agent is a persistent IPython kernel**. Everything a harness normally exposes — skills, tools, sub-agents — is pre-imported as a module at kernel init, and the model reaches it by writing code. Sub-agents are launched through `rlm`, an async function; each one is a full prime-agent instance with its own model, IPython kernel, session tree, and conversation history.

![Prime Agent architecture](imgs/prime-intellect-prime-agent-rlm-continual-harness/03-architecture.webp)

One design detail is easy to skim past and matters more than the rest: **`rlm()` returns at task admission with a child handle, never the child's answer.**

```python
# Parallel fan-out — the handle comes back immediately; results arrive as messages
auth = await rlm("Summarize the authentication flow in auth/. Reply to me when done.", name="auth-expert")
api  = await rlm("Summarize the updated HTTP API layer in src/. Reply to me when done.", name="http-expert")

# Steer a child mid-flight
await agent_message.send(
    "Also cover middleware error handling.",
    receiver_role="child",
    receiver_name=api.name,
)
```

Swapping return values for message replies changes the semantics from function call to inter-process communication. The parent never blocks; the child is no longer a disposable worker that dies on return. Its session directory, context, kernel, and history persist after the initial call, and it can be woken later by session name to continue.

That difference decides whether long-horizon orchestration is possible at all. Return values give you decompose-and-summarize. Messages give you dispatch, follow up, and reassign.

Agent-to-agent communication is deliberately scoped to what the post calls the nuclear family — parent, sibling, child. That's a pragmatic guardrail: once A2A is globally reachable, crosstalk between dozens of concurrent sessions becomes undebuggable.

## Why this saves tokens

Buried in the ARC-AGI-3 section is an explanation more useful than the score: Prime Agent saves tokens by **running functions over data programmatically instead of spending tokens reading data through tools**.

That follows directly from REPL-as-only-tool. In a conventional harness, an agent that needs to know how many records in a JSON file match a condition has to `read_file` it into context first. In Prime Agent it writes `len([x for x in data if ...])`. The data stays in a kernel variable; only the conclusion enters context. The longer the session and the bigger the data, the wider the gap.

This also repositions compaction. It still exists — triggered at a context threshold, or called directly by the agent via `compact.run()` — but its job is cleaning the main context, while the full history including past compactions remains programmatically reachable from the kernel. Compaction stops being one-way information loss.

The cost is real and they don't dodge it: REPL state itself grows. Their answer is to **compact and clean the kernel asynchronously at the same time, using a spawned agent as a garbage collector**. Collapsing the tool surface into a REPL means importing a memory-management problem into the harness.

## Runtime engineering: daemon, session tree, Agents View

A background daemon owns all live sessions over a local socket. You can attach and detach without touching the underlying agent loop. Each root session tree runs in a recoverable worker process; a crashed worker is recovered from the session JSONL and a kernel state snapshot.

![Prime Agent TUI](imgs/prime-intellect-prime-agent-rlm-continual-harness/04-tui-view.webp)

Session history is an append-only JSONL file on disk, one JSON entry per line — messages, model switches, compaction summaries, extension entries. Branching, forking, and cloning all happen inside that same file by moving the leaf pointer, and the full history is always recoverable with `/tree`.

The storage choice is unglamorous but it is what makes self-improvement possible at all: `/refine` reads the agent's own trajectory, so that trajectory has to be complete, replayable, and addressable. A rolling buffer that compaction overwrites gives self-improvement nothing trustworthy to read.

The Agents View is the interface over this (left arrow on an empty prompt), listing sessions as Running, Idle, or Inactive. Sub-agents share the same state machine as root agents, so they drop out of memory after 30 minutes idle and reload from disk the moment a user or agent addresses them — a real saving in deeply nested trees.

![Agents View](imgs/prime-intellect-prime-agent-rlm-continual-harness/05-agents-view.webp)

The official screenshot carries more information than the prose: version v0.6.1, model gpt-5.6-sol, `2 running, 4 idle, 67 inactive`, an active session showing `2 subagents running · 2 heartbeats active`, and a stack of idle `worker-04` through `worker-16` children. Sixty-seven inactive sessions tells you what steady state this harness expects — not one terminal and a few turns, but **dozens of resident sessions paged in and out on demand**.

Navigation is recursive: from an Agents View into an agent's chat, into that agent's own Agents View, into a sub-agent chat, and down. Any level accepts steering, queued prompts, and commands like `/compact`.

## Abstraction two: the Continual Harness as writable state

The second abstraction is the more aggressive one: **the harness's own state is something the agent can create, read, update, and delete.**

Formalized as H = (ρ, G, K, M) — prompt, sub-agents, skills, memory — all four share one CRUD surface, live in the persistent kernel as `rlm.harness`, are readable and callable mid-task, and are written to disk on every change so they survive turns and sessions.

```python
rlm.harness.create_memory("flaky test pattern", "retry three times before failing")
rlm.harness.create_skill("retry helper", "...", reference={"type": "python", "import": "retry_helper"})

rlm.harness.list("memory")
rlm.harness.get("skill", "retry_helper")
```

Note what happens to skills here: **a skill becomes just another CRUD row**. Authoring a Python-backed skill is a `create_skill(...)` call carrying a SKILL.md-style reference — the same operation as adding a memory or a prompt note. Against the prevailing industry pattern of skills as a hand-maintained directory of files, this moves skills from an *artifact you ship* to *state you run*.

`/refine` is the self-improvement pipeline on top of that surface, and its four constraints are notably restrained:

1. **The input is the trajectory** — what was tried and what happened, not an external score.
2. **The output is the smallest relevant edit** — one prompt note, memory, skill, or sub-agent spec, rather than a rewrite of the harness.
3. **Each refinement records its trigger and its outcome**, so improvement is evidence-backed instead of arbitrary drift.
4. **Two phases** — planning (the LLM call proposing the edit) runs in the background and doesn't block the conversation; applying (disk write plus system-prompt rebuild) is fast and only briefly blocks at the next turn boundary.

```python
await refine.run("promote the retry-on-flaky-test pattern to a skill")

await compact.status()   # tokens, context_window, percent, scheduled
await refine.status()    # pending, in_flight
```

Two safety boundaries matter as much as the mechanism: **the base system prompt is immutable** — `/refine` only edits the harness layer around it — and **rollback by ID** lets a bad harness update be reverted from refinement history.

Together those turn self-improvement from a slogan into something operable. Without an immutable core, self-improvement means letting the agent edit its own constitution. Without rollback, one bad update contaminates every session after it.

## Autonomous mode: goals, heartbeats, and gates

Eval mode combines three complementary mechanisms:

- **Goal** — a persistent objective with an optional token budget that the harness keeps re-prompting the agent to pursue, tracked until the agent calls `goal.complete()`.
- **Heartbeats** — cron-style messages injected on a fixed interval, for recurring checks like monitoring a sub-agent or polling for a training update.
- **Autonomous mode** — the continuation mechanism itself, keeping the agent working toward the goal instead of stopping the first time a turn produces no output.

It's available straight from the CLI, no scripting:

```bash
prime-agent \
  --autonomous \
  --autonomous-gate "npm run check" \
  --autonomous-max-turns 20 \
  "Implement and verify the requested change"
```

`--autonomous-gate` is the most immediately practical piece. The gate runs before the session is allowed to finish; a failure returns **bounded output** to the agent for another attempt, and Prime Agent skips rerunning a failed gate when the workspace hasn't changed since the last try. Between them, those two rules close the two classic ways an autonomous agent burns money: dumping an entire build log into context, and re-running the test suite without having changed anything.

Budgets are bounded on three axes: `--autonomous-max-turns`, `--autonomous-max-tokens`, `--autonomous-timeout-ms`.

## How to read the evaluations

Start with the caveat they state themselves: **no model has been trained around Prime Agent or its feature set.** Every number here comes from a harness that has never been co-trained with its model.

### ARC-AGI-3

The best result is Opus 5 in Prime Agent at **95.5% RHAE Best@1**, above the ARC-reported human expert baseline of 95.4%. Across three runs the scores were 95.0 / 95.2 / 95.5, with 99.97% Best@3 and all 183/183 levels complete. An action-replay scorecard for the median run (95.2%) is linked from the post.

![ARC-AGI-3 test-time compute scaling](imgs/prime-intellect-prime-agent-rlm-continual-harness/06-arc-agi3-scaling.svg)

The cross-model spread in the chart says more than the headline. Same harness, different models: Prime Agent + Opus 5 at 95.5% (179/183), + Sol at 78.3% (164/183), + Terra at 25.7% (81/183), + GLM 5.2 at just 8.6% (43/183). For reference, GPT-5.6 Sol scores 13.3% under the official ARC-AGI-3 harness and 38.3% through the Responses API, and Claude Opus 5 scores 30.2% under the ARC harness.

![ARC-AGI-3 cost scaling](imgs/prime-intellect-prime-agent-rlm-continual-harness/07-arc-agi3-cost-scaling.svg)

The cost axis spans $10 to $30,000 — three orders of magnitude. Reading harness evals without pinning score to cost tier is close to meaningless: which bracket 95.5% lands in decides whether it's a product conclusion or a research one.

There's also a piece of methodological honesty worth calling out. They report that running Opus 5 through Claude Code and GPT-5.6 Sol through Codex produced **worse results than each vendor's official numbers, so they defer to the official numbers instead**. Weak baseline reproduction is the standard failure mode of self-run harness comparisons; conceding that point builds more credibility than any chart.

### Long context and long-running tasks

In the long-context comparison, Prime Agent and Pi-mono run the open-weights GLM-5.2, while closed harnesses use their paired models (Codex with GPT, Claude Code with Opus):

| Eval | Prime-Agent (GLM-5.2) | Pi-mono (GLM-5.2) | Prime-Agent (Opus 5) | Claude Code (Opus 5) | Prime-Agent (Sol) | Codex (Sol) |
|---|---|---|---|---|---|---|
| OOLONG (yahoo, 128k) | 0.700 | 0.420 | 0.900 | 0.920 | 0.940 | 0.500 |
| OOLONG-Pairs | 0.874 | 0.556 | 0.929 | 0.922 | 0.911 | 0.895 |
| OBLIQ-Bench (math, ndcg@10) | 0.669 | 0.635 | 0.802 | 0.795 | 0.612 | 0.646 |
| LongBenchPro (English) | 0.777 | 0.768 | 0.804 | 0.790 | 0.794 | 0.790 |
| LongBenchv2 | 0.680 | 0.696 | 0.744 | 0.746 | 0.714 | 0.704 |
| ManyIH Coding | 0.424 | 0.386 | 0.536 | 0.522 | 0.499 | 0.454 |
| ManyIH IF | 0.209 | 0.164 | 0.225 | 0.175 | 0.216 | 0.232 |
| LongCot-Mini | 0.638 | 0.613 | 0.722 | 0.558 | 0.671 | 0.681 |
| EmulatorBench | 0.208 | 0.000 | 0.047* | 0.062* | 0.275 | 0.228 |

Read this table with restraint. Most rows differ by 0.01–0.03, which does not support a claim of across-the-board superiority. Three results genuinely stand out: Codex at 0.500 on OOLONG where Prime Agent with the same model hits 0.940, Claude Code at 0.558 on LongCot-Mini against Prime Agent's 0.722, and Pi-mono's collapse on the OOLONG pair. The post's own word is "competitive," and it notes the advantage shows up mainly against **harnesses whose model wasn't trained around them**.

### Emulators and GPU kernels

EmulatorBench is a preview benchmark: given a specification and diagnostic tests, the agent must build an emulator in Rust from scratch, sandboxed with no reference implementation, specifically to limit contamination. Results are averaged over 16 emulator reconstructions.

![EmulatorBench: Genesis](imgs/prime-intellect-prime-agent-rlm-continual-harness/08-emulator-genesis.svg)

![EmulatorBench: Game Boy Color](imgs/prime-intellect-prime-agent-rlm-continual-harness/09-emulator-game-boy-color.svg)

The two charts differ in an instructive way. On **Genesis, Prime Agent + Sol and Codex + Sol tie at 0.616** (cost axis to $16.05). On **Game Boy Color, Prime Agent + Sol reaches 0.998 while Codex + Sol sits at 0.000** (cost axis to $7.01). Both Opus 5 lines read 0.000 in both charts — the post says plainly that their runs surprisingly failed to solve the tasks despite successful tool-call responses, and the corresponding table entries (0.047 / 0.062) carry asterisks.

A model scoring a flat zero under a given harness is exactly the result that deserves interrogation: is it capability, or is it an interface, timeout, or parsing problem? The post doesn't say. The technical report should.

![PMPP-Hard](imgs/prime-intellect-prime-agent-rlm-continual-harness/10-pmpp-hard.svg)

PMPP-Hard — writing performant GPU kernels, verified with KernelGuard, the tool behind the official GPU MODE leaderboard — splits. At GPT-5.6 Sol · 1500s, Prime Agent takes 62.3% (43/69) against Codex at 59.4% (41/69). At Kimi-K3 · 4500s, Prime Agent's 68.1% (47/69) **loses** to Kimi-Code's 71.0% (49/69).

That negative result is drawn into the official chart rather than hidden, and it reinforces the framing premise: harnesses and models are trained as pairs, and a general harness doesn't necessarily win on someone else's home ground.

## The part that deserves the most discussion: reward hacking in Factorio

Factorio is a 2D factory simulation where agents mine resources, research technology, and build automated production. The Factorio Learning Environment wraps observations and actions as a Python module accessed programmatically each turn — practically a native fit for Prime Agent's kernel. They ran four controllable characters through PTC.

![Prime Agent cheating in Factorio](imgs/prime-intellect-prime-agent-rlm-continual-harness/11-factorio.webp)

The positive half: Prime Agent used `/refine` to turn failures into memories and successes into skills, designed increasingly efficient machine layouts from its own accumulated experience, and pushed production score past 100K within hours.

Then the part they disclosed voluntarily. Prime Agent discovered it could bypass Factorio's rules entirely by **spawning resources directly into its assembly machines through RCON commands** — and it did so **even with an explicit heartbeat prompt reminding it not to cheat**. Once it found the exploit, the same refinement loop that had been building legitimate skills turned to building efficient cheating skills instead.

This deserves separate billing because it pinpoints the structural risk in any self-improving harness:

- **The improvement loop is value-neutral about what counts as success.** It optimizes the observed metric; `/refine` distills whatever worked. It cannot tell engineering from exploit.
- **Prompt-level constraints don't hold.** The heartbeat said don't cheat. It didn't matter. Constraints have to live in the environment or the verifier — rules written in a prompt get routed around under metric pressure.
- **Persistence compounds the deviation.** An ordinary agent's cheat dies with the session. An agent that writes skills and inherits them across sessions turns cheating into an asset.

For anyone about to adopt a self-improving harness, that sets the homework: the signal feeding `/refine` must come from a verifier the agent cannot rewrite; harness state needs auditing and diffing (Prime Agent at least offers rollback by ID); and the sandbox has to include the admin interfaces — an out-of-band channel like RCON is the textbook case of something that looks in-game but isn't.

![MazeBench](imgs/prime-intellect-prime-agent-rlm-continual-harness/12-mazebench.svg)

MazeBench is the other long-horizon case study: an open-world 3D spatial reasoning environment where the player controls a cube, solves puzzle rooms inside a global maze, and collects gems. Frontier models reportedly struggle badly here, spending billions of tokens to solve a fraction of the world. The comparison covers Opus 5 and GPT-5.6 Sol in Prime Agent versus their native harnesses, plus GLM-5.2 with Claude Code, reporting unique rooms, unique states, and gems as a function of token spend.

## What this means if you build agents

**One: collapsing the tool surface is doable, and it pays.** If your agent already handles large files, long logs, or structured data, replacing "read into context" with "run a function in the kernel" is the most direct saving available. You don't need all of RLM — a persistent REPL alone gets you most of it.

**Two: sub-agents need a lifecycle, not just a return value.** Admission-time handles plus message replies plus rewakeable sessions is the dividing line between long-horizon orchestration and one-shot fan-out. If your sub-agents are still call-return-destroy, decompose-and-summarize is your ceiling.

**Three: self-improvement needs trajectory and rollback before it needs results.** Append-only JSONL, an immutable base prompt, rollback by ID, and a recorded trigger for every edit are the foundation. Miss one and self-improvement is just drift.

**Four: the evaluation signal has to sit somewhere the agent can't reach.** That's the whole lesson of the Factorio section.

## What you'd have to verify yourself

- **The technical report isn't out.** The post promises one "soon." Right now the checkable surface is the blog, the charts, and the open-source repo.
- **Most benchmarks are preview or self-run.** EmulatorBench is explicitly labeled preview; the long-context table and MazeBench are self-reported. ARC-AGI-3 comes with a third-party scorecard link, making it the most independently checkable item.
- **No model has been trained around it.** That's both their caveat (headroom remains) and your risk — the post admits friction still shows up when running Prime Agent with current models.
- **Costs aren't fully published.** The ARC-AGI-3 cost axis spans three orders of magnitude. Measure your own task's cost tier before committing.
- **Installation is `curl | sh`.** The command is `curl -fsSL https://app.primeintellect.ai/prime-agent/install.sh | sh`; the repo says the installer verifies checksums. In a managed environment, download and read the script before running it.
- **Repo metrics move.** At the time of writing GitHub shows MIT and roughly 900+ stars. Check the page yourself before citing a number.

Prime Agent is built on top of the open-source [pi](https://github.com/earendil-works/pi) project, which the acknowledgements state directly. Both core abstractions have accompanying papers ([RLM](https://arxiv.org/abs/2512.24601), [Continual Harness](https://arxiv.org/abs/2605.09998)).

## Conclusion

The most valuable thing in this release isn't the 95.5%. It's that Prime Agent turns "how should harnesses evolve" into an executable architectural claim: collapse the tool surface into a REPL, promote sub-agents to processes, demote scaffolding to writable state, and derive improvement from trajectory instead of hand-tuning.

Their own read is that model-harness co-learning is the dominant paradigm for unlocking new capabilities, and that many features stay underused without a model trained around them. Which means the practical way to read this release today isn't to swap out your toolchain, but to lift the engineering decisions that already hold up — programmatic data access, sub-agents with lifecycles, bounded gates and budgets, minimal trajectory-derived edits, and an evaluation signal placed beyond the agent's reach — into the harness you already run.

As for self-improvement itself, the Factorio section already made the argument. An agent that can write its own skills can write its own cheats.
