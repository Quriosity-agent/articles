---
title: "GLM-5.3 深度拆解：同一个 743B 基座，Z.ai 把后训练扩展推向 Coding Agent 和网络安全"
date: 2026-08-14
source: "https://x.com/Zai_org/status/2088132965922476159?s=20"
canonical: "https://z.ai/blog/glm-5.3"
docs: "https://docs.z.ai/guides/llm/glm-5.3"
security_ledger: "https://cvd.z.ai/"
tags:
  - Z.ai
  - GLM-5.3
  - Coding Agent
  - Cybersecurity
  - Post-training
  - Long-horizon RL
  - Slime
  - Open Weights
---

# GLM-5.3 深度拆解：同一个 743B 基座，Z.ai 把后训练扩展推向 Coding Agent 和网络安全

> **TL;DR:** Z.ai 在 2026-08-14 发布 GLM-5.3，官方定位是 “Built to Code. Ready for Cyber Defense.” 这次最关键的不是换了一个更大的 base model，而是 Z.ai 明确说：GLM-5.3 使用和 GLM-5.2 相同的 743B 基座，所有增益来自 post-training scaling。它把训练环境从长程 coding 继续推到真实工程工作流、漏洞发现和利用链推理。注意一个边界：发布日权重还没有立刻放出，官方说会在发布后两周完成安全评估和加固后公开；截至 2026-08-15，文档也写着 GLM-5.3 API coming soon，但 GLM Coding Plan 用户已经可用。

- **X source:** [Z.ai announcement](https://x.com/Zai_org/status/2088132965922476159?s=20)
- **Tech blog:** [GLM-5.3: Frontier Coding with Emergent Cyber Capabilities](https://z.ai/blog/glm-5.3)
- **Docs:** [GLM-5.3 overview](https://docs.z.ai/guides/llm/glm-5.3)
- **Security ledger:** [Z.ai Security Disclosure Ledger](https://cvd.z.ai/)
- **Published:** 2026-08-14
- **Topic:** Coding agents / post-training scaling / cyber capability / long-horizon RL / open-weight release caveats

![GLM-5.3 launch card](imgs/zai-glm-53-post-training-cyber-coding-agent/01-x-launch-card.jpg)

## 一句话判断

GLM-5.3 是 GLM-5.2 路线的继续，但重点从“长上下文能不能支撑长程 agent”变成了“后训练环境能不能把模型推向真实工程和安全任务”。

仓库里之前已经写过 GLM-5.2。那篇的核心是 1M context、IndexShare、SAO、Slime、anti-hacking 和推理 serving：也就是长程 agent 不散架需要什么基础设施。

GLM-5.3 的变化更窄，也更锋利。Z.ai 这次没有讲一个新架构故事，而是强调：**Scaling post-training is all we did.** 同一个 base，通过更多环境、更复杂任务和更多训练 compute，把能力推到 coding、agentic workflow 和 cyber defense。

这句话如果成立，说明竞争点正在从“谁有更大的基座模型”往“谁有更可执行、可验证、可扩展的训练环境”迁移。

## 发布日最容易误读的一点：开放权重，但不是当天可下载

X 原帖说 GLM-5.3 有 top-tier coding and agentic capabilities，并且这些能力来自对 743B base model 的 post-training。博客里还说它会 release weights，但时间点是 launch 后两周，前提是安全评估和 hardening 完成。

所以这篇不能把 GLM-5.3 写成“已经开源可本地部署”。更准确的状态是：

| 项目 | 发布日状态 |
|---|---|
| GLM Coding Plan | 已向订阅用户 rollout |
| ZCode / coding agents | 官方建议在 ZCode、Claude Code、OpenCode 等 agent 中使用 |
| 标准 GLM-5.3 API | 文档写着 coming soon |
| 本地权重 | 官方承诺发布后两周公开 |
| 上下文 / 输出 | 文档列出 1M context、128K maximum output tokens |

这对使用者很重要。它现在更像“产品/订阅入口优先，权重延迟释放”的发布，而不是 Hugging Face model card 先行。

## Benchmark 不是故事，故事是训练环境

官方给了大量 public benchmark 数字。值得看，但不能只看排名。

![GLM-5.3 benchmark overview](imgs/zai-glm-53-post-training-cyber-coding-agent/02-glm-53-benchmark-table.webp)

几个最能说明 GLM-5.3 相比 GLM-5.2 变化的数字：

| Benchmark | GLM-5.2 | GLM-5.3 | 变化信号 |
|---|---:|---:|---|
| Terminal-Bench 3.0 | 4.6 | 28.3 | 终端型长程任务显著提升 |
| DeepSWE v1.1 | 46.2 | 66.9 | 容器内软件工程任务更强 |
| Agents' Last Exam CLI | 23.8 | 28.5 | 通用 agent task 有提升 |
| AutomationBench v1.0.6 | 26.2 | 48.2 | 自动化任务跃迁明显 |
| CyberGym | 77.2 | 84.5 | 漏洞发现 benchmark 提升 |
| ExploitBench | 24.4 | 54.4 | 利用链推理能力翻倍级提升 |
| ExploitGym 2h / 6h | 29 / 39 | 105 / 130 | 时间预算下完成更多 exploitation task |

这些数字的解释要加 caveat。官方 footnotes 里大量 benchmark 都跑在特定 harness 下，例如 Claude Code 2.1.207、mini-swe-agent、官方 evaluator、不同 context 和 max output 设置。模型能力、agent harness、工具权限、容器、timeout、反作弊策略会混在一起。

但趋势仍然清楚：GLM-5.3 的增益主要落在执行型、长程型、带工具和环境反馈的任务上，而不是普通短题 coding。

## 私有 Code Bench 的价值和风险

Z.ai 还引入了自家的 Z.ai Code Bench，用来评估 coding agent 在真实用户场景下的表现。它看两个维度：end-to-end task completion rate 和 fine-grained checklist accuracy。

![Z.ai Code Bench effort comparison](imgs/zai-glm-53-post-training-cyber-coding-agent/03-zai-code-bench-effort.webp)

官方报告了几个很强的数字：

- Max effort 下，GLM-5.3 达到 34.5%，约 75K output tokens / task；
- GLM-5.2 是 23.4%，约 96K output tokens / task；
- High effort 下，GLM-5.3 达到 31.4%，约 50K output tokens；
- 同图中 Claude Opus 4.8 为 29.5%，约 120K output tokens；
- GLM-5.3 仍落后 Claude Fable 5，后者 Max effort 达到 39.5%。

这个图真正有用的不是“谁赢了谁”。私有 benchmark 无法让外部复现，也可能和产品使用场景更贴近。它的价值在于 Z.ai 把 **accuracy / output token cost / effort level** 放在同一张图里。

Coding agent 的下一阶段不是单纯“模型更聪明”，而是“在给定 token、时间、成本和验证条件下，能否把任务推进到可交付状态”。Z.ai Code Bench 正在测这个维度。

## Cyber capability：从找 bug 到推进利用链

GLM-5.3 最值得单独写的，是 cyber 部分。Z.ai 说他们在 post-training 中加入了 vulnerability discovery data 和 environments，结果超出预期：模型不只是更会识别孤立漏洞，而是开始跨多个 exploitation stages 形成更连贯的计划。

![GLM-5.3 cyber benchmark](imgs/zai-glm-53-post-training-cyber-coding-agent/04-cyber-benchmark.webp)

官方给出的三组结果分别对应不同阶段：

| Benchmark | 测什么 | GLM-5.3 的官方结果 |
|---|---|---|
| CyberGym | 白盒源码环境中识别、验证漏洞并触发 fault | 84.5% |
| ExploitBench | 对真实漏洞做更深入的利用推理 | 54.4% |
| ExploitGym | 在 2h / 6h 预算内完成 exploitation tasks | 105 / 130 |

这里要保持克制。GLM-5.3 在 CyberGym 上领先 Mythos 5 和 GPT-5.6 Sol 一点点，但在 ExploitBench 和 ExploitGym 上仍明显落后闭源前沿。Z.ai 自己也承认：越往利用链深处走，和 closed frontier 的差距越大。

真正值得注意的是方向：cyber 能力不是孤立地“会读 CVE”，而是和 long-horizon agent training 共享一套能力结构，包括搜索代码、构造假设、运行验证、修改 payload、观察反馈、继续迭代。这正是安全任务危险也有价值的地方。

## Security Disclosure Ledger 是这次发布里最不该忽略的部分

博客里还有一块非常具体：Z.ai 说自 GLM-5.2 以来，他们和中国多家安全团队合作，把模型用于真实代码库，在专家审查、筛选和去重后，识别出 2,436 个漏洞，覆盖 269 个项目；披露账本当前把其中 1,097 个标为 critical/high。

Z.ai 还上线了 [Security Disclosure Ledger](https://cvd.z.ai/)。页面当前显示：

| 指标 | 数值 |
|---|---:|
| 已收录漏洞 | 2,436 |
| 已公开 | 53 |
| 未公开 / embargo | 2,383 |
| 严重及高危 | 1,097 |
| 覆盖开源项目 | 269 |
| 影响时间跨度 | 45 年 |

这个 ledger 的意义比一个 benchmark 分数更大。因为 cyber agent 一旦能真实发现漏洞，关键问题就不是“模型分数多少”，而是披露流程、专家复核、去重、CVE、厂商协调、embargo、滥用风险和审计记录。

也就是说，GLM-5.3 的 cyber 发布不是单纯能力展示，而是把模型能力接到一个 disclosure workflow 里。这个工作流现在还需要大量人工和制度约束，但方向是对的：安全 agent 的产物不能只停在 demo，它必须进入负责披露的管道。

## Slime 的角色：训练环境变成可插拔数据流

GLM-5.3 继续建立在 Z.ai 的 open-source post-training framework [slime](https://github.com/THUDM/slime) 上。博客说，slime 用 Megatron 作为训练侧，SGLang 作为 rollout 侧，把 training、rollout 和 data buffer 放进同一条 dataflow。

这背后的产品含义是：长程 RL 不再是“拿一批 prompt 训练模型”，而是把 math、code、sandbox、verifier、agentic environments 都当作数据生成模块接进去。

GLM-5.3 还提到几个工程优化：

- top-p mask、top-k / full-vocabulary OPD；
- R3-style setup 和训练-推理 logprob 对齐；
- 平均 logprob difference 控制到 `1e-7` 级；
- local storage 作为额外 cache layer；
- 多 teacher OPD 的 dynamic teacher switching 和 prefetch；
- router 与 slime 的联合调度、负载均衡；
- long-horizon coding RL 端到端训练 throughput 提升 2.3x 以上。

这些细节看起来不像发布会 headline，但它们决定了“训练更多真实环境”能不能规模化。没有这层系统能力，post-training scaling 只会卡在环境构建和 rollout 成本上。

## API 迁移：thinking 不能关了

对开发者来说，GLM-5.3 还有一个直接兼容性变化：官方文档说它支持三档 thinking effort：

- `low`
- `high`
- `max`

但 `thinking.type: "disabled"` 不再支持。也就是说，如果现有应用依赖关闭 thinking，需要先改成：

```json
{
  "model": "glm-5.3",
  "thinking": { "type": "enabled" },
  "reasoning_effort": "low"
}
```

然后再切模型 ID。官方明确说，否则 request will fail。

这再次说明一个趋势：reasoning effort 已经变成模型产品的 API contract、成本控制和调度接口。对 coding agent 来说，`max` 是官方推荐；对普通集成来说，`low` 可能才是迁移起点。

## 对 agent 产品的启发

GLM-5.3 给 agent 产品团队的启发主要有五个：

1. **环境比题库更重要。** 真正推动能力的不是更多 LeetCode，而是可执行、可验证、贴近真实工作的 long-horizon environments。
2. **评测要同时看质量和成本。** Output tokens、effort level、timeout、harness 和 verifier 都是模型能力的一部分。
3. **安全能力需要流程承接。** Cyber agent 的输出必须进入 disclosure ledger、专家复核和 embargo 管道。
4. **开放权重不等于当天可用。** 743B 级模型就算放权重，部署和 serving 仍是基础设施问题。
5. **thinking 是产品旋钮。** 不能把 reasoning effort 当成内部细节，它会影响价格、延迟、成功率和迁移风险。

如果 GLM-5.2 的重点是“agent 怎么工作更久”，GLM-5.3 的重点就是“agent 在更真实、更危险、更长链路的环境里怎么训练和验收”。

## 最后

GLM-5.3 不是一次“新基座模型发布”，更像一次后训练基础设施的阶段性结果展示。

它把同一个 743B base 继续往长程 coding 和 cyber defense 推，数字上很亮眼，但真正的变量是环境、验证器、反作弊、披露流程和成本控制。未来开放模型能不能继续追近闭源前沿，很可能不只取决于参数规模，而取决于谁能持续生产高质量、可验证、难作弊、贴近真实工作的训练环境。
