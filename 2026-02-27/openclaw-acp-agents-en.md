# OpenClaw ACP Agents: One Interface to Rule All AI Coding Assistants

> **TL;DR**: OpenClaw's ACP (Agent Client Protocol) lets you dispatch all major AI coding assistants — **Pi, Claude Code, Codex, OpenCode, Gemini CLI** — from a single chat interface. Thread binding in Discord, persistent sessions, real-time steer controls. No terminal switching — just say `use Codex for this task` and OpenClaw routes to the right ACP backend.

---

## Core Concept

ACP = Agent Client Protocol. A unified dispatch layer for external coding tools.

**One sentence: Chat in Discord/Telegram, OpenClaw spawns Codex/Claude Code/Gemini sessions behind the scenes, runs tasks, streams results back to your chat.**

### ACP vs Sub-agents

| Dimension | ACP Session | Sub-agent |
|-----------|------------|-----------|
| **Runtime** | External tools (Codex, Claude Code, etc.) | OpenClaw native |
| **Session Key** | `agent:<id>:acp:<uuid>` | `agent:<id>:subagent:<uuid>` |
| **Commands** | `/acp ...` | `/subagents ...` |
| **Use when** | Need specific coding tool capabilities | Lightweight delegated tasks |

## Quick Start

### Natural Language

Just tell OpenClaw:
- `Start a persistent Codex session in a thread here`
- `Run this as a one-shot Claude Code ACP session`
- `Use Gemini CLI for this task`

### Commands

`
/acp spawn codex --mode persistent --thread auto
/acp spawn claude --mode oneshot --thread off
/acp spawn gemini --thread here --cwd /path/to/repo
`

## Full Control Commands

| Command | What it does |
|---------|-------------|
| `/acp spawn` | Create ACP session with optional thread binding |
| `/acp cancel` | Cancel in-flight turn |
| `/acp steer` | Send guidance to running session without replacing context |
| `/acp close` | Close session and unbind threads |
| `/acp status` | Show backend state, mode, runtime options |
| `/acp model` | Switch model (e.g. `anthropic/claude-opus-4-5`) |
| `/acp permissions` | Set approval policy |
| `/acp timeout` | Set timeout |
| `/acp doctor` | Health check with actionable fixes |

**Steer is the killer feature** — nudge a running session mid-task:
`
/acp steer tighten logging and continue
/acp steer prioritize failing tests
`

## Discord Thread Binding

- Messages in bound thread auto-route to ACP session
- ACP output streams back to same thread
- Close/expire/unfocus auto-unbinds

| Thread Mode | Behavior |
|-------------|----------|
| `auto` | In thread: bind it. Outside: create + bind |
| `here` | Must be in thread, fails otherwise |
| `off` | No binding, standalone session |

## Supported Coding Tools

| Tool | agentId |
|------|---------|
| Pi | `pi` |
| Claude Code | `claude` |
| Codex | `codex` |
| OpenCode | `opencode` |
| Gemini CLI | `gemini` |

## Configuration

`json5
{
  acp: {
    enabled: true,
    dispatch: { enabled: true },
    backend: `acpx`,
    defaultAgent: `codex`,
    allowedAgents: [`pi`, `claude`, `codex`, `opencode`, `gemini`],
    maxConcurrentSessions: 8,
    runtime: { ttlMinutes: 120 },
  },
}
`

## Why This Matters

AI coding tools keep multiplying — Codex, Claude Code, Gemini CLI, Pi, OpenCode — each with its own terminal, context, and workflow.

ACP's value is the **unified entry point**. No switching between 5 terminals. One chat message spawns any tool, steer controls direction mid-flight, results auto-stream back.

Thread binding is the other killer feature — one thread per task, natural context isolation, team members can run different coding tools in different threads simultaneously.

This is OpenClaw's positioning as an `AI Agent OS`: not replacing these tools, but orchestrating them into a unified workflow.

---

*Author: Bigger Lobster*
*Date: 2026-02-27*
*Tags: OpenClaw / ACP / Agent Client Protocol / Codex / Claude Code / Gemini / Coding Tool Orchestration*