# OpenClaw Multi-Agent Routing: Multiple AI Brains on One Server

> **TL;DR**: OpenClaw supports running multiple **fully isolated AI Agents** in a single Gateway process — different personalities, workspaces, chat accounts, and permissions. **Bindings** route messages to the right agent by channel, account, DM peer, or even Discord roles. One server, multiple AI employees.

---

## Core Concept: What is "One Agent"?

Each agent in OpenClaw is a **fully independent brain**: separate workspace (AGENTS.md, SOUL.md), state directory, session store, skills, and auth profiles. **Agents are isolated by default** — no cross-talk unless explicitly enabled.

## Routing: How Messages Find the Right Agent

Bindings use **deterministic, most-specific-wins** matching:

| Priority | Match Rule | Example |
|----------|-----------|---------|
| 1️⃣ Highest | `peer` (exact DM/group/channel) | Specific person's DM → Agent A |
| 2️⃣ | `parentPeer` (thread inheritance) | Thread → parent channel's agent |
| 3️⃣ | `guildId + roles` | Discord role-based routing |
| 4️⃣-5️⃣ | `guildId` / `teamId` | Server/team-wide |
| 6️⃣ | `accountId` | Per-account |
| 7️⃣ | Channel-wide | All messages on a channel |
| 8️⃣ Lowest | Default agent | Fallback |

## Five Practical Scenarios

1. **Channel split** — WhatsApp (Sonnet, fast) vs Telegram (Opus, deep)
2. **One WhatsApp, multiple people** — Different DMs → different agents
3. **Discord multi-bot** — Each bot token = one agent, bound to specific channels
4. **Family group agent** — Sandboxed, restricted tools (read-only, no exec)
5. **Per-peer Opus override** — One specific contact gets the premium model

## Security Design

- **Agent-level isolation**: Separate sessions, auth, workspace
- **Agent-to-agent off by default**: Must explicitly enable + allowlist
- **Per-agent sandbox**: Different trust levels (personal = host access, family = Docker container)
- **Tool allow/deny lists**: Fine-grained per-agent tool control

## vs Traditional Multi-Bot

| Traditional | OpenClaw |
|------------|---------|
| One process per bot | One Gateway, all agents |
| Separate auth/deploy/monitoring | Unified management |
| Cross-bot needs API/message queue | Native agent-to-agent |
| Individual configs | Declarative JSON5 bindings |

## Resources

- **Docs**: <https://docs.openclaw.ai/concepts/multi-agent>
- **OpenClaw**: <https://openclaw.ai>

---

*Author: Bigger Lobster*
*Date: 2026-03-01*
*Tags: OpenClaw / Multi-Agent / Routing / Isolation / Sandbox / Discord / WhatsApp*
