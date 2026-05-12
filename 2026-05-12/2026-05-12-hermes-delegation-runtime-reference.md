# Hermes Agent Delegation 运行时参考：`delegate_task` 不是后台队列，而是可控的子 Agent 调度层

> Source: <https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation>  
> Related: [[2026-05-09/2026-05-09-hermes-agent-delegation-guide|Hermes Agent Delegation 实战指南]] / [[2026-05-12/2026-05-12-hermes-agent-parallel-delegation-patterns|Hermes Agent Parallel Tasks 指南]]  
> Date: 2026-05-12  
> Tags: Hermes Agent / delegate_task / Subagent Runtime / Agent Orchestration / Toolsets / Reliability

![Hermes Agent banner](imgs/hermes-delegation-runtime-reference/hermes-agent-banner.png)

## 1. 这篇文档应该当成“运行时说明书”读

Hermes 官方的 Subagent Delegation 文档表面上是在介绍 `delegate_task`：单任务怎么写、批量并行怎么写、默认并发是多少、子 Agent 能用哪些工具。但如果只把它看成 API 参考，会错过更重要的一点：**它其实定义了 Hermes 多 Agent 的运行时边界。**

之前两篇文章已经分别讲过 delegation 的基本概念和工作流模式：

- 5 月 9 日那篇偏“为什么要把复杂任务拆给子 Agent”；
- 5 月 12 日 Parallel Tasks 那篇偏“怎么把 parallel research、code review、方案比较组织成模式”。

这篇换一个角度：把官方 delegation 页面当成一份 runtime contract，看清楚 `delegate_task` 到底保证什么、不保证什么，以及什么时候应该换成 `execute_code`、`cronjob` 或后台 Hermes process。

一句话：**`delegate_task` 不是“多开几个聊天窗口”，也不是“后台任务队列”，而是父 Agent 当前 turn 内的同步子任务调度层。**

## 2. 最核心的语义：子 Agent 是 fresh conversation

文档里最重要的一句话是：子 Agent 会启动一个完全新的 conversation，只知道父 Agent 在 `goal` 和 `context` 里显式传入的内容。

这意味着它不知道：

- 用户刚刚说过什么；
- 父 Agent 已经读过哪些文件；
- 某个错误来自哪条命令；
- 项目路径、测试命令、风险边界；
- 哪些文件可以改，哪些文件绝对不能动。

所以这个调用本质上是无效的：

```python
delegate_task(goal="Fix the error")
```

对子 Agent 来说，“the error” 没有上下文。更好的写法应该像一张 mini issue：

```python
delegate_task(
    goal="Fix the TypeError in api/handlers.py",
    context="""
Project path: /home/user/myproject.
api/handlers.py line 47 raises: 'NoneType' object has no attribute 'get'.
process_request() receives a dict from parse_body(), but parse_body() returns None
when Content-Type is missing. Use Python 3.11. Make the smallest safe fix and run pytest.
""",
    toolsets=["terminal", "file"],
)
```

这条规则对 Agent 编排很关键：**delegation 的质量取决于父 Agent 给上下文的质量。** 子 Agent 不是“分身记忆”，而是一个拿到工单后独立执行的 worker。

## 3. 批量并行：默认 3 个，但这不是鼓励无限拆分

文档说明，`tasks=[...]` 批量模式默认最多 3 个子 Agent 并发，可通过 `delegation.max_concurrent_children` 或 `DELEGATION_MAX_CONCURRENT_CHILDREN` 调整；超出限制的 batch 会报错，而不是静默截断。

这几个细节很实用：

| 语义 | 含义 |
|---|---|
| 默认并发 3 | 适合常见的研究、review、方案比较，不会默认制造过大成本 |
| 结果按输入顺序返回 | 即使完成顺序不同，父 Agent 拿到的结果仍然可预测 |
| CLI 有实时树状进度 | 适合观察每个子 Agent 的工具调用和完成情况 |
| gateway 里进度会批量回传 | Discord/Telegram 这种平台不会被每个子调用刷屏 |
| 父 turn 被 interrupt 会传播给子 Agent | 这是它不是 durable queue 的关键证据 |

所以，调高并发不是越高越好。并发数越高，问题会从“速度”变成“调度”：

- 子任务之间是否真的独立？
- 是否会同时改同一批文件？
- 是否会同时访问同一个 repo 的 git index？
- 父 Agent 是否能验证多个 summary 的真实性？
- 成本和速率限制是否可控？

如果任务只是“把 100 个文件做机械转换”，`delegate_task` 反而不是最优解。那应该用 `execute_code` 写脚本，或者用终端命令批处理。

## 4. toolsets 是权限边界，不只是性能优化

`toolsets` 参数看起来像“给子 Agent 开哪些工具”，实际上它是子 Agent 的权限边界。

文档给出的常见组合很清楚：

| Toolsets | 适合场景 |
|---|---|
| `["web"]` | research、fact-checking、查文档 |
| `["terminal", "file"]` | 代码修改、debug、build/test |
| `["terminal", "file", "web"]` | 需要查资料又要改代码的 full-stack 任务 |
| `["file"]` | 只读分析、无需运行命令的代码审查 |
| `["terminal"]` | 系统管理、进程检查、环境诊断 |

更重要的是，某些工具对子 Agent 是默认禁止的：

- `clarify`：子 Agent 不能直接问用户；
- `memory`：不能写共享长期记忆；
- `send_message`：不能跨平台发消息；
- `execute_code`：避免绕过 reasoning loop；
- `delegate_task`：leaf 子 Agent 不能继续无限派生。

这体现了一个很好的安全设计：**父 Agent 负责与用户和外部世界交互，子 Agent 负责在限定权限内完成工单。**

如果让每个子 Agent 都能发消息、写记忆、再开子 Agent，整个系统很快会变成难以审计的递归自动化。Hermes 的默认限制是在逼用户把 orchestrator 和 worker 的职责分清楚。

## 5. nested orchestration：默认平面化，递归必须显式开启

官方文档也提到 `role="orchestrator"` 和 `delegation.max_spawn_depth`。默认情况下 delegation 是 flat 的：父 Agent 可以开 children，但 children 不能再开 grandchildren。

如果要让子 Agent 继续调度自己的子任务，需要：

```python
delegate_task(
    goal="Survey three code review approaches and recommend one",
    role="orchestrator",
    context="...",
)
```

并且配置里要把 `max_spawn_depth` 从默认的 1 调高到 2 或 3。

这个功能很强，但也很危险。文档特别提醒：如果 `max_spawn_depth=3` 且 `max_concurrent_children=3`，理论上可以形成 3×3×3 = 27 个叶子 Agent。成本、速率限制、日志审计和 side effect 风险都会指数级上升。

所以我会把 nested orchestration 看成高级功能，而不是默认工作方式。绝大多数场景下，平面 batch 足够：父 Agent 拆任务，多个 leaf 子 Agent 干活，父 Agent 汇总和验证。

## 6. lifetime：这是最容易误用的部分

`delegate_task` 是同步的。它运行在父 Agent 当前 turn 内，父 Agent 会等待所有子 Agent 完成或被取消。它不是后台任务队列。

这带来三个直接后果：

1. 如果用户发新消息打断当前 turn，活跃子 Agent 会被 interrupt；
2. 子 Agent 不会在父 turn 结束后继续跑；
3. 被取消的子 Agent 可能返回 `status="interrupted"`，但由于父 turn 也被打断，这个结果未必会进入用户可见回复。

因此，长期任务应该换工具：

| 需求 | 更合适的机制 |
|---|---|
| 当前回合内并行研究/审查 | `delegate_task` |
| 机械数据收集、批处理、格式转换 | `execute_code` |
| 定时或一次性延迟运行，完成后回消息 | `cronjob(action="create")` |
| 需要独立长期运行、可 poll 日志 | `terminal(background=True, notify_on_complete=True)` + `hermes chat -q` |
| 多篇文章/多项工程并发写入同一 repo | 独立 Hermes process + git worktree/选择性 staging |

这也是为什么“同时写多篇文章”不应该简单塞进一个 `delegate_task(tasks=[...])`：如果中途用户继续对话，父 turn 可能被中断；而且多个子 Agent 还可能同时改 README、MOC、git index。更稳的是独立后台进程，甚至每篇一个 worktree。

## 7. `delegate_task` vs `execute_code`：判断标准是“要不要判断”

官方文档把这两者对比得很直接：

- `delegate_task`：完整 LLM reasoning loop，有工具、有上下文隔离、成本更高，适合需要判断的任务；
- `execute_code`：只是 Python 脚本通过 RPC 调工具，没有对话推理，成本低，适合机械流程。

我的经验判断可以更简单：

> 如果你能把流程写成确定性的脚本，就用 `execute_code`。如果你需要一个 fresh mind 去阅读、判断、取舍、总结，就用 `delegate_task`。

例如：

- “遍历 200 个 Markdown 文件，找出缺少 frontmatter 的文件” → `execute_code`；
- “读这 20 个文件，判断架构上哪里最脆弱” → `delegate_task`；
- “把这些 URL 全部抓下来并提取标题” → `execute_code`；
- “比较这些产品的定位差异，给出创业机会判断” → `delegate_task`。

## 8. 一个实用的 delegation checklist

实际调用前，父 Agent 应该先检查这张表：

- 这个子任务是否真的需要推理？
- 子任务是否能在当前 turn 内完成？
- 子任务是否与其它子任务互相独立？
- `goal` 是否清楚到一个陌生工程师也能执行？
- `context` 是否包含路径、错误、约束、测试命令、预期输出？
- toolsets 是否最小化？
- 子 Agent 是否可能产生外部 side effect？
- 父 Agent 准备如何验证 summary？
- 如果任务失败或被 interrupt，有没有 fallback？

如果这些问题答不上来，先不要 delegate。不是每个复杂任务都需要更多 Agent；很多时候真正需要的是更好的任务定义。

## 9. 结论：Delegation 的本质是“受控并行”，不是“自动放权”

Hermes 的 `delegate_task` 设计得很克制：fresh context、受限 toolsets、默认 flat、同步生命周期、final summary 回流。这些限制不是缺点，而是让多 Agent 系统可控的关键。

真正会用 delegation 的人，不是能一次开最多子 Agent 的人，而是能回答三个问题的人：

1. 这个任务为什么值得拆出去？
2. 子 Agent 需要知道什么、能做什么、不能做什么？
3. 父 Agent 如何验证结果并承担最终责任？

把这三点想清楚，`delegate_task` 才会从“并行炫技”变成可靠的 Agent 工程工具。