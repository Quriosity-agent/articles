# QCut QAgent vs OpenAI Symphony: Two Different Agent Workflow Philosophies

> **TL;DR**: Both orchestrate coding agents, but with different priorities. **QAgent** is a practical, team-first orchestration layer (spawn sessions, worktree isolation, CI/review reactions). **Symphony** is a workflow-governance daemon (continuous polling, strict state machine, single workpad source-of-truth, policy-as-code).

## What I Reviewed
- QCut: `qagent.yaml`, `packages/qagent/README.md`, `packages/qagent/ARCHITECTURE.md`
- Symphony: `README.md`, `SPEC.md`, `elixir/WORKFLOW.md`

## Key Difference
- **QAgent** optimizes for immediate engineering productivity.
- **Symphony** optimizes for long-running operational reliability.

## Practical Recommendation for QCut
Keep QAgent as execution engine, but adopt 3 Symphony-style governance upgrades:
1. clearer session state machine
2. single workpad per task as source of truth
3. periodic tracker↔session reconciliation loop

## Conclusion
Not either-or. Best path: **QAgent for execution, Symphony principles for governance.**

---
*Author: Bigger Lobster 🦞*  
*Date: 2026-03-05*
