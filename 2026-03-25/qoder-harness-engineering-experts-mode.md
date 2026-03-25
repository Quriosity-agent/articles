# Qoder 如何把 Harness Engineering 做进 Experts Mode

> 原文：[@qoder_ai_ide](https://x.com/qoder_ai_ide/status/2036437931867644016) 发布的 X Article  
> 日期：2026-03-24

![Qoder Experts Mode](https://pbs.twimg.com/media/HELhagGaIAMymAI.jpg)
*图片来源：[@qoder_ai_ide](https://x.com/qoder_ai_ide) / X*

---

## 背景：竞争焦点已经变了

上个月 OpenAI 发了一篇文章：*Harness Engineering: leveraging Codex in an agent-first world*。核心数据：3 个工程师（后来 7 个），5 个月，零行手写代码，产出了一百万行代码、大约 1,500 个 PR。全部由 Agent 驱动。

同期 Stripe、Ramp、Coinbase 也公开了各自的 coding agent 系统内部架构。

信号很明确：**竞争优势已经从"模型能力"转移到了模型之外的一切 —— 也就是 Harness Engineering。**

## 什么是 Harness Engineering？

打个比方：

| 概念 | 类比 |
|------|------|
| Model | CPU（原始算力） |
| Context Window | RAM（有限工作内存） |
| Agent Harness | 操作系统（管理上下文、启动流程、标准驱动） |
| Agent | 应用程序（运行在 OS 上） |

Harness 位于 Agent Framework 之上。Framework 给你积木：工具调用、agentic loop。Harness 给你剩下的：prompt 预设、标准化工具调用、生命周期钩子，以及生产环境里真正需要的能力 —— 规划、文件系统访问、子 agent 协调、验证循环。

**Harness Engineering = AI Agent 的控制系统设计。** 目标：构建基础设施，让 agent 在长时间迭代中持续写出正确代码，而且你能审计、回滚、扩展。

## 行业现状：谁在做？

- **Stripe** — fork 了 Block 的 Goose，构建 Blueprint（状态机，交替确定性节点和 agentic 任务节点），每周合并 1,300+ 完全由 agent 编写的 PR
- **Shopify** — 开源了 Roast，一个交错 AI 步骤和确定性代码的 workflow 框架
- **Ramp** — 在 OpenCode 上构建 Inspect，在 Modal 沙箱中并行执行，30% 合并的 PR 由 agent 编写
- **Coinbase** — 从零构建 Cloudbot，把 PR review 周期从 150 小时压缩到 15 小时
- **OpenAI** — 用 Codex 推动"零手写代码"到百万行规模

这些团队都解决了实际问题：沙箱隔离、上下文预注入、确定性编排。但它们有一个共同的结构性约束：**agent 仍然是单体的** —— 一个模型实例、一个 context window、一条执行路径。

## 单 Agent Harness 的 5 个结构性限制

1. **Context window 是零和博弈** — 研究、编码、测试、review 的上下文全部争夺同一个窗口。任务越复杂，信息密度越低。
2. **角色切换的认知负荷** — 一个 agent 不停切换架构研究、实现、测试执行，就像让一个人同时当 Tech Lead、SWE、QA 和 Code Reviewer。
3. **长执行链中的漂移** — 任务链越长，偏离原始目标的概率越高。没有外部检查点，错误会传播和累积。
4. **缺失功能正确性验证** — 现有实践关注内部质量和一致性，但对"产品是否真的能用"验证不足。代码可以架构干净、lint 通过、文档完善，但业务逻辑是错的。
5. **终端执行风险** — agent 跑 shell 命令时，一条错误命令可能造成不可逆损害。大多数 Harness 靠黑名单或确认对话框，黑名单容易绕过，确认框用户盲点。

## Qoder Experts Mode：怎么解？

Qoder 的方案是把单 agent 升级为**多专家协作系统**。内部 benchmark 显示：**比单 agent 模式质量高 67%，成本不到 2/3。**

### 1. 协调与执行分离

Leader 协调，永不实现。它接收需求、分解任务、管理依赖、跟踪进度、汇报结果。类似 Tech Lead 和领域工程师的关系。从 Harness Engineering 视角看，Leader 是一个 meta-Harness：管理一组专门化的 Agent Harness。

### 2. 异步并行：DAG 驱动的任务编排

所有 SWE Agent 默认异步并行运行。依赖关系形成轻量 DAG："实现后端 API"和"构建前端页面"并行跑；"集成测试"等两者都完成。每个专家在自己的隔离 context window 中工作，零和问题消失。

### 3. 星型拓扑：集中协调

SWE Agent 之间不直接通信，所有协调通过 Leader 路由。Qoder 早期考虑过 P2P 通信但否决了 —— agent 之间直接对话时没人掌握全局，两个专家可能做出矛盾决策而无人察觉。用户也在协调路径中：可以随时插入新指令，Leader 在下一个循环拾取。

### 4. 专业化角色：每个专家都是独立 Harness

**这是对最终输出质量影响最大的设计决策。** 每个专家是针对特定任务类型调优的独立 Harness：不同的工具集、不同的上下文注入策略、不同的执行约束。不是换个 system prompt —— 整个 Harness 都不同。

每个专家的 context window 只包含与其角色相关的信息。这就是 Qoder 应对 Context Rot 的方式 —— 角色隔离从源头消除上下文竞争，比他们试过的任何压缩策略效果都好。

### 5. 跨模型调度：Harness 层的模型编排

单 agent 系统把你锁定在一个模型上。不同能力在不同模型间差异很大：

- **Researcher** — 最强推理模型，综合搜索结果
- **Dev** — 最佳代码生成模型
- **Browser** — 多模态模型，简单验证用轻量回退
- **Reviewer** — 对安全和性能问题最敏感的模型

Leader 把任务类型匹配到模型能力。质量和成本同时改善：精准的模型-任务匹配避免为不需要的能力付费。

> 内部 benchmark：比 Agent Mode 质量高 67%，比 Claude Code Agent Teams 质量高 16%，成本不到 2/3。

### 6. 功能正确性验证：弥补行业空白

大多数 Harness 能告诉你代码干不干净，但不能告诉你产品是否真的能用。Qoder 构建了三个验证专家：

- **Browser 专家** — 在真实浏览器中对用户流程执行 E2E 验证
- **QA 专家** — 使用变更感知上下文机制，验证范围限定在当前变更实际影响的代码
- **Code Reviewer 专家** — 语义 diff + 调用链分析，捕获在隔离看起来没问题但在调用图其他位置引入副作用的情况

验证在编码完成后立即触发，错误在传播到下游任务之前被捕获。

### 7. 自我进化：从静态 Harness 到动态学习系统

传统 Harness 是静态的。Qoder Experts 引入任务级技能提取：系统检测到纠正、恢复的失败或显式用户指令时，Leader 和每个 SWE Agent 从各自领域独立提取可重用技能。

这些技能持久化在记忆系统中，相似任务出现时自动召回。随时间推移，系统不再犯已经学过的错误。

### 8. 终端执行安全：多平台沙箱 + 智能拦截

Shell 语法在不同操作系统间差异巨大。Qoder 为每种 shell（PowerShell、Bash/Zsh、Cmd）构建了独立的 AST 解析器，能穿透命令嵌套识别每个实际执行的子命令。

解析后，命令经过三重独立风险检查：
1. 硬编码黑名单（已知危险命令）
2. 规则引擎（单独无害但组合危险的命令-参数组合）
3. LLM 语义分析层（读取命令意图，补充前两层遗漏）

任何一个触发都阻止执行。通过检查的命令仍在 OS 级沙箱中运行。

## 思考

Qoder 这篇文章的核心论点很清晰：**当我们希望 agent 像工程团队一样协作时，Harness 需要从包装单个模型进化到组织一个团队。**

几个值得关注的设计选择：

- **星型拓扑 > P2P** — 简化了状态追踪，但 Leader 成为单点瓶颈
- **角色隔离消除 Context Rot** — 比压缩策略更根本的解法
- **跨模型调度** — 这是多 agent 架构天然的优势，单 agent 做不到
- **三重安全检查** — 比单纯的 blocklist 或确认框靠谱得多

67% 的质量提升数字很亮眼，但没有公开具体的 benchmark 方法论。期待后续更多细节。

不管怎样，Harness Engineering 从概念到产品化，Qoder 走得很实在。

---

🦞
