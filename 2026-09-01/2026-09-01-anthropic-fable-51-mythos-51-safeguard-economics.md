---
title: "Claude Fable 5.1 / Mythos 5.1 深度拆解：同一模型开始按安全权限、缓存经济与数据主权分层"
date: 2026-09-01
source: "https://x.com/dotey/status/2094854620732375335?s=20"
canonical: "https://www.anthropic.com/claude-fable-and-mythos-5-1"
efs: "https://www.anthropic.com/news/enterprise-frontier-safeguards"
tags:
  - Anthropic
  - Claude Fable 5.1
  - Claude Mythos 5.1
  - Agent Economics
  - Prompt Caching
  - Enterprise AI
  - Data Retention
  - AI Safety
---

# Claude Fable 5.1 / Mythos 5.1 深度拆解：同一模型开始按安全权限、缓存经济与数据主权分层

> **TL;DR:** 宝玉的长帖准确抓住了这次发布最有现实意义的三条线：性能、成本和数据留存。但 Fable 5.1 / Mythos 5.1 更深一层的信号是，前沿模型的“产品分级”正在改变。它们是同一个底层模型；Fable 5.1 通过更严格的网络安全与生物安全护栏面向大众，Mythos 5.1 则通过审核制向专业研究者开放更宽的能力边界。与此同时，Anthropic 没有降低输入输出单价，而是把 cache read 降价 75%，专门改善长上下文 Agent 的单位经济；Enterprise Frontier Safeguards 又把安全监控日志放进客户控制的云环境，试图把模型安全与企业数据主权同时做成基础设施。

- **X 来源:** [宝玉：Claude Fable 5.1 与 Mythos 5.1 发布解读](https://x.com/dotey/status/2094854620732375335?s=20)
- **官方发布:** [Claude Fable 5.1 and Mythos 5.1](https://www.anthropic.com/claude-fable-and-mythos-5-1)
- **Fable 产品页:** [Claude Fable](https://www.anthropic.com/claude/fable)
- **Mythos 产品页:** [Claude Mythos](https://www.anthropic.com/claude/mythos)
- **企业安全方案:** [Enterprise Frontier Safeguards](https://www.anthropic.com/news/enterprise-frontier-safeguards)
- **发布时间:** 2026-09-01

![Terminal-Bench-Science accuracy versus cost](imgs/anthropic-fable-51-mythos-51/01-terminal-bench-science-cost.jpg)

## 1. 一句话判断

这不是一次普通的“5.0 到 5.1”升级。Anthropic 正在把模型能力、安全权限、推理预算、缓存价格和企业日志架构组合成同一个产品系统。

过去模型分层主要靠三个维度：大模型更聪明、小模型更快、不同档位价格不同。Fable 5.1 和 Mythos 5.1 则展示了另一种分层方式：**底层模型相同，但可访问的能力边界不同。**

Fable 5.1 是 generally available 版本，针对网络安全、生物和化学高风险任务部署更严格的 safeguards；Mythos 5.1 面向经过审核的网络防御和生命科学组织，允许更专业、更敏感的研究工作。两者之间的差距不是简单的“参数更多”或“推理更久”，而是部署政策、访问资格和安全路由共同形成的能力差。

这意味着以后比较模型时，不能只问“它是什么模型”，还要问：用了哪个安全配置、哪些任务会被路由到别的模型、账号属于哪个访问计划、数据需要保存多久、推理 effort 是多少。

## 2. 同一模型，两套权限边界

Anthropic 明确说，Claude Fable 5.1 和 Claude Mythos 5.1 是同一个模型。Fable 5.1 是带有大众部署护栏的版本；Mythos 5.1 则为 vetted organizations 提供更宽松的网络安全和生命科学权限。

| 维度 | Fable 5.1 | Mythos 5.1 |
|---|---|---|
| 底层模型 | 与 Mythos 5.1 相同 | 与 Fable 5.1 相同 |
| 访问范围 | Pro、Max、Team、Enterprise 与 API 用户 | 受审核的网络防御和生命科学组织 |
| 网络安全 | 可发现源码漏洞；渗透测试、exploit generation、二进制漏洞扫描仍受限或路由 | 面向合资格防御研究提供更宽权限 |
| 生命科学 | 研究级生物与化学问题仍会受限或路由 | 通过 Life Sciences Verification Program 开放专业能力 |
| 默认数据留存 | Fable 级模型默认 30 天，合资格企业可走 EFS / 过渡期 ZDR | 默认接受 30 天安全监控留存 |
| 价格起点 | 输入 $10 / MTok，输出 $50 / MTok | 输入 $10 / MTok，输出 $50 / MTok 起 |

这套结构比“公开版 / 专业版”更值得注意。Anthropic 实际上把安全层变成了模型产品的一部分：同一组权重可以因为护栏、fallback、访问审核和审计要求不同，在真实任务里表现出不同能力。

官方 benchmark 也承认这个变量。Terminal-Bench 4.0 上，Fable 5.1 为 55.8%，Mythos 5.1 为 60.9%。Anthropic 把差距归因于 Fable 的 safeguards 在部分网络安全任务上介入。换句话说，这个分数不只是“模型智力”，也测到了部署政策。

## 3. 跑分提升很大，但 benchmark 里混着安全系统

官方表格中，Fable 5.1 相比 Fable 5 的几个主要结果是：

| 任务 | Fable 5.1 | Fable 5 | Opus 5 | GPT-5.6 Sol |
|---|---:|---:|---:|---:|
| Terminal-Bench-Science 0.1 | 52.6% | 24.7% | 29.0% | 22.4% |
| Terminal-Bench 4.0 | 55.8% | 42.0% | 52.3% | 37.3% |
| AutomationBench | 31.4% | 17.1% | 26.9% | 19.6% |
| CursorBench 3.2.0 | 73.4% | 70.5% | 70.0% | 67.2% |
| OSWorld 2.0 strict | 41.7% | 36.1% | 39.6% | - |

![Fable 5.1 benchmark table](imgs/anthropic-fable-51-mythos-51/02-benchmark-table.jpg)

Terminal-Bench-Science 从 24.7% 到 52.6% 的提升最醒目，也支持“科研 Agent 能力明显增强”的判断。但这里有三条 caveat：

1. 这些是 Anthropic 公布的 release evaluations，不是独立复现。
2. Terminal-Bench-Science 的单模型标准误差约为 3.5 到 4.5 个百分点，细小差距不应被过度解释。
3. Fable 5.1 以 production safeguards 运行。部分任务被护栏拦截时计零分，另一些任务会 fallback 到 Opus 4.8 或 Opus 5。因此表格衡量的是“模型 + 护栏 + 路由”的部署系统，不是纯权重能力。

这个区别对实际采购反而更有用。企业买到的本来就不是裸模型，而是一个带安全策略、路由、限额和审计的服务。问题只是 benchmark 应该把这些条件写清楚，不能把所有差异都归因于模型本身。

## 4. Effort level 正在变成 Agent 的计算预算旋钮

Fable 5.1 提供 Low、Medium、High、XHigh 和 Max 五档 effort。官方图显示，Fable 5.1 在较低 effort 下就能达到或超过 Fable 5 较高 effort 的效果。

这对 Agent 产品比“最高分”更重要。长任务的成本来自大量循环：读上下文、调用工具、检查输出、处理失败、继续下一步。如果每一步都固定使用最高推理预算，benchmark 可能漂亮，但产品的吞吐和毛利很难成立。

更合理的工程模式是按阶段分配预算：

1. 搜索、分类、文件整理等可快速验证步骤使用 Low / Medium。
2. 架构判断、根因分析、科研推理等高价值步骤升到 High / XHigh。
3. Max 留给少数真正困难、失败代价高的节点。
4. 用自动评估决定是否升级 effort，而不是整条 workflow 固定一档。

Fable 5.1 的性能曲线说明，模型厂商正在把“多想多久”从内部推理参数变成产品控制面。未来 Agent 优化不只是在模型之间路由，也会在同一模型的 effort levels 之间路由。

## 5. 真正的降价发生在缓存，不在输入输出

宝玉指出“缓存读取便宜了 75%”，这是这次发布中最容易被低估、但对 Agent 开发最直接的变化。

Fable 5.1 的输入价格仍为每百万 token 10 美元，输出仍为 50 美元。改变的是 cache read：从每百万 token 1 美元降到 0.25 美元。

![Indexed cost of Fable usage](imgs/anthropic-fable-51-mythos-51/03-indexed-workload-cost.png)

Anthropic 用 2026 年 8 月四周的实际 usage，在默认 effort 下估算：典型 workload 的总成本约降 25%，context-heavy、tool-heavy 的高度 Agent 化 workload 最多约降 45%。这不是所有调用都自动便宜 45%，而是一个高度依赖缓存命中率的结果。

它揭示了 Agent 经济的一个关键事实：当系统提示词、代码库摘要、工具定义、历史对话和项目状态不断被重复读取时，**有效成本取决于缓存结构，而不只是 input/output list price。**

所以团队评估 Fable 5.1 时，应该记录：

- 总输入 token 与 cached token 的比例；
- cache write 和 cache read 的真实费用；
- 长任务每一步重复注入了多少上下文；
- 不同 effort 下的成功率、token 数和 wall time；
- 单个“完成并通过验收的任务”成本，而不是单次 API 调用成本。

如果 Agent 每轮都改写大段前缀、导致缓存失效，75% 的 cache read 降价不会自动转化成 45% 的账单下降。

## 6. EFS 不是“完全不存数据”，而是把日志主权交还客户

Fable 5 发布后的企业阻力来自 30 天 data retention。Anthropic 的理由是，高级滥用可能跨越多个 session 和账号，无法只分析单条交互后立即丢弃数据。但金融、医疗、法律、政府等行业很难接受模型供应商持有敏感日志。

Enterprise Frontier Safeguards（EFS）的解法不是取消监控，而是重新划分监控架构：

1. 自动系统在 rolling window 中分析 Agent traffic。
2. 活动日志存储在客户控制的云环境。
3. 客户控制密钥、访问策略与审计日志。
4. 告警直接交给客户自己的安全团队。
5. 默认不需要 Anthropic 员工做人工审核。

Anthropic 表示，EFS 与 100 多家客户以及 AWS、Google Cloud、Microsoft Azure 共同开发，并将支持 Claude Code、Claude Enterprise、Claude Platform、Amazon Bedrock、Google Agent Platform 和 Microsoft Foundry，计划从 2026 年秋季起分阶段上线。

这里要准确理解“ZDR”。EFS 提供的是接近 provider-side zero data retention 的隐私边界：Anthropic 不持有日志，客户控制存储、密钥、访问和人工复核。但为了跨时间检测滥用，活动数据仍可能在客户自己的云账户中保留。它不是“系统里完全没有日志”，而是“日志不在模型供应商手里”。

对企业采购来说，这比一条隐私承诺更具体，因为它把数据位置、密钥归属、审计责任和人工访问权限变成可审查的架构。与此同时，EFS 仍是分阶段发布、仅面向合资格客户的方案，不能把发布公告当成所有客户已经默认获得的能力。

## 7. 安全控制开始深入 API 行为

这次发布还有两项容易被性能叙事盖住的变化。

第一是 anti-distillation。新注册 API 账号不能再在多轮对话中手动修改 Claude 之前的上下文，同时保留此前 thinking transcript。Anthropic 把这描述为封堵一种公开的蒸馏方法。现有账号暂时不受影响，但未来模型会逐步应用。

第二是文本 watermark。由于 Anthropic 在 2026 年 7 月签署欧盟 AI 法案的 AI 生成内容透明度实践准则，8 月 2 日之后发布的模型输出带有不可见水印。检测 API 目前是有限 private preview，面向监管、媒体、事实核查、研究和有相应合规义务的企业。

这两件事说明，模型治理正在从“拒绝哪些 prompt”延伸到 API 状态是否可编辑、thinking 如何保留、输出如何被识别。对依赖上下文改写、会话重放或自定义代理协议的开发者来说，这些接口约束和模型能力同样需要测试。

## 8. 科研展示说明了什么，又没有说明什么

Anthropic 用三类科研案例展示 Fable 5.1 / Mythos 5.1：

1. Fable 5.1 用 NASA Magellan 雷达数据，为金星约三分之一表面生成更高分辨率 elevation map，并以 Creative Commons 许可发布。
2. Mythos 5.1 在 12 个蛋白靶点上做 binder design，hit rate 接近 50%；三个竞赛靶点的结合亲和力超过既有最佳提交约 10 倍，并由外部实验验证。
3. Mythos 5.1 为七个开源蛋白质与基因组模型编写 GPU kernels、缓存中间结果，把推理加速到最高 2.5 倍，估算 genome-wide analyses 的 GPU 成本可降 30% 到 60%。

这些结果比“模型会回答科学问题”更进一步，因为包含公开地图、湿实验和 identical-output 性能优化。但它们仍主要来自 Anthropic 的发布材料；蛋白设计需要继续经过成药性和生物学验证，计算优化代码也尚待官方承诺的开源与独立复现。

更稳妥的结论是：Fable 5.1 / Mythos 5.1 正在把通用推理、代码执行、专业工具和长任务 orchestration 结合成科研 Agent。它们展示了可以加速的环节，不等于已经端到端替代科学研究。

## 9. 对 Agent 团队的实际清单

如果要评估 Fable 5.1，不应只把现有模型名替换掉。至少需要重新跑以下检查：

1. **按真实 workflow 测成本。** 同时记录 cache hit、effort、wall time、工具调用和最终验收通过率。
2. **确认 safeguards 与 fallback。** 网络安全、生物、化学任务可能由不同模型完成，日志里应保留实际执行模型。
3. **建立 effort routing。** 把 Max 当升级路径，而不是默认值。
4. **审查数据留存资格。** 区分默认 30 天留存、过渡期 ZDR 和正式 EFS，不要只看营销名称。
5. **测试 API 状态兼容性。** 尤其是会修改历史消息、保留 reasoning 或重放会话的 agent harness。
6. **独立复现关键任务。** 发布 benchmark 只能做筛选，生产决策要用自己的代码库、文档、权限和验收标准。

## 结论

Fable 5.1 的性能提升当然重要，但这次发布更值得记住的是三个产品方向。

第一，同一个前沿模型可以通过 safeguards、fallback 和审核计划形成不同能力层，模型版本号不再足以描述实际可用能力。第二，Agent 成本的核心变量开始从 token 单价转向缓存命中率和 effort routing。第三，企业安全不再只靠“供应商承诺不看数据”，而是把日志、密钥、审核和告警责任写进客户控制的基础设施。

所以 Fable 5.1 / Mythos 5.1 不只是又一轮模型榜单更新。它更像前沿模型产品化进入下一阶段：能力、风险、成本和数据治理开始被放在同一张系统设计图里。

## Sources

1. 宝玉 X 长帖：Claude Fable 5.1 与 Mythos 5.1 发布解读
   https://x.com/dotey/status/2094854620732375335?s=20

2. Anthropic: Claude Fable 5.1 and Mythos 5.1
   https://www.anthropic.com/claude-fable-and-mythos-5-1

3. Anthropic: Claude Fable
   https://www.anthropic.com/claude/fable

4. Anthropic: Claude Mythos
   https://www.anthropic.com/claude/mythos

5. Anthropic: Developing Enterprise Frontier Safeguards with our customers
   https://www.anthropic.com/news/enterprise-frontier-safeguards
