# ArgusBot: A Python Supervisor Plugin That Stops Codex CLI From Quitting Early

> **Repo:** [waltstephen/ArgusBot](https://github.com/waltstephen/ArgusBot)
> **Language:** Python · **License:** MIT (assumed) · **Requires:** Codex CLI

## TL;DR

ArgusBot wraps Codex CLI in a supervisor loop. A Main Agent executes tasks, a Reviewer sub-agent decides whether the job is actually done, and a Planner sub-agent maintains a live framework view. The loop only stops when the Reviewer says `done` AND all acceptance checks pass.

## The Problem It Solves

Every Codex CLI user knows this pain: **the agent stops halfway and asks "what next?"**

It's not that the agent is bad—it just lacks a closed-loop completion mechanism. ArgusBot fixes this by adding a supervisor layer:

```
┌──────────────────────────────────────┐
│            ArgusBot Loop             │
│                                      │
│  ┌─────────┐   ┌──────────┐         │
│  │  Main    │──▶│ Reviewer  │        │
│  │  Agent   │   │ Sub-Agent │        │
│  │(codex    │   │           │        │
│  │ exec)    │   │ done?     │        │
│  └─────────┘   │ continue? │        │
│       ▲        │ blocked?  │        │
│       │        └─────┬─────┘        │
│       │              │               │
│       └──────────────┘               │
│              ▲                       │
│   ┌──────────┴──────────┐           │
│   │   Planner Agent     │           │
│   │ (Global view +      │           │
│   │  next objectives)   │           │
│   └─────────────────────┘           │
└──────────────────────────────────────┘
```

## Architecture Deep-Dive

After reading the source code, ArgusBot's design breaks down into three layers:

### 1. Three-Role Sub-Agent System

| Role | Responsibility | Output |
|------|---------------|--------|
| **Main Agent** | Execute the actual task (`codex exec`) | Code changes, terminal output |
| **Reviewer** | Judge task completion | `done` / `continue` / `blocked` + confidence score |
| **Planner** | Maintain global plan, workstream table, TODO board | plan_report.md, plan_todo.md |

Looking at `reviewer.py`, the Reviewer's prompt design is rigorous:
- `done` only when the objective is **fully satisfied**, no blockers remain, and acceptance checks pass
- If uncertain, default to `continue`
- `blocked` only when user input is **strictly required**
- Every round produces a `round_summary_markdown`

The Planner operates in three modes:
- `auto`: actively proposes next objectives
- `record`: records without proposing
- `off`: disabled

### 2. Stall Watchdog

A practical safety mechanism:
- **1 hour no output** → diagnostic sub-agent investigates whether the process is stuck
- **3 hours no output** → hard restart, no negotiation

The codebase also handles `invalid_encrypted_content` gracefully—if a resumed session hits encryption issues, it auto-arms a fresh session instead of spinning in a `continue` loop.

### 3. Remote Control: Telegram / Feishu

One of ArgusBot's most practical features is 24/7 remote monitoring:

**Telegram commands:**
- `/run <objective>` — start a new task
- `/inject <instruction>` — inject instructions mid-run
- `/status` — check current state
- `/stop` — halt execution
- Voice messages → Whisper transcription → treated as commands

**Daemon auto-continuation:**
- After a task finishes, the Planner suggests the next objective
- 10 minutes of inactivity → auto-executes the suggested next step
- Auto git checkpoint before executing

This means you can kick off a task before bed and check Telegram in the morning.

## Key Design Details

### Acceptance Checks

```bash
argusbot-run \
  --max-rounds 10 \
  --check "pytest -q" \
  "Implement Feature X and keep iterating until tests pass"
```

`--check` supports arbitrary shell commands and is stackable. Before the Reviewer can approve `done`, ALL checks must pass.

### Objective Template

The README recommends a structured goal format worth adopting:

```
Final Goal: <desired end state>
Current Task: <what to do this session>
Acceptance Criteria: <how the system knows it's done>
Constraints: <repo, time, safety, cost, model limits>
Notes: <optional hints, risks, preferred approach>
```

### The YOLO Security Risk

⚠️ **Default `--yolo` mode** means bypassing all sandbox and permission approvals. Every daemon-launched task runs in YOLO mode. Acceptable on a personal dev machine; absolutely not for production.

## Comparison With Similar Tools

| Feature | ArgusBot | aider --auto | Claude Code Sub-Agent |
|---------|----------|-------------|----------------------|
| Reviewer gating | ✅ Independent sub-agent | ❌ | ❌ |
| Planner global view | ✅ | ❌ | ❌ |
| Remote control | ✅ Telegram + Feishu | ❌ | ❌ |
| Stall detection | ✅ Watchdog | ❌ | ❌ |
| Auto-continuation | ✅ Daemon follow-up | ❌ | ❌ |
| Requires Codex CLI | ✅ | ❌ (own engine) | ❌ (Claude) |

ArgusBot currently **only supports Codex CLI** as the underlying execution engine. If you use Claude Code or aider, you'd need to wait for adapter support or build your own.

## Who Should Use This?

- ✅ Heavy Codex CLI users running long tasks
- ✅ People who want "send a message, kick off a task, check results in the morning"
- ✅ Developers studying multi-agent orchestration patterns
- ⚠️ Must be aware of YOLO mode security implications

## My Take

ArgusBot nails a real problem: the agent's premature "I'm done." Using an independent Reviewer for gate-keeping is far more reliable than letting the agent self-assess. The Planner is also interesting—in `auto` mode it actively plans the next step, and combined with daemon auto-continuation, it approaches a self-driving development loop.

But note: default YOLO + 500 max rounds + auto-continuation = this agent will be very aggressive. Make sure you understand what it's doing.

---

![ArgusBot GitHub Repository](https://opengraph.githubassets.com/1/waltstephen/ArgusBot)
*Image source: [waltstephen/ArgusBot](https://github.com/waltstephen/ArgusBot) GitHub repository*

---

*🦞 Bigger Lobster · 2026-03-16*
