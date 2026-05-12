# Hermes Agent Parallel Tasks 指南：从“会委派”到“会编排”

> Source: <https://hermes-agent.nousresearch.com/docs/guides/delegation-patterns>  
> Related: <https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation>  
> Date: 2026-05-12  
> Tags: Hermes Agent / delegate_task / Parallel Tasks / Subagent Delegation / Multi-Agent Orchestration / Agent Workflow

## 1. 这篇文档真正讲的是“委派模式”，不是 API 参数

Hermes 已经有一篇完整的 `delegate_task` 功能参考，解释子 Agent 的隔离上下文、toolsets、并发、超时、嵌套 delegation、durability 等细节。`Delegation & Parallel Work` 这篇 guide 的价值不在于重复参数表，而是把问题往前推了一步：**什么时候该把任务拆出去，应该拆成什么形状，父 Agent 应该如何接回结果。**

这对实际使用 Agent 很关键。很多人以为 parallel tasks 就是“多开几个 Agent”。但真正的工程问题不是开几个，而是：

- 哪些任务值得并行；
- 哪些任务不该委派；
- 子 Agent 需要哪些上下文；
- 哪些 toolsets 应该开放；
- 父 Agent 如何验证子 Agent 的总结；
- 什么时候该用 `execute_code`、`cronjob` 或后台 terminal，而不是 `delegate_task`。

一句话：**delegation pattern 是 Agent 工作流设计，不是单纯的工具调用技巧。**

## 2. 什么时候应该 delegate

官方 guide 给出的判断标准很实用：适合 delegation 的任务一般有三个特征。

第一，**需要推理和判断**。例如 debugging、code review、research synthesis。它们不是一个简单工具调用能解决的，而是需要读材料、形成判断、输出结论。

第二，**中间过程会污染主上下文**。比如阅读大量网页、扫一批文件、追踪多个 bug 入口。主 Agent 最后并不需要所有过程，只需要结构化总结。

第三，**天然可以拆成独立 workstreams**。比如同时研究三种方案、分别 review 安全/性能/可维护性、让不同子 Agent 读不同模块。

反过来，不该 delegate 的场景也很明确：

- 单次工具调用：直接用工具；
- 机械流程：用 `execute_code`；
- 需要持续问用户的问题：子 Agent 不能 `clarify`；
- 很小的文件修改：直接做；
- 必须跨 turn 存活的长任务：用 `cronjob` 或 `terminal(background=True, notify_on_complete=True)`。

这里最容易忽略的是最后一点：`delegate_task` 是同步的。它运行在父 Agent 当前 turn 里。如果父 turn 被打断，子 Agent 会被 cancel，未完成工作会丢掉。所以它适合“当前回合内完成的并行子任务”，不是后台任务队列。

## 3. Pattern 1：Parallel Research

最经典的模式是 parallel research：把多个互相独立的研究问题拆给多个子 Agent。

比如用户说：

```text
Research these three topics in parallel:
1. Current state of WebAssembly outside the browser
2. RISC-V server chip adoption in 2025
3. Practical quantum computing applications

Focus on recent developments and key players.
```

Hermes 背后可以把它拆成：

```python
delegate_task(tasks=[
    {
        "goal": "Research WebAssembly outside the browser in 2025",
        "context": "Focus on: runtimes (Wasmtime, Wasmer), cloud/edge use cases, WASI progress",
        "toolsets": ["web"],
    },
    {
        "goal": "Research RISC-V server chip adoption",
        "context": "Focus on: server chips shipping, cloud providers adopting, software ecosystem",
        "toolsets": ["web"],
    },
    {
        "goal": "Research practical quantum computing applications",
        "context": "Focus on: error correction breakthroughs, real-world use cases, key companies",
        "toolsets": ["web"],
    },
])
```

这个模式的重点不是“并行搜索更快”，而是**每个子 Agent 都有独立的研究视角**。它们不会互相污染上下文，也不会把几十条搜索结果塞进主对话。父 Agent 最后拿到三份 summary，再合成 briefing。

适合的场景：

- 多个技术方向对比；
- 多家公司/产品调研；
- 多篇论文快速扫读；
- 为一篇长文收集素材；
- 市场、竞品、开源项目并行研究。

## 4. Pattern 2：Code Review

第二个模式是把 code review 委派给 fresh-context subagent。

例如：

```text
Review the authentication module at src/auth/ for security issues.
Check for SQL injection, JWT validation problems, password handling,
and session management. Fix anything you find and run the tests.
```

对应的 `delegate_task` 应该把所有必要背景写进 `context`：

```python
delegate_task(
    goal="Review src/auth/ for security issues and fix any found",
    context="""Project at /home/user/webapp. Python 3.11, Flask, PyJWT, bcrypt.
    Auth files: src/auth/login.py, src/auth/jwt.py, src/auth/middleware.py
    Test command: pytest tests/auth/ -v
    Focus on: SQL injection, JWT validation, password hashing, session management.
    Fix issues found and verify tests pass.""",
    toolsets=["terminal", "file"],
)
```

这段示例其实暴露了 delegation 的第一原则：**子 Agent 什么都不知道。**

它不知道刚才你们讨论了什么，不知道项目目录在哪里，不知道测试命令，也不知道哪些文件能改、哪些不能改。父 Agent 必须把路径、错误、运行方式、约束、预期输出都写清楚。

Code review 特别适合 delegation，因为它有两个好处：

1. 子 Agent 可以用新上下文重新审视代码，减少父对话里已有假设的影响；
2. review 过程会读很多文件，但父 Agent 最后只需要风险、证据、patch summary 和测试结果。

但这里也有一个硬规则：**子 Agent 的 summary 不是事实本身。** 如果它说“tests pass”，父 Agent 仍然应该自己验证测试或至少检查 diff。

## 5. Pattern 3：Compare Alternatives

第三个模式是 parallel alternatives：让多个子 Agent 分别评估不同方案，然后父 Agent 做最终决策。

官方例子是给 Django app 增加全文搜索：

1. PostgreSQL `tsvector`；
2. Elasticsearch + `django-elasticsearch-dsl`；
3. Meilisearch + `meilisearch-python`。

每个子 Agent 只研究一个方案，并从 setup complexity、query capabilities、resource requirements、maintenance overhead 等维度输出结论。

这种模式的好处是：**隔离带来公平性。**

如果一个 Agent 在同一个上下文里连续研究三个方案，很容易被第一个方案的叙事带偏。拆成三个子 Agent 后，每个方案都有独立论证，父 Agent 再统一做 trade-off table。

这对产品和架构决策很有用：

- 选数据库；
- 选向量库；
- 选 job queue；
- 选云服务；
- 选 LLM provider；
- 选视频生成/语音识别/浏览器自动化方案。

最终输出最好不是“推荐 A”，而是一张决策表：成本、复杂度、风险、迁移难度、适合场景、不适合场景。

## 6. Pattern 4：Multi-File Refactoring

第四个模式是大范围重构。核心思路是：**并行可以提高速度，但只能并行互不重叠的文件。**

官方示例把 API response format 改造拆成三条线：

- 子 Agent A：改 API endpoint handlers；
- 子 Agent B：改 client SDK；
- 子 Agent C：改 API docs。

每个子 Agent 都拿到明确文件列表、旧格式、新格式、import 路径和测试命令。

这类任务的收益很明显：如果三个子任务编辑不同目录，parallel work 可以大幅减少等待时间。但风险也同样明显：如果两个子 Agent 同时改同一个文件，就可能产生冲突或互相覆盖。

所以 multi-file refactoring 的实用规则是：

- 明确列出每个子 Agent 负责的文件；
- 不要让两个子 Agent 写同一文件；
- 共享文件留给父 Agent 最后统一处理；
- 子 Agent 完成后，父 Agent 必须看 diff、跑测试、做最终集成；
- 如果是 git repo，最好配合 worktree 或清晰的分支策略。

Delegation 在这里像一个 mini build farm，但父 Agent 仍然是 release manager。

## 7. Pattern 5：Gather Then Analyze

这篇 guide 最值得借鉴的模式是 `Gather Then Analyze`：机械收集用 `execute_code`，高层分析用 `delegate_task`。

官方示例是先用 `execute_code` 批量搜索、提取网页、保存 JSON：

```python
execute_code("""
# collect search results and extracted pages
# save to /tmp/ai-funding-data.json
""")
```

然后再把分析任务交给子 Agent：

```python
delegate_task(
    goal="Analyze AI funding data and write a market report",
    context="""Raw data at /tmp/ai-funding-data.json contains search results and
    extracted web pages about AI funding, acquisitions, and IPOs in Q1 2026.
    Write a structured market report: key deals, trends, notable players,
    and outlook. Focus on deals over $100M.""",
    toolsets=["terminal", "file"],
)
```

这个模式非常重要，因为它避免了一个常见误区：把所有事情都交给 LLM 子 Agent。

如果任务只是“循环调用十几个工具、整理 JSON、去重、过滤”，`execute_code` 更便宜、更稳定、更可控。等数据收集完成后，再让子 Agent 做判断、归纳、写报告。

换句话说：

- **机械步骤用代码；**
- **判断步骤用 Agent；**
- **最终 synthesis 由父 Agent 负责。**

这是很多复杂工作流最省 token、也最可靠的结构。

## 8. Toolset selection：不要给子 Agent 过多权限

官方 guide 给了一个简单表：

| 任务类型 | Toolsets | 原因 |
|---|---|---|
| Web research | `["web"]` | 只需要搜索和网页提取 |
| Code work | `["terminal", "file"]` | 需要 shell 和文件操作 |
| Full-stack | `["terminal", "file", "web"]` | 同时需要本地与网络 |
| Read-only analysis | `["file"]` | 只读文件，不需要执行命令 |

这个表背后的原则是最小权限。研究子 Agent 不该拿 terminal；只读 review 不该有写文件权限；本地代码任务不一定需要 web。

这不只是安全问题，也是认知问题。工具越多，子 Agent 越容易走偏。好的 delegation prompt 应该让子 Agent 很难做错事。

## 9. 并发和深度：parallelism 有乘法成本

Hermes 默认 batch concurrency 是 3，可以通过 `delegation.max_concurrent_children` 调整。文档也说明没有硬上限，只有 floor of 1。但这不代表应该随便开到 30。

并行数越大，成本、日志量、冲突概率、验证负担都会上升。尤其是 nested delegation：默认 leaf subagent 不能再调用 `delegate_task`。只有 `role="orchestrator"` 并且 `delegation.max_spawn_depth` 提高后，才允许进一步嵌套。

这意味着 Hermes 默认选择了安全设计：flat delegation first，nested orchestration opt-in。

对大多数实际任务，我会这样用：

- 1 个父 Agent；
- 2-3 个子 Agent；
- 每个子 Agent 做一个明确方向；
- 父 Agent 统一验收和整合；
- 只有任务天然是树状结构时，才考虑 orchestrator children。

## 10. 给 builder 的实用模板

如果你想让 Hermes 并行处理任务，可以直接用这个模板：

```text
Use parallel delegation for these independent workstreams:

1. [Workstream A]
   Scope:
   Sources/files:
   Constraints:
   Output:

2. [Workstream B]
   Scope:
   Sources/files:
   Constraints:
   Output:

3. [Workstream C]
   Scope:
   Sources/files:
   Constraints:
   Output:

Parent task:
- Compare the returned summaries.
- Verify claims that involve file changes or tests.
- Produce the final integrated answer.
- Mention uncertainty explicitly.
```

如果是代码任务，再加上：

```text
Project root:
Test command:
Files allowed to edit:
Files not allowed to edit:
Do not touch shared files unless explicitly listed.
Return changed files, tests run, and remaining risks.
```

## 11. 结论：parallel tasks 的本质是“父 Agent 变成 orchestrator”

`Delegation & Parallel Work` 这篇文档真正想教的不是某个 API，而是一种工作方式：父 Agent 不再把所有事情都塞进一个上下文，而是像项目负责人一样，把任务拆给独立 worker，收回 summary，再做 synthesis 和 verification。

这套模式的边界也很清楚：

- 子 Agent 没有主对话记忆；
- 子 Agent 不能问用户；
- 子 Agent 的工作不会跨 turn 持久运行；
- 子 Agent 的 summary 必须被验证；
- 并发不是越大越好；
- toolsets 应该最小化。

用得好，delegation 可以让 Hermes 从“一个聪明聊天助手”变成“一个能组织并行工作流的 agent runtime”。

真正的关键不是 `delegate_task` 这个函数，而是你是否能把任务拆成清晰、独立、可验收的 workstreams。
