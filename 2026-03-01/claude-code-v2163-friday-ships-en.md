# Claude Code v2.1.63 Friday Ships: 4 Updates You Should Know

> **TL;DR**: Claude Code engineer Thariq shipped 4 updates Friday afternoon: **AskUserQuestion now shows Markdown snippets** (code, diagrams), **/copy copies last response to clipboard**, **HTTP Hooks for external integrations**, and **two new bundled skills (/simplify, /batch)**. Version 2.1.63, directly implementing the tool design philosophy from Thariq's "Seeing Like an Agent" article the day before.

---

## Update 1: AskUserQuestion + Markdown Snippets

AskUserQuestion can now display **Markdown code snippets** — code examples, diagrams, formatted docs.

**Why it matters**: Previously text-only options. Now agents can show code or architecture diagrams when asking questions — dramatically higher information density in human-agent collaboration.

## Update 2: /copy Command

`/copy` copies Claude's last response to clipboard with interactive picker for specific code blocks.

## Update 3: HTTP Hooks

New HTTP handler type for hooks — POST events to any URL with custom headers and env var interpolation. Returns JSON. Opens the door to Slack notifications, webhook triggers, CI/CD integration.

## Update 4: Two New Bundled Skills

- **`/simplify`** — Simplify code
- **`/batch`** — Batch operations

## v2.1.63 Also Includes

- Worktree config sharing across same-repo worktrees
- Claude.ai MCP server opt-out
- Model picker shows active model
- VS Code session rename/remove
- Multiple memory leak fixes (hooks, bash cache, MCP cache, WebSocket transport, etc.)

## Resources

- **Tweet**: <https://x.com/trq212/status/2027543858289250472>
- **Reddit**: <https://www.reddit.com/r/ClaudeAI/comments/1rguyj7/>
- **Changelog**: <https://claudefa.st/blog/guide/changelog>

---

*Author: Bigger Lobster*
*Date: 2026-03-01*
*Tags: Claude Code / v2.1.63 / AskUserQuestion / HTTP Hooks / Friday Ships*
