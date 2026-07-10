---
title: "Cursor × SpaceXAI Grok 4.5：AI IDE 的竞争点，正在从调用模型变成训练模型"
date: 2026-07-08
source: "https://x.com/cursor_ai/status/2074915744999969059"
canonical: "https://cursor.com/blog/grok-4-5"
tags:
  - Cursor
  - SpaceXAI
  - Grok 4.5
  - AI Coding
  - Agentic Coding
  - Model Training
  - AI IDE
---

# Cursor × SpaceXAI Grok 4.5：AI IDE 的竞争点，正在从调用模型变成训练模型

> **TL;DR:** Cursor 在 2026-07-08 宣布与 SpaceXAI 共同训练 Grok 4.5，并称它是 Cursor 目前最强、也是第一个不只为软件工程构建的模型。更完整的 Cursor blog 说明：Grok 4.5 是 MoE 模型，训练使用了 trillions of tokens 的 Cursor 数据，覆盖开发者与代码库、软件工具、agent 环境的交互；并通过现实环境中的强化学习训练长程任务。真正值得看的不是某个 benchmark 数字，而是 AI IDE 正在从“接入 Claude/OpenAI/Google 模型”走向“用自己的产品数据和工作流训练一类专用模型”。

- **Source X post:** [Cursor on X](https://x.com/cursor_ai/status/2074915744999969059)
- **Canonical post:** [Introducing Grok 4.5 - Cursor](https://cursor.com/blog/grok-4-5)
- **SpaceXAI post:** [Introducing Grok 4.5 - SpaceXAI](https://x.ai/news/grok-4-5)
- **Accessed:** 2026-07-10
- **Tags:** Cursor / SpaceXAI / Grok 4.5 / AI coding / agentic coding / model training / AI IDE

![Cursor Grok 4.5 benchmark announcement](imgs/cursor-spacexai-grok45-model-training/cursor-grok45-announcement.png)

## 一句话判断

**Grok 4.5 这条新闻的关键，不是 Cursor 又支持了一个模型，而是 Cursor 开始把自己的 IDE 使用数据变成模型训练优势。**

Cursor 原推很短：他们和 SpaceXAI 合作训练 Grok 4.5，并称这是 Cursor 目前最强模型，也是第一个为软件工程之外场景构建的模型。真正的信息在官方 blog：Grok 4.5 是 Cursor 与 SpaceXAI 共同训练的 mixture-of-experts 模型，训练里包含大量 Cursor 数据，覆盖开发者与代码库、软件工具、agent 的交互方式。

这件事把 AI 编程工具的竞争往前推了一层。

过去 Cursor、Claude Code、Codex、Windsurf、OpenCode 这类产品的核心问题是：谁的 harness 更好，谁更会组织 repo context、工具调用、patch、测试、review、long-running task。模型是外部供应商提供的，IDE 在模型之上做产品体验。

Grok 4.5 表示另一种路径：**AI IDE 自己成为模型训练数据和训练任务的来源。**

## 从 Composer 2.5 到 Grok 4.5：Cursor 不只想做 coding specialist

Cursor blog 里有一个很重要的对比：Composer 2.5 被训练成 coding specialist，而 Grok 4.5 的数据混合更宽，加入高质量 STEM 任务、研究论文和更广泛的知识工作。

这解释了原推里那句“第一个不只为软件工程构建的模型”。

Cursor 的野心不是只让 agent 更会改代码，而是让它能处理更长、更杂、更像真实电脑工作的任务：

- 软件工程；
- 数据科学；
- 金融分析；
- 法律工作；
- 其他需要使用工具、调查问题、修正错误、验证结果的电脑任务。

这和最近一段时间 agent 产品的趋势一致：coding agent 正在外溢成 computer-work agent。代码只是最早可验证、最高频、付费意愿最强的入口。真正的目标是让模型能够在文件、终端、浏览器、表格、文档、幻灯片之间持续行动。

## Cursor 数据为什么值钱

Cursor 官方说，Grok 4.5 训练包含 trillions of tokens 的 Cursor 数据，捕捉用户与代码库、软件工具之间的大量交互。这句话很关键。

普通代码预训练数据能告诉模型“代码长什么样”。Cursor 数据能告诉模型更多：

1. **开发者如何提需求**：真实用户并不会总写清楚 issue，他们会含糊、补充、反悔、改范围；
2. **agent 如何探索 repo**：看哪些文件、运行哪些命令、怎么从错误输出里找线索；
3. **修改如何被验证**：测试、lint、类型检查、运行 app、查看 diff；
4. **人类如何纠偏**：哪些回答被接受，哪些需要重试；
5. **工具链如何失败**：依赖安装失败、测试 flaky、权限问题、上下文遗漏、错误路径。

这类数据比单纯 GitHub 代码更接近“软件工程过程”。如果模型能学习这些轨迹，它学到的不只是函数和 API，而是开发者与 agent 共同完成任务的行为分布。

这也是 AI IDE 的护城河可能变化的地方。未来最有价值的不是谁能把更多 tokens 塞进上下文，而是谁能把真实任务循环转化成训练信号：观察、计划、编辑、运行、失败、恢复、验收。

## 强化学习环境：用 agent 构造 agent 训练任务

Cursor blog 还提到，他们在现实环境中用强化学习训练困难问题，覆盖软件工程和更广泛知识工作。这些环境教模型调查问题、使用工具、从错误中恢复、验证结果。

更有意思的是环境构造方式：工程师指定问题和验证方式，大量 agent 负责构造、测试、改进环境；有些环境如果靠人类团队可能需要很久。Cursor 说这是用上一代模型加速下一代模型的一种方式。

这部分信息比榜单更重要。它说明模型训练正在变成一个闭环：

1. 产品里产生真实任务轨迹；
2. 团队抽象出可验证任务；
3. agent 帮忙生成和测试训练环境；
4. 新模型在环境里 RL；
5. 新模型进入产品，产生更高质量轨迹；
6. 再进入下一轮训练。

这就是 agent 产品最有威力的 flywheel。用户越多，真实失败模式越多；失败模式越多，训练环境越具体；环境越具体，模型越贴合工作流。

## Benchmark 数字怎么看

Cursor 附图列了几个工程 benchmark：

| Benchmark | Grok 4.5 | 对比信号 |
|---|---:|---|
| Terminal-Bench 2.1 | 83.3% | 接近 GPT-5.5 83.4%、Fable 5 84.3% |
| SWE-Bench Multilingual | 78.0% | 低于 Opus 4.8 84.4%，高于 GPT-5.5 77.8% |
| DeepSWE 1.0 | 62.0% | 低于 GPT-5.5 64.3%、Fable 5 66.1%，高于 Opus 4.8 55.8% |
| SWE-Bench Pro | 64.7% | 低于 Fable 5 80.3%、Opus 4.8 69.2%，高于 GPT-5.5 58.6% |

这些数字说明 Grok 4.5 已经是很强的工程模型，但不是所有维度都第一。尤其在 SWE-Bench Pro 上，Fable 5 仍然明显更高。

更重要的是官方脚注。

第一，Cursor 说明 SWE-Bench Pro 和 Terminal-Bench 对第三方模型使用的是 self-reported scores；SWE-Bench Multilingual 里的 GPT-5.5 分数来自 Cursor 内部运行。也就是说，这些不是一个完全独立、统一 harness、统一预算的第三方评测。

第二，Cursor 明确排除了 CursorBench。原因是 Grok 4.5 训练中意外包含了一个早期 Cursor 代码库快照，因此在 CursorBench 上有优势，具体影响不明；相关数据已为未来模型移除，Cursor 也在更新 CursorBench。

这个脚注反而增强了这次发布的可信度，因为它把 benchmark contamination 的问题摆到台面上。对用模型做生产决策的人来说，这比单纯喊“第一”更有信息量。

## 训练数据污染为什么是大问题

CursorBench 的排除值得单独讲。

AI IDE 自己训练模型，会天然遇到一个难题：产品数据越贴近真实工作流，越容易接近自己的私有评测集、代码库、内部任务和历史 bug。模型越深度学习产品环境，越难保证某些 benchmark 没有被“见过”。

这不是 Cursor 独有的问题。任何用真实产品数据训练 agent 的公司都会遇到：

- 内部代码是否进入训练；
- 用户数据是否被允许用于训练；
- benchmark 是否被训练数据污染；
- 测试任务是否和真实轨迹太相似；
- 模型是否学会了特定 harness 的捷径。

所以未来 AI IDE 的评测不只要问“分数多少”，还要问：

1. 评测集和训练数据如何隔离？
2. 是否有独立第三方复现？
3. 是否公开 harness、预算、上下文、工具权限？
4. 是否报告被排除的 benchmark 和原因？
5. 是否有跨产品、跨 repo、跨语言的迁移测试？

Grok 4.5 的 CursorBench caveat 很适合作为行业样本：当模型来自产品数据时，benchmark governance 会变成产品可信度的一部分。

## 价格和可用性：它不是只给 Cursor 自己用

Cursor blog 说 Grok 4.5 已在 Cursor 的 desktop、web、iOS、CLI 和 SDK 中可用，个人和团队订阅计划包含模型用量，并在首周提供 double usage。价格上，base model 是 $2/M input tokens 和 $6/M output tokens；fast variant 是 $4/M input tokens 和 $18/M output tokens。

SpaceXAI 官方页也说 Grok 4.5 可在 Grok Build、Cursor 全计划和 SpaceXAI console 使用，并补充 EU 区域暂不可用，预计 7 月中旬开放。

这说明它不是一个只服务 Cursor IDE 的内部模型，而是 Cursor 与 SpaceXAI 共同训练、再跨产品分发的模型：

- 在 Cursor 里做 coding / agentic coding；
- 在 Grok Build 里做更广泛的电脑任务；
- 通过 API console 给开发者集成；
- 通过 pricing 和 token efficiency 与 OpenAI/Anthropic/Google 竞争。

如果这个模式跑通，AI IDE 公司就不只是模型客户，也会变成模型共同研发方、数据方、评测方和分发方。

## 对 AI IDE 竞争的影响

这条新闻对 Cursor 自己的意义很直接：它降低了对单一外部模型供应商的依赖。

过去 AI IDE 竞争有一个结构性风险：如果 Claude、GPT、Gemini 或其他模型在某个月突然领先，产品体验会跟着漂移；如果模型供应商自己做 coding agent，IDE 也会面对上游下场竞争。

共同训练 Grok 4.5 后，Cursor 至少多了三层主动权：

1. **训练数据主动权**：能把真实 IDE 交互转化为模型改进；
2. **任务定义主动权**：能设计更贴合自己产品的 RL 环境和验收任务；
3. **模型组合主动权**：Composer 2.5 继续做更小的 coding specialist，Grok 4.5 做更大的通用 agent/knowledge work 模型。

这也会逼其他 AI coding 产品思考自己的模型策略。只做上层 UX 仍然有价值，但如果竞争对手能把产品使用数据反馈到模型训练，纯粹“换模型供应商”的差异会越来越薄。

## 团队该怎么用它

对普通工程团队来说，我不会建议只因为发布图就立刻把 Grok 4.5 设为唯一默认模型。更合理的做法是把它加入模型路由：

| 场景 | 是否适合试 Grok 4.5 |
|---|---|
| 长时间 repo 修改、终端操作、工具调用 | 很适合测试 |
| 多语言 SWE 任务 | 值得和 Opus/GPT/Fable 对照 |
| 办公文档、表格、研究型电脑任务 | 值得探索，因为训练目标已超出 coding |
| 高风险安全/代码审计 | 需要看新增 safeguards 和组织策略 |
| 需要最强 SWE-Bench Pro 表现的任务 | 仍应与 Fable/Opus 等强模型并跑 |
| 内部敏感代码 | 先确认 Cursor/SpaceXAI 的数据使用、隐私和企业配置 |

真正的评测方式也很简单：拿自己团队真实任务做 A/B，不要只看公开榜单。比如同一个 bugfix、迁移、测试修复、文档生成、Excel 建模任务，让 Grok 4.5、Composer 2.5、Claude、GPT 分别跑，记录：

- 完成率；
- 人工干预次数；
- 测试失败次数；
- 输出 token 和耗时；
- 是否贴合代码风格；
- 是否在工具失败后正确恢复；
- reviewer 是否愿意合并。

这类工作流指标，比“榜单相差 1 个点”更能决定真实生产价值。

## 结论

Cursor 与 SpaceXAI 共同训练 Grok 4.5，是 AI IDE 竞争的一次明显升级。

它说明 Cursor 不满足于做模型之上的壳，也不只做更好的 repo context 和 agent UX。它开始把自己的用户交互、工具轨迹、代码库经验、RL 环境构造能力，变成模型本身的一部分。

这会带来两个方向的变化：

- 好的一面：模型会更贴近真实工程和电脑工作流，更懂得使用工具、恢复错误、验证结果；
- 需要警惕的一面：训练数据边界、评测污染、用户数据治理和 benchmark 透明度会变得更重要。

所以 Grok 4.5 最值得记住的不是 83.3% 还是 64.7%。真正的信号是：**AI coding 产品正在从“模型调用方”变成“模型共训方”。**

下一轮 AI IDE 的护城河，可能不只是编辑器体验，而是产品数据、训练环境、评测治理和模型路由共同组成的闭环。
