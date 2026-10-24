---
title: "Inside InkOS: Managing AI Story Creation with Canon, Context, and Recoverable Artifacts"
date: 2026-10-24
source: "https://github.com/Narcooo/inkos"
tags:
  - InkOS
  - AI Writing
  - Story Creation
  - Agent Harness
  - Canon Management
  - Context Engineering
  - Narrative Forecast
  - Visual Novel
  - Source Audit
---

# Inside InkOS: Managing AI Story Creation with Canon, Context, and Recoverable Artifacts

The opening paragraphs are the easy demonstration of AI writing. Sustained delivery is harder: who knows a secret, which object was lost, whether an earlier promise was fulfilled, and which later chapters an edit invalidates.

InkOS separates those concerns from chat history into author intent, story state, chapter plans, review observations, and versioned files. **Its main value is organizing story production, not supplying a new writing model or turning prompts into automatic publication.**

![Upstream InkOS Studio creation entry screen](imgs/inkos-stateful-story-creation-harness/studio-dashboard.png)

*An upstream screenshot showing creation entry points and sessions. It is supplied by the project, not captured from an application launched during this review.*

This October 24, 2026 review inspected [`Narcooo/inkos`](https://github.com/Narcooo/inkos) at [`56aa33b`](https://github.com/Narcooo/inkos/tree/56aa33b04a27c45cc7a91f3d018187a77aec54ea) and ran selected tests in a temporary checkout. No model APIs were called, no manuscript or cover generated, and no personal work imported.

## Source and Installed Versions Are Different

The inspected `master` declares package version `2.0.0`; its README explicitly calls it development code. At review time, both npm `latest` and the latest formal GitHub Release were **1.8.0**, released August 17, 2026. [Development README](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/README.md), [v1.8.0 Release](https://github.com/Narcooo/inkos/releases/tag/v1.8.0), [npm package](https://www.npmjs.com/package/@actalk/inkos)

This article analyzes that development snapshot, not a promise that a default npm install provides every behavior described. The 1.8.0 release notes already include shared-harness work, so these ideas should not all be presented as first appearing in 2.0.

The repository separates `packages/core`, `packages/cli`, and `packages/studio`: production/state logic, terminal interfaces, and the web workspace. The hosted experience, published package, and development branch need separate evaluation.

## Multiple Roles Need an Execution Host

InkOS names planning, context composition, writing, state settlement, review, and revision roles. More roles do not inherently provide reliability, nor imply eight independent models concurrently editing one book.

The more consequential structure is a shared execution layer:

| Object | Practical meaning |
|---|---|
| Work | A creative work with identity, type, and registered artifacts |
| Profile | Available capabilities and confirmation policy for that work type |
| Episode | The execution record of one creative task |
| ActionResult / Artifact | Structured execution results and file/revision references |

`CreativeHarnessRuntime.executeAction()` checks capability access and authorization based on risk, request source, and confirmation. Mutations can pass through a per-work queue and book lock; start, completion, failure, and cancellation produce recorded events. [Runtime source](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/harness/runtime.ts)

That is more explicit than asking a model to remember to save. It is application-level governance, however, not an operating-system sandbox. A successful tool call still cannot determine whether the prose is compelling.

## Compile the Chapter's Context Before Writing

Long-term direction, near-term emphasis, and the next chapter's task are different inputs. InkOS records them separately within the work's source directory:

```text
story/author_intent.md                 Long-term direction
story/current_focus.md                 Current emphasis
story/runtime/chapter-XXXX.intent.md   Chapter intent
story/runtime/chapter-XXXX.context.json Selected context
story/runtime/chapter-XXXX.trace.json  Sources and assembly trace
```

Its shared compiler distinguishes `protected` from `compressible` fragments. When a budget is exceeded, a semantic compiler can summarize compressible material. Protected context exceeding the budget produces an explicit error rather than silent truncation. Source IDs and token estimates are retained in the trace. [Context compiler](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/harness/context-compiler.ts)

The benefit is not infinite memory. It is the ability to investigate what the model actually received and why something was omitted. Summaries can still lose meaning; traceability does not eliminate review.

## Canon, Readable Projections, and Search Are Different Things

The long-form workflow distinguishes authoritative structured state from readable views and retrieval indexes:

| Layer | Purpose |
|---|---|
| `story/state/*.json` | Structured facts, hooks, and chapter summaries |
| `story/*.md` | Human-readable projections of state and summaries |
| `story/memory.db` | Rebuildable SQLite FTS5/BM25 retrieval index |

`retrieveMemorySelection()` loads structured hooks and summaries, rebuilds their search projection, and uses a semantic selector to choose candidate material. A search hit is not a new canonical fact, and relevance ranking does not determine when a promise must be resolved. [Memory retrieval](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/utils/memory-retrieval.ts)

Two reliability questions remain separate. Code can validate a state schema, but the schema alone cannot establish that a recorded fact is supported by the manuscript. Model-based settlement and subsequent review still matter.

## Review Produces Observations; Revision Is Separate

The current review mechanism records observations rather than reducing creative quality to one universal pass score. A source resolver can convert model-selected line ranges into host-held excerpts and check that quotations exist in the named material. [Observation source](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/models/observation.ts)

That makes feedback inspectable, not infallible. Evidence that a sentence exists is different from evidence that the sentence should be removed.

If the review call fails, `reviewChapterDraft()` preserves the prose and records review unavailability instead of interpreting a model failure as bad writing. Revision is a separate action. This should not be summarized as automatic scoring followed by endless rewriting. [Chapter review](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/pipeline/chapter-review.ts)

## Candidate Futures Stay Outside Canon

Writers often compare alternatives such as accepting or rejecting an offer. Narrative forecasts store these futures separately from chapters and authoritative state.

Selecting a branch writes `selected-branch-plan.md`; applying it to an outline, chapter intent, or canon is another step. Input fingerprints can mark older forecasts stale after canonical changes, but do not establish that an old plan remains suitable. [Forecast runner](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/forecast/runner.ts)

Tests executed here used a model substitute to produce two branches and checked that creation, reading, and selection left canonical files unchanged. That verifies isolation, not the quality of either storyline.

## Recoverable Files Matter More Than Completion Claims

A chapter can appear complete while its corresponding story state remains unsaved. The file-set committer stages outputs and a recovery journal, backs up originals, and replaces files. Failures trigger rollback; later recovery can process transactions whose owning process has disappeared. [File-set implementation](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/utils/atomic-file-set.ts)

Selected tests covered failure during replacement and recovery after terminating a writer subprocess. This uses multiple filesystem operations, however, and should not be advertised as full database ACID, instantaneous snapshot visibility to every reader, or guaranteed durability through any power failure. No power-loss test was performed.

Likewise, versions, manifests, and tool results establish which artifacts exist. They do not authorize the conclusion that the book is ready for publication. Engineering completion and creative acceptance remain distinct.

## More Than Novels, Not Automatically Finished Films

Studio also exposes scripts, storyboards, interactive stories, and open-world experiences. The interactive-story delivery code validates a story graph and supports HTML, JSON, and Ink exports. Its HTML player advances nodes using variables, conditions, and choices. [Interactive delivery code](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/harness/tools/film-delivery.ts)

![Upstream InkOS interactive story graph](imgs/inkos-stateful-story-creation-harness/interactive-story-graph.png)

*The project's example graph for “Fog Station No. 12.” Counts and labels are upstream demonstration content, not results generated here or evidence of player acceptance.*

These are different delivery forms. A novel, a storyboard document, a playable narrative page, and a fully voiced video are not interchangeable artifacts. A graph does not establish completed video generation, dubbing, editing, or distribution.

External `SKILL.md` packages primarily supply expertise and static references; they do not automatically gain script execution or bypass tool confirmations. Methods can be extended without treating instructions as executed deliverables. [Skill loader](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/skills/external-loader.ts)

## What This Review Verified

Core dependencies were installed from the lockfile in a temporary clone with install scripts disabled. **Nine selected test files, containing 54 tests, passed.** They cover file recovery, chapter versions, forecast isolation, context compaction, structured state, local search, Skill loading, and mocked harness flows.

The complete suite was not run. No Studio launch, global installation, real model call, cover generation, or complete manuscript production was attempted. Screenshots are upstream assets. Literary quality, sustained long-form consistency, actual costs, and provider compatibility were not independently accepted. [Sources and commands](imgs/inkos-stateful-story-creation-harness/SOURCES.md)

A useful personal evaluation would start with a new test work: write two chapters, change a fact affecting later events, and inspect review evidence, version recovery, and state changes. Before sending unpublished material to an external model, establish where it goes. The AGPL-3.0 code license does not replace model-service terms or grant rights to imported source works.

InkOS's strongest idea is recording intended work, actual context, saved artifacts, and unresolved editorial judgments separately. It improves control and traceability of creation; whether the story deserves to be read remains a question for writers and readers.
