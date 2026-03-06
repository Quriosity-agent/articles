# OpenAI Symphony Elixir Source Code Deep Dive: What 9,000 Lines of Code Actually Do

> **TL;DR**: Symphony is OpenAI's open-source agent orchestration service, implemented in Elixir. We tore apart its source code and found that nearly half of the 9,000 lines handle UI and configuration. The real scheduling core is ~2,100 lines. More interestingly, the most valuable parts aren't code at all — they're markdown skill files that define how agents should commit, create PRs, and merge code.

---

## What is Symphony

Symphony is a **long-running automation service** that:
1. Continuously polls a Linear issue board
2. Creates an isolated workspace per issue
3. Launches a Codex agent in each workspace
4. Lets agents autonomously complete development tasks

```
Linear Board (Todo)
    ↓ poll
Symphony Orchestrator
    ↓ dispatch
┌─────────────────┐
│ Workspace QUR-11 │ → Codex Agent → commit → PR
│ Workspace QUR-12 │ → Codex Agent → commit → PR
│ Workspace QUR-13 │ → Codex Agent → commit → PR
└─────────────────┘
    ↓
Human Review → Merge → Done
```

---

## Code Volume Analysis

Total: ~**9,000 lines of Elixir** (lib/), broken down by module:

| File | Lines | Share | Purpose |
|------|-------|-------|---------|
| `status_dashboard.ex` | 1,949 | 22% | Terminal UI rendering |
| `orchestrator.ex` | 1,457 | 16% | **Core scheduler** |
| `codex/app_server.ex` | 985 | 11% | Codex JSON-RPC communication |
| `config.ex` | 938 | 11% | Configuration parsing |
| `linear/client.ex` | 530 | 6% | Linear GraphQL API |
| `dashboard_live.ex` | 330 | 4% | Web dashboard |
| `workspace.ex` | 282 | 3% | Workspace file management |
| Other | ~2,430 | 27% | Misc modules |

### Key Finding

**UI + Config = 35%**: The dashboard (terminal + web) plus config parsing accounts for one-third of the codebase.

**Core scheduling + execution + API = ~2,100 lines**: The orchestrator + agent_runner + linear client — this is what actually does the work.

---

## Six-Layer Architecture

```
┌─ Policy Layer ──────────────┐
│  WORKFLOW.md (in your repo)  │  ← Defines agent behavior
│  YAML config + Prompt tmpl   │
├─ Configuration Layer ───────┤
│  config.ex (938 lines)       │  ← Parse config, env vars
├─ Coordination Layer ────────┤
│  orchestrator.ex (1,457)     │  ← Polling, dispatch, retry, concurrency
├─ Execution Layer ───────────┤
│  agent_runner.ex (154)       │  ← Launch agent, manage workspace
│  workspace.ex (282)          │
├─ Integration Layer ─────────┤
│  linear/client.ex (530)      │  ← Linear GraphQL API
│  codex/app_server.ex (985)   │  ← Codex communication protocol
├─ Observability Layer ───────┤
│  status_dashboard.ex (1,949) │  ← Terminal + Web UI
│  dashboard_live.ex (330)     │
└─────────────────────────────┘
```

---

## Core Scheduling Logic (Pseudocode)

```python
# orchestrator.ex core loop
every poll_interval_ms:
    issues = linear.fetch(states=["Todo", "In Progress"])
    
    for issue in issues:
        if issue.id in running:      continue  # already running
        if len(running) >= max:      continue  # concurrency full
        if issue.is_blocked:         continue  # blocked by deps
        
        workspace = create_workspace(issue.identifier)
        run_hook("after_create")  # git clone etc.
        
        prompt = render_template(WORKFLOW.md, issue)
        spawn_agent(workspace, prompt)
    
    # State reconciliation
    for issue_id in running:
        current_state = linear.fetch_state(issue_id)
        if current_state in terminal_states:
            stop_agent(issue_id)
            cleanup_workspace(issue_id)
    
    # Retry queue
    for entry in retry_queue:
        if now >= entry.due_at:
            re_dispatch(entry.issue_id)
```

---

## Why Elixir

From the README FAQ:

> Elixir is built on Erlang/BEAM/OTP, which is great for supervising long-running processes. It also supports hot code reloading without stopping actively running subagents.

Core reasons:
1. **Supervisor pattern** — crashed agents auto-restart
2. **Process isolation** — each agent is an independent BEAM process
3. **Hot reloading** — update code without stopping running agents
4. **Message passing** — inter-process communication is a first-class citizen

For most teams though, Node.js `child_process` + pm2 is sufficient.

---

## Codex Communication Protocol

Symphony communicates with Codex via JSON-RPC over stdio:

```
Symphony ──stdio──→ Codex app-server
         ←stdio──
```

Flow:
1. `initialize` → establish connection
2. `thread.start` → create session thread
3. `turn.start(prompt)` → send task
4. Read event stream (tool calls, token usage, completion signals)
5. `turn.completed` → turn finished

Each issue runs up to `max_turns` (default 20). If a turn completes but the issue is still active, it automatically starts the next turn.

---

## .codex/skills — The Real Gold

The most valuable part of the entire repo isn't the Elixir code — it's **6 markdown skill files**:

| Skill | Purpose | Lines |
|-------|---------|-------|
| `commit` | How to write proper commit messages | ~50 |
| `pull` | How to safely merge main and resolve conflicts | ~120 |
| `push` | How to push code and create/update PRs | ~80 |
| `land` | How to monitor CI, handle reviews, squash merge | ~200 |
| `linear` | How to operate Linear API | ~150 |
| `debug` | How to debug Symphony logs | ~80 |

These skills are **language-agnostic pure markdown instructions** — whether you use Codex or Claude Code, just show them to the agent and they work.

---

## WORKFLOW.md — The Agent's Operations Manual

This is Symphony's most important design artifact: a **19KB markdown file** defining the complete agent workflow.

### State Machine

```
Todo → In Progress → Human Review → Merging → Done
                         ↓
                      Rework → Start Over
```

### Workpad Pattern

Each issue maintains a persistent comment as a "work journal":

```markdown
## Codex Workpad

### Plan
- [ ] 1. Parent task
  - [ ] 1.1 Child task

### Acceptance Criteria
- [ ] Criterion 1

### Validation
- [ ] Test: `make test`

### Notes
- Progress entries

### Confusions
- Unclear points (only when applicable)
```

### Key Rules
- **Reproduce before fixing** — confirm the issue exists before changing code
- **Rework = start over** — close old PR, new branch, fresh start
- **Out of scope = new issue** — don't expand current PR scope
- **All review comments must be addressed** — either change code or provide justification

---

## Practical Value for Other Projects

### Directly Reusable (Cross-Language)
- ✅ Skill files (commit/pull/push/land) — pure markdown, any agent can use them
- ✅ WORKFLOW.md state machine design — adapt to your issue tracker
- ✅ Workpad pattern — tracking progress via issue comments
- ✅ PR template — Context/TL;DR/Summary/Alternatives/Test Plan

### Needs Adaptation
- ⚠️ Scheduling logic — concepts transferable, code needs rewriting
- ⚠️ Linear integration — swap for GitHub Issues or other trackers

### Not Needed
- ❌ Codex app-server protocol — Codex-specific
- ❌ Elixir OTP abstractions — unless your project uses Elixir
- ❌ Token accounting logic — Codex protocol details

---

## Comparison with DIY Approach

| Dimension | Symphony (Elixir) | DIY (Node/TS + Existing Tools) |
|-----------|-------------------|-------------------------------|
| Code volume | ~9,000 lines | ~500-800 lines |
| Language | Elixir | TypeScript |
| Agent | Codex (proprietary protocol) | Claude Code / any CLI |
| Tracker | Linear (GraphQL) | GitHub Issues (`gh` CLI) |
| Scheduling | Custom orchestrator | cron + child_process |
| UI | Custom terminal + Phoenix | Existing dashboard |
| Deployment | Requires Erlang/OTP | Node.js |
| Maturity | "engineering preview" | Depends on implementation |

Core difference: Symphony builds from the ground up; DIY assembles existing tools. **Same result, different path.**

---

## 🦞 Lobster Verdict

Symphony's codebase spans 9,000 lines, but everything it teaches us fits in 7 markdown files.

**The real value isn't in the Elixir code — it's in the markdown files that define "how agents should work properly."**

This validates an emerging trend: in the AI agent era, **specifications (prompts/skills/workflows) matter more than implementation (code)**. Because agents can write the implementation themselves, but humans must define the specifications.

OpenAI built a framework in 13,000 lines of Elixir. We picked 7 markdown files and got the same core capabilities.

That's efficiency.

---

## Sources
- GitHub: <https://github.com/openai/symphony>
- SPEC: <https://github.com/openai/symphony/blob/main/SPEC.md>
- Harness Engineering: <https://openai.com/index/harness-engineering/>

---

*Author: 🦞 Lobster Detective*  
*Date: 2026-03-07*  
*Tags: OpenAI / Symphony / Elixir / Agent Orchestration / Codex / Source Code Analysis*
