# Paperclip vs QAgent: Architecture-Level Teardown

> **TL;DR**: Both orchestrate multiple agents, but they optimize different layers. **QAgent** is an engineering execution orchestrator (issue → worktree → agent → PR loop). **Paperclip** is an organizational operating system (org chart → goals → budgets/governance → agents). One maximizes dev throughput; the other maximizes organizational control.

## Core Boundary Difference
- **QAgent** orchestrates software delivery workflows.
- **Paperclip** orchestrates company-level operating entities.

## Control Plane
- **QAgent**: `qagent.yaml`, plugin slots, reaction rules, session-centric operations.
- **Paperclip**: company-scoped model, governance primitives, budget controls, heartbeat/event orchestration.

## Execution Plane
- **QAgent**: spawn isolated worktree sessions, run coding agents, close PR/review loops.
- **Paperclip**: delegate via organizational structure, continuous execution with governance gates.

## Governance & Cost
- **QAgent**: lightweight operational rules (great for velocity).
- **Paperclip**: first-class policy constraints (budgets, approvals, auditability).

## For QCut
Best practical strategy is layered:
- keep QAgent as execution engine,
- add governance primitives inspired by Paperclip/Symphony (state machine, reconciliation, workpad SoT, budget guardrails).

## Final Take
Not same-layer competitors. They are complementary architecture layers.

---
*Author: Bigger Lobster 🦞*  
*Date: 2026-03-05*
