---
title: "Sakana Fugu 深度拆解：下一代模型竞争点，可能不是更大的单体模型，而是会调度模型的模型"
date: 2026-06-22
source: "https://sakana.ai/fugu-release/"
product_page: "https://sakana.ai/fugu/"
technical_report: "https://github.com/SakanaAI/fugu/blob/main/Fugu_technical_report.pdf"
tags:
  - Sakana AI
  - Sakana Fugu
  - Fugu Ultra
  - Model Orchestration
  - Multi-Agent
  - Agent Runtime
  - OpenAI-Compatible API
---

# Sakana Fugu 深度拆解：下一代模型竞争点，可能不是更大的单体模型，而是会调度模型的模型

Sakana AI 在 2026-06-22 发布了 Sakana Fugu 和 Fugu Ultra。官方标题很直接：**One Model to Command Them All**。

这不是又一个普通大模型发布。Fugu 的核心主张是：把一个多模型、多 agent 的 orchestration system 包装成“一个模型 API”。用户从外部只调用一个 OpenAI-compatible endpoint；系统内部由 Fugu 判断是否自己回答、是否调用其他模型、如何分工、如何验证、如何合成最终答案。

![Sakana Fugu architecture overview](imgs/sakana-fugu-model-orchestration/fugu-architecture.webp)

## 一句话概括

**Sakana Fugu 的重点不是“我比某个单体模型更聪明”，而是把模型选择、任务委派、验证和结果合成变成一个可训练的模型能力。它试图把 multi-agent runtime 从应用层框架，下沉到模型接口本身。**

如果这条路线成立，未来开发者接入的可能不再是“某个模型”，而是“一个会调度模型池的模型”。

## Fugu 到底是什么

官方对 Fugu 的定义很有意思：它是一个“像单一模型一样工作的多 agent 系统”。用户把请求发到一个 endpoint，Fugu 决定处理方式：

1. 简单任务，直接解决；
2. 复杂任务，组装多个 expert models；
3. 在 agent pool 中做模型选择；
4. 把子任务委派给不同 agent；
5. 对中间结果做验证；
6. 合成一个最终答案。

更关键的是，Sakana 说 Fugu 自身也是一个语言模型，专门训练来理解什么时候委派、agent 之间应该如何沟通、如何把多个结果合并成可靠答案。官方图里甚至写到，它可以调用 agent pool 里的 closed/open models，也可以递归调用自己的实例。

这和传统 agent framework 的区别在于：传统方式通常由开发者写 router、planner、executor、critic、verifier，然后用 prompt 和代码 glue 在一起。Fugu 想把这些协调策略学出来，变成模型内部能力。

## 两个模型：Fugu 和 Fugu Ultra

发布时有两个型号：

| 模型 | 官方定位 | 适合场景 |
|---|---|---|
| Fugu | 性能和低延迟平衡 | 日常工作、Codex 类 coding / code review、聊天服务 |
| Fugu Ultra | 最大化复杂问题的回答质量 | AI research、论文复现、网络安全分析、文献和专利调查 |

两个模型都通过单一 OpenAI-compatible API 访问。产品页还强调，团队可以把特定 agents 从 pool 中 opt out，以满足数据、隐私、合规或组织要求。

这点很实际。多模型系统最大的企业问题不是“能不能调很多模型”，而是“哪些模型能碰我的数据”。如果 orchestration layer 不能按 provider/model 做排除，它很难进入有合规要求的工作流。

## 为什么 Sakana 把它讲成 AI sovereignty

Fugu release 的叙事不只是技术，也很明显地带着“供应链韧性”意味。

Sakana 的说法是：AI 不能长期依赖某一个单一供应商，尤其在关键基础设施、金融、治理等场景中，API 访问可能受到监管、出口管制和外交政策影响。官方用 Anthropic Fable / Mythos access 变化作为例子，说明 access 可以在一夜之间变化。

这个叙事有商业意味，但也切中了 agent 产品的现实风险。很多团队现在把整个产品能力绑定到一个 vendor model：

- 价格变了，成本模型就变；
- rate limit 变了，产品稳定性就变；
- 某区域访问变了，业务可用性就变；
- 模型行为变了，评测和 prompt 都要重做；
- 某模型下线或被限制，生产系统需要紧急迁移。

Fugu 给出的解法不是让用户自己维护复杂 router，而是让一个 learned orchestrator 在可替换 agent pool 上工作。某个 provider 出问题时，系统理论上可以绕开它。

这里的长期价值不是“省一次迁移成本”，而是把模型供应链韧性变成 runtime 能力。

## Benchmark：强，但要看清比较方式

Sakana 官方图表显示，Fugu Ultra 在多个 benchmark 上接近或超过一批 frontier baselines，包括 LiveCodeBench、GPQA-D、CharXiv Reasoning、SWEBench Pro、SciCode、Humanity's Last Exam、Terminal Bench 2.1、CTI-REALM 等。

![Fugu benchmark comparison grid](imgs/sakana-fugu-model-orchestration/release-benchmark-grid.webp)

需要注意几个 caveat。

第一，官方说明 Fugu 以外的 baseline 分数来自各模型提供方报告；Fable 5 和 Mythos Preview 如果同一 benchmark 有两个分数，会取较高者。

第二，Fable 5 和 Mythos Preview 不在 Fugu 的 agent pool 中，因为它们不是 publicly accessible。也就是说，图中不是“Fugu 调了 Fable/Mythos 才赢”，而是用这些模型作为对照。

第三，SWEBench Pro 使用 mini-swe-agent 作为 scaffolding。agent benchmark 不能只看裸模型分数，harness 本身就是能力的一部分。

第四，Fugu 是 orchestration model，底层模型池可能会变化。它的 benchmark 结果更像“某个时间点的 Fugu runtime + agent pool + harness 表现”，而不是一个静态权重的永恒分数。

这些 caveat 不削弱 Fugu 的意义，反而说明这类产品评价方式要变。我们不再只比较单个模型参数，而是在比较一个动态 runtime。

## 与底层模型的关系：Fugu 不是普通 ensemble

发布页还给了一张 Fugu 与其 underlying foundation models 的对比表。它想表达的是：Fugu 不只是把多个模型投票平均，而是在特定任务上通过调度、委派和合成，获得比底层模型更好的结果。

![Fugu benchmark table against underlying models](imgs/sakana-fugu-model-orchestration/release-benchmark-table.webp)

这和常规 ensemble 有差异。

传统 ensemble 常见做法是同题多答、投票、rerank 或 self-consistency。Fugu 的目标更像任务级 coordination：不同 agent 可能承担计划、实现、验证、搜索、解释、批评等角色；协作模式不是用户手写固定 workflow，而是由模型学出来。

这也是 Sakana 把 Trinity 和 Conductor 两篇 ICLR 2026 论文放在 foundation section 的原因：

- **TRINITY**：用 lightweight evolved coordinator，在多轮里给不同 LLM 分配 Thinker、Worker、Verifier 等角色；
- **Conductor**：用 reinforcement learning 学自然语言协调策略，让系统设计 agent 通信模式和 focused prompts。

Fugu 像是把这条研究线产品化：从“我们可以训练 coordinator”走向“把 coordinator 包成一个可调用模型”。

## AutoResearch 案例：长程任务才是 orchestration 的主场

产品页里最有意思的实验不是普通榜单，而是 AutoResearch。

官方描述的实验是：一个 AI agent 自主改进小 GPT 的训练 recipe。它使用 AutoResearch 框架，反复编辑训练代码、运行实验，只保留让 validation bits-per-byte 降低的改动。实验在单张 H100 上跑了约 14 小时，总共 123 次实验。Fugu Ultra 最终得到官方报告的最佳平均 BPB：0.9774 ± 0.0019，优于 Model C 的 0.9781、Model B 的 0.9793 和 Model A 的 0.9822；最佳单次 run 到 0.9748。

![Fugu product benchmark and AutoResearch chart](imgs/sakana-fugu-model-orchestration/product-benchmark-chart.webp)

这类任务比普通问答更能说明 orchestration 的价值。因为它包含：

1. 理解实验目标；
2. 修改代码；
3. 运行训练；
4. 读取指标；
5. 分析失败；
6. 尝试新 hyperparameters；
7. 在长时间内维护方向感。

单个模型一次回答再好，也不等于能连续 14 小时做研究迭代。Fugu Ultra 的主张正是：当任务变成长程、开放、多步、需要不断验证时，调度多个 expert agents 可能比调用单一 frontier model 更稳。

## Pricing 也暴露了一个产品难题

产品页的 pricing 部分说明，Fugu 有 pay-as-you-go 和 subscription plan。更值得注意的是 pay-as-you-go 的计费逻辑：

- 如果只有 1 个 agent active，用户支付该 underlying model 的标准费率；
- 如果多个 agents active，Sakana 表示不会把模型费用层层叠加，而是基于参与的最高 tier model 收一个单一费率；
- Fugu Ultra 有 `fugu-ultra-20260615` 的固定计费项；
- subscription tiers 同时包含 Fugu 和 Fugu Ultra。

这暴露了 multi-agent 产品的一个核心问题：如果每次内部调度都按所有子模型 token 叠加计费，用户很难预测成本，也很难把它接进生产工作流。Fugu 试图把内部复杂性封装成更稳定的外部价格模型。

这和 API 抽象是一体两面。你不能一边说“用户只需要调一个模型”，一边把内部每个 agent 的成本细节原样暴露出去。真正产品化的 orchestration，需要同时隐藏技术复杂度和成本复杂度。

## 对开发者意味着什么

如果 Fugu 这类产品成立，开发者接入 agent 能力的方式会发生变化。

过去的路径是：

1. 选一个主模型；
2. 写 planner prompt；
3. 接 search/code/browser/tools；
4. 写 router；
5. 写 verifier；
6. 处理失败重试；
7. 接多个 provider 做 fallback。

Fugu 的路径是：

1. 调一个 OpenAI-compatible model；
2. 把复杂调度交给 Fugu；
3. 通过 agent pool controls 管合规边界；
4. 在任务层做验收，而不是在每个子 agent 层写 glue。

这不会让应用层 agent framework 消失。业务系统仍然需要权限、工具、状态、审计、文件、数据库、UI 和人类验收。但模型层如果已经会做一部分 model orchestration，应用层 agent 可以从“调度模型”更多转向“管理任务状态和安全边界”。

## 风险与待验证点

Fugu 的方向很重要，但也有几个需要看清的风险。

第一，orchestration 可解释性。用户只调用一个模型，但内部可能调用多个 agents。生产环境会需要知道：谁看过数据、哪些 provider 被调用、为什么委派、哪些中间证据被保留。

第二，benchmark 可复现性。官方已经说明很多 baseline 是 provider-reported，agent benchmark 又依赖 harness。未来最好看到第三方复测、固定 agent pool 配置和更透明的评测日志。

第三，延迟和成本。Fugu 主打把复杂多 agent 系统包成单 API，但复杂任务仍然要付出时间和 compute。低延迟 Fugu 与高质量 Fugu Ultra 的分层说明，这不是免费的能力提升。

第四，安全与数据边界。允许 opt out 某些 agents 是好方向，但企业还会关心日志、数据保留、区域、加密、审计、模型训练使用条款等细节。

第五，底层模型供应变化。Fugu 的优势来自可替换 agent pool，但这也意味着产品表现可能随着 pool 变化而变化。版本化、回归测试和任务级 SLA 会变得很重要。

## 对 Agent 产品的启发

Fugu 给 Agent 产品的启发主要有三点。

第一，**模型选择本身会变成模型能力**。过去我们在代码里写 router；未来可能由一个 trained orchestrator 学会任务分配。

第二，**多 agent 不一定要暴露给用户**。用户想要的是一个可靠结果，不是看到十个 agent 互相聊天。Fugu 的“single model API”是一个很强的 UX 观点。

第三，**AI sovereignty 会进入产品架构**。供应商可替换、模型池可控、provider opt-out、价格可预测，都会成为企业 agent runtime 的基础能力。

这对 QCut、OpenClaw、Hermes 这类 agent runtime 也有启发：应用层不应该只做“选模型下拉框”。更长期的设计，是把任务类型、数据敏感度、成本预算、延迟目标、可靠性要求和 provider 可用性一起输入调度系统。

## 结论

Sakana Fugu 的发布代表一种新抽象：**模型不只是回答问题，也可以负责调度模型。**

这条路线和“更大上下文”“更强 coding benchmark”“更快视频生成”不冲突，但它指向另一个竞争层：谁能把多个模型、多个 agent、多个 provider 的集体能力，稳定地包装成一个开发者愿意接入的 API。

如果说过去两年模型竞争的关键词是 scaling，那么 Fugu 想押注的关键词是 orchestration。真正的问题不只是“哪个模型最强”，而是：

- 谁能为一个任务选对模型组合？
- 谁能在长程任务里持续验证和修正？
- 谁能在供应商变化时保持产品可用？
- 谁能把多 agent 的复杂性压缩成可预测的 API、价格和合规边界？

Fugu 还需要更多第三方验证，但它已经把一个重要问题推到台前：未来的 agent runtime，可能不会只依赖一个更大的大脑，而会依赖一个会组织很多大脑的大脑。
