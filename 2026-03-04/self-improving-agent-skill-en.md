# Self-Improving Agent: Teaching AI to Keep an "Error Journal" for Continuous Learning

> **TL;DR**: An OpenClaw/Claude Code skill that makes AI agents log errors, corrections, and feature requests to `.learnings/` markdown files. When patterns recur 3+ times, they get "promoted" to project memory (CLAUDE.md/AGENTS.md). Source code reviewed — safe and clean.

---

## How It Works
```
Agent makes mistake → .learnings/ERRORS.md
User corrects agent → .learnings/LEARNINGS.md
User wants feature  → .learnings/FEATURE_REQUESTS.md
        ↓
Accumulate + verify
        ↓
Promote to CLAUDE.md / AGENTS.md / TOOLS.md
        ↓
Future sessions auto-read → same mistake never repeated
```

## Hook System
- **activator.sh**: Post-prompt reminder (~50-100 tokens overhead)
- **error-detector.sh**: Detects 20+ error patterns in Bash output
- **handler.js**: OpenClaw bootstrap injection (virtual file)

## Promotion Rules
- Recurrence >= 3 times
- Seen across 2+ distinct tasks
- Within 30-day window
→ Auto-promote to CLAUDE.md / AGENTS.md / TOOLS.md

## Source Code Review: ✅ Safe
- No network requests, no data exfiltration
- Only reads/writes local `.learnings/` directory
- Hooks only inject text reminders
- 15 files total, all transparent

## Resources
- ClawHub: <https://clawhub.ai/pskoett/self-improving-agent>
- GitHub: <https://github.com/peterskoett/self-improving-agent>

---

*Author: Bigger Lobster 🦞*
*Date: 2026-03-04*
*Tags: Self-Improving Agent / Continuous Learning / Error Logging*
