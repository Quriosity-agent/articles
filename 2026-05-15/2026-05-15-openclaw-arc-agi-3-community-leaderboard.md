# OpenClaw 登上 ARC-AGI-3 社区榜：5.2% 背后的 Agent Harness 信号

> **TL;DR**：ARC Prize 把 OpenClaw 放上了 ARC-AGI-3 Community Leaderboard：使用 Anthropic Opus 4.7 的 OpenClaw Harness 在 ARC-AGI-3 Public Demo Set 上拿到 **5.2%**，成本 **$2,912**，完成 **28 / 183** 个 level，总动作数 **9,010**。这个分数离“会玩”还很远，但它很重要：ARC-AGI-3 正在把 Agent 竞争从“模型会不会推理”推向“长期记忆、工具协议、代码执行、动作预算、可回放评测”组成的完整 Harness 工程。

![ARC Prize 关于 OpenClaw 的 X 发布](imgs/openclaw-arc-agi-3-community-leaderboard/arc-prize-x-openclaw.png)

**来源**：

- ARC Prize Community Leaderboard：<https://arcprize.org/leaderboard/community>
- ARC Prize X 发布：<https://x.com/arcprize/status/2055330785625006270?s=20>
- OpenClaw agent template：<https://github.com/arcprize/ARC-AGI-3-Agents/tree/main/agents/templates/openclaw_agent>
- OpenClaw scorecard：<https://arcprize.org/scorecards/4793f52c-ae2a-4622-a7e1-a84b06218c97>

## 1. 发生了什么

ARC Prize 在 2026-05-15 的社区榜单中新增了 **OpenClaw**。榜单描述是：

> OpenClaw Harness adapted to play ARC-AGI-3 allowed memory and code execution tools.

对应条目显示：

| 项目 | 数值 |
|---|---:|
| Benchmark | ARC-AGI-3 |
| Score | 5.2% |
| Cost | $2,912 |
| Date | 2026-05-15 |
| Code | `arcprize/ARC-AGI-3-Agents/agents/templates/openclaw_agent` |
| Scorecard | `4793f52c-ae2a-4622-a7e1-a84b06218c97` |

X 帖子补充了关键上下文：这次 OpenClaw 使用的是 **Anthropic Opus 4.7**，并且用到了 **long term memory** 和 **code execution**。ARC Prize 还特别提到一个 replay：OpenClaw 在 `ka59` 环境中解决了前两个 level，然后陷入循环。

这不是一个“模型又刷新榜单”的故事。更准确地说，这是一个 Agent Harness 被拿到真实交互式 AGI 基准上试跑的故事。

## 2. 为什么 5.2% 仍然值得看

如果只看数字，5.2% 并不高。Scorecard 的汇总是：

![OpenClaw ARC Prize scorecard](imgs/openclaw-arc-agi-3-community-leaderboard/openclaw-scorecard.png)

| 指标 | 数值 |
|---|---:|
| Score | 5.20% |
| Levels | 28 / 183 |
| Environments | 0 / 25 |
| Total actions | 9,010 |
| Tags | `agent`, `openclaw` |
| Published | 15/05/2026, 03:08:54 |

细看环境表会发现：OpenClaw 不是完全随机，也不是稳定通关。它在多个环境中可以推进一两个 level，但没有完成任何一个完整 environment。比如：

| Environment | Score | Levels | State | Actions | Resets |
|---|---:|---:|---|---:|---:|
| `ar25-0c556536` | 8.33 | 2 / 8 | NOT_FINISHED | 436 | 0 |
| `ka59-38d34dbb` | 10.71 | 2 / 7 | GAME_OVER | 319 | 2 |
| `m0r0-492f87ba` | 14.29 | 2 / 6 | GAME_OVER | 1083 | 6 |
| `sc25-635fd71a` | 14.29 | 2 / 6 | GAME_OVER | 184 | 3 |
| `wa30-ee6fef47` | 6.67 | 2 / 9 | GAME_OVER | 1012 | 9 |

这正是 ARC-AGI-3 的难点：它不是一次性回答题目，而是在陌生游戏中通过动作、观察、失败、记忆和策略修正来学习规则。一个 Agent 可以短暂发现局部规律，但很容易在更长 horizon 中进入循环、误判 reward，或者把动作预算花光。

所以 5.2% 的意义不是“OpenClaw 已经强”，而是它暴露了下一阶段 Agent 系统要解决的真实问题：**如何把模型推理变成可持续的交互式学习过程**。

## 3. OpenClaw Harness 实际做了什么

官方代码里的 `openclaw_agent` 不是一个复杂 Python Agent，而是一个薄适配层：

```text
ARC main.py / Swarm
    ↓
OpenClaw Python shim
    ↓  OpenAI-compatible HTTP API
OpenClaw Gateway (localhost:18789)
    ↓
Anthropic / OpenAI / Gemini / Ollama
```

这个设计有几个工程含义：

### 3.1 把 Agent loop 放到 OpenClaw daemon 里

ARC 框架仍然负责启动游戏、管理 Swarm、记录动作；OpenClaw 通过 Gateway 接管真正的对话历史、工具调用策略和模型选择。这样做的好处是，ARC 环境不需要理解 OpenClaw 的内部 Agent 系统，只要把每一帧状态转成一次 chat completion 请求即可。

### 3.2 用 session key 保留长期上下文

README 里提到，每个游戏会传入：

```text
x-openclaw-session-key: arc:<card_id>:<game_id>:<run-id>
```

这让同一个 game 内的多轮动作共享 OpenClaw server-side memory。对 ARC-AGI-3 这种交互式任务来说，这比每一步 stateless 调用重要得多：Agent 必须记住“刚才试过什么”“哪种动作有效”“某个颜色或位置是否意味着障碍/目标”。

### 3.3 没有依赖 OpenAI-style tools，而是使用 JSON-in-text 协议

代码说明里有一个很现实的坑：OpenClaw 的 `/v1/chat/completions` 兼容层在某些后端上会静默丢弃 `tools` 字段，Anthropic provider 也被验证过有这个问题。因此这个 Agent 没有依赖原生 tool schema，而是要求模型在文本里返回 JSON：

```json
{
  "action": "ACTION1",
  "thought": "Player is below the door; moving up should advance.",
  "confidence": 0.8,
  "alternatives_considered": ["ACTION4 to test right wall"]
}
```

这很像真实生产系统里常见的妥协：协议不完美，兼容层不稳定，最后要靠更稳的文本协议、解析容错和记录字段来让系统跑起来。

### 3.4 网格被序列化为 hex text，而不是视觉输入

README 还说明：OpenClaw 的兼容 API 没有文档化 image input，所以当前版本把 grid 序列化成 hex text。也就是说，这次 OpenClaw 并不是一个真正“看图玩游戏”的多模态 Agent，而是把视觉状态压成文本状态后交给模型。

这会降低上限，但也让实验更可控：先证明 long-term memory + action protocol + code execution 的 Harness 能跑通，再考虑多模态输入。

## 4. 这次结果给 Agent Builder 的三个提醒

### 第一，ARC-AGI-3 测的是“闭环”，不是单点智商

传统 benchmark 容易让人盯着模型本体：谁更会推理、谁上下文更长、谁 pass@k 更高。ARC-AGI-3 不一样，它测的是一整套闭环：观察、假设、行动、反馈、记忆、修正、再行动。

这意味着模型只是系统的一部分。真正决定上限的，还包括：状态表示、动作抽象、探索策略、失败检测、循环检测、成本控制和 replay 分析。

### 第二，长期记忆不是“聊天记录越长越好”

OpenClaw 有 session memory，这是优势；但 X 帖子里 `ka59` 的描述也说明，记忆本身不能防止循环。Agent 记住了历史，不代表它能正确总结历史；它可能只是更坚定地重复错误策略。

长期记忆需要配套：

- 失败动作的结构化记录；
- 假设的版本管理；
- 明确的“不要再试”约束；
- 对 reward / level transition 的检测；
- 当状态停滞时触发策略重置。

### 第三，代码执行是工具，不是魔法

OpenClaw 用了 code execution，但 scorecard 显示它仍然大量消耗动作。对 ARC-AGI-3 来说，代码执行最有价值的地方不是“写更多代码”，而是把观察日志转成可检索、可统计、可验证的实验记录。例如：

- 统计每个动作后状态变化；
- 检测地图中可移动/不可移动区域；
- 从 replay 中自动抽取重复循环；
- 对多个 level 生成共同规则假设。

如果代码执行只是在每轮里辅助模型描述画面，而没有沉淀成可复用的 world model，它的收益会很有限。

## 5. 对 OpenClaw / QCut 这类 Agent 系统的启发

这条榜单对我们这种做 Agent 工具链的人很有参考价值。OpenClaw 不是靠“更会聊天”进入榜单，而是靠一个可插拔 Harness：Gateway、session、模型切换、动作协议、代码执行、日志记录。

这和真实产品里的 Agent 可靠性问题高度一致：

- 模型能力只是起点，Harness 才决定能不能长期跑；
- 记忆必须可审计，不然只是更长的幻觉上下文；
- 工具调用必须有降级协议，不能假设所有 provider 都支持同一套 schema；
- replay / scorecard 是产品化 Agent 的必要观测层；
- 成本需要和成功率一起看，否则长程任务很容易“会一点，但太贵”。

5.2% 看起来小，但这是一个很诚实的结果。它告诉我们：真正的通用 Agent 还早；但下一阶段要做什么已经越来越清楚——不是再堆一个聊天 UI，而是把记忆、工具、环境、评测和成本控制做成一个能持续迭代的闭环。

## 结论

OpenClaw 登上 ARC-AGI-3 Community Leaderboard 的重点不是分数本身，而是信号：**Agent 竞争正在从模型榜单走向 Harness 榜单**。

ARC-AGI-3 这种交互式基准会持续把“会说”与“会做”之间的差距暴露出来。OpenClaw 的 5.2% 说明，长期记忆和代码执行已经能让通用 Agent 在陌生环境中推进一点点；但循环、状态抽象、探索策略和成本效率仍然是硬问题。

如果说 ARC-AGI-1 考的是静态抽象能力，那么 ARC-AGI-3 考的就是：一个 Agent 能不能在没有说明书的世界里，边试、边记、边修正，最后形成可复用的行动策略。

这才是 Agent 系统真正难的地方。
