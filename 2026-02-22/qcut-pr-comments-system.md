# QCut PR Comments 系统：自动化提取、评估和批量修复 PR Review 评论

> 来源：[donghaozhang/qcut/.claude/skills/pr-comments](https://github.com/donghaozhang/qcut/tree/master/qcut/.claude/skills/pr-comments)
> 项目：QCut Video Editor

---

## 1. 概述

当你的 PR 收到大量来自 CodeRabbit、Gemini Code Assist 等 AI 审查工具的评论时，逐条处理非常耗时。QCut 团队构建了一套 **Claude Code 自定义技能**，实现了完整的流水线：

```
导出 PR 评论 → 预处理为任务 → 分析分组 → 逐个/批量修复 → 解决线程 → 提交推送
```

**核心价值：**
- 🔄 一键导出 PR 所有 review 评论为独立 Markdown 文件
- 🧹 自动清理 `<details>` 等噪音，添加评估指令
- 📊 按源文件分组，自底向上排序（避免行号偏移）
- 🤖 Agent 自动评估每条评论：修复/不适用/已修复
- ✅ 自动解决 GitHub 线程 + 提交推送

---

## 2. 架构

### 两个命令 + 一个技能

```
.claude/
├── commands/
│   ├── prit.md          # /prit — 导出并预处理当前 PR
│   └── prtaskit.md      # /prtaskit — 逐个处理任务，修复→解决→提交
└── skills/
    └── pr-comments/
        ├── SKILL.md             # 技能入口（7 个 action）
        ├── review-fix.md        # 单条评论评估指南
        ├── review-batch.md      # 批量处理指南
        └── scripts/
            ├── export.sh        # 导出 inline review 评论
            ├── export-all.sh    # 导出所有评论（线程+review）
            ├── preprocess.sh    # 单文件预处理
            ├── batch-preprocess.sh  # 批量预处理
            ├── analyze.sh       # 按文件分组分析
            └── resolve-thread.sh    # 解决 GitHub 线程
```

### 数据流

```
GitHub PR
    │
    ▼ export.sh
docs/pr-comments/pr-102/          ← 原始评论（每条一个 .md）
    │
    ▼ batch-preprocess.sh
docs/pr-comments/pr-102-tasks/    ← 预处理后的任务文件
    │
    ▼ analyze.sh
按文件分组 + 行号降序排列
    │
    ▼ Agent 评估 + 修复
FIXED / NOT_APPLICABLE / ALREADY_FIXED
    │
    ▼ resolve-thread.sh
docs/pr-comments/pr-102-tasks_completed/  ← 已完成的任务
    │
    ▼ git commit + push
```

---

## 3. 命令详解

### /prit — 导出并预处理

```markdown
# prit.md
echo ".claude/skills/pr-comments/SKILL.md use this skill to export preprocess current pr"
```

输入 `/prit` 后，Agent 会：
1. 检测当前分支的 PR 编号
2. 调用 `export.sh` 导出所有 review 评论
3. 调用 `batch-preprocess.sh` 预处理为任务文件
4. 调用 `analyze.sh` 显示分组分析

### /prtaskit — 逐个处理任务

```markdown
# prtaskit.md
echo ".claude/skills/pr-comments/SKILL.md use this skill to process all tasks one by one, fix resolve git"
```

输入 `/prtaskit` 后，Agent 会：
1. 读取任务目录中的所有 `.md` 文件
2. 按文件分组，行号降序排列
3. 逐个评估并修复
4. 解决 GitHub 线程
5. 提交并推送代码

---

## 4. 技能的 7 个 Action

### Action 1: Export
```bash
bash .claude/skills/pr-comments/scripts/export.sh donghaozhang/qcut 102
```
通过 `gh api` 获取 PR 的所有 inline review 评论，每条保存为独立 Markdown 文件。

### Action 2: Preprocess
```bash
bash .claude/skills/pr-comments/scripts/batch-preprocess.sh docs/pr-comments/pr-102
```
清理原始评论（移除 `<details>` 块、HTML 注释），添加评估指令模板。

### Action 3: Analyze
```bash
bash .claude/skills/pr-comments/scripts/analyze.sh docs/pr-comments/pr-102-tasks
```
输出按源文件分组的表格，行号降序排列，告诉你处理顺序。

### Action 4: Fix（单条）
Agent 读取任务文件 → 读取源文件 → 评估 → 修复或解释。

### Action 5: Batch（批量）
**关键设计：自底向上修复。** 同一文件的多条评论，从最大行号开始修复，避免行号偏移。

### Action 6: Resolve
```bash
bash .claude/skills/pr-comments/scripts/resolve-thread.sh donghaozhang/qcut 102 2742327370
```
通过 GraphQL API 解决 PR review 线程，并将任务文件移到 `_completed` 目录。

### Action 7: Git
Agent 自动 `git add` → `commit` → `push`，只提交修改的源文件（不提交任务文件）。

---

## 5. 自底向上修复的关键

这是整个系统最巧妙的设计：

```
文件有 400 行。评论在 110、253、330 行。

❌ 自顶向下（错误）：
  - 修复第 110 行（增加 3 行）→ 文件变 403 行
  - 修复第 253 行 → 实际命中旧的第 250 行（偏移了！）
  - 修复第 330 行 → 完全错误的位置

✅ 自底向上（正确）：
  - 先修复第 330 行 → 上面的行不受影响
  - 再修复第 253 行 → 上面的行仍然正确
  - 最后修复第 110 行 → 没问题
```

---

## 6. 评估结果类型

| 结果 | 含义 | 后续动作 |
|------|------|---------|
| **FIXED** | 评论有效，已修复代码 | 解决线程 → 提交推送 |
| **NOT_APPLICABLE** | 评论无效或不适用 | 不解决（留 PR 评论解释） |
| **ALREADY_FIXED** | 问题已被修复 | 解决线程（不提交） |

---

## 7. 完整源码

### 7.1 commands/prit.md

```markdown
# Create a project command
echo ".claude/skills/pr-comments/SKILL.md use this skill to export preprocess current pr"
```

### 7.2 commands/prtaskit.md

```markdown
# Create a project command
echo ".claude/skills/pr-comments/SKILL.md use this skill to process all tasks one by one, fix resolve git"
```

### 7.3 skills/pr-comments/SKILL.md

```markdown
---
name: pr-comments
description: Export, preprocess, and fix GitHub PR review comments.
argument-hint: <action> [args...]
disable-model-invocation: true
allowed-tools: Bash(gh *), Bash(jq *), Bash(mkdir *), Bash(sed *), Bash(git *), Read, Edit, Glob, Grep
---

7 actions: export, preprocess, analyze, fix, batch, resolve, git
Complete workflow from export → preprocess → analyze → fix → resolve → commit
```

### 7.4 review-fix.md

```markdown
# PR Review Evaluator & Fixer

1. Read task file (contains file path, line number, issue description, comment ID)
2. Read the source file
3. Evaluate if feedback is valid
4. If valid: Fix code → Resolve thread → Commit and push
5. If invalid: Explain in 2-3 sentences

Output format:
## Result: [FIXED | NOT_APPLICABLE | ALREADY_FIXED]
**File:** path/to/file.ts
**Line:** 123
**Comment ID:** 2742327370
**Action taken:** [Description]
**Thread resolved:** [Yes | No | N/A]
**Committed:** [Yes (hash) | No]
```

### 7.5 review-batch.md

```markdown
# Batch PR Review Processor

Critical: Group by source file, process bottom-up.

1. List all .md task files
2. Group by source file
3. For each file: sort by line DESC, read once, fix each comment
4. Summary table with results
5. git commit + push all fixed files together
```

### 7.6 scripts/export.sh

```bash
#!/bin/bash
# Usage: ./export.sh owner/repo pr_number [output_dir]
set -e
REPO=${1:-""} PR=${2:-""} OUTPUT_DIR=${3:-"docs/pr-comments/pr-${PR}"}

# Fetch via gh api repos/${REPO}/pulls/${PR}/comments
# Loop through each comment, extract: id, user, path, line, body, html_url
# Save each as individual markdown file
# Filename: ${user}_${safe_path}_L${line}_${id}.md
```

### 7.7 scripts/export-all.sh

```bash
#!/bin/bash
# Exports BOTH thread comments AND inline review comments
# Thread: gh api repos/${REPO}/issues/${PR}/comments → thread/
# Review: gh api repos/${REPO}/pulls/${PR}/comments → review/
```

### 7.8 scripts/preprocess.sh

```bash
#!/bin/bash
# Cleans comment: removes <details> blocks, HTML comments
# Adds evaluation task prompt with file path and line number
# Output: ready-for-agent task file
```

### 7.9 scripts/batch-preprocess.sh

```bash
#!/bin/bash
# Runs preprocess.sh on all .md files in input directory
# Skips README.md
# Output: {input_dir}-tasks/ directory
```

### 7.10 scripts/analyze.sh

```bash
#!/bin/bash
# Groups task files by source file
# Outputs table: | Source File | Lines (fix bottom-up) | Count |
# Lines sorted descending within each group
# Compatible with macOS bash 3 and Linux bash 4+
```

### 7.11 scripts/resolve-thread.sh

```bash
#!/bin/bash
# Uses GitHub GraphQL API to:
# 1. Find the review thread containing the comment ID
# 2. Resolve the thread (mutation resolveReviewThread)
# 3. Move task file to _completed/ directory
```

---

## 8. 端到端工作流

```bash
# 1. 导出 PR 评论
/pr-comments export donghaozhang/qcut 102

# 2. 预处理为任务文件
/pr-comments preprocess docs/pr-comments/pr-102

# 3. 分析分组（查看哪些文件有多条评论）
/pr-comments analyze docs/pr-comments/pr-102-tasks

# 4a. 修复单条
/pr-comments fix docs/pr-comments/pr-102-tasks/comment.md

# 4b. 或批量修复
/pr-comments batch docs/pr-comments/pr-102-tasks

# 5. 解决线程（自动移到 completed）
/pr-comments resolve donghaozhang/qcut 102 2742327370 docs/pr-comments/pr-102-tasks/comment.md

# 6. Agent 自动 commit + push
```

---

## 9. 与 Anthropic 官方插件的对比

| | Anthropic /code-review | Anthropic PR Review Toolkit | QCut PR Comments |
|---|---|---|---|
| **定位** | 预防性审查 | 预防性审查 | 事后修复 |
| **时机** | PR 创建时 | 开发过程中 | PR 收到评论后 |
| **输入** | 代码 diff | 代码 diff | 已有的 review 评论 |
| **输出** | 新的 PR 评论 | 终端报告 | 修复代码 + 解决线程 |
| **自动修复** | ❌ 只提建议 | ❌ 只提建议 | ✅ 自动修复代码 |
| **线程管理** | ❌ | ❌ | ✅ 自动解决 |
| **Git 集成** | ❌ | ❌ | ✅ 自动 commit + push |

**互补关系：** Anthropic 的插件在 PR 创建时**找问题**，QCut 的系统在收到评论后**修问题**。

---

## 10. 总结

QCut PR Comments 系统解决的是一个非常实际的问题：**AI 审查工具产生大量评论，人工处理成本高。** 它的设计精妙在于：

1. **完整流水线** — 从导出到修复到提交，全链路自动化
2. **自底向上** — 避免行号偏移的核心设计
3. **三态评估** — FIXED / NOT_APPLICABLE / ALREADY_FIXED
4. **线程解决** — GraphQL API 自动关闭已处理的评论
5. **Shell 脚本 + Agent** — 脚本做数据处理，Agent 做智能判断

这不是另一个"AI 审查"工具——而是一个 **"AI 修复 AI 审查结果"** 的工具。

---

*本文基于 [donghaozhang/qcut](https://github.com/donghaozhang/qcut) 仓库的 .claude/ 目录整理。*
*日期：2026-02-22*
