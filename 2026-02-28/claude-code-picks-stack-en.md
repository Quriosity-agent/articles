# Claude Code's Hidden Power: 2,430 Picks Reveal How AI Defines Your Tech Stack

> **TL;DR**: Amplifying.ai ran 2,430 open-ended prompts against Claude Code ("what should I use?" — no tool names), across 3 models, 4 project types, 20 categories. **Biggest finding: agents build, not buy.** Custom/DIY is the most common "recommendation" (252 picks). When agents do pick third-party tools, a default stack emerges: **Vercel + PostgreSQL + Stripe + Tailwind + shadcn/ui + pnpm + GitHub Actions + Sentry + Resend + Zustand**. Redux and Express primary picks: **zero**.

---

## Claude Code Is the New Gatekeeper

When a developer says "add a database" and lets Claude Code handle it, the agent doesn't just suggest — it installs packages, writes imports, configures connections, commits code. **The tool it picks is the tool that ships.**

- **Tool vendors**: If the agent doesn't pick you, you're invisible to a growing share of new projects
- **Developers**: Your default stack is increasingly shaped by what the agent knows, not what you researched
- **Ecosystem**: Understanding what AI agents choose is competitive intelligence

## Study Design

| Dimension | Data |
|-----------|------|
| **Agent** | Claude Code CLI v2.1.39 |
| **Models** | Sonnet 4.5, Opus 4.5, Opus 4.6 |
| **Projects** | Next.js SaaS, Python API, React SPA, Node CLI |
| **Prompts** | 100 open-ended questions, 5 phrasing variants |
| **Total** | 2,430 responses (3 independent runs per model×project) |
| **Extraction** | 85.3% (2,073 identifiable primary picks) |

**No prompt names any tool.** Just "what should I use?"

## Biggest Finding: Agents Build, Not Buy

If Custom/DIY were a single tool, it's the **most common recommendation** — 252 picks, more than GitHub Actions (152) or Vitest (101).

| Category | Custom/DIY Rate | How |
|----------|----------------|-----|
| Feature Flags | **69%** | Config files + env vars + React Context |
| Auth (Python) | **100%** | JWT + passlib + python-jose |
| Auth (overall) | **48%** | JWT + custom session handling |
| Observability | 22% | Prometheus + structlog + custom alerting |
| Email | 22% | SMTP + custom transactional email |

## Near-Monopolies (>75%)

| Category | Winner | Share | Runners-up |
|----------|--------|-------|------------|
| CI/CD | GitHub Actions | **94%** | GitLab CI: 0 primary picks |
| Payments | Stripe | **91%** | PayPal: 0 primary picks |
| UI Components | shadcn/ui | **90%** | Radix/Chakra/MUI: alternatives only |
| Deployment (JS) | Vercel | **100%** | AWS: 0 primary picks |

## Strong Defaults (50-75%)

| Category | Default | Share | Surprise |
|----------|---------|-------|----------|
| Styling | Tailwind CSS | **68%** | styled-components nearly gone |
| State Mgmt | **Zustand** | **65%** | **Redux: 0 primary picks** (23 mentions, 2 alt picks) |
| Observability | Sentry | **63%** | 22% build their own |
| Email | **Resend** | **63%** | SendGrid only 7% primary |
| Testing | Vitest/pytest | **59%** | Jest only 4.1% |
| Database | PostgreSQL | **58%** | MongoDB: 0 primary picks |
| Package Mgr | **pnpm** | **56%** | yarn only 0.7%! |

### The Death of Redux
**0 primary picks in 2,430 tests.** Mentioned 23 times ("you could use Redux but I wouldn't recommend it"), alt-picked only twice. The model deliberately chooses Zustand (65%) or React Context (16%).

### yarn's Decline
pnpm 56%, npm 23%, bun 20%, **yarn 0.7%**. 51 alternative mentions but almost never the primary recommendation.

## Model Consensus: 90%

All 3 models agree on top tool in 18/20 categories within-ecosystem.

**Most interesting shift — ORM (JS) "recency signal":**

| Model | Prisma | Drizzle |
|-------|--------|---------|
| Sonnet 4.5 | **79%** | 21% |
| Opus 4.5 | 40% | **60%** |
| Opus 4.6 | 0% | **100%** |

**Drizzle completely replaced Prisma in the newest model.** The strongest recency signal in the dataset.

## Why This Matters

This isn't just a tech stack survey. It reveals a **new tool distribution channel**.

As more developers let AI agents choose tools:
- **Training data frequency drives market share** — not quality, but visibility
- **Agent preferences create feedback loops** — agent picks X → more projects use X → more training data → agent picks X more
- **Traditional marketing channels (conferences, blogs, docs) lose influence**

For developers: **Know what your AI is choosing for you.** Don't let training data determine your architecture.

## Resources

- **Full report**: <https://amplifying.ai/research/claude-code-picks/report>
- **Deck version**: <https://amplifying.ai/research/claude-code-picks/deck>
- **Researchers**: Edwin Ong & Alex Vikati @ Amplifying

---

*Author: Bigger Lobster*
*Date: 2026-02-28*
*Tags: Claude Code / Tech Stack / AI Agent / Tool Market / Vercel / Zustand / Drizzle / Redux*
