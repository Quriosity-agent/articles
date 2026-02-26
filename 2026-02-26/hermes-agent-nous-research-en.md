# Hermes Agent: Nous Research's Fully Open-Source Personal AI Agent

**Source: GitHub - NousResearch/hermes-agent**

---

## TL;DR

Nous Research released Hermes Agent — a fully open-source, persistent personal AI agent that lives on your server, connects to your messaging platforms (Telegram/Discord/Slack/WhatsApp), learns your projects, builds its own skills, runs scheduled tasks, and gets smarter the longer it runs. Think OpenClaw but open-source, with built-in RL training environments.

---

## Key Features

### Persistent Agent That Grows With You
Not a one-shot chatbot — a **server-resident agent** with persistent memory (MEMORY.md + USER.md) that remembers your preferences, projects, and environment across sessions.

### Any Model, Zero Lock-in
- **Nous Portal** — Subscription, zero-config
- **OpenRouter** — 200+ models, pay-per-use
- **Self-hosted** — VLLM/SGLang/any OpenAI-compatible endpoint

Switch with `hermes model` — no code changes.

### Multi-Platform Messaging Gateway
Single gateway process connects **Telegram + Discord + Slack + WhatsApp + CLI**. Cross-platform message mirroring — start on Telegram, continue on Discord.

### Self-Evolving Skills System
When the agent solves a complex problem, it writes a Skill document for next time. Skills follow the [agentskills.io](https://agentskills.io) open standard. Search, share, and install community skills via the Skills Hub.

### Five Terminal Backends (Real Sandboxing)

| Backend | Use Case |
|---------|----------|
| **Local** | Direct execution (default) |
| **Docker** | Container isolation |
| **SSH** | Remote server (recommended: agent can't modify its own code) |
| **Singularity** | HPC clusters |
| **Modal** | Serverless cloud |

### Subagent Delegation
`delegate_task` spawns isolated child agents with their own context and terminal. Up to 3 parallel. Depth limit of 2 (no grandchildren).

### Cron Scheduling
Natural language: "Every morning at 9am, send AI funding news to Telegram." Gateway runs them unattended.

### RL Training (Research-Ready)
Built-in Atropos RL framework for training tool-calling models with reinforcement learning. Batch generation of thousands of parallel trajectories, trajectory compression, custom reward functions via ToolContext.

---

## Can It Control Claude Code and Codex?

**Yes!** The terminal tool supports **PTY mode** (`pty=true`), explicitly designed for interactive CLI tools. From the README:

> "PTY mode (`pty=true`) enables interactive CLI tools like Codex and Claude Code."

This means Hermes Agent can:
1. Launch Claude Code or Codex sessions in the background
2. Monitor and send instructions via the `process` tool
3. Orchestrate multiple coding agents like an agent swarm

Combined with `delegate_task` for parallel subagents, you could theoretically build an Elvis-style agent swarm — Hermes as the orchestration layer, spawning multiple subagents each running Codex/Claude Code in isolated terminals.

**Caveat:** This is terminal-level integration (sending keystrokes, reading output), not native API integration. OpenClaw's integration with Claude Code is deeper (direct sub-agent spawning with structured results). Hermes requires more prompt engineering to manage the interaction.

---

## Comparison with OpenClaw

| Feature | Hermes Agent | OpenClaw |
|---------|-------------|---------|
| **Open Source** | ✅ MIT | ❌ Commercial |
| **Model Support** | OpenRouter 200+ / self-hosted / Nous Portal | Anthropic / OpenAI / multi-provider |
| **Messaging** | Telegram / Discord / Slack / WhatsApp / CLI | Telegram / Discord / WhatsApp / Signal / iMessage / CLI |
| **Skills System** | ✅ agentskills.io standard | ✅ Custom skill system |
| **Persistent Memory** | MEMORY.md + USER.md (token-capped) | MEMORY.md + USER.md |
| **Terminal Sandbox** | 5 backends (Docker/SSH/Modal etc.) | Local + Docker |
| **Subagents** | ✅ delegate_task | ✅ sessions_spawn |
| **Cron** | ✅ Natural language | ✅ Natural language |
| **Code Execution** | ✅ Python RPC sandbox | ✅ exec tool |
| **RL Training** | ✅ Atropos integration | ❌ |
| **Browser** | Browserbase | Chrome Relay / OpenClaw browser |
| **Voice** | Edge TTS / ElevenLabs / OpenAI | TTS tool |
| **SOUL.md** | ✅ | ✅ |
| **AGENTS.md** | ✅ Hierarchical merge | ✅ |

---

## Installation

```bash
# Linux/macOS
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/setup-hermes.sh | bash

# Windows (PowerShell)
irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/setup-hermes.ps1 | iex
```

---

## Why This Matters

1. **Fully open-source OpenClaw alternative** — MIT license, fork and modify freely
2. **Research + Product in one** — Same architecture serves as personal agent AND RL training platform
3. **By Nous Research** — One of the most respected teams in the open-source LLM community (Hermes model series)
4. **Zero model lock-in** — Any OpenAI-compatible API works, including local models
5. **Agent swarm potential** — PTY terminal + subagents = multi-agent coding orchestration

---

*Repository: <https://github.com/NousResearch/hermes-agent>*
*License: MIT*
*Article compiled from the repository README.*
