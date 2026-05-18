# Codex Goals Deep Dive: Productizing “Keep Going” into an Auditable Completion Contract

> Source: [Using Goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)  
> Publisher: OpenAI Developers Cookbook  
> Authors: Raj Pathak, Stefano Fabbri  
> Published: 2026-05-09  
> Article date: 2026-05-18  
> Tags: Codex / AI Agent / Goals / Coding Agents / Evidence Loop / Agent Runtime / Developer Tools

![Codex Goals: from one-off prompts to persistent objectives](imgs/codex-goals-persistent-objectives/goal-loop.webp)

OpenAI’s Cookbook article “Using Goals in Codex” appears to introduce a new command: `/goal`. But the real story is not the command surface. It is that OpenAI is turning one of the most common and unstable instructions in AI coding workflows — “keep going until this is actually done” — into a **thread-scoped, pausable, resumable, auditable completion contract**.

That is very different from a normal prompt. A prompt says “do the next thing.” A Goal says “continue working until a verifiable state is true.” The former is right for a one-off edit, explanation, or code review. The latter is designed for performance optimization, flaky tests, migrations, benchmark tuning, complex bug hunts, and research reproductions where the path is uncertain but the finish line can be defined.

Peter’s articles have already covered Codex multi-agent swarms, Figma MCP, and Ask Question. This article takes a different angle: **should long-running AI agent work be driven by prompts, or by verifiable objectives?**

---

## 1. Goals solve continuity and convergence, not just capability

The official definition is direct: Goals are persistent objectives in Codex that keep a thread working toward a defined outcome across turns.

Three words matter:

- **persistent**: the objective survives turns, so the user does not have to keep saying “keep going”;
- **defined outcome**: the target is not an open-ended wish but a completion condition;
- **across turns**: Codex can choose the next action based on what it learned in the previous step.

This is one of the weakest parts of many coding-agent workflows. A model may be capable of running tests, changing code, reading logs, and checking benchmarks. But if every iteration needs manual user steering, the system is only semi-automated. If the loop is fully automatic with no bounded objective, it can drift, burn budget, or overstate uncertain results.

Goals add a state machine between those extremes: the objective persists, but completion must be decided by evidence.

---

## 2. `/goal` is not a longer prompt; it is a completion contract

The basic command is simple:

```bash
/goal Reduce p95 latency below 120 ms without regressing correctness tests
```

Lifecycle controls live on the same surface:

```bash
/goal          # View the current Goal
/goal pause    # Pause
/goal resume   # Resume
/goal clear    # Clear
```

Goals are available starting in Codex `0.128.0`. Installation or update can be done with npm:

```bash
npm install -g @openai/codex@latest
codex --version
```

or Homebrew:

```bash
brew update
brew upgrade --cask codex
codex --version
```

But the critical part is how the Goal is written. The official guide recommends that strong Goals include six elements:

| Element | Purpose |
|---|---|
| Outcome | What should be true when work is done |
| Verification surface | The tests, benchmark, report, artifact, logs, or source material that prove it |
| Constraints | What must not regress |
| Boundaries | Which files, tools, data, repositories, or resources Codex may use |
| Iteration policy | How Codex should choose the next step after each attempt |
| Blocked stop condition | How Codex should stop honestly when no defensible path remains |

This is more important than simply giving the model more context. It turns the task from “try something” into “iterate under an audit standard.”

A thin Goal is:

```bash
/goal Reduce p95 checkout latency below 120 ms without regressing correctness tests
```

A stronger Goal is:

```bash
/goal Reduce p95 checkout latency below 120 ms, verified by the checkout benchmark, while keeping the correctness suite green. Use only the checkout service, benchmark fixtures, and related tests. Between iterations, record what changed, what the benchmark showed, and the next best experiment to try. If the benchmark cannot run or no valid paths remain, stop with the attempted paths, the evidence gathered, the blocker, and the next input needed.
```

That may look verbose, but it defines the agent’s boundary, acceptance criteria, and failure exit. That is what lets a long-running task converge safely.

---

## 3. Architecturally, a Goal is thread-scoped state, not global memory

![What a Goal adds to a thread](imgs/codex-goals-persistent-objectives/goal-state.webp)

The official article emphasizes that Goals are implemented as persisted thread state, not global memory and not project-level instructions.

That design choice matters. The evidence for a Goal usually lives in the current thread: files Codex inspected, commands it ran, diffs it produced, logs it saw, benchmark outputs, and moments where the user interrupted or changed direction.

If a Goal were global memory, it could contaminate future work. If it were a project instruction, it could turn a temporary objective into a permanent development rule. Thread scope is the right boundary: persistent enough to survive multiple turns, local enough not to become a global bias.

The architecture can be read as several layers:

1. **Durable state**: objective, status, budget, and usage;
2. **Lifecycle controls**: active, paused, complete, budget-limited;
3. **Continuation policy**: continue only when the thread is idle, no user input is queued, and no other work is pending;
4. **Evidence check**: completion must be checked against files, tests, logs, benchmarks, or artifacts;
5. **Budget handling**: when the budget is reached, summarize progress and blockers rather than calling the objective complete.

This is not a naïve while loop. It is a controlled continuation layer in the agent runtime.

---

## 4. The product principle: let the objective persist, but let evidence decide

The article’s key sentence is: Codex can keep moving, but the evidence decides whether it is done.

That is a useful product principle for AI agents.

Without Goals, users often send prompts like:

```text
Keep going.
Try the next likely fix.
Run the benchmark again.
Now check the tests.
Continue until this is actually done.
```

Those are not task instructions. They are **control semantics**. If control semantics are repeatedly patched in through natural language, agent behavior becomes unstable: sometimes it stops too early, sometimes it over-acts, and sometimes it treats “I did some work” as “the task is complete.”

A Goal makes those control semantics explicit:

- “continue” becomes an active Goal;
- “done” becomes a verification surface;
- “do not cross this line” becomes constraints and boundaries;
- “stop if this is blocked” becomes a blocked stop condition;
- “do not run forever” becomes a budget.

That is the shift from prompt engineering to agent-runtime engineering.

---

## 5. Why research reproduction is the strongest example

The article’s complex case study is reproducing Buehler et al.’s Deep Hedging paper. This example is more revealing than a normal performance optimization task because research reproduction is inherently uncertain:

- original random seeds may be missing;
- training paths may be unavailable;
- checkpoints may be missing;
- TensorFlow graphs, optimizer state, and full simulation state may be unavailable;
- some claims can be approximately supported but not exactly replayed.

The weak Goal is:

```bash
/goal Reproduce Buehler et al., "Deep Hedging"
```

The stronger Goal is:

```bash
/goal Produce the strongest evidence-backed reproduction of Buehler et al., "Deep Hedging," using the available paper materials and local resources. Attempt every headline result, verify the outputs, and end with a report that separates reproduced mechanics, approximate trained results, blocked exact replay, and remaining uncertainty.
```

Notice what this does. It does not require Codex to “succeed” at all costs. It asks Codex to maximize evidence and stratify the conclusion:

- reproduced mechanics;
- approximate trained results;
- blocked exact replay;
- remaining uncertainty.

That is critical. Many AI-agent failures are not failures to act. They are failures to distinguish proxy evidence, partial reconstruction, and exact reproduction. A Goal predefines the epistemic boundary: what counts as confirmed, what only supports a claim, what is blocked, and what remains unknown.

![Complex research tasks need an evidence ledger, not a single success claim](imgs/codex-goals-persistent-objectives/evidence-ledger.webp)

---

## 6. Lessons for systems like OpenClaw, Hermes, and QCut

This Cookbook article is useful for any agent runtime, not just Codex.

### First: long-running tasks need explicit objective state

If a task may span multiple turns, tools, or test results, the system should have an explicit objective state. It should not live only in chat history, and it should not rely on repeated “please continue” messages.

### Second: completion should bind to evidence, not model self-assessment

The dangerous agent phrase is “this should work now.” For code tasks, completion should bind to tests, benchmarks, diffs, and artifacts. For research tasks, it should bind to sources, reproduction scripts, tables, error ranges, and reasons something cannot be reproduced.

### Third: pause / resume / clear are product capabilities, not accessory buttons

Real agent work is interrupted. Users jump in, budgets expire, environments fail, tests are flaky, and requirements change. Goal lifecycle controls make those states first-class.

### Fourth: a blocked stop condition is more important than “never give up”

An industrial-grade agent should not try forever. When no valid path remains, it should stop and report what it tried, what evidence it collected, what blocked progress, and what input would unlock the next step.

This is especially relevant to Peter’s article-writing jobs, repo deep dives, QCut engineering tasks, and OpenClaw multi-agent orchestration. The target should not be “agents that run forever.” It should be “agents that know when to continue, when to stop, and how to explain both.”

---

## 7. When not to use Goals

The official guide gives useful counterexamples.

Do not use a Goal for:

- a one-line edit;
- a simple explanation;
- a short code review;
- a question that needs one answer and then a stop;
- vague “make this better” requests;
- open-ended wishes without tests, benchmarks, artifacts, or an evidence surface.

If the task does not have a durable objective, an evidence-based finish line, and a multi-turn investigation path, a normal prompt is better.

That is also good product judgment. Not everything should be agentified. Goals are not about making Codex more “autonomous” in the abstract. They are about making inherently multi-step work more controllable.

---

## 8. Conclusion: Goals move Codex from tool toward runtime

`/goal` looks like a command, but it introduces a different operating model for Codex: isolated prompts become a stateful work loop.

The key is not “automatic continuation.” The key is “continuation inside a user-defined contract.” The objective persists inside the thread, lifecycle is controlled, budget is visible, completion requires evidence, and blockers must be reported honestly.

For coding agents, that may matter more than raw model capability. The hard part in real engineering tasks is often not whether the model can write the next patch. It is whether the system can:

- remember the final objective;
- choose the next step after failure;
- stay within boundaries;
- prove completion through tests and benchmarks;
- stop honestly when completion is not possible.

Codex Goals’ answer is: let the objective persist, but let evidence decide.

That is the direction agent runtimes need to move: not unlimited autonomy, but **verifiable, pausable, resumable, auditable work loops**.
