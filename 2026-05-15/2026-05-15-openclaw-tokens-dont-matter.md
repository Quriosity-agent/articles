# 如果 Tokens 不重要，软件团队会怎么组织？从 OpenClaw 的“100 个 Codex”工作流看 Agent-Native SDLC

> **TL;DR**：Peter Steinberger 在 X 上回应外界对 AI spend 的讨论时，给出了一个比“花了多少钱”更重要的问题：**如果 tokens 不再是主要约束，我们会怎样构建软件？** 他描述的 OpenClaw 工作流不是“一个聊天机器人帮忙写代码”，而是一套 agent-native SDLC：约 100 个 Codex 在云端并行跑，覆盖 PR/issue review、安全审查、issue 聚类、垃圾评论处理、性能回归、会议到 PR、Crabbox 复现场景、Clawpatch 语义切分和安全审计。真正的信号不是“烧 tokens”，而是软件组织的瓶颈从人力时间，转向调度、验证、权限、成本上限和审计证据。

![Peter Steinberger's X post on OpenClaw AI spend](imgs/openclaw-tokens-dont-matter/steipete-openclaw-token-spend-post.webp)

**来源**：

- X post：<https://x.com/steipete/status/2055405041843052792?s=20>
- Crabbox docs：<https://crabbox.sh/>
- Clawpatch docs：<https://clawpatch.ai/>
- 相关旧文：[[2026-05-10/2026-05-10-crabbox-remote-agent-workspace-control-plane|Crabbox：给 Agent 的远程测试盒与工作区控制平面]]
- 相关旧文：[[2026-04-30/2026-04-30-clawsweeper-architecture-practical-guide|Clawsweeper 架构实用指南]]

## 1. 这条 X 真正提出的问题

Peter 的原话核心不是“我用了很多 AI”，而是：

> How would we build software in the future if tokens don't matter?

这句话很关键。大多数团队今天讨论 AI 编程时，默认约束是：一次对话多少钱、一次推理多久、上下文窗口够不够、人工 review 能不能跟上。OpenClaw 这里反过来做实验：假设 token 预算不是第一瓶颈，软件工程组织会变成什么形状？

他列出的工作流包括：

- 云端常驻约 **100 个 Codex**，review 每个 PR 和每个 issue；
- fix landed on main 后，`@clawsweeper` 会回头找到 6 个月前的老 issue，并用精确引用关闭它；
- 每个 commit 都跑 Codex 做 security review；
- Codex 自动做 issue 去重、聚类，并报告最紧急的问题；
- agent 可以重建复杂环境，启动 ephemeral `crabbox.sh` 机器，登录 Telegram 之类的外部服务，录制 before/after 视频并贴到 PR；
- 新 issue 如果符合 documented vision，Codex 自动创建 PR，再由另一个 Codex review；
- Codex 扫描垃圾评论并封禁用户；
- Codex 验证性能 benchmark，把 regression 报到 Discord；
- 会议监听 agent 在讨论新功能时就主动创建 PR；
- `clawpatch.ai` 把项目切成 functional units，用于 review、找 bug 和 regression；
- 安全侧用类似切分方式结合 Vercel deepsec 和 Codex Security 找 regression 与漏洞。

这不是一个“写代码助手”的列表，而是一张软件工厂的自动化拓扑图。

## 2. 从 Copilot 到 agent swarm：角色发生了变化

传统 Copilot 模式里，人是调度器：人决定看哪个 issue、开哪个分支、跑哪个测试、什么时候发 PR、怎么记录证据。AI 只是局部补全或局部建议。

OpenClaw 这条帖子描述的是另一种形态：

| 传统 AI coding | OpenClaw 式 agent-native SDLC |
|---|---|
| 人发起一次任务 | agent 持续监听 repo / issue / commit / meeting |
| AI 帮写局部代码 | 多个 agent 分工 review、复现、聚类、修复、验证 |
| 测试环境靠本地/CI | ephemeral Crabbox 远程 testbox 随任务启动 |
| 结果靠文字描述 | 截图、视频、日志、JUnit、benchmark regression 报告作为证据 |
| review 是人工瓶颈 | AI 先做第一轮归类、查重、风险提示和候选 PR |
| 成本按单次对话衡量 | 成本按组织吞吐量和验证闭环衡量 |

关键变化是：AI 不再只在 IDE 里回答问题，而是进入了软件交付链路本身。

## 3. Crabbox：为什么“能跑起来”是 Agent 软件工程的底座

![Crabbox remote testbox docs](imgs/openclaw-tokens-dont-matter/crabbox-remote-testbox-docs.webp)

帖子里提到 agent 会 spin up ephemeral `crabbox.sh` machines。Crabbox 的文档把它定义为 **shared agent workspace control plane**：保持本地开发体验不变，但把 compute、tests 和 review evidence 移到 owned 或 provider-backed remote capacity。

Crabbox 的基本循环是：

```bash
crabbox run -- pnpm test
# lease cbx_8f2 - hetzner cax21 - ready 11s
# sync 184 files (1.2 MB)
# tests passed in 47s - released
```

它解决的是 agent 落地中的一个硬问题：**代码建议很便宜，可信复现很贵。**

一个 agent 要自动修 issue，不能只在上下文里“认为”自己修好了。它需要：

- 租一台短生命周期机器；
- 同步 dirty checkout；
- 跑真实命令；
- 登录必要外部服务；
- 采集截图、视频、JUnit、日志、lease metadata；
- 把 before/after 证据贴回 PR；
- 用 TTL 和 spend cap 控制成本；
- 最后释放资源。

这就是为什么 Crabbox 不是边缘工具，而是 agent swarm 的执行底座。没有这种可复现 testbox，100 个 Codex 很容易变成 100 个会写漂亮理由但无法证明结果的评论机器人。

## 4. Clawpatch：把 repo 切成 agent 可以理解的工作单元

![Clawpatch code review docs](imgs/openclaw-tokens-dont-matter/clawpatch-code-review-docs.webp)

Peter 提到 `clawpatch.ai` 的作用是把项目切成 functional units，用来 review、找 bug 和 regression。Clawpatch 文档里的说法是：它把 codebase 映射成 semantic feature slices，review bounded context，并把 findings 和 fix attempts 持久化。

这件事很重要，因为 repo 太大时，直接把“整个项目”丢给 agent 是低质量策略。Clawpatch 试图创建更适合 agent 的中间层：

- **Feature Mapping**：routes、commands、packages、CLI scripts、tests；
- **Context Boundaries**：entrypoints、owned files、nearby tests、trust boundaries；
- **Findings**：category、severity、confidence、evidence、recommendation；
- **Patch Attempts**：每个 finding 的 fix loop 和 validation results；
- **Safety**：clean worktree checks、no implicit commits、audit trail、schema validation。

这和帖子里的“tokens don't matter”是一体两面：当你愿意并行跑很多 agent 时，最先爆炸的不是 token 账单，而是上下文组织、任务边界和验证状态。Clawpatch 这种 semantic slicing 就是在回答：如何把一个 repo 切成可分派、可审计、可复跑的小块？

## 5. 真正的瓶颈从 token 变成 orchestrator

如果 token 成本下降一个数量级，软件团队不会简单地“多问几次 ChatGPT”。真正会发生的是：更多工作变成后台常驻 loop。

帖子里每个场景都可以抽象成一个 loop：

| Loop | 触发器 | Agent 动作 | 输出物 |
|---|---|---|---|
| PR review | 新 PR / commit | review code、查安全问题、跑测试 | review comment / finding / patch |
| Issue triage | 新 issue / 老 issue | 去重、聚类、关联 fix | report / close reference |
| Reproduction | bug report | 启动 Crabbox、复现、录屏 | before/after video、logs |
| Performance | benchmark run | 对比 baseline、找 regression | Discord alert / PR comment |
| Meeting-to-code | 会议讨论 | 识别 feature、创建 PR | draft PR / issue |
| Security | code slice / commit | deepsec / Codex Security / threat review | vulnerability finding / remediation |
| Moderation | 新评论 | 检测 spam、block | moderation action |

这些 loop 的难点不是“让模型生成文字”，而是 orchestration：谁能触发？权限是什么？最多花多少钱？失败怎么重试？输出怎么验证？多个 agent 冲突怎么办？人在哪里介入？

因此，OpenClaw 的核心实验更像一个“软件组织操作系统”，而不是一个 coding chatbot。

## 6. “AI spend”应该怎么被衡量？

外界容易把焦点放在 token bill 上，但这可能是错误指标。对 agent-native 团队来说，更合理的指标是：

- 每美元能关闭多少有效 issue？
- 每美元能避免多少 security regression？
- 每美元能节省多少 reviewer time？
- 每美元能提前发现多少性能退化？
- 多少 AI 产出能进入可验证状态，而不是停留在 comment？
- 人类需要 review 的候选 PR 中，多少真的值得看？

如果一个后台 Codex 花了钱但只产生噪音，那是浪费。如果它自动复现 bug、生成证据、定位旧 issue、触发安全审查，并减少人类上下文切换，那它更像 DevOps / QA / AppSec 的自动化预算，而不是聊天成本。

这也是 Peter 最后说 “All that automation allows us to run this project extremely lean” 的原因：lean 不是 token 少，而是人少、交接少、等待少、遗漏少。

## 7. 风险：Agent swarm 不是免费午餐

这种模式很激进，也有明显风险：

1. **成本失控**：100 个 agent 如果没有 TTL、spend cap、priority queue，很容易烧穿预算。
2. **权限扩散**：agent 能登录 Telegram、改 issue、开 PR、block 用户，就必须有细粒度权限和审计。
3. **噪音爆炸**：自动 review 如果没有 confidence、dedupe、severity gate，会让人类更累。
4. **验证幻觉**：agent 声称修复不等于真实修复，所以需要 Crabbox 这样的证据链。
5. **供应链风险**：自动安全扫描、自动 patch、自动 PR 必须限制 destructive operations 和 secret exposure。
6. **组织依赖**：如果团队开始依赖后台 agent，agent outage 会变成工程流程 outage。

换句话说，token 不重要以后，治理更重要。

## 8. 对 QCut / OpenClaw 类项目的启发

这条帖子对所有 agent 产品都有启发：

- 不要只做一个“会回答”的 agent，要做能监听事件、启动环境、产出证据、回写系统的 agent；
- 不要只优化 prompt，要优化任务切片、状态持久化、权限边界、成本上限和验证闭环；
- 不要把 AI review 当成单次评论，而要把它变成可恢复、可去重、可聚类、可审计的持续流程；
- 不要让 agent 只写 patch，要让它同时生成 proof：测试日志、截图、录屏、benchmark diff、issue reference；
- 不要忽视“人机接口”：Discord、GitHub、会议、PR、issue、docs 都是 agent swarm 的操作界面。

## 结论

Peter 这条 X 的价值在于，它把讨论从“AI 花费吓人吗？”转到了“当推理成本足够低，软件组织会怎么重构？”

OpenClaw 的答案看起来是：让 agent 成为持续运行的软件工程劳动力，把 repo、issue、PR、CI、会议、测试环境、安全审查和 Discord 全部接进同一个自动化平面。Crabbox 提供可复现执行环境，Clawpatch 提供可分派的语义切片，Clawsweeper 连接 issue 与修复历史，Codex / Codex Security / deepsec 则成为并行认知工人。

这不是简单的“用 AI 写代码”。这是在设计一个 token-cheap 时代的软件公司。
