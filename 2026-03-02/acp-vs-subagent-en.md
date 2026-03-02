# ACP vs Sub-Agent: Two Modes of AI Agent Collaboration — Which One to Pick?

> **TL;DR**: Agent Client Protocol (ACP) and Sub-Agents are two collaboration modes. **ACP is a standardized protocol** — like LSP made language servers universal across IDEs, ACP makes coding agents universal across editors. **Sub-Agent is internal delegation** — a parent agent spawns child tasks. Choose based on: **cross-system interop** (ACP) vs **internal task dispatch** (Sub-Agent).

---

## Quick Distinction

| | ACP | Sub-Agent |
|--|-----|-----------|
| **Analogy** | USB-C — standard interface, plug and play | Internal email — boss assigns tasks to team |
| **Nature** | **Protocol** | **Pattern** |
| **Solves** | Agent ↔ Editor interop | Task decomposition & parallel execution |

## What Is ACP?

Initiated by Zed, ACP solves the N×M integration explosion between agents and editors — same approach as LSP for language servers.

- **Communication**: JSON-RPC 2.0 over stdin/stdout (local) or HTTP/WebSocket (remote)
- **Reuses MCP types**: No reinventing the wheel
- **Bidirectional**: Agent can request permissions from editor
- **30+ agents supported**: Claude Code, Codex, Gemini CLI, Copilot, Cursor, OpenClaw, Kiro, Windsurf...

## What Is Sub-Agent?

Internal task delegation — parent agent breaks large tasks into subtasks for child agents.

- **Same runtime**: Runs inside OpenClaw
- **Auto-reports**: Notifies parent on completion
- **Steerable**: Parent can steer or kill child agents
- **Shared workspace**: Access to parent's filesystem

## Comparison

| Dimension | ACP | Sub-Agent |
|-----------|-----|-----------|
| **Positioning** | Cross-system protocol | Internal delegation |
| **Runtime** | External agent process | OpenClaw internal |
| **Communication** | JSON-RPC stdio | Internal messaging |
| **Thread binding** | ✅ Supported | ❌ Not directly |
| **Persistent sessions** | ✅ `mode: "session"` | ❌ Usually one-shot |
| **Use case** | Professional coding with Codex/Claude Code | Quick background tasks |

## When to Use Which

**ACP**: Need specific external agent, persistent conversation, thread binding, or agent-specific capabilities.

**Sub-Agent**: Quick one-shot tasks, parallel execution, keeping main agent responsive.

**Neither**: Simple edits, quick queries — just use the main agent directly.

## ACP's Ecosystem Significance

Like LSP revolutionized language server integration (write once, run everywhere), ACP does the same for coding agents. Any ACP agent works with any ACP editor — plug and play.

## Resources

- **ACP**: <https://agentclientprotocol.com>
- **OpenClaw ACP**: <https://docs.openclaw.ai/tools/acp-agents>
- **OpenClaw Sub-Agents**: <https://docs.openclaw.ai/tools/subagents>

---

*Author: Bigger Lobster*
*Date: 2026-03-02*
*Tags: ACP / Sub-Agent / Agent Client Protocol / OpenClaw / Zed / LSP*
