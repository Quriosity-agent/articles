---
title: "Factory Droid on Large Software Tasks: Coding Agents Need an Executable Standard of Completion"
date: 2026-08-27
source: "https://x.com/droid_35719/status/2093068852917899336?s=61"
canonical: "https://factory.ai/news/what-it-takes-for-coding-agents-to-complete-large-software-tasks"
x_article: "https://x.com/i/article/2093068846634819584"
tags:
  - Factory
  - Droid
  - Coding Agent
  - ProgramBench
  - Software Engineering
  - Agent Evaluation
  - Validation
  - Multi-Agent
---

# Factory Droid on Large Software Tasks: Coding Agents Need an Executable Standard of Completion

> **TL;DR:** On August 27, 2026, Factory published an experiment on Droid and large software tasks. It selected 24 hard ProgramBench tasks and compared a single-agent setup with a three-role system: orchestrator, implementer, and validator. The main lesson is not that “more agents” automatically solve software engineering. The stronger result came from moving completion judgment out of the implementer’s context and into an executable standard of completion that is built before implementation, owned by the validator, expanded as needed, and prevented from collapsing around the current candidate. The results are strong, but the caveats matter: one run per cell, no variance estimates, system runs were much longer and more expensive, tasks were hand-picked hard cases, 141 of 144 cells were graded, and six Fable cells used Opus substitutes. The right takeaway is not “Droid can now rewrite large software autonomously.” It is that long-horizon coding agents need independent validation systems and governed completion standards.

- **X source:** [luckyalways1 / @droid_35719](https://x.com/droid_35719/status/2093068852917899336?s=61)
- **X Article:** [What it Takes for Coding Agents to Complete Large Software Tasks](https://x.com/i/article/2093068846634819584)
- **Canonical post:** [Factory blog](https://factory.ai/news/what-it-takes-for-coding-agents-to-complete-large-software-tasks)
- **Benchmark:** [ProgramBench](https://programbench.com/)
- **Published:** 2026-08-27
- **Tags:** Factory / Droid / Coding Agent / ProgramBench / Agent Evaluation / Multi-Agent / Validation

![Factory Droid ProgramBench cover](imgs/factory-droid-completion-standard/01-cover.jpg)

## 1. The Core Claim

Factory’s article is about a specific failure mode: coding agents stop too early on large software tasks.

On a small task, an agent can implement a patch, run a few checks, inspect the result, and decide whether to continue. That local loop is often enough for a bugfix, a narrow feature, or a script.

Large tasks are different. A requirement can describe the intended outcome without specifying what must be run, inspected, and compared before the work counts as complete. The agent constructs validation as it goes. Each local judgment can be reasonable while large parts of the whole remain unmeasured.

Factory’s point is that the single agent may not be out of coding ability. It may lack a complete account of what is still missing. It declares completion inside its own partial evidence.

The experiment is therefore about externalizing the standard of completion.

## 2. The Benchmark: ProgramBench, Not A Bugfix Suite

ProgramBench is a cleanroom software-engineering benchmark. Each task gives the agent a reference program, fixtures, and partial documentation. The reference is a black-box oracle: the agent can execute it, but cannot read its source, decompile it, trace it, inspect hidden tests, or use the internet.

The goal is not to fix one bug. The agent must implement a program from scratch so that its observable behavior matches the reference. ProgramBench’s own site frames the task as: given a compiled binary and documentation, agents must architect and implement a complete codebase that reproduces the original program’s behavior.

The ProgramBench paper gives useful context. It was submitted on May 5, 2026 and includes 200 tasks, ranging from compact CLI tools to widely used systems such as FFmpeg, SQLite, and the PHP interpreter. In the paper’s original evaluation of nine language models, none fully resolved any task, and the best model passed 95% of tests on only 3% of tasks.

This is not a “fill in one function” benchmark. It tests holistic software reconstruction: architecture, interface discovery, edge behavior, file formats, error output, flag combinations, long context, and validation strategy.

![ProgramBench selected hard tasks](imgs/factory-droid-completion-standard/02-selected-programbench-tasks.jpg)

Factory did not run all 200 tasks. It selected 24 of the hardest tasks based on current top leaderboard scores. The article says the set was hand-picked and weighted toward low best-public scores. Some hard-end candidates were dropped for persistent safety blocks, single-agent saturation, or a score gated by one undocumented environment variable.

That matters. The results are a signal on selected hard cases, not an unbiased average across the full benchmark.

## 3. The `gdal` Example: 36% To 90%

Factory uses `gdal` as the main example.

`gdal` is the command-line tool of the GDAL project, a core utility in geospatial data processing. Factory says the upstream project is roughly 2M lines of C/C++, or 1.9M after removing bundled third-party libraries. The CLI surface reachable in this task configuration is roughly 600K lines.

Droid rebuilt `gdal` in two ways:

| Condition | Mechanism | Result |
|---|---|---:|
| Single agent | The agent implemented, checked, and decided for itself when it was done | 17K lines of C++, 36% behavioral parity |
| System run | A validator first built a completion standard, an implementer worked against it, and an orchestrator decided next steps | 115K lines of C++, 90% behavioral parity |

The important detail is that the single agent did not run out of time or budget. It stopped because it assessed its own work as done. The failure was premature completion judgment, not exhausted capability.

Factory also gives two other headline examples. The same system improved the 7-Zip recreation from 54% to 95%, and DuckDB from 34% to 80%. Several recreations reached the upper 90s.

That suggests the completion-standard structure transferred across ProgramBench tasks. It does not prove the same gains will appear on every real software task, where the oracle is usually less crisp.

## 4. The System Is About Validation Separation

Factory’s system condition has three roles:

1. **Orchestrator:** decides what to measure, interprets validator findings, issues implementation directives, and decides when to ship.
2. **Implementer:** investigates the reference, writes code, runs checks, and advances the candidate.
3. **Validator:** builds an instrument before implementation and uses it to measure successive candidates.

The important part is the information boundary:

| Dimension | Single-agent campaign | System campaign |
|---|---|---|
| Implementation loop | Agent investigates, implements, runs checks, and judges its work | Implementer investigates, implements, runs checks, and judges its work |
| Completion standard | Develops inside the same context as the candidate | Validator constructs an independent instrument before implementation |
| Independent measurement | None during the campaign | Validator measures successive candidates against its instrument |
| Information flow | Agent sees all checks and results | Instrument and raw results remain with the validator; clustered findings cross the wall |
| Campaign control | Agent chooses what to do next and when to stop | Orchestrator adjudicates findings, issues directives, and decides when to ship |

![Factory Droid experimental design](imgs/factory-droid-completion-standard/03-experimental-design.jpg)

This is not just “multi-agent is smarter.” If the implementer sees every validator test, the sparse sample becomes the target, and the candidate can overfit visible checks. Factory’s design lets findings cross the wall, but keeps the instrument itself on the measuring side.

The validator and implementer can use the same model, reasoning level, and reference program. The difference is not extra knowledge. The difference is that validation authority is isolated from the implementation context.

## 5. What The Instrument Does

Full behavioral parity is not directly measurable in ProgramBench. A program accepts an effectively unbounded space of inputs, flags, file formats, combinations, and error conditions. Any practical validation strategy has to sample that space.

Factory calls that sampled validation system an instrument. Before implementation begins, the validator surveys the reference program, maps where behavior lives, and builds weighted cases plus comparison rules. The article gives two `gdal` cases:

```text
D('hillshade.combined', ['raster', 'hillshade', '--variant', 'combined', 'dem.tif', 'out.tif'])
D('contour.levels', ['raster', 'contour', '--levels', '120,150,180', 'dem.tif', 'out.geojson'])
```

The comparator matters more than the sample syntax. For every case, the runner executes the oracle and candidate sequentially in the same absolute sandbox path and compares four channels:

1. exit code;
2. stdout bytes;
3. stderr bytes;
4. full work-tree delta, including created, modified, and deleted files plus exact file bytes.

The default is byte identity. A relaxation is allowed only through a named normalizer attached to a specific case. Factory says the `gdal` validator wrote hundreds of cases and licensed exactly two relaxations: a masked heap address in debug traces and a date embedded in a file header.

![Factory validator case details](imgs/factory-droid-completion-standard/05-validator-case-two.jpg)

That is the engineering lesson. Many agent evaluations fail because the test semantics are too soft. Factory turns completion into a runnable, comparable, traceable instrument.

## 6. The Wall Prevents The Sample From Becoming The Product

Factory’s system has a wall.

The validator can expand the instrument as it learns more, but cannot weaken it to accommodate the current candidate. The implementer never authors the instrument, runs it, or sees its cases or raw output. The orchestrator receives clustered root-cause findings and turns them into directives at the level of missing features, subsystems, or behavior.

![The system with three roles and the wall](imgs/factory-droid-completion-standard/06-instrument-wall.jpg)

The `gdal` directive shown in the article does not say “fix test 37.” It describes a weak behavior frontier:

```text
Stub frontier (dominant mass, ~60 verbs)

- vgrid: all 11 grid methods
- mdim group on multidim VRT + classic-input pins
- sozip: create / list / validate / optimize
- DEM suite: contour, hillshade, aspect, slope, viewshed, roughness, tpi, tri
- rasterize, pixel-info, calc, mosaic + stack, tile, footprint
```

![Orchestrator directive from gdal run](imgs/factory-droid-completion-standard/07-orchestrator-directive.jpg)

This is the wall’s practical purpose. The implementer learns where the candidate is weak, but not the hidden sample. It still has to investigate the reference independently. That reduces sample leakage while preserving actionable feedback.

## 7. Results: Strong Gains, Real Caveats

Factory ran three model panels: Fable 5, Kimi K3, and GPT-5.6 Sol. For each selected task and model panel, it ran one single-agent campaign and one system campaign.

The headline medians:

| Model panel | Single median | System median | Gap closed | Wall time |
|---|---:|---:|---:|---:|
| Fable 5 xhigh | 56.7 | 89.3 | 73% | 8.5h -> 96h |
| Kimi K3 high | 45.1 | 75.4 | 42% | 9.0h -> 64h |
| GPT-5.6 Sol max | 48.6 | 66.2 | 25% | 1.5h -> 24h |

![Factory Droid model panel results](imgs/factory-droid-completion-standard/09-model-panel-results.jpg)

The gains are substantial, but the caveats are part of the result:

1. **Not compute-matched.** System runs were much longer and more expensive. On `gdal`, the system run used 14x the credits and 13x the wall time.
2. **One run per cell.** Every number is a single campaign, not a repeated-run average. There is no variance estimate.
3. **Not every cell was scored.** 141 of 144 cells were graded. Three system runs were interrupted and not rerun.
4. **Fable has substitutes.** Six Fable cells used Opus after Fable was safety-blocked: bedtools2, gromacs, pandoc, samtools, sox, and tree-sitter.
5. **The tasks were hand-picked.** The 24 tasks are weighted toward hard cases, not randomly sampled.

The defensible conclusion is narrower and stronger: externalizing the completion standard changed the agent’s stopping behavior and improved hidden-suite scores on these ProgramBench tasks. It does not prove that the same structure will produce the same gains on every production engineering task.

## 8. Why This Matters For Real Engineering Teams

Most real engineering work does not come with a ProgramBench-style reference binary and hidden behavioral suite. Migrations, rewrites, payments changes, permission-system refactors, mobile adaptations, and data-pipeline replacements usually have requirements, old systems, logs, user flows, and institutional memory.

The principle still transfers:

1. **Define completion evidence before implementation.** Do not let the agent decide what “done” means while it is writing the candidate.
2. **Separate implementation and validation.** The same model can play different roles, but context and information flow must differ.
3. **Make validation executable.** A checklist is not enough. The standard should be runnable, comparable, and reusable.
4. **Allow expansion, not compromise.** Add cases as new behavior is discovered; do not weaken the standard because the candidate lacks coverage.
5. **Convert raw failures into root-cause directives.** The implementer needs direction, not direct access to the hidden sample.
6. **Keep final scoring independent.** Shipping should include evaluation the development loop did not already see.

This is close to established practices such as requirements traceability, acceptance tests, conformance suites, and independent verification and validation. The difference is that agents reduce the cost of creating and maintaining a project-specific standard.

## 9. Product Implications For Coding Agents

The article gives three direct product lessons.

First, **long-horizon failure is often completion failure, not generation failure.** An agent can write 17K lines of working C++ and still cover only 36% of behavior because it does not know how much it missed.

Second, **multi-agent products need explicit validation boundaries.** “Orchestrator + implementer + validator” is not enough. The system has to specify who owns the instrument, who sees raw failures, who receives clustered findings, and who decides whether the standard should expand.

Third, **cost rises with a better completion standard.** Factory does not hide this. The `gdal` system run used 3.00B credits and 196.9h of wall time, with the implementer accounting for 97% of system spend. A stronger standard makes the agent continue working. Products need budgets, priorities, stop conditions, and explainable progress toward acceptance.

![Task frontier gains](imgs/factory-droid-completion-standard/08-task-frontier-gains.jpg)

## 10. My Read: Agents Need To Know What They Have Not Done

Most coding-agent demos show what the agent can do: fix bugs, write features, run tests, open PRs, call tools.

Factory’s article asks a more production-relevant question: how does the agent know it is done?

For large software tasks, completion is not a feeling. It is an evidence system:

1. behavior inventory;
2. executable validation procedures;
3. independent evaluation context;
4. anti-leakage information boundaries;
5. root-cause feedback;
6. final independent scoring;
7. cost and time accounting.

That is why this article is worth tracking. It identifies a concrete coding-agent failure mode: the agent does not only make mistakes; it can also stop early because it lacks a global measure of unfinished work.

The next coding-agent race will not be only about which model writes better code. It will be about which system can keep the model accountable to an external, executable, non-collapsing standard of completion.

## Sources

1. X source
   https://x.com/droid_35719/status/2093068852917899336?s=61

2. X Article
   https://x.com/i/article/2093068846634819584

3. Factory: What it Takes for Coding Agents to Complete Large Software Tasks
   https://factory.ai/news/what-it-takes-for-coding-agents-to-complete-large-software-tasks

4. ProgramBench
   https://programbench.com/

5. ProgramBench paper: Can Language Models Rebuild Programs From Scratch?
   https://arxiv.org/abs/2605.03546

6. Factory `pb-gdal-fable` artifact
   https://github.com/Factory-AI/pb-gdal-fable
