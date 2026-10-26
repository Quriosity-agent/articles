# Chinese Novelist Skill: Organizing Long-Form Fiction with Files, Style Anchors, and a Fact Ledger

> Reviewed and probed October 27, 2026. Repository: [PenglongHuang/chinese-novelist-skill](https://github.com/PenglongHuang/chinese-novelist-skill). The inspected master commit is `7017828`, dated October 21. The latest formal release at review time was [v2.3.1](https://github.com/PenglongHuang/chinese-novelist-skill/releases/tag/v2.3.1), published October 20 UTC. This article's date is the review date, not the project's launch date.

Chinese Novelist Skill gives an existing coding Agent a Chinese-fiction workflow: clarify the premise, save characters and outlines, write chapters, maintain summaries, and check length. It introduces neither a trained model nor a standalone desktop editor. The inspected repository mainly contains Markdown instructions, templates, and guides, plus one Python length-checking script.

Its interesting contribution is repeatedly bringing the Agent back to organized project material. Its central limitation is the distance between instructions written in a document and guarantees enforced by software. [Skill entry point](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/SKILL.md)

![Upstream demonstration of a planning summary and writing-mode selection](imgs/chinese-novelist-skill-workflow-audit/phase2-plan.png)

*All three images are upstream demonstration screenshots, not novels generated during this review. Some displayed file numbers predate the current conventions; the pinned source described below is authoritative for this article.*

## 1. A Readable, Editable Writing Procedure

`SKILL.md` delegates details to stage documents covering initialization, progressive questions, title selection, planning approval, writing-mode selection, chapter production, and final validation. The Agent reads the relevant document when entering a stage.

Compared with asking for thirty chapters in one prompt, this adds a repeatable sequence and explicit deliverables, not new reasoning capability. Creating directories, updating records, and invoking tools remain the host Agent's responsibility. The repository does not contain its own persistent task scheduler.

After planning approval, the instructions favor continuous drafting without per-chapter confirmation. This is a batch-drafting approach rather than an editorial workflow requiring author sign-off at each chapter. Model costs, tool permissions, and runtime limits still apply: a free Skill does not make full-length generation free.

## 2. Different Files Carry Different Kinds of Memory

The current conventions divide project material as follows:

| File | Responsibility |
|---|---|
| `00-人物档案.md` | Character traits, flaws, speech, fears, and relationships |
| `01-大纲.md` | Chapter events, transitions, hooks, and the setting/fact ledger |
| `02-写作计划.json` | Chapter numbers, paths, statuses, counts, retries, and mode |
| `03-文风基准.md` | Style fingerprint, example prose, exclusions, and book-specific anchors |
| `99-章节摘要.md` | Summaries appended as chapters finish |
| `第XX章-标题.md` | Chapter content |

Summaries no longer continually expand the outline, and progress is not inferred solely from chat. Initialization instructs the Agent to inspect plan states for unfinished projects. If the plan is damaged, it attempts to reconstruct progress from summaries, existing files, and length checks. [Planning](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/references/flows/phase2-planning.md), [shared mechanisms](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/references/flows/shared-infrastructure.md)

A separate `user-preferences.json` stores preferences such as genre, viewpoint, and tone. This memory consists of files the Agent reads and writes. It is neither model retraining nor unlimited context. Recovery still depends on those records having been saved accurately.

![Upstream demonstration of preferences and an unfinished-project entry](imgs/chinese-novelist-skill-workflow-audit/memory-demo.png)

## 3. Style Anchors and Fact Ledgers Address Different Problems

The style baseline goes beyond labels such as cinematic or restrained. Planning calls for example prose, followed by passages selected from the completed first chapter as book-specific references. Concrete prose gives the model a more specific target than abstract adjectives.

The fact ledger distinguishes what readers currently know, the full truth, and the chapter planned for disclosure. It also registers hard facts such as dates, ages, amounts, and headcounts. This targets numerical drift and premature revelation. [Ledger template](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/references/guides/outline-template.md)

These remain Agent instructions. No independent program in the inspected repository extracts all narrative facts, proves character knowledge boundaries, or detects every contradiction. An incorrect entry can propagate. A ledger makes mistakes easier to locate; it does not make its contents automatically true.

## 4. Parallel Drafting Trades Dependency Completeness for Speed

The project describes serial, batched subagent, and Agent Teams workflows. Batched subagents receive non-overlapping chapter ranges, write sequentially within each range, and run concurrently across ranges.

Importantly, a later batch may start before the preceding batch's final chapter exists. The instructions allow it to proceed from outline transitions and hooks, then ask the main Agent to inspect batch boundaries afterward. This is a speed-versus-dependency tradeoff, not evidence that multiple Agents automatically share a consistent story state.

Shared-file rules require rereading before edits, modifying only assigned fields, and relying on host editing tools to detect stale changes. The repository does not implement separate cross-file transactions or locks. Exclusive team-task claims likewise require a host that actually supplies that capability. The documented fallback for missing team support is batched subagents; compatibility still needs host-specific testing. [Parallel workflow and write protocol](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/references/flows/phase3-writing.md)

## 5. Automatic Validation Primarily Means a Length Check

No Skill installation or model run was performed. Instead, **ten synthetic behavior probes** exercised the sole Python script. All reproduced their expected observations, including limitations:

- The default minimum is 3,000 characters from `U+4E00–U+9FFF`. Latin text and digits do not count. This is neither a token count nor a general word count.
- After skipping a chapter heading, the extractor counts subsequent content without isolating `## 正文`. A fixture with only two prose characters counted as eight after including summary material and section labels.
- A 5,001-character fixture passes the default check: it enforces a minimum, not the writing instructions' 5,000-character upper target.
- `--all` scans existing `第*.md` files without reading the writing plan. A planned but absent chapter is not detected by that scan alone; the Agent must separately check existence.
- Insufficient length and a missing individual file return exit codes 1 and 2 respectively, and Arabic chapter numbers sort numerically. A negative minimum is accepted, allowing even empty prose to pass.

These probes establish script behavior, not literary quality. The reproduction script is [probe_wordcount.py](imgs/chinese-novelist-skill-workflow-audit/probe_wordcount.py); provenance is in [SOURCES.md](imgs/chinese-novelist-skill-workflow-audit/SOURCES.md). [Upstream checker](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/scripts/check_chapter_wordcount.py)

The advertised quantitative removal of AI-like prose also needs a precise reading: the guide specifies frequency limits for constructions, imagery, and repeated gestures, but delegates checking to the Agent. There is no separate implemented style detector. [Style checklist](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/references/guides/chapter-guide.md)

![Upstream demonstration of chapter files and a Markdown manuscript preview](imgs/chinese-novelist-skill-workflow-audit/phase4-done.png)

## 6. Inspect Unresolved Items, Not Just the Completed Status

Final validation specifies at most three repair rounds, but permits the project to become `completed` afterward even if some chapters remain below target, provided the report flags them. That status therefore means the procedure ended, not that every check passed. Meanwhile, the chapter checklist says to keep expanding short chapters until they pass, leaving stopping conditions at different levels in need of coordination. [Final validation](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/references/flows/phase4-validation.md)

A useful trial would bound chapter count, spend, and retries, then begin serially. Track one important numerical fact, test whether a planned revelation stays hidden until its intended chapter, and interrupt a run to compare recorded progress with actual files. Test parallel speed only after those basic behaviors are reliable.

The repository uses MIT licensing. Its Roadmap still lists a visualization panel as work in progress; the demonstration images should not be mistaken for a bundled complete application dashboard. The README's third-party model-service sponsorship is not a required dependency, and promotional pricing or service quality was not verified here. [Roadmap](https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/ROADMAP.md)

**The practical contribution is packaging easily forgotten long-form writing steps into a reusable procedure. File separation, prose-based style references, and fact registration are useful ideas. Continuity, concurrency safety, and readable fiction still depend on the host, author review, and evaluation with real manuscripts.**
