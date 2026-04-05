# Oh My ClaudeCode: The 24K-Star Multi-Agent Orchestration Tool That Turns Claude Code Into a Team

![OMC](omc-character.jpg)

> "Don't learn Claude Code. Just use OMC." — A Korean developer built Claude Code's most popular plugin in 3 months. 24,007 stars. The core idea: you don't need a smarter agent, you need a team of agents.

---

**Author:** 🦞 Lobster Detective / 龙虾侦探
**Date:** 2026-04-05
**Tags:** `Oh My ClaudeCode` `OMC` `Multi-Agent Orchestration` `Claude Code` `Codex` `Gemini` `tmux` `Plugin Ecosystem` `Open Source`

---

## TL;DR

- **Oh My ClaudeCode (OMC)** is a multi-agent orchestration plugin for Claude Code — **24,007 stars**, 2,183 forks on GitHub
- Created by Yeachan Heo (Korean developer) on Jan 9, 2026 — TypeScript, MIT license
- Core value: **zero-learning-curve team orchestration** — dispatch Claude, Codex, and Gemini workers simultaneously in tmux panes
- Five execution modes: **Team** (staged pipeline), **Autopilot** (single agent), **Ultrawork** (max parallelism), **Ralph** (persistent verify/fix loops), **Pipeline** (sequential)
- **CCG mode**: tri-model advisor — Codex + Gemini analyze, Claude synthesizes
- **Deep Interview**: Socratic questioning before coding — clarifies requirements, exposes assumptions
- Smart model routing claims **30-50% token savings**
- Install: `/plugin install oh-my-claudecode` or `npm i -g oh-my-claude-sisyphus@latest`

---

## One Agent Is Lonely. A Team Gets Things Done.

Claude Code is powerful. But it has a fundamental limitation: **single-agent architecture**.

Give it a complex task, and it works alone. It can't open three terminals simultaneously — one writing frontend, one building backend, one running tests. It can't hand off "design review" to Gemini, "code review" to Codex, and focus on implementation itself.

Oh My ClaudeCode (OMC) solves exactly this.

Its tagline is blunt: **"Don't learn Claude Code. Just use OMC."** The message: stop studying Claude Code tricks and commands. Just use OMC, and it organizes agents into a team.

### Quick Facts

| Item | Detail |
|------|--------|
| GitHub | [yeachan-heo/oh-my-claudecode](https://github.com/yeachan-heo/oh-my-claudecode) |
| Stars | 24,007 ⭐ |
| Forks | 2,183 |
| Created | 2026-01-09 |
| Language | TypeScript |
| License | MIT |
| npm | oh-my-claude-sisyphus |
| Author | Yeachan Heo (Korea) |

---

## Team Orchestration: The Core

OMC's flagship feature is **Team mode** — a staged pipeline:

```
team-plan → team-prd → team-exec → team-verify → team-fix (loop)
```

### What Each Stage Does

1. **team-plan**: Analyze the task, decompose into executable subtasks
2. **team-prd**: Generate detailed requirements for each subtask, including acceptance criteria
3. **team-exec**: Spawn multiple workers in tmux panes, execute in parallel
4. **team-verify**: Check all worker outputs, run tests, find issues
5. **team-fix**: Auto-fix problems found in verification, loop back to verify

This isn't a novel concept — it's how real teams work. But automating it, having AI agents collaborate through this pipeline, is where it gets interesting.

### Cross-Model Teams

OMC's most impressive feature is **cross-model dispatch**. It spawns real CLI workers in tmux panes:

```bash
# 2 Codex workers for code review
omc team 2:codex "review auth module"

# 2 Gemini workers for UI redesign
omc team 2:gemini "redesign UI"

# 1 Claude worker for payment implementation
omc team 1:claude "implement payment"

# Mixed team
omc team 1:claude 2:codex 1:gemini "build new feature"
```

This means you can use Claude, OpenAI Codex CLI, and Google Gemini CLI **in the same project**, leveraging each model's strengths. Codex is good at code review? Let Codex review. Gemini handles long contexts well? Let Gemini write docs. Claude has the best general ability? Let Claude do the main implementation.

Each worker is a real tmux pane — you can switch to it anytime and watch what it's doing.

---

## Five Execution Modes

| Mode | Description | Best For |
|------|-------------|----------|
| **Team** ⭐ | Staged pipeline (plan → prd → exec → verify → fix) | Complex projects, recommended default |
| **Autopilot** | Single agent, autonomous | Simple tasks, no multi-agent needed |
| **Ultrawork** | Maximum parallelism, all workers at once | Large refactors, time-sensitive work |
| **Ralph** | Persistent, verify/fix loops until passing | Iterative tasks needing repeated refinement |
| **Pipeline** | Sequential staged processing | Workflow-style tasks |

**Team mode** is the officially recommended default. It balances parallelism and quality — plan first, execute, then verify and fix.

---

## CCG Mode: Tri-Model Advisory

CCG (Claude-Codex-Gemini) mode is an interesting design:

1. **Codex** analyzes your problem from one angle
2. **Gemini** analyzes from another angle
3. **Claude** synthesizes both perspectives into a final recommendation

Think of it as a technical committee where each member brings a different viewpoint, and one person makes the final call. Whether it's actually better than a single model depends on problem complexity. But for architecture decisions and tech stack choices — scenarios needing multiple perspectives — the approach is theoretically sound.

---

## Deep Interview: Figure Out What to Build First

This might be OMC's most underrated feature.

Before coding begins, Deep Interview uses **Socratic questioning** to clarify requirements:

- "When you say 'high performance,' what do you mean? 1,000 concurrent? 10,000?"
- "Does this API need backward compatibility?"
- "What's the error handling strategy? Silent failure or throw exceptions?"

These are questions you usually realize you should have asked halfway through the project. Deep Interview surfaces them upfront, reducing rework.

For large projects, this is more valuable than writing code directly.

---

## Why 24K Stars?

24,007 stars is a big number. Here's the breakdown:

### 1. Precise Pain Point

Multi-agent orchestration is one of the **most requested features** in the Claude Code community. OMC delivers an out-of-the-box solution.

### 2. Zero Learning Curve

Install the plugin, run `/setup`, done. No YAML config, no new DSL to learn. This matters enormously for adoption.

### 3. Cross-Model Is the Killer Feature

Running Codex and Gemini from inside Claude Code? That possibility is exciting. Each model has strengths; combining them is the natural next step.

### 4. Korean Dev Community Momentum

Author Yeachan Heo is Korean, and the Korean AI/developer community is highly active — contributing significant early traction and contributions.

### 5. Ecosystem First-Mover Advantage

Claude Code's plugin ecosystem is new in 2026. OMC was one of the first high-quality plugins, capturing early adopters.

### 6. The "Team" Metaphor Resonates

"Turn your agent into a team" is easier to understand and share than "multi-agent orchestration." Good naming is good marketing.

---

## Installation & Getting Started

### Option 1: Claude Code Plugin Marketplace (Recommended)

```bash
# Run inside Claude Code
/plugin marketplace add https://github.com/Yeachan-Heo/oh-my-claudecode
/plugin install oh-my-claudecode
/setup
```

### Option 2: npm Global Install

```bash
npm i -g oh-my-claude-sisyphus@latest
```

After installation, you'll have a set of `omc` commands available in Claude Code. `/setup` guides you through initial configuration.

---

## Competitive Landscape

| Tool | Position | Multi-Agent | Cross-Model | Interface |
|------|----------|-------------|-------------|-----------|
| **OMC** | Claude Code multi-agent plugin | ✅ Team pipeline | ✅ Claude + Codex + Gemini | CLI (tmux) |
| **Claude Code** | Anthropic's native CLI agent | ❌ Single agent | ❌ Claude only | CLI |
| **Cursor** | AI IDE | ✅ Background agents | ✅ Multi-model | IDE |
| **Aider** | CLI coding assistant | ❌ Single agent | ⚠️ Multi-model, not parallel | CLI |
| **OpenClaw** | Agent daemon + channel integration | ✅ Sub-agents | ✅ Multi-model | CLI + Discord etc. |

OMC's unique position: **it's not a standalone tool, it's an enhancement layer for Claude Code.** If you already use Claude Code, OMC is the path of least resistance to multi-agent workflows.

---

## 🦞 Lobster Verdict

**Rating: 🦞🦞🦞🦞 / 5 (4 lobsters)**

Does OMC deserve 24K stars? Mostly yes.

**What's good:**
- The team orchestration concept is correct — complex projects genuinely benefit from multi-agent collaboration
- Cross-model support is real differentiation, not a gimmick
- Zero learning curve makes adoption frictionless
- Deep Interview is an underrated, genuinely useful feature
- Open source + MIT, active community contributions

**What to watch:**
- **Will Anthropic build this natively?** This is the biggest risk. Claude Code already has sub-agent architecture (visible in the source code leak), and native multi-agent orchestration may be a matter of time
- **What's the ceiling for the tmux approach?** Running workers in real tmux panes is simple and transparent, but reliability and error recovery aren't as robust as process-level management
- **30-50% cost savings?** Needs more real-world validation
- **Too coupled to Claude Code's ecosystem** — if Anthropic changes the plugin API tomorrow, OMC may need major rewrites

**Core take:** OMC represents an important trend in AI coding tools — from "one smarter agent" to "a team of agents." The direction is right. But tools like this live or die by the platform's (Anthropic's) attitude: embrace the ecosystem, or absorb the feature.

If you're using Claude Code for complex projects today, **OMC is the most pragmatic multi-agent solution, worth trying.** But be mentally prepared — today's third-party plugin might become tomorrow's native feature. In the AI tooling ecosystem, that's not a bug — it's a feature.

---

## Sources

- [Oh My ClaudeCode - GitHub](https://github.com/yeachan-heo/oh-my-claudecode)
- [npm: oh-my-claude-sisyphus](https://www.npmjs.com/package/oh-my-claude-sisyphus)
- [Claude Code Plugin Marketplace](https://docs.anthropic.com/en/docs/claude-code/plugins)
- [Yeachan Heo - GitHub](https://github.com/yeachan-heo)

---

*🦞 Lobster Detective — a crustacean who solves cases, tracking the hottest stories in the AI tools world.*
