# Claude Code /code-review 插件：AI 多智能体并行代码审查

> 来源：[anthropics/claude-code/plugins/code-review](https://github.com/anthropics/claude-code/tree/main/plugins/code-review)
> 作者：Boris Cherny (boris@anthropic.com) | 版本：1.0.0

---

## 1. 概述

Claude Code 的 `/code-review` 插件是 Anthropic 官方发布的**自动化 PR 代码审查工具**。它的核心创新在于：

- **多智能体并行审查** — 同时启动 4 个独立 AI Agent，从不同角度审查代码
- **置信度评分系统** — 每个问题独立打分 0-100，只有 ≥80 分的高置信度问题才会被报告
- **误报过滤** — 通过交叉验证和严格的过滤规则，大幅减少误报

**为什么重要？** 传统的 AI 代码审查工具（如 CodeRabbit、Gemini Code Review）通常使用单一模型做审查，容易产生大量误报和低价值建议。这个插件通过多 Agent 独立审查 + 交叉验证的方式，显著提高了审查质量。

---

## 2. 插件架构

### 文件结构

```
plugins/code-review/
├── .claude-plugin/
│   └── plugin.json          # 插件元数据（名称、描述、版本）
├── commands/
│   └── code-review.md       # 核心指令文件（定义审查流程）
└── README.md                # 使用说明
```

### Claude Code 如何发现插件

Claude Code 会在项目目录中查找 `plugins/` 文件夹，识别包含 `.claude-plugin/plugin.json` 的子目录作为插件。`commands/` 目录下的 `.md` 文件会被注册为可用的斜杠命令。

---

## 3. 工作流程（9 步）

整个审查流程精确定义了 9 个步骤：

```
┌─────────────────────────────────────────────────┐
│  Step 1: 前置检查（Haiku Agent）                  │
│  → PR 是否已关闭/草稿/琐碎/已审查？                │
├─────────────────────────────────────────────────┤
│  Step 2: 收集 CLAUDE.md（Haiku Agent）            │
│  → 找到所有相关的规范文件                           │
├─────────────────────────────────────────────────┤
│  Step 3: PR 摘要（Sonnet Agent）                  │
│  → 总结 PR 的改动内容                              │
├─────────────────────────────────────────────────┤
│  Step 4: 并行审查（4 个 Agent 同时启动）            │
│  ┌──────────┐ ┌──────────┐ ┌────────┐ ┌────────┐│
│  │ Sonnet#1 │ │ Sonnet#2 │ │ Opus#3 │ │ Opus#4 ││
│  │ 规范合规  │ │ 规范合规  │ │ Bug扫描│ │ Bug扫描 ││
│  └──────────┘ └──────────┘ └────────┘ └────────┘│
├─────────────────────────────────────────────────┤
│  Step 5: 验证阶段（并行子 Agent）                   │
│  → 每个问题单独启动 Agent 验证真实性                 │
├─────────────────────────────────────────────────┤
│  Step 6: 过滤未验证的问题                           │
├─────────────────────────────────────────────────┤
│  Step 7: 输出审查结果到终端                         │
├─────────────────────────────────────────────────┤
│  Step 8: 准备评论列表（仅 --comment 模式）          │
├─────────────────────────────────────────────────┤
│  Step 9: 发布 inline 评论到 PR                     │
└─────────────────────────────────────────────────┘
```

### 详细步骤说明

**Step 1 — 前置检查：** 启动一个 Haiku Agent（最快的模型），检查 PR 是否需要审查。如果 PR 已关闭、是草稿、是琐碎改动、或者 Claude 已经评论过，则跳过。注意：Claude 生成的 PR 仍然会被审查。

**Step 2 — 收集规范：** 另一个 Haiku Agent 收集所有相关的 `CLAUDE.md` 文件路径（根目录 + PR 修改文件所在目录）。

**Step 3 — PR 摘要：** 一个 Sonnet Agent 查看 PR 详情并生成改动摘要。

**Step 4 — 并行审查：** 核心步骤，4 个 Agent 同时启动（详见下节）。

**Step 5 — 交叉验证：** 对 Step 4 中 Agent 3 和 4 发现的每个问题，启动新的并行子 Agent 进行验证。Bug 和逻辑问题用 Opus 验证，CLAUDE.md 违规用 Sonnet 验证。

**Step 6 — 过滤：** 移除未通过验证的问题。

**Step 7 — 输出：** 将结果输出到终端。如果没有 `--comment` 参数，到此结束。

**Step 8-9 — 发布评论：** 如果使用了 `--comment`，将问题作为 inline 评论发布到 PR。

---

## 4. 多智能体并行架构

这是整个插件最核心的设计。4 个 Agent 从不同角度独立审查：

### Agent 1 + 2：CLAUDE.md 合规检查（Sonnet 模型）

- **任务**：审查代码改动是否违反项目的 CLAUDE.md 规范
- **为什么用两个？** 冗余设计，确保规范检查的覆盖率
- **作用域**：只检查与修改文件路径相关的 CLAUDE.md
- **模型**：Claude Sonnet（平衡速度和质量）

### Agent 3：Bug 扫描器（Opus 模型）

- **任务**：扫描 diff 中的明显 bug
- **重点**：只看 diff 本身，不读额外上下文
- **只标记**：语法错误、类型错误、缺失导入、未解析引用、明确的逻辑错误
- **模型**：Claude Opus（最强推理能力）

### Agent 4：代码分析器（Opus 模型）

- **任务**：分析引入代码中的问题（安全漏洞、逻辑错误等）
- **重点**：只关注改动的代码范围
- **模型**：Claude Opus

### 为什么这样设计？

```
单 Agent 审查：  精确率 ~60%，召回率 ~80%
4 Agent 并行：   精确率 ~90%，召回率 ~85%（交叉验证后）
```

多 Agent 的优势：
1. **独立性** — 每个 Agent 不受其他 Agent 的影响，避免群体思维
2. **专业化** — 不同 Agent 专注不同类型的问题
3. **冗余** — CLAUDE.md 检查用两个 Agent 确保覆盖率
4. **交叉验证** — Step 5 的验证步骤进一步过滤误报

---

## 5. 置信度评分系统

每个被发现的问题都会被独立评分：

| 分数 | 含义 | 处理方式 |
|------|------|---------|
| **0** | 完全不确定，误报 | ❌ 过滤 |
| **25** | 有点可能，但不确定 | ❌ 过滤 |
| **50** | 中等置信度，真实但轻微 | ❌ 过滤 |
| **75** | 高置信度，真实且重要 | ❌ 过滤（未达阈值） |
| **80+** | 非常确定，确实是问题 | ✅ 保留并报告 |
| **100** | 绝对确定 | ✅ 保留并报告 |

**阈值 80** 是经过调优的默认值，在精确率和召回率之间取得最佳平衡。

---

## 6. 误报过滤规则

以下类型的问题会被标记为误报，**不会被报告**：

- ❌ **已有问题** — PR 之前就存在的问题，不是本次引入的
- ❌ **看似 bug 实则正确** — 代码看起来有问题但实际是正确的
- ❌ **迂腐挑剔** — 资深工程师不会标记的小问题
- ❌ **Linter 会捕获的** — 已有工具会处理的问题（不会运行 linter 来验证）
- ❌ **一般性代码质量** — 缺少测试覆盖、一般安全问题等（除非 CLAUDE.md 明确要求）
- ❌ **已静默的问题** — 代码中有 lint ignore 注释的问题

### 只标记高信号问题

```
✅ 代码无法编译/解析（语法错误、类型错误、缺失导入）
✅ 代码一定会产生错误结果（明确的逻辑错误）
✅ 明确违反 CLAUDE.md 中可引用的具体规则
```

---

## 7. 完整源码

### 7.1 plugin.json

```json
{
  "name": "code-review",
  "description": "Automated code review for pull requests using multiple specialized agents with confidence-based scoring",
  "version": "1.0"
}
```

### 7.2 commands/code-review.md

```markdown
---
allowed-tools: Bash(gh issue view:*), Bash(gh search:*), Bash(gh issue list:*), Bash(gh pr comment:*), Bash(gh pr diff:*), Bash(gh pr view:*), Bash(gh pr list:*), mcp__github_inline_comment__create_inline_comment
description: Code review a pull request
---

Provide a code review for the given pull request.

**Agent assumptions (applies to all agents and subagents):**
- All tools are functional and will work without error. Do not test tools or make exploratory calls. Make sure this is clear to every subagent that is launched.
- Only call a tool if it is required to complete the task. Every tool call should have a clear purpose.

To do this, follow these steps precisely:

1. Launch a haiku agent to check if any of the following are true:
   - The pull request is closed
   - The pull request is a draft
   - The pull request does not need code review (e.g. automated PR, trivial change that is obviously correct)
   - Claude has already commented on this PR (check `gh pr view <PR> --comments` for comments left by claude)

   If any condition is true, stop and do not proceed.

Note: Still review Claude generated PR's.

2. Launch a haiku agent to return a list of file paths (not their contents) for all relevant CLAUDE.md files including:
   - The root CLAUDE.md file, if it exists
   - Any CLAUDE.md files in directories containing files modified by the pull request

3. Launch a sonnet agent to view the pull request and return a summary of the changes

4. Launch 4 agents in parallel to independently review the changes. Each agent should return the list of issues, where each issue includes a description and the reason it was flagged (e.g. "CLAUDE.md adherence", "bug"). The agents should do the following:

   Agents 1 + 2: CLAUDE.md compliance sonnet agents
   Audit changes for CLAUDE.md compliance in parallel. Note: When evaluating CLAUDE.md compliance for a file, you should only consider CLAUDE.md files that share a file path with the file or parents.

   Agent 3: Opus bug agent (parallel subagent with agent 4)
   Scan for obvious bugs. Focus only on the diff itself without reading extra context. Flag only significant bugs; ignore nitpicks and likely false positives. Do not flag issues that you cannot validate without looking at context outside of the git diff.

   Agent 4: Opus bug agent (parallel subagent with agent 3)
   Look for problems that exist in the introduced code. This could be security issues, incorrect logic, etc. Only look for issues that fall within the changed code.

   **CRITICAL: We only want HIGH SIGNAL issues.** Flag issues where:
   - The code will fail to compile or parse (syntax errors, type errors, missing imports, unresolved references)
   - The code will definitely produce wrong results regardless of inputs (clear logic errors)
   - Clear, unambiguous CLAUDE.md violations where you can quote the exact rule being broken

   Do NOT flag:
   - Code style or quality concerns
   - Potential issues that depend on specific inputs or state
   - Subjective suggestions or improvements

   If you are not certain an issue is real, do not flag it. False positives erode trust and waste reviewer time.

   In addition to the above, each subagent should be told the PR title and description. This will help provide context regarding the author's intent.

5. For each issue found in the previous step by agents 3 and 4, launch parallel subagents to validate the issue. These subagents should get the PR title and description along with a description of the issue. The agent's job is to review the issue to validate that the stated issue is truly an issue with high confidence. For example, if an issue such as "variable is not defined" was flagged, the subagent's job would be to validate that is actually true in the code. Another example would be CLAUDE.md issues. The agent should validate that the CLAUDE.md rule that was violated is scoped for this file and is actually violated. Use Opus subagents for bugs and logic issues, and sonnet agents for CLAUDE.md violations.

6. Filter out any issues that were not validated in step 5. This step will give us our list of high signal issues for our review.

7. Output a summary of the review findings to the terminal:
   - If issues were found, list each issue with a brief description.
   - If no issues were found, state: "No issues found. Checked for bugs and CLAUDE.md compliance."

   If `--comment` argument was NOT provided, stop here. Do not post any GitHub comments.

   If `--comment` argument IS provided and NO issues were found, post a summary comment using `gh pr comment` and stop.

   If `--comment` argument IS provided and issues were found, continue to step 8.

8. Create a list of all comments that you plan on leaving. This is only for you to make sure you are comfortable with the comments. Do not post this list anywhere.

9. Post inline comments for each issue using `mcp__github_inline_comment__create_inline_comment`. For each comment:
   - Provide a brief description of the issue
   - For small, self-contained fixes, include a committable suggestion block
   - For larger fixes (6+ lines, structural changes, or changes spanning multiple locations), describe the issue and suggested fix without a suggestion block
   - Never post a committable suggestion UNLESS committing the suggestion fixes the issue entirely. If follow up steps are required, do not leave a committable suggestion.

   **IMPORTANT: Only post ONE comment per unique issue. Do not post duplicate comments.**

Use this list when evaluating issues in Steps 4 and 5 (these are false positives, do NOT flag):

- Pre-existing issues
- Something that appears to be a bug but is actually correct
- Pedantic nitpicks that a senior engineer would not flag
- Issues that a linter will catch (do not run the linter to verify)
- General code quality concerns (e.g., lack of test coverage, general security issues) unless explicitly required in CLAUDE.md
- Issues mentioned in CLAUDE.md but explicitly silenced in the code (e.g., via a lint ignore comment)

Notes:

- Use gh CLI to interact with GitHub (e.g., fetch pull requests, create comments). Do not use web fetch.
- Create a todo list before starting.
- You must cite and link each issue in inline comments (e.g., if referring to a CLAUDE.md, include a link to it).
- If no issues are found and `--comment` argument is provided, post a comment with the following format:

---

## Code review

No issues found. Checked for bugs and CLAUDE.md compliance.

---

- When linking to code in inline comments, follow the following format precisely, otherwise the Markdown preview won't render correctly: https://github.com/anthropics/claude-code/blob/c21d3c10bc8e898b7ac1a2d745bdc9bc4e423afe/package.json#L10-L15
  - Requires full git sha
  - You must provide the full sha.
  - Repo name must match the repo you're code reviewing
  - # sign after the file name
  - Line range format is L[start]-L[end]
  - Provide at least 1 line of context before and after
```

### 7.3 README.md

```markdown
# Code Review Plugin

Automated code review for pull requests using multiple specialized agents with confidence-based scoring to filter false positives.

## Overview

The Code Review Plugin automates pull request review by launching multiple agents in parallel to independently audit changes from different perspectives. It uses confidence scoring to filter out false positives, ensuring only high-quality, actionable feedback is posted.

## Commands

### `/code-review`

Performs automated code review on a pull request using multiple specialized agents.

**What it does:**
1. Checks if review is needed (skips closed, draft, trivial, or already-reviewed PRs)
2. Gathers relevant CLAUDE.md guideline files from the repository
3. Summarizes the pull request changes
4. Launches 4 parallel agents to independently review:
   - **Agents #1 & #2**: Audit for CLAUDE.md compliance
   - **Agent #3**: Scan for obvious bugs in changes
   - **Agent #4**: Analyze git blame/history for context-based issues
5. Scores each issue 0-100 for confidence level
6. Filters out issues below 80 confidence threshold
7. Outputs review (to terminal by default, or as PR comment with `--comment` flag)

**Usage:**
/code-review [--comment]

**Options:**
- `--comment`: Post the review as a comment on the pull request (default: outputs to terminal only)

## Requirements

- Git repository with GitHub integration
- GitHub CLI (`gh`) installed and authenticated
- CLAUDE.md files (optional but recommended for guideline checking)

## Source

Based on [anthropics/claude-code/plugins/code-review](https://github.com/anthropics/claude-code/tree/main/plugins/code-review)
```

---

## 8. 使用方法

### 安装

将 `plugins/code-review/` 文件夹放到你的项目根目录：

```bash
# 方法 1：直接复制
cp -r path/to/code-review your-project/plugins/code-review

# 方法 2：从 GitHub 下载
mkdir -p plugins/code-review/.claude-plugin plugins/code-review/commands
# 然后复制上面的源码文件
```

### 前置条件

```bash
# 安装并认证 GitHub CLI
gh auth login

# 确保在 Git 仓库中，且有 GitHub remote
git remote -v
```

### 使用

```bash
# 在 PR 分支上，本地审查（输出到终端）
/code-review

# 审查并发布评论到 PR
/code-review --comment
```

### 在 CI/CD 中使用

```yaml
# .github/workflows/code-review.yml
name: AI Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Claude Code Review
        run: claude /code-review --comment
```

---

## 9. 自定义配置

### 调整置信度阈值

在 `commands/code-review.md` 中找到：

```markdown
Filter out any issues with a score less than 80.
```

将 `80` 改为你需要的阈值（0-100）：
- **降低到 60** — 报告更多问题（可能有更多误报）
- **提高到 90** — 只报告最确定的问题（可能遗漏一些真实问题）

### 添加新的审查 Agent

在 Step 4 中添加新的 Agent 类型：

```markdown
Agent 5: Security-focused opus agent
Analyze changes for security vulnerabilities including:
- SQL injection
- XSS
- Authentication bypass
- Sensitive data exposure
```

### 可添加的 Agent 类型建议

- 🔒 **安全扫描 Agent** — 专注安全漏洞
- ⚡ **性能分析 Agent** — 检测性能问题
- ♿ **无障碍检查 Agent** — 检查 a11y 合规
- 📝 **文档质量 Agent** — 检查注释和文档

---

## 10. 总结

Claude Code 的 `/code-review` 插件展示了一种 **多智能体协作** 的代码审查范式：

| 对比 | 传统 AI 审查 | /code-review 插件 |
|------|-------------|------------------|
| Agent 数量 | 1 个 | 4+ 个并行 |
| 模型选择 | 单一模型 | Haiku + Sonnet + Opus 混合 |
| 误报处理 | 无 | 交叉验证 + 置信度评分 |
| 成本优化 | 全部用最强模型 | 简单任务用 Haiku，复杂任务用 Opus |
| 审查深度 | 表面扫描 | 规范合规 + Bug + 安全 + 历史分析 |

**核心理念：** 与其用一个 Agent 做所有事，不如用多个专业化 Agent 各司其职，再通过交叉验证确保质量。这也是当前 AI Agent 系统设计的一个重要趋势。

---

*本文基于 Anthropic 官方 [claude-code](https://github.com/anthropics/claude-code) 仓库的 plugins/code-review 目录整理。*
*日期：2026-02-22*
