# gstack Deep Dive: Office Hours + CEO Review — YC's CEO Built an AI Product Thinking Toolchain

> **TL;DR:** Garry Tan (YC CEO) open-sourced gstack — a system that turns Claude Code into a virtual engineering team via Markdown skill files. This article focuses on two "thinking" skills that write zero code but determine whether every line you write afterwards is worth writing: `/office-hours` (product diagnostic) and `/plan-ceo-review` (CEO-level plan review).

**Source:** [donghaozhang/gstack](https://github.com/donghaozhang/gstack) (fork of garrytan/gstack)

---

## Context: One Person Shipping 10,000-20,000 Lines Per Day

In the gstack README, Garry Tan drops a staggering number: over **600,000 lines of production code** in 60 days, 35% tests, while running YC full-time. His last 7-day retro across 3 projects: **140,751 lines added, 362 commits, ~115K net LOC**.

The secret isn't working harder. It's turning Claude Code into an **18-person virtual team** — CEO, eng manager, designer, QA, release engineer — all defined as Markdown skill files, all MIT-licensed.

The core philosophy is called **"Boil the Lake"**: AI makes the marginal cost of completeness near-zero, so always choose the complete implementation. Never take shortcuts.

---

## `/office-hours`: Six Lethal Questions Before Writing Code

This skill simulates YC Office Hours. The goal: **make sure you understand the problem before proposing solutions.**

### Two Modes

| Mode | When to Use | Style |
|------|------------|-------|
| **Startup Mode** | Startups / intrapreneurship | Hard diagnostic, no mercy |
| **Builder Mode** | Hackathons / open source / learning / side projects | Enthusiastic collaborator, design thinking |

### Startup Mode: The Six Forcing Questions

Smart-routed based on product stage — you don't always get all six:

- **Pre-product (idea stage) →** Q1 Demand Reality, Q2 Status Quo, Q3 Desperate Specificity
- **Has users →** Q2 Status Quo, Q4 Narrowest Wedge, Q5 Observation
- **Has paying customers →** Q4 Narrowest Wedge, Q5 Observation, Q6 Future-Fit

**Q1 — Demand Reality**

> "What's the strongest evidence you have that someone actually wants this — not 'is interested,' not 'signed up for a waitlist,' but would be genuinely upset if it disappeared tomorrow?"

Red flags 🚩:
- "People say it's interesting" — interest is free
- "We got 500 waitlist signups" — signups aren't demand
- "VCs are excited about the space" — that's not your demand

**Q2 — The Status Quo Is Your Real Competitor**

Not the other startup, not the big company — the cobbled-together spreadsheet-and-Slack-messages workaround your user already lives with. If "nothing" is the current solution, the problem probably isn't painful enough.

**Q3 — Desperate Specificity**

"Enterprises in healthcare" is not a customer. You need: a name, a role, a company, a reason.

**Q4 — Narrowest Wedge**

> "What's the smallest version someone would pay real money for this week?"

If no one can get value from a smaller version, the value proposition itself isn't clear — not that the product needs to be bigger.

### Anti-Sycophancy Rules

This is the **strictest anti-sycophancy instruction set** I've ever seen in a production AI tool:

❌ Never say:
- "That's an interesting approach" — take a position instead
- "You might want to consider..." — say "This is wrong because..."
- "That could work" — say whether it WILL work and what evidence is missing

✅ Always:
- **Take a position** on every answer
- State what evidence would change your position
- Challenge the **strongest version** of the founder's claim, not a strawman

### Output

No code. Only a **design document**, auto-saved to `~/.gstack/projects/`, ready for `/plan-ceo-review` to consume.

---

## `/plan-ceo-review`: CEO-Level Plan Review

With the design doc in hand, this skill enters **Mega Plan Review Mode** — evaluating the entire plan through the lens of a CEO.

### Four Review Modes

| Mode | Posture | Key Phrase |
|------|---------|-----------|
| **SCOPE EXPANSION** | Build a cathedral. Envision the platonic ideal. | "10x better for 2x effort" |
| **SELECTIVE EXPANSION** | Hold scope, evaluate expansions individually | Cherry-pick |
| **HOLD SCOPE** | Pure defense. Find every failure mode. | Bulletproof |
| **SCOPE REDUCTION** | Surgical. Cut to minimum viable. | Ruthless |

Critical rule: **the user is 100% in control**. Every scope change is an explicit opt-in. No silent additions or removals.

### Nine Prime Directives

1. **Zero silent failures** — every failure mode must be visible
2. **Every error has a name** — not "handle errors" but the specific exception class, trigger, catch, user-visible result, and whether it's tested
3. **Data flows have shadow paths** — happy path + nil input + empty input + upstream error = 4 paths per flow
4. **Interactions have edge cases** — double-click, navigate-away-mid-action, slow connection, stale state, back button
5. **Observability is scope** — dashboards, alerts, and runbooks are first-class deliverables
6. **Diagrams are mandatory** — ASCII art for every non-trivial flow
7. **Everything deferred must be written down** — vague intentions are lies. TODOS.md or it doesn't exist
8. **Optimize for 6 months out** — if today's fix is next quarter's nightmare, say so
9. **Permission to say "scrap it"** — if there's a fundamentally better approach, surface it now

### 18 CEO Cognitive Patterns

This is the **highest information-density section** in all of gstack. Key highlights:

- **Bezos Two-Way Doors** — most decisions are reversible. Move fast. Only slow down for irreversible + high-magnitude decisions.
- **Munger Inversion** — after asking "how do we win?", ask "what would make us fail?"
- **Jobs Focus as Subtraction** — went from 350 products to 10. Default: do fewer things, better.
- **70% Information Is Enough** — by the time you have 90%, you're too slow (Bezos)
- **Horowitz Wartime Awareness** — correctly diagnose peacetime vs. wartime. Peacetime habits kill wartime companies
- **Altman Leverage Obsession** — find inputs where small effort creates massive output. Technology is the ultimate leverage

### The Completeness Principle

| Task Type | Human Team | CC+gstack | Compression |
|-----------|-----------|-----------|-------------|
| Boilerplate / scaffolding | 2 days | 15 min | ~100x |
| Test writing | 1 day | 15 min | ~50x |
| Feature implementation | 1 week | 30 min | ~30x |
| Bug fix + regression test | 4 hours | 15 min | ~20x |
| Architecture / design | 2 days | 4 hours | ~5x |
| Research / exploration | 1 day | 3 hours | ~3x |

Core argument: **"good enough" is the wrong instinct in the AI era.** When "complete" costs minutes more, always choose complete.

---

## The Full Sprint Flow

```
/office-hours → Design document
      ↓
/plan-ceo-review → CEO review (scope, ambition, cognitive biases)
      ↓
/plan-eng-review → Eng review (architecture diagrams, test matrix, failure modes)
      ↓
Implementation (AI writes, you review)
      ↓
/review → Auto-fix + human confirmation
      ↓
/qa → Real browser click-through testing
      ↓
/ship → Tests + PR
```

One person, one feature sprint, about 30 minutes. But here's the game-changer: **you can run 10-15 of these sprints in parallel.** Different features, different branches, different agents.

---

## Takeaways for Builders

1. **Diagnose before you operate.** The six forcing questions from `/office-hours` can be used standalone — no gstack, no Claude Code needed. Next time someone says "I have an idea," try these six questions.

2. **Anti-sycophancy can be engineered.** gstack bans specific sycophantic phrases via Markdown instructions and requires the AI to take a position on every answer. This pattern is portable to any AI workflow.

3. **"Boil the Lake" reframes decision-making.** When AI makes complete implementation only 5 minutes more expensive, the old "ship MVP first" playbook needs recalibration. MVP isn't wrong — but the granularity of what counts as MVP has shifted.

4. **CEO cognitive patterns are universal.** Those 18 patterns aren't just for code review — product decisions, hiring, fundraising, strategy planning, all of it applies.

---

## Links

- **gstack source:** <https://github.com/donghaozhang/gstack>
- **office-hours SKILL.md:** <https://github.com/donghaozhang/gstack/blob/main/office-hours/SKILL.md>
- **plan-ceo-review SKILL.md:** <https://github.com/donghaozhang/gstack/blob/main/plan-ceo-review/SKILL.md>
- **Garry Tan "Boil the Ocean" essay:** <https://garryslist.org/posts/boil-the-ocean>

---

*Written 2026-03-23 | A complete teardown of gstack's office-hours + plan-ceo-review skills*

🦞
