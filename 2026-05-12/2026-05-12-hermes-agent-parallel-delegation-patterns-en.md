# Hermes Agent Parallel Tasks Guide: From Delegation to Orchestration

> Source: <https://hermes-agent.nousresearch.com/docs/guides/delegation-patterns>  
> Related: <https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation>  
> Date: 2026-05-12  
> Tags: Hermes Agent / delegate_task / Parallel Tasks / Subagent Delegation / Multi-Agent Orchestration / Agent Workflow

## 1. This guide is about delegation patterns, not just API parameters

Hermes already has a full `delegate_task` reference covering isolated context, toolsets, concurrency, timeouts, nested delegation, durability, and configuration. The value of the `Delegation & Parallel Work` guide is different: it explains **when to split work out, what shape the split should take, and how the parent agent should integrate the results.**

That is the real engineering problem. Parallel tasks are not just “spawn more agents.” The important questions are:

- which tasks deserve parallelism;
- which tasks should not be delegated;
- what context each child needs;
- which toolsets should be granted;
- how the parent verifies summaries;
- when to use `execute_code`, `cronjob`, or background terminal instead of `delegate_task`.

In short: **delegation patterns are workflow design, not just tool usage.**

## 2. When to delegate

The official guide gives a practical rule: delegate tasks that are reasoning-heavy, context-heavy, or naturally independent.

Good candidates include debugging, code review, research synthesis, codebase exploration, competitor research, and option comparison. These tasks require judgment and often produce lots of intermediate material that the parent conversation does not need to retain.

Bad candidates are just as important:

- single tool call: use the tool directly;
- mechanical multi-step workflow: use `execute_code`;
- tasks requiring user clarification: child agents cannot `clarify`;
- tiny file edits: do them directly;
- durable long-running work: use `cronjob` or `terminal(background=True, notify_on_complete=True)`.

The durability point matters. `delegate_task` is synchronous. It runs inside the parent agent’s current turn. If that turn is interrupted, active children are cancelled and unfinished work is discarded. It is not a background queue.

## 3. Pattern 1: Parallel Research

The most obvious pattern is parallel research: split independent research questions across child agents.

Example request:

```text
Research these three topics in parallel:
1. Current state of WebAssembly outside the browser
2. RISC-V server chip adoption in 2025
3. Practical quantum computing applications

Focus on recent developments and key players.
```

Hermes can translate that into:

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

The main benefit is not merely speed. The main benefit is **independent context**. Each child agent investigates one direction without contaminating the parent context with every search result. The parent receives concise summaries and synthesizes them into one briefing.

This works well for market research, product comparisons, paper surveys, long-form article research, and multi-company competitive analysis.

## 4. Pattern 2: Code Review

A second pattern is delegating code review to a fresh-context subagent.

Example:

```text
Review the authentication module at src/auth/ for security issues.
Check for SQL injection, JWT validation problems, password handling,
and session management. Fix anything you find and run the tests.
```

The key is to pass all required context explicitly:

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

This example illustrates the first law of delegation: **subagents know nothing.** They do not know the previous conversation, project paths, test commands, risk boundaries, or implicit assumptions. The parent must write those into `goal` and `context`.

Code review is a strong use case because the child can approach the module without the parent conversation’s bias, read many files, and return only the important risks, evidence, patch summary, and test outcome.

But the parent must still verify. A subagent summary is a report, not proof. If it says “tests pass,” the parent should check the diff and run or inspect the tests.

## 5. Pattern 3: Compare Alternatives

Another powerful pattern is parallel option comparison.

The official guide uses full-text search for a Django app as the example:

1. PostgreSQL `tsvector`;
2. Elasticsearch with `django-elasticsearch-dsl`;
3. Meilisearch with `meilisearch-python`.

Each child evaluates one option across setup complexity, query capabilities, resource requirements, and maintenance overhead. The parent then builds the final trade-off table.

The benefit is fairness. If one agent studies all options sequentially, the first option can frame the rest of the analysis. Separate subagents let each option stand on its own merits before synthesis.

This is useful for choosing databases, vector stores, job queues, cloud providers, LLM providers, video models, speech APIs, or browser automation stacks.

The final answer should usually be a decision matrix, not just “choose A.”

## 6. Pattern 4: Multi-File Refactoring

For large refactors, delegation can split work across independent parts of the codebase.

The guide’s example changes an API response format across three workstreams:

- endpoint handlers;
- client SDK methods;
- API documentation.

Each child receives explicit file lists, old format, new format, imports, and tests.

The rule is simple: **parallelize across different files, not the same file.**

If two subagents may edit the same file, do not delegate that file to both. Keep shared files for the parent agent to handle after the child work completes. The parent remains responsible for checking diffs, running tests, resolving conflicts, and doing final integration.

Delegation here behaves like a small build farm, but the parent agent is still the release manager.

## 7. Pattern 5: Gather Then Analyze

The most important pattern in the guide may be `Gather Then Analyze`.

The idea: use `execute_code` for mechanical data collection, then use `delegate_task` for reasoning-heavy analysis.

For example, `execute_code` can loop through many search queries, extract pages, deduplicate results, and save structured JSON. Then a child agent analyzes the collected data and writes a market report.

This avoids a common mistake: using LLM subagents for everything.

A better split is:

- **mechanical steps → code;**
- **judgment steps → agent;**
- **final synthesis → parent.**

This pattern is often cheaper, more reliable, and easier to verify than letting a subagent perform many repetitive tool calls.

## 8. Toolset selection: use least privilege

The guide gives a simple toolset table:

| Task type | Toolsets | Why |
|---|---|---|
| Web research | `["web"]` | Search and extraction only |
| Code work | `["terminal", "file"]` | Shell plus file operations |
| Full-stack | `["terminal", "file", "web"]` | Local and online context |
| Read-only analysis | `["file"]` | Can read files without shell |

The principle is least privilege. A web research subagent should not need terminal access. A read-only reviewer should not need write access. A local code task may not need web.

This is not only about safety. It also keeps the child focused. Fewer tools means fewer ways to wander away from the task.

## 9. Concurrency and depth: parallelism has multiplicative cost

Hermes defaults to 3 concurrent children per batch, configurable through `delegation.max_concurrent_children`. There is no hard ceiling, but that does not mean “set it to 30” by default.

More workers means more cost, more logs, more conflicts, and more verification burden.

Nested delegation is also opt-in. Leaf children cannot call `delegate_task`. Orchestrator children only retain delegation when `role="orchestrator"` is used and `delegation.max_spawn_depth` is raised above the default of 1.

The default design is intentionally safe: flat delegation first, nested orchestration only when explicitly enabled.

For most real tasks, a good pattern is:

- one parent agent;
- two or three child agents;
- one clear direction per child;
- parent verifies and integrates;
- nested orchestration only for naturally tree-shaped work.

## 10. A practical prompt template

Use this template when you want Hermes to run parallel workstreams:

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

For code tasks, add:

```text
Project root:
Test command:
Files allowed to edit:
Files not allowed to edit:
Do not touch shared files unless explicitly listed.
Return changed files, tests run, and remaining risks.
```

## 11. Conclusion: parallel tasks turn the parent agent into an orchestrator

The core lesson of `Delegation & Parallel Work` is not an API trick. It is an operating model: the parent agent becomes an orchestrator. It decomposes work, gives each child a clear contract, receives summaries, verifies claims, and performs final synthesis.

The boundaries are equally important:

- child agents do not inherit conversation history;
- child agents cannot ask the user;
- `delegate_task` does not survive parent-turn interruption;
- summaries must be verified;
- parallelism should be bounded;
- toolsets should be minimal.

Used well, delegation turns Hermes from a single smart assistant into an agent runtime that can coordinate parallel workstreams. The hard part is not calling `delegate_task`; the hard part is carving work into clear, independent, verifiable units.
