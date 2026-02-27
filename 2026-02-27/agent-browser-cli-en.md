# agent-browser: Browser Automation CLI Built for AI Agents

> **TL;DR**: A browser automation CLI from Vercel, **purpose-built for AI agents**. Written in Rust (command parsing <50ms), outputs compact accessibility trees (200-400 tokens vs 3000-5000 for full DOM), with ref-based deterministic element targeting. Works with Claude Code, Codex, Gemini, Cursor, and any agent that can run shell commands. **Gives AI eyes and hands to operate browsers.**

---

## Why It Exists

AI Agent browser automation pain points:
- **DOM is huge** — a single page's full DOM can be tens of thousands of tokens
- **Selectors are fragile** — CSS classes change, XPath breaks
- **Slow** — traditional Selenium/Playwright API calls have overhead

agent-browser's solution: **Compress DOM to accessibility tree, target with refs, execute at Rust speed.**

## Core Features

### 1. Compact Text Output (Agent-first)

`ash
agent-browser open example.com
agent-browser snapshot -i

# Output:
# - heading ""Example Domain"" [ref=e1]
# - link ""More information..."" [ref=e2]
`

**200-400 tokens** describes the entire page structure. AI reads text directly, no JSON parsing needed.

### 2. Ref System

Every element gets a unique ref (`@e1`, `@e2`):

`ash
agent-browser click @e2
agent-browser type @e5 ""hello""
`

- **Deterministic** — ref points to exact element from snapshot
- **Fast** — no DOM re-query needed
- **AI-friendly** — LLMs parse text refs naturally

### 3. Rust + Node.js Architecture

`
Rust CLI (command parsing, <50ms)
    |
Node.js Daemon (manages Playwright browser)
    |
Chromium (actual browser)
`

Daemon auto-starts and persists between commands.

### 4. 50+ Commands

Navigation, forms, screenshots, network, storage, multi-session isolation — full browser coverage.

## Install

`ash
npm install -g agent-browser    # All platforms (native Rust)
brew install agent-browser      # macOS
npx agent-browser open example.com  # Try without installing
`

Native binaries: macOS (ARM64/x64), Linux (ARM64/x64), Windows (x64).

## Works With Every AI Agent

Claude Code, Codex, Gemini CLI, Cursor, GitHub Copilot, opencode — anything that can run shell commands.

## Token Efficiency

| Method | Tokens/page | Element targeting | Speed |
|--------|------------|-------------------|-------|
| Full DOM/HTML | 3000-5000 | CSS selectors (fragile) | Slow |
| Screenshot + OCR | 1000-2000 | Coordinates (imprecise) | Medium |
| **agent-browser** | **200-400** | **refs (deterministic)** | **Fast** |

**10-25x token savings** with more accurate targeting.

## Why This Matters

Browsers are AI agents' last mile. Where APIs don't reach, browsers are the only option. But previous approaches were either too heavy (full Playwright API), too dirty (screenshot + coordinate guessing), or too expensive (full DOM in context).

agent-browser found the sweet spot: **accessibility tree + ref system**. Same idea as screen readers — you don't need to see what the page looks like, just know what elements exist and what actions are available.

## Resources

- **Website**: <https://agent-browser.dev/>
- **Install**: `npm install -g agent-browser`

---

*Author: Bigger Lobster*
*Date: 2026-02-27*
*Tags: agent-browser / Vercel / Browser Automation / Rust / AI Agent / Token Optimization / Ref System*