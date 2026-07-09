---
title: "Lapian Notes Deep Dive: AI Film Study Works Best When Viewing Becomes an Editable Structure"
date: 2026-07-09
source: "https://github.com/bkingfilm/lapian-notes"
canonical: "https://github.com/bkingfilm/lapian-notes"
tags:
  - Lapian Notes
  - Film Analysis
  - AI Film Study
  - Creator Workflow
  - Local-First
  - Screenwriting
---

# Lapian Notes Deep Dive: AI Film Study Works Best When Viewing Becomes an Editable Structure

> **TL;DR:** `bkingfilm/lapian-notes` turns film breakdown into a local-first study workbench. It extracts frames, reads subtitles, packages evidence for any AI system, imports the returned JSON, and turns it into story-lane timelines, structure trees, audience-emotion curves, and editable segment notes. The interesting part is not “AI watches a movie for you.” It is that a movie becomes a structured, reviewable, revisable learning object.

- **Source:** [bkingfilm/lapian-notes](https://github.com/bkingfilm/lapian-notes)
- **Accessed:** 2026-07-09
- **Latest public release visible on GitHub:** `v0.1.3 苹果电脑一键启动`, shown on GitHub as 2026-07-08
- **Topic:** local film-breakdown tools / AI analysis package / film structure study / creator workflow
- **Tags:** Lapian Notes / film analysis / AI-assisted film study / local-first / screenwriting

![Lapian Notes interface screenshot: story-lane timeline, audience curve, and structure tree with frame stills](imgs/lapian-notes-ai-film-analysis-workbench/screenshot.jpg)

## One-line Takeaway

**Lapian Notes is built around a useful product judgment: AI should not simply “understand the film” on behalf of the creator. It should work from a traceable evidence package, then return structured output that a human can keep editing.**

That matters more than the feature list. Many AI film-analysis tools collapse the experience into an upload button and a generated summary. `lapian-notes` does the opposite. It separates the workflow into four steps: import a film, generate an AI analysis package, import the AI result, and refine the breakdown.

That may feel less magical, but it is closer to how real film study works. A breakdown is not a review. It is a way to build a reusable map of what happened, where it happened, how it was staged, and why it worked.

## It does not bind users to one model; it packages the movie for AI

The README makes one important design choice explicit: the AI analysis package can be sent to ChatGPT or any other AI system. It is not tied to a single AI service, and it does not require an API key.

The implementation matches that claim. `src/lib/framePackage.ts` exports a ZIP containing:

| File | Purpose |
|---|---|
| `frames/` | Film stills extracted in timeline order, with timecodes in filenames |
| `subtitles.srt` / `subtitles.json` | Subtitle text and structured subtitles |
| `project.json` | Film metadata and frame timing context |
| `prompt.md` | The analysis instruction for the AI |
| `schema.json` | The JSON structure the AI must return |
| `剧情资料.md` / `research.md` | Optional script material, plot notes, reviews, or research supplied by the user |

This is a practical intermediate layer. The tool does not need to control which model the user chooses. It controls the input format and the output contract. Instead of asking a vague question like “analyze this movie,” it asks the model to analyze a concrete evidence bundle and return importable JSON.

For creators, that is more durable than a direct API integration. Models can change, but the workflow remains: collect evidence, constrain the task, import structured results, then revise by hand.

## One frame per second: incomplete viewing, but a shared evidence index

The frame extraction logic in `src/lib/videoFrames.ts` is deliberately simple. It uses a browser video element to read metadata, builds sample times from a fixed interval, seeks to each time, draws the frame to a canvas, and exports JPEG stills. The product description describes the default timeline as one frame per second.

That is an important tradeoff. One frame per second cannot replace full viewing. It will miss fine motion, performance details, exact cutting rhythm, and sound changes. But it is enough to create a first-pass structural index.

In other words, the point is not to reduce cinema to screenshots. The point is to give both the AI and the human a shared timeline coordinate system:

- frame stills help identify segment boundaries, scene changes, and visual context;
- subtitles provide dialogue and information-release clues;
- the user can jump between timeline, structure tree, and segment notes;
- exported Markdown can preserve timecodes and segment relationships.

That is better for learning than a long generated essay. An essay is a conclusion. A breakdown note is a process.

## Story lanes turn plot into reusable narrative threads

The “story-lane timeline” described in the README is the product’s strongest idea. After the AI result is imported, the tool lays segments across lanes named for that specific film. Segments reused by multiple lines become reference cards.

That solves an old problem in story analysis: a scene rarely belongs to only one line.

A single segment may:

- push the protagonist’s action forward;
- increase antagonist pressure;
- reveal world rules;
- change a relationship;
- shift audience emotion;
- plant information that pays off later.

Ordinary tables often force a segment into one category. Story lanes allow the same segment to be referenced by multiple threads, which is closer to how narrative structure actually works. `src/lib/aiImport.ts` explicitly normalizes `storyLines`, `primaryLine`, `sharedLines`, and audience-curve points, so the product is not merely importing a list of chapters. It is importing a visual narrative network.

For AI video and short-drama creators, that is a useful lesson: studying a reference film should not stop at “what happened in this segment?” The sharper question is, “Which story functions did this segment serve at the same time?”

## Segment deep dives turn one-pass analysis into an iterative loop

Lapian Notes does not stop at one full-film analysis. The README says any segment can be packaged separately and sent to AI for scene- and shot-level breakdown.

The code path `exportSegmentDeepDivePackage` exports only the frames and subtitles inside the selected segment, then generates a more focused prompt. That prompt asks the AI to return:

- `screenplayBlocks`: scene, action, and dialogue blocks in timeline order;
- `techniques`: composition, shot size, camera position, editing rhythm, transitions, sound, and other audiovisual methods;
- `keyBeats`: major beats with timecodes;
- segment-level judgments such as `creativeIntent`, `informationControl`, `rhythmDesign`, and `audienceExperience`.

This is where the tool becomes more than an automatic summarizer. The full-film analysis builds the skeleton. Segment deep dives add texture. A creator can get a coarse structure first, then iteratively interrogate important passages, revise fields, and add evidence.

## Local-first is not a slogan; it fits the copyright and study context

The source README states that the tool runs locally and that films and notes are not uploaded to a server. Its storage model follows the same pattern: note text is saved in `localStorage`, frame stills are cached in IndexedDB, and a saved project becomes a self-contained ZIP.

That is not just a technical preference. Film breakdown has two sensitive edges.

First, the user may be working with copyrighted film files. Even when the use is personal study, uploading the full film to a third-party service is not a safe default.

Second, the notes themselves can contain a creator’s private learning path: scripts, reviews, structure judgments, personal observations, and reusable craft lessons. They are not public search results. They are working material.

So local-first is the right default for this category. It also explains why the project includes `run.bat`, `run.command`, and `setup.ps1`: the target user may not be a developer, but still needs to run the tool on their own computer.

## The engineering boundaries are visible, and that is a good thing

Based on the public README and code, Lapian Notes is not a cloud collaboration platform or an end-to-end video-understanding model. Its boundaries are clear:

- automatic transcoding and subtitle search depend on the local dev-server interface;
- static builds downgrade those two capabilities to manual workflows;
- H.264 MP4 is the easiest browser-compatible format, while other formats may need ffmpeg;
- frame extraction is sampling, not complete video understanding;
- imported AI JSON still requires human checking;
- subtitle search uses public subtitle sources, and the README warns against commercial use.

Those boundaries make the product more credible. It does not pretend to fully automate film understanding. It places AI inside an inspectable workflow: AI drafts; humans verify, correct, and deepen the analysis.

## The lesson for AI creative tools: build the evidence workbench before the generate button

Placed inside the broader AI video and AI screenwriting stack, Lapian Notes points to a simple idea: creators need analysis and learning workbenches, not only generation interfaces.

A mature video-creation stack needs two loops:

| Loop | Goal | Typical output |
|---|---|---|
| Generation loop | Turn prompt/reference into video | shots, clips, storyboards, finished edits |
| Learning loop | Extract structure from existing work | timelines, segment functions, rhythm curves, reusable methods |

Many tools focus almost entirely on the first loop, so creators keep tuning prompts by instinct. Lapian Notes shows why the second loop matters. Study strong work first, extract structure, then translate that structure into new creative decisions.

For AI video workflows, this can become a practical pre-production layer:

1. import a reference film or scene;
2. align frames, subtitles, and supporting material;
3. use AI to draft a structure map;
4. manually verify segment function and audiovisual method;
5. export Markdown into a personal library of rhythm, scene design, and narrative patterns;
6. translate those patterns back into prompts, storyboards, and reference packs.

That is healthier than copying a recognizable shot. It teaches the creator to extract principles rather than imitate surface style.

## What to watch next

First, AI analysis quality. The tool constrains output with prompts and schemas, but different models will vary in how well they read film stills, subtitles, and narrative structure. Model recommendations, sample outputs, JSON repair, and multi-pass validation could matter a lot.

Second, frame granularity. One frame per second is good for macro structure, but action films, musicals, experimental cinema, and fast-cut sequences may need finer sampling or shot-boundary detection.

Third, subtitles and rights. Automatic subtitle search reduces friction, but users still need clear source, language, version, and rights signals.

Fourth, whether it grows from a single-film note tool into a personal film-study library. If segment functions, audiovisual techniques, rhythm curves, and reusable methods become searchable across projects, the tool turns into a creator’s private craft database.

## Closing

Lapian Notes is worth paying attention to because it does not frame AI film study as a magic summary. It frames it as a pipeline: local evidence capture, AI draft, structured import, human refinement, Markdown export.

That is the right shape. AI is most useful here when it helps build a revisable working draft from well-packaged evidence. It is not a substitute for taste.

Real film breakdown is not “watching a movie and writing thoughts.” It is turning viewing into structure, structure into method, and method into the next piece of work. `lapian-notes` productizes exactly that loop.
