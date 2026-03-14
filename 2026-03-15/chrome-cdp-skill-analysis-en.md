# chrome-cdp-skill: Give Your AI Agent Access to Your Live Chrome Session

> No new browser instance. No re-login. No Puppeteer. Just connect to the Chrome tabs you already have open.

![chrome-cdp-skill repository](https://opengraph.githubassets.com/1/pasky/chrome-cdp-skill)
*Image source: [pasky/chrome-cdp-skill](https://github.com/pasky/chrome-cdp-skill) on GitHub*

## The Problem

Almost every browser automation tool (Puppeteer, Playwright, Selenium) launches a **fresh, isolated browser instance**. That means:

- All your login sessions are gone
- Cookies and state start from zero
- The page your agent sees is nothing like the page you're working on

For the use case of "let my AI agent interact with the page I'm currently looking at," traditional approaches completely miss the mark.

## What chrome-cdp-skill Does

[chrome-cdp-skill](https://github.com/pasky/chrome-cdp-skill) by Petr Baudiš ([@xpasky](https://x.com/xpasky)) takes a dead-simple approach:

**Connect directly to your running Chrome via the Chrome DevTools Protocol (CDP) WebSocket.**

No Puppeteer dependency. No `npm install`. Just Node.js 22+ and Chrome with remote debugging enabled.

### Installation

Pi users, one line:

```bash
pi install git:github.com/pasky/chrome-cdp-skill@v1.0.1
```

Manual setup: copy the `skills/chrome-cdp/` directory to wherever your agent loads skills from.

### Enable Chrome Debugging

Navigate to `chrome://inspect/#remote-debugging` and flip the toggle. Done.

## Command Reference

All commands run through `scripts/cdp.mjs`. `<target>` is a unique targetId prefix from `list`:

| Command | What it does |
|---------|-------------|
| `list` | List all open tabs |
| `shot <target>` | Screenshot (saves to /tmp/screenshot.png) |
| `snap <target>` | Accessibility tree (compact, semantic) |
| `html <target> [selector]` | Full HTML or scoped to a CSS selector |
| `eval <target> "expr"` | Execute JS in page context |
| `nav <target> <url>` | Navigate and wait for load |
| `click <target> "selector"` | Click element by CSS selector |
| `clickxy <target> <x> <y>` | Click at CSS pixel coordinates |
| `type <target> "text"` | Type at focused element |
| `loadall <target> "selector"` | Click "load more" until gone |
| `evalraw <target> <method> [json]` | Raw CDP command passthrough |
| `stop [target]` | Stop daemon(s) |

## Architecture Highlights

### 1. Persistent Daemon Model

On first access to a tab, chrome-cdp spawns a lightweight background daemon that holds the WebSocket connection open. Chrome's "Allow debugging" modal fires once; all subsequent commands reuse the daemon silently.

Daemons auto-exit after 20 minutes of inactivity.

### 2. Handles 100+ Tabs

Puppeteer-based tools often time out during target enumeration with many open tabs. chrome-cdp connects directly via WebSocket with one daemon per tab — no interference between tabs.

### 3. Cross-Origin iframe Support

The `type` command uses `Input.insertText`, which works inside cross-origin iframes where `eval` cannot reach.

## Comparison with chrome-devtools-mcp

Google's official [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) reconnects on every command, causing:
- Chrome's "Allow debugging" modal to reappear repeatedly
- Target enumeration timeouts with many tabs open

chrome-cdp-skill solves both problems with its persistent daemon architecture.

## Coordinate System

`shot` saves images at **native resolution** (CSS pixels × DPR). CDP input events (`clickxy`) take **CSS pixels**:

```
CSS px = screenshot px / DPR
```

On Retina (DPR=2), divide screenshot coordinates by 2 for correct click positions. `shot` prints the current page DPR.

## Use Cases

- Let AI agents operate on pages you're logged into (Gmail, GitHub, internal tools)
- Have an agent intervene mid-workflow without losing page state
- Stable automation across 100+ open tabs
- Quick debugging — much faster than spinning up a full browser automation framework

## Summary

chrome-cdp-skill's design philosophy is clear: **don't launch a new browser — connect to the one the user is already running.** The implementation matches: one script file, zero-install dependencies, direct WebSocket connection.

For the "AI sees what I see" use case, this is arguably the most lightweight and practical solution available today.

---

🦞
