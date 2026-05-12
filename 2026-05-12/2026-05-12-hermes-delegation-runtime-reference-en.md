# Hermes Agent Delegation Runtime Reference: `delegate_task` Is Not a Background Queue, but a Controlled Subagent Scheduler

> Source: <https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation>  
> Related: [[2026-05-09/2026-05-09-hermes-agent-delegation-guide-en|Practical Guide to Hermes Agent Delegation]] / [[2026-05-12/2026-05-12-hermes-agent-parallel-delegation-patterns-en|Hermes Agent Parallel Tasks Guide]]  
> Date: 2026-05-12  
> Tags: Hermes Agent / delegate_task / Subagent Runtime / Agent Orchestration / Toolsets / Reliability

![Hermes Agent banner](imgs/hermes-delegation-runtime-reference/hermes-agent-banner.png)

## 1. Read this doc as a runtime contract

The official Hermes Subagent Delegation page looks like a reference for `delegate_task`: how to run a single subtask, how to run a parallel batch, what the default concurrency is, and which tools a child agent may use. But the more important reading is this: **the page defines the runtime boundary of Hermes multi-agent execution.**

Two earlier articles already covered neighboring angles:

- the May 9 article explained why complex work should be split into subagents;
- the May 12 Parallel Tasks article explained workflow patterns such as parallel research, code review, and alternative comparison.

This article takes a different angle: it treats the official delegation page as a runtime contract. What does `delegate_task` guarantee? What does it deliberately refuse to guarantee? When should you switch to `execute_code`, `cronjob`, or a separate background Hermes process instead?

Short version: **`delegate_task` is not “opening more chat windows,” and it is not a background job queue. It is a synchronous subtask scheduler inside the parent agent's current turn.**

## 2. The core semantic: every subagent is a fresh conversation

The most important line in the documentation is that a subagent starts with a completely fresh conversation. It only knows what the parent explicitly passes through `goal` and `context`.

It does not know:

- what the user said earlier;
- which files the parent already read;
- which command produced an error;
- the project path, test command, or risk boundary;
- which files may be changed and which must not be touched.

So this call is essentially under-specified:

```python
delegate_task(goal="Fix the error")
```

To the child, “the error” is meaningless. A better call looks like a small issue ticket:

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

This is the first engineering rule of delegation: **the quality of a delegated task is bounded by the quality of the context the parent provides.** A subagent is not a memory clone. It is an independent worker receiving a work order.

## 3. Parallel batches: default concurrency is 3, but that is not an invitation to split everything

The docs say that `tasks=[...]` batch mode runs up to 3 subagents concurrently by default. The value can be changed with `delegation.max_concurrent_children` or `DELEGATION_MAX_CONCURRENT_CHILDREN`. Batches larger than the limit produce a tool error instead of being silently truncated.

Several runtime details matter:

| Runtime behavior | Meaning |
|---|---|
| Default concurrency of 3 | Enough for common research, review, and comparison tasks without exploding cost by default |
| Results are returned in input order | The parent receives a predictable structure even if tasks finish in a different order |
| CLI shows a live tree view | Each child’s tool calls and completion line can be observed |
| Gateway progress is batched | Discord/Telegram users are not spammed by every child tool call |
| Interrupting the parent interrupts active children | This is the clearest sign that delegation is not a durable queue |

Raising concurrency is not automatically better. As concurrency grows, the hard problem changes from speed to orchestration:

- Are the subtasks truly independent?
- Could they modify the same files?
- Could they fight over the same git index?
- Can the parent verify several summaries rather than trusting them?
- Are rate limits and cost still acceptable?

If the work is “convert 100 files mechanically,” `delegate_task` is probably the wrong tool. Use `execute_code` or a terminal script instead.

## 4. Toolsets are a permission boundary, not just a performance knob

The `toolsets` parameter looks like a convenience setting, but it is also a permission boundary for the child agent.

The common patterns are straightforward:

| Toolsets | Good for |
|---|---|
| `["web"]` | Research, fact-checking, documentation lookup |
| `["terminal", "file"]` | Code changes, debugging, builds, tests |
| `["terminal", "file", "web"]` | Full-stack tasks that need both docs and code edits |
| `["file"]` | Read-only analysis or review without execution |
| `["terminal"]` | System administration, process checks, environment diagnostics |

Some tools are blocked for subagents by design:

- `clarify`: children cannot ask the user questions;
- `memory`: children cannot write shared long-term memory;
- `send_message`: children cannot send cross-platform messages;
- `execute_code`: children should operate through the reasoning loop;
- `delegate_task`: leaf children cannot recursively spawn more children.

That is a sensible safety model: **the parent agent owns user interaction and external side effects; child agents execute bounded work orders under restricted permissions.**

If every child could send messages, write memory, and spawn more children, the system would quickly become un-auditable recursive automation. Hermes' defaults force a clean distinction between orchestrator and worker.

## 5. Nested orchestration: flat by default, recursion must be explicit

The docs also mention `role="orchestrator"` and `delegation.max_spawn_depth`. By default, delegation is flat: the parent can spawn children, but those children cannot spawn grandchildren.

To allow a child to delegate further, the parent can request an orchestrator child:

```python
delegate_task(
    goal="Survey three code review approaches and recommend one",
    role="orchestrator",
    context="...",
)
```

But this only works if `max_spawn_depth` is raised from the default of 1 to 2 or 3.

This is powerful, but it is also dangerous. The documentation warns that with `max_spawn_depth=3` and `max_concurrent_children=3`, the tree can reach 3×3×3 = 27 leaf agents. Cost, rate limits, logging, verification, and side-effect control all become harder.

I would treat nested orchestration as an advanced feature, not the default path. Most workflows only need flat batching: the parent decomposes work, leaf agents execute, and the parent synthesizes and verifies.

## 6. Lifetime: the easiest part to misuse

`delegate_task` is synchronous. It runs inside the parent agent's current turn. The parent waits until all children finish or are cancelled. It is not a background job queue.

Three consequences follow:

1. if the user sends a new message and interrupts the current turn, active children are interrupted too;
2. children do not continue after the parent turn ends;
3. interrupted children may return `status="interrupted"`, but because the parent was interrupted too, that result may never become visible to the user.

Long-running work should use a different mechanism:

| Need | Better mechanism |
|---|---|
| Current-turn parallel research or review | `delegate_task` |
| Mechanical collection, conversion, or batch processing | `execute_code` |
| Scheduled or delayed one-shot task that reports back later | `cronjob(action="create")` |
| Independent long-running task with pollable logs | `terminal(background=True, notify_on_complete=True)` plus `hermes chat -q` |
| Multiple article/code agents editing the same repo | Separate Hermes processes plus git worktrees or careful selective staging |

This is why “write several articles at once” should not simply be stuffed into one `delegate_task(tasks=[...])`. The parent turn may be interrupted, and several children may fight over README, MOC, and the git index. Separate background processes, ideally with worktrees, are more robust.

## 7. `delegate_task` vs `execute_code`: the decision is whether judgment is required

The official comparison is clear:

- `delegate_task`: full LLM reasoning loop, isolated context, tool access, higher token cost, best for judgment-heavy tasks;
- `execute_code`: a Python script with tool RPC, no conversation, lower cost, best for deterministic workflows.

My simpler rule:

> If the process can be written as a deterministic script, use `execute_code`. If it needs a fresh mind to read, judge, trade off, and summarize, use `delegate_task`.

Examples:

- “Scan 200 Markdown files and list which lack frontmatter” → `execute_code`;
- “Read these 20 files and decide where the architecture is weakest” → `delegate_task`;
- “Fetch all these URLs and extract titles” → `execute_code`;
- “Compare these products and identify the real startup opportunity” → `delegate_task`.

## 8. A practical delegation checklist

Before delegating, the parent agent should ask:

- Does this subtask truly require reasoning?
- Can it finish inside the current turn?
- Is it independent from the other subtasks?
- Is `goal` clear enough for a stranger to execute?
- Does `context` include paths, errors, constraints, test commands, and expected output?
- Are the toolsets minimal?
- Could the child produce external side effects?
- How will the parent verify the summary?
- If it fails or is interrupted, what is the fallback?

If these questions are not answerable, do not delegate yet. Not every complex task needs more agents. Often it needs a better task definition.

## 9. Conclusion: delegation is controlled parallelism, not automatic surrender

Hermes' `delegate_task` is intentionally conservative: fresh context, restricted toolsets, flat by default, synchronous lifetime, final-summary-only return. These constraints are not weaknesses. They are what make multi-agent execution auditable.

The best delegation users are not the ones who spawn the most subagents. They are the ones who can answer three questions:

1. Why is this work worth splitting out?
2. What does the child need to know, what may it do, and what must it not do?
3. How will the parent verify the result and remain responsible for the final answer?

Once those questions are clear, `delegate_task` stops being a parallelism trick and becomes a reliable engineering tool for agent workflows.