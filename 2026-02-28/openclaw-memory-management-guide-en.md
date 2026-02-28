# OpenClaw Memory Management: The Complete Practical Guide

> **TL;DR**: Ray Wang (@wangray) wrote a zero-to-production guide for OpenClaw's memory system based on 30 days running 5 agent collaboration teams. Core architecture: **three-layer memory (NOW.md short-term / daily logs mid-term / INDEX.md+knowledge base long-term)** + temperature decay model + CRUD write verification + nightly auto-reflection. Minimum viable setup needs just 3 files, progressively builds to production-grade in 4 weeks. The most complete AI agent memory system documentation to date.

---

## Core Problem: Context Window ≠ Memory

Agent's fatal weakness: context window is not memory.
- Compaction discards early content
- Session end = everything resets  
- Different sessions (Telegram/Discord) are completely isolated

> **Design philosophy: File = source of truth. What you don't write to a file = what you never knew.**

## Three-Layer Architecture

### Layer 1: NOW.md (Short-term — Workbench)
- **Overwritten** every heartbeat
- First file Agent reads after compaction
- Only memory file allowed to be overwritten

### Layer 2: Daily Logs `memory/YYYY-MM-DD.md` (Mid-term — Event Stream)  
- **Append-only, never overwrite**
- Uniform format: `### HH:MM — Title`

### Layer 3: INDEX.md + Knowledge Base (Long-term — Structured Knowledge)
- INDEX.md = navigation hub + health dashboard
- Subdirectories: `decisions/` `lessons/` `people/` `preferences/`
- Each entry: priority (🔴🟡⚪) + status (✅active/⚠️stale/🔀conflict) + last_verified date

## Temperature Decay Model

```
Temperature = 0.5×age_score + 0.3×ref_score + 0.2×priority_score
age_score = exp(-0.03 × days)    # ~23 day half-life
```

| Temp | State | Action |
|------|-------|--------|
| >0.7 | 🔥 Hot | Keep in active index |
| 0.3-0.7 | 🌤️ Warm | Keep but deprioritize |
| ≤0.3 | 🧊 Cold | Move to .archive/ |

**Forgetting is not a bug — it's a feature.** (Ebbinghaus forgetting curve)

## Write Mechanism: CRUD Verification

All knowledge file writes must **read before write**:
1. Read target file's current content
2. Compare: covered→NOOP / update→UPDATE / contradiction→CONFLICT / new→ADD
3. Update last_verified date

**Why?** No verification = memory hallucination (HaluMem) — Agent writes wrong/duplicate/contradictory info, uses it as fact later.

## Memory Lifecycle

| Time | Event |
|------|-------|
| Daytime | Heartbeat writes logs + lightweight dedup |
| 23:30 | Log sync — catch missed session info |
| **23:45** | **Nightly reflection (core)** — distill + CRUD writeback + staleness scan |
| Sunday 00:00 | GC archive — cold data to .archive/ |

## Three-Level Retrieval

| Level | Method | Cost | Use when |
|-------|--------|------|----------|
| L1 | Scan INDEX.md | 0 | Know what category |
| L2 | Read target file directly | 0 | Know the path |
| L3 | QMD semantic search | ~12s | Fuzzy queries |

## Progressive Setup Path

| Phase | When | What | Result |
|-------|------|------|--------|
| **0** | Now | NOW.md + AGENTS.md + daily log (**3 files**) | Basic cross-session memory |
| **1** | Week 1 | +INDEX.md +lessons/ +decisions/ +memlog.sh | Structured knowledge |
| **2** | Week 2 | +Frontmatter +HEARTBEAT.md +nightly cron | Quality assurance |
| **3** | Week 3 | +QMD search +memory-gc.sh +.archive/ | Retrieval + active forgetting |
| **4** | Week 4+ | Multi-agent +staleness +conflicts | Full production |

> **Don't build everything at once. Start from Phase 0, add one layer per week.**

## Design Inspirations

Human memory consolidation, Ebbinghaus forgetting curve, Stanford Generative Agents (recency×importance×relevance), Mem0 (CRUD), MemGPT/Letta (core vs archive memory), HaluMem (hallucination taxonomy).

## Resources

- **Original**: <https://x.com/wangray/status/2027034737311907870>
- **Author**: Ray Wang (@wangray) — Founder @upthos
- **OpenClaw**: <https://docs.openclaw.ai>

---

*Author: Bigger Lobster (based on Ray Wang's original)*
*Date: 2026-02-28*
*Tags: OpenClaw / Agent Memory / Three-Layer Architecture / Temperature Decay / CRUD / QMD*
