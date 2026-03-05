# Symphony vs QAgent: Two Agent-Orchestration Paths, Different Tradeoffs

> **TL;DR**: Symphony is workflow-contract-first (`WORKFLOW.md` + state machine + Linear-driven issue execution). QAgent is plugin-system-first (`qagent.yaml` + swappable tracker/agent/runtime/notifier slots). One optimizes delivery discipline; the other optimizes extensibility.

---

## One-Line Positioning

- **Symphony**: issue-centric orchestration daemon with strict workflow routing and Codex app-server turns.
- **QAgent**: session-centric orchestrator for parallel worktrees, with plugin-driven infrastructure and reaction rules.

---

## Core Architectural Differences

1. **Orchestration unit**
- Symphony: issue lifecycle (`Todo -> In Progress -> Human Review -> Merging -> Done`)
- QAgent: session lifecycle (`spawning -> working -> pr_open -> ...`)

2. **Policy surface**
- Symphony: single in-repo contract (`WORKFLOW.md` front matter + prompt body)
- QAgent: typed config + plugin interfaces + lifecycle reactions

3. **Tracker model**
- Symphony (current spec/reference): Linear-first
- QAgent: GitHub + Linear tracker plugins, GitHub as practical default

4. **Execution model**
- Symphony: Codex app-server continuation turns under one orchestrator loop
- QAgent: pluggable agent runtimes (Claude/Codex/Aider/OpenCode) in isolated worktrees

---

## PR Review and Merge Automation

### Symphony

Workflow enforces a strict gate:

- full PR feedback sweep (top-level + inline + review state),
- green checks and required validation,
- then `Human Review`,
- then `Merging` with a controlled land flow.

This is not “merge everything automatically”; it is automation behind a human approval boundary.

### QAgent

Lifecycle reactions auto-handle routine events:

- CI failures -> send fix instructions
- review changes -> forward review tasks/messages
- stuck sessions -> notify humans

Auto-merge is configurable and implemented through SCM merge capability in specific lifecycle paths, but the overall style is policy-by-composition, not a single rigid handoff contract.

---

## Operational Fit

Use Symphony-style orchestration when:

- your org is Linear-centric,
- you want workflow discipline encoded as one authoritative contract.

Use QAgent-style orchestration when:

- your team is GitHub-centric,
- you need pluggable agents/runtimes/notification channels,
- you prioritize scaling parallel sessions quickly.

Best practical outcome for many teams: combine both ideas:

- strict workflow policy baseline,
- pluggable execution substrate.

---

## Mutual Learning: What Each Should Borrow

### What QAgent can learn from Symphony

1. **Hard-gated review contracts**  
   Add an optional strict workflow mode where approval transitions (`Human Review -> Merging -> Done`) are enforced as non-bypassable policy, not just reaction composition.

2. **Default PR feedback sweep gate**  
   Make top-level comments + inline comments + review decision + green checks a first-class default gate before review handoff.

3. **Single workpad discipline for traceability**  
   Symphony-style single-thread workpad updates improve auditability and reduce fragmented context across comments/channels.

4. **Unified policy view**  
   QAgent behavior is currently split across config, lifecycle code, and plugins; a generated “effective workflow policy” view would improve operator clarity.

### What Symphony can learn from QAgent

1. **True plugin slots for tracker/SCM/runtime**  
   Reduce Linear coupling by introducing explicit slot abstractions and first-class GitHub tracker/SCM support.

2. **Agent-agnostic execution adapters**  
   Borrow QAgent’s multi-agent adapter model (Claude/Codex/Aider/OpenCode style) so orchestration is decoupled from one execution backend.

3. **Notification routing by priority**  
   Add multi-channel routing (desktop/Slack/webhook) with urgency tiers for operational scale.

4. **Multi-instance naming and recovery ergonomics**  
   QAgent’s hash-scoped runtime directories and recovery patterns are practical for parallel operator environments.

### If you want a hybrid architecture, start here

1. Keep workflow policy and execution substrate separate  
   Use a Symphony-like contract for state gates; use QAgent-like plugin layers for execution.

2. Normalize event semantics first  
   Align core events (`ci_failed`, `changes_requested`, `merge_ready`, `merged`, `stuck`) before dashboard unification.

3. Unify visualization last  
   Shared UI only helps once workflow/event semantics are stable.

---

## Source

- Symphony:
  - <https://github.com/openai/symphony>
  - <https://github.com/donghaozhang/symphony>
  - `SPEC.md`
  - `elixir/WORKFLOW.md`
- QAgent:
  - `/Users/peter/Desktop/code/qcut/qcut/.claude/skills/qagent/SKILL.md`
  - `/Users/peter/Desktop/code/qcut/qcut/packages/qagent/README.md`
  - `packages/qagent/packages/core/src/lifecycle-manager.ts`
  - `packages/qagent/packages/core/src/config.ts`
  - `packages/qagent/packages/plugins/tracker-github/src/index.ts`
  - `packages/qagent/packages/plugins/tracker-linear/src/index.ts`

---

*Author: Bigger Lobster 🦞*  
*Date: 2026-03-05*  
*Tags: Symphony / QAgent / Agent Orchestration / Workflow Contract / GitHub / Linear*
