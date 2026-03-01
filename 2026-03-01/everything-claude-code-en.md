# Everything Claude Code: The 50K-Star AI Agent Performance System

> **TL;DR**: **Everything Claude Code (ECC)** is a 50K+ star open-source project providing a **complete performance optimization system** for AI coding agents — 13 agents, 56 skills, 32 commands. Covers token optimization, memory persistence, continuous learning, security scanning, multi-agent orchestration. Works across Claude Code, Codex, Cowork, OpenCode. From an Anthropic hackathon-winning team, refined over 10+ months of daily production use.

---

## Not Another Dotfile Repo

Most Claude Code "configs" are a settings file and some rules. ECC is a **system**:

| Layer | Contents | Count |
|-------|----------|-------|
| **Agents** | Specialized sub-agents (planner, architect, TDD, security...) | 13 |
| **Skills** | Workflow definitions and domain knowledge | 56 |
| **Commands** | Slash commands | 32 |
| **Rules** | Coding standards (TS/Python/Go/Java) | Multi-lang |
| **Hooks** | Lifecycle hooks (auto-save context, continuous learning) | Node.js |
| **Tests** | Internal validation | 992 |

## Six Core Capabilities

1. **Token Optimization** — Model selection, prompt slimming, background processes
2. **Memory Persistence** — Hooks auto-save/load context across sessions
3. **Continuous Learning** — `/learn` extracts patterns; Instinct v2 with confidence scoring
4. **Verification Loops** — Checkpoint vs continuous evals, grader types, pass@k
5. **Parallelization** — Git worktrees, cascade method, PM2 multi-agent
6. **Security Scanning** — AgentShield integration, 1282 tests, 102 rules

## Install (2 minutes)

```bash
/plugin marketplace add affaan-m/everything-claude-code
/plugin install everything-claude-code@everything-claude-code
```

## Multi-Framework Support

Works with Claude Code, Codex, Cowork, OpenCode, and Cursor.

## Stats

| Metric | Value |
|--------|-------|
| ⭐ Stars | 50,000+ |
| 🍴 Forks | 6,000+ |
| 👥 Contributors | 30+ |
| 🧪 Tests | 992 |
| 🏆 | Anthropic Hackathon Winner |

## Resources

- **GitHub**: <https://github.com/affaan-m/everything-claude-code>
- **Marketplace**: <https://github.com/marketplace/ecc-tools>

---

*Author: Bigger Lobster*
*Date: 2026-03-01*
*Tags: Claude Code / AI Agent / Performance / Codex / Continuous Learning / Security*
