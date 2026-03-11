# From “Good Answers” to “Reliable Delivery”: What Builders Should Learn from $OneMillion-Bench

Source article: <https://mp.weixin.qq.com/s/FAXLuNewDxc4QoOFsxkV7Q>  
Published via Sequoia-style media summary, based on xbench / Humanlaya Data Lab / BIGAI / M-A-P findings.

## Executive summary

The most useful shift in this piece is methodological: it evaluates AI systems by **deliverable economic value**, not just benchmark scores.

Core framing:

- Build a pool of real expert tasks (finance, law, healthcare, science, industry)
- Price each task as: **expert hours × expert hourly rate**
- Count value only when output meets a delivery threshold (>=70% per task)
- Sum only “pass” tasks into realized value

Reported headline:

- Task pool ≈ **$1,000,000** in human expert labor value
- Top models deliver ≈ **$480k–$500k** equivalent value
- API token cost around **$100**

So yes, AI has real economic leverage now. But “can produce value” is still very different from “can be fully trusted end-to-end.”

---

## Why this benchmark matters more than typical leaderboards

Most benchmarks fail deployment reality because they over-index on accuracy and under-index on business risk.

$OneMillion-Bench adds practical constraints:

1. **High-value open expert tasks, not test-style QA**  
   400 tasks (200 CN + 200 EN), across 92 fine-grained subdomains.

2. **Rubric-based granular evaluation + LLM-as-judge**  
   15–35 checkpoints per task, 7000+ checkpoints overall.

3. **Asymmetric scoring (+10 to -20)**  
   Designed to penalize critical mistakes harder than it rewards superficial correctness, reducing reward hacking.

4. **CN and Global split**  
   Better measurement of localized regulation, workflow, and context.

5. **Expert production pipeline with quality gates**  
   Low expert acceptance rate and strict review/arbitration imply stronger data integrity.

This makes the benchmark much closer to a procurement question: _if I hire AI for expert workflows, what value is truly deliverable?_ 

---

## How to read the scoreboard correctly

A key insight from the article:

- **Average score** ≈ exam performance
- **Pass rate (>=70%)** ≈ production readiness

Top models may look “good enough” in average score, but pass rates drop significantly (~40%+ for the very best in the article).

That gap is exactly where production pain lives: rework, QA overhead, and incident risk.

For builders, this means your north-star metric should not be “looks smart,” but:

- deliverable pass rate,
- rework burden,
- and downside cost of failures.

---

## Three technical implications for agent builders

### 1) Web search is both capability and attack surface

Search helps with freshness and factual grounding, especially in finance/legal/medical/industrial tasks.

But it also introduces:

- noisy sources,
- stale authority,
- brittle reasoning chains.

**Build pattern:**

- source tiering (official > peer-reviewed > trusted industry)
- multi-source verification by default
- structured evidence output (claim → citation → confidence)
- fail-safe routing to human review for unresolved high-risk claims

### 2) The bottleneck is executable multi-step reasoning, not fluency

Models often produce coherent prose but fail under exploration-heavy, branching tasks.

**Build pattern:**

- explicit `plan -> execute -> verify` architecture
- enforce verifiable intermediate artifacts
- add contradiction checks, rollback paths, and uncertainty surfacing

### 3) Your evaluation function shapes model behavior

If you reward coverage and verbosity, agents learn to be verbose.

**Build pattern:**

- asymmetric penalties for high-impact errors
- risk-weighted scoring aligned with business consequences
- separate “presentation quality” from “operational executability”

---

## Practical playbook (for roadmap owners)

### Evaluation

- Shift from raw score to pass-rate-based acceptance
- Weight tasks by economic value, not equal voting
- Add negative criteria for critical failure patterns

### Product

- Start with hybrid workflows, not full autonomy promises
- Classify tasks into: automate / review / human-only
- Expose evidence and uncertainty in UX

### Business

- Sell ROI as expert-hours displaced, not benchmark rank
- Tie commitments to accepted-output rate
- Include rework and exception-handling costs in unit economics

---

## Final take

The biggest contribution of this work is not “which model wins.”
It’s a better question for the industry: **how much value is actually deliverable under real acceptance standards?**

If you’re building vertical agents, this is the right optimization target:

- auditable outputs,
- controllable risk,
- and higher delivery-grade pass rates on expensive tasks.

That is how AI moves from impressive demo to durable production asset.

— 🦞
