# Claude Code 构建手记：像 Agent 一样思考

> **TL;DR**: Anthropic 的 Thariq（Claude Code 核心开发者）分享了构建 Claude Code 工具系统的实战经验。核心洞察：**设计 Agent 工具不是科学，是艺术** — 你需要"像 Agent 一样看世界"。文章揭秘了 AskUserQuestion、Todo→Task 演进、搜索从 RAG 到 Grep 的转变、渐进式信息披露等关键设计决策背后的思考过程。

---

## 🎯 核心框架：工具要匹配 Agent 的能力

Thariq 用了一个精妙的比喻：想象你要解一道数学难题，你想要什么工具？

| 工具 | 能力 | 限制 |
|------|------|------|
| 纸 | 最低门槛 | 手动计算慢 |
| 计算器 | 更快 | 要会操作高级功能 |
| 电脑 | 最强 | 要会写代码 |

**关键：工具要匹配使用者的能力，而不是越多越好。** 怎么知道 Agent 的能力边界？**观察它的输出、实验、学会"像 Agent 一样看"。**

## 🔧 案例 1：AskUserQuestion — 三次迭代

目标：提升 Claude 的"提问"能力（elicitation），降低用户回答的摩擦。

### 尝试 1：在 ExitPlanTool 里加问题数组
- 在计划工具里塞一个问题列表
- ❌ **失败**：混淆了 Claude — 同时要输出计划和关于计划的问题，如果用户的回答和计划矛盾怎么办？

### 尝试 2：修改输出格式
- 让 Claude 用特殊 markdown 格式输出问题（带选项的 bullet list）
- ❌ **失败**：Claude 有时能做到，但不保证 — 会多加句子、漏掉选项、换格式

### 尝试 3：专用 AskUserQuestion Tool ✅
- 独立工具，Claude 随时可以调用
- 触发后弹出 modal 显示问题，阻塞 agent 循环等用户回答
- ✅ **成功**：结构化输出 + 多选项 + 可组合（Agent SDK、Skills 都能用）
- **最重要的发现：Claude 喜欢调用这个工具，输出质量高**

> **"即使设计得再好的工具，如果模型不理解怎么调用，也没用。"**

## 📋 案例 2：Todo → Task 的演进

### 早期：TodoWrite
- Claude 需要 Todo 列表保持专注
- 还需要**每 5 轮系统提醒**才不会忘记目标
- 对当时的模型能力是够用的

### 现在：Task Tool
- 模型变强后，不需要被提醒了 — 提醒反而**限制**了它（觉得必须死板执行 Todo）
- Opus 4.5 的 sub-agent 能力大幅提升，但 Todo 无法跨 agent 协作
- Task Tool 支持：**依赖关系、跨 sub-agent 共享更新、可修改/删除**

> **"随着模型能力提升，曾经需要的工具可能变成约束。要不断重新审视工具的必要性。"**

## 🔍 案例 3：搜索工具的演进

| 阶段 | 方式 | 问题 |
|------|------|------|
| V1 | RAG 向量数据库 | 需要索引和配置；脆弱；**上下文是给的不是找的** |
| V2 | Grep 工具 | Claude 自己搜索代码库；自己构建上下文 |
| V3 | Agent Skills + 渐进式披露 | 读 skill 文件 → 文件引用其他文件 → 递归发现 |

**核心洞察：Claude 从"不会构建自己的上下文"进化到"能跨多层文件嵌套搜索精确找到需要的信息"。**

渐进式披露（Progressive Disclosure）成为加功能不加工具的核心手段。

## 📚 案例 4：Claude Code Guide — 不加工具加能力

问题：Claude 不了解 Claude Code 自己（MCP 怎么加、slash command 是什么）。

| 方案 | 结果 |
|------|------|
| 放进 system prompt | ❌ 大多数用户不问这个，白白增加 context rot |
| 给 Claude docs 链接让它自己搜 | 🟡 能用但加载太多结果到上下文 |
| **Claude Code Guide sub-agent** | ✅ 专门的 sub-agent，有详细的搜索指令，只返回答案 |

**Claude Code 目前有 ~20 个工具，每加一个工具的门槛都很高** — 因为多一个选项就多一份模型的思考负担。

## 💡 关键设计原则

1. **工具匹配能力** — 不是给最多工具，而是给最适合的工具
2. **观察模型行为** — 设计工具前先看 Claude 怎么用现有工具
3. **随模型进化更新** — 旧工具可能变成新约束
4. **渐进式披露 > 加工具** — 能通过文件链接解决的不要新建工具
5. **结构化 > 自由格式** — Tool Call 比纯文本输出更可靠
6. **少即是多** — ~20 个工具，每个新增都要过高门槛

## 💭 为什么这很重要

这篇文章的价值不在于具体的工具设计，而在于**思维方式**：

- **不是"给 Agent 最多的工具"，而是"给它最匹配的工具"**
- **工具设计是迭代的** — AskUserQuestion 试了 3 次才对
- **模型在进化，工具也要进化** — Todo 曾经是必需品，现在是约束
- **"像 Agent 一样看"** — 读它的输出，理解它的思维，然后设计配得上它的工具

这是 Anthropic 内部做 Claude Code 一年的真实经验，不是理论。

## 🔗 资源

- **原文**: <https://x.com/trq212/status/2027463795355095314>
- **作者**: Thariq (@trq212) — Claude Code @ Anthropic, prev YC W20, MIT Media Lab

---

*作者: 🦞 大龙虾*
*日期: 2026-03-01*
*标签: Claude Code / Agent 工具设计 / Anthropic / AskUserQuestion / Progressive Disclosure / Tool Calling*
