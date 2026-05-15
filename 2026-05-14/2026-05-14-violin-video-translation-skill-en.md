# Violin Deep Dive: Turning Video Translation into an Open-Source Claude Code Skill

Repo: <https://github.com/shang-zhu/violin>  
Live demo: <https://www.violin-ai.com>  
Inspected on: 2026-05-14  
Inspected commit: `edfb68b`  
GitHub status: 59 stars / 10 forks / MIT License

---
**Author:** 🦞 龙虾侦探 / Lobster Detective  
**Date:** 2026-05-14  
**Tags:** Violin, Video Translation, Dubbing, Claude Code Skill, FastAPI, Whisper, TTS, Together AI, Cartesia, ElevenLabs, FFmpeg
---

![Violin GitHub repo](imgs/violin-video-translation-skill/github-repo.png)

Violin looks, at first, like a video translation tool: upload a video, transcribe the speech, translate the text, synthesize a target-language voice-over, and remux the result back into the video with aligned subtitles.

But from an engineering perspective, the more interesting point is not “another dubbing demo.” It is that **Violin packages video translation into three callable surfaces: a CLI, a FastAPI web app, and a Claude Code skill.**

That means Violin is not only a webpage for humans to click. It is trying to turn “video translation” into a media skill that agents can invoke reliably.

For systems like QCut, OpenClaw, and Hermes, this is the useful lesson: future AI video tools are not just about model capability. They are about packaging transcription, translation, TTS, alignment, cost tracking, deployment, APIs, and agent instructions into composable engineering modules.

---

## One-sentence takeaway

**Violin’s value is not that it invents the video translation pipeline; it is that it productizes that pipeline into an agent-friendly open-source skill.**

Key properties:

- 33 target languages;
- handpicked native-speaker voices for 16 high-frequency languages;
- default stack: Together AI + Whisper Large v3 + DeepSeek V4 Pro + Cartesia Sonic 3;
- TTS can switch across Together, ElevenLabs, and OpenAI;
- one shared pipeline powers both the CLI and the FastAPI worker;
- the web runtime includes job lifecycle, upload limits, URL download, BYOK, trial limits, and cleanup;
- completed jobs support in-video Q&A using subtitles plus sampled frames;
- the repository includes `.claude/skills/video-translator/SKILL.md`, installable as a Claude Code skill.

This is not a one-file script. It is a small but complete AI media runtime.

---

## Repo size: small, but already product-shaped

I inspected commit `edfb68b`. The repository is compact, but its boundaries are clear:

| Metric | Value |
|---|---:|
| Total files, excluding `.git` | 66 |
| Text/code files | 50 |
| Text/code lines | about 7,598 |
| Python files | 34 files / about 5,000 lines |
| `api/` | 15 text files / about 3,360 lines |
| `pipeline/` | 17 text files / about 2,999 lines |
| Prompt/config/skill assets | `prompts/`, `config/`, `.claude/skills/` |
| Media assets | demo mp4s, posters, logo |

The directory structure tells the story:

```text
pipeline/    core video translation pipeline
api/         FastAPI server, job management, web UI, chat
prompts/     translation, style, and video-Q&A prompts
config/      defaults, production overrides, alternative providers
.claude/     Claude Code skill
assets/      logo/demo/outcome assets
```

Projects in this category often stop at the notebook or script stage. Violin has crossed the first productization threshold: it has a CLI, an API, a UI, Docker/Caddy deployment files, cost tracking, job storage, and skill distribution.

---

## Core pipeline: a five-step video translation loop

The core lives in `pipeline/orchestrator.py`, where `dub_video()` is the main entry point. Both the CLI and the FastAPI worker call the same function.

The flow is:

```text
Video
  ├─ ffmpeg → extract 16 kHz WAV audio
  ├─ Whisper Large v3 → word-level timestamps / sentence segments
  ├─ LLM → translate segments with style profile
  ├─ TTS → synthesize target-language speech per segment
  └─ ffmpeg → align video/audio, output mp4 + optional SRT
```

The important part is not merely “calling four models.” Each stage contains engineering work:

1. **Transcription**  
   `transcriber.py` processes Whisper output, merges continuous fragments, and splits them into sentence units.

2. **Translation**  
   `translator.py` translates segment batches and supports style directives. The default config even includes ASR correction hints, such as rewriting `03` to `o3` in OpenAI model names.

3. **TTS**  
   `tts.py` is a provider dispatcher. It can route to Together-hosted Cartesia, ElevenLabs, or OpenAI. The default model is `cartesia/sonic-3`.

4. **Video alignment**  
   `merger.py` uses ffmpeg to rebuild speech chunks, gap chunks, original audio, and dubbed audio. This is not a naive audio-track replacement. It handles speed clamps, freeze-frame fallback, gap audio, and single-pass AAC encoding.

5. **Subtitle output**  
   Aligned segments can be exported as SRT, which becomes both a user-facing asset and the foundation for video Q&A.

The real work is in boundary handling: timestamps, speaking speed, silent gaps, original-audio mixing, audio encoding drift, concurrency, and cost telemetry—not just API chaining.

---

## The best design choice: one pipeline, multiple entry points

Many AI media repositories fragment quickly: the CLI has one path, the web app has another, and the demo notebook has a third.

Violin’s structure is cleaner:

- CLI: `main.py` parses arguments, then calls `dub_video()`;
- Web: `api/worker.py` reads job parameters, then calls `dub_video()`;
- Skill: `.claude/skills/video-translator/SKILL.md` teaches Claude Code how to invoke the `violin` CLI.

Different product surfaces, one execution layer.

That matters for agent tools. Agents suffer when “the webpage works, but the CLI behaves differently,” or “the API works, but the skill instructions are a separate implementation.” Violin uses shared `DubOptions` and `DubResult` objects to converge those surfaces into one path.

A media capability meant for both humans and agents should look like this:

```text
Human UI ─┐
CLI      ├─ shared DubOptions → dub_video() → DubResult
API      ┤
Agent    ┘
```

This layered structure is more important than building a polished web demo first.

---

## Claude Code Skill: Violin’s most differentiated product surface

The repository includes:

```text
.claude/skills/video-translator/SKILL.md
```

And `pyproject.toml` uses `force-include` to package `.claude` into the wheel. Users can run:

```bash
violin --install-skill
```

to copy the skill into `~/.claude/skills/`.

The skill file does several practical things:

- defines trigger conditions: the user wants to translate, dub, or voice-over a video;
- limits allowed tools to `Bash` and `Read`;
- runs pre-flight checks for `violin`, the input file, and `TOGETHER_API_KEY`;
- gives decision rules for CLI vs API;
- explains style choices: kids, academic, casual, storyteller, news;
- explicitly tells the agent not to switch to OpenAI or ElevenLabs inside the skill flow, and to point users to repo configuration instead;
- warns that large videos should have rough cost quoted first.

This is a distributable operations manual. It does not merely tell Claude Code that a command named `violin` exists; it tells Claude when to use it, what to check first, what not to do, and how to report the result.

That is the value of an agent skill: packaging human operational knowledge, command-line affordances, and safety boundaries together.

---

## Web app: not a toy UI, but a job runtime

The `api/` directory is richer than the README initially suggests.

It is not just a FastAPI upload endpoint. It implements a full job lifecycle:

- `POST /jobs` uploads a video and creates a job;
- `POST /jobs/from-url` downloads a video URL using `yt-dlp`;
- `GET /jobs/{id}` polls status;
- `POST /jobs/{id}/cancel` cancels work;
- `DELETE /jobs/{id}` deletes job files;
- `GET /jobs/{id}/video` and `/srt` download results;
- `GET /jobs/{id}/segments` returns subtitle segments;
- `POST /jobs/{id}/chat` asks questions about the completed video.

The web runtime also includes production boundaries:

- file extension allowlist;
- duration probing with `ffprobe`;
- configurable maximum file size and duration;
- per-IP free-trial limits;
- BYOK for Together/OpenAI/ElevenLabs keys;
- job TTL cleanup;
- SQLite stats for cost, runtime, segments, and provider choices.

These details look mundane, but they determine whether a demo can be publicly deployed. Video jobs are large, slow, expensive, and failure-prone. A usable public demo needs these operational limits.

---

## In-video Q&A: turning subtitles and frames into post-processing assets

One easy-to-miss feature is that Violin supports asking questions about a completed video.

`api/video_chat.py` works by:

1. selecting a context window around the user’s current playback time;
2. retrieving subtitle segments inside that window;
3. sampling frames from the video with ffmpeg;
4. sending subtitle text plus frame data URLs to a vision-capable chat model;
5. returning an answer and the context range used.

This means Violin does not just output a translated video. It preserves structured intermediate assets: subtitles, segments, timestamps, and frames. Those assets can power search, Q&A, summaries, clipping, and chaptering.

For QCut, this is an important lesson: intermediate outputs in an AI video pipeline should not be treated as disposable temp files. They should become the indexing layer for later agent operations.

---

## Configuration: replaceable providers, clear defaults

Violin centralizes configuration in `config/default.yaml` and supports deep-merged overrides through `--config`.

The default stack is:

| Stage | Default provider / model |
|---|---|
| Transcription | Together / `openai/whisper-large-v3` |
| Translation | Together / `deepseek-ai/DeepSeek-V4-Pro` |
| TTS | Together / `cartesia/sonic-3` |
| Chat | Together / `Qwen/Qwen3.5-397B-A17B` |

It also supports OpenAI and ElevenLabs paths.

This configuration design has two advantages:

1. ordinary users get clear defaults and do not need to understand every model first;
2. advanced users can replace providers without modifying the core pipeline.

`pipeline/pricing.py` also records cost telemetry: Whisper per minute, TTS per million characters, and translation per million tokens. It is only informational, but it matters for a public web demo because video translation cost is driven by TTS and long media processing.

---

## Product lesson: the real problem is callability

If we only look at model capability, video translation is no longer novel. Violin’s stronger contribution is callability:

- for terminal users: CLI;
- for web users: FastAPI + browser UI;
- for agents: Claude Code Skill;
- for deployers: Dockerfile + docker-compose + Caddy;
- for advanced users: YAML provider overrides;
- for public demos: BYOK, free trial, upload limits, job TTL;
- for downstream tasks: segments, SRT, and video chat.

This is a useful open-source AI product pattern:

> Do not only open-source a model-calling script. Open-source a capability that humans, APIs, and agents can all consume.

---

## Limitations and risks

Violin is still early. The README also makes clear that it is a personal open-source project, not a Together AI product.

Important caveats:

1. **Copyright and permission risk**  
   The README explicitly tells users to process content they have rights to use: their own recordings, Creative Commons, public domain content, and so on.

2. **Long-video cost and reliability**  
   TTS characters, Whisper minutes, and ffmpeg concurrency all magnify cost and resource usage. Production deployments should set `max_duration_seconds`, `max_file_size_mb`, and `MAX_WORKERS` carefully.

3. **Multi-speaker dubbing and lip sync are not the core goal**  
   The current design is closer to voice-over dubbing than full cinematic multi-character dubbing with lip synchronization.

4. **Default configuration depends on external APIs**  
   The default path requires a Together key; OpenAI and ElevenLabs paths require their own keys. Offline or local-model deployment is not the current focus.

5. **The web surface needs continued hardening**  
   URL upload with `yt-dlp`, user-provided API keys, and public video processing all call for stronger sandboxing, log redaction, rate limiting, and abuse protection.

These limitations do not erase the project’s value. They show that Violin is in the important transition zone between demo and product.

---

## What QCut, Hermes, and OpenClaw can borrow

### For QCut

Violin demonstrates a reusable media-skill shape: input video, output translated video, SRT, segments, original-audio sidecar, and cost telemetry. QCut can treat such capabilities as pipeline nodes rather than UI-only features.

### For Hermes

The skill file itself is worth studying. It does not vaguely describe “how to translate a video.” It specifies pre-flight checks, commands, decisions, don’ts, and reporting format. That kind of skill belongs in reusable procedural memory, not in generic long-term memory.

### For OpenClaw

OpenClaw could treat Violin as an external tool dispatched by an agent: a user uploads a video or URL in Discord, the agent estimates cost and permissions, calls the CLI or API, then returns the video and subtitles. Media jobs like this belong in background task queues rather than synchronous chat turns.

---

## Closing: video translation is moving from app to skill

Violin is worth watching because it turns “video translation” from an application feature into an installable, callable, deployable, agent-readable skill.

That may be the direction for many AI media tools:

- an app is the interface for humans;
- an API is the interface for systems;
- a CLI is the interface for automation;
- a skill is the interface for agents, including operational instructions and safety boundaries.

Violin implements a small but complete version of all four layers.

For builders, the lesson is not “copy this video translation app.” It is: **if you want AI to operate a media capability reliably, do not stop at a demo. Package it as an engineering skill with configuration, cost tracking, permissions, deployment, and agent instructions.**