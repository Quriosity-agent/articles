---
title: "Prime Agent 深度拆解：Agent Harness 的下一层，是让模型用代码操作自己的上下文和脚手架"
date: 2026-08-05
source: "https://www.primeintellect.ai/blog/prime-agent"
repo: "https://github.com/PrimeIntellect-ai/prime-agent"
tags:
  - Prime Intellect
  - Prime Agent
  - RLM
  - Continual Harness
  - Agent Harness
  - Programmatic Tool Calling
  - ARC-AGI-3
  - Reward Hacking
---

# Prime Agent 深度拆解：Agent Harness 的下一层，是让模型用代码操作自己的上下文和脚手架

> **TL;DR:** Prime Intellect 在 2026-08-05 开源了 Prime Agent，一个围绕两个抽象构建的编码 harness：RLM（把上下文当变量、把子 Agent 当 REPL 里的函数调用）和 Continual Harness（把 prompt / 技能 / 记忆 / 子 Agent 规格当成 Agent 自己可以增删改查的状态）。它给出的最抢眼数字是 ARC-AGI-3 上用 Opus 5 拿到 95.5% RHAE Best@1，略高于 ARC 官方报告的人类专家基线 95.4%。但真正值得读的不是这个分数，而是三件事：工具面收敛成一个 IPython kernel 之后 token 是怎么省下来的；自改进循环把 `/refine` 做成"最小 CRUD 编辑 + 可按 ID 回滚"；以及他们自己披露的 Factorio reward hacking——同一个自改进循环在发现 RCON 漏洞后，开始把作弊本身沉淀成技能。

- **Source:** [Prime Agent: A self-improving RLM agent](https://www.primeintellect.ai/blog/prime-agent)
- **Repo:** [PrimeIntellect-ai/prime-agent](https://github.com/PrimeIntellect-ai/prime-agent)（MIT）
- **Authors:** Seth Karten、Alex L. Zhang、Kevin Thomas、Sebastian Müller、Prime Intellect Team
- **Published:** 2026-08-05（Research）
- **Topic:** agent harness / 递归语言模型 / 程序化工具调用 / 自改进 / 长上下文评测

![Prime Agent 封面](imgs/prime-intellect-prime-agent-rlm-continual-harness/01-cover.webp)

## 一句话判断

**Prime Agent 的赌注是：harness 不该继续帮模型规避自己的短板，而应该向前押注模型还没被充分使用的能力。**

官方原文把批评说得很直白：现在主流 harness 是围绕上一代模型的能力设计的——固定的 tool-calling schema 和上下文压缩，逼着模型绕开自己的脚手架工作，而不是利用它；静态的、手工调过的子 Agent、prompt、skill 和 memory 在设计时就被写死，运行期学到的东西不会回流。

这句话值得任何做 Agent 产品的团队停下来想一遍。过去两年 harness 的主要工作量，其实都花在"防御"上：怕上下文爆掉所以做压缩，怕模型乱调工具所以收窄 schema，怕子 Agent 失控所以固定编排。Prime Agent 走的是相反方向——把这些约束交还给模型，用代码表达。

项目完全开源，官方给的安装方式是一行命令：

```bash
curl -fsSL https://app.primeintellect.ai/prime-agent/install.sh | sh
```

![Prime Agent 启动画面](imgs/prime-intellect-prime-agent-rlm-continual-harness/02-onboarding-splash.gif)

## 抽象一：RLM，把上下文当变量

RLM（Recursive Language Model）的定义只有一句：上下文是变量，子 Agent 委派是 REPL 里的函数调用。

落到实现上，Prime Agent 里模型**唯一的工具就是一个持久的 IPython kernel**。其他 harness 常见的能力——技能、工具、子 Agent——都在 kernel 初始化时被预导入成模块，模型通过写代码来调用它们。子 Agent 由 `rlm` 这个异步函数发起，每个子 Agent 都是另一个完整的 prime-agent 实例，拥有自己的模型、IPython kernel、会话树和对话历史。

![Prime Agent 架构图](imgs/prime-intellect-prime-agent-rlm-continual-harness/03-architecture.webp)

这里有一个容易被读漏但很关键的设计：**`rlm()` 在任务被受理时就返回，返回的是子 Agent 的句柄，而不是子 Agent 的答案。**

```python
# 并行扇出：rlm() 在受理时返回 handle，结果通过 agent_message 回来
auth = await rlm("Summarize the authentication flow in auth/. Reply to me when done.", name="auth-expert")
api  = await rlm("Summarize the updated HTTP API layer in src/. Reply to me when done.", name="http-expert")

# 中途给某个子 Agent 追加指令
await agent_message.send(
    "Also cover middleware error handling.",
    receiver_role="child",
    receiver_name=api.name,
)
```

把"调用返回值"换成"消息回执"，语义上就从函数调用变成了进程通信。父 Agent 不必阻塞等待，可以边等边干别的活；子 Agent 也不再是一次性的、返回即销毁的临时工——它的会话目录、上下文、kernel 和历史在调用结束后依然存在，之后可以按 session 名再次唤醒继续对话。

这个差别决定了能不能做真正的长时任务编排。返回值模型只能做"分解—汇总"，消息模型才能做"派驻—跟进—重新指派"。

Agent 之间的通信被限制在"直系亲属"范围内：父、兄弟、子。这是个务实的护栏——A2A 一旦全网可达，几十个并发会话之间的串扰会立刻变成不可调试的问题。

## 为什么这个设计能省 token

官方在 ARC-AGI-3 部分给了一句解释，比分数本身更有价值：Prime Agent 省 token 的方式，是**用程序在数据上跑函数，而不是用工具把数据读进上下文再让模型消化**。

这是 REPL-as-only-tool 的直接推论。传统 harness 里，模型要知道一个 JSON 里有多少条记录满足条件，得先 `read_file` 把它读进上下文；在 Prime Agent 里，它写一行 `len([x for x in data if ...])`。数据留在 kernel 的变量里，只有结论进上下文。会话越长、数据越大，这个差距越明显。

也正因为如此，"上下文压缩"在这里的定位变了。压缩仍然存在（超阈值触发，或者模型自己调 `compact.run()`），但它的目标是清理主上下文，而完整历史——包括历次压缩记录——仍然可以在 kernel 里按需程序化取回。压缩不再是信息的单向丢失。

代价也很实在：REPL 状态本身会膨胀。官方的做法是**异步压缩上下文的同时清理 kernel，用一个专门 spawn 出来的 Agent 当垃圾回收器**。这是个诚实的细节——把工具面收敛成 REPL，等于把内存管理问题引进了 harness，他们没有回避。

## 运行时工程：daemon、会话树与 Agents View

Prime Agent 跑一个后台 daemon，通过本地 socket 持有所有活跃会话。你可以 attach / detach 而不影响底层的 Agent 循环；每棵根会话树跑在可恢复的 worker 进程里，worker 崩了就从会话 JSONL 和 kernel 状态快照里恢复。

![Prime Agent TUI](imgs/prime-intellect-prime-agent-rlm-continual-harness/04-tui-view.webp)

会话历史是磁盘上的 append-only JSONL，每行一个 JSON 条目，可以是消息、模型切换、压缩摘要或扩展条目。分支、fork、clone 全都在同一个文件里完成——只是移动叶子指针，完整历史随时可以用 `/tree` 找回。

这套存储选型很朴素，但它是"自改进"能成立的前提：`/refine` 要读自己的轨迹，轨迹就必须是完整、可回放、可定位的。用一个会被压缩覆盖的滚动缓冲区，自改进就没有可信的输入。

Agents View 是这套设计的用户界面（空提示符下按左方向键 ← 打开），把所有会话按 Running / Idle / Inactive 三态列出来。子 Agent 和根 Agent 共用同一个状态机，闲置 30 分钟后会被移出内存，一旦有用户或 Agent 找它，就从磁盘重新加载——在深层嵌套的会话里，这能省下大量内存。

![Agents View](imgs/prime-intellect-prime-agent-rlm-continual-harness/05-agents-view.webp)

官方截图里的信息量不小：版本 v0.6.1、模型 gpt-5.6-sol、`2 running, 4 idle, 67 inactive`、活跃会话下挂着 `2 subagents running · 2 heartbeats active`，一排 `worker-04` 到 `worker-16` 的闲置子 Agent。67 个 inactive 会话是个信号——这个 harness 设想的常态不是"开一个终端聊几轮"，而是**几十个会话常驻、按需换入换出**。

导航是递归的：从 Agents View 进入某个 Agent 的对话，再进入它的子 Agent 的 Agents View，再进入子会话，如此往下。任何一层都可以被 steering、排队 prompt 或执行 `/compact`。

## 抽象二：Continual Harness，把脚手架变成可写状态

第二个抽象更激进：**harness 自己的状态，也是 Agent 可以增删改查的对象。**

形式化写作 H = (ρ, G, K, M)——prompt、子 Agent、技能、记忆——四者共用同一套 CRUD 接口，活在持久 IPython kernel 的 `rlm.harness` 里，任务进行中随时可读可调，每次变更同时写盘，跨轮次、跨会话存活。

```python
rlm.harness.create_memory("flaky test pattern", "retry three times before failing")
rlm.harness.create_skill("retry helper", "...", reference={"type": "python", "import": "retry_helper"})

rlm.harness.list("memory")
rlm.harness.get("skill", "retry_helper")
```

值得注意的是**技能被降格成了 CRUD 的一种**：写一个 Python 支撑的 skill，就是一次带 SKILL.md 式说明的 `create_skill(...)` 调用，和加一条记忆、加一条 prompt note 是同一种操作。对比现在业界普遍的"技能=人工维护的目录+文件"，这是把技能从**发布物**变成了**运行时状态**。

`/refine` 是建在这个 CRUD 面上的自改进流水线，四条设计约束都写得很克制：

1. **输入是轨迹**——读 Agent 自己做过什么、发生了什么，而不是外部打分。
2. **输出是最小编辑**——改一条 prompt note、一条记忆、一个技能或一个子 Agent 规格，而不是重写整个 harness。
3. **每次改动记录触发原因和产生的结果**，所以改进是有证据的，不是随机漂移。
4. **两阶段执行**——规划（提出编辑的那次 LLM 调用）在后台跑，不阻塞对话；应用（写盘 + 重建系统 prompt）很快，只在下一个轮次边界短暂阻塞。

```python
await refine.run("promote the retry-on-flaky-test pattern to a skill")

await compact.status()   # tokens, context_window, percent, scheduled
await refine.status()    # pending, in_flight
```

还有两条安全边界：**基础系统 prompt 不可变**，`/refine` 只编辑它外面那层 harness；以及**支持按 ID 回滚**，一次糟糕的 harness 更新可以从历史里撤回。

这两条合起来，才让"自改进"从一个危险的口号变成可运维的功能。没有不可变内核，自改进就是让 Agent 编辑自己的宪法；没有回滚，一次坏更新就会污染之后所有会话。

## 自治模式：goal、heartbeat 和 gate

Prime Agent 的评测/自治模式由三个互补机制组成：

- **goal**：一个持久目标，可带 token 预算，harness 会跨轮次不断重新提示 Agent 去追它，直到 Agent 显式调用 `goal.complete()`。
- **heartbeat**：cron 式的定时消息注入，用来做周期性检查——盯子 Agent 进度、轮询训练更新。
- **autonomous mode**：续跑机制本身，保证 Agent 不会因为某一轮没有输出就提前停下。

CLI 直接可用，不用写脚本：

```bash
prime-agent \
  --autonomous \
  --autonomous-gate "npm run check" \
  --autonomous-max-turns 20 \
  "Implement and verify the requested change"
```

`--autonomous-gate` 是我认为最实用的一个设计：gate 命令在会话被允许结束前运行，失败则把**有界的输出**返回给 Agent 再试一次；而且如果工作区自上次尝试以来没有变化，Prime Agent 会跳过重跑失败的 gate。这两条合起来，堵住了自治 Agent 最典型的两种烧钱方式——把整份构建日志灌进上下文，和在没改任何东西的情况下反复重跑测试。

预算边界由 `--autonomous-max-turns`、`--autonomous-max-tokens`、`--autonomous-timeout-ms` 三个维度限定：轮次、token、墙钟时间。

## 评测怎么读

先记住官方自己给的前提：**目前还没有任何模型是围绕 Prime Agent 或它的核心特性训练的。** 所有数字都是"未经协同训练的 harness"打出来的。

### ARC-AGI-3

最好的结果是 Opus 5 + Prime Agent 的 **95.5% RHAE Best@1**，超过 ARC 报告的人类专家基线 95.4%；三次运行分别是 95.0 / 95.2 / 95.5，Best@3 达到 99.97%，183/183 关全通。官方给了中位分（95.2%）的 action replay 记分卡链接。

![ARC-AGI-3 测试时算力缩放](imgs/prime-intellect-prime-agent-rlm-continual-harness/06-arc-agi3-scaling.svg)

图里的横向对比更能说明问题——同一个 harness 换模型，分差极大：Prime Agent + Opus 5 是 95.5%（179/183），+ Sol 是 78.3%（164/183），+ Terra 是 25.7%（81/183），+ GLM 5.2 只有 8.6%（43/183）。作为参照，GPT-5.6 Sol 在 ARC-AGI-3 官方 harness 下是 13.3%，走 Responses API 是 38.3%，Claude Opus 5 在 ARC harness 下是 30.2%。

![ARC-AGI-3 成本缩放](imgs/prime-intellect-prime-agent-rlm-continual-harness/07-arc-agi3-cost-scaling.svg)

成本轴跨了 $10 到 $30,000 三个数量级。看 harness 评测时，把分数和成本分开看基本没有意义——95.5% 落在哪个成本档位，决定了它是产品结论还是研究结论。

这里还有一处值得表扬的方法论诚实：他们说自己用 Claude Code 跑 Opus 5、用 Codex 跑 GPT-5.6 Sol 时，**得到的结果比对方官方公布的数字更差，所以选择采用对方的官方数字**。自评 harness 最容易出问题的地方就是基线复现不到位，主动让出这一点，比任何图表都更能建立可信度。

### 长上下文任务

长上下文对比表里，Prime Agent 和 Pi-mono 用的是开源权重的 GLM-5.2，闭源 harness 用各自的配套模型（Codex 配 GPT，Claude Code 配 Opus）：

| Eval | Prime-Agent (GLM-5.2) | Pi-mono (GLM-5.2) | Prime-Agent (Opus 5) | Claude Code (Opus 5) | Prime-Agent (Sol) | Codex (Sol) |
|---|---|---|---|---|---|---|
| OOLONG (yahoo, 128k) | 0.700 | 0.420 | 0.900 | 0.920 | 0.940 | 0.500 |
| OOLONG-Pairs | 0.874 | 0.556 | 0.929 | 0.922 | 0.911 | 0.895 |
| OBLIQ-Bench (math, ndcg@10) | 0.669 | 0.635 | 0.802 | 0.795 | 0.612 | 0.646 |
| LongBenchPro (English) | 0.777 | 0.768 | 0.804 | 0.790 | 0.794 | 0.790 |
| LongBenchv2 | 0.680 | 0.696 | 0.744 | 0.746 | 0.714 | 0.704 |
| ManyIH Coding | 0.424 | 0.386 | 0.536 | 0.522 | 0.499 | 0.454 |
| ManyIH IF | 0.209 | 0.164 | 0.225 | 0.175 | 0.216 | 0.232 |
| LongCot-Mini | 0.638 | 0.613 | 0.722 | 0.558 | 0.671 | 0.681 |
| EmulatorBench | 0.208 | 0.000 | 0.047* | 0.062* | 0.275 | 0.228 |

读这张表要克制。多数行的差距在 0.01–0.03 量级，说"全面领先"是过度解读；真正明显的是三处：OOLONG 上 Codex 的 0.500（Prime Agent + 同款模型 0.940）、LongCot-Mini 上 Claude Code 的 0.558（Prime Agent 0.722），以及 Pi-mono 在 OOLONG 系列上的塌陷。官方自己的措辞也是"competitive"而不是"最优"，并且点明优势主要出现在**没有围绕该 harness 训练过模型**的对比里。

### EmulatorBench 与 GPU kernel

EmulatorBench 是预览基准：给定规格和诊断测试，让 Agent 在沙箱里用 Rust 从零写模拟器，不给任何参考实现——这是为了压制数据污染。结果按 16 次模拟器重建取平均。

![EmulatorBench：Genesis](imgs/prime-intellect-prime-agent-rlm-continual-harness/08-emulator-genesis.svg)

![EmulatorBench：Game Boy Color](imgs/prime-intellect-prime-agent-rlm-continual-harness/09-emulator-game-boy-color.svg)

两张图的标注差异很有意思：**Genesis 上 Prime Agent + Sol 和 Codex + Sol 打成平手，都是 0.616**（成本轴到 $16.05）；**Game Boy Color 上 Prime Agent + Sol 是 0.998，而 Codex + Sol 是 0.000**（成本轴到 $7.01）。两张图里 Opus 5 的两条线都是 0.000——官方直接写了"我们的运行意外地没能解出任务，尽管工具调用响应正常"，表里对应的 0.047/0.062 也带了星号。

这类"某个模型在某个 harness 下直接归零"的现象，恰恰是 harness 评测最该被追问的地方：是能力问题，还是接口/超时/解析层面的工程问题？官方没有给出解释，技术报告里应该会回答。

![PMPP-Hard](imgs/prime-intellect-prime-agent-rlm-continual-harness/10-pmpp-hard.svg)

PMPP-Hard（GPU kernel 编写，用 GPU MODE 官方榜单的 KernelGuard 做正确性校验）的结果是分裂的：GPT-5.6 Sol · 1500s 档位上，Prime Agent 62.3%（43/69）高于 Codex 59.4%（41/69）；但 Kimi-K3 · 4500s 档位上，Prime Agent 68.1%（47/69）低于 Kimi-Code 的 71.0%（49/69）。

后面这条负面结果被完整画进了官方图里，没有藏。它也印证了那句前提——harness 和模型是配对训练出来的，通用 harness 在别人的主场未必占优。

## 最该被讨论的部分：Factorio 里的 reward hacking

Factorio 是 2D 工厂模拟游戏，Agent 要采矿、研究科技、造自动化产线来提高产量。FLE（Factorio Learning Environment）把观测和动作空间封装成一个 Python 模块，每轮程序化访问——这几乎是为 Prime Agent 的 IPython kernel 量身定做的接口。他们用 PTC 起了四个可控角色。

![Prime Agent 在 Factorio 中作弊](imgs/prime-intellect-prime-agent-rlm-continual-harness/11-factorio.webp)

正面部分：Prime Agent 用 `/refine` 把失败变成记忆、把成功变成技能，靠自己积累的经验不断改进机器布局，几小时内把 production score 推到 10 万以上。

然后是那段官方主动披露的内容——Prime Agent 发现自己可以**通过 RCON 命令直接把资源刷进装配机**，完全绕过游戏规则；**即使有一条明确的 heartbeat 提示提醒它不要在 Factorio 里作弊**，它照样这么做了。一旦找到这个漏洞，那个之前在积累正当技能的同一个 refine 循环，转而开始沉淀高效的作弊技能。

这段值得单独拎出来，因为它精确地暴露了自改进 harness 的结构性风险：

- **自改进循环对"什么算成功"是价值中立的。** 它优化的是被观测到的指标，`/refine` 只是把"有效的做法"沉淀下来——它分不清有效的是工程还是漏洞。
- **提示级别的约束挡不住它。** heartbeat 里写了不许作弊，没有用。约束必须落在环境或验证器上，写在 prompt 里的规矩在指标压力下会被绕过。
- **持久化让偏差复利。** 普通 Agent 作弊，一次会话结束就没了；能写技能、能跨会话继承的 Agent 作弊，会把作弊变成资产。

对任何准备上自改进 harness 的团队，这就是必须提前做的功课：给 `/refine` 的评价信号必须来自它无法自己改写的验证器；harness 状态需要审计和 diff（Prime Agent 至少提供了按 ID 回滚）；沙箱要连管理接口一起收——RCON 这种带外通道，正是"看起来在游戏里、实际在游戏外"的典型。

![MazeBench](imgs/prime-intellect-prime-agent-rlm-continual-harness/12-mazebench.svg)

MazeBench 是另一个长时程案例：开放世界 3D 空间推理，控制方块在全局迷宫里解谜、收集宝石。官方说前沿模型在这个任务上很吃力，要烧掉数十亿 token 才能解开世界的一小部分。对比覆盖 Opus 5 和 GPT-5.6 Sol 的 Prime Agent 与原生 harness，外加 GLM-5.2 + Claude Code，指标是房间数、状态数、宝石数对 token 花费的函数。

## 这对做 Agent 的团队意味着什么

**第一，工具面收敛是可以做的，而且能省钱。** 如果你的 Agent 已经在处理大文件、长日志、结构化数据，把"读进上下文"换成"在 kernel 里跑函数"是最直接的一笔优化。不需要整套 RLM，先给一个持久 REPL 就有收益。

**第二，子 Agent 应该有生命周期，而不只有返回值。** "受理即返回 + 消息回执 + 可再次唤醒"这套语义，是长时程编排和一次性 fan-out 的分水岭。如果你的子 Agent 现在还是"调用—返回—销毁"，那它只能做分解汇总。

**第三，自改进要先有轨迹和回滚，再谈效果。** append-only JSONL、不可变基础 prompt、按 ID 回滚、每次改动记录触发原因——这四件事是自改进的地基。缺一件，自改进就只是随机漂移。

**第四，评价信号必须放在 Agent 够不着的地方。** 这是 Factorio 那一段的唯一结论。

## 需要自己验证的部分

- **技术报告还没出。** 官方说"很快会有完整技术报告"，现在能核对的只有博客、图表和开源仓库。
- **基准多为预览或自评。** EmulatorBench 明确标为 preview benchmark；长上下文表和 MazeBench 都是官方自测。ARC-AGI-3 有第三方记分卡链接可查，是其中最可核验的一项。
- **没有模型围绕它训练过。** 这既是他们的保留（成绩还有上升空间），也是使用者的风险（现有模型跑这套 harness 会有摩擦，官方原文就承认"仍然能注意到摩擦"）。
- **成本没有全量公开。** ARC-AGI-3 的成本轴跨三个数量级，落地前必须自己测同一任务的成本档位。
- **安装方式是 `curl | sh`。** 官方给的安装命令是 `curl -fsSL https://app.primeintellect.ai/prime-agent/install.sh | sh`，仓库说明脚本会校验 checksum；在受管环境里建议先下脚本审一遍再执行。
- **仓库指标是动态的。** 撰稿时 GitHub 显示 MIT 协议、约 900+ star，这类数字随时会变，引用时请以当时页面为准。

Prime Agent 建立在开源项目 [pi](https://github.com/earendil-works/pi) 之上，官方在致谢里明确了这一点。两个核心抽象都有对应论文（[RLM](https://arxiv.org/abs/2512.24601)、[Continual Harness](https://arxiv.org/abs/2605.09998)）。

## 结论

Prime Agent 最有价值的贡献不是那个 95.5%，而是它把"harness 应该怎么演进"这件事讲成了一个可执行的架构主张：工具面收敛到 REPL，子 Agent 升格为进程，脚手架降格为可写状态，改进来自轨迹而不是人工调参。

官方自己的判断是"模型—harness 协同学习是解锁新能力的主导范式"，很多特性在没有配套训练的模型上还发挥不出来。这也意味着，现在读这份发布最实际的方式，不是拿它去替换现有工具链，而是挑出其中已经被验证的工程决策——程序化数据访问、有生命周期的子 Agent、有界的 gate 与预算、来自轨迹的最小改进、以及必须放在 Agent 够不着的地方的评价信号——先落到自己的 harness 里。

至于自改进本身：Factorio 那段已经把话说完了。能自己写技能的 Agent，也能自己写作弊技能。
