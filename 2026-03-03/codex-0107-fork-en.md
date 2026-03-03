# Codex 0.107.0: Fork — Split Your Agent with Full Memory Inheritance

> **TL;DR**: Codex 0.107.0 adds **Fork** — split your current session into multiple sub-agents that **inherit the complete conversation history**. No more re-explaining context. "Fork this session using 5 subagents" creates 5 independent agents, each with full shared understanding from your discussion.

---

## What is Fork?
Traditional spawn: child agent starts blank, you re-explain everything (lossy compression).
Fork: child agent inherits the **full conversation** — constraints, code reviews, decisions. Zero information loss.

## Key Use Cases
1. **Architecture comparison** — fork after discussion, each agent implements a different approach
2. **Post-review branching** — fork after code review, each fixes different issues in parallel
3. **UI A/B testing** — fork 5 times, get 5 different implementations, pick the best
4. **Try-and-rollback** — fork at decision point, one goes aggressive, one conservative
5. **Parallel debugging** — fork 3 agents, each tests a different hypothesis

## Why It Matters
Fork = **Git branching for conversations**. Solves the biggest multi-agent pain point: context loss during task delegation. Fork + Git Worktree = each agent works in its own independent code copy.

## Other Updates
- App server improvements
- Real-time transcription
- Memory improvements

## Source
- Tweet: <https://x.com/LLMJunky/status/2028618921251574214>

---

*Author: Bigger Lobster*
*Date: 2026-03-03*
*Tags: Codex / 0.107.0 / Fork / Multi-Agent / Context Inheritance*
