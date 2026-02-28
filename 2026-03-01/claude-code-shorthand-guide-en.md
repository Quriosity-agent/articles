# The Shorthand Guide to Everything Claude Code: 10 Months of Daily Use

> **TL;DR**: cogsec (@affaanmustafa) shares a complete Claude Code setup after 10 months of daily use — Skills, Hooks, Subagents, MCPs, Plugins, all covered. **Core lesson: Context Window is your most precious resource. Configure 20-30 MCPs but keep under 10 enabled.** 7,600+ likes, Anthropic x Forum Ventures hackathon winner. The most comprehensive Claude Code configuration guide to date.

---

## Six Modules Overview

| Module | Purpose | Location |
|--------|---------|----------|
| **Skills** | Workflow shortcuts | `~/.claude/skills/` |
| **Commands** | Slash commands | `~/.claude/commands/` |
| **Hooks** | Event-driven automation | JSON config |
| **Subagents** | Task delegation | `~/.claude/agents/` |
| **MCPs** | External service connections | `~/.claude.json` |
| **Plugins** | Bundled toolsets | Plugin marketplace |

## Skills & Commands

Skills are scoped workflow shortcuts that can be **chained** in a single prompt:
- `/refactor-clean` — Clean dead code after long sessions
- `/tdd`, `/e2e`, `/test-coverage` — Testing workflows

## Hooks — Event-Driven Automation

| Type | When | Use |
|------|------|-----|
| PreToolUse | Before tool runs | Validation, reminders |
| PostToolUse | After tool finishes | Formatting, type checking |
| Stop | Claude finishes | Audit for console.logs |

**Author's production hooks:** tmux reminders, block unnecessary .md files, auto-Prettier, TypeScript checks, console.log warnings.

> **Pro tip:** Use `hookify` plugin to create hooks conversationally!

## Subagents — Task Delegation

9 specialized agents: planner, architect, tdd-guide, code-reviewer, security-reviewer, build-error-resolver, e2e-runner, refactor-cleaner, doc-updater.

**Key: Scope each subagent with limited tools = focused execution.**

## Context Window Management (Most Important)

**200k context with too many tools might leave only 70k effective.**

- Configure 20-30 MCPs, enable only 5-6 per project
- Install many plugins, enable only 4-5 at a time
- Keep under 80 tools active
- Use `disabledMcpServers` per project

## Efficiency Tips

- `/fork` — Parallel conversations for non-overlapping tasks
- **Git Worktrees** — Multiple Claude instances without conflicts
- **mgrep** — Better than ripgrep, local + web search
- `Ctrl+U` delete line, `Tab` toggle thinking, `Esc Esc` interrupt

## Key Takeaways

1. Don't overcomplicate — configuration is fine-tuning, not architecture
2. Context window is precious — disable unused MCPs/plugins
3. Parallel execution — fork conversations, git worktrees
4. Automate repetitive — hooks for formatting, linting
5. Scope subagents — limited tools = focused execution

## Resources

- **Original**: <https://x.com/affaanmustafa/status/2012378465664745795>
- **Author**: cogsec (@affaanmustafa) — Anthropic x Forum Ventures hackathon winner

---

*Author: Bigger Lobster*
*Date: 2026-03-01*
*Tags: Claude Code / Skills / Hooks / Subagents / MCP / Plugins / Context Window*
