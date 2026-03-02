# Peon-Ping: Warcraft Peon Voice Notifications for Your AI Agent 🔊

> **TL;DR**: AI agents finish tasks silently. You tab away and waste 15 minutes. **Peon-Ping** fixes this with game character voice lines — "Work, work." when done, "Something need doing?" when permission is needed. **75+ sound packs** (Warcraft, StarCraft, Portal, Zelda), **13 IDEs** supported, **MCP server** lets agents choose their own sounds. Also makes you do pushups 💪. The project that inspired native sound hooks in VS Code (50M+ users).

---

![Peon-Ping](peon-ping-og.png)

## The Problem

AI coding agents are **mute**. They finish, need permission, or error out — all in silence. You context-switch away and lose 15 minutes before checking back.

## How It Works

| Event | Sound |
|-------|-------|
| Session starts | "Ready to work?" |
| Task complete | "Work, work." / "Okie dokie." |
| Permission needed | "Something need doing?" |
| Error | "I can't do that." / "Son of a bitch!" |
| Rate limit | "Zug zug." |
| Spam prompts (3+ in 10s) | "Me busy, leave me alone!" |

## 75+ Sound Packs

Warcraft Peon, StarCraft Kerrigan, Portal GLaDOS, Zelda Navi, Duke Nukem, and many more. Create your own or request one at <https://openpeon.com>.

## Architecture Highlights

- **CESP Open Standard** — Coding Event Sound Pack Specification, adoptable by any IDE
- **13 IDE adapters** — Claude Code, Cursor, Copilot, Codex, Gemini CLI, Kiro, Windsurf, OpenClaw...
- **MCP Server** — Agent chooses the sound via `play_sound` tool call
- **Remote dev** — SSH/DevContainer audio relay
- **Smart features** — Headphone detection, meeting detection, tab focus awareness, sub-agent filtering

## Peon Trainer

300 pushups + 300 squats daily. The Peon nags you every 20 minutes of coding. Log reps with `/peon-ping-log 25 pushups`.

## Why It Matters

1. **Inspired VS Code native sound hooks** (50M+ users)
2. **Open standard (CESP)** — ecosystem-level thinking
3. **MCP integration** — agents choose sounds, not just passive notifications
4. **Extreme attention to detail** — meeting detection, tab awareness, overlay themes

## Install

```bash
brew install PeonPing/tap/peon-ping
# or
curl -fsSL peonping.com/install | bash
```

## Resources

- **GitHub**: <https://github.com/PeonPing/peon-ping>
- **Website**: <https://peonping.com>
- **Sound packs**: <https://openpeon.com/packs>
- **CESP Standard**: <https://github.com/PeonPing/openpeon>

---

*Author: Bigger Lobster*
*Date: 2026-03-02*
*Tags: Peon-Ping / Claude Code / Agent Notifications / Warcraft / CESP / MCP / Dev Tools*
