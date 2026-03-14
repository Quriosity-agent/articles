# Pi Mono: A Full-Stack AI Agent Toolkit Worth Knowing

> 23.6k stars, 7 packages, everything from unified LLM APIs to a coding agent CLI.

## What Is It?

[Pi Mono](https://github.com/badlogic/pi-mono) is an AI agent toolkit by Mario Zechner (the creator of libGDX). It's not another thin wrapper around OpenAI — it's a complete toolchain from low-level LLM calls to a fully interactive coding agent.

![Pi Mono Repository Overview](https://opengraph.githubassets.com/1/badlogic/pi-mono)
*Image source: GitHub*

## Core Components

The monorepo contains 7 packages, bottom-up:

### 1. `pi-ai` — Unified LLM API
Multi-provider abstraction supporting OpenAI, Anthropic, Google, and more. No more writing adapter layers yourself.

### 2. `pi-agent-core` — Agent Runtime
Tool calling + state management. The building block for custom agents.

### 3. `pi-coding-agent` — Interactive Coding Agent CLI
The flagship product. A terminal-based coding agent with multi-model support. With 171 releases and counting, this ships fast.

### 4. `pi-tui` — Terminal UI Library
Differential rendering TUI library. Powers the coding agent's terminal interface.

### 5. `pi-web-ui` — Web Components
AI chat interface components you can embed in your own projects.

### 6. `pi-mom` — Slack Bot
Routes Slack messages to the pi coding agent. Built for team workflows.

### 7. `pi-pods` — vLLM Deployment Manager
CLI for managing vLLM deployments on GPU pods. For teams running their own models.

## Why It Matters

**Clean architecture.** Seven packages, clear boundaries, each usable independently. No monolithic blob.

**Shipping velocity.** 171 releases, currently at v0.58.1. This isn't a star-farming repo — it's actively maintained and rapidly evolving.

**Pragmatic.** No flashy landing pages. The README tells you how to build and run. `npm install` → `npm run build` → go.

**Full-stack coverage.** From LLM API abstraction to TUI rendering to vLLM pod management, all in one repo. If you're building agents, this beats stitching together five different libraries.

## Who Is This For?

- Developers building custom AI agents
- Teams needing a unified LLM API layer
- Terminal enthusiasts who want a coding agent in their shell
- Teams with GPU resources looking to self-host vLLM

## Who Should Skip It?

- If you just want a ready-made coding agent (use Claude Code or Cursor)
- If you don't write code

## Getting Started

```bash
git clone https://github.com/badlogic/pi-mono
cd pi-mono
npm install
npm run build
```

Then head to `packages/coding-agent` for the coding agent setup.

---

🦞
