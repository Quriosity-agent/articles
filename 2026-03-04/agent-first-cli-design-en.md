# Agent-First CLI Design: 50 Years from Unix Pipes to AI Agents

> **TL;DR**: Unix philosophy (1978): "Program output should become another program's input." 50 years later, the best implementation evolved from `grep/awk` to `--json + AI Agent`. This article covers the Agent-First CLI design pattern with Vercel CLI and QCut CLI examples.

---

## Evolution of CLI Output (50 Years)
```
1970s: Plain text → grep/awk/sed (fragile parsing)
1990s: Structured options → --format, -o (less guessing)  
2020s: JSON output → --json (structured, field names = API)
2025s: Agent-First → JSON + Markdown guide + self-discovery
```

## 5 Agent-First CLI Principles
1. **Dual-mode output** — Human-readable default, `--json` for agents
2. **Unified error format** — `{"status":"error","code":"NOT_FOUND"}`
3. **Async long tasks** — Return jobId, poll for status
4. **Self-discoverable params** — `--help --json` returns schema
5. **Human-in-the-loop pauses** — ToS, billing decisions wait for human

## Why JSON Is the New Plain Text
| | 1978 Plain Text | 2026 JSON |
|--|----------------|-----------|
| Universal | All programs read it | All languages parse it |
| Pipeline | grep/awk/sed | jq / AI Agent |
| Schema | None (convention) | Field names = schema |
| Consumers | Humans + scripts | Humans + scripts + **AI Agents** |

## Key Insight
Unix philosophy was never "output must be plain text." It was "make your output consumable by the next program." In 1978 that meant grep. In 2026 it means AI Agents. The means changed; the principle didn't.

## Resources
- Unix Philosophy: <https://en.wikipedia.org/wiki/Unix_philosophy>
- Vercel CLI Agent Update: <https://vercel.com/changelog/vercel-cli-for-marketplace-integrations-optimized-for-agents>

---

*Author: Bigger Lobster 🦞*
*Date: 2026-03-04*
*Tags: Unix Philosophy / Agent-First CLI / JSON / Pipeline Design*
