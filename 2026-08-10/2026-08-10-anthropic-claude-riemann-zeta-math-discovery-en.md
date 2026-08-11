---
title: "Anthropic's Riemann Zeta Result: Claude Did Not Prove RH, but It Made AI Math Discovery Verifiable"
date: 2026-08-10
source: "https://www.anthropic.com/research/riemann-zeta"
canonical: "https://www.anthropic.com/research/riemann-zeta"
paper: "https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf"
formalization: "https://github.com/anthropics/zeta-23-lean"
tags:
  - Anthropic
  - Claude
  - Riemann Hypothesis
  - Riemann Zeta Function
  - AI for Math
  - Lean
  - Claude Code
  - Multi-Agent Research
---

# Anthropic's Riemann Zeta Result: Claude Did Not Prove RH, but It Made AI Math Discovery Verifiable

> **TL;DR:** On August 10, 2026, Anthropic published an AI-assisted mathematics result: an unreleased research version of Claude did not prove the Riemann hypothesis, but while trying, it improved the unconditional lower bound for the proportion of zeta zeros satisfying the hypothesis from 41.6% to about 67.2%. This is not “AI solved a Millennium Prize problem,” and it is not a normal benchmark. The important signal is the workflow: Claude Code, 31M output tokens, about 60 subagents, 2,400 shell commands, hundreds of Python scripts, numerical checks, prior-art search, human mathematical review, and a Lean 4 / Mathlib formalization. AI mathematics is moving from “the model writes a convincing proof” toward an engineering pipeline for candidate discovery, peer review, formal proof, and reproducible process records.

- **Source:** [Learning more about Claude's mathematical capabilities](https://www.anthropic.com/research/riemann-zeta)
- **Paper:** [More than two thirds of the zeros of the Riemann zeta function lie on the critical line](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf)
- **Formalization:** [anthropics/zeta-23-lean](https://github.com/anthropics/zeta-23-lean)
- **Informal note:** [Anthropic note for experts](https://www-cdn.anthropic.com/23455459f8832d06bb175cc0f88d019aed962ef8.pdf)
- **Discovery appendix:** [Claude's explanation of how it arrived at the result](https://www-cdn.anthropic.com/d7f3ecf1d01392d887f8bc974ca187e2a121b1ed.pdf)
- **Transcripts:** [Typeset and annotated Claude sub-agent transcripts](https://www-cdn.anthropic.com/8a0d1add3c637b858a9a181e98c40e9548c3f44f.pdf)
- **Published:** 2026-08-10
- **Topic:** AI-assisted mathematics / Riemann zeta function / Lean formalization / multi-agent discovery workflow

![Anthropic Riemann zeta research hero](imgs/anthropic-claude-riemann-zeta-math-discovery/01-anthropic-riemann-zeta-hero.webp)

## One-line Takeaway

**The key point is not that Claude got close to proving the Riemann hypothesis. The key point is that Anthropic turned an AI mathematics result into something reviewable, formalized, and process-auditable.**

The Riemann hypothesis remains open. Anthropic explicitly says it does not expect Claude’s techniques to lead to a proof of RH.

But that does not make the result trivial. Claude improved a related question: among the nontrivial zeros of the Riemann zeta function, what minimum proportion can be proven to lie on the critical line `Re(s)=1/2`? The previous unconditional lower bound was 41.6%. Claude’s result is about 67.2%, with the paper titled more directly: more than two thirds of the zeros lie on the critical line.

The value here is not that the conjecture is solved. It is progress on a long-running program: even if we cannot prove all zeros lie on the critical line, how large a proportion can we prove?

## What Was Proved

Very roughly, zeros of the Riemann zeta function control fine structure in the distribution of prime numbers. The Riemann hypothesis says all nontrivial zeros lie on the critical line `Re(s)=1/2`.

The full conjecture is still open. But mathematicians have proved that some proportion of zeros do lie on that line. That lower bound has improved over time:

| Stage | Meaning |
|---|---|
| Hardy | Infinitely many zeros lie on the critical line |
| Selberg | A positive proportion of zeros lie on the line |
| Levinson / Conrey / later work | The proportion lower bound improves |
| Record around 2020 | About 41.6% |
| Claude's result | About 67.2%, with a core two-thirds theorem |

The paper’s main results can be read as:

- at least two thirds of the relevant zeta zeros lie on the critical line;
- at least two thirds are simple and on the critical line;
- at least five sixths are distinct;
- with a Montgomery–Taylor-style optimized window, the critical-line and simple-on-line constants become about 0.6725, while the distinct-zeros constant becomes about 0.83625;
- analogous statements extend to primitive Dirichlet L-functions.

None of this says “all zeros.” These are unconditional proportion lower bounds.

## The Technical Move: Reading Montgomery Without Assuming RH

Anthropic’s post says Claude combined recent work by Baluyot, Goldston, Suriajaya, and Turnage-Butterbaugh with a 2000 paper by Bombieri to surpass the previous 41.6% lower bound.

More technically: Montgomery developed powerful pair-correlation techniques for studying zeta zeros in 1973, but part of the interpretation depended on assuming RH. Later work put Montgomery’s prime-side calculation into a more unconditional framework. Claude’s key move was not to recover termwise positivity on the zero side. Instead, it treated the whole space through a linear-algebraic reading of a Weil Hermitian form.

The paper’s abstract names the ingredients: Sylvester inertia, a rank–trace inequality, and von Neumann’s trace inequality replace the positivity reading that is easy under RH but fails off the line. Put more plainly, Claude did not find a mystical shortcut to RH. It found a sharper bookkeeping device that turns existing analytic number theory inputs into a stronger proportion result.

That is also why Anthropic is careful: the result matters, but it probably is not a path to proving RH.

## Methodology: Claude Code as a Math Research Workbench

The most engineering-shaped part of the story is Claude’s discovery process.

Anthropic describes the workflow like this:

| Step | Detail |
|---|---|
| Initial task | Jarred Sumner asked Claude to “take a real stab” at the Riemann hypothesis |
| First attempt | Claude generated and tried 650 ideas, none of which worked |
| Second attempt | Claude spent about a day and a half coordinating roughly 60 Claude subagents |
| Tool use | 31M output tokens, 2,400 shell commands, and hundreds of Python scripts |
| Self-checking | Thousands of numerical checks against known zeta zeros, with subagents reviewing each other |
| Prior-art search | 54 arXiv papers downloaded to check whether the result was already known |
| Independent review | Subagents searched for counterexamples and re-proved the result from scratch |
| Human validation | Anthropic mathematicians Levent Alpöge and Ralph Furman examined the work and took responsibility for communicating it |
| Formalization | Eric Easley worked with Claude on a Lean formalization |

This is not a normal benchmark and not ordinary chat. It looks more like a research harness: the model proposes ideas, tools run computations, subagents divide the search, humans maintain direction and review boundaries, and a formal system pins down the proof object.

One striking detail is that Sumner is not a mathematician and mostly provided encouragement. That should not be romanticized as “encouragement solves math.” The more grounded interpretation is that once a model can search and self-review, the human may not need to supply every mathematical step. But the human still sets the target, keeps the process moving, asks for verification, and decides when expert review is needed.

## Lean Formalization Is the Hard Boundary

The danger in AI mathematics is not that the proof is ugly. It is that the proof is persuasive while containing a small hole. Natural-language mathematical arguments can fool non-experts and still cost experts real time to debug.

Anthropic’s decision to release a Lean 4 / Mathlib formalization is therefore central. The `anthropics/zeta-23-lean` README calls the repository a static companion artifact, not a maintained project. It says the repo contains a complete, `sorry`-free Lean 4 / Mathlib formalization of Theorems A–E, including the analytic inputs used by the proof.

The repository also states several audit boundaries:

- the top-level theorems have no additional hypotheses;
- the repository declares no project-specific axioms;
- `#print axioms` for headline theorems reports only Lean’s three standard axioms: `propext`, `Classical.choice`, and `Quot.sound`;
- there are no `sorry`s under `Zeta23/` or `Solution`;
- comparator configs check consistency between trusted statements and solution theorems.

This does not remove the need for mathematicians. Formal proof still depends on Mathlib, definition choices, whether the formal statement captures the intended informal claim, and whether the paper-to-Lean translation is correct. But it sharply improves the review surface. The core claim is no longer only a convincing PDF.

## How This Differs from OpenAI Astra

This repository recently covered OpenAI’s Astra math and theoretical computer science results. Anthropic’s result belongs in the same broad trend, but the signal is different.

| Dimension | OpenAI Astra math results | Anthropic zeta result |
|---|---|---|
| Format | Many results across fields | One deep result in a classic direction |
| Emphasis | Ten long-standing problems, paper collection, Lean certificates | Discovery process, subagent collaboration, formalization repo, transcripts |
| Mathematical object | Geometry, coding theory, group theory, complexity, cryptography, combinatorics | Riemann zeta zeros and critical-line proportions |
| Product signal | AI math can produce batches of candidate results | Claude Code can host long-running research search |
| Main risk | Community validation across many results | Over-reading one result as progress on RH itself |

Together, they suggest two layers in AI mathematics. The model layer generates candidate arguments. The engineering layer turns those arguments into reviewable objects. Without the second layer, the first can become persuasive hallucination. Without the first layer, the second is just conventional formalization work.

## How Not to Read This

This release is easy to misread, so the boundaries matter.

First, Claude did not prove the Riemann hypothesis. It advanced a related lower-bound problem.

Second, 67.2% does not mean “Claude numerically checked 67.2% of zeros.” It is an asymptotic proportion lower-bound theorem.

Third, this is not a reproducible result for public Claude. Anthropic used an unreleased research version of Claude, so users should not assume current product Claude has the same mathematical research capability.

Fourth, formalization is not a substitute for peer review. It hardens the core proof, but mathematical meaning, context, dependencies, statement translation, and community absorption still require experts.

Fifth, the non-mathematician-with-encouragement detail is not the core method. The core method is model search, tool use, subagent review, prior-art checking, expert validation, and formal proof.

## What This Means for AI Research Tools

Translated into product language, this event gives a concrete spec for AI research agents:

- they need long-running execution, not one-shot replies;
- they need multi-agent division of labor, not a single endless thread;
- they need shell, Python, literature search, numerical experiments, and proof assistants;
- they need internal review loops that actively search for counterexamples;
- they need prior-art checks to avoid rediscovering known results;
- they need ways to translate informal arguments into formal proof;
- they need human experts to own final communication and responsibility.

That is closer to a research operating system than a math chatbot.

Future AI math tools may compete less on “which model can solve a problem in chat” and more on how reliably they manage the discovery process: problem selection, assumption tracking, experiment logs, proof state, formalization progress, citation graphs, failed branches, and expert review all become first-class objects.

## Conclusion

Anthropic’s Riemann zeta release should not be framed as “Claude proved RH.” The more accurate view is that Claude produced a new lower-bound result on a problem related to RH, and Anthropic wrapped it in human mathematical review plus Lean formalization.

That is already important.

The next stage of AI mathematics will not be powered only by models saying “I have a proof.” It will require discovery, computation, literature, review, formalization, and human responsibility to be connected in one pipeline. Anthropic’s strongest signal is not only the result, but the fact that the result arrived with an auditable AI math discovery workflow.
