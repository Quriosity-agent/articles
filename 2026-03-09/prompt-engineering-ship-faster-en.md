# Prompt Engineering That Actually Works: Ship 10x Faster With AI Coding Agents

> **TL;DR**: Prompt engineering isn't magic words — it's **clarity, structure, and intention**. Based on @nothiingf4's viral thread and real development experience, here are the tactics that actually matter. Core principle: the quality of context you give determines the quality of output you get.

---

## Core Principles

Prompt engineering comes down to three things:

- **Clarity** — AI doesn't read minds. What you say is what you get
- **Structure** — Organized input produces organized output
- **Intention** — Be explicit about what you want. Don't make AI guess

---

## Tactic 1: Role Before Task

```
❌ "Write me a function"
✅ "You are a TypeScript backend engineer. Write a function that takes a userId,
   queries the last 10 orders from PostgreSQL, and returns Order[]. Use Drizzle ORM."
```

**Why it works:** Role-setting narrows the AI's search space. Say "TypeScript backend engineer" and it won't offer Python solutions.

---

## Tactic 2: Constraints Over Freedom

```
❌ "Write a good API"
✅ "Write a REST API endpoint:
- POST /api/orders
- Input: { userId: string, items: { productId: string, qty: number }[] }
- Validation: userId non-empty, items at least 1, qty > 0
- Success: 201 + orderId
- Failure: 400 + error message
- Use Zod for schema validation"
```

**Constraints = quality.** The more specific the prompt, the fewer revision cycles.

---

## Tactic 3: Show Examples (Few-shot)

```
"Convert these Git commit messages to conventional commits format:

Input: 'fixed the login bug'
Output: 'fix(auth): resolve login redirect loop'

Input: 'added dark mode'
Output: 'feat(ui): add dark mode toggle with system preference detection'

Now process these:
- 'updated deps'
- 'refactored user service'
- 'removed old code'"
```

**One good example beats ten paragraphs of description.**

---

## Tactic 4: Step by Step, Not All at Once

```
❌ "Build me a full-stack e-commerce site with auth, products, cart, payments, order tracking"

✅ Step by step:
1. "Design the database schema: users, products, orders. PostgreSQL + Drizzle"
2. "Based on this schema, write CRUD API routes"
3. "Build the product list page with React + TanStack Query"
4. "Add shopping cart logic with Zustand"
```

**Small steps > giant leaps.** AI accuracy in narrow scope is far higher than in broad scope.

---

## Tactic 5: Say What NOT to Do

```
"Refactor this function. Requirements:
- Do NOT change the function signature
- Do NOT add new dependencies
- Do NOT modify tests
- Only optimize the internal implementation"
```

**Negative constraints matter as much as positive requirements.** Many prompt failures happen because AI did something you didn't want.

---

## Tactic 6: Use Existing Code as Context

```
"Look at this file's code style (early returns, snake_case, no-else-after-return),
then write a new function in the same style: processPayment(order: Order): Promise<Receipt>"
```

**Letting AI learn style from existing code is 10x more effective than describing the style.**

---

## Tactic 7: Request Structured Output

```
"Analyze this code for issues. Use this format:

## Issues
1. [Severity: HIGH/MEDIUM/LOW] Description
   - Location: filename:line
   - Fix: specific change

## Summary
- High priority: X
- Medium priority: X"
```

**Templated output = predictable quality.**

---

## Tactic 8: Iterate, Don't Rewrite

```
Round 1: "Write a logging middleware"
→ AI outputs v1

Round 2: "Add to this middleware: request timing, error auto-capture, correlation ID"
→ AI improves on v1

Round 3: "Optimize: avoid serializing large bodies, add content-length limit"
→ AI optimizes v2
```

**Working with AI is like code review — progressive refinement.**

---

## Special Tips for AI Coding Agents

When using Claude Code / Codex / Cursor:

- **Read before write** — "First read all files in src/auth/, understand the auth flow, then modify the login logic"
- **Give checklists** — "After completing, verify: 1) Type safety 2) Error handling 3) Test coverage 4) No console.log"
- **Use SKILL.md to codify common prompts** — Write team conventions as skills, auto-loaded every time
- **Limit scope** — "Only modify src/components/Header.tsx, don't touch other files"

---

## Anti-patterns

- ❌ "Write me the best code" — "best" is undefined
- ❌ 10 requirements in one prompt — split them
- ❌ No context, just "give me output" — garbage in, garbage out
- ❌ Using output without review — AI makes mistakes, always review
- ❌ Prompt tricks instead of clarity — tricks are brittle, clarity is stable

---

## References

- Original tweet: <https://x.com/nothiingf4/status/2030682331670056964>
- Prompt Engineering Guide: <https://www.promptingguide.ai/>

---

*Written 2026-03-09 by 🦞*
