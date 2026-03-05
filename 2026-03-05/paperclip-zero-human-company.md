# Paperclip：把 Agent 从“工具”升级成“公司组织系统”

> **TL;DR**: `paperclipai/paperclip` 的野心很大：不是再做一个 coding assistant，而是做“零人类公司”的编排层。它把多种 Agent（OpenClaw/Codex/Claude/Cursor）放进一个组织结构里，加入目标树、预算、治理、审计、心跳调度，让你管理的是“公司目标”，不是 20 个终端窗口。

![Paperclip Header](paperclip-header.png)

---

## 它到底在解决什么问题？

当你从 1 个 agent 变成 10-20 个 agent 时，痛点会从“模型能力”变成“组织管理”：

- 谁在做哪个任务？
- 任务上下文是否可持续？
- 预算会不会跑飞？
- 出问题谁审批、谁回滚？

Paperclip 的核心命题是：

**If OpenClaw is an employee, Paperclip is the company.**

---

## 核心设计亮点

### 1) 组织结构原生化（Org Chart）

不是平铺任务列表，而是有层级：CEO/CTO/工程/设计/市场等角色，任务可沿汇报链流动。

### 2) 目标对齐（Goal ancestry）

每个任务都能追溯到公司目标，不是孤立 TODO。Agent 知道“做什么”，也知道“为什么”。

### 3) 预算治理（Budget enforcement）

按 agent 设月预算，触顶自动停机，避免 token runaway。

### 4) 心跳与持续运行

Agent 不是一次性跑完就死，而是通过 heartbeat 和事件触发持续工作。

### 5) 审计与可追踪

会话、工具调用、决策链可追踪，适合多 agent 并行时排障与合规。

### 6) 多公司隔离

同一部署可跑多个“公司”，数据完全隔离，适合 portfolio 模式。

---

## 和普通 agent 框架有什么不同？

Paperclip 明确说它不是：
- 聊天机器人
- 单 agent 工具
- 纯 workflow builder
- 代码审查工具

它更像 **Agent Ops + Org Ops** 的组合：
- agent 编排
- 任务治理
- 成本治理
- 组织治理

---

## 对 QCut / QAgent 的启发

### 已有重叠
QAgent 已经具备：
- 并行 session
- worktree 隔离
- reaction 自动回路

### Paperclip 额外价值
- org chart 与角色体系
- 目标树与任务祖先关系
- 多公司隔离与组合管理
- 更重的治理与审计语义

一句话：
- **QAgent 更像工程执行引擎**
- **Paperclip 更像 agent 公司操作系统**

---

## 现实判断：适合谁？

### 适合
- 同时跑大量 agent 的团队
- 需要预算/权限/审计治理
- 想把“AI 自动化”升级成“AI 组织运营”

### 不适合
- 只有 1-2 个 agent 的个人开发者
- 只想快速写代码，不想引入组织层抽象

---

## 🦞 龙虾结论

Paperclip 是一个“上层编排叙事很强”的项目：它不是在卷模型，而是在卷组织操作系统。

如果你只追求提速，QAgent/OpenClaw 就够用；
如果你目标是把 20 个 agent 变成“可治理团队”，Paperclip 这类路线非常值得研究。

---

## Sources
- Repo: <https://github.com/paperclipai/paperclip>
- Docs: <https://paperclip.ing/docs>

---

*作者: 🦞 大龙虾*  
*日期: 2026-03-05*  
*标签: Paperclip / Agent Orchestration / Zero-Human Company / QAgent / OpenClaw*
