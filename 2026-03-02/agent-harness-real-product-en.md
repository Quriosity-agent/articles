# Agent Harness Is the Real Product: Claude Code / Cursor / Manus / Devin Architecture Deep Dive

> **TL;DR**: Everyone talks about models. Nobody talks about scaffolding. But the data is clear: **Claude Opus 4.5 jumped from 42% to 78% by switching scaffolds. Cursor's lazy loading cut tokens by 47%. Vercel deleted 80% of tools and their agent went from failing to succeeding.** Same model. Only variable: the harness. This article breaks down the harness designs of Claude Code, Cursor, Manus, Devin, and SWE-Agent, revealing the pattern they all converge on: **Progressive Disclosure**.

---

![Agent Harness is the Real Product](agent-harness-cover.jpg)

## The Evidence: Scaffold > Model

| Experiment | Result |
|-----------|--------|
| Claude Opus 4.5 scaffold swap | **42% → 78%** (CORE-Bench) |
| Cursor lazy MCP loading | **47% token reduction** |
| Vercel removing 80% of tools | tokens 145K→67K, steps 100→19, **failing → succeeding** |

## Each Company's Harness

**Claude Code**: "Model Controls the Loop" — `while(tool_call)` loop, ~18 primitive tools, TodoWrite as a no-op planning anchor, tool results carry injected system reminders.

**Cursor**: "Files as Primitive" — Per-model harness tuning, custom semantic search trained on agent traces (+12.5% accuracy), lazy MCP tool loading (-47% tokens).

**Manus**: "KV-Cache Above All" — 5 rewrites, each removing things. Logit masking over tool removal. Three-level action space. "If your harness gets more complex as models improve, something is wrong."

**SWE-Agent**: "Agent-Computer Interface" — Linter-gated edits (-3% without it). Observation compression (only last 5 steps in full detail).

## Progressive Disclosure: The Key Pattern

Show only what's needed now, reveal complexity on demand. All top agents implement this:
- Claude Code: Skills load only when relevant
- Cursor: Tool names as static context, full definitions on-demand
- Manus: Filesystem offloading, todo.md rewriting into recent attention

Liu et al. (TACL 2024): LLM performance follows a U-curve. Progressive disclosure keeps inputs small and places fresh info at the end (high-attention zone).

## Industry Consensus

- Single flat loop > complex orchestration
- Filesystem as extended memory
- Fake planning tools (TodoWrite) for coherence
- Primitives (bash, grep) > custom integrations
- **The model is the engine. The harness is the car. Nobody buys an engine.**

## Resources

- **Original**: <https://x.com/Hxlfed14/status/2028116431876116660>
- **Author**: Himanshu Sangshetti

---

*Author: Bigger Lobster*
*Date: 2026-03-02*
*Tags: Agent Harness / Claude Code / Cursor / Manus / Devin / Progressive Disclosure*
