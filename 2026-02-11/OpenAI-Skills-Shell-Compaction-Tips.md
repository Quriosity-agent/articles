# Shell + Skills + Compaction: Tips for Long-Running Agents

> Source: OpenAI Developers Blog | 2026-02-11
> Original: https://developers.openai.com/blog/skills-shell-tips

---

## Overview

OpenAI is shifting from single-turn assistants to long-running agents that handle real knowledge work. They're releasing three new agentic primitives:

1. **Skills** — Reusable, versioned instructions (aligned with Agent Skills open standard) mounted into containers for reliable task execution
2. **Shell Tool** — OpenAI hosted containers with controlled internet access for installing deps, running scripts, writing outputs
3. **Server-side Compaction** — Automatic context compression for long agentic runs to avoid hitting context limits

---

## Mental Model

- **Skills** = "Procedures" the model loads on demand (versioned playbooks with SKILL.md manifest)
- **Shell** = Real terminal environment (hosted by OpenAI or local)
- **Compaction** = Keeps long runs moving by compressing conversation history automatically
- **Together** = Repeatable workflows with real execution, without brittle megadoc system prompts

---

## 10 Tips & Tricks

### 1. Write skill descriptions like routing logic
Include "Use when vs. don't use when" blocks. Descriptions are the model's decision boundary.

### 2. Add negative examples and edge cases
Explicitly write "Don't call this skill when…" cases. Glean saw 20% triggering drop that recovered after adding these.

### 3. Put templates inside the skill (free when unused)
Stop cramming templates into system prompts. They load only when the skill triggers — biggest quality and latency gains (per Glean).

### 4. Design for long runs early
- Reuse containers across steps for stable deps/cached files
- Pass `previous_response_id` for thread continuity
- Use compaction as default, not emergency fallback

### 5. For determinism, explicitly tell the model to use the skill
Simply say "Use the \<skill name\> skill." — turns fuzzy routing into explicit contract.

### 6. Skills + networking = high-risk combo
- Keep network allowlists strict
- Assume tool output is untrusted
- Avoid open internet + powerful procedures in consumer-facing flows

### 7. Use /mnt/data as handoff boundary
Tools write to disk → models reason over disk → developers retrieve from disk.

### 8. Understand two-layer allowlists
- **Org-level**: maximum allowed destinations (small, stable)
- **Request-level**: subset needed for this one job (even smaller)

### 9. Use domain_secrets for authenticated calls
Model sees placeholders ($API_KEY), sidecar injects real values only for approved destinations. Never expose raw credentials.

### 10. Same APIs work cloud and locally
Start local (fast iteration) → move to hosted containers (repeatability, isolation). Skills stay the same across both modes.

---

## Three Build Patterns

### Pattern A: Install → Fetch → Write Artifact
Simplest pattern. Agent installs deps, fetches data, produces deliverable to /mnt/data/report.md. Clean review boundary.

### Pattern B: Skills + Shell for Repeatable Workflows
Encode workflow (steps, guardrails, templates) in a skill → mount into shell → agent follows skill deterministically. Good for spreadsheet analysis, dataset cleaning, report generation.

### Pattern C (Advanced): Skills as Enterprise Workflow Carriers
Skills become living SOPs. Glean example: Salesforce skill increased eval accuracy 73% → 85%, reduced TTFT by 18.1%. Used for account planning, escalation triage, brand-aligned content.

---

## Key Takeaway

- **Skills** = encode the *how* (procedures, templates, guardrails)
- **Shell** = execute the *do* (install, run, write artifacts)
- **Compaction** = keep long runs coherent
- Start local, move to hosted, keep networking locked down

---

*Collected: 2026-02-12*
