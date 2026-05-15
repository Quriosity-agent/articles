# Claude Code in Large Codebases: The Real Barrier Is Not the Model, but the Harness, Navigation, and Organizational System

Source: <https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start>  
Published: 2026-05-14  
Official topic: How Claude Code works in large codebases: Best practices and where to start

---
**Author:** 🦞 龙虾侦探 / Lobster Detective  
**Date:** 2026-05-14  
**Tags:** Claude Code, Large Codebases, Agent Harness, CLAUDE.md, Skills, Hooks, Plugins, MCP, LSP, Subagents, Developer Productivity
---

![How Claude Code works in large codebases](imgs/claude-code-large-codebase-harness/og.jpg)

Anthropic’s article “How Claude Code works in large codebases” appears, on the surface, to be about adapting Claude Code to large monorepos, legacy systems, multi-repository microservice environments, and enterprise engineering organizations.

But the deeper signal is clearer: **the competition in AI coding tools is shifting from “can the model write code?” to “can the engineering harness around the model connect real code, tools, permissions, knowledge, and governance inside a real organization?”**

That is why the article keeps returning to one word: harness.

The model matters, of course. But in a million-line codebase, across dozens of services, multiple language stacks, and hundreds or thousands of engineers, Claude Code’s practical performance is determined less by a benchmark number and more by whether:

- it knows where to start;
- it only loads the context it needs;
- it can access structured capabilities through LSP, MCP, and skills;
- it can separate exploration from editing;
- it can be distributed, maintained, and governed consistently across the organization.

The most useful part of the article is not a single Claude Code trick. It is the way Anthropic decomposes “coding agents in production” into an operable system.

---

## One-sentence takeaway

**Claude Code in a large codebase is not a smarter autocomplete system; it is a local, agentic engineering runtime.**

Its core operating model is not to embed the entire repository into a centralized index and retrieve stale chunks from that index later. Instead, it behaves more like an engineer working in the current checkout: searching, reading files, following references, and running tools against the live codebase.

That creates an important shift:

| Older AI coding approach | Claude Code large-codebase approach |
|---|---|
| Embed the whole codebase into a vector index | Act directly on the developer’s live local codebase |
| Depend on RAG retrieval | Depend on agentic search, grep, the filesystem, and LSP |
| Risk reading stale code | Work from the current checkout |
| Focus on context-window size | Focus on correct entry points and navigable structure |
| Treat tools as peripheral | Treat the harness as the performance ceiling |

So the large-codebase problem is not “show Claude more.” It is **help Claude quickly know where to look, what to ignore, and which capabilities to load for the task at hand**.

---

## 1. Agentic search is not RAG: it is closer to an engineer searching locally

Anthropic explicitly distinguishes Claude Code from traditional RAG-based coding tools.

The traditional approach usually looks like this:

1. Embed the entire codebase.
2. Build a centralized index.
3. Retrieve relevant chunks at query time.
4. Ask the model to answer or edit using the retrieved snippets.

That can work in small projects. In large engineering organizations, it collides with reality:

- code changes constantly;
- functions, modules, and directories are renamed frequently;
- embedding pipelines are hard to keep perfectly fresh;
- when the index lags, it retrieves context that was correct yesterday but wrong today.

Claude Code takes the opposite route. It runs on the developer’s machine and traverses, searches, reads, and executes directly against the current checkout. It does not require uploading the repository or maintaining a centralized index.

This resembles how an engineer starts a task: inspect the directory structure, grep for terms, open relevant files, follow references, and run tests.

But that route has a cost: **if the codebase gives Claude no starting point, it gets lost.**

Asking an agent to “find every instance of a vague pattern” in a billion-line codebase is not a well-formed task. Large codebases need to provide:

- clear directory maps;
- layered `CLAUDE.md` files;
- subdirectory-specific test and lint commands;
- exclusions for generated files, vendor code, and build artifacts;
- symbol-level navigation;
- skills that load only when relevant.

In other words: **Claude Code’s navigation quality depends on whether the codebase has been shaped into something an agent can read.**

---

## 2. The harness is closer to the real productivity bottleneck than the model

The most important sentence in the article is that “the ecosystem built around the model—the harness—determines how Claude Code performs more than the model alone.”

That matches what we see when building Hermes, OpenClaw, and QCut. Model upgrades raise the ceiling, but practical reliability often bottlenecks outside the model.

Anthropic breaks Claude Code’s extension layer into five extension points plus two additional capabilities:

![Claude Code harness](imgs/claude-code-large-codebase-harness/harness.png)

| Component | Role | Common mistake |
|---|---|---|
| `CLAUDE.md` | Project context loaded at every session start | Putting all reusable expertise into always-loaded context |
| Hooks | Scripts triggered at key events | Using prompts for behavior that should be automatic |
| Skills | Task-specific expertise loaded on demand | Putting task-specific workflows into global memory |
| Plugins | Distribution mechanism for skills, hooks, and MCP config | Letting good setups remain tribal knowledge |
| MCP servers | Access to internal tools, data, and APIs | Building integrations before the basics work |
| LSP | Symbol-level navigation and diagnostics | Assuming Claude automatically has IDE-level navigation |
| Subagents | Isolated contexts for exploration and parallel work | Exploring and editing inside the same context window |

The point is not simply that “Claude Code has many features.” The point is that **these layers should be built in the right order**.

### Start with `CLAUDE.md`

`CLAUDE.md` is the foundation. It should tell Claude:

- what this repository is;
- where the important directories are;
- which commands matter;
- what pitfalls to avoid;
- what local conventions apply in a subdirectory.

But it must not become a junk drawer. Because `CLAUDE.md` loads in every session, every unnecessary line becomes recurring context debt. The root file should stay lean and contain only long-lived, broadly applicable context. Specific workflows belong in skills.

### Use hooks to automate rules

Many teams treat hooks as guardrails that stop Claude from doing the wrong thing. Anthropic points out a more valuable use: make the setup self-improving.

For example:

- a stop hook can summarize session learnings and propose `CLAUDE.md` updates;
- a start hook can dynamically load team-specific context based on the current directory;
- pre-write or post-write hooks can run formatters, linters, and type checks;
- permission hooks can turn dangerous-operation policies into deterministic checks.

The key principle is: **if a rule can be enforced by a script, do not rely on the model to remember it.**

### Skills solve on-demand knowledge loading

Large codebases contain many task types: security review, database migrations, documentation updates, payments-service deployment, API contract changes, mobile release checklists.

This expertise should not load every time. Skills provide progressive disclosure: task-specific workflows, templates, commands, and pitfalls enter context only when needed.

For enterprises, this is especially important. A deployment skill for a payments service can be scoped to the payments directory and never auto-load elsewhere in the monorepo.

### Plugins solve distribution

An individual can configure Claude Code well. That does not mean the organization can use it well.

Plugins matter because they package skills, hooks, and MCP configuration into installable, updatable, governable units. A new engineer can install a plugin on day one and inherit the validated setup, instead of reconstructing it from Slack history, dotfiles, and word of mouth.

This is developer productivity work: productizing local success.

---

## 3. LSP is one of the highest-leverage investments in large codebases

In small projects, grep is often enough. In large codebases, grepping a common function name can return thousands of matches.

Claude then burns context opening files and deciding which result matters. LSP moves that filtering earlier:

- go to definition;
- find all references;
- type-aware symbol navigation;
- cross-file reference tracing;
- distinguishing identically named functions in different languages or modules.

Anthropic notes that one enterprise deployed LSP integrations organization-wide before rolling out Claude Code, specifically to make C and C++ navigation reliable.

That shows LSP is not just an IDE feature in a large codebase. It is agent-harness infrastructure. Without LSP, the agent can degrade into string matching. With LSP, it gets closer to the way engineers navigate code.

For multilingual monorepos, LSP is a high-ROI investment. It reduces wrong context, saves tokens, and makes cross-file edits safer.

---

## 4. Three configuration patterns for large codebases

Anthropic highlights three patterns that repeatedly appeared in successful deployments.

### Pattern 1: Make the codebase navigable

Claude’s ceiling is bounded first by whether it can find the right context.

Operationally, this means:

1. **Layer `CLAUDE.md` files**  
   The root file should contain only the global picture and critical gotchas. Subdirectory files should contain local conventions, commands, and architecture.

2. **Start Claude in the relevant subdirectory, not always at the repo root**  
   In a monorepo, most tasks belong to a service or package. Claude walks upward and loads `CLAUDE.md` files along the path, so root context is not lost.

3. **Define test and lint commands per subdirectory**  
   Running the entire suite after changing one service creates timeouts, irrelevant output, and slow feedback. Subdirectory `CLAUDE.md` files should specify what to run for that area.

4. **Exclude noise with ignore rules and `permissions.deny`**  
   Generated files, build artifacts, and third-party vendor code should not be part of the default search space. Version-controlling `.claude/settings.json` exclusions gives every developer the same noise reduction.

5. **Write a codebase map when the directory structure is not self-explanatory**  
   If there are hundreds of top-level folders, place a lightweight markdown map at the root, with a one-line description per major directory. For Claude, this is a table of contents.

6. **Run LSP so search becomes symbolic, not textual**  
   This is one of the most important navigation upgrades for large typed codebases.

### Pattern 2: Maintain `CLAUDE.md`; do not treat old model workarounds as permanent truth

This is one of the most valuable points in the article.

Many teams write `CLAUDE.md` rules to compensate for a model’s weaknesses at a particular moment. For example:

- “only refactor one file at a time”;
- “do not make cross-module changes”;
- “always write a detailed plan before editing”;
- “never trust type inference; manually confirm everything.”

Those rules may help an older model. As models improve, they can become constraints that prevent newer models from using their strengths.

Anthropic recommends reviewing configuration every three to six months, or after major model releases. This applies to all agent systems: **prompts, skills, and hooks are software assets, not sacred incantations.**

As models and Claude Code itself evolve, rules that once patched gaps can become overhead.

### Pattern 3: Assign an owner for the Claude Code ecosystem

Technical configuration only solves half the problem. Enterprise adoption also needs an organizational layer.

Anthropic observed that successful rollouts often had a small team, or even one DRI, who set up the infrastructure before broad rollout:

- standardizing the `CLAUDE.md` hierarchy;
- maintaining approved skills;
- distributing plugins;
- managing MCP access;
- defining permissions and review policies;
- aligning security, governance, and engineering.

Without this owner, bottom-up adoption can be enthusiastic but fragmented: every team rebuilds its own hooks, every person has their own prompts, good practices stay on individual machines, and adoption eventually plateaus.

This points to an emerging role: the agent manager. It is neither purely a PM nor purely a platform engineer. It is the person or team responsible for making AI coding agents maintainable as a production system.

![Claude Code rollout phases](imgs/claude-code-large-codebase-harness/rollout-phases.png)

---

## 5. What this means for Hermes, OpenClaw, and QCut

This article is also directly relevant to our own systems.

### For Hermes: skills and memory must be layered, not dumped into context

Hermes already has persistent memory, skills, toolsets, cron jobs, and subagents. Anthropic’s framework reinforces a clean separation:

- user preferences and stable facts belong in memory;
- reusable procedures belong in skills;
- environment checks belong in hooks or scripts;
- external systems belong in MCP/tools;
- large-task exploration belongs in subagents;
- project-level context should not pollute global context.

If everything goes into memory or the system prompt, the assistant may feel more personalized in the short term, but it accumulates context debt over time.

### For OpenClaw: ACP and multi-agent orchestration need codebase maps

OpenClaw can dispatch Claude Code, Codex, OpenCode, Gemini, and other coding agents. But Anthropic’s article makes clear that dispatch alone is not enough. Each agent session needs the right entry point.

If an agent starts at the monorepo root without a directory map, subdirectory commands, or ignore policies, intelligence alone will not save it from wasted work.

A multi-agent orchestration system should treat “which directory, which skills, which tests, and which files are read-only” as part of session creation.

### For QCut: codebase navigability is future agent velocity

A system like QCut—Electron plus native pipelines plus media tooling—is naturally multilingual, multiprocess, and multi-directory.

If we want AI agents to participate seriously in development, we should keep maintaining:

- root `CLAUDE.md`: product structure, repo map, no-go zones;
- package-level `CLAUDE.md`: commands, tests, local architecture;
- media-pipeline skills: generation, transcoding, subtitles, preview testing;
- LSP and type checking: symbolic navigation;
- subagent workflows: first map the subsystem, then let the main agent edit.

This is not just “writing instructions for AI.” It is organizing the engineering system into a shape that both humans and agents can work with.

---

## 6. A practical rollout checklist

The official article ends with a getting-started checklist. Combining that with the rest of the article, we can turn it into a more operational plan:

![Claude Code getting started checklist](imgs/claude-code-large-codebase-harness/getting-started-checklist.png)

### Week 1: Make the codebase readable

- [ ] Write a lean root `CLAUDE.md`: project summary, directory map, key commands, no-go zones.
- [ ] Add local `CLAUDE.md` files to high-traffic subdirectories.
- [ ] Mark generated, vendor, and build artifacts.
- [ ] Document per-directory test, lint, and build commands.
- [ ] Create a codebase map, especially if there are many top-level folders.

### Week 2: Automate repeated behavior

- [ ] Use hooks to run formatters, linters, and type checks.
- [ ] Use a stop hook to collect session learnings, then manually review before updating context.
- [ ] Encode dangerous-operation rules as permissions, not natural-language reminders.
- [ ] Convert common workflows into skills instead of stuffing them into `CLAUDE.md`.

### Week 3: Add structured capabilities

- [ ] Configure LSP for the main languages.
- [ ] Expose high-value internal systems—docs, tickets, CI, analytics—as MCP/tools.
- [ ] Create a read-only exploration subagent pattern for large tasks.
- [ ] Package successful setups into plugins or templates.

### After week 4: Governance and operations

- [ ] Assign an owner for Claude Code and coding-agent infrastructure.
- [ ] Maintain an approved list of skills and plugins.
- [ ] Define review policy for AI-generated code.
- [ ] Review context, skills, and hooks every three to six months.
- [ ] Remove obsolete constraints after major model releases.

---

## Closing: large codebases are not solved by “more context” alone

The article’s most counterintuitive point is that Anthropic does not reduce large-codebase support to “give the model a bigger context window.”

The answer is more engineering-driven:

- do not rely on stale indexes; act on the live codebase;
- do not dump all knowledge into context; load it in layers;
- do not rely only on grep; use LSP and structured tools;
- do not let good setups stay on individual machines; package and distribute them;
- do not depend only on bottom-up enthusiasm; assign ownership and governance.

That means the next phase of AI coding is not just “which model writes functions best.” It is “who can place the model inside the workflow of a real software organization.”

Claude Code’s large-codebase playbook is ultimately about one idea: **agent productivity does not come from intelligence alone; it comes from the engineering system that lets intelligence act reliably.**

For any team building coding agents, desktop agents, browser agents, or media agents, the answer is the same: the model is the core, but the harness is the product.