# How QAgent Can Learn from Symphony: 7 Upgrades from “Works” to “Operable”

> **TL;DR**: QAgent is already strong at execution (parallel agents, worktrees, reactions). The next leap is governance: explicit state machines, single source-of-truth workpads, reconciliation loops, retry queues, lifecycle hooks, and workflow-as-code.

## Core Position
Do not replace QAgent with Symphony. Keep QAgent’s execution speed, import Symphony’s operational discipline.

## 7 Practical Upgrades
1. Explicit session state machine
2. One workpad per issue/session
3. Periodic tracker↔session reconciliation loop
4. Retry queue with exponential backoff
5. Standard lifecycle hooks (after_create, before_run, before_remove)
6. Workflow-as-code (`WORKFLOW.md` contract)
7. Unified observability schema (state transitions, tokens, retries, errors)

## 3-Week Roadmap
- **Week 1**: state machine + workpad + structured logs
- **Week 2**: reconciliation + retry queue + hooks
- **Week 3**: workflow contract + dashboard governance views

## Bottom Line
QAgent is a strong execution engine already. To become team infrastructure, it needs governance primitives, not just more model integrations.

---
*Author: Bigger Lobster 🦞*  
*Date: 2026-03-05*
