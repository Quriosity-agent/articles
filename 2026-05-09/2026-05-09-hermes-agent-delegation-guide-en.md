# Practical Guide to Hermes Agent Delegation: Splitting Complex Work Across Subagents

> Source: <https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation>  
> Date: 2026-05-09  
> Tags: Hermes Agent / delegate_task / Subagent Delegation / Multi-Agent / Agent Orchestration / Workflow

![Hermes Agent banner](imgs/hermes-agent-delegation-guide/hermes-agent-banner.png)

## 1. Delegation is not just “more agents” — it is cleaner context management

When people first see Hermes Agent’s `delegate_task`, they often think of it as a way to run multiple agents in parallel. That is true, but it is not the most important point.

The real point is: **the parent agent does not need to keep every research step, codebase exploration, debugging attempt, or review thread inside one giant conversation.**

Complex tasks often break down because:

- research produces a lot of intermediate noise;
- codebase exploration touches many files, but only a few conclusions matter;
- one problem needs security, performance, product, and maintainability perspectives;
- several workstreams can run independently;
- the parent conversation should stay clean while subtasks may need trial and error.

Hermes delegation lets the parent agent move those bounded pieces of work into isolated child agents. The parent defines the goal, provides context, sets boundaries, and integrates results. The child agent works independently and returns a final summary.

In one sentence: **`delegate_task` is both a context-management tool and a parallel-workflow tool.**

## 2. What `delegate_task` is

The official documentation describes `delegate_task` as a tool that spawns child `AIAgent` instances. Each child has:

- isolated context;
- restricted toolsets;
- its own terminal session;
- a fresh conversation;
- only its final summary injected back into the parent context.

A minimal example:

```python
delegate_task(
    goal="Debug why tests fail",
    context="Error: assertion in test_foo.py line 42",
    toolsets=["terminal", "file"],
)
```

Batch mode is also supported:

```python
delegate_task(tasks=[
    {"goal": "Research topic A", "toolsets": ["web"]},
    {"goal": "Research topic B", "toolsets": ["web"]},
    {"goal": "Fix the build", "toolsets": ["terminal", "file"]},
])
```

By default, Hermes runs up to 3 concurrent child agents. This can be configured with `delegation.max_concurrent_children` or the `DELEGATION_MAX_CONCURRENT_CHILDREN` environment variable.

## 3. The most important rule: subagents know nothing

This is the most common pitfall.

A child agent is not a memory clone of the parent. It starts with a completely fresh conversation. It does not know:

- what the user said earlier;
- which files the parent already inspected;
- what previous tool calls returned;
- what implicit assumptions were established in the main conversation;
- the real project path, run commands, or risk boundaries.

The child only knows what the parent passes through `goal` and `context`.

This is a bad prompt:

```python
delegate_task(goal="Fix the error")
```

“The error” means nothing to the child.

A better version:

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

The core engineering principle is simple: **do not make the child agent guess hidden context.**

## 4. A practical mental model: editor-in-chief + specialist reporter

Think of the parent agent as an editor-in-chief and the child agent as a specialist reporter.

A good editor does not say: “look into that thing.” A good editor says:

- which angle to investigate;
- what background matters;
- what sources or files to inspect;
- what not to touch;
- what format to deliver;
- which claims need evidence;
- what uncertainty should be reported.

For `delegate_task`, a good delegation prompt usually includes six parts:

1. **Goal** — what this child task should accomplish;
2. **Context** — why it matters and what is already known;
3. **Scope** — what to include and exclude;
4. **Permissions** — whether file writes, commands, or network access are allowed;
5. **Output contract** — bullets, table, file paths, findings, or patch summary;
6. **Uncertainty handling** — state unknowns instead of inventing facts.

Recommended template:

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

## 5. When to use delegation

### 5.1 Documentation research

This article itself is a good example. A parent agent can delegate source-gathering first:

```text
Research the Hermes Agent delegation documentation.
Extract the core mechanics, examples, configuration options, limitations, and pitfalls.
Do not write files. Return a structured bilingual outline with source links.
```

The task is bounded, the deliverable is clear, and there are no risky side effects.

### 5.2 Codebase exploration

Large codebases can easily flood the parent context. Delegate one module to a child:

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

The parent receives the important files, flow, and risks without absorbing every file the child read.

### 5.3 Parallel option comparison

Suppose you are choosing between Redis, Postgres, and SQLite for job state storage. You can assign one child to each option:

- Redis: throughput, expiration, operational complexity;
- Postgres: consistency, queries, schema evolution;
- SQLite: local deployment, locks, concurrency limits.

The parent then merges the three outputs into a decision table.

### 5.4 Multi-perspective review

A single PR can be split into:

- security review;
- performance review;
- maintainability review;
- test coverage review.

Each child focuses on one lens. The parent prioritizes and synthesizes.

### 5.5 Tasks with lots of intermediate work

Good examples include:

- tracing why tests fail;
- finding possible bug entry points;
- reading a batch of papers or docs;
- researching several competitors;
- collecting material for a long article.

These tasks share one property: **the process is long, but the final output should be structured and compact.**

## 6. When not to use delegation

### 6.1 Tiny tasks

Renaming a variable, reading a short file, or checking a single value does not need a subagent. Delegation has coordination cost.

### 6.2 Work that depends heavily on hidden parent context

If a child needs many implicit details from the current conversation, avoid delegation unless you are willing to write those details into `context`.

### 6.3 Tasks requiring constant user clarification

Child agents cannot `clarify` and cannot talk to the user directly. They are good for “take this task and report back,” not for interactive negotiation.

### 6.4 High-risk side effects

Examples include deleting files, editing production config, running database migrations, or broad refactors. These can be delegated only with strict boundaries:

```text
Analysis only. Do not modify files. Do not run destructive commands.
Return a proposed plan and wait for parent approval.
```

## 7. Toolset selection: give the child exactly what it needs

The official docs provide useful patterns:

| Toolsets | Best for |
|---|---|
| `["terminal", "file"]` | Code work, debugging, builds, tests |
| `["web"]` | Research, fact-checking, documentation lookup |
| `["terminal", "file", "web"]` | Full-stack tasks needing local + web access |
| `["file"]` | Read-only code review without execution |
| `["terminal"]` | System administration and process checks |

The principle: **do not grant tools the child does not need.**

If the task is web research, do not grant file or terminal access. If it is local code review, web access may be unnecessary. If it is read-only review, say so explicitly.

Hermes also blocks some tools for child agents. Leaf subagents cannot call `delegate_task`, `clarify`, `memory`, `send_message`, or `execute_code`. This prevents runaway recursion, user-interaction confusion, shared-memory side effects, and external messaging from children.

## 8. Batch mode: parallelism is not automatically better

`delegate_task(tasks=[...])` runs child agents in parallel through a thread pool. Important details:

- default concurrency is 3;
- batches larger than the limit return a tool error rather than being silently truncated;
- results are sorted by input task index, not completion time;
- CLI mode can show a live tree of child tool calls;
- gateway mode batches progress back to the parent progress callback;
- interrupting the parent interrupts all active children.

Batch mode is best for independent tasks whose results can be merged.

Bad example:

1. Child A designs the API;
2. Child B builds the frontend based on A’s API;
3. Child C writes tests based on B’s implementation.

These tasks have dependencies. They should run in stages, not one parallel batch.

## 9. Nested orchestration: possible, but use it carefully

By default, delegation is flat: the parent spawns children, and children cannot spawn grandchildren.

For multi-stage workflows, a parent can spawn an orchestrator child:

```python
delegate_task(
    goal="Survey three code review approaches and recommend one",
    role="orchestrator",
    context="...",
)
```

But there are limits:

- default `max_spawn_depth` is 1, so delegation is flat;
- to let orchestrator children spawn workers, raise `delegation.max_spawn_depth` to 2;
- there is a depth cap;
- `delegation.orchestrator_enabled: false` disables this globally;
- cost can multiply quickly — depth 3 with 3-way fanout can reach 27 leaf agents.

Recommendation: **do not enable nested orchestration until you can clearly draw the task tree.** Start with flat delegation first.

## 10. Lifetime: `delegate_task` is not a durable job queue

This boundary matters.

`delegate_task` is synchronous. It runs inside the parent’s current turn and blocks the parent until children finish or are cancelled. It is not a durable background queue.

If the user sends a new message, `/stop`, or `/new`, active children are cancelled. They do not continue after the parent turn ends.

So:

- short, reasoning-heavy, interruptible subtasks: use `delegate_task`;
- durable long-running work: use `cronjob(action="create")`;
- long shell jobs such as tests, builds, or downloads: use `terminal(background=True, notify_on_complete=True)`.

Delegation is a temporary workgroup inside the current turn, not a persistent worker system.

## 11. `delegate_task` vs `execute_code`

The official docs also compare these two tools. A practical summary:

| Factor | `delegate_task` | `execute_code` |
|---|---|---|
| Nature | Another LLM agent loop | Python script execution |
| Best for | Judgment, exploration, multi-step reasoning | Mechanical data processing and scripted workflows |
| Context | Fresh conversation, explicit context needed | No conversation; script + stdout only |
| Cost | Higher | Lower |
| Parallelism | 3 child agents by default | Single script |
| Output | Child summary | stdout |

Rule of thumb:

- use `delegate_task` when the subtask requires judgment;
- use `execute_code` when it is calculation, filtering, or batch processing;
- use background terminal or cron for long-running durable work.

## 12. Configuration: what is worth tuning

Example config:

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

Practical advice:

- `max_iterations`: maximum tool-calling turns per child; raise for complex code tasks;
- `max_concurrent_children`: default 3 is a safe balance for most machines and API budgets;
- `child_timeout_seconds`: default is 600 seconds; raise for slower reasoning models;
- `model/provider`: use a cheaper/faster child model and keep the strong model for parent synthesis;
- `max_spawn_depth`: keep the default unless you truly need nested orchestration.

If a child times out after making zero API calls, Hermes writes diagnostics to `~/.hermes/logs/subagent-timeout-<session>-<timestamp>.log`, including config snapshot, credential resolution trace, and early errors. This is useful for provider, auth, and tool-schema debugging.

## 13. A delegation prompt I would actually use

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

The value of this template is not politeness; it is reducing ambiguity. It includes path, symptoms, scope, permissions, and output format.

## 14. Five common pitfalls

### Pitfall 1: Writing the task like a riddle

“Check what’s wrong with this repo” is not a task; it is a wish. A child agent needs an executable investigation direction.

### Pitfall 2: Forgetting file permissions

For research, say `Do not modify files`. If edits are allowed, say “make the smallest safe change” and list what not to touch.

### Pitfall 3: Not asking for evidence

Engineering conclusions should include file paths, line numbers, command output, or source links. Otherwise the parent cannot verify them.

### Pitfall 4: Over-parallelizing

Three independent angles are useful. Ten vague tasks produce ten vague summaries.

### Pitfall 5: Skipping parent synthesis

The final artifact is not the child summary. It is the parent’s synthesized decision, article, patch, plan, or user-ready answer.

## 15. Conclusion: `delegate_task` is cognitive outsourcing for the parent agent

Hermes Agent delegation is not multi-agent theater. It makes complex work more controllable:

- child agents handle local complexity;
- the parent keeps the global objective;
- intermediate noise stays in child contexts;
- final conclusions enter the parent context;
- parallelism is used only for truly independent tasks;
- boundaries and output contracts are explicit.

If you remember one sentence, make it this: **use `delegate_task` as if you are briefing a very capable colleague with complete amnesia. The better the brief, the better the delegation.**
