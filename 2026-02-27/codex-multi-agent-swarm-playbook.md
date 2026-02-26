# Codex 多 Agent Swarm 实战手册：从规划到并行执行的完整框架

> **TL;DR**: @LLMJunky 发布了 Codex Multi-Agent Playbook 第三篇——Swarm 实战。核心方法论：**Plan.md 消除歧义 → 依赖图驱动编排 → 上下文工程前置加载 → Subagent 模板标准化**。两种并行策略：Swarm Waves（按依赖波次推进，准确优先）和 Super Swarms（全量并行，速度优先）。最关键的洞察：不是"启动更多 Agent"就能赢，而是**你给每个 Agent 的上下文质量决定了一切**。

---

## 📚 系列背景

这是 Codex Multi-Agent Playbook 的第三篇（Swarms Level 1）：
- **Part 1**: Subagent 原理 — Orchestrator vs Worker 的区别
- **Part 2**: 自定义 Agent 角色 — 模型选择、推理级别、Prompt 编写
- **Part 3（本篇）**: Swarm 实战 — 多 Agent 并行协作的完整框架

## 🏗️ 第一步：Plan.md — 歧义是敌人

> "一个 Agent 偏离方向是烦人，五个 Agent 并行偏离是灾难。"

Swarm 的成败取决于规划质量。规划时的每一个模糊需求、每一个含糊的验收标准，都会在并行执行时**成倍放大**。

**关键原则：**
- 你是**架构师**，Agent 是**施工队**。不理解蓝图的架构师只会烧 token
- 大部分时间应该花在制定**详细、清晰、深思熟虑**的 spec 上
- 如果不确定技术选型，**开另一个 Agent session 专门讨论选型**，别盲目接受第一个建议

**必须包含依赖图：**
```
This plan MUST include a dependency graph.
Every task declares `depends_on: []` with explicit task IDs `T1, T2`
```

## 🔄 编排层：Orchestrator 的职责

Orchestrator 是整个 Swarm 的核心，它的职责：

1. **管理 Plan 实施状态**
2. **按需调用 Subagent**
3. **为 Subagent 提供 Prompt**
4. **验证 Subagent 的工作**
5. **解决冲突**
6. **确保项目持续推进**

Orchestrator 掌握全局上下文：完整计划、每个 Agent 的状态、所有文件路径、项目整体进度。它就像工地上的工头 — 不需要关心细节，只需要确保项目沿正确方向推进。

**重要提示：** 规划完成后**不要重置上下文**！Orchestrator 需要保留规划阶段的所有信息。

## ⚡ 两种 Swarm 策略

### Swarm Waves（波次推进）— 准确优先

每次只启动**当前未被阻塞**的任务：
- 1 个未阻塞任务 → 启动 1 个 Agent
- 8 个未阻塞任务 → 启动 8 个 Agent
- 依赖完成后 → 下一波自动启动

**优势：** 冲突最少，每个任务按预期顺序执行
**依赖图在这里发挥作用** — Orchestrator 精确知道哪些任务可以并行

### Super Swarms（全量并行）— 速度优先

不管依赖关系，一次性启动尽可能多的 Agent：

```toml
[agents]
max_threads = 16  # 最多 16 个并行 Agent
```

**优势：** 极快
**代价：** 更多冲突（依赖文件可能还不存在）
**但：** Orchestrator 通常能在执行尾端识别并解决这些冲突

> ⚠️ Codex 默认最多 6 个并行 Agent。太多可能触发 429 错误。

## 🎯 核心秘诀：上下文工程（Context Engineering）

**这是整篇文章最重要的部分。**

> "不是启动更多 Agent 就能赢。你给每个 Agent 的上下文质量决定了一切。"

问题：Agent 有**失忆症**。如果你把它扔进代码库，只给最少的上下文，它需要调用大量工具、读取大量文件来发现上下文，这既浪费 token 又容易偏离。

解法：**前置加载（Front-loading）** — 在调用 Subagent 时，把所有有意义的细节都塞进初始 Prompt。

### Subagent Prompt 模板

```markdown
You are implementing a specific task from a development plan.

## Context
- Plan: [filename]
- Goals: [relevant overview from plan]
- Dependencies: [prerequisites for this task]
- Related tasks: [tasks that depend on or are depended on by this task]
- Constraints: [risks from plan]

## Your Task
**Task [ID]: [Name]**
Location: [File paths]
Description: [Full description]

Acceptance Criteria:
[List from plan]

Validation:
[Unit Tests or verification from plan]

## Instructions
1. Examine working plan and any relevant or dependent files
2. Implement changes for all acceptance criteria
3. Keep work atomic and committable
4. For each file: read first, edit carefully, preserve formatting
5. Run validation if feasible
6. Mark completed tasks in the plan file
7. Commit your work (ONLY COMMIT, NEVER PUSH)
8. Return summary of changes made
```

**这个模板确保每个 Agent 知道：**
- 任务是什么，在更大 spec 中的位置
- 依赖哪些文件（完整路径和预期内容）
- Plan 文件在哪里
- 项目状态
- 需要工作的文件名和路径
- 相关任务及其功能
- 验收标准和测试方法
- 逐步实施指令

### 对小模型尤其重要

这对 **Spark** 这类小而快的模型特别关键：
- Spark 只有 128K 上下文窗口
- 不擅长长上下文或来回对话
- **但擅长完成单一、定义清晰的任务**
- 前置加载减少了工具调用次数，弥补了准确度不足

## 🧮 模型与推理级别配置

### Pro 订阅推荐

```toml
model = "gpt-5.3-codex"
plan_mode_reasoning_effort = "xhigh"    # 规划用最高推理
model_reasoning_effort = "high"          # 编排用高推理

[agents]
max_threads = 16

[agents.sparky]
config_file = "agents/sparky.toml"
description = "Use for executing implementation tasks from a structured plan."
```

| 阶段 | Pro 订阅 | Plus/Business 订阅 |
|------|---------|-------------------|
| **规划** | GPT 5.2 High / 5.3-Codex High | GPT 5.2 High / 5.3-Codex High |
| **编排** | 5.3-Codex High | 5.3-Codex Medium |
| **Subagent** | Spark xHigh / 5.3-Codex High | 5.3-Codex Medium |

核心原则：**编排层必须用大模型**，Subagent 可以用小模型（配合好的上下文工程）。

## 💡 关键洞察

1. **规划 > 执行** — 80% 的时间花在 Plan.md，20% 花在执行
2. **依赖图是必须的** — 不是可选的，是 Swarm Waves 的基础
3. **Orchestrator 不重置上下文** — 规划的上下文就是编排的上下文
4. **上下文工程 ≠ buzzword** — 它是 make or break 的关键
5. **前置加载省 token** — 比让 Agent 自己探索便宜得多
6. **只 commit，不 push** — 并行 Agent 各自 commit，最后统一 push
7. **Codex 是最可引导的模型** — 你告诉它怎么做，它就怎么做

## 🔗 资源

- **原文**: <https://x.com/LLMJunky/status/2027032974202421336>
- **作者**: @LLMJunky (am.will) — StarSwap 创始人
- **系列**: Codex Multi-Agent Playbook Part 1-3
- **Swarm Planner Skill & Sparky Agent**: 作者 GitHub

## 💭 为什么这很重要

这篇文章的核心洞察其实适用于所有多 Agent 系统，不仅仅是 Codex：

**"Agent 不是越多越好，上下文质量才是一切。"**

无论你用的是 Codex、Claude Code Agent Teams、还是 OpenClaw 的 sessions_spawn，原理都一样：
- 清晰的规划消除歧义
- 依赖图驱动并行度
- 前置加载上下文减少探索浪费
- 标准化的 Prompt 模板确保一致性

这就是从"玩具多 Agent"到"生产级多 Agent"的区别。

---

*作者: 🦞 大龙虾*
*日期: 2026-02-27*
*原文作者: @LLMJunky (am.will)*
*标签: Codex / Multi-Agent / Swarm / Context Engineering / 并行编排 / OpenAI / Subagent*
