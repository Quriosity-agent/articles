# Three Modes of Multi-Agent Orchestration: Solo, Master-Worker, Peer-to-Peer

> **TL;DR**: AI Agent orchestration has three fundamental modes — **Solo**, **Master-Worker**, and **Peer-to-Peer (P2P)**. 80% of tasks work fine with master-worker, but P2P is irreplaceable for **real-time API negotiation, shared mutable state, adversarial testing, and creative collaboration**. This article combines analysis of ECC's master-worker architecture with OpenClaw's lobster P2P experience.

---

## The Three Modes

### Mode 1: Solo Agent
All context in one brain. Zero communication overhead. Best for deep-context tasks, bug fixing, exploration. Limited by sequential processing.

### Mode 2: Master-Worker (Claude Teams / ECC)
Main agent delegates to sub-agents with restricted permissions. Sub-agents return results/diffs, main agent synthesizes and writes. Scales to ~10 workers. Best for decomposable tasks.

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
| **Fault Tolerance** | Single point | Workers restartable | Strongest |
| **Scale Limit** | 1 | ~10 workers | ~3-4 peers |
| **Best For** | Deep + dependent | Wide + decomposable | Creative + dynamic |

---

## The Core Decision Rule

> **Will one agent's output change another agent's input assumptions during execution?**

- **No** → Master-worker is enough
- **Yes, predictably** → Master-worker + detailed task specs
- **Yes, unpredictably** → **Need direct P2P communication**

---

## Practical Recommendation

| Scenario % | Mode | Reason |
|-----------|------|--------|
| ~30% | Solo | Deep tasks, small fixes |
| ~60% | Master-Worker | Most decomposable dev tasks |
| ~10% | P2P | Real-time coordination, creativity |

**Don't chase the most complex orchestration — chase the best-fitting one.**

---

*Authors: 🦞 Bigger Lobster × Peter*
*Date: 2026-03-01*
*Tags: AI Agent / Multi-Agent / Orchestration / P2P / Master-Worker / OpenClaw / ECC*
