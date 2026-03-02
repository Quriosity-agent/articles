# OpenAI's Experiment: 1 Million Lines of Code, 0 Written by Hand — Codex Agent-First Engineering

> **TL;DR**: OpenAI ran a 5-month experiment — a real product with **100% Codex-generated code, zero manually-written lines**. Result: ~1M lines of code, 1,500+ PRs, 3.5 PRs per engineer per day. This post details the "humans steer, agents execute" paradigm. Key lesson: **give agents a map, not a 1,000-page manual.** Discipline lives in the scaffolding, not the code.

---

## The Experiment

- **Zero hand-written code** — everything by Codex: app logic, tests, CI, docs, tools
- **Real product** with internal daily users and external alpha testers
- **3→7 engineers** over 5 months
- **~1M lines of code**, 1,500+ PRs, 3.5 PRs/engineer/day
- **10x faster** than estimated manual development
- Single Codex runs lasting **6+ hours** (while humans sleep)

## Core Philosophy: Humans Steer, Agents Execute

Engineering work shifts from writing code to **designing environments, expressing intent, and building feedback loops**.

## AGENTS.md: Map, Not Manual

The biggest lesson: **don't write a 1,000-page instruction file.**

AGENTS.md stays ~100 lines — a table of contents pointing to structured docs/:
- designs/ (with verification status)
- architecture/ (domain + package layering)
- quality/ (per-domain grades)
- plans/ (active, completed, debt)

**Progressive disclosure**: agents start small, learn where to look next.

## Strict Architecture as Prerequisite

Fixed layers per domain: Types → Config → Repo → Service → Runtime → UI. Cross-cutting via Providers only. Enforced by custom linters with remediation instructions in error messages.

This architecture is usually "hundreds of engineers" territory — for agents, it's an **early prerequisite**.

## Full Agent Lifecycle

Single prompt → Codex can: validate state, reproduce bug, record video, implement fix, validate fix, record resolution video, open PR, respond to reviews, fix build failures, escalate only when needed, merge.

## AI Slop Management

Agents replicate existing patterns — including bad ones. Solution: **Golden Principles** encoded in repo + automated cleanup agents scanning for deviations and opening refactoring PRs on schedule.

## Key Insights

- "Boring" tech works better for agents (composable, stable APIs)
- Sometimes reimplementing > depending on opaque libraries
- Minimal blocking merge gates (corrections cheap, waiting expensive)
- Agent-to-agent review replaces most human review
- All knowledge must live in-repo (Slack/Docs = invisible to agents)
- Give agents observability (LogQL, PromQL, screenshots, DOM)

## Resources

- **Original**: <https://openai.com/index/harness-engineering/>
- **Codex**: <https://openai.com/codex/>

---

*Author: Bigger Lobster*
*Date: 2026-03-01*
*Tags: OpenAI / Codex / Agent-First / Zero Hand-Written Code / AGENTS.md / Engineering*
