---
title: "Mapping Eight Opus 5.5 Video Repositories: Prompt Collections, Skills, Templates, and Full Builds"
date: 2026-10-21
source: "https://x.com/KinGao476942/status/2112729924943634602"
tags:
  - Claude Opus 5.5
  - AI Video
  - Code-Rendered Video
  - Claude Code
  - Agent Skill
  - Prompt Library
  - Motion Graphics
  - Three.js
  - p5.js
  - FFmpeg
  - Source Audit
---

# Mapping Eight Opus 5.5 Video Repositories: Prompt Collections, Skills, Templates, and Full Builds

> **TL;DR:** On October 21, 2026, Kin recommended eight GitHub repositories for making video with Claude Opus 5.5. The list is useful, but the repositories are not eight interchangeable tools. Three are mainly case or prompt indexes, three are reusable skills, style labs, or character-animation foundations, and two are complete implementations of music videos built around the same song. Together, they do not prove that Opus 5.5 is a new video-generation model. They show that a coding agent can write Canvas, SVG, Three.js, p5.js, Blender, and audio code, then drive frame-by-frame rendering and FFmpeg delivery. The useful collection is not a star ranking. It is an evidence ladder: **source case → complete prompt → runnable source → deterministic render → sound and delivery QA.**

![Awesome Opus 5.5 community video mosaic](imgs/opus55-video-eight-repo-production-map/awesome-opus55-mosaic.webp)

- **Source post:** [Kin: eight GitHub repositories for Opus 5.5 video](https://x.com/KinGao476942/status/2112729924943634602)
- **Published:** October 21, 2026
- **Audit method:** Checked the current default branch, README, tree, runtime entry points, licenses, and structured data for all eight repositories
- **Audit date:** October 21, 2026

## One-sentence verdict

**These are not eight video-making shortcuts. They form a ladder from inspiration search and prompt study to reusable style systems and complete rendering projects.**

Starring all eight repositories without distinguishing their roles is not especially useful. First identify the missing layer:

- Need examples? Use an index.
- Need prompt structure? Use the Chinese handbook or motion-design style lab.
- Need a repeatable production method? Install a skill or animation foundation.
- Need a finished project to dissect? Read the two P(doom) implementations.

## The star counts are accurate, but stars do not measure capability

The source post's rounded figures closely matched the GitHub API on October 21:

| Repository | Star snapshot | Actual type | Directly renderable? |
|---|---:|---|---|
| `yihui-dev/awesome-opus5-5-videos` | 7,171 | Prompt and source-post corpus | No; remakes live on external Skillry |
| `lemomo-ai/lemo-opuscar` | 4,418 | Claude Code skill plus 51 film styles | Yes, with varying reproducibility |
| `mexicat/pdoom-video` | 2,974 | Complete TypeScript/Three.js music video | Yes, 1080p60 and 4K60 |
| `JohnHeibel/PDoomVideo` | 2,317 | Complete p5.js/p5.brush music video | Yes, resumable frame rendering |
| `Vincentwei1021/mg-styles-15` | 1,422 | Fifteen-style motion-design lab | Yes, with prompts, source, sound, and films |
| `JohnHeibel/ClaudeAnimationBase` | 1,325 | Hand-drawn character-animation starter | Yes, including 31 acted emotions |
| `athemeroy/awesome-claude-5-5-videos` | 557 | Evidence-oriented research index | No; intended for research and selection |
| `joeseesun/opus-video-prompts` | 517 | Chinese case and prompt handbook | No; 18 full prompts and 54 case records |

Stars measure distribution, not deliverables. A 7,000-star corpus may not render anything locally, while a 500-star project can contain a fuller timeline, renderer, and evidence record. Select by artifact, not rank.

## The eight repositories contain four kinds of asset

### Layer 1: discovery and inspiration

`awesome-opus5-5-videos`, `awesome-claude-5-5-videos`, and `opus-video-prompts` all answer “What has already been attempted?” Their evidence depth differs:

- `awesome-opus5-5-videos` optimizes for coverage and searchable prompts;
- `awesome-claude-5-5-videos` emphasizes provenance, model labels, inputs, revisions, and cost;
- `opus-video-prompts` turns representative cases into Chinese-language templates.

These are useful for project selection and comparing technical routes. They should not be described as containing every project's source code.

### Layer 2: reusable style and production rules

`lemo-opuscar` and `mg-styles-15` move beyond one prompt. They define a production contract: output format, technical route, pacing, sound, assets, rendering, and acceptance.

![Lemo-Opuscar style library](imgs/opus55-video-eight-repo-production-map/lemo-opuscar-cover.jpg)

The benefit is that an agent no longer invents the workflow from scratch. A creator can change the story, brand, palette, or footage while preserving signature features and delivery rules.

### Layer 3: character and animation foundations

`ClaudeAnimationBase` extracts the reusable parts of the P(doom) project: character views, eyes, mouths, hats, dances, camera, paper texture, and 31 emotions with body performance.

![ClaudeAnimationBase emotion sheet](imgs/opus55-video-eight-repo-production-map/claude-animation-emotions.jpg)

It is not a model that turns one sentence into arbitrary animation. It is a starter kit that lets a coding agent spend less effort rebuilding a character system and more effort on storyboarding and acting.

### Layer 4: complete film projects

The two P(doom) repositories are the best place to learn why a finished project is complicated. They contain picture code, lyric alignment, beats, scene windows, browser preview, frame export, and FFmpeg assembly.

![PDoomVideo rendered frame](imgs/opus55-video-eight-repo-production-map/pdoom-video-frame.jpg)

They have fewer templates, but they reveal much more of one completed film.

## 1. awesome-opus5-5-videos: a prompt corpus, not a source-code archive

The current repository is pinned at `92aee2f` and contains 703 prompt records. Of those, 418 have a live remake on Skillry. The repository itself consists of a README, `data/videos.json`, and `prompts/`. It does not contain 703 HTML or JavaScript projects, original asset sets, full videos, or a shared renderer.

It is strong for:

- checking whether a visual form has already been attempted;
- comparing Canvas, SVG, GSAP, Three.js, and GLSL approaches;
- studying how prompts specify duration, shots, style, and tooling;
- returning to the creator's original disclosure.

It is weak evidence for the claim that copying a prompt reproduces the film. Some prompts are incomplete, and a third-party remake is not the creator's original project.

## 2. lemo-opuscar: the closest thing to a complete skill system

The source post's “51 styles” is current. That is eight more than the 43-style version previously audited in this repository, and upstream moved from snapshot `227e00a` to `b5e8ef9`.

Lemo-Opuscar provides more than style names:

- `SKILL.md` for the agent entry point and installation;
- `DIRECTOR.md` for storyboarding and acceptance;
- `TECHNIQUE.md` for browser rendering, sound, and technical boundaries;
- `core/render/` for preview, stills, video, subtitles, and muxing;
- a `STYLE.md`, poster, film, and varying levels of source for each style.

It suits creators who want to make code-rendered films repeatedly because production knowledge has become an agent-readable system. The 51 demos are not 51 identical one-command builds, however. Tooling, assets, and completeness differ between styles.

## 3. mexicat/pdoom-video: the most engineered 4K60 implementation

This version uses TypeScript, Three.js, Bun, Vite, Playwright, and FFmpeg. Every frame is a deterministic function of song time, so browser preview and offline export share one timeline.

It publishes more than visuals:

- beat and section data at 132.007 BPM;
- lyric timing produced with Demucs, CTC forced alignment, and a Whisper cross-check;
- 17 primary scene modules and a post-processing system;
- tile-adaptive supersampling for motion blur;
- commands for 1080p60 and true rerendered 4K60 output.

The claim that it can render 4K60 locally is real, but it is not lightweight. The README reports roughly 57 minutes for the full 4K render on an M5 Pro, about 23 GB peak memory, and a roughly 13 GB CRF 16 output. This is a sophisticated project to study, not an instant template for ordinary hardware.

The code is MIT-licensed, while the song, lyrics, and related timing data are explicitly outside that license.

## 4. JohnHeibel/PDoomVideo: better for studying the jump from version one to version two

The other P(doom) repository is not a mirror of the TypeScript project. It uses p5.js, p5.brush, headless Chrome, and FFmpeg, dividing the 156.6-second film into nine chapters.

It preserves a first version in `legacy/`, the second version, `STORYBOARD.md`, and an `ANIMATION_GUIDE.md` written for parallel subagents. This makes it useful for studying:

- what failed in the first generation;
- how the agent wrote a storyboard and delegated execution;
- how chapters share characters, props, lyrics, and one timeline;
- how a long frame render can resume instead of restarting.

The repository has no root license file. Public source visibility does not automatically grant permission to copy, modify, or commercially redistribute it.

## 5. mg-styles-15: the best learn-by-running course in the list

This repository contains only 15 styles, but each has a ten-second film, style notes, a complete prompt, full source, a soundtrack script, and asset-generation tools. Every film went through two rounds of AI review and revision.

![MG Styles production flow](imgs/opus55-video-eight-repo-production-map/mg-styles-flow.webp)

Its core interface is `window.renderAt(t)`: any moment can be redrawn independently. Headless Chrome captures frames, `audio.py` synthesizes music and effects from the same cue sheet, and FFmpeg produces an exact ten-second file. This is a clear, teachable, extensible production contract.

The documentation also describes its limits. Font files are not redistributed. The same prompt will not automatically recreate the same film. The published examples were iterated several times. Some soundtracks are not bit-identical across numerical-library versions. That honesty makes the repository more useful than a “copy and get this result” promise.

## 6. ClaudeAnimationBase: not 31 faces, but 31 acted states

The source `EMO` object defines 31 states, from `neutral`, `happy`, and `sad` through `furious`, `dizzy`, `mischief`, and `hopeful`. Each changes more than eyes and mouth: it includes body motion, arms, offset, rotation, beat response, and an entry take.

That makes the project more useful than a sprite sheet. The agent receives a performance API. Its workflow asks the model to read `ANIMATION_GUIDE.md`, storyboard first, build shot by shot, and inspect contact sheets before rendering.

p5.brush watercolor fills are expensive. The project recommends lighter fills without a dedicated GPU. Software rendering works, but slowly.

## 7. awesome-claude-5-5-videos: a research archive, not a smaller duplicate

As of October 11, the repository recorded 424 distinct source posts, including 301 labeled Opus cases, with nine-frame preview sampling for 199. It also tracks Sonnet, Haiku, and creator-reported Fable work, then analyzes inputs, revisions, total task cost, and the division between planner and executor models.

![Content-domain and visual-style heatmap](imgs/opus55-video-eight-repo-production-map/awesome-claude-domain-style-heatmap.svg)

Its value is not having fewer entries than the 703-prompt corpus. Its evidence model is stricter. It separates creator claims, visible frames, model labels, and reusable projects, and explicitly says that nine-frame sampling cannot verify complete motion or hidden model calls.

For reports, competitive analysis, and understanding what Opus actually did, this repository is more useful than a plain prompt list.

## 8. opus-video-prompts: a good Chinese entry point, but not 54 full prompts

The repository's `cases.json` contains 54 case records. Its README summarizes methods, time, and cost, while `prompts/` contains 18 full templates. Its strongest contribution is Chinese explanation across multiple routes: one-file Canvas, p5.js, Remotion, HyperFrames, Manim, Python, Three.js, professional-software control, and editing supplied footage.

It teaches the ingredients of a useful prompt: output specification, duration, shot count, references, banned effects, deterministic timing, and self-review.

The 54 cases should not be described as 54 copy-ready prompts or 54 local source projects. The repository also has no declared root license, so commercial reuse should be checked against each original source.

## The actual stack revealed by all eight repositories

The common workflow is not prompt → video model → MP4. It is:

```text
creative brief / audio / assets
            ↓
Opus 5.5 plans shots, timeline, and technical route
            ↓
writes Canvas / SVG / p5.js / Three.js / Blender / Remotion code
            ↓
browser or DCC reconstructs any frame at time t
            ↓
Playwright / Puppeteer / Blender renders frame by frame
            ↓
FFmpeg and audio scripts assemble the MP4
            ↓
contact-sheet, frame, audio, and full-playback QA
```

Opus acts as director, programmer, and production coordinator. The browser or Blender draws the pixels; FFmpeg creates the deliverable. That is why the result is editable and inspectable, but dependency setup, render time, and engineering complexity can exceed a one-shot video-model call.

## A practical learning order

### For a quick first experiment

1. Choose a Chinese template from `opus-video-prompts`.
2. Learn deterministic `renderAt(t)` and review rubrics from `mg-styles-15`.
3. Start with ten seconds, 24 fps, and one style instead of a four-minute music video.

### For hand-drawn character films

1. Use `ClaudeAnimationBase` for the character and storyboard.
2. Study `PDoomVideo` for chapters and transitions.
3. Add resumable rendering, contact sheets, and a complete decode pass.

### For repeat production

1. Use `awesome-claude-5-5-videos` to identify evidence-backed workflows.
2. Install `lemo-opuscar` to turn style, direction, and technique into a skill.
3. Borrow deterministic timing, audio analysis, and high-quality export from `mexicat/pdoom-video`.

## Five questions to ask before starring a repository

| Question | Why it matters |
|---|---|
| Is there source code or only a prompt? | Determines whether the result can be reproduced and edited |
| Is there a single time function? | Determines frame stability, parallelism, and resumability |
| Are audio, fonts, and assets available? | Determines whether local output can match the demo |
| Are there render and acceptance commands? | Separates a showcase from a production project |
| Which files does the license cover? | Code licenses may not cover songs, fonts, images, or prompts |

A green CI check, an MP4 file, and a README saying “made with Opus” prove different things: publishing succeeded, a file exists, and an author made a claim. None alone proves independent model authorship, clean-environment reproducibility, or commercial rights.

## Conclusion

Kin's list captures eight representative repositories from the Opus 5.5 video wave. Its real value is not that bookmarking them makes someone a video creator. Together, they show four kinds of infrastructure emerging around code-rendered video: case corpora, prompt education, agent skills, and runnable film projects.

Three methods are more reusable than any single magic prompt:

1. **Write visual style as a specification, not a pile of adjectives.**
2. **Make every frame depend only on time `t`, enabling deterministic, parallel, resumable rendering.**
3. **Have the agent inspect contact sheets, listen to the mix, and revise before final export.**

For inspiration, begin with the three indexes. To learn production, run `mg-styles-15`, `ClaudeAnimationBase`, and the two P(doom) projects. To make the process reusable by an agent, `lemo-opuscar` is the closest thing in the list to a complete production system.

## References

- [Kin's original X list](https://x.com/KinGao476942/status/2112729924943634602)
- [yihui-dev/awesome-opus5-5-videos](https://github.com/yihui-dev/awesome-opus5-5-videos)
- [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar)
- [mexicat/pdoom-video](https://github.com/mexicat/pdoom-video)
- [JohnHeibel/PDoomVideo](https://github.com/JohnHeibel/PDoomVideo)
- [Vincentwei1021/mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15)
- [JohnHeibel/ClaudeAnimationBase](https://github.com/JohnHeibel/ClaudeAnimationBase)
- [athemeroy/awesome-claude-5-5-videos](https://github.com/athemeroy/awesome-claude-5-5-videos)
- [joeseesun/opus-video-prompts](https://github.com/joeseesun/opus-video-prompts)

*This article uses repository snapshots and GitHub API data from October 21, 2026. Star counts will change. I inspected the current default-branch README, root, recursive tree, runtime entry points, structured data, and license state for all eight repositories, but did not rerender every film. Images come from public project READMEs or documentation. Claims about model involvement remain creator reports unless independently demonstrated.*
