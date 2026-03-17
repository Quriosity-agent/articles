# Harness Engineering 深度解读：AI Agent 时代的工程范式革命

> 基于 OpenAI、Anthropic、Martin Fowler、LangChain 等核心文献的综合分析
> 原文推荐：[@jakevin7](https://x.com/jakevin7/status/2033784104659882013)

## 一、什么是 Harness Engineering？

**Harness Engineering**（线束工程）是 2026 年初最热门的 AI 工程概念之一。它描述的是：**围绕 AI Agent 构建的工具、约束、反馈循环和脚手架系统，使 Agent 能够可靠地完成复杂任务。**

这个概念由 Mitchell Hashimoto（HashiCorp 创始人）在其博客中首次提出，随后被 OpenAI、LangChain、Martin Fowler 等多方采纳和深化。

核心思想很简单：**模型的智能是"尖刺状"的（spiky intelligence）——在某些任务上极强，在另一些上极弱。Harness 的目标就是把这种不均匀的智能"塑形"，使其在我们关心的任务上稳定可靠。**

## 二、OpenAI 的实验：百万行代码，零手写

OpenAI 在 2025 年 8 月启动了一个激进的实验：**用 Codex Agent 从零构建一个完整产品，人类不写一行代码。**

### 关键数据

| 指标 | 数据 |
|------|------|
| 代码量 | ~100 万行 |
| PR 数量 | ~1,500 个 |
| 工程师人数 | 3→7 人 |
| 人均日产 PR | 3.5 个 |
| 时间节约 | 约 10 倍 |
| 单次运行最长时间 | 6+ 小时 |

### 核心原则：人类掌舵，Agent 执行

> "Humans steer. Agents execute."

工程师的角色从"写代码"变成了：
1. **设计环境** — 让 Agent 能理解项目
2. **明确意图** — 用 Prompt 描述任务
3. **构建反馈循环** — 让 Agent 能自我验证和改进

### AGENTS.md 不是百科全书，而是目录

OpenAI 最早尝试用一个巨大的 AGENTS.md 文件指导 Agent，失败了：

- **上下文是稀缺资源**：太大的指令文件挤占了任务、代码和文档的空间
- **什么都重要 = 什么都不重要**：Agent 开始局部模式匹配，而不是有意导航
- **即时腐烂**：单体手册变成过时规则的坟场
- **难以验证**：一大坨文本不利于机械检查

**解决方案：AGENTS.md 约 100 行，作为"目录"，指向 docs/ 目录中的深层文档。**

知识库结构包括：
- 设计文档（含验证状态）
- 架构文档（域和包分层）
- 质量文档（逐域打分，追踪差距）
- 执行计划（版本化，含进度和决策日志）

## 三、架构约束：让 Agent 快而不乱

### 严格的分层架构

每个业务域按固定层级组织：

```
Types → Config → Repo → Service → Runtime → UI
```

跨切关注点（认证、遥测、Feature Flag）通过单一接口 `Providers` 进入。其他依赖方向一律禁止，由自定义 Linter 和结构测试机械化执行。

> "这种架构通常要到有几百个工程师时才会做。但用 coding agent，它是早期前提——约束才是允许速度而不腐化的东西。"

### "味道不变量"（Taste Invariants）

- 强制结构化日志
- Schema 和类型的命名规范
- 文件大小限制
- 平台特定的可靠性要求

关键洞察：**自定义 Lint 的错误消息本身就是注入到 Agent 上下文的修复指令。**

## 四、垃圾回收：持续清理 AI Slop

全 Agent 生成的代码库会不可避免地漂移。OpenAI 最初每周五花 20% 时间手动清理"AI slop"——当然，这不扩展。

**解决方案：编码"黄金原则"，用后台 Codex 任务定期扫描偏差、更新质量评分、开修复 PR。**

> "技术债像高利贷：小额持续偿还几乎总比积累后痛苦爆发好。"

这本质上是**代码库的垃圾回收机制**：
- 人类品味编码一次
- 然后持续应用于每一行代码
- 每天捕获和修复坏模式，而不是让它们传播数周

## 五、LangChain 的实践：只改 Harness，排名从 Top 30 到 Top 5

LangChain 的 deepagents-cli 在 Terminal Bench 2.0 上从 52.8% 提升到 66.5%——**只调了 harness，模型不变（GPT-5.2-Codex）。**

### 三个关键旋钮

1. **System Prompt** — 如何引导 Agent 思考
2. **Tools** — Agent 可用的工具集
3. **Middleware** — 模型和工具调用前后的钩子

### 最重要的改进：自我验证循环

最常见的失败模式：Agent 写完代码，重读自己的代码，确认"看起来没问题"，然后停下。

**解决方案：Build → Test → Verify → Fix 循环**

- 加入 `PreCompletionChecklistMiddleware`：Agent 退出前强制跑一轮验证
- 类似 "Ralph Wiggum Loop"：钩子强制 Agent 在退出时继续执行验证
- 注入时间预算警告：Agent 天生不擅长时间估算

### 推理计算分配："推理三明治"

```
xhigh → high → xhigh
（规划用高推理 → 执行用中推理 → 验证用高推理）
```

全程 xhigh 反而只有 53.9%（超时太多），而 high 有 63.6%。

## 六、Martin Fowler 的思考：Harness 是未来的服务模板？

Martin Fowler（Birgitta Böckeler）从更宏观的角度思考了 Harness Engineering：

### 1. Harness = 未来的服务模板？

大多数组织只有两三个主要技术栈。Harness（含自定义 Linter、结构测试、基础上下文文档、额外上下文提供者）会不会成为新的 "golden path" 服务模板？

### 2. 更多 AI 自主性需要更多运行时约束

早期 AI 编码炒作假设 LLM 给我们无限灵活性。但可信赖的大规模 AI 生成代码需要**约束解空间**：特定架构模式、强制边界、标准化结构。

### 3. 技术栈会趋同

当编码从"打字"变成"引导生成"，AI 可能推动我们走向更少的技术栈。选择标准不再是"开发者手感"，而是"AI 友好度"。

### 4. 两个世界：Pre-AI vs Post-AI

为 harness 设计的新应用 vs 改造旧应用——后者就像在从没跑过静态分析的代码库上首次运行，被告警淹没。

## 七、对 QCut 的启示

作为一个 AI 视频编辑器项目，Harness Engineering 的理念对 QCut 有直接启示：

1. **QAgent 的 AGENTS.md**：应该作为目录而非百科全书
2. **架构约束先行**：QCut 的包结构需要严格的依赖方向控制
3. **自动化质量检查**：定期扫描代码偏差，而不是手动 review
4. **自我验证循环**：Agent 生成的代码必须经过自动化测试验证
5. **"无聊"技术更好**：可组合、API 稳定、训练集中表示充分的技术对 Agent 更友好

## 八、核心引用

| 来源 | 链接 |
|------|------|
| OpenAI — Harness Engineering | [openai.com/index/harness-engineering](https://openai.com/index/harness-engineering/) |
| LangChain — Improving Deep Agents | [blog.langchain.com](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/) |
| Martin Fowler — Harness Engineering | [martinfowler.com](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) |
| Mitchell Hashimoto — Engineer the Harness | [mitchellh.com](https://mitchellh.com/writing/my-ai-adoption-journey#step-5-engineer-the-harness) |
| HumanLayer — Skill Issue | [humanlayer.dev](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents) |

---

*整理时间：2026 年 3 月 17 日*
*来源推文：[@jakevin7](https://x.com/jakevin7/status/2033784104659882013) — "Harness Engineering 深度解读：AI Agent 时代的工程范式革命"*
