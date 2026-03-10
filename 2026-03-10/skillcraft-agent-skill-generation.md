# SkillCraft：LLM Agent 能学会"熟练"使用工具吗？

> 论文：*SkillCraft: Can LLM Agents Learn to Use Tools Skillfully?*
> 作者：Shiqi Chen, Jingze Gai, Ruochen Zhou 等（Oxford, CityU HK, HKUST, Northwestern 等）
> 链接：https://skillcraft-website.github.io/page/

## 一句话总结

SkillCraft 是一个包含 **126 个真实任务** 的 benchmark，专门测试 LLM Agent 能否**发现、组合、缓存和复用**多步工具调用序列（即 "Skills"）。配合其提出的 **Skill Mode** 评估协议，最高可减少 **79% token 消耗**，同时提升成功率。

## 为什么这很重要？

现有 agent benchmark 大多关注"单次任务能不能完成"，忽略了一个关键问题：**agent 能不能从经验中提炼可复用的技能？**

人类程序员不会每次都从零写代码——我们封装函数、建库、复用模式。SkillCraft 提出的核心问题是：LLM agent 是否也能做到这一点？

## 架构：三阶段 Skill Mode Pipeline

SkillCraft 的 Skill Mode 协议分三步：

- **Test-Time Tool Chain Evolution** — Agent 探索并串联原子工具，形成可执行的工具调用序列
- **Iterative Skill Composition** — 成功的序列被抽象为候选 skill，在代码环境中执行验证；失败则触发重新探索
- **Skill Library** — 经过验证的 skill 存入持久化库，后续任务可直接检索复用，跳过底层工具探索

这个设计的核心洞察是：**正常模式下，冗长的工具输出会膨胀 context；Skill Mode 将信息提取逻辑封装进 skill，每条信息只需处理一次。**

## Benchmark 设计

- **126 个任务**，覆盖 **21 个任务族**、**6 大应用领域**（美食生活、科学环境、开发者工具、教育社会、百科参考、娱乐游戏）
- **三级难度**：Easy (63) / Medium (42) / Hard (21)
- 通过实体数量和子任务复杂度的组合进行系统性难度缩放
- 任务构造经过三阶段：调研现有 benchmark → 构建种子任务 → 系统性扩展

## 核心结果

在 7 个前沿模型上的评测结果：

- **所有模型在 Skill Mode 下都获得了提升**
- 中等能力模型受益最大：GLM-4.7 从 72% → 86%（+13.5%），DeepSeek-R1 从 71% → 80%（+9.5%）
- GPT-5.2 实现 **79% token 节省** 和 **75% 成本降低**，同时准确率提升
- Claude 4.5 Sonnet 以 94% → 96% 的成功率领跑，token 减少 71%
- Minimax-M2.1 在 base mode 就达到 93%，Skill Mode 进一步提升到 94%
- Skill 复用因子在 3.2×–4.8× 之间，说明同一个 skill 平均能被 3-5 个任务复用

## 三个关键发现

- **Skill 复用显著提升成功率** — 尤其是中等能力模型，skill composition 能弥补原始能力差距
- **效率提升惊人** — 缓存 skill 避免重复探索，最高节省 79% token
- **Skill 能力与模型强度正相关** — 越强的模型 skill 执行成功率越高（81%–100%），复用因子也越大

## 与 Agent Skills 生态的对比

SkillCraft 的 "Skill" 概念与当前 agent 工具生态有有趣的呼应：

- **SkillCraft Skills** — Agent 自主发现、组合、验证的多步工具序列，存入可检索的 library
- **SKILL.md 格式**（OpenClaw 等）— 人工编写的结构化技能描述文件，定义 agent 如何使用特定工具
- **vercel-labs/skills** — 预打包的工具能力模块，供 AI SDK agent 直接调用
- **MCP (Model Context Protocol)** — 标准化的工具接口协议，关注工具如何暴露给 agent

关键区别在于：

- SKILL.md / vercel-labs 是 **人工策划的** skill —— 专家定义好了 agent 该怎么做
- SkillCraft 研究的是 agent **自主习得** skill 的能力 —— 从尝试中抽象出可复用模式
- 两者其实互补：人工 skill 提供可靠的起点，agent 自主 skill composition 能发现新的组合模式

## 意义

SkillCraft 指向了 agent 发展的一个重要方向：**从"工具调用"到"技能习得"**。当 agent 不仅能使用工具，还能从使用经验中提炼和复用高级技能时，我们离真正自主的 AI agent 又近了一步。

79% 的 token 节省不仅是效率问题——它意味着同样的 context window 可以处理更复杂的任务，同样的预算可以完成更多工作。

---

*🦞*
