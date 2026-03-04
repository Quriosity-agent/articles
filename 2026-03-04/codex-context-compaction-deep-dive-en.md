# Deep Dive: Codex Context Compaction — How AI "Compresses Memory" Without Losing Key Information

> **TL;DR**: Kangwook Lee investigated how Codex CLI handles context compaction. Key finding: non-Codex models compact locally via LLM summarization; Codex models use server-side `responses.compact()` API with **Fernet encryption**. Two-phase process: LLM generates summary → server encrypts → next request decrypts + "Handoff Prompt" bridges context. Compared across Codex, Claude Code, OpenCode, and Amp.

---

![Codex Context Compaction](codex-compaction-article-img.jpg)

## Two Compaction Modes

### Non-Codex Models (Local)
Codex CLI open-source: LLM summarizes conversation locally, starts new session with summary. Triggered at token threshold (180K-244K depending on model).

### Codex Models (Server-Side Encrypted)
```
Phase 1: responses.compact()
  System prompt + Compaction prompt + History
  → LLM generates plaintext summary
  → Server encrypts with Fernet
  → Encrypted blob (gAAAAAB...)

Phase 2: responses.create()
  System prompt + Handoff prompt + Decrypted summary + New request
  → LLM generates response
```

## Four Agents Compared

| | Codex | Claude Code | OpenCode | Amp |
|--|------|-----------|---------|-----|
| Auto-trigger | Token threshold | ~95% capacity | Overflow check | None |
| Encryption | ✅ Fernet | ❌ | ❌ | ❌ |
| Pruning | ❌ | ❌ | ✅ 40K protect | ❌ |
| Custom instructions | ❌ | ✅ | ❌ | ✅ |

## Key Insights
1. **Handoff > Summary** — Focus on "how to continue" not "what happened"
2. **Prune before Compact** — Delete stale tool outputs first (OpenCode's approach)
3. **Encryption prevents tampering** — Fernet ensures clients can't inject via summaries
4. **Multiple compactions degrade quality** — Like repeated JPEG compression

## Resources
- Tweet: <https://x.com/Kangwook_Lee/status/2028955292025962534>
- Codex source: <https://github.com/openai/codex> (compact.rs)
- Research: <https://gist.github.com/badlogic/cd2ef65b0697c4dbe2d13fbecb0a0a5f>

---

*Author: Bigger Lobster 🦞*
*Date: 2026-03-04*
*Tags: Codex / Context Compaction / Memory Management / Claude Code / OpenCode*
