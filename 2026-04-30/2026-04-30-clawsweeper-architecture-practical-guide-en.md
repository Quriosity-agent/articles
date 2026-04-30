# ClawSweeper Deep Dive: How a “Conservative” Open-Source Maintenance Bot Actually Works

GitHub repo: <https://github.com/donghaozhang/clawsweeper>

If you have ever maintained a large open-source repository, you know the reality:

- issues and PRs keep piling up;
- real actionable items get mixed together with noise;
- maintainer time gets drained by repetitive work like triage, syncing, and follow-up.

The value of ClawSweeper is not that it “automates more.” Its value is that it **automates conservatively and correctly**. It puts automation inside a very clear boundary: **review first, suggest second, execute carefully last**.

---

## 1. Project overview: what problem is it actually solving?

ClawSweeper is a maintenance bot in the OpenClaw ecosystem. Right now it mainly targets two repositories:

- `openclaw/openclaw`
- `openclaw/clawhub`

It has two independent workflows:

1. **Issue/PR Sweeper**
   - Generates a structured review report for each open issue / PR
   - Syncs one continuously updated public review comment instead of spamming new comments
   - Only enters the closing path when evidence is strong and the item state has not changed

2. **Commit Sweeper**
   - Watches code pushes on the `main` branch
   - Reviews code-oriented commits one by one and writes reports to disk
   - Can optionally publish a GitHub Check Run as a secondary visibility surface

In one sentence: **this is not a “code-fixing bot”; it is a high-evidence, low-aggression maintenance automation control layer.**

---

## 2. Core capabilities: why it feels conservative but useful

Looking across the README, the `src/` code, and the GitHub workflows, several key capabilities stand out.

### 1) Two-layer execution model: Review and Apply are separated

- **Review Lane proposes, but never closes anything**
- **Apply Lane is the only part that actually writes to GitHub** (comment sync / close)

This separation matters a lot in engineering terms. It decouples **judgment** from **mutation**, reducing the chance of accidental closes and unsafe actions.

### 2) Every item is traceable: file-based audit trail

Reports are written into:

- `records/<repo-slug>/items/<number>.md`
- `records/<repo-slug>/closed/<number>.md`
- `records/<repo-slug>/commits/<sha>.md`

That means the bot is not a black box. It is a persistent record system that is **auditable, replayable, and diffable**.

### 3) Repository policy is configurable (Repository Profile)

`src/repository-profiles.ts` defines repository-specific governance differences:

- for OpenClaw, a fuller set of close reasons is allowed;
- for ClawHub, the rules are stricter (for example, auto-close is allowed only in a much narrower set of cases).

So it is one engine with multiple governance profiles.

### 4) Low-latency event path plus periodic batch processing

- Batch mode: scheduled scans, sharded parallelism, incremental progress
- Event mode: `repository_dispatch` can trigger precise review and safe apply for a single item

This gives the system a balance between throughput and responsiveness.

### 5) Strong anti-noise and safety guardrails

From `src/clawsweeper.ts`, you can see a lot of gatekeeping logic:

- maintainer-author protection (do not auto-close)
- protected-label protection (`security`, `beta-blocker`, etc.)
- linked PR and same-author issue/PR pair protection
- snapshot drift verification (if the item changed, apply is blocked)
- GitHub throttling handling and transient retry with backoff

This is the real technical meaning of its “conservative” design.

---

## 3. How it works: architecture and flow breakdown

### 1) Core code structure

- `src/clawsweeper.ts`: main engine (planning, review, apply, audit, dashboard)
- `src/repository-profiles.ts`: repo-specific strategy and close rules
- `src/commit-sweeper.ts`: main commit review pipeline
- `src/commit-classifier.ts`: cheap pre-classification for commits (whether it is worth invoking Codex)
- `src/commit-checks.ts`: maps commit reports into GitHub Checks

### 2) Issue/PR pipeline (high-level)

1. Planner selects candidate items (based on recency, activity, and policy)
2. Shards review them in parallel and produce artifacts
3. Publish merges outputs and updates records
4. Comment Sync updates the single durable review comment
5. Apply closes only **high-confidence, unchanged** proposals

### 3) Commit pipeline (high-level)

1. Receive a `main` branch push (with support for range backfill)
2. Run cheap classification first (skip docs-only or asset-only changes)
3. Review code commits one by one
4. Write reports into `records/.../commits/<sha>.md`
5. Optionally publish Checks; `findings` can be handed off to downstream fix pipelines like Clownfish

---

## 4. How to get started: deployment and usage

The stack is: TypeScript + Node (Node 24+) + pnpm + GitHub Actions.

### Common local commands

```bash
corepack enable
pnpm install
pnpm run build

# Plan candidates
pnpm run plan -- --target-repo openclaw/openclaw --batch-size 5 --shard-count 100 --max-pages 250

# Review
pnpm run review -- --target-repo openclaw/openclaw --target-dir ../openclaw --batch-size 5 --max-pages 250 --artifact-dir artifacts/reviews

# Merge review artifacts
pnpm run apply-artifacts -- --target-repo openclaw/openclaw --artifact-dir artifacts/reviews

# Apply proposed closes (carefully)
pnpm run apply-decisions -- --target-repo openclaw/openclaw --limit 20 --apply-kind all
```

### Key CI workflow files

- `.github/workflows/sweep.yml`: full issue / PR pipeline
- `.github/workflows/commit-review.yml`: full commit review pipeline
- `.github/workflows/ci.yml`: build, test, format, and checks

---

## 5. Design choices worth borrowing

### 1) One durable comment instead of comment flooding

It uses a marker mechanism to locate and update a single in-place review comment, instead of repeatedly spamming the same PR.

### 2) Report as Source of Truth

Execution decisions are based on comparison between persisted report files and real-time GitHub state, not temporary in-memory state.

### 3) Classify first, then call the LLM

Commits go through a cheap path-level classifier first. Obviously non-code changes are skipped, which saves model cost.

### 4) Make observability part of the product

The README dashboard is not decorative. It is the unified entry point for runtime status, coverage cadence, recent actions, and audit health.

---

## 6. Limits and risk notes

Even careful automation has boundaries, and ClawSweeper is no exception:

1. **It depends heavily on GitHub APIs and token permissions**: rate limiting or incomplete permissions will affect throughput and consistency.
2. **Model judgment is not infallible**: that is exactly why the system chooses conservative execution, but maintainer spot-checks are still necessary.
3. **Rule complexity will grow**: as more repositories and more policy variations are added, configuration and explainability costs increase.
4. **Close policy requires organizational consensus**: deciding which reasons are allowed for auto-close is fundamentally a governance question, not just a technical one.

---

## 7. Who is this best suited for?

ClawSweeper is especially worth studying or adapting if your team looks like this:

- a medium or large open-source repository with visible issue / PR backlog;
- a need for continuous cleanup, but with no tolerance for aggressive auto-closing;
- a desire to turn maintenance work into an auditable record system;
- existing GitHub Actions infrastructure and willingness to adopt rule-driven governance.

If your repository is small, low-volume, and easy to maintain manually, the full stack may be overkill. In that case, the two ideas most worth borrowing first are **Review/Apply separation** and the **durable comment** model.

---

## Conclusion

The most interesting thing about ClawSweeper is not that it “uses an LLM.” It is that it embeds model capability inside a mature repository-governance framework:

- evidence first, action second;
- proposal first, execution second;
- traceability first, scale second.

For any team that wants to upgrade repository maintenance from repetitive manual labor into an engineered system, this project is genuinely worth studying.

---
**Author:** 🦞 Lobster Detective  
**Date:** 2026-04-30  
**Tags:** ClawSweeper, OpenClaw, GitHub Automation, Repository Maintenance, Agent Workflow, Open Source Governance
