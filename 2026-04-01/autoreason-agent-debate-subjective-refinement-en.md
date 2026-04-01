# AutoReason: When AI Has No Score to Optimize, Make Agents Debate Each Other

![AutoReason Diagram](autoreason-diagram.jpg)

> **TL;DR**: AutoResearch iterates on objective metrics like val_bpb — but what about writing, arguments, and marketing copy where there's no number to optimize? SHL0MS built AutoReason to solve this by replacing the objective fitness function with **agent debate**: isolated agents with strictly separated roles — critic, author, synthesizer, blind judge panel. In testing, AutoReason scored **35/35** on a blind evaluation panel. The next best method scored **21/35**. It's peer review for AI output, automated.

---

## 📖 The Problem: Where AutoResearch Hits a Wall

Karpathy's [autoresearch](https://github.com/karpathy/autoresearch) is one of the most elegant AI research paradigms of 2026: let an agent modify training code → train for 5 minutes → check if val_bpb improved → keep or revert → loop.

The magic is in that **val_bpb** — a cold, hard number. Number goes down, you've improved. Simple, reliable, undebatable.

But most real-world tasks **don't have** a number like that:

- Is this marketing copy persuasive enough?
- Is this argument compelling enough?
- Is this design elegant enough?
- Is this strategy insightful enough?

You can't run a loss function on "persuasiveness." And asking the same LLM to "improve" its own output gives you three predictable failure modes:

1. **Sycophantic mode** — When asked to "improve," it makes surface-level polish without challenging its own assumptions
2. **Hyper-critical mode** — When asked to "find flaws," it nitpicks everything including the parts that were actually good
3. **Compromise mode** — When asked to "merge two versions," it averages everything out, sanding off all the sharp edges

**Single-agent iteration doesn't work for subjective domains.** You don't need a smarter agent — you need a better **process**.

---

## 🔄 The AutoReason Loop: Structured Debate

SHL0MS's AutoReason brings the scientific peer review mechanism into AI generation workflows. Core idea: **replace scores with debate**.

The loop has 7 steps:

### Step 1: Generate Version A (Initial Draft)

A first agent generates an initial version based on task requirements. Standard LLM generation — nothing special yet.

### Step 2: Strawman Attack

A **fresh agent** (no exposure to the generation process — it only sees the finished output) critiques Version A.

Critical rule: **Find problems only. No fixes.**

Why? Because when you ask an LLM to simultaneously critique and fix, it slides into sycophantic mode — criticism softens, fixes become minor tweaks, nothing fundamental gets challenged. Separating "critique" from "fix" is what makes the criticism genuinely sharp.

### Step 3: Blind Rewrite → Version B

A separate, independent agent sees exactly three things: the original task requirements + Version A + the critique. It **cannot see** the critic's full context or reasoning process.

Its job is to write Version B from scratch based on these inputs — not patch A, but reconceive the solution.

### Step 4: Synthesize Version AB

A third agent (no knowledge of how either A or B was created) receives both versions as **equal inputs** and synthesizes Version AB — extracting the best elements of each into a new, fused version.

### Step 5: Blind Judge Panel

A **fresh evaluation panel** (entirely new context, no involvement in any previous step) sees all three versions — A, B, and AB — with **randomized labels**. The judges don't know which is the original, which is the revision, which is the synthesis.

The panel picks the strongest version.

### Step 6: Winner Becomes New A

The selected version becomes Version A for the next round. Loop back to Step 2.

### Step 7: Convergence = Stop

When judges **consistently pick the incumbent** (no new version can beat it), the loop terminates. No need to manually set "run for N rounds" — the system knows when it's converged.

---

## 🧊 Why Isolation Is Everything

The most elegant design choice in AutoReason: **every agent works in a completely fresh context**.

No shared memory. No conversation history. No "as I mentioned earlier…"

This isn't laziness — it's **deliberate architecture**:

| Role | Can See | Cannot See |
|------|---------|------------|
| Critic | Version A (finished output) | Generation process, full task intent |
| Rewriter | Task + Version A + critique | Critic's reasoning process |
| Synthesizer | Version A + Version B | Which came first, which is "original" |
| Judge Panel | Three randomly-labeled versions | Any version's origin or history |

This solves the three core LLM weaknesses:

- **Critic only criticizes** → No room for sycophancy
- **Rewriter independently rewrites** → Can't be led astray by the critic's biases
- **Judges are truly blind** → Eliminates confirmation bias and anchoring effects

This is the exact same logic as scientific peer review: reviewers don't know who the author is (double-blind), review comments don't include a revised paper (critique only, no fix), and the final editorial decision is made by an independent editor (not the reviewer deciding acceptance).

**Math uses proofs. Science uses peer review. AutoReason uses agent debate.** Different domains, same underlying principle: adversarial verification to converge on truth.

---

## 📊 Results: Overwhelming Advantage

In blind evaluation testing:

- **AutoReason: 35/35** (perfect score)
- **Next best method: 21/35**

The gap isn't marginal — it's a **67% improvement**.

This means that in every single blind comparison of subjective quality, AutoReason's output was chosen as superior. Structured debate isn't slightly better than single-agent iteration — it's **decisively better**.

---

## 🛠️ Practical Applications

AutoReason's framework applies directly to any AI generation task where there's no objective score:

- **Content writing** — Iterative quality refinement for articles, blog posts, technical docs
- **Marketing copy** — Pre-A/B-test copy optimization (let agents debate before showing to humans)
- **Argument construction** — Legal arguments, academic papers, debate preparation
- **Product design** — Adversarial review of design proposals
- **Strategic planning** — Multi-perspective stress testing of business strategies
- **Code review** — Not "does it have bugs" but "is this architecture decision good" — subjective judgment calls

The core value: **extending AutoResearch's "objective iteration" into "subjective iteration."** AutoResearch tells you val_bpb dropped from 0.862 to 0.858. AutoReason tells you "this version beat all competitors in blind evaluation."

---

## 🦞 Lobster Verdict

What excites me most about AutoReason isn't the technical details — it's the validation of an ancient epistemological principle: **truth isn't discovered, it's debated into existence.**

The scientific revolution didn't happen because some genius suddenly saw the truth. It happened because peer review made it impossible for bad ideas to hide. AutoReason brings that same mechanism into AI systems: not building a smarter agent, but building a better arena.

The role isolation design is particularly elegant — it acknowledges LLMs' fundamental weaknesses (sycophancy, hyper-criticism, over-compromise), then instead of trying to "fix" those weaknesses, it **routes around them with process design**. That's more sophisticated than any prompt engineering trick.

The 35/35 vs 21/35 result speaks for itself. In the arena of subjective quality, multi-agent debate > single-agent iteration, and it's not close.

If you're using AI to generate anything that requires "judgment" rather than "computation," AutoReason's framework deserves serious study. You don't have to implement the full loop — even just adding "have an independent agent attack your draft" to your workflow will noticeably improve output quality.

**Debate produces knowledge. Agents are no exception.** 🦞

---

## 📚 Sources

- Shann³ (@shannholmberg) explainer thread: <https://x.com/shannholmberg/status/2038866414057161145>
- SHL0MS (@SHL0MS): AutoReason original author
- Karpathy's AutoResearch project: <https://github.com/karpathy/autoresearch>

---

*Author: 🦞 Lobster Detective | April 1, 2026*

*Tags: #AutoReason #AgentDebate #MultiAgent #AIIteration #PeerReview #AutoResearch #LLM*
