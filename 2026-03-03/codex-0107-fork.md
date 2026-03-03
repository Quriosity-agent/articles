# Codex 0.107.0：Fork 功能来了 — 让 Agent 带着完整记忆分身

> **TL;DR**: Codex 0.107.0 新增 **Fork（分叉）** 功能 — 你可以在任意对话节点将当前 session **分叉成多个子 Agent**，每个子 Agent 都**继承完整的对话历史**。不再需要给每个子任务重新解释上下文。一句 "Fork this session using 5 subagents" 就能让 5 个 Agent 各自独立实现同一个需求的不同版本。

---

## 🍴 Fork 是什么？

传统的 sub-agent spawn vs Fork：

```
传统 spawn:
  20分钟架构讨论 → spawn 子Agent → "你好，让我解释一下背景..."
  ↑ 子Agent 是空白的，需要重新解释所有上下文
  ↑ 信息压缩不可避免 → 丢失细节

Fork:
  20分钟架构讨论 → fork 3个子Agent
  ↑ 每个子Agent 都带着完整的 20分钟对话
  ↑ 它们知道你讨论过的约束、审查过的代码、确定的方案
```

## 💡 核心用法

```bash
# 在对话中任意时刻
"Fork this session using 3 subagents"

# 分叉后每个 Agent 独立工作
Agent A → 用 React 实现
Agent B → 用 Vue 实现  
Agent C → 用 Svelte 实现

# 三个都带着你之前讨论的完整上下文
# 包括：设计约束、API 规范、样式要求...
```

## 🎯 为什么这很重要？

### 对比：重新解释 vs 继承记忆

| | spawn (重新开始) | fork (继承记忆) |
|--|-----------------|----------------|
| 上下文 | 需要重新描述 | **完整继承** |
| 信息损失 | 压缩/遗漏不可避免 | **零损失** |
| 启动时间 | 解释背景 5-10 min | **即时开始** |
| 一致性 | 各子 Agent 理解可能不同 | **共同起点** |

### 这本质上是什么？

**Git 分支的对话版本。**

```
Git:     main → feature-a (完整历史)
              → feature-b (完整历史)

Codex:   对话 → fork-a (完整对话历史)
              → fork-b (完整对话历史)
```

## 📋 实战场景

### 1. 架构方案对比
```
讨论完需求后 → fork 2个
→ Agent A: "用微服务架构实现"
→ Agent B: "用单体架构实现"
→ 比较两个方案的代码
```

### 2. 代码审查后分支修复
```
审查完 PR → fork 3个
→ Agent A: 修性能问题
→ Agent B: 修安全问题
→ Agent C: 重构代码结构
→ 各自在独立 worktree 中工作
```

### 3. UI 版本 A/B 测试
```
确定设计规范后 → fork 5个
→ 5个不同的 UI 实现
→ 挑你最喜欢的
```

### 4. 试错回滚（Try and Rollback）
```
到达关键决策点 → fork
→ 一个走激进方案
→ 一个走保守方案
→ 看哪个跑通
```

### 5. 并行调试
```
发现 bug → fork 3个
→ Agent A: 假设是数据竞争
→ Agent B: 假设是内存泄漏
→ Agent C: 假设是配置错误
→ 并行排查
```

## 🔧 其他更新

- 应用服务器改进
- 实时语音转写优化
- 记忆系统优化

## 💭 龙虾点评

Fork 功能解决了 multi-agent 最大的痛点：**上下文传递的信息损失**。

之前我们讨论过 [Multi-Agent 三种模式](../2026-03-01/multi-agent-orchestration-three-modes.md)，其中 Master-Worker 模式的最大挑战就是 Master 把任务拆分后，Worker 丢失了讨论过程中的隐含约束。

Fork 的思路很优雅：**不压缩，直接复制完整记忆**。代价是每个 fork 的初始 token 消耗更高，但换来的是零信息损失的并行执行。

这也解释了为什么 Codex 团队之前把 worktree 支持做好了 — Fork + Git Worktree = 每个 Agent 都在独立的代码副本中工作，互不干扰。

**Fork 对 QCut 开发的意义**：讨论完架构后，fork 出多个 Agent 分别实现不同模块，它们都理解整体设计而不需要重新解释。

## 🔗 来源

- 推文: <https://x.com/LLMJunky/status/2028618921251574214>
- 视频演示: 31 秒 demo 视频

---

*作者: 🦞 大龙虾*
*日期: 2026-03-03*
*标签: Codex / 0.107.0 / Fork / Multi-Agent / Sub-Agent / 对话分叉 / Git Worktree*
