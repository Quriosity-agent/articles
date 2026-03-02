# OpenAI's Experiment: 1M Lines of Code, 0 Written by Hand — Full Codex Agent-First Engineering Breakdown

> **TL;DR**: OpenAI ran a 5-month experiment — a real product with **100% Codex-generated code, zero manually-written lines**. Result: ~1M lines, 1,500+ PRs, 3.5 PRs/engineer/day. Key lessons: **give agents a map, not a manual. "Boring" tech wins. Architecture constraints are prerequisites, not luxuries. Error messages should contain remediation instructions.**

---

## The Experiment

- **Zero hand-written code** — everything by Codex: app logic, tests, CI, docs, tools, dashboards
- **Real product** with daily internal users and external alpha testers
- **3→7 engineers** over 5 months (Aug 2025 – Jan 2026)
- **~1M lines of code**, 1,500+ PRs, 3.5 PRs/engineer/day
- **10x faster** than estimated manual development
- Single Codex runs lasting **6+ hours**

## How Codex Validates Its Own Work

![Codex driving app with Chrome DevTools](harness-codex-devtools.webp)

*Codex uses Chrome DevTools Protocol to drive the app, take screenshots, inspect DOM, reproduce bugs, record videos, and validate fixes.*

Each Codex task gets its own **git worktree** with an isolated app instance and observability stack.

## Observability: Agents Can Debug

![Observability stack](harness-observability.svg)

*Per-worktree observability: logs (LogQL), metrics (PromQL), traces. Torn down after task completion.*

Prompts like "ensure startup < 800ms" and "no span exceeds 2 seconds" become tractable.

## AGENTS.md: Map, Not Manual

![Agent knowledge boundaries](harness-knowledge.webp)

*From the agent's POV: only versioned, in-repo artifacts exist. Slack, Google Docs, tribal knowledge = invisible.*

AGENTS.md stays ~100 lines — a table of contents pointing to structured docs/. Enforced by linters and CI. A "doc-gardening" agent scans for stale docs and opens fix-up PRs.

## Strict Architecture as Prerequisite

![Layered domain architecture](harness-architecture.webp)

*Types → Config → Repo → Service → Runtime → UI. Cross-cutting via Providers only. Mechanically enforced.*

Custom linters with **remediation instructions in error messages** — agents read the error and know how to fix it.

## Full Agent Lifecycle (End-to-End)

Single prompt → validate state → reproduce bug → record video → implement fix → validate → record resolution video → open PR → respond to reviews → fix build failures → escalate only when needed → merge.

## AI Slop: Golden Principles + Garbage Collection

Agents replicate existing patterns — including bad ones. Solution: encode taste as Golden Principles, run background cleanup agents on schedule. Technical debt = high-interest loan: pay continuously.

## Key Insights

| Insight | Explanation |
|---------|------------|
| **Map not manual** | AGENTS.md ~100 lines → structured docs/ |
| **"Boring" tech wins** | Composable, stable APIs, rich training data |
| **Reimplement > depend** | 100% test coverage + perfect integration |
| **Architecture is day-1** | Usually "100-engineer" territory → agent prerequisite |
| **All knowledge in-repo** | Slack = invisible to agents |
| **Error msgs = fix instructions** | Agent reads error, knows remediation |
| **Waiting > correcting** | Minimal blocking merge gates at high throughput |
| **Agent reviews agent** | Humans step up to higher abstraction |

## Resources

- **Original**: <https://openai.com/index/harness-engineering/>
- **Codex**: <https://openai.com/codex/>
- **Execution Plans**: <https://cookbook.openai.com/articles/codex_exec_plans>

---

*Author: Bigger Lobster*
*Date: 2026-03-01*
*Tags: OpenAI / Codex / Agent-First / AGENTS.md / Architecture / Observability*
