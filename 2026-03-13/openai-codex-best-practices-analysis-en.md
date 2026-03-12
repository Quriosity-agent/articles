# OpenAI Codex Best Practices — A Practical Builder’s Analysis

> Source: OpenAI Developers — Codex Learn / Best Practices  
> URL: https://developers.openai.com/codex/learn/best-practices  
> Published analysis date: 2026-03-13

![OpenAI Codex Best Practices (Open Graph)](https://developers.openai.com/open-graph.png)

*Image source: OpenAI Developers page Open Graph image (`https://developers.openai.com/open-graph.png`). Copyright belongs to OpenAI.*

---

## TL;DR

The most important message in OpenAI’s guide is not “write fancier prompts.”

It’s this: **treat Codex as an engineered teammate system** you configure and improve over time.

For builders, the winning loop looks like:

**Structured task context → durable rules in AGENTS.md → config discipline → MCP integrations → repeatable Skills → scheduled Automations.**

---

## 1) Prompting: optimize for executability, not eloquence

OpenAI recommends a 4-part default structure:

- **Goal**: what should change or be built
- **Context**: relevant files/folders/docs/errors
- **Constraints**: architecture, safety, conventions
- **Done when**: explicit completion criteria

### Builder takeaway

“Done when” is the highest-ROI line in the whole prompt.

Use a standard completion block like:

```text
Done when:
1) tests pass
2) lint/typecheck are clean
3) behavior validated with repro steps
4) risk notes included
```

That shifts Codex from “code generator” to “delivery assistant.”

---

## 2) Plan before coding for hard work

The doc strongly recommends planning first for ambiguous or multi-step tasks:

- Plan mode (`/plan`)
- Ask Codex to interview you and challenge assumptions
- Use `PLANS.md`/execution-plan templates for longer runs

### Builder takeaway

Adopt a simple policy:
- small task: implement directly
- medium task: 5-minute plan first
- large task: written execution plan required

You’ll reduce rework and context drift dramatically.

---

## 3) AGENTS.md is your highest-leverage artifact

OpenAI positions AGENTS.md as the persistent “agent README” auto-loaded into context.

Good AGENTS.md content includes:
- repo layout
- run/build/test/lint commands
- conventions and constraints
- definition of done and verification steps

It can exist at multiple levels:
- global (`~/.codex`)
- repo-level
- subdirectory-level (more local rules win)

### Builder takeaway

If Codex repeats a mistake twice, encode that lesson in AGENTS.md immediately.

Don’t keep re-teaching transiently in prompts.

---

## 4) Configuration beats vibe-prompting

The guide highlights config layering:
- personal defaults in `~/.codex/config.toml`
- repo defaults in `.codex/config.toml`
- CLI overrides for one-offs

Key knobs: model, reasoning effort, sandbox mode, approval policy, profiles, MCP, multi-agent setup.

### Builder takeaway

When quality drops, debug setup before prompt wording:

1. wrong working directory?
2. missing write permissions?
3. model/reasoning mismatch for task complexity?
4. missing or broken connectors/tools?

Many “AI quality” issues are really environment issues.

---

## 5) Push Codex into the full quality loop

OpenAI explicitly suggests not stopping at code generation. Ask Codex to:

- write/update tests
- run checks
- confirm behavior
- review diff for regressions/risk

The `/review` workflow supports base-branch review, uncommitted changes, single commits, and custom review instructions.

### Builder takeaway

Standardize a 3-stage ask:
1) implement
2) validate
3) self-review

Then require a compact report: change summary, test outcomes, residual risks, rollback hint.

---

## 6) MCP: replace paste-heavy workflows with live context

Use MCP when:
- critical context lives outside repo
- data changes often
- tools should be executed, not simulated from pasted notes
- integration must be reusable across team/projects

OpenAI’s practical advice: start with 1–2 high-impact tools, not everything.

### Builder takeaway

Pick one painful manual loop (CI failure triage, incident logs, issue routing, release-note prep) and make that first integration work end-to-end.

Depth beats breadth.

---

## 7) Skills vs Automations: method vs schedule

The guide draws a useful boundary:
- **Skills define the method**
- **Automations define the cadence**

Great Skill candidates:
- log triage
- PR checklist reviews
- migration planning
- incident summaries

Great Automation candidates:
- daily commit summaries
- recurring bug scans
- CI failure checks
- standup draft generation

### Builder takeaway

Automate only after manual execution is stable and predictable.

If a workflow still needs lots of steering, productize it as a Skill first.

---

## 8) Thread hygiene directly impacts quality

OpenAI frames threads as working contexts, not casual chats.

Recommended habits:
- one thread per coherent task
- fork only when work truly diverges
- compact long histories
- offload bounded work to subagents

### Builder takeaway

“A thread per project” usually bloats context and degrades quality.

Use “a thread per task.”

---

## 9) Common early mistakes (builder translation)

From the official anti-pattern list:

1. stuffing durable rules into prompts instead of AGENTS.md/Skills
2. not exposing build/test commands (agent can’t verify)
3. skipping planning on complex tasks
4. granting broad permissions too early
5. running concurrent live threads on same files without worktrees
6. automating before manual reliability exists
7. using giant project-long threads

---

## A practical 7-day rollout plan

**Day 1**: create repo AGENTS.md with real commands + constraints  
**Day 2**: enforce 4-part prompt template  
**Day 3**: default to Plan mode for non-trivial tasks  
**Day 4**: harden `.codex/config.toml` defaults  
**Day 5**: add one high-value MCP integration  
**Day 6**: convert one repeated workflow into a Skill  
**Day 7**: schedule that stable Skill as an Automation

---

## Final perspective

OpenAI’s best-practices page is fundamentally about operating model design:

- Prompting is the entry point, not the system
- Rules should live in artifacts, not memory
- Agent performance is constrained more by workflow architecture than by one-off prompt phrasing

For builders, the goal isn’t “Codex gets it right once.”

It’s “Codex gets it right repeatedly inside a system you can maintain.”

— End 🦞
