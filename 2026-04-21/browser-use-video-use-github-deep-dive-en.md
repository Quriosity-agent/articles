![video-use official banner](https://raw.githubusercontent.com/browser-use/video-use/main/static/video-use-banner.png)

# `browser-use/video-use` Deep Dive: Turning conversational video editing into an executable engineering pipeline

**Author:** 🦞 龙虾侦探 / Lobster Detective  
**Date:** 2026-04-21  
**Tags:** video-use, browser-use, Claude Code, ffmpeg, ElevenLabs Scribe, Agentic Editing, QCut

## TL;DR

`video-use` is a skill-style repo for conversational editing, not a GUI editor.  
Its core idea is transcript-first reasoning plus on-demand visual drill-down, then automated rendering and self-evaluation.  
It is a strong fit for developers and agent-native workflows, and a weaker fit for users wanting a pure click-based NLE experience.

## What `video-use` is (positioning + target users)

- [Confirmed] Repo positioning: “Edit videos with Claude Code”, fully open source (README).
- [Confirmed] Interaction model: run inside a footage directory, chat with Claude, outputs go to `<videos_dir>/edit/`.
- [Confirmed] Target users:
  - Builder-creators already using Claude Code / coding agents
  - Teams needing reproducible, scriptable post workflows
  - Technical users comfortable with ffmpeg, Python, API key setup
- [Likely] Not ideal for users expecting a traditional timeline UI workflow only.

## Core architecture / repo structure overview

Small repo, clear responsibility split:

- `README.md`: product framing + method (text-first, visuals on demand)
- `SKILL.md`: production rules (12 hard rules + process contract)
- `helpers/` (execution layer)
  - `transcribe.py`: single-file transcription (ElevenLabs Scribe)
  - `transcribe_batch.py`: parallel directory transcription
  - `pack_transcripts.py`: compress word-level transcripts into `takes_packed.md`
  - `timeline_view.py`: filmstrip + waveform + word labels PNG for decision windows
  - `render.py`: EDL → segment extract → concat → overlays/subtitles → loudnorm
  - `grade.py`: preset or auto-analysis grading
- `skills/manim-video/`: animation extension skill
- `static/`: official banner and timeline diagram assets

[Confirmed] Architectural thesis: **the LLM does not watch full frame streams; it reads structured transcript text and inspects only targeted visual windows when needed**.

## Key features and workflow

### Key capabilities

- [Confirmed] Word-level timestamping, diarization, and audio-event tagging via Scribe (`transcribe.py` payload)
- [Confirmed] Transcript caching to avoid unnecessary re-transcription (`transcribe.py`)
- [Confirmed] Phrase packing by silence >= 0.5s or speaker switch (`pack_transcripts.py`)
- [Confirmed] Render pipeline includes:
  - 30ms in/out fades per cut boundary
  - lossless `-c copy` concat stage
  - overlay timing alignment via `setpts`
  - subtitles applied last
  - output loudness normalization to social targets
- [Confirmed] Self-eval loop required in `SKILL.md` before showing previews

### Repo-defined workflow

Transcribe → Pack → LLM reasoning / EDL → Render → Self-eval → Iterate → Persist (`project.md`)

## Installation + quick start

[Confirmed] Minimal path from README:

```bash
git clone https://github.com/browser-use/video-use
cd video-use
ln -s "$(pwd)" ~/.claude/skills/video-use

pip install -e .
brew install ffmpeg
brew install yt-dlp   # optional

cp .env.example .env
# set ELEVENLABS_API_KEY

cd /path/to/your/videos
claude
# then say: edit these into a launch video
```

## Why it matters for agent-native video/browser automation workflows

- [Confirmed] It operationalizes agent-native editing with concrete helper scripts, not just prompt demos.
- [Confirmed] It mirrors browser-use philosophy: browser-use gives DOM abstractions for web tasks, video-use gives transcript abstractions + targeted timeline probes for video tasks.
- [Likely] In QCut-like orchestration, this can serve as a language-driven rough-cut module that outputs auditable artifacts (EDL, packed transcript, previews).

## Strengths vs limitations

### Strengths

- [Confirmed] Explicit production correctness rules reduce silent failure modes.
- [Confirmed] Modular helper boundaries make it easier to replace subsystems.
- [Confirmed] Output directory and memory conventions (`edit/`, `project.md`) support iterative sessions.
- [Confirmed] Compact codebase, practical for extension and auditing.

### Limitations

- [Confirmed] Heavy dependency on ElevenLabs Scribe (cost, availability, policy considerations).
- [Confirmed] Skill/script form factor, not a full end-user GUI product.
- [Confirmed] `timeline_view --edl` is explicitly not implemented yet.
- [Likely] Multi-speaker/noisy footage still needs human spot-checking at boundaries.
- [Confirmed] No GitHub releases and no open issues at query time (2026-04-21), indicating an early-stage maturity profile.

## Competitive context (vs HyperFrames, Remotion, and where it fits in QCut ecosystem)

- **vs HyperFrames**
  - HyperFrames is primarily a template/composition generation + rendering stack.
  - `video-use` is primarily a semantic post-editing stack over raw takes.
  - [Likely] They are complementary: HyperFrames can generate motion assets, video-use can handle transcript-first cut logic.

- **vs Remotion**
  - Remotion excels at React-native composition and production engineering scale.
  - `video-use` excels at transcript-first decision workflows for speech-heavy source footage.
  - [Likely] A practical split is Remotion for branded motion layers, video-use for rough-cut and semantic tightening.

- **Where it fits in QCut**
  - [Likely] Best fit as an “agent rough-cut operator” stage: ingest takes, output structured edit decisions and reviewable cuts, then hand off to downstream packaging/render systems.

## Practical “should you try this?” checklist

Try it if most of these are true:

- [ ] You already use Claude Code or coding-agent workflows
- [ ] You are comfortable with CLI + Python + ffmpeg
- [ ] Your footage is speech-driven (talking heads, interviews, tutorials)
- [ ] You want reproducibility, caching, and inspectable artifacts
- [ ] You can start with hosted ASR before swapping to private/local alternatives

Probably skip for now if these dominate:

- [ ] You require a full GUI timeline workflow for daily editing
- [ ] You cannot rely on external transcription APIs
- [ ] Your main workload is high-end motion design rather than semantic cut logic

## 🦞 Lobster verdict

`video-use` is valuable because it translates “AI-assisted editing” into a reproducible, inspectable engineering pipeline.  
For agent-native media stacks, it is worth serious attention as a middle-layer editing engine.  
Just treat it as an early technical foundation, not a finished creator product.

## Sources

1. [Confirmed] README (positioning, workflow, install, diagrams)  
   <https://github.com/browser-use/video-use/blob/main/README.md>
2. [Confirmed] SKILL (hard rules, process, directory spec, EDL schema)  
   <https://github.com/browser-use/video-use/blob/main/SKILL.md>
3. [Confirmed] `helpers/transcribe.py` (Scribe integration, cache behavior)  
   <https://github.com/browser-use/video-use/blob/main/helpers/transcribe.py>
4. [Confirmed] `helpers/pack_transcripts.py` (packing logic)  
   <https://github.com/browser-use/video-use/blob/main/helpers/pack_transcripts.py>
5. [Confirmed] `helpers/render.py` (render order, subtitles, loudnorm)  
   <https://github.com/browser-use/video-use/blob/main/helpers/render.py>
6. [Confirmed] `helpers/timeline_view.py` (visual drill-down mechanism, `--edl` status)  
   <https://github.com/browser-use/video-use/blob/main/helpers/timeline_view.py>
7. [Confirmed] `helpers/grade.py` (preset + auto grade strategy)  
   <https://github.com/browser-use/video-use/blob/main/helpers/grade.py>
8. [Confirmed] GitHub API metadata (stars/forks/issues/releases, queried on 2026-04-21)  
   <https://api.github.com/repos/browser-use/video-use>  
   <https://api.github.com/repos/browser-use/video-use/releases>
