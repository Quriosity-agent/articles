---
title: "earshot Source Audit: It Does Not Give Agents Ears; It Turns Sound into Testable Evidence"
date: 2026-10-16
source: "https://github.com/donghaozhang/earshot"
canonical: "https://github.com/Leonxlnx/earshot"
tags:
  - earshot
  - Audio QA
  - Coding Agent
  - MCP
  - CLAP
  - AudioSet
  - Sound Design
  - Procedural Audio
  - FFmpeg
  - Source Audit
---

# earshot Source Audit: It Does Not Give Agents Ears; It Turns Sound into Testable Evidence

> **TL;DR:** earshot is neither a transcription tool nor a wrapper that uploads audio to a large model for a free-form opinion. It combines CLAP, an AudioSet classifier, and conventional audio measurement on a local CPU, turning sound into text, JSON, timelines, and annotated images that an Agent can reason about. It can test whether an effect resembles a “deep mechanical key,” find the best 240 milliseconds inside a long recording, measure whether an impact lands late against a visual cut, and compare a launch-film mix with a reference profile. Its `forge` loop can also synthesize sounds in code, score them, mutate parameters, and render again. The advance is making sound an inspectable engineering artifact. It still cannot judge taste, emotion, copyright, or spoken content, and its event labels inside dense mixes are much less reliable than its headline suggests.

![Frames from the earshot launch film](imgs/earshot-agent-audio-evidence-layer/earshot-launch-frames.png)

- **User-provided repository:** [donghaozhang/earshot](https://github.com/donghaozhang/earshot)
- **Upstream repository:** [Leonxlnx/earshot](https://github.com/Leonxlnx/earshot)
- **v0.1.0 release:** [Release and 22-second launch film](https://github.com/Leonxlnx/earshot/releases/tag/v0.1.0)
- **Audited snapshot:** [`108763c`](https://github.com/Leonxlnx/earshot/tree/108763c62648c78dbac14f5bebcd3c61ac7931cd)
- **Published:** 2026-10-16
- **Accessed:** 2026-10-17

## One-sentence verdict

**earshot does not simulate human hearing for an Agent. It adds Agent-readable meters, retrieval, and acceptance loops to audio production.**

Coding Agents can already write Remotion, Three.js, or game code and invoke FFmpeg to render a film. After rendering, however, they usually cannot answer basic audio questions reliably:

- Is this a deep keyboard `thock` or a cheap click?
- Which hit inside a ten-minute field recording is clean enough to use?
- Does the sound land 80 milliseconds after the picture cut?
- Does the musical peak coincide with the product reveal?
- Is the mix quiet, hot, over-compressed, or broken only in one section?
- Did a revision move closer to the reference, or did the Agent merely change its adjectives?

earshot does not solve this by asking a model for an unconstrained listening impression. It first converts audio into intermediate evidence that can be reread and compared.

## It separates “hearing” into three capabilities

### Layer one: objective measurement without a model

`measure` applies conventional signal processing to report LUFS, true peak, LRA, noise floor, attack, decay, spectrum, tempo, and key. This is the meter layer: it does not guess what an object sounds like.

For delivery QA, these numbers often matter more than adjectives. Clipping, truncated tails, excessive decoded AAC peaks, and sections that fail to approach silence are directly testable conditions.

### Layer two: semantic questions through open models

earshot downloads two models totaling approximately 1.4 GB:

- **CLAP `laion/larger_clap_general`:** maps text and audio into one embedding space for `describe`, `match`, `rank`, `find`, and similarity to references;
- **AST `MIT/ast-finetuned-audioset-10-10-0.4593`:** returns 527 AudioSet labels as an independent broad-category signal.

The repository does not misrepresent CLAP cosine as a probability. It calibrates similarity against a vocabulary, reports a z-score and a `strong / plausible / weak / no match` verdict, and preserves alternative readings. An Agent can therefore learn that a file is a strong keyboard match but resembles an Enter key more than a spacebar, rather than receiving a context-free 0.83.

### Layer three: a whole film as temporal evidence

`timeline` lists sound events, sections, loudness curves, beats, picture cuts, and offsets against cue frames. `sheet` draws video frames, event tags, a spectrogram, waveform, loudness, and synchronization markers into one PNG.

![earshot annotated listening sheet](imgs/earshot-agent-audio-evidence-layer/earshot-listening-sheet.png)

This image is the clearest product explanation in the project. An Agent that cannot play audio can inspect its temporal structure: crowded regions, intentional gaps, impacts on cuts, and soft whooshes that pass through a transition without producing a new onset.

## Sixteen CLI commands form four production loops

| Loop | Main commands | What the Agent receives |
|---|---|---|
| Asset selection | `describe`, `match`, `rank`, `find` | Sound descriptions, semantic fit, candidate order, and usable trims inside long recordings |
| Comparison and QA | `compare`, `ab`, `realness`, `measure` | Distance from references, A/B differences, real-recording vs code-synthesis tendency, and objective measurements |
| Film review | `timeline`, `sheet`, `critique`, `profile` | AV sync, listening transcript, analysis image, and a scorecard based on custom references |
| Creation and integration | `forge`, `llm`, `mcp`, `doctor` | Procedural sound search, optional Gemini opinion, Agent tools, and installation diagnosis |

This decomposition is better suited to automation than “upload a file and return a paragraph.” Every operation has explicit inputs, structured outputs, and failure behavior. A compact text summary serves the Agent; `--json` returns full data; `--out` preserves an audit artifact.

## How it differs from a general audio LLM

earshot does not upload audio by default. Its models run on a local CPU, embeddings and results are cached on disk, and analyses can be repeated offline. Only the optional `llm --yes-upload` route calls Gemini, and the implementation requires both an API key and explicit consent.

The systems also answer different questions:

| Local earshot | General audio LLM |
|---|---|
| Exact loudness, peaks, timing, and synchronization offsets | Overall impressions, narrative, and verbal advice |
| Stable ranking across hundreds of candidates | Open-ended comments on a small sample |
| JSON, timelines, and comparable metrics | Natural-language opinion |
| Project-specific reference profiles | Implicit taste from model training |
| No upload by default | Usually sends audio to a service |
| No speech-content understanding | May provide transcription and language understanding |

The best relationship is complementary. earshot supplies meters, localization, and regression evidence. An audio LLM can offer a second opinion, but its timestamps and taste judgments should still be checked through `timeline`, `ab`, and human listening.

## `forge` is the most ambitious component

`earshot forge` does not place recordings inside the generated sound. A recipe uses modal resonators, contact excitations, filtered noise, a computed room, and microphone noise to produce 48 kHz audio. A critic scores each candidate against several lenses:

```text
Define a physical synthesis recipe and parameter space
        ↓
Render a batch and normalize each result to -1 dBFS
        ↓
Compare target text, plausible confusions, real references, and measured tone
        ↓
Keep elites, shrink the step, and mutate parameters
        ↓
Re-render on unseen random seeds for robustness
        ↓
Let the Agent read the failures, edit the recipe structure, and repeat
```

The repository includes six recipes: click, impact, keypress, pluck, pop, and whoosh. This is not neural audio generation. It is evolutionary optimization over explainable DSP parameters. Every candidate retains its parameters, seed, and scores, so a poor output can be diagnosed as “500-630 Hz is 16 dB above every reference” or “the tail is too long” rather than simply rerolled.

The author also documents the Goodhart risk clearly. The search optimizes earshot's own models, so it can eventually pass every model check without becoming a better sound. The `p_real` model is especially easy to fool with a modal resonator, a room response, and a noise floor.

The README reports a small 15-trial blind comparison. One listener, the author, selected the synthesized item 8 times when it was paired with a real recording. That is interesting, but one listener and 15 decisions do not establish perceptual equivalence. Model-independent spectrum measurements, robust rerenders on new seeds, and a larger human blind test remain necessary.

## MCP makes it useful to Agents, but not every command is an MCP tool

The MCP server registers 13 tools: `measure`, `describe`, `match`, `rank`, `find`, `compare`, `ab`, `realness`, `timeline`, `sheet`, `critique`, `doctor`, and `llm_critique`.

That provides two engineering advantages:

1. Models load on the first server call and remain warm, avoiding a fresh 20-40 second startup for every command.
2. Tool metadata distinguishes read-only local analysis, local image output, and network upload. `llm_critique` is marked as open-world and still requires consent.

The README phrase “same tools as an MCP server” should not be read literally. `forge` and `profile` are absent from the MCP `TOOLS` registry, so an Agent must invoke them through the CLI or Python API. MCP operations are also serialized behind one process lock to avoid racing model imports or saturating a CPU.

This is not a critical defect. It does mean that the practical v0.1.0 runtime is hybrid: persistent MCP for repeated analysis, scripts for profile building and forge batches.

## The validation is unusually candid about scope

The repository includes evaluation commands, derived JSON, and result tables under `eval/` and `docs/VALIDATION.md`. Its main reported results are:

| Capability | Release result | Correct interpretation |
|---|---|---|
| Semantic matching | Estimated 98% precision for the right sound category in the held-out `strong` band | Exact-variant precision is about 61%; the strong ratio rests on only three wrong pairs and has a wide interval |
| Real vs synthesized | Group-held-out ROC-AUC 0.922 over 1,484 clips | Thresholds were selected on the same held-out predictions; long-file calibration includes only 23 synthesized files |
| Mixed-event detection | 93.2% recall over placed effects in a 60-second soundtrack | Recall falls to 64.7% for effects more than 6 dB under the music |
| AV synchronization | For 140 attack-aligned cues, 96% of offset estimates were within one frame | Soft whooshes and swells can still be reported as unsounded cuts |
| Event labels | Correct broad kind for roughly half of exposed events and a quarter under music | Timing and level are more reliable than the tag |
| Launch scorecard | 86% of checks fell inside leave-one-out ranges from seven reference films | It was not blind, some rules changed after the first run, and it represents only those seven films' style |

These qualifications make the project more credible. It does not call AUC “92% accuracy,” nor does it present the range of seven SaaS/AI launch films as a universal definition of taste.

## What it can and cannot judge

**Relatively trustworthy:**

- LUFS, dBTP, LRA, timing, spectrum, and hard-cut synchronization;
- whether an isolated effect matches a concrete description;
- ranking a candidate library and finding clean moments inside a recording;
- obvious forms of simple code synthesis;
- objective differences before and after a revision.

**Hints only:**

- the exact identity of events inside a dense mix;
- music genre and mood;
- “normal” ranges derived from seven reference launch films;
- `realness` for designed chimes, whooshes, and electronic music.

**Cannot judge:**

- beauty, emotion, narrative fit, or brand taste;
- what speech says;
- provenance, permission, or attribution;
- a synthesized layer completely masked by a louder mix;
- content above the models' 14 kHz front-end limit.

earshot is therefore best understood as sound QA and retrieval infrastructure, not the final creative director.

## Source audit: inspectable, but not a turnkey mature product

The user-provided `donghaozhang/earshot` repository is a fork of `Leonxlnx/earshot`. At review time, both `main` branches pointed to the same `108763c` commit. The repository contains one root commit; `pyproject.toml` identifies version `0.1.0`, marks it Alpha, and licenses the code under MIT.

The snapshot contains:

- the Python package, 16 CLI commands, and 13 MCP tools;
- CLAP and AST wrappers, calibration vocabulary, realness weights, and a launch profile;
- six forge recipes and evolutionary search;
- two Agent skills: `earshot` for listening and `real-sound` for producing soundtracks from licensed recordings;
- tests, evaluation scripts, derived JSON, validation reports, and a limits document.

I ran `compileall` over the package, tests, evaluation scripts, and skill scripts under Python 3.14; static syntax compilation passed. I did not install PyTorch, Transformers, SciPy, and the other complete dependencies or download the approximately 1.4 GB of models. The repository's stated “128 passed, 14 skipped” release result is therefore not presented as a local test run.

The full evaluation also cannot be reconstructed from a clone alone. Its 344 Freesound/Mixkit recordings, seven professional films, and production project are withheld for licensing reasons. The repository contains scripts, descriptions, and derived numbers. That is considerably more transparent than a benchmark screenshot, but still means “method and results are inspectable,” not “raw data is fully reproducible.”

The one-commit snapshot also shows minor documentation drift. `docs/DESIGN.md` still says “No synthesized deliverables,” while the README and skill make `forge` a central capability. A line in the skill says no human has listened yet, while the README now reports the author's 15-trial blind test. This does not break the main code path, but it is a reminder that the README, skills, and design notes are rapidly evolving v0.1 material rather than a stable specification.

## Where it is useful in video, games, and Agent workflows

earshot fits processes that can already render media but cannot yet review their own audio:

1. After an Agent downloads candidate effects, use `rank` to build a shortlist.
2. Use `find` to extract a clean moment from the winning recording.
3. Gate it through `describe`, `realness`, and objective measurements.
4. After mixing, generate a `timeline` and `sheet`.
5. Check cue synchronization and use `ab` to verify each revision.
6. Build a profile from the project's own admired films rather than blindly using the bundled seven.
7. Keep final taste, narrative, and brand approval with a human listener.

The bundled `real-sound` skill expands this into a fuller soundtrack workflow: license manifests, design JSON, a deterministic mixer, stems, loudness and sync QA, credits, and muxing. earshot itself is the ear and the meters; the skill is the production procedure that surrounds them.

## Conclusion

earshot matters less as proof that AI can finally hear like a person than as a system that converts audio into evidence an Agent can preserve, compare, cite, and use to trigger rework.

For one effect, it can describe, retrieve, trim, and compare. For a finished film, it can produce an event timeline, synchronization readings, and an annotated analysis image. For procedural sound, it can put synthesis parameters inside a generate-score-mutate-retest loop. CLI, Python, MCP, and skills make these capabilities available inside long-running Coding Agent workflows instead of isolating them in a standalone audio application.

Measurement is not taste, sounding real does not establish provenance, and passing the system's own critic does not mean a person likes the result. As an automatic creative director, earshot would overpromise. As a test framework and evidence layer for sound production, it fills a genuinely scarce part of the Agent stack.

## Sources

- [donghaozhang/earshot - user-provided fork](https://github.com/donghaozhang/earshot)
- [Leonxlnx/earshot - upstream](https://github.com/Leonxlnx/earshot)
- [v0.1.0 release and launch film](https://github.com/Leonxlnx/earshot/releases/tag/v0.1.0)
- [Validation report](https://github.com/Leonxlnx/earshot/blob/108763c62648c78dbac14f5bebcd3c61ac7931cd/docs/VALIDATION.md)
- [Documented limits](https://github.com/Leonxlnx/earshot/blob/108763c62648c78dbac14f5bebcd3c61ac7931cd/docs/LIMITS.md)
- [Design notes](https://github.com/Leonxlnx/earshot/blob/108763c62648c78dbac14f5bebcd3c61ac7931cd/docs/DESIGN.md)
- [MCP server implementation](https://github.com/Leonxlnx/earshot/blob/108763c62648c78dbac14f5bebcd3c61ac7931cd/earshot/mcp_server.py)
- [Forge search implementation](https://github.com/Leonxlnx/earshot/blob/108763c62648c78dbac14f5bebcd3c61ac7931cd/earshot/forge/search.py)

*Audited on 2026-10-17 at commit `108763c62648c78dbac14f5bebcd3c61ac7931cd`. The user-provided fork and upstream were identical at that point. The release film was verified as a 22-second, 1920x1080 H.264/AAC file; both images come from the repository's `docs/media/` folder. Static syntax compilation passed, but this review did not install the full model stack or rerun benchmarks whose licensed source media is unavailable.*
