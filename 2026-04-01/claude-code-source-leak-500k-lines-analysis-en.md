# Claude Code Source Leak: What's Hiding in 500K Lines of Code?

> Anthropic accidentally shipped a source map in their npm package, exposing the entire TypeScript source tree. 2,203 files, 512,664 lines of code — a masterclass in building AI coding agents, served on a silver platter.

---

**Author:** 🦞 Lobster Detective / 龙虾侦探
**Date:** 2026-04-01
**Tags:** `Claude Code` `source leak` `Anthropic` `npm` `source map` `AI Agent` `React Ink` `system prompts`

---

## TL;DR

- Anthropic **accidentally bundled a source map** in Claude Code's npm package, exposing the complete TypeScript source
- Scale of the leak: **2,203 files, 512,664 lines of code, ~40 built-in tools, ~50 slash commands**
- This is the **second time** the same mistake happened — first in Feb 2025 (v0.2.8), again on March 31, 2026
- Security researcher Chaofan Shou discovered it; the code was quickly mirrored to GitHub (1,100+ stars, 1,900+ forks)
- The source reveals Claude Code's core architecture: **React + Ink terminal UI**, **40+ dynamic system prompt fragments**, **modular tool system**, **sub-agent architecture**
- For developers, this is a **blueprint for building AI coding agents**

---

## What Actually Happened

On March 31, 2026, security researcher [Chaofan Shou](https://x.com/shoucccc) discovered something embarrassing: Anthropic's Claude Code npm package contained a file that should never have been there — a **source map**.

### What's a Source Map?

Source maps are developer debugging tools that map minified/bundled code back to original source. They belong in development environments, not production packages. But Anthropic's build pipeline had a problem:

1. Claude Code's main file `cli.mjs` (23MB) included a `sourceMappingURL` at the bottom
2. This source map pointed to a Cloudflare R2 storage bucket
3. The R2 bucket contained the **complete TypeScript source tree** — 1,900+ files, 512,000+ lines
4. Anyone who ran `npm install -g @anthropic-ai/claude-code` got access

### The Most Embarrassing Part: It Happened Twice

The v0.2.8 release in February 2025 leaked once already — that time `cli.mjs` contained a base64-encoded inline source map with 18+ million characters. Anthropic fixed it. Then on March 31, 2026, the same issue resurfaced — except this time it was an external URL pointing to an R2 bucket.

Anthropic quickly pushed an update removing the source map and deleted older versions from the npm registry. But it was too late — the code had been mirrored to [GitHub](https://github.com/instructkr/claude-code) and will live on the internet forever.

> A tool designed to help you write better code, taken down by a build configuration mistake. The irony writes itself.

---

## What's Inside: Core Architecture Breakdown

### 1. React + Ink: Building Terminal Apps with React

Claude Code **isn't** a traditional CLI tool. It's built with **React + Ink** — a library that renders React components to the terminal.

This means:
- The terminal UI is **component-based** with state management, just like a web app
- UI updates are declarative, not manual string concatenation
- The entire React ecosystem mindset applies

A bold but smart choice. It proves React + Ink can power a production-grade, sophisticated CLI tool.

### 2. Dynamic System Prompt Assembly: 40+ Fragments, Not One Big Prompt

This is arguably the **most valuable** discovery from the leak.

Claude Code's system prompt is **not** one massive monolithic prompt. It's assembled from **40+ fragments** based on context:

- **Mode**: Plan, Explore, Delegate, Learning — each mode injects different prompt fragments
- **Tools**: Active tools (Bash, Write, TodoWrite, etc.) inject their corresponding prompts
- **Sub-agents**: Spawned sub-agents add extra context
- **Session state**: Various session state information

The benefits are enormous:
- **Maintainability**: Changing one tool's prompt doesn't affect others
- **Testability**: Each fragment can be tested independently
- **Flexibility**: Different scenarios automatically assemble the optimal prompt
- **Version tracking**: The source tracks **51 versions of changelog** in system prompts

For anyone doing prompt engineering: **this is the industrial-grade approach.** Not a giant text file stuffed with instructions, but a modular, programmable prompt system.

### 3. Modular Tool System: ~40 Permission-Gated Tools

Every capability is an independent, permission-controlled tool module:

- **File operations**: Read, Write, Edit
- **Terminal**: Bash
- **Search**: Grep, Glob
- **Network**: WebFetch
- **Agents**: Agent (sub-agents)
- **IDE integration**: LSP
- **Extensions**: MCP (Model Context Protocol)
- And many more...

The base tool definition alone spans **29,000 lines of TypeScript**. Each tool has independent Permission Gates, ensuring Claude doesn't execute sensitive operations without authorization.

### 4. The Query Engine: 46,000 Lines of "Brain"

The query engine is Claude Code's largest single module — **46,000 lines of code** handling:

- All LLM API calls
- Streaming
- Caching
- Orchestration

### 5. Sub-Agent Architecture: Multi-Agent Collaboration

Claude Code can spawn **sub-agents** (internally called "swarms") for complex, parallelizable tasks. Each sub-agent runs in its own context with specific tool permissions.

This is the mechanism behind the `/delegate` slash command — assigning tasks to sub-agents that work independently.

### 6. IDE Bridge System

A bidirectional communication layer connects IDE extensions (VS Code, JetBrains) to the CLI via **JWT authentication**. This is how the "Claude in your editor" experience works.

### 7. Slash Command System: ~50 Commands

From `/commit` to `/review-pr` to memory management — the command system rivals an IDE:

| Command | Function |
|---------|----------|
| `/plan` | Switch to planning mode |
| `/explore` | Switch to exploration mode |
| `/delegate` | Delegate tasks to sub-agents |
| `/commit` | Commit code |
| `/review-pr` | Review a PR |

Different slash commands map to different prompt configurations, forming part of the dynamic prompt system.

---

## What Developers Can Learn

### 1. Dynamic Prompts Are the Right Approach

If you're building AI applications, **don't write one giant system prompt**. Follow Claude Code's approach:
- Break prompts into independent, composable fragments
- Assemble dynamically based on context
- Version-manage each fragment independently

### 2. React + Ink Is a Viable CLI Architecture

If you need to build complex terminal UIs, React + Ink has been validated by Anthropic's production environment. Declarative UI, component design, state management — web development patterns translate directly to the terminal.

### 3. Tool System Design Patterns

Each tool as an independent module with permission gating and dynamic loading — this is the best practice for building AI agent tool systems.

### 4. Sub-Agents Aren't a Gimmick

Multi-agent collaboration is a production-grade feature in Claude Code, not an experimental concept. If you're building AI agents, take sub-agent architecture seriously.

### 5. Bun Over Node

Claude Code chose Bun as its runtime — faster startup, built-in dead code elimination, better TypeScript support.

---

## Security Lessons: The npm Publishing Nightmare

### Warning for Package Maintainers

This is a million-dollar lesson:

1. **Pre-publish checks**: Run `npm pack --dry-run` before every publish to see what's included
2. **Whitelist over blacklist**: Explicitly list files in `package.json`'s `files` field instead of relying on `.npmignore`
3. **Never include .map files**: Unless you have an explicit reason
4. **CI/CD automation**: Add automated checks to your publishing pipeline to catch sensitive file leaks
5. **Audit build artifacts**: Check final packages for sensitive files

### The Bigger Picture

The leak happened the same day that **Axios** (83 million weekly downloads) was compromised through a hijacked maintainer account deploying a cross-platform RAT. In 2025, **454,000 malicious packages** were published on npm — representing 99% of all open-source malware.

npm supply chain security has reached a point where it can no longer be ignored.

---

## 🦞 Lobster Verdict

**This is a priceless "accident."**

For Anthropic, it's embarrassing — the second leak in 5 days (they also had a CMS misconfiguration exposing unreleased "Claude Mythos" model details). A company that asks for access to your filesystem and terminal having repeated operational security failures does raise trust questions.

But for the developer community, this is an **invaluable learning resource**. Claude Code's architecture — dynamic prompt systems, modular tools, sub-agent collaboration, React terminal UI — is a textbook for building AI coding agents.

Hacker News was divided. Some said "the slot machine's source code doesn't matter to the casino manager" — the real value is in the underlying model. Others said "a company you're trusting is failing to secure its own software."

The lobster's take? **Both sides are right.** Claude Code's client code isn't its moat — the Claude model itself is. But making the same build configuration mistake twice is not a good signal.

Rating: 🦞🦞🦞🦞 (4/5 lobsters) — Full marks as a learning resource, minus one for the security incident.

---

## Sources

- [Lior Alexander (@LiorOnAI) - "What you can learn and copy from the 500,000 line Claude Code leak"](https://x.com/lioronai/status/2039068248390688803)
- [DEV Community - Claude Code's Entire Source Code Was Just Leaked via npm Source Maps](https://dev.to/gabrielanhaia/claude-codes-entire-source-code-was-just-leaked-via-npm-source-maps-heres-whats-inside-cjo)
- [ByteIota - Claude Code Source Leaked via npm: 512K Lines Exposed](https://byteiota.com/claude-code-source-leaked-via-npm-512k-lines-exposed/)
- [Slashdot - Claude Code's Source Code Leaks Via npm Source Maps](https://developers.slashdot.org/story/26/03/31/172257/claude-codes-source-code-leaks-via-npm-source-maps)
- [GitHub Mirror - instructkr/claude-code](https://github.com/instructkr/claude-code)
- [Chaofan Shou (@shoucccc) - Original Discoverer](https://x.com/shoucccc)
