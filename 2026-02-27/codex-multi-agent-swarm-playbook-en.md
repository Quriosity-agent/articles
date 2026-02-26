# Codex Multi-Agent Swarm Playbook: The Complete Framework from Planning to Parallel Execution

> **TL;DR**: @LLMJunky's Codex Multi-Agent Playbook Part 3 — Swarms in practice. Core methodology: **Plan.md eliminates ambiguity → dependency graphs drive orchestration → context engineering front-loads subagents → standardized prompt templates ensure consistency**. Two parallel strategies: Swarm Waves (dependency-ordered waves, accuracy-first) and Super Swarms (total parallelism, speed-first). The key insight: it's not about spawning more agents — **the quality of context you give each agent determines everything**.

---

## 📚 Series Context

This is Part 3 of the Codex Multi-Agent Playbook (Swarms Level 1):
- **Part 1**: Subagent fundamentals — Orchestrator vs Worker differences
- **Part 2**: Custom agent roles — model selection, reasoning levels, prompt writing
- **Part 3 (this)**: Swarm practice — the complete multi-agent parallel framework

## 🏗️ Step 1: Plan.md — Ambiguity Is the Enemy

> "One agent drifting is annoying. Five agents drifting in parallel is a disaster."

Swarm success depends on planning quality. Every vague requirement, every unclear acceptance criteria multiplies across all parallel agents.

**Key principles:**
- You are the **architect**, agents are the **builders**. An architect who doesn't understand the blueprint burns tokens
- Most time should be spent crafting a **detailed, clear, intentional** spec
- If unsure about tech choices, **open another agent session to discuss options** — don't blindly accept the first suggestion

**Must include dependency graph:**
```
This plan MUST include a dependency graph.
Every task declares `depends_on: []` with explicit task IDs `T1, T2`
```

## 🔄 The Orchestration Layer

The Orchestrator is the swarm's core, responsible for:

1. **Managing plan implementation state**
2. **Spawning subagents as needed**
3. **Providing subagent prompts**
4. **Validating subagent work**
5. **Resolving conflicts**
6. **Keeping the project moving forward**

The Orchestrator holds full context: the complete plan, every agent's state, all file paths, overall project status. Like a foreman on a job site — doesn't need to worry about minutiae, just keeps things on the right path.

**Important:** Don't reset context after planning! The orchestrator needs all that planning context.

## ⚡ Two Swarm Strategies

### Swarm Waves — Accuracy First

Launch only currently **unblocked** tasks per wave:
- 1 unblocked task → spawn 1 agent
- 8 unblocked tasks → spawn 8 agents
- Dependencies complete → next wave auto-launches

**Advantage:** Fewest conflicts, tasks execute in expected order.
The dependency graph makes this work — the orchestrator knows exactly which tasks can run in parallel.

### Super Swarms — Speed First

Launch as many agents as possible regardless of dependencies:

```toml
[agents]
max_threads = 16  # Up to 16 parallel agents
```

**Advantage:** Extremely fast
**Cost:** More conflicts (dependency files may not exist yet)
**But:** The orchestrator is usually adept at resolving conflicts on the tail end

> ⚠️ Codex defaults to max 6 parallel agents. Too many may trigger 429 errors.

## 🎯 The Secret Sauce: Context Engineering

**This is the most important section.**

> "It's not about spawning more agents. The quality of context you give each agent determines everything."

The problem: Agents have **amnesia**. Drop one into a codebase with minimal context, and it'll burn tokens calling tools and reading files to discover context before it can even start working.

The solution: **Front-loading** — pack every meaningful detail into the subagent's initial prompt.

### The Subagent Prompt Template

```markdown
You are implementing a specific task from a development plan.

## Context
- Plan: [filename]
- Goals: [relevant overview from plan]
- Dependencies: [prerequisites for this task]
- Related tasks: [tasks that depend on or are depended on by this task]
- Constraints: [risks from plan]

## Your Task
**Task [ID]: [Name]**
Location: [File paths]
Description: [Full description]

Acceptance Criteria: [List from plan]
Validation: [Unit Tests or verification from plan]

## Instructions
1. Examine working plan and any relevant or dependent files
2. Implement changes for all acceptance criteria
3. Keep work atomic and committable
4. For each file: read first, edit carefully, preserve formatting
5. Run validation if feasible
6. Mark completed tasks in the plan file
7. Commit your work (ONLY COMMIT, NEVER PUSH)
8. Return summary of changes made
```

**Each agent knows:**
- What the task is and its place in the larger spec
- Which files it depends on (full paths)
- Where the plan file is
- Project state
- File names and paths to work on
- Related tasks and their function
- Acceptance criteria and testing methodology

### Especially Critical for Small Models

This is crucial for fast models like **Spark** (128K context):
- Not good at long-context or back-and-forth conversation
- **Excellent at completing singular, well-defined tasks**
- Front-loading reduces tool calls, compensating for lower accuracy

## 🧮 Model & Reasoning Configuration

```toml
model = "gpt-5.3-codex"
plan_mode_reasoning_effort = "xhigh"    # Planning: max reasoning
model_reasoning_effort = "high"          # Orchestration: high reasoning

[agents]
max_threads = 16

[agents.sparky]
config_file = "agents/sparky.toml"
description = "Use for executing implementation tasks from a structured plan."
```

| Phase | Pro Subscription | Plus/Business |
|-------|-----------------|---------------|
| **Planning** | GPT 5.2 High / 5.3-Codex High | GPT 5.2 High / 5.3-Codex High |
| **Orchestration** | 5.3-Codex High | 5.3-Codex Medium |
| **Subagents** | Spark xHigh / 5.3-Codex High | 5.3-Codex Medium |

Core rule: **Orchestration must use large models**. Subagents can use smaller models with good context engineering.

## 💡 Key Insights

1. **Planning > Execution** — 80% of time on Plan.md, 20% on execution
2. **Dependency graphs are mandatory** — foundation for Swarm Waves
3. **Don't reset orchestrator context** — planning context IS orchestration context
4. **Context engineering isn't a buzzword** — it's the make-or-break factor
5. **Front-loading saves tokens** — cheaper than letting agents explore
6. **Commit only, never push** — parallel agents commit individually, push at the end
7. **Codex is the most steerable model** — tell it what to do, and it does it

## 🔗 Resources

- **Original**: <https://x.com/LLMJunky/status/2027032974202421336>
- **Author**: @LLMJunky (am.will) — Founder, StarSwap
- **Series**: Codex Multi-Agent Playbook Parts 1-3
- **Swarm Planner Skill & Sparky Agent**: Author's GitHub

## 💭 Why This Matters

The core insight applies to ALL multi-agent systems, not just Codex:

**"Agents aren't better in quantity — context quality is everything."**

Whether you're using Codex, Claude Code Agent Teams, or OpenClaw's sessions_spawn, the principles are the same:
- Clear planning eliminates ambiguity
- Dependency graphs drive parallelism
- Front-loading context reduces wasted exploration
- Standardized prompt templates ensure consistency

This is the difference between toy multi-agent demos and production-grade multi-agent systems.

---

*Author: 🦞 Bigger Lobster*
*Date: 2026-02-27*
*Original author: @LLMJunky (am.will)*
*Tags: Codex / Multi-Agent / Swarm / Context Engineering / Parallel Orchestration / OpenAI / Subagent*
