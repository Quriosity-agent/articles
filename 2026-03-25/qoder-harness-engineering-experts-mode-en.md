# How Qoder Builds Harness Engineering into Experts Mode

> Source: X Article by [@qoder_ai_ide](https://x.com/qoder_ai_ide/status/2036437931867644016)  
> Date: 2026-03-24

![Qoder Experts Mode](https://pbs.twimg.com/media/HELhagGaIAMymAI.jpg)
*Image credit: [@qoder_ai_ide](https://x.com/qoder_ai_ide) / X*

---

## The Competition Has Moved

Last month OpenAI published *Harness Engineering: leveraging Codex in an agent-first world*. The headline: 3 engineers (later 7), five months, zero hand-written code, one million lines of code, ~1,500 PRs. All agent-driven.

Around the same time, Stripe, Ramp, and Coinbase went public with the internals of their own coding agent systems.

The signal is clear: **the competitive edge has shifted from "model capability" to everything outside the model — Harness Engineering.**

## What Is Harness Engineering?

A quick analogy:

| Concept | Analogy |
|---------|---------|
| Model | CPU (raw compute) |
| Context Window | RAM (limited working memory) |
| Agent Harness | Operating System (manages context, startup routines, standard drivers) |
| Agent | Application (runs on the OS) |

A Harness sits above an Agent Framework. Frameworks give you building blocks: tool calling, agentic loops. A Harness gives you the rest — prompt presets, standardized tool invocation, lifecycle hooks, and the production capabilities you actually need: planning, file system access, sub-agent coordination, verification loops.

**Harness Engineering = control system design for AI Agents.** The goal: build infrastructure so the agent writes correct code consistently, across long-running iterations, in a way you can audit, roll back, and extend.

## Industry Landscape

Harness Engineering is already in production at top engineering organizations:

- **Stripe** — forked Block's Goose, built Blueprint (a state machine alternating deterministic and agentic nodes), merges 1,300+ fully agent-authored PRs per week
- **Shopify** — open-sourced Roast, interleaving AI steps with deterministic code
- **Ramp** — built Inspect on OpenCode, running sessions in Modal sandboxes with parallel execution; 30% of merged PRs are agent-written
- **Coinbase** — built Cloudbot from scratch, compressing PR review from 150 hours to 15
- **OpenAI** — pushed "zero hand-written code" to million-line scale with Codex

Each team solved real problems: sandbox isolation, context pre-hydration, deterministic orchestration. But they all share one structural constraint: **the agent is still monolithic** — one model instance, one context window, one execution path.

## Five Structural Limits of Single-Agent Harness

1. **Context window as zero-sum game** — Research, coding, testing, and review context all compete for the same window. More complex tasks → lower information density.
2. **Cognitive overhead of role-switching** — An agent constantly switching between architecture research, implementation, and test execution is like asking one person to be Tech Lead, SWE, QA, and Code Reviewer simultaneously.
3. **Drift in long execution chains** — The longer the chain, the higher the probability of drifting from the original goal. Without external checkpoints, errors propagate and compound.
4. **Missing functional correctness verification** — Current practices focus on internal quality but underinvest in verifying the product actually works. A codebase can be architecturally clean, lint-free, and well-documented while the business logic is wrong.
5. **Terminal execution risk** — A single mistaken shell command can cause irreversible damage. Blocklists are easy to bypass; confirmation dialogs get blindly clicked through.

## Qoder Experts Mode: The Architecture

Qoder's answer is upgrading from a single agent to a **multi-expert collaboration system**. Internal benchmarks: **67% higher quality than single-agent mode, at less than 2/3 the cost.**

### 1. Coordination Separated from Execution

The Leader coordinates — it never implements. It receives requirements, decomposes tasks, manages dependencies, tracks progress, and reports results. From a Harness Engineering perspective, the Leader is a meta-Harness: it manages a set of specialized Agent Harnesses, each with its own toolset, context strategy, and execution constraints.

### 2. Async Parallelism: DAG-Driven Task Orchestration

All SWE Agents run asynchronously in parallel by default. Dependencies form a lightweight DAG: "Implement backend API" and "Build frontend page" run in parallel; "Integration test" waits for both. Each expert works in its own isolated context window — the zero-sum problem disappears.

### 3. Star Topology: Centralized Coordination

SWE Agents don't communicate directly. All coordination routes through the Leader. Qoder considered peer-to-peer early on and rejected it — when agents talk to each other, nobody holds the complete picture. Two experts can make contradictory decisions and no one notices. Users are also in the coordination path: they can insert new instructions at any time.

### 4. Specialized Roles: Each Expert Is Its Own Harness

**This is the design choice that matters most to final output quality.** Each expert is a separate Harness tuned for a specific task type — different toolsets, different context injection strategies, different execution constraints. Not just swapping a system prompt — the entire Harness is different.

Each expert's context window contains only role-relevant information. This is how Qoder deals with Context Rot — role isolation eliminates context competition at the source, which works better than any compression strategy they tried.

### 5. Cross-Model Scheduling

Since each expert runs independently, each can use a different model:

- **Researcher** — strongest reasoning model for synthesis across search results
- **Dev** — best code generation model
- **Browser** — multimodal model, with lightweight fallback for simple verification
- **Reviewer** — model most sensitive to security and performance issues

The Leader matches task types to model capabilities. Quality and cost improve simultaneously: precise model-task matching avoids paying for capabilities you don't need.

> Internal benchmarks: 67% higher quality vs Agent Mode, 16% higher quality vs Claude Code Agent Teams, at less than 2/3 the cost.

### 6. Functional Correctness Verification

Most Harness systems can tell you whether code is clean. Fewer can tell you whether the product actually works. Qoder built three verification experts:

- **Browser Expert** — runs E2E verification against real user flows in a real browser, checking interaction flows, page rendering, and visual regression
- **QA Expert** — uses change-aware context to scope verification to code actually affected by the current change
- **Code Reviewer Expert** — semantic diff + call-chain analysis to catch side effects that look fine in isolation

Verification triggers right after coding completes — errors get caught before spreading to downstream tasks.

### 7. Self-Evolution: From Static Harness to Dynamic Learning

Traditional Harness systems are static. Qoder Experts introduces task-level skill extraction: when the system detects a correction, a recovered failure, or an explicit user instruction, the Leader and each SWE Agent independently extract reusable skills from their domains.

These skills persist in a memory system and get recalled automatically on similar tasks. Over time, the system stops making mistakes it has already learned from.

### 8. Terminal Execution Safety

Shell syntax varies dramatically across OSes. Qoder built independent AST parsers for each shell (PowerShell, Bash/Zsh, Cmd) that penetrate command nesting to identify every sub-command that will actually execute.

After parsing, commands go through three independent risk checks:
1. Hard-coded blocklist (known dangerous commands)
2. Rule engine (individually harmless but dangerous in combination)
3. LLM semantic analysis (reads command intent, catches what the first two miss)

Any single trigger blocks execution. Commands that pass all three still run inside OS-level sandboxes.

## Analysis

Qoder's core thesis is clear: **when we want agents to collaborate like an engineering team, the Harness needs to evolve from wrapping a single model to organizing a team.**

Key design choices worth noting:

- **Star topology over P2P** — simplifies state tracking, but the Leader becomes a single point of bottleneck
- **Role isolation to eliminate Context Rot** — a more fundamental fix than compression strategies
- **Cross-model scheduling** — a natural advantage of multi-agent architecture that single-agent systems can't replicate
- **Triple-layer safety checks** — significantly more robust than blocklists or confirmation dialogs alone

The 67% quality improvement is impressive, though the specific benchmark methodology isn't public yet. Looking forward to more details.

Regardless, Qoder has taken Harness Engineering from concept to product in a very practical way.

---

🦞
