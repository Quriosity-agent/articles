# Lessons from Building Claude Code: Seeing Like an Agent

> **TL;DR**: Thariq from Anthropic (Claude Code core dev) shares hard-won lessons on designing Claude Code's tool system. Key insight: **designing agent tools is art, not science** — you need to "see like an agent." The article reveals the thinking behind AskUserQuestion (3 attempts), Todo→Task evolution, RAG→Grep search shift, and progressive disclosure as a pattern for adding capabilities without adding tools.

---

## Core Framework: Tools Must Match Agent Abilities

Imagine solving a hard math problem. What tools would you want?
- **Paper**: minimum, but slow manual calculations
- **Calculator**: faster, but need to know advanced operations  
- **Computer**: most powerful, but need to code

**Key: Shape tools to the model's abilities.** How do you know those abilities? Watch its outputs, experiment, learn to see like an agent.

## Case 1: AskUserQuestion — Three Iterations

**Goal**: Better elicitation, lower friction for user answers.

| Attempt | Approach | Result |
|---------|----------|--------|
| 1 | Add questions array to ExitPlanTool | ❌ Confused Claude — plan + questions about plan conflicted |
| 2 | Custom markdown output format | ❌ Not guaranteed — Claude appended extra text, omitted options |
| **3** | **Dedicated AskUserQuestion Tool** | ✅ Structured output, modal UI, blocks agent loop |

> "Even the best designed tool doesn't work if Claude doesn't understand how to call it."

## Case 2: Todo → Task Evolution

**Before**: TodoWrite + system reminders every 5 turns to keep Claude on track.

**After**: Task Tool — because stronger models don't need reminders. Reminders actually **constrained** them (Claude thought it must stick to the list). Tasks support dependencies, cross-subagent sharing, modification/deletion.

> "As model capabilities increase, tools that were once needed might now be constraining them."

## Case 3: Search Evolution

| Phase | Method | Issue |
|-------|--------|-------|
| V1 | RAG vector DB | Needed indexing; fragile; context was *given* not *found* |
| V2 | Grep tool | Claude searches codebase itself; builds own context |
| V3 | Skills + progressive disclosure | Read skill → follow references → recursive discovery |

**Claude went from not being able to build its own context to nested multi-layer search finding exactly what it needs.**

## Case 4: Guide Subagent — Capability Without a Tool

Claude didn't know about itself (how to add MCPs, slash commands). Solutions tried:
- System prompt: ❌ context rot for rarely-asked questions
- Docs link: 🟡 Claude loaded too many results
- **Guide subagent**: ✅ Specialized searcher, returns just the answer

**Claude Code has ~20 tools. The bar to add a new one is high** — each option adds cognitive load for the model.

## Key Design Principles

1. **Match tools to abilities** — not most tools, but best-fit tools
2. **Watch model behavior** — observe before designing
3. **Evolve with the model** — old tools become new constraints
4. **Progressive disclosure > new tools** — file links over tool additions
5. **Structured > freeform** — Tool Call beats plain text output
6. **Less is more** — ~20 tools, high bar for each addition

## Resources

- **Original**: <https://x.com/trq212/status/2027463795355095314>
- **Author**: Thariq (@trq212) — Claude Code @ Anthropic

---

*Author: Bigger Lobster*
*Date: 2026-03-01*
*Tags: Claude Code / Agent Tool Design / Anthropic / AskUserQuestion / Progressive Disclosure*
