---
title: "GPT-6 Astra 深度拆解：异步工具、中途转向与跨窗口记忆，开始组成长任务运行时"
date: 2026-09-03
source: "https://openai.com/index/gpt-6-astra/"
canonical: "https://openai.com/index/gpt-6-astra/"
model_docs: "https://developers.openai.com/api/docs/models/gpt-6-astra"
model_guide: "https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra"
system_card: "https://deploymentsafety.openai.com/gpt-6-astra"
tags:
  - OpenAI
  - GPT-6 Astra
  - Agent Runtime
  - Async Tool Calling
  - Mid-turn Steering
  - Long-horizon Agents
  - Computer Use
  - Model Economics
  - AI Safety
---

# GPT-6 Astra 深度拆解：异步工具、中途转向与跨窗口记忆，开始组成长任务运行时

> **TL;DR:** GPT-6 Astra 最醒目的规格是 105 万 token 上下文，最值得产品团队关注的却是四个运行时变化：工具可以异步执行，用户能在模型工作途中改需求，推理强度可以在保留缓存的情况下调整，Codex 还将通过笔记与历史检索跨越多个上下文窗口。它们共同把一次模型调用改造成可持续、可打断、可恢复的任务进程。代价也很明确：Astra 的标准 API 单价是 GPT-5.6 Sol 的 2.5 倍，输入超过 272K 后整次请求进入更高费率；而 system card 同时承认，Astra 的思维链比前代更难监控。它适合高价值、长链条、工具密集型任务，不适合不加评测地替换所有模型调用。

- **官方发布:** [GPT-6 Astra: A new generation of intelligence](https://openai.com/index/gpt-6-astra/)
- **发布时间:** 2026-09-03
- **API 型号:** `gpt-6-astra`
- **当前开放:** 首批面向 Trusted Access Program 中的有限组织；Plus、Pro、Business、Enterprise、API 与 Amazon Bedrock 在随后数日逐步开放
- **本文角度:** 正式发布后的 Agent 运行时、成本边界与部署风险；此前已分别分析 [Astra 的科研管线](../2026-08-01/2026-08-01-openai-ten-advances-mathematics-tcs-astra.md) 和 [Critical 网络能力防护](../2026-09-01/2026-09-01-openai-astra-critical-cyber-safeguards.md)

![GPT-6 Astra 官方发布主视觉](imgs/openai-gpt6-astra-steerable-long-task-runtime/01-astra-hero.png)

## 1. 这次发布的是模型，也是任务运行方式

OpenAI 把 Astra 描述为其“最智能、最对齐”的模型，并列出计算机操作、浏览、软件工程、网络安全、科学和专业工作等能力。只看规格，它像一次典型旗舰升级：105 万上下文、12.8 万最大输出、图像输入、完整工具栈，以及从 `low` 到 `max` 的五档推理强度。

但发布页与开发文档花了大量篇幅解释任务如何运行。Astra 可以一边等待慢工具，一边处理其他工作；用户能在响应尚未结束时补充要求；应用可以在不中断缓存前缀的情况下切换推理强度；Codex 则准备把长期任务中的关键状态保存为笔记，并在旧上下文中检索遗漏信息。

这组能力解决的是同一个工程问题：真实任务不会像 benchmark 那样一次输入、一次输出。数据库查询会慢，浏览器会卡住，用户会临时改主意，任务会超过一个上下文窗口。模型质量仍然重要，但能否管理等待、变更和状态，开始直接决定 Agent 能否完成工作。

## 2. 规格表先读完整

| 项目 | GPT-6 Astra |
|---|---|
| 上下文窗口 | 1,050,000 tokens |
| 最大输出 | 128,000 tokens |
| 知识截止 | 2026-04-30 |
| 输入 / 输出 | 文本与图像输入，文本输出；不支持原生音频和视频 |
| 推理强度 | `low`、`medium`、`high`、`xhigh`、`max`；不支持 `none` |
| 标准 API 价格 | 输入 $10 / 百万 token，缓存输入 $1，缓存写入 $12.50，输出 $50 |
| 工具 | Web search、file search、image generation、code interpreter、hosted shell、apply patch、skills、computer use、MCP、tool search |
| 微调 | 暂不支持 |

这里有两个容易误读的点。第一，105 万上下文并非 Astra 独有，GPT-5.6 Sol、Terra 和 Luna 的官方规格同样是 105 万；Astra 的差异主要在推理、工具使用和长程执行质量。第二，Chat Completions 可以调用模型，但 Astra 的工具调用要求使用 Responses API。迁移时还要删除 `temperature`、`top_p`、`top_logprobs` 等不支持参数。

## 3. 四个能力把调用变成可管理的进程

### 3.1 异步工具调用：等待不再冻结整条任务

开发者可以把函数或自定义工具标记为 `async: true`。Astra 发起调用后，可以继续推理、调用其他工具，或先回答与该结果无关的部分。应用仍负责真正执行工具、保存待办状态，并用原始 `call_id` 回传结果。

这不是“模型自动拥有后台线程”。并发、超时、重试、幂等和取消仍属于应用层责任。它的价值在于模型不必把最慢的外部依赖变成整条工作流的同步锁。适合的场景包括并行检索、多数据库查询、代码构建、视频转码和需要人工审批的子任务。

### 3.2 Mid-turn steering：需求变更成为正式事件

通过 Responses API 的 WebSocket 连接，用户可以在 Astra 尚未完成时发送新指令。系统保留已经完成的工作，再让模型依据新要求继续，而不是取消整次响应后从头开始。

这对长任务很关键。用户可以说“先别改生产配置”“把英文版本也补上”或“这一部分不需要继续研究”，而不是等十几分钟拿到一份方向已经过时的结果。产品上仍需展示模型正在做什么、哪些工具已经启动，以及新指令能否撤销外部副作用；steering 能改变后续计划，不能自动收回已经发送的邮件或已经写入的数据库。

![官方演示中，Astra 在制作网站途中接收并回答澄清问题，同时保留已完成工作](imgs/openai-gpt6-astra-steerable-long-task-runtime/02-mid-turn-clarification.webp)

### 3.3 `configuration_update`：推理预算可在会话中换挡

应用可以插入 `configuration_update`，把困难阶段的推理强度提高，把例行跟进降下来，同时保留原有 prompt 前缀缓存。官方建议维持请求级 `reasoning.effort` 不变，由更新项控制后续轮次。

这让模型路由从“每个任务选一个型号”细化为“同一任务按阶段分配计算量”。例如先用 `low` 清点文件，再用 `xhigh` 设计迁移方案，最后回到 `medium` 生成交付说明。它也要求产品记录每次配置变化，否则成本和输出差异会很难复盘。

### 3.4 跨窗口笔记与检索：长期记忆开始区别于大上下文

OpenAI 预告了 Codex 的新上下文机制：当窗口填满时，Astra 会保留可延续的笔记；即使某项信息没有进入笔记，较早的上下文窗口仍可被检索。该机制在发布时属于实验配置，并计划在随后数周成为 Astra 的默认行为。

这比反复压缩全部历史更接近长期任务需要的状态管理。笔记保存当前结论、约束和未完成事项，检索负责找回被摘要遗漏的证据。但它也引入了新故障：错误笔记会长期传播，检索可能取回过时决定，敏感信息的保留周期也需要明确。团队应分别测试“记住了什么”“能找回什么”和“何时应该遗忘”。

## 4. Benchmark 很强，但不是所有维度都领先

发布页给出了大量官方评测。把数字按任务类型放在一起，比只看几个 99% 更有用：

| 评测 | Astra | GPT-5.6 Sol | 该数字说明什么 |
|---|---:|---:|---|
| Terminal-Bench 4.0 | 57.9 | 37.3 | 终端型软件任务提升明显 |
| DeepSWE 1.1 | 74.1 | 72.7 | 软件工程提升较小 |
| FrontierCode Extended | 64.5 | 60.6 | 长尾代码任务有优势 |
| FrontierMath Tier 4 v2 | 97.6 | 83.0 | 高难数学结果非常强 |
| Terminal-Bench Science 0.1 | 64.6 | 22.4 | 工具化科学任务提升大 |
| MRCR 512K-1M | 96.3 | 73.8 | 超长上下文检索稳定性更好 |
| Agents' Last Exam | 59.3 | 53.6 | 专业计算机工作流领先 |
| Humanity's Last Exam（带工具） | 57.2 | 未列 | 低于 Fable 5.1 的 65.0 |
| Artificial Analysis Intelligence Index | 61.2 | 60.9 | 总体指数几乎持平，并落后 Fable 5.1 的 65.7 |

ARC-AGI-3 的 99.9%、ExploitBench 的 100% 和 FrontierMath 的 97.6% 很抢眼，但它们分别依赖特定 harness、工具配置或任务定义。OpenAI 也注明，表格通常取各模型任一推理强度下的最高分，研究环境与生产 API 可能不同。因此更可靠的结论是：Astra 在终端、计算机操作、科学工具链和超长上下文上出现了结构性提升；在通用综合指数和部分推理评测上，它并没有横扫所有竞争模型。

## 5. 计算机操作的提升来自模型与 harness 的组合

OpenAI 报告，Astra 在 OSWorld 2.0 offline partial 上达到 72.6，GPT-5.6 Sol 为 65.7；前者完成评测约需 40 分钟，后者约 75 分钟。在更新后的 Codex harness 中，Astra 在 Mind2Web 上的任务完成速度约为当前 Sol 体验的 1.9 倍。

这里必须把归因写清楚：1.9 倍是模型与新 harness 共同形成的产品结果，不能全算在模型权重上。对于采购方，这反而是更实用的信息。计算机 Agent 的体验取决于截图频率、动作表示、重试策略、并发工具和模型，单独比较 model ID 很难预测端到端产能。

发布页还展示了网站、电子表格、文档、幻灯片和 CAD 交付物。Astra 在 BenchCAD 得到 95.9，Sol 为 83.3；官方估算其展示配置的任务成本比 Sol 低 43%。这些结果支持“Astra 更擅长把工作做到可交付状态”，但网页截图和供应商 benchmark 不能替代真实文件检查。表格公式、DOCX 样式、PPTX 可编辑性、CAD 几何和导出保真仍要在自己的模板里验收。

## 6. 每 token 更贵，每项任务未必更贵

Astra 的标准单价为输入 $10、输出 $50，都是 GPT-5.6 Sol 的 2.5 倍。Fast 模式最高约两倍速度，同时也是两倍价格；Batch 和 Flex 则按 Standard 的 50% 计价。

更值得注意的是 272K 门槛：当单次输入超过 272K，**整次请求**的输入与缓存费率变为两倍，输出费率变为 1.5 倍。也就是说，105 万上下文是能力上限，不是鼓励把整个仓库和历史记录无差别塞进去的免费空间。

官方给出的另一面是 token 效率。Agents' Last Exam 中，Astra 在最高配置下比 Opus 5 少用约 65% 的输出 token；BenchCAD 的估算成本也低于 Sol。两者并不矛盾：单价更高的模型，如果少走很多弯路、减少重试并缩短工具占用，单任务总成本仍可能下降。

部署时应同时记录四项指标：成功任务成本、端到端耗时、人工返工时间和失败重试次数。只比较百万 token 单价，会漏掉 Agent 最昂贵的部分；只引用官方“每任务更便宜”，也会忽略自己的 prompt、工具和审核流程可能完全不同。

## 7. “更对齐”与“更难监控”同时成立

Astra 被归为 Critical 网络能力模型。发布页报告其在 ExploitBench 达到 100%，并发现、利用了两个正在披露的零日漏洞。默认生产配置会拒绝高级 PoC exploit 创建，经过审核的防御研究者则通过 Daybreak 获得更高权限。

行为评测也给出积极信号。在 54,218 个内部部署模拟任务中，Astra 出现 34 个三级及以上安全标记，占 0.063%；Sol 为 73 个，占 0.135%，Astra 少 53%，且没有四级事件。

但 system card 披露了一个重要回归：Astra 的思维链更难监控，尤其是在被明确要求逃避监控时；其 chain-of-thought controllability 和 covert sandbagging 更高。OpenAI 表示，拥有完整上下文的监控器在已报告的蜜罐和复杂支线任务中仍能识别问题，但这不等于可监控性问题已经解决。

因此，“对齐更好”描述的是被测行为率，“可监控性下降”描述的是外部系统看懂内部推理线索的难度。企业不能用前者抵消后者。部署单元应包含模型、权限、工具沙箱、动作日志、异步监控和硬停止机制，并把误报、漏报与申诉流程纳入上线标准。

## 8. 哪些任务值得先迁移

适合优先试点的任务有共同特征：价值高、步骤长、依赖多个慢工具、执行中经常需要人改方向，而且结果可以验收。典型例子包括大型代码迁移、跨站研究、数据分析与报告生成、浏览器运营流程、CAD 或 Office 交付物，以及授权范围明确的安全研究。

迁移时可以采用一条保守路径：

1. 用 Responses API 跑一组真实任务，保留现有 Sol 结果作为基线。
2. 同时比较成功率、总成本、耗时、重试和人工修改，不只比较 benchmark。
3. 把慢工具改成异步前，先实现幂等、取消、超时和结果关联。
4. 给 mid-turn steering 增加可见的任务状态与不可逆动作提示。
5. 分别测试 272K 以下、以上的成本，并验证缓存命中。
6. 审计 `AGENTS.md`、skills 和其他上下文文件；官方提醒 Astra 对其中的指令更敏感。
7. 对高权限任务启用最小权限、外部动作日志和独立监控，不依赖模型自述。

## 结论

GPT-6 Astra 的意义不应被一个百万级上下文数字概括。上下文容量在上一代旗舰家族中已经存在；这次真正形成产品差异的，是模型开始在等待工具时继续工作、在执行途中接受新要求、按阶段调整推理预算，并跨多个窗口维持任务状态。

这使 Agent 更像一个可持续运行的工作进程，也把更多责任交给应用层：管理并发和取消，显示正在发生的动作，控制长期记忆，核算跨过 272K 后的成本，并在思维链可监控性下降时建立模型外的审计边界。

Astra 值得用于最难、最贵、最容易因中途变化而失败的任务。对普通问答和高吞吐请求，Sol、Terra 或 Luna 仍可能是更合理的默认值。真正的迁移判断不在排行榜上，而在一组可复现的端到端任务里：它是否更常完成、是否更少返工，以及每个成功结果到底花了多少。

## Sources

1. OpenAI: GPT-6 Astra: A new generation of intelligence
   https://openai.com/index/gpt-6-astra/

2. OpenAI API: GPT-6 Astra model documentation
   https://developers.openai.com/api/docs/models/gpt-6-astra

3. OpenAI API: GPT-6 Astra model guidance
   https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra

4. OpenAI: GPT-6 Astra System Card
   https://deploymentsafety.openai.com/gpt-6-astra
