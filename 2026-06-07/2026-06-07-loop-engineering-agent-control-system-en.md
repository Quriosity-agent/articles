---
title: "Loop Engineering Deep Dive: In the Agent Era, the Real Design Target Is Not the Prompt but the Self-Driving Control System"
date: 2026-06-07
source: "https://x.com/addyosmani/status/2064127981161959567?s=20"
canonical: "https://addyosmani.com/blog/loop-engineering/"
x_article: "https://x.com/i/article/2064122477731852288"
author: "Addy Osmani"
tags:
  - Loop Engineering
  - AI Agents
  - Coding Agents
  - Codex
  - Claude Code
  - Agent Harness
  - Agentic Software Engineering
---

# Loop Engineering Deep Dive: In the Agent Era, the Real Design Target Is Not the Prompt but the Self-Driving Control System

Addy Osmani posted and shared [**Loop Engineering**](https://addyosmani.com/blog/loop-engineering/) on X. The article turns a set of recent AI-coding one-liners into a concrete engineering frame. Peter Steinberger argued that developers should stop merely prompting coding agents and start designing the loops that prompt them. Boris Cherny, who leads Claude Code, said he no longer directly prompts Claude; he writes loops that prompt Claude and figure out what to do next.

This is not just “prompt engineering with a new label.” The real shift is a transfer of control: **the human is no longer manually acting as scheduler, context manager, tester, and reviewer turn by turn. Those actions move into a repeatable, observable, stoppable, and accountable control system.**

For tools such as QCut, OpenClaw, Hermes, Claude Code, and Codex, this matters a lot. Once an agent can keep editing code, running tests, opening PRs, reading issues, checking logs, and sending messages, the bottleneck is no longer whether one answer is smart enough. The bottleneck becomes: who discovers the work, who isolates the change, who verifies success, what happens after failure, and when must control return to a human? The answers to those questions are loop engineering.

## The one-sentence version

**Loop engineering upgrades “what should I prompt the agent next?” into “what system should I design so the agent can keep working toward a goal, on a cadence, with verification?”**

Addy’s definition is direct: loop engineering means replacing yourself as the person who prompts the agent. The system does it instead. A loop is a recursive goal: you define an objective, and the AI system executes, observes, corrects, and repeats until the goal is complete or a handoff condition is triggered.

That is very different from classic prompt engineering:

| Layer | What you design | Typical question |
|---|---|---|
| Prompt Engineering | A single instruction | “What should I say to get a good answer?” |
| Context Engineering | The context window | “Which files, rules, history, and constraints should the model see?” |
| Harness Engineering | One agent’s runtime | “What tools, permissions, sandbox, memory, and feedback does the agent have?” |
| Loop Engineering | The system that repeatedly starts and verifies agents | “How does the system discover work, assign it, check results, record state, and continue?” |
| Orchestration | Multiple loops or agents as an organization | “How do parallel tasks, PRs, CI, review, and deployment become a production line?” |

Loop engineering does not eliminate prompts. It moves prompts from manual input into a larger operating system.

## Addy’s five pieces, plus external memory

Addy breaks a working loop into five primitives plus a state/memory layer:

1. **Automations**: scheduled discovery, inspection, and triage;
2. **Worktrees**: isolated directories and branches so parallel agents do not overwrite each other;
3. **Skills**: reusable project knowledge, conventions, and hard-won lessons;
4. **Plugins / Connectors**: real tool access through MCP, APIs, Slack, Linear, GitHub, databases, and so on;
5. **Sub-agents**: separate agents for ideation, implementation, and verification;
6. **State / Memory**: Markdown files, Linear boards, issues, run logs, or databases that record what has been done and what comes next.

The sixth item is easy to underestimate. Addy’s line is exactly right: **“The agent forgets, the repo doesn’t.”** Models forget, sessions end, and context gets compressed. Repositories, state files, issue boards, and run logs persist. Without external state, every loop starts by guessing the world again. With external state, a loop can become an ongoing engineering process rather than a smart one-shot execution.

## Why it matters now: the primitives are becoming product features

A year ago, building this kind of loop usually meant maintaining a pile of glue code: cron, shell scripts, `git worktree`, CI hooks, log parsers, API calls, PR creation, Slack notifications, and state-file updates. It could work, but it was brittle and understood only by the person who wrote it.

Addy’s observation is that these capabilities are moving from custom glue into first-class AI-coding products. His article maps Codex app and Claude Code like this:

| Primitive | Job in the loop | Codex app | Claude Code |
|---|---|---|---|
| Automations | Scheduled discovery and triage | Automations tab, Triage inbox, `/goal` | scheduled tasks, cron, `/loop`, `/goal`, hooks, GitHub Actions |
| Worktrees | Isolate parallel changes | built-in worktree per thread | `git worktree`, `--worktree`, subagent worktree isolation |
| Skills | Codify project knowledge | `SKILL.md` Agent Skills | `SKILL.md` Agent Skills |
| Connectors | Reach external tools | MCP connectors, plugins | MCP servers, plugins |
| Sub-agents | Separate maker and checker | TOML subagents in `.codex/agents/` | `.claude/agents/`, agent teams |
| State | Track progress | Markdown, Linear, memory | Markdown, `AGENTS.md`, Linear/MCP, memory |

That means loop engineering is not a proprietary feature of one tool. It is a cross-tool architectural shape. Product names will change, but the stable primitives are likely to remain: trigger, isolation, skill, connector, sub-agent, state, verification, and stopping condition.

## `/loop` versus `/goal`: metronome versus completion contract

One useful distinction in the article is that `/loop` and `/goal` are not the same thing.

- **`/loop` is closer to a metronome**: rerun a task every so often, such as checking CI hourly, summarizing issues daily, or scanning recent changes on a schedule.
- **`/goal` is closer to a completion contract**: give the agent a verifiable target and let it continue across turns until that target is met, such as “all tests under `test/auth` pass and lint is clean.”

The latter is where much of the engineering value sits. AI agents usually do not fail because they cannot start. They fail because they do not reliably know when to stop. Without a clear stopping condition, a loop tends to either declare victory too early or retry forever while burning tokens.

A good `/goal` is therefore not “fix auth.” It looks more like this:

```text
Goal: Fix the recently introduced session refresh bug in the auth module.
Success criteria:
1. `pnpm test test/auth/session-refresh.test.ts` passes;
2. `pnpm lint --filter auth` passes;
3. Do not change the public API unless the PR description explains why;
4. After three failed attempts, write the logs and assumptions into `loop-run-log.md` and stop.
```

That is loop engineering: goal, verification, boundary, stopping rule, and handoff.

## Worktrees are the foundation of agent parallelism

As soon as multiple agents edit the same repository, the first thing to break is usually not intelligence but file collision. Two agents modifying the same files in the same checkout is no better than two engineers committing into the same uncoordinated workspace.

This is why `git worktree` becomes more than a Git trick. It is the safety foundation for an agent factory. Each agent gets an independent checkout, branch, and test environment. If it fails, it pollutes only its own workspace.

But worktrees solve mechanical conflict, not product judgment. Addy’s “orchestration tax” is real here: you can run ten agents in parallel, but you may not be able to review ten PRs. **Parallelism moves the bottleneck from code generation to human review, integration, and decision-making.** If that bottleneck is not designed, more agents simply create more review debris.

## Skills move project intent out of human memory

In a single chat, a human can keep adding project context: do not touch this directory, run tests this way, this API has history, this UI should match that component. A loop runs unattended, so it cannot rely on a human being there every time to patch missing context.

Skills become the loop’s long-term intent layer. They put project knowledge into `SKILL.md`, references, scripts, and templates so every run reads the same constraints. Examples include:

- code style and directory boundaries;
- common test commands;
- architecture red lines;
- release steps;
- review checklists;
- previous incidents and pitfalls.

For Peter’s Hermes and QCut workflows, a skill is not a prompt collection. It is closer to a team operating manual. Without skills, the loop re-infers the project every cycle. With skills, the loop compounds knowledge.

## The value of sub-agents: separate the maker from the grader

Addy emphasizes sub-agents because the agent that wrote the code should not be the only judge of whether it is done. Models are often too generous toward their own outputs, especially after many repair attempts.

A better structure is:

1. an explorer reads the code, locates the problem, and proposes an approach;
2. an implementer makes the change;
3. a verifier reads only the spec, diff, tests, and logs, and tries to reject the result;
4. a human reviewer handles product tradeoffs the verifier cannot decide.

That is the maker-checker split. It costs more tokens, but in an unattended loop it is often worth it because it gives the word “done” some meaning.

## What a practical loop looks like

Put the pieces together and a small software team can start with a very modest loop:

1. a morning automation starts;
2. it reads yesterday’s CI failures, open issues, and recent commits;
3. it calls a triage skill and writes candidate tasks into `loop-state.md`;
4. it opens one worktree for each small task;
5. an implementer agent attempts the fix;
6. a verifier agent checks tests, lint, diff, and the skill checklist;
7. if the result passes, the loop opens a PR and updates the Linear/GitHub issue;
8. if the result is uncertain or failed, the loop writes to a triage inbox for a human;
9. the next run continues from the state file instead of starting over.

This is not science fiction and it does not require a super-agent. It is more like the next layer after CI/CD. CI/CD automates build, test, and deployment. Loop engineering automates discovery, repair, verification, and handoff.

## Implications for QCut, OpenClaw, and Hermes

The article maps directly onto several things Peter is building or operating:

- **QCut**: a video-generation pipeline is already a loop across scripts, assets, shots, audio, subtitles, preview, export, and retry. The hard part is designing success criteria and recoverable state at each step, not writing one giant “generate a video” prompt.
- **OpenClaw**: the value of multi-agent coding is not merely running many Codex sessions. It is giving each agent a worktree, budget, scope, reviewer, and stopping condition.
- **Hermes**: cron jobs, skills, memory, toolsets, and Discord delivery are already a loop runtime. The key is to give every job external state, verification, and failure reporting rather than merely “call the model on a schedule.”
- **Article automation**: turning an X link into an article can itself be looped: parse the source, resolve the canonical page, preserve media, write bilingual versions, update README/MOC, commit and push, then verify GitHub links.

In other words, loop engineering is not only for coding agents. Any workflow where AI repeatedly processes tasks, checks results, records state, and decides the next step can be redesigned through this frame.

## The dangerous misunderstanding: a loop is not full self-driving

Addy’s most important warning is not that loops are powerful, but that loops make mistakes happen faster. He names three risks:

1. **Verification is still your responsibility**: an unattended loop can make unattended mistakes;
2. **Comprehension debt grows**: the faster agents write code, the easier it is for human understanding to fall behind;
3. **Cognitive surrender is dangerous**: if humans only press start and accept the result, the loop becomes a tool for avoiding thought.

This is the key point. A good loop does not remove the engineer. It upgrades the engineer from manually pushing every turn to designing the control system, defining acceptance criteria, handling exceptions, and reviewing consequential decisions.

If a team has no tests, logs, permission boundaries, state, or review process, then an hourly agent that edits code is not loop engineering. It is an automated incident generator.

## My take: prompts remain, but the leverage has moved upward

Prompt engineering will not disappear. We still need clear goals, constraints, context, and evaluation criteria. But the highest leverage point has moved from “how elegant is this one prompt?” to “can this system keep producing verifiable results?”

The valuable AI-engineering questions now look more like these:

- Which tasks deserve a loop, and which must remain human-driven?
- What is the success condition for each loop?
- How many failures before stopping?
- Where is state written?
- Who has permission to change what?
- How is the verifier independent from the maker?
- What are the token and time budgets?
- How does the result enter a PR, issue, document, or user-facing product?

Addy’s closing principle is the right one: **Build the loop. Stay the engineer.**

That is why loop engineering deserves serious attention. It is not a slogan about letting AI work for you. It is a reminder that once agents can keep acting, the real engineering problem is to make their actions controllable, inspectable, stoppable, and recoverable.
