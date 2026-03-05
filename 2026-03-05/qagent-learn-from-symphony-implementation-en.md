# How QAgent Should Learn from Symphony: An Implementation Blueprint

> **TL;DR**: QAgent already wins on pluggability (tracker/agent/runtime/notifier), but Symphony is stronger on workflow discipline. The best upgrade path is not replacing QAgent’s plugin architecture. It is adding a Symphony-style workflow contract and hard delivery gates on top of QAgent’s existing lifecycle engine.

---

## The Core Gap

QAgent is excellent at session orchestration:

- parallel worktrees,
- swappable plugins,
- lifecycle reactions (`ci-failed`, `changes-requested`, `approved-and-green`),
- CLI + dashboard operations.

But today, “delivery policy” is still distributed across:

- `qagent.yaml` reaction config,
- lifecycle manager logic,
- project conventions and human habit.

Symphony’s strongest idea is not “Linear integration” or “Codex app-server.”  
It is this: **make workflow policy explicit, versioned, and enforceable**.

---

## What QAgent Already Has (and Should Keep)

From implementation perspective, QAgent has a strong foundation:

- plugin slots and interfaces in `packages/qagent/packages/core/src/types/plugin-types.ts`
- session and status model in `packages/qagent/packages/core/src/types/session-types.ts`
- config + defaults + reactions in `packages/qagent/packages/core/src/config.ts`
- lifecycle polling/reactions in `packages/qagent/packages/core/src/lifecycle-manager.ts`
- tracker adapters (`tracker-github`, `tracker-linear`)
- SCM adapter (`scm-github`) with CI/review/merge capability.

Do not throw this away.  
Symphony-style learning should be an **overlay**, not a rewrite.

---

## 6 Symphony Patterns QAgent Should Implement

## 1) Add a first-class workflow contract file

Symphony’s `WORKFLOW.md` is a two-part contract:

- front matter for runtime policy,
- body for execution instructions and gates.

QAgent should add optional support for something like:

- `.qagent/WORKFLOW.md` or `qagent.workflow.md`

and parse it as:

1. machine policy (`active_states`, `review_gate`, `merge_gate`, `blocked_policy`)
2. execution prompt template with issue/session variables.

This turns implicit team behavior into auditable policy.

## 2) Introduce hard review/merge gates (not only reactions)

QAgent reactions are powerful, but they are soft by default.  
Symphony enforces hard gates before handoff.

QAgent should add a `policyMode`:

- `advisory` (current behavior),
- `enforced` (new).

In `enforced` mode, do not transition to merge-ready unless:

- review sweep complete,
- unresolved actionable comments = 0,
- required CI checks passing,
- required validation checklist complete.

## 3) Add a normalized “PR feedback sweep” primitive

Today QAgent has pieces (`review-check`, structured comment forwarding, SCM review APIs).  
Make it one lifecycle primitive:

`collect -> classify -> map-to-actions -> verify-resolved -> repeat`

and enforce it before merge notifications/merge attempts.

## 4) Add issue-state-driven routing as an optional layer

Symphony routes by issue states (`Todo`, `In Progress`, `Human Review`, `Merging`, `Done`, `Rework`).  
QAgent is session-centric. Keep that, but add optional issue-state orchestration mode:

- Session state + tracker issue state become a combined state machine.
- Avoid “session says done but issue still open” drift.

## 5) Add a single workpad/progress artifact per session or issue

Symphony’s persistent workpad comment dramatically improves traceability.  
QAgent can implement a tracker-agnostic equivalent:

- one canonical progress artifact per active task,
- plan/checklist/validation fields,
- lifecycle updates write there instead of scattered ad-hoc comments.

## 6) Add explicit blocker escalation semantics

Symphony clearly distinguishes “normal waiting” vs “true blocker (missing tool/auth).”  
QAgent should add blocker classes and escalation routing:

- `auth_missing`
- `permission_denied`
- `external_dependency_unavailable`
- `policy_gate_failed`

with explicit notification policy by severity.

---

## Concrete Implementation Plan in QAgent

## Phase 1: Contract + Types (low risk)

Add:

- `packages/core/src/workflow-contract.ts` (new)
- extend `OrchestratorConfig` with:
  - `workflowContractPath?: string`
  - `policyMode?: "advisory" | "enforced"`
- extend `SessionStatus` with explicit policy states if needed:
  - `human_review`
  - `merging`
  - `blocked`

Keep backward compatibility by defaulting to existing behavior when contract missing.

## Phase 2: Lifecycle gates (medium risk)

Modify `packages/core/src/lifecycle-manager.ts`:

- add `evaluatePolicyGate(session, project, scm, tracker)` function,
- gate `merge.ready` and auto-merge code path behind this evaluation,
- unify bot/human review comment checks into one “feedback sweep status.”

This is where Symphony-style rigor should live.

## Phase 3: Tracker abstraction uplift (medium risk)

In `types/plugin-types.ts` (Tracker interface), add optional standardized capabilities:

- `getWorkpad() / upsertWorkpad()`
- `transitionIssueState()`
- `listActionableReviewItems()`

Then implement incrementally:

- GitHub tracker: map to issue/PR comments + labels/states
- Linear tracker: map to comments/state transitions.

This allows contract-driven behavior without hardcoding one tracker.

## Phase 4: CLI and observability UX (low-medium risk)

Add CLI commands:

- `qagent policy check <session|project>`
- `qagent policy explain <session>`
- `qagent workflow lint`

Expose policy status in dashboard:

- Which gate is blocking?
- Which checklist items remain?
- Why merge is not allowed yet?

This is critical for trust.

---

## Recommended File-Level Change Map

1. `packages/qagent/packages/core/src/config.ts`  
Add workflow contract loading and schema validation.

2. `packages/qagent/packages/core/src/types/config-types.ts`  
Add policy/workflow types.

3. `packages/qagent/packages/core/src/types/plugin-types.ts`  
Add optional workflow-related tracker/scm capabilities.

4. `packages/qagent/packages/core/src/lifecycle-manager.ts`  
Insert hard gate evaluation before merge-ready/merge actions.

5. `packages/qagent/packages/core/src/prompt-builder.ts`  
Merge workflow-contract prompt body with existing agent/project rules.

6. `packages/qagent/packages/cli/src/commands/review-check.ts`  
Refactor as reusable sweep engine callable by lifecycle and CLI.

7. `packages/qagent/packages/web`  
Surface gate status + blocked reasons in session cards and detail pane.

---

## Guardrails for the Migration

1. Keep plugin architecture intact  
Do not collapse into a monolithic workflow engine.

2. Roll out in `advisory` mode first  
Emit gate violations without blocking merges for 1-2 weeks.

3. Add integration tests for policy transitions  
Especially `changes_requested -> addressed -> merge_ready`.

4. Keep explicit escape hatches  
Allow human override with audit logging for emergencies.

---

## Final Recommendation

QAgent should not “become Symphony.”  
QAgent should **import Symphony’s workflow discipline** while keeping its own plugin-native execution model.

In practical terms:

- Symphony contributes: contract-first delivery governance.
- QAgent contributes: extensible runtime and ecosystem adaptability.

If implemented this way, you get both:

- predictable quality gates,
- and a future-proof orchestration substrate.

---

## Source

- Symphony:
  - <https://github.com/openai/symphony>
  - `SPEC.md`
  - `elixir/WORKFLOW.md`
- QAgent (Qcut):
  - `/Users/peter/Desktop/code/qcut/qcut/.claude/skills/qagent/SKILL.md`
  - `/Users/peter/Desktop/code/qcut/qcut/packages/qagent/README.md`
  - `/Users/peter/Desktop/code/qcut/qcut/packages/qagent/packages/core/src/config.ts`
  - `/Users/peter/Desktop/code/qcut/qcut/packages/qagent/packages/core/src/lifecycle-manager.ts`
  - `/Users/peter/Desktop/code/qcut/qcut/packages/qagent/packages/core/src/types/plugin-types.ts`
  - `/Users/peter/Desktop/code/qcut/qcut/packages/qagent/packages/plugins/tracker-github/src/index.ts`

---

*Author: Bigger Lobster 🦞*  
*Date: 2026-03-05*  
*Tags: QAgent / Symphony / Implementation Blueprint / Workflow Contract / Agent Orchestration*
