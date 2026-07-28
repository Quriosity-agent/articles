# Kimi K3 深度拆解：开源 3T 模型的真正变量，是长程 Agent 的运行成本与控制面

> **TL;DR:** Kimi K3 最值得关注的不是“2.8T 参数”这个最大模型叙事，而是 Moonshot 把开源权重、1M 上下文、原生视觉、Kimi Code / Kimi Work / API 和自动缓存放进同一个长程 Agent 运行时里。它官方承认整体体验仍落后于 Claude Fable 5 和 GPT-5.6 Sol，完整权重要到 2026-07-27 才释放，技术报告也还没发；但它已经把开源模型的竞争点从“能不能做题”推到“能不能连续跑仓库、文档、表格、视觉反馈和工具链”。

> **更新（2026-07-27）：** 完整权重和技术报告已经发布，部署与许可证审计见 [Kimi K3 权重发布审计](../2026-07-27/2026-07-27-kimi-k3-open-weight-release-agent-state-infrastructure.md)。本文保留首发时点的产品与运行时判断。

- **Source:** [Kimi K3: Open Frontier Intelligence](https://www.kimi.com/blog/kimi-k3)
- **API docs:** [Kimi K3 Quickstart](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart)
- **Model list:** [Kimi API Model List](https://platform.kimi.ai/docs/models)
- **Pricing:** [Flagship Model Kimi K3 Pricing](https://platform.kimi.ai/docs/pricing/chat-k3)
- **Published:** 2026-07-17
- **Tags:** Kimi K3 / Moonshot AI / Open Weight / 3T Model / Agent Runtime / Long Context / Coding Agent / Kimi Code / Kimi Work

![Kimi K3 hero](imgs/kimi-k3-open-frontier-intelligence/01-kimi-k3-hero.webp)

## 1. K3 的重点不是“大”，而是把大模型放进长程 Agent 运行时

官方把 Kimi K3 定义为 2.8T 参数、原生视觉、1M token 上下文的 open 3T-class 模型。这个数字当然重要：它把开源权重模型推到接近闭源 frontier 的参数规模。但如果只看“世界最大开源模型”，会错过 K3 更实际的变化：它不是孤立发布一个 checkpoint，而是直接进入 Kimi.com、Kimi Work、Kimi Code 和 Kimi API。

这说明 Moonshot 这次卖的不是一个聊天模型，而是一整套 Agent 运行面：

1. **Kimi Code** 承接长程工程任务，模型要能理解大仓库、调用终端、读日志、跑测试、根据截图迭代。
2. **Kimi Work** 承接知识工作，模型要把 PDF、网页、表格、图表、幻灯片和交互式可视化接成项目。
3. **Kimi API** 承接开发者集成，模型名是 `kimi-k3`，默认总是在 thinking mode，启动时只支持 `reasoning_effort="max"`。
4. **1M 上下文 + 自动缓存** 承接成本控制，长前缀复用时自动尝试 cache hit，不要求开发者显式管理 cache ID。

K3 的真正问题因此不是“它是不是比某个闭源模型聪明 2%”，而是：一个开源权重模型能不能在真实 Agent 工作流里承担足够长的上下文、足够多的工具调用、足够稳定的视觉反馈循环，以及足够可预测的成本。

## 2. 公开 benchmark 要按 harness 读，不要按榜单读

官方图表里，Kimi K3 在 coding、general agents、visual agents、knowledge work 等多组任务上给出了强势结果。尤其是 coding 部分，它强调 long-horizon coding、GPU kernel optimization、MiniTriton 编译器、游戏开发、芯片设计和 research coding 这些多小时级任务，而不是只展示短题。

![Kimi K3 coding benchmarks](imgs/kimi-k3-open-frontier-intelligence/02-kimi-k3-coding-benchmarks.webp)

但这类 benchmark 不能被读成“同一模型裸跑同一题”。官方脚注很关键：Kimi K3 的结果都在 max reasoning effort 下获得，不同 benchmark 会使用 KimiCode、Claude Code 或 Codex 等不同 agentic harness。比如 Terminal-Bench、SWE Marathon、FrontierSWE、KCB 2.0、OfficeQA Pro、SpreadsheetBench 2 等，都涉及不同的工具封装和执行环境。

这意味着这些结果更像是在比较“模型 + 工具运行时 + 上下文策略 + 默认策略”的组合，而不是纯模型能力。对开发者来说，这反而更有用：你不会把一个模型直接接到空气里，而是接进 CLI、IDE、CI、浏览器、文档系统和内部工具。K3 的价值要在这个组合层验证。

![Kimi K3 agent and vision benchmarks](imgs/kimi-k3-open-frontier-intelligence/03-kimi-k3-agent-vision-benchmarks.webp)

官方对 BrowseComp 的说明也值得单独看：它采用类似 Claude model cards 的 context compaction 策略，在 300K tokens 触发；如果用 1M token context 且不做 context management，Kimi K3 官方声称能到 90.4。这里真正的变量不是“搜索题分数”，而是长上下文、压缩策略和 agent 状态保真之间的权衡。

![BrowseComp cost curve](imgs/kimi-k3-open-frontier-intelligence/05-browsecomp-cost-curve.webp)

## 3. 架构路线：KDA、AttnRes 和 16/896 experts 是为了让长程任务可服务

K3 的架构关键词包括 Kimi Delta Attention、Attention Residuals、Stable LatentMoE、Gated MLA、SiTU、Per-Head Muon 和 Quantile Balancing。官方给出的核心解释是：KDA 和 AttnRes 改善长序列与深层网络中的信息流，Stable LatentMoE 让模型在 896 个专家里激活 16 个，训练和数据配方一起带来相对 Kimi K2 约 2.5x 的 overall scaling efficiency。

这套说法在技术报告发布前还只能当作 release-claim 读，但方向很明确：K3 不是只靠堆参数，而是在争取把大规模 MoE 做成可训练、可推理、可缓存、可服务的系统。

![Kimi K3 expert routing](imgs/kimi-k3-open-frontier-intelligence/07-kimi-k3-expert-routing.webp)

这也是开源权重模型最容易被误读的地方。2.8T 参数开源，并不等于普通团队可以在几张卡上舒服自托管。官方文档建议 K3 部署在 64 张或更多加速器组成的 supernode 配置上；同时，因为 KDA 给传统 prefix caching 带来新问题，Moonshot 表示会向 vLLM 社区贡献对应实现。也就是说，开放权重只是第一层，真正的生产门槛在 serving。

## 4. 成本曲线比参数规模更接近生产问题

官方 API 价格是：cache-hit input $0.30 / MTok，cache-miss input $3.00 / MTok，output $15.00 / MTok。文档强调 K3 的 1M token context 不按上下文长度分层收费，而是 flat pay-as-you-go；在 coding workloads 中，官方 API 声称 cache hit rate 超过 90%。

![Kimi Code Bench cost curve](imgs/kimi-k3-open-frontier-intelligence/04-kimi-code-bench-cost-curve.webp)

这组价格的含义很微妙。K3 不是廉价小模型路线，输出价格已经进入 frontier 模型预算区间；但如果长仓库、长文档、长任务可以稳定命中缓存，实际成本会更接近“第一次读入昂贵，后续迭代便宜”的项目型计费。

这对 Agent 产品非常关键。长程 Agent 的成本不是单次 prompt，而是一个 session 里反复读取仓库、计划、改代码、跑测试、看截图、修 bug、整理报告的总成本。K3 想证明的是：1M context + automatic caching + Kimi Code harness 可以让大型上下文任务从“每次重新读世界”变成“维护一个可复用工作记忆”。

## 5. Kimi Work 的信号：知识工作正在变成可交互项目，而不是报告生成

K3 launch page 里另一个容易被 benchmark 掩盖的部分，是 Kimi Work 的案例：42 年 AI ASIC 行业研究网站、fusion industry report、GWTC-5 gravitational-wave analysis、infographic-style presentations、Widgets 和 Dashboard。

![Kimi K3 internal knowledge work bench](imgs/kimi-k3-open-frontier-intelligence/06-internal-knowledge-work-bench.webp)

这些例子说明 Moonshot 正在把“知识工作”定义成更宽的输出形态：不是只交一份 Markdown 报告，而是交互式网页、可视化、可编辑图表、可持续更新的 widget，以及围绕主题组织的 dashboard。

这和 K3 的原生视觉、长上下文、工具调用是同一件事。知识工作 Agent 最难的不是写一段漂亮摘要，而是保持项目状态：资料从哪里来、图表如何生成、数据是否可追溯、用户下一轮修改会影响哪些组件、dashboard 怎样持续更新。K3 的产品包装把这些状态管理能力推到了前台。

## 6. 上线限制比发布口号更值得抄进 AGENTS.md

K3 官方限制写得很具体，开发者应该直接把其中几条转成系统提示和 harness 约束。

第一，K3 对 thinking history 敏感。文档要求多轮对话和工具调用时，把 API 返回的完整 assistant message 带回下一轮，而不是只保留 `content`。官方还提醒：如果 harness 没有正确传回历史 thinking content，或者一个进行中的 session 从别的模型切到 K3，生成质量可能变得很不稳定。

第二，K3 可能过度主动。官方说它的训练特别强调长程挑战任务，所以遇到小问题或模糊意图时，可能替用户做出意外决定。如果你的场景要求 Agent 严格待在边界内，应该在 system prompt 或 `AGENTS.md` 里写清楚约束。

第三，API 还有几个实际限制：启动时 `reasoning_effort` 只有 `max`；`max_completion_tokens` 默认 131072，最高 1048576；temperature、top_p、n、presence_penalty、frequency_penalty 是固定值；vision input 不支持 public image URLs，需要 base64 或 `ms://<file-id>`；web search 正在更新，官方不建议近期用于生产。

这些限制不是小字。它们决定了 K3 能否被稳定接进现有 Agent 产品：历史状态怎么存、工具消息怎么回放、模型切换怎么做、模糊任务能不能自动继续、视觉输入如何上传、搜索功能是否要外置。

## 7. 真正的判断标准：等权重，也等报告，更要等自己的任务

K3 发布时，官方自己也给了两个冷静信号：完整模型权重要到 2026-07-27 才释放，架构、训练和评估细节要等 K3 technical report；同时它承认整体用户体验仍然和 Claude Fable 5、GPT-5.6 Sol 存在明显差距。

所以这不是一个可以马上盖棺定论的模型。更合理的判断方式是三层：

1. **权重层**：等完整权重、license、推理框架支持、量化方案和 vLLM KDA cache 实现落地。
2. **运行时层**：用 Kimi Code / Claude Code / OpenHands / 自己的 harness 跑同一批长程任务，区分模型能力和工具系统能力。
3. **经济层**：按真实 session 计算 cache hit、输出长度、失败重试、人工接管和 GPU/云 API 成本。

Kimi K3 的意义，不是证明开源模型已经完全超过闭源 frontier，而是把开源模型第一次放到了一个足够接近 frontier Agent 工作流的位置：会写代码、会看图、会长时间保持上下文、会接工具、会进入桌面工作台，也会暴露 serving 和 harness 的全部复杂性。

如果说 K2.5 的故事是“开源模型也能做多模态 Agent”，K3 的故事就是“开源模型开始竞争长程 Agent 的运行系统”。接下来要看的不是发布页上谁赢了几分，而是哪一种模型栈能在真实工作里连续跑十小时，还能让成本、边界和错误都被人看得见。
