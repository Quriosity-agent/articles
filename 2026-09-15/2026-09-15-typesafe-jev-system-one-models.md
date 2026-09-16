---
title: "TypeSafe Jev 深度拆解：放弃生成文本，AI 才能成为软件里的概率型 if 语句"
date: 2026-09-15
source: "https://typesafe.ai/blog/introducing-system-one-models-and-jev"
canonical: "https://typesafe.ai/blog/introducing-system-one-models-and-jev"
tags:
  - TypeSafe AI
  - Jev
  - System One Models
  - RLCD
  - Structured Outputs
  - Calibrated Decisions
  - AI Automation
  - Probabilistic Software
---

# TypeSafe Jev 深度拆解：放弃生成文本，AI 才能成为软件里的概率型 if 语句

> **TL;DR:** TypeSafe AI 发布的 Jev 不是聊天模型，也不是把普通 LLM 套上 JSON Schema。它接收文本或 JSON 状态，以及一组提前定义好的 `Noul`、`Choice`、`Score` 问题，直接返回类型固定的答案、概率分布和置信度。TypeSafe 声称，这种 System One Model 通过并行采样和 Reinforcement Learning for Calibrated Decisions（RLCD），能以 70–500ms 延迟和每百万输入 token 0.042 美元的价格，把语义判断嵌入普通代码。真正成立的突破是“输出空间被封闭，因此不会出现 schema 或 tool-call 形状错误”；仍待证明的部分是语义正确率、概率校准、跨领域泛化和长期价格可持续性。

- **发布方:** [TypeSafe AI](https://typesafe.ai/)
- **发布文章:** [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- **作者:** Diogo Almeida，TypeSafe 创始人
- **发布日期:** 2026-09-15
- **产品状态:** Jev early access；托管 API，模型权重未公开
- **公开开发组件:** Python/TypeScript SDK、Agent Skill、System One LLM Adapter，均为 MIT License
- **核验日期:** 2026-09-16

![TypeSafe 为 Jev 与 System One Models 制作的发布主视觉](imgs/typesafe-jev-system-one-models/01-jev-system-one-hero.png)

## 一句话判断

Jev 最值得注意的地方不是“又一个更快的模型”，而是它主动放弃了 LLM 最有代表性的能力：**自由生成字符串。**

普通 LLM 的接口是 `文本 -> 文本`。即使启用 structured output，底层任务仍然是逐 token 生成，再由 schema、parser、retry 和业务代码把字符串重新压回有限状态。Jev 把接口改成：

```text
非结构化或结构化状态 + 有限答案空间
                     ↓
类型化决策 + 概率分布 + 置信度
```

这让它更像一个可学习的、带不确定性的函数调用，而不是助手。TypeSafe 自己把这种形态称为“smart if-statements”：神经网络处理模糊语义，传统代码掌握流程、权重、阈值和副作用。

## System One 不是“快一点的 System Two”

名字借自 Daniel Kahneman 的 System 1 / System 2 区分。这里的 System One 指快速、直觉式、聚焦的判断；它不写回复、不生成代码，也不展示推理。

Jev 适合的问题形状是：一个懂业务的人拿到充分上下文后，几秒钟内能做出的原子判断。

- 这封邮件是否表达紧迫性？
- 工单应路由到 billing、technical 还是 sales？
- 客户愤怒程度处在哪个定义好的等级？
- 这段 Agent trace 是否需要人工复查？

它不适合“一次分析全部信息并给出最佳方案”。复杂任务要拆成若干独立判断，再由代码组合。换句话说，Jev 没有消灭 workflow engineering，反而把工作流设计提升为产品的主要工程资产。

## 三种原语定义了它能说什么

TypeSafe API 当前只公开三类 question primitive：

| 原语 | 问题形状 | 返回值 | 适合用途 |
|---|---|---|---|
| `Noul` | 是 / 否 | “是”的概率，0 到 1 | 是否欺诈、是否紧急、是否提到某技能 |
| `Choice` | 从封闭集合中选一项 | 选中项、所有选项概率、confidence | 意图分类、团队路由、文档类型 |
| `Score` | 在有序等级上评分 | 可插值分数、等级概率、confidence | 严重度、风险、情绪、质量 |

一次请求可以把三种问题混在一起。所有问题共享同一份 `state`，但彼此独立评估，不会把前一个答案偷偷作为后一个问题的上下文。官方建议把能针对同一状态提出的问题一次发完，包括暂时用不到的“投机问题”，由代码决定采用哪些答案。

文档给出的请求 token 预算约为 32,000，约合 15 万英文字符。`Choice` 的 cardinality 上限为 255；超过时需要先独立评分，再做第二阶段选择。它目前处理的是文本或 JSON 状态，不支持图片输入。

## 置信度不是“模型又说了一遍我很确定”

`Choice` 和 `Score` 的 confidence 是从完整概率分布计算出来的统计量，不是另一段自我评价。分布越集中，confidence 越高；分布越平，说明答案空间没有明显赢家、标准含混，或输入证据不足。`Noul` 本身就是 P(true)，所以没有单独 confidence 字段。

这里有两个经常被混淆的层次：

1. **概率**回答每个选项各有多大可能。
2. **校准**要求长期来看，被赋予 0.8 概率的事件应当约有 80% 发生。

校准只对一组预测有意义，不能保证单个 0.99 的答案一定正确。TypeSafe 文档也明确建议按风险设置不同阈值：低风险读取操作可以自动执行；转账、封禁或删除等高风险动作，即使 confidence 很高，也应加入确认或人工复核。

这比让普通 LLM在 prose 结尾补一句“置信度 95%”更可用，但仍需要团队在自己的数据分布上画 calibration curve，测 Expected Calibration Error、Brier score，以及不同阈值下的误报和漏报。

## 为什么并行输出可能真的更快

传统 LLM 自回归生成：第 N 个 token 依赖前 N-1 个 token。答案越长，解码次数越多；如果模型要同时回答 30 个分类问题，仍要把标签、概率和 JSON 标点逐 token 写出来。

TypeSafe 声称 Jev 用新的模型架构和 parallel sampler，一次计算全部问题的决策分布。它不需要生成解释、重复字段名或等待结束符，因此新增独立问题对延迟影响很小。官方把这种模式称为 speculative fan-out：状态只传一次，几十到几百个判断并行展开。

发布页给出的价格和延迟是：

| 指标 | Jev 官方价格/结果 |
|---|---|
| 输入价格 | 0.042 美元 / 百万 token |
| 输出价格 | 免费，官方称低到不值得计量 |
| 端到端延迟 | 70–500ms |
| 官方相对主张 | System One 形状任务上快 40–200 倍 |

这些数字有合理的架构解释，却还不是独立 benchmark。发布方说明测速通常从美国西海岸的员工笔记本发起，服务也部署在那里；成本是否受到 launch subsidy 影响，要靠长期运营证明。

## RLCD 公开了目标，没有公开配方

TypeSafe 把训练方法称为 Reinforcement Learning for Calibrated Decisions：

- RLHF 优化人类偏好的聊天回答；
- RLVR 优化可以程序验证的推理结果；
- RLCD 优化封闭答案空间中的决策与校准概率。

这个目标定义很清楚：高概率要对应更高实际正确率，模型不能靠“说得像对的”拿奖励。但截至发布时，TypeSafe 没有公开 Jev 的参数规模、基础模型、具体架构、训练数据、RLCD loss/reward 设计、校准方法、训练计算量、权重或技术论文。

因此，“新架构”和“新训练算法”目前是产品方主张，不是外部可以复现的研究结论。还有一个搜索层面的提醒：RLCD 这个缩写此前已用于 Reinforcement Learning from Contrast Distillation，那是另一套 2023 年的语言模型对齐方法，与 TypeSafe 的 Calibrated Decisions 无关。

## Workflow eval 测的不是通用智能

TypeSafe 没有把 Jev 放进传统聊天、数学或 coding leaderboard，而是设计了四个 workflow eval：

- Security Incidents；
- Agent Trace Observability；
- Invoice Processing；
- Customer Service。

每个任务先被拆成一张固定 compute graph：代码完成确定性规则，模型只回答窄问题。所有参评模型使用同一 workflow。参考标签不是人工真值，而是 GPT-6 Astra 与 Claude Fable 5.1 在 high thinking 下对每个问题给出的概率平均值。

![四个 workflow 平均后的准确率与单次工作流成本，Jev 位于官方成本 Pareto frontier](imgs/typesafe-jev-system-one-models/02-workflow-accuracy-cost.png)

图中 Jev 平均准确率约 67.8%，低于部分高成本模型，但成本只有约 0.0004 美元/工作流。TypeSafe 首页的“快 193.6 倍、便宜 444.6 倍”来自这组评测的高端差距；发布文章自己提醒，它们很可能处在现实收益的上沿。

这个评测有三项值得肯定的设计：

1. workflow 固定，避免每个模型配一套不同 harness；
2. 同时比较“结构化工作流”和“一个 prompt 包办全部逻辑”；
3. 公开任务、查询、分歧和成本，而不是只给一张排行榜。

它也有四个明显限制：

1. 四个 workflow 都由 TypeSafe capability team 制作，可能天然贴合产品范式；
2. “正确答案”是两个前沿模型的共识，不是真实业务结果；
3. 参评 LLM 用 default reasoning，而参考模型用 high thinking；
4. Jev 只和对照模型在 System One 形状任务上比较，不能推出通用智能同级。

![Security Incidents workflow：模型做窄判断，代码完成分支、阈值与动作编排](imgs/typesafe-jev-system-one-models/03-security-workflow.png)

真正有价值的结论不是 Jev “击败前沿模型”，而是：当任务能被分解成大量独立判断时，自由文本模型可能是一个过度通用、价格过高的计算形态。

## “不会幻觉”需要改写成更精确的话

发布页写 Jev “can’t hallucinate”，但同一页面的平均准确率图又显示它会判断错误。两者并不矛盾，只是 hallucination 被缩窄成了输出契约问题。

Jev 的答案空间由调用者预先定义，因此它不会：

- 发明不存在的 enum；
- 少一个必填字段；
- 把数字写成 prose；
- 生成 schema 之外的 tool call；
- 突然开始解释、拒绝或输出 Markdown。

这类结构错误确实可以从设计上消除。但 Jev 仍可能在 `billing`、`technical`、`sales` 三个合法选项中选错一个，也可能给错误答案很高概率。那是**语义错误**，不是类型错误。

![TypeSafe 发布页中的结构化输出与 tool-call error rate 图](imgs/typesafe-jev-system-one-models/04-structured-tool-error-rates.png)

图中的 Jev 0% 也不是实测样本率。TypeSafe 明确写道：这个数字“not empirical”，因为 schema matching 是架构保证，所以直接把 0% 放进图中。作为结构保证，这个说法可验证且很强；把它扩展成“模型不会产生错误事实或错误判断”则不成立。

## 它和 LLM structured output 的真正差别

OpenAI、Anthropic 等 API 已经能用 JSON Schema、tool calling 和 constrained decoding 产生结构化结果。TypeSafe 甚至开源了 `system-one-adapter-python`，把普通 LLM 包装成与 TypeSafe API 兼容的 `Noul`、`Choice`、`Score` 接口，用于公平比较。

差异不在“能不能得到 JSON”，而在优化对象：

| 路线 | 模型本体优化目标 | 输出生成方式 | 失败处理 |
|---|---|---|---|
| LLM + structured output | 通用文本与推理 | 自回归生成受限 JSON | schema 约束、解析、重试、概率归一化 |
| Jev | 类型化决策与校准概率 | 官方称并行产生所有答案 | 输出空间内生受限，不需要文本修复 |

普通 LLM 的优势是开放式推理、解释、代码、长链规划和新答案生成；Jev 的优势是固定答案空间、高并发、低延迟和概率接口。二者更像协作关系：Jev 负责分类、路由、评分、guardrail 和验证；遇到低 confidence 或确实需要生成内容时，再升级到 reasoning model 或人。

## 对 Agent 产品最现实的用法

Jev 不太像 Agent 的大脑，更像 Agent runtime 里的高速控制平面：

- 在每次 tool call 前判断风险、意图和权限等级；
- 检查执行 trace 是否异常、是否需要人工查看；
- 给 RAG 文档打相关性、矛盾和 prompt injection 分数；
- 从数百个 Skill 中预筛候选，再把少量全文交给推理模型；
- 对客服、风控、账单和安全告警做 confidence-gated routing；
- 作为廉价 verifier，决定是否接受、重试或升级一次昂贵生成。

这会改变系统成本模型。过去团队常把所有语义任务都发送给一个昂贵 LLM；System One 路线把绝大多数窄判断前移到低延迟决策层，只让少数困难样本进入生成式模型。

但要得到可靠系统，问题、选项、阈值和规则必须集中管理、版本化并用真实流量回放。TypeSafe 自己的 Agent Skill 也承认，coding agent 不擅长一次写对问题，开发者应共同编辑，并把阈值和 questions 放在容易审查的单一位置。

## 现在还不能下什么结论

Jev 仍是 early access，本次检查也没有可用的 TypeSafe API key，因此没有独立复测延迟、成本、稳定性或校准曲线。现阶段不能确认：

- 70–500ms 在跨地区、并发和长状态下是否稳定；
- 0.042 美元 / MTok 是否是长期可持续价格；
- calibration 在客户私有分布、非英语文本或分布漂移后是否保持；
- 独立问题在共享 state 下是否真的完全不互相干扰；
- 32K token 上下文接近上限时的准确率变化；
- 模型架构、训练数据与 RLCD 是否能被第三方复现；
- 服务的数据保留、企业合规和 SLA 是否适合高风险生产系统。

SDK 和 Agent Skill 开源不等于模型开源。开发者可以审查客户端、类型和 retry 行为，但 Jev 本身是托管黑盒。

## 结论

Jev 提出了一条很值得认真看的路线：AI 不一定要先学会写无限自由的字符串，再被工程师费力塞回软件；它可以从一开始就被训练成一个有限、概率化、可组合的决策接口。

这条路线牺牲了通用生成能力，换来结构保证、并行效率和可用于路由的概率。它最有说服力的成果不是“零幻觉”，而是**零 schema 越界**；最需要继续验证的不是能不能输出合法类型，而是这些概率在真实业务分布中是否诚实、稳定，并且长期优于更便宜的小型分类器或 LLM structured output。

如果 TypeSafe 能用第三方数据证明校准、跨域迁移和价格可持续性，System One Models 可能成为 Agent 系统的一层新基础设施：不是替代推理模型，而是让大量过去不值得调用模型的 if 语句获得语义判断能力。

## Sources

1. TypeSafe AI, “Introducing System One Models & Jev”
   https://typesafe.ai/blog/introducing-system-one-models-and-jev

2. TypeSafe documentation: System One
   https://docs.typesafe.ai/concepts/system-one

3. TypeSafe documentation: Primitives
   https://docs.typesafe.ai/primitives

4. TypeSafe documentation: Confidence
   https://docs.typesafe.ai/confidence

5. TypeSafe Workflow Evals
   https://evals.typesafe.ai/

6. TypeSafe AI primer and RLCD description
   https://docs.typesafe.ai/introduction/machine-learning-primer

7. TypeSafe System One Adapter for LLM comparisons
   https://github.com/typesafe-ai/system-one-adapter-python

8. TypeSafe Python and TypeScript SDKs
   https://github.com/typesafe-ai/typesafe-sdk-python
   https://github.com/typesafe-ai/typesafe-sdk-js

9. Prior, unrelated RLCD paper: Reinforcement Learning from Contrast Distillation
   https://arxiv.org/abs/2307.12950
