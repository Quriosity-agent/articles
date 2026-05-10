# Hermes Agent Delegation 实战指南：如何把复杂任务拆给子 Agent

> Source: <https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation>  
> Date: 2026-05-09  
> Tags: Hermes Agent / delegate_task / Subagent Delegation / Multi-Agent / Agent Orchestration / Workflow

![Hermes Agent banner](imgs/hermes-agent-delegation-guide/hermes-agent-banner.png)

## 1. Delegation 解决的不是“让 Agent 更多”，而是“让上下文更干净”

很多人第一次看到 Hermes Agent 的 `delegate_task`，会把它理解成“开多个 Agent 并行干活”。这当然没错，但不是最关键的点。

真正关键的是：**主 Agent 不需要把所有研究、探索、调试、审查过程都塞进同一个上下文里。**

在复杂任务里，一个 Agent 很容易被这些东西拖垮：

- 资料搜索过程中产生大量中间信息；
- 代码库探索会读很多文件，但最后只有少数结论有用；
- 同一个问题需要从安全、性能、产品、工程维护多个角度看；
- 任务天然可以并行，例如同时研究三个方案；
- 主对话需要保持清晰，但子任务需要大量试错。

Hermes 的 delegation 模式就是把这些“需要独立思考、但不一定需要污染主上下文”的工作拆出去。主 Agent 负责判断目标、拆任务、给上下文、验收结果；子 Agent 负责在自己的隔离环境里完成一个明确任务，最后只把总结交回来。

一句话：**`delegate_task` 是 Agent 的上下文管理工具，也是并行工作流工具。**

## 2. `delegate_task` 到底是什么

官方文档把它定义得很直接：`delegate_task` 会 spawn child `AIAgent` instances，每个子 Agent 都有：

- 独立上下文；
- 受限制的 toolsets；
- 自己的 terminal session；
- 一段全新的 conversation；
- 最终只把 summary 返回给 parent context。

最小例子是这样：

```python
delegate_task(
    goal="Debug why tests fail",
    context="Error: assertion in test_foo.py line 42",
    toolsets=["terminal", "file"],
)
```

批量并行也可以：

```python
delegate_task(tasks=[
    {"goal": "Research topic A", "toolsets": ["web"]},
    {"goal": "Research topic B", "toolsets": ["web"]},
    {"goal": "Fix the build", "toolsets": ["terminal", "file"]},
])
```

默认最多并发 3 个子 Agent，这个限制可以通过 `delegation.max_concurrent_children` 或环境变量 `DELEGATION_MAX_CONCURRENT_CHILDREN` 调整。

## 3. 最重要的规则：子 Agent 什么都不知道

这是使用 delegation 时最容易踩坑的地方。

子 Agent 不是主 Agent 的“分身记忆”。它启动时是一个完全新的 conversation，不知道：

- 用户之前说过什么；
- 主 Agent 已经读过哪些文件；
- 上一个工具调用返回了什么；
- 你们在主对话里达成了哪些隐含约定；
- 这个项目的真实路径、运行方式、风险边界。

它唯一知道的，就是主 Agent 在 `goal` 和 `context` 里传给它的内容。

所以这个 prompt 很差：

```python
delegate_task(goal="Fix the error")
```

因为“the error” 对子 Agent 来说没有任何含义。

更好的写法是：

```python
delegate_task(
    goal="Fix the TypeError in api/handlers.py",
    context="""
Project path: /home/user/myproject.
api/handlers.py line 47 raises: 'NoneType' object has no attribute 'get'.
process_request() receives a dict from parse_body(), but parse_body() returns None
when Content-Type is missing. The project uses Python 3.11.
Please inspect the relevant code, make the smallest safe fix, and run the tests.
""",
    toolsets=["terminal", "file"],
)
```

这就是 delegation 的核心工程原则：**不要把隐含上下文留给子 Agent 猜。**

## 4. 一个实用 mental model：主编 + 专题记者

可以把主 Agent 想成主编，把子 Agent 想成专题记者。

主编不会对记者说：“去看看那个问题。”主编会说：

- 你负责哪个方向；
- 背景是什么；
- 需要采访/调查哪些材料；
- 不要碰哪些东西；
- 最后交什么格式；
- 哪些结论必须带证据；
- 哪些不确定性要标出来。

对应到 `delegate_task`，一个好的 delegation prompt 通常包含六个部分：

1. **Goal**：这个子任务到底要完成什么；
2. **Context**：为什么要做、主任务是什么、已有事实是什么；
3. **Scope**：只看什么，不看什么；
4. **Permissions**：是否允许写文件、跑命令、访问网络；
5. **Output contract**：返回 bullet list、表格、文件路径、结论还是 patch summary；
6. **Uncertainty handling**：不能确定时要说明，不要编造。

推荐模板：

```text
Task:
Research the Hermes Agent delegation feature and summarize it for a practical article.

Context:
The article is for Chinese-speaking builders. It should explain what delegation is,
when to use it, how it works, limitations, pitfalls, and examples.

Constraints:
- Do not write files.
- Do not invent undocumented API details.
- If the source is inaccessible, say so.
- Include source links.

Expected output:
- Key facts
- Practical examples
- Pitfalls
- Recommended prompt template
- Source links
```

## 5. 什么时候应该用 delegation

### 5.1 文档研究

比如这篇文章本身就适合先委派一个子 Agent 做资料整理：

```text
Research the Hermes Agent delegation documentation.
Extract the core mechanics, examples, configuration options, limitations, and pitfalls.
Do not write files. Return a structured bilingual outline with source links.
```

这种任务边界清楚、输出可验收、不会产生高风险副作用，非常适合 delegation。

### 5.2 代码库探索

大型代码库探索很容易污染主上下文。可以让子 Agent 专门负责一个模块：

```text
Inspect /Users/peter/my-app.
Find where authentication is implemented.
Do not modify files.
Return:
- key files
- request flow
- likely extension points
- risks or unclear areas
```

主 Agent 最后只需要拿到“关键文件 + 调用链 + 风险”，不需要把子 Agent 读过的几十个文件都装进主对话。

### 5.3 并行方案比较

如果你要比较 Redis、Postgres、SQLite 三种 job state 存储方式，可以开三个子 Agent 分别研究：

- Redis：关注吞吐、过期、运维复杂度；
- Postgres：关注一致性、查询、schema 演进；
- SQLite：关注本地部署、锁、并发限制。

最后主 Agent 把三份结论合成一张决策表。这比一个 Agent 在同一上下文里来回切换视角更干净。

### 5.4 多角度 review

同一个 PR 可以拆成：

- 安全 review；
- 性能 review；
- 可维护性 review；
- 测试覆盖 review。

每个子 Agent 只看一个角度，主 Agent 做最终优先级排序。

### 5.5 会产生大量中间过程的任务

例如：

- 追踪测试失败原因；
- 找出某个 bug 的所有可能入口；
- 阅读一批论文或文档；
- 对多个竞品做调研；
- 为一篇长文收集素材。

这些任务的共同点是：**过程很长，但最终只需要结构化结论。**

## 6. 什么时候不该用 delegation

### 6.1 小到一两步就能完成的任务

改一个变量名、查一个短文件、算一个简单值，不需要委派。Delegation 有协调成本，用错了会变慢。

### 6.2 强依赖主对话隐含上下文的任务

如果子 Agent 必须知道很多“刚才我们聊过但没有写出来”的东西，就不要轻易委派。除非你愿意把上下文完整写进 `context`。

### 6.3 需要持续和用户来回确认的任务

子 Agent 不能 `clarify`，也不能直接和用户对话。它适合“接任务 → 独立完成 → 回报告”，不适合边做边问。

### 6.4 高风险副作用任务

例如：删除文件、改生产配置、跑数据库 migration、大范围重构。不是绝对不能委派，但必须写清楚权限边界：

```text
Analysis only. Do not modify files. Do not run destructive commands.
Return a proposed plan and wait for parent approval.
```

## 7. Toolset 选择：给子 Agent 刚好够用的工具

官方文档给出的推荐模式很实用：

| Toolsets | 适合场景 |
|---|---|
| `["terminal", "file"]` | 代码修改、调试、构建、测试 |
| `["web"]` | 资料研究、事实核查、查文档 |
| `["terminal", "file", "web"]` | 需要本地 + 网络的完整任务 |
| `["file"]` | 只读代码 review，不需要执行命令 |
| `["terminal"]` | 系统管理、进程和环境检查 |

原则是：**能不给的工具就不给。**

如果只是研究网页，不要给 file/terminal；如果只是看本地代码，不一定要给 web；如果只需要 read-only review，就不要默认允许修改文件。

Hermes 也会阻止一些子 Agent 工具能力：默认 leaf 子 Agent 不能调用 `delegate_task`、`clarify`、`memory`、`send_message`、`execute_code`。原因很清楚：避免递归失控、避免共享记忆副作用、避免子 Agent 直接对外发送消息。

## 8. Batch mode：并行不是越多越好

`delegate_task(tasks=[...])` 会用线程池并行跑多个子 Agent。关键细节：

- 默认最大并发是 3；
- 超过并发上限的大 batch 会返回 tool error，而不是静默截断；
- 结果会按输入 task index 排序，而不是按完成时间；
- CLI 模式会展示子 Agent 工具调用树；
- gateway 模式会把进度批量转发给 parent progress callback；
- parent 被 interrupt 时，所有 active children 都会被 interrupt。

这意味着 batch mode 最适合“独立、并行、结果可合并”的任务。不要把强依赖的步骤硬塞进同一个 batch。

坏例子：

1. 子 Agent A 先设计 API；
2. 子 Agent B 根据 A 的 API 写前端；
3. 子 Agent C 根据 B 的实现写测试。

这三个任务其实有依赖关系，不适合同时 batch。更好的做法是分阶段：先让 A 做设计，主 Agent 验收后，再开 B/C。

## 9. Nested orchestration：可以递归，但要非常克制

默认情况下，delegation 是 flat 的：parent spawn child，child 不能再 spawn grandchild。

如果要做多阶段编排，可以使用 `role="orchestrator"`，让子 Agent 保留 delegation 能力：

```python
delegate_task(
    goal="Survey three code review approaches and recommend one",
    role="orchestrator",
    context="...",
)
```

但这里有几个限制：

- 默认 `max_spawn_depth` 是 1，所以 flat；
- 要让 orchestrator child 再 spawn worker，需要把 `delegation.max_spawn_depth` 提高到 2；
- 最高深度有 cap；
- `delegation.orchestrator_enabled: false` 可以全局关闭；
- 成本会乘法增长，例如 depth 3、每层 3 并发，理论上可能到 27 个 leaf agents。

我的建议：**除非你已经能清楚画出任务树，否则不要急着开 nested orchestration。** 先用 flat delegation 把主 Agent + 几个子 Agent 的流程跑顺。

## 10. Lifetime：`delegate_task` 不是后台任务队列

这是另一个重要边界。

`delegate_task` 是同步的：它运行在 parent 当前 turn 里，会阻塞 parent，直到子 Agent 完成或被取消。它不是 durable background job。

如果用户发新消息、`/stop`、`/new`，active children 会被取消；子 Agent 不会在 parent turn 结束后继续跑。

所以：

- 短时间、可中断、需要 reasoning 的子任务：用 `delegate_task`；
- 必须长期运行、不能被当前对话打断的任务：用 `cronjob(action="create")`；
- 长时间 shell 任务，比如测试、构建、下载：用 `terminal(background=True, notify_on_complete=True)`。

这个边界非常实用。不要把 delegation 当成任务队列，它更像“当前回合里的临时工作组”。

## 11. `delegate_task` vs `execute_code`

官方文档也专门比较了这两个工具。我的理解是：

| 维度 | `delegate_task` | `execute_code` |
|---|---|---|
| 本质 | 另一个 LLM Agent 推理循环 | Python 脚本执行 |
| 适合 | 需要判断、探索、多步推理 | 机械化数据处理、批量工具调用 |
| 上下文 | 新 conversation，需要传 context | 无 conversation，只看脚本和 stdout |
| 成本 | 更高 | 更低 |
| 并行 | 默认最多 3 个子 Agent | 单脚本 |
| 输出 | 子 Agent summary | stdout |

经验法则：

- 需要“判断”的，用 `delegate_task`；
- 需要“算/筛/批处理”的，用 `execute_code`；
- 需要“长期跑”的，用 background terminal 或 cron。

## 12. 配置项：什么时候值得调

官方示例配置：

```yaml
# ~/.hermes/config.yaml
delegation:
  max_iterations: 50
  max_concurrent_children: 3
  max_spawn_depth: 1
  orchestrator_enabled: true
  model: "google/gemini-3-flash-preview"
  provider: "openrouter"
```

几个实用建议：

- `max_iterations`：子 Agent 最多 tool-calling turns，复杂代码任务可以高一点；
- `max_concurrent_children`：并发数，默认 3 对大多数机器和 API budget 都比较安全；
- `child_timeout_seconds`：默认 600 秒，慢 reasoning model 可以适当提高；
- `model/provider`：可以给子 Agent 配便宜更快的模型，让主 Agent 用强模型做整合；
- `max_spawn_depth`：除非确实需要 nested orchestration，否则保持默认。

如果子 Agent zero-call timeout，Hermes 会把诊断写到 `~/.hermes/logs/subagent-timeout-<session>-<timestamp>.log`，里面包含配置快照、credential resolution trace 和早期错误信息。这对排查 provider、auth、tool schema 问题很有用。

## 13. 一套我会实际使用的 delegation prompt 写法

下面是一个适合日常工程任务的模板：

```text
Goal:
Inspect the authentication flow and identify why login intermittently returns 500.

Context:
Project path: /Users/peter/my-service.
The issue appears in production logs after POST /login.
Relevant symptoms:
- stack trace mentions src/auth/session.py
- happens when users log in with Google OAuth
- local tests currently pass

Scope:
Focus on auth routes, OAuth callback handling, session creation, and database writes.
Do not inspect unrelated billing or notification modules.

Permissions:
Analysis only. Do not modify files. You may read files and run non-destructive tests.

Expected output:
- top 3 likely causes
- file paths and evidence
- commands run
- uncertainty / what still needs confirmation
- recommended next step
```

这个模板的重点不是礼貌，而是降低误解：路径、症状、范围、权限、输出格式都写清楚。

## 14. 最常见的五个坑

### 坑 1：把任务写得像谜语

“看看这个 repo 有什么问题”不是任务，是愿望。子 Agent 需要可执行的调查方向。

### 坑 2：忘记写是否允许修改文件

如果只是研究，明确写 `Do not modify files`。如果允许修改，也要写“只做最小改动”“不要碰哪些文件”。

### 坑 3：没有要求证据

工程任务里，结论必须带路径、行号、命令输出或 source link。否则主 Agent 很难验收。

### 坑 4：过度并行

并行三个独立方向很好；并行十个含糊方向只会制造十份含糊总结。

### 坑 5：主 Agent 不做整合

Delegation 的最终产物不是子 Agent summary，而是主 Agent 基于 summary 形成的决策、文章、patch、计划或用户可执行答案。

## 15. 结论：`delegate_task` 是给主 Agent 用的“认知外包”

Hermes Agent 的 delegation 不是为了炫技式多 Agent，而是为了让复杂任务更可控：

- 子 Agent 处理局部复杂性；
- 主 Agent 保持全局目标；
- 中间噪音留在子上下文；
- 最终结论进入主上下文；
- 并行只用于真正独立的任务；
- 权限边界和输出格式必须写清楚。

如果只记住一句话：**把 `delegate_task` 当成“给一个完全失忆但很能干的同事写任务 brief”。Brief 写得越清楚，delegation 越可靠。**
