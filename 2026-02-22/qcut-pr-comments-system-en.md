# QCut PR Comments System: Automated Extraction, Evaluation, and Batch-Fixing of PR Review Comments

> Source: [donghaozhang/qcut/.claude/skills/pr-comments](https://github.com/donghaozhang/qcut/tree/master/qcut/.claude/skills/pr-comments)
> Project: QCut Video Editor

---

## 1. Overview

When your PRs accumulate dozens of review comments from CodeRabbit, Gemini Code Assist, and other AI review tools, processing them one-by-one is tedious. The QCut team built a **custom Claude Code skill** that implements a complete pipeline:

```
Export PR comments → Preprocess into tasks → Analyze groupings → Fix individually/batch → Resolve threads → Commit & push
```

**Core Value:**
- 🔄 One-click export of all PR review comments as individual Markdown files
- 🧹 Auto-clean `<details>` noise, add evaluation instructions
- 📊 Group by source file, sort bottom-up (prevents line number shifts)
- 🤖 Agent auto-evaluates each comment: fix / not applicable / already fixed
- ✅ Auto-resolve GitHub threads + commit & push

---

## 2. Architecture

### Two Commands + One Skill

```
.claude/
├── commands/
│   ├── prit.md          # /prit — Export and preprocess current PR
│   └── prtaskit.md      # /prtaskit — Process all tasks: fix → resolve → commit
└── skills/
    └── pr-comments/
        ├── SKILL.md             # Skill entry point (7 actions)
        ├── review-fix.md        # Single comment evaluation guide
        ├── review-batch.md      # Batch processing guide
        └── scripts/
            ├── export.sh        # Export inline review comments
            ├── export-all.sh    # Export all comments (thread + review)
            ├── preprocess.sh    # Single file preprocessing
            ├── batch-preprocess.sh  # Batch preprocessing
            ├── analyze.sh       # Group-by-file analysis
            └── resolve-thread.sh    # Resolve GitHub threads
```

### Data Flow

```
GitHub PR
    │
    ▼ export.sh
docs/pr-comments/pr-102/          ← Raw comments (one .md each)
    │
    ▼ batch-preprocess.sh
docs/pr-comments/pr-102-tasks/    ← Preprocessed task files
    │
    ▼ analyze.sh
Grouped by file + line numbers descending
    │
    ▼ Agent evaluates + fixes
FIXED / NOT_APPLICABLE / ALREADY_FIXED
    │
    ▼ resolve-thread.sh
docs/pr-comments/pr-102-tasks_completed/  ← Completed tasks
    │
    ▼ git commit + push
```

---

## 3. Commands

### /prit — Export and Preprocess

```markdown
echo ".claude/skills/pr-comments/SKILL.md use this skill to export preprocess current pr"
```

When you type `/prit`, the agent will:
1. Detect the current branch's PR number
2. Call `export.sh` to export all review comments
3. Call `batch-preprocess.sh` to preprocess into task files
4. Call `analyze.sh` to show grouped analysis

### /prtaskit — Process All Tasks

```markdown
echo ".claude/skills/pr-comments/SKILL.md use this skill to process all tasks one by one, fix resolve git"
```

When you type `/prtaskit`, the agent will:
1. Read all `.md` files in the tasks directory
2. Group by file, sort by line number descending
3. Evaluate and fix each comment
4. Resolve GitHub threads
5. Commit and push code

---

## 4. The Seven Actions

| # | Action | Script | Description |
|---|--------|--------|-------------|
| 1 | **Export** | `export.sh` | Fetch PR inline comments via `gh api`, save as individual .md files |
| 2 | **Preprocess** | `batch-preprocess.sh` | Clean `<details>` blocks, add evaluation prompts |
| 3 | **Analyze** | `analyze.sh` | Group by source file, show bottom-up fix order |
| 4 | **Fix** | Agent + `review-fix.md` | Evaluate single comment: fix code or explain why N/A |
| 5 | **Batch** | Agent + `review-batch.md` | Process all tasks grouped by file, bottom-up |
| 6 | **Resolve** | `resolve-thread.sh` | GraphQL API to resolve PR thread, move to completed |
| 7 | **Git** | Agent (direct) | `git add` → `commit` → `push` modified source files |

---

## 5. The Bottom-Up Fix Strategy

This is the most clever design in the entire system:

```
File has 400 lines. Comments at lines 110, 253, 330.

❌ Top-down (WRONG):
  - Fix line 110 (adds 3 lines) → file now 403 lines
  - Fix line 253 → actually hits old line 250 (shifted!)
  - Fix line 330 → completely wrong location

✅ Bottom-up (CORRECT):
  - Fix line 330 first → lines above unchanged
  - Fix line 253 → lines above still correct
  - Fix line 110 → no problem
```

---

## 6. Evaluation Result Types

| Result | Meaning | Follow-up |
|--------|---------|-----------|
| **FIXED** | Comment valid, code fixed | Resolve thread → commit & push |
| **NOT_APPLICABLE** | Comment invalid or doesn't apply | Don't resolve (leave PR comment explaining) |
| **ALREADY_FIXED** | Issue already resolved | Resolve thread (no commit needed) |

---

## 7. Complete Source Code

### 7.1 scripts/export.sh

```bash
#!/bin/bash
# PR Comments Exporter
# Usage: ./export.sh owner/repo pr_number [output_dir]
set -e

REPO=${1:-""} PR=${2:-""} OUTPUT_DIR=${3:-"docs/pr-comments/pr-${PR}"}

# Validate, check gh + jq dependencies
# Fetch: gh api "repos/${REPO}/pulls/${PR}/comments"
# Loop: extract id, user, path, line, body, html_url
# Save each as: ${user}_${safe_path}_L${line}_${id}.md
```

### 7.2 scripts/export-all.sh

```bash
#!/bin/bash
# Exports BOTH thread comments AND inline review comments
# Thread comments: gh api repos/${REPO}/issues/${PR}/comments → thread/
# Review comments: gh api repos/${REPO}/pulls/${PR}/comments → review/
# Separate directories for different comment types
```

### 7.3 scripts/preprocess.sh

```bash
#!/bin/bash
# Preprocess single PR comment for agent evaluation
# - Extracts content before <details> block
# - Removes HTML comments
# - Adds task prompt with file path and line number
# - Output: ready-for-agent task file with instructions
```

### 7.4 scripts/batch-preprocess.sh

```bash
#!/bin/bash
# Runs preprocess.sh on all .md files in input directory
# Skips README.md
# Creates {input_dir}-tasks/ output directory
```

### 7.5 scripts/analyze.sh

```bash
#!/bin/bash
# Groups task files by source file
# Output table: | Source File | Lines (fix bottom-up) | Count |
# Lines sorted descending within each group
# Compatible with macOS bash 3 and Linux bash 4+
```

### 7.6 scripts/resolve-thread.sh

```bash
#!/bin/bash
# Uses GitHub GraphQL API to:
# 1. Query all review threads, find one containing comment ID
# 2. Check if already resolved
# 3. Mutation: resolveReviewThread(input: {threadId: "..."})
# 4. Move task file to _completed/ directory
```

### 7.7 review-fix.md

```markdown
# PR Review Evaluator & Fixer

1. Read task file → read source file → evaluate validity
2. FIXED: Fix code → resolve thread → commit & push
3. NOT_APPLICABLE: Explain in 2-3 sentences
4. ALREADY_FIXED: Resolve thread, skip commit

Output: Result, File, Line, Comment ID, Action, Thread status, Commit status
```

### 7.8 review-batch.md

```markdown
# Batch PR Review Processor

Critical: Group by source file, fix bottom-up (descending line numbers).
1. Group tasks by source file
2. Sort each group by line DESC
3. Read source file ONCE per group
4. Fix each comment bottom to top
5. Summary table + git commit all together
```

---

## 8. End-to-End Workflow

```bash
# Step 1: Export comments from PR
/pr-comments export donghaozhang/qcut 102

# Step 2: Preprocess into task files
/pr-comments preprocess docs/pr-comments/pr-102

# Step 3: Analyze (see file groupings and fix order)
/pr-comments analyze docs/pr-comments/pr-102-tasks

# Step 4a: Fix single comment
/pr-comments fix docs/pr-comments/pr-102-tasks/comment.md

# Step 4b: Or batch fix all
/pr-comments batch docs/pr-comments/pr-102-tasks

# Step 5: Resolve thread (auto-moves to completed)
/pr-comments resolve donghaozhang/qcut 102 2742327370 docs/pr-comments/pr-102-tasks/comment.md

# Step 6: Agent auto commits + pushes
```

---

## 9. Comparison with Anthropic's Official Plugins

| | Anthropic /code-review | Anthropic PR Review Toolkit | QCut PR Comments |
|---|---|---|---|
| **Purpose** | Preventive review | Preventive review | Post-hoc fixing |
| **Timing** | When PR is created | During development | After receiving comments |
| **Input** | Code diff | Code diff | Existing review comments |
| **Output** | New PR comments | Terminal reports | Fixed code + resolved threads |
| **Auto-fix** | ❌ Suggestions only | ❌ Suggestions only | ✅ Auto-fixes code |
| **Thread management** | ❌ | ❌ | ✅ Auto-resolves |
| **Git integration** | ❌ | ❌ | ✅ Auto commit + push |

**Complementary:** Anthropic's plugins **find issues** when creating PRs. QCut's system **fixes issues** after receiving review comments. Together they form a complete review cycle.

---

## 10. Summary

The QCut PR Comments system solves a very practical problem: **AI review tools generate many comments, manual processing is expensive.** Its design highlights:

1. **Complete pipeline** — From export to fix to commit, fully automated
2. **Bottom-up fixing** — Core design preventing line number shifts
3. **Three-state evaluation** — FIXED / NOT_APPLICABLE / ALREADY_FIXED
4. **Thread resolution** — GraphQL API auto-closes processed comments
5. **Shell scripts + Agent** — Scripts handle data, Agent handles intelligence

This isn't another "AI review" tool — it's an **"AI fixes AI review results"** tool.

---

*Based on the [donghaozhang/qcut](https://github.com/donghaozhang/qcut) repository's .claude/ directory.*
*Date: 2026-02-22*
