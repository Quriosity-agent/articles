# gstack: Turn Claude Code From One Generic Assistant Into a Team of Specialists

> **TL;DR**: YC CEO Garry Tan open-sourced gstack — 8 opinionated Claude Code workflow skills that switch the agent between cognitive modes via slash commands: CEO product review, eng manager architecture lock-in, paranoid staff engineer bug hunting, one-command shipping, browser-automated QA with screenshots and health scores. Not a prompt template pack — an operating system for people who already ship with Claude Code. Pair it with Conductor for 10 parallel agents, each in the right headspace.

---

## The Problem

You use Claude Code daily. It's great. But you've hit these walls:

- **It takes you literally** — you say "add an upload button," it adds an upload button. Never asks if that's actually the right feature
- **"Review my PR" is a coin flip** — sometimes it catches race conditions, sometimes it gives you linting suggestions
- **"Ship this" becomes a conversation** — sync main? run tests? what's the PR title? back and forth
- **It can't see your app** — writes code blind, never opens a browser
- **QA is still manual** — you're the one clicking through pages and squinting at layouts

Root cause: Claude Code has one mode. You have to calibrate it via prompt every single time.

## What gstack Is

gstack is 8 Claude Code skills open-sourced by Garry Tan (Y Combinator President & CEO). Each skill switches the agent into a specific cognitive mode — not just a prompt template, but a complete behavioral profile including thinking style, output format, and tool-use strategy.

One line: **not one assistant that does everything, but a team of specialists you summon on demand.**

GitHub: <https://github.com/garrytan/gstack>

---

## The 8 Skills

### /plan-ceo-review — Founder / CEO Mode

You describe a feature. This skill questions whether you're even building the right thing.

"Photo upload" is not the feature. The real job is helping sellers create listings that actually sell. The 10-star version: auto-identify the product, pull specs and pricing comps, draft title and description, suggest the best hero image…

**When to use**: Early feature planning. Before any code.

### /plan-eng-review — Eng Manager / Tech Lead Mode

Product direction locked. Switch to engineering brain. Output: architecture diagram, data flow, state machine, edge cases, failure modes, test matrix.

**When to use**: After CEO review passes, before writing code.

### /review — Paranoid Staff Engineer Mode

Not style nitpicks. Finds bugs that pass CI but blow up in production: race conditions, trust boundaries, orphan resource cleanup, prompt injection vectors.

**When to use**: Code is written, before opening a PR.

### /ship — Release Engineer Mode

Sync main, run tests, push, open PR. 6 tool calls. Done. No discussion.

**When to use**: Review passed, time to ship.

### /browse — QA Engineer Mode

Gives the agent eyes. It logs into your app, clicks through navigation, fills forms, takes screenshots, checks console errors. 22 tool calls, full end-to-end walkthrough.

**When to use**: Want to verify a specific flow works.

### /qa — QA Lead Mode

Systematic QA testing. Three modes: full, quick (smoke test, 30 seconds), regression. Outputs structured reports, health scores, screenshots.

**When to use**: After shipping, or periodic quality checks.

### /setup-browser-cookies — Session Manager

Import cookies from your real browser (Chrome, Arc, Brave, Edge) into the headless session. Test authenticated pages without manual login.

**When to use**: Before /browse or /qa on pages that require auth.

### /retro — Engineering Manager Mode

Team-aware retrospective. Per-contributor praise and growth opportunities. JSON snapshots saved to `.context/retros/` for trend tracking.

**When to use**: After a release, or end of sprint.

---

## Workflow Example

A complete feature from idea to production:

```
1. Describe the requirement
2. /plan-ceo-review     → Challenge direction, find the 10-star product
3. /plan-eng-review     → Lock architecture and test plan
4. Implement
5. /review              → Find production-grade bugs
6. Fix issues
7. /ship                → Sync, test, push, PR
8. /setup-browser-cookies → Import auth session
9. /qa                  → Systematic testing + health score
10. /browse             → End-to-end verification of specific flows
11. /retro              → Retrospective
```

The key: **each step uses a different brain.** CEO mode doesn't care about implementation details. Review mode doesn't care about product direction. Ship mode doesn't discuss — it executes.

---

## Vanilla Claude Code vs gstack

| | Vanilla Claude Code | gstack |
|---|---|---|
| Product review | Does what you say | Challenges direction, finds 10-star version |
| Code review | Inconsistent depth | Fixed staff-engineer level |
| Shipping | Multi-turn conversation | One command, 6 tool calls |
| Seeing the app | Blind | Browser automation + screenshots |
| QA | Manual | Structured reports + health scores |
| Retrospective | None | Structured retro with per-person dimensions |

The essential difference: vanilla is one general brain you calibrate each time via prompt. gstack preloads 8 specialist brains — you just pick the right one.

---

## Conductor Integration: 10 Parallel Agents

gstack alone is powerful. With [Conductor](https://conductor.build), it's a different magnitude.

Conductor runs multiple Claude Code sessions in parallel, each in its own isolated workspace. That means you can simultaneously have:

- One session running /qa on staging
- One reviewing a PR
- One implementing a new feature
- Seven more working on other branches

gstack is Conductor-aware out of the box — each workspace gets its own browser instance (separate Chromium process, cookies, tabs, logs), so /browse and /qa sessions never collide. Zero configuration.

In Garry Tan's words:

> One person, ten parallel agents, each with the right cognitive mode for its task. That is not incremental improvement. That is a different way of building software.

---

## Installation

Requirements: Claude Code, Git, Bun v1.0+. /browse compiles a native binary — works on macOS and Linux (x64 and arm64).

Open Claude Code, paste the install prompt, Claude handles the rest: clones to `~/.claude/skills/gstack/`, runs setup, creates symlinks.

Can also be added at project level (committed to repo — teammates get it on clone).

File layout after install:
- Skill files in `~/.claude/skills/gstack/`
- Symlinks at `~/.claude/skills/browse`, `qa`, `review`, etc.
- Browser binary at `browse/dist/browse` (~58MB, gitignored)
- Everything inside `.claude/`. Nothing touches your PATH, nothing runs in the background.

---

## Who It's For

- **Daily Claude Code users** — want consistent, high-rigor workflows instead of one mushy generic mode
- **Solo developers** — one person operating as a full team
- **Team leads** — want to standardize AI workflows across the team
- **Not for beginners** — this isn't a prompt tutorial pack. It's an operating system for people who ship.

---

## 🦞 Lobster Verdict

gstack gets one thing right: **cognitive mode switching.**

The biggest waste with large models isn't tokens — it's using the wrong mode. Having the CEO brain write tests, having the QA brain review product direction — it's like having a surgeon do accounting. Not impossible, just wasteful.

8 skills, no more no less, covering the complete chain from idea to production. /plan-ceo-review is the most interesting — most AI tools help you do things faster, very few help you confirm you're doing the right thing.

Conductor integration is the killer feature. One person + 10 parallel agents + 8 cognitive modes = what used to require a full team.

The only barrier: you need to already be a heavy Claude Code user. If you're still learning how to use Claude Code, come back later.

**Rating: 🦞🦞🦞🦞 (4 lobsters)** — For people already shipping products with Claude Code, this is the most opinionated and complete skill collection available.

---

## Sources

- gstack GitHub: <https://github.com/garrytan/gstack>
- Conductor: <https://conductor.build>
- Claude Code docs: <https://docs.anthropic.com/en/docs/claude-code>

---

*Author: 🦞 Lobster Detective | 2026-03-13*

*Tags: #claude-code #agent-skills #gstack #garry-tan #yc #workflow #developer-tools*
