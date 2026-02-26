# Claude Code Memory System: How AI Finally Remembers You

> **TL;DR**: Claude Code now has two persistent memory systems: **Auto Memory** (Claude automatically records project patterns, debugging insights, and your preferences) + **CLAUDE.md files** (instructions and rules you write). Six-layer memory hierarchy from org-wide policies to per-project personal preferences, `@import` syntax for file references, `.claude/rules/` with path-scoped rules. All loaded automatically at session start, persists across sessions.

---

## 🧠 Two Memory Types

| Type | Written by | Content | Persistence |
|------|-----------|---------|-------------|
| **Auto Memory** | Claude itself | Project patterns, debugging insights, architecture notes, your preferences | ✅ Cross-session |
| **CLAUDE.md** | You (developer) | Instructions, rules, coding standards, common commands | ✅ Cross-session |

Both are loaded into Claude's context at the start of every session.

## 📂 Six-Layer Memory Hierarchy

From broadest to most specific (higher specificity = higher priority):

| Layer | Location | Purpose | Shared With |
|-------|----------|---------|-------------|
| **Managed policy** | OS-specific system path | Org-wide standards from IT/DevOps | Entire organization |
| **Project memory** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared project instructions | Team via Git |
| **Project rules** | `./.claude/rules/*.md` | Modular, topic-specific rules | Team via Git |
| **User memory** | `~/.claude/CLAUDE.md` | Personal preferences (all projects) | Just you |
| **Project local** | `./CLAUDE.local.md` | Personal project-specific prefs | Just you (auto-.gitignored) |
| **Auto memory** | `~/.claude/projects/<project>/memory/` | Claude's automatic notes | Just you (per-project) |

**Loading rules:**
- Walks up from cwd, reads all CLAUDE.md and CLAUDE.local.md files
- Child directory CLAUDE.md files load on-demand
- Auto Memory loads only the first 200 lines of MEMORY.md

## 🤖 Auto Memory Deep Dive

The most interesting new feature. Claude **automatically** records useful info as it works:

- **Project patterns** — build commands, test conventions, code style
- **Debugging insights** — solutions to tricky problems, common error causes
- **Architecture notes** — key files, module relationships, important abstractions
- **Your preferences** — communication style, workflow habits, tool choices

### Storage Structure

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Concise index, loaded every session
├── debugging.md       # Detailed debugging pattern notes
├── api-conventions.md # API design decisions
└── ...                # Any other topic files
```

**Key design decisions:**
- Only the first 200 lines of `MEMORY.md` are loaded — Claude keeps it concise by moving details into topic files
- Topic files are read on-demand, not at startup
- Per-project isolation via git repo root path

### Manually Trigger Memory

Just tell Claude directly:
- *"Remember that we use pnpm, not npm"*
- *"Save to memory that the API tests require a local Redis instance"*

### Toggle Controls

```json
// ~/.claude/settings.json — disable globally
{ "autoMemoryEnabled": false }

// .claude/settings.json — disable per-project
{ "autoMemoryEnabled": false }
```

Environment variable takes highest priority:
```bash
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1  # Force off
CLAUDE_CODE_DISABLE_AUTO_MEMORY=0  # Force on
```

## 📎 CLAUDE.md Imports

Reference other files using `@path` syntax:

```markdown
See @README for project overview and @package.json for available commands.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

- Relative and absolute paths supported
- Recursive imports up to 5 levels deep
- `@` inside code blocks is ignored
- First-time approval dialog for external imports

## 📐 Modular Rules: `.claude/rules/`

Split rules into focused files for large projects:

```
.claude/rules/
├── frontend/
│   ├── react.md
│   └── styles.md
├── backend/
│   ├── api.md
│   └── database.md
└── general.md
```

All `.md` files discovered recursively and auto-loaded.

### Path-Scoped Rules

Use YAML frontmatter to scope rules to specific files:

```markdown
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules
- All API endpoints must include input validation
- Use the standard error response format
```

Supports glob patterns and brace expansion: `src/**/*.{ts,tsx}`.
Rules without `paths` apply unconditionally.

### Symlinks & Cross-Project Sharing

```bash
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

Share rules across projects without copy-pasting.

## 🏢 Organization-Level Management

IT/DevOps can deploy centralized CLAUDE.md files via MDM, Group Policy, or Ansible — ensuring consistent coding standards and security policies across all developers.

## 💡 Best Practices

- **Be specific** — "Use 2-space indentation" beats "Format code properly"
- **Use structure** — One bullet per memory, group related items under headings
- **Review periodically** — Update memories as your project evolves
- **Use path-scoped rules sparingly** — Only when rules truly apply to specific file types
- **Keep rule files focused** — One topic per file

## 🔗 Resources

- **Official docs**: <https://code.claude.com/docs/en/memory>
- **Full docs index**: <https://code.claude.com/docs/llms.txt>

## 💭 Why This Matters

One of the biggest pain points with Claude Code was session amnesia — every new session, you'd repeat the same setup instructions. What build tool to use, how tests run, code style preferences.

With Auto Memory + layered CLAUDE.md, Claude Code can **actually remember you**. The six-layer hierarchy covers everything from "company-wide standards" to "my personal preferences in this one project." Path-scoped rules are particularly elegant — frontend and backend code automatically get different conventions.

For teams, `.claude/rules/` + Git version control = your AI coding standards are now code-reviewable.

---

*Author: 🦞 Bigger Lobster*
*Date: 2026-02-27*
*Tags: Claude Code / Memory System / Auto Memory / CLAUDE.md / Project Rules / Anthropic*
