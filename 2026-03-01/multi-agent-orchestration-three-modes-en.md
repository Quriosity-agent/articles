# Three Modes of Multi-Agent Orchestration: Solo, Master-Worker, Peer-to-Peer — With AST Merge Analysis

> **TL;DR**: AI Agent orchestration has three fundamental modes — **Solo**, **Master-Worker**, and **Peer-to-Peer (P2P)**. 80% of tasks work fine with master-worker, but P2P is irreplaceable for **real-time API negotiation, shared mutable state, and adversarial testing**. This article combines analysis of ECC's master-worker architecture with OpenClaw's lobster P2P experience, and deeply examines whether AST-level merging is a viable solution for multi-agent code conflicts.

---

## The Three Modes

### Mode 1: Solo Agent
All context in one brain. Zero communication overhead. Best for deep-context tasks, bug fixing, exploration. Limited by sequential processing.

### Mode 2: Master-Worker (Claude Teams / ECC)
Main agent delegates to sub-agents with restricted permissions. Sub-agents return results/diffs, main agent synthesizes and writes. Scales to ~10 workers. **No merge conflicts** — only one writer.

**ECC's implementation**: Claude writes all code ("Code Sovereignty"), Codex/Gemini only produce diffs and reviews. Three-phase pipeline: plan → execute → review.

### Mode 3: Peer-to-Peer (Lobster Mode)
Agents communicate directly without a central coordinator. Self-organized task division, file locking, alternating commits. Scales to ~3-4 peers. Best for real-time coordination and creative work.

---

## Full Comparison

| Dimension | Solo | Master-Worker | P2P |
|-----------|------|--------------|-----|
| **Context Sharing** | 100% | Fragmented | On-demand |
| **Parallelism** | 0 | High (independent tasks) | High (with overhead) |
| **Communication** | 0 | O(n) | O(n²) |
| **Merge Conflicts** | None | None (single writer) | File locking needed |
| **Fault Tolerance** | Single point | Workers restartable | Strongest |
| **Scale Limit** | 1 | ~10 workers | ~3-4 peers |
| **Creativity** | Single perspective | Multi-view filtered | Highest |
| **Best For** | Deep + dependent | Wide + decomposable | Creative + dynamic |

---

## When Do Agents Need Direct Communication?

> **Will one agent's output change another agent's input assumptions during execution?**

- **No** → Master-worker is enough
- **Yes, predictably** → Master-worker + detailed task specs
- **Yes, unpredictably** → **Need direct P2P communication**

Four scenarios requiring P2P: real-time API negotiation, shared mutable state, adversarial testing, creative collaboration. But honestly, **90% of programming tasks don't need it.**

---

## The Merge Conflict Problem

### Git Worktree Issues
Each agent gets a worktree — parallel + isolated. But merge has three pitfalls:
1. **Semantic conflicts** — git says OK, but logic breaks (changed function signature vs. old call site)
2. **Merge overhead** — understanding both sides may cost more context than just writing it
3. **O(n²) complexity** — scales poorly with agent count

### AST-Level Merging: Sounds Great, Not Practical

**What AST merge could solve (~50-60% of conflicts):**
- Same file, different regions → auto-merge (Git can't)
- Same function, different statements → auto-merge

**What it can't solve (~40%):**
- Cross-file semantic conflicts (changed signature in file A, old call in file B)
- True logic contradictions

**The fundamental problem**: Even after AST auto-merge, you still need LLM review to catch semantic conflicts in the "successfully merged" portion. So you can't skip the LLM pass.

**Is AST merge worth building?** For most teams: **no.** Building AST parsers for every language costs 100x more than just letting LLM review the full git diff. Only worthwhile at extreme scale (100+ agents, commits per minute).

**Current state of AST merge tools:**
| Tool | What it does | Production-ready? |
|------|-------------|-------------------|
| Semantic Merge | AST merge for C#/Java | ❌ Discontinued |
| Difftastic (25K⭐) | AST diff display | ⚠️ Diff only, no merge |
| GumTree | Academic AST diff | ❌ Research only |

---

## Practical Merge Solutions (What Actually Works)

| Approach | How | Best For |
|----------|-----|---------|
| **File locking** | Lock files per agent, work on main | 2-3 agents, rapid prototyping |
| **Single writer** | Only main agent writes | Production code, quality-first |
| **Branch + LLM merge** | Agent branches, LLM reviews | Medium complexity |
| **Microservice split** | Each agent owns a service | Large projects |

---

## Conclusion

| Scenario % | Mode | Reason |
|-----------|------|--------|
| ~30% | Solo | Deep tasks, small fixes |
| ~60% | Master-Worker | Most decomposable dev tasks |
| ~10% | P2P | Real-time coordination, creativity |

**Don't chase the most complex orchestration — chase the best-fitting one.**

For merge conflicts? **File locking or single-writer. Don't bother with AST.**

---

*Authors: 🦞 Bigger Lobster × Peter*
*Date: 2026-03-01*
*Source: Live technical discussion in Discord #articles*
*Tags: AI Agent / Multi-Agent / Orchestration / P2P / AST Merge / OpenClaw / ECC / Claude Code*
