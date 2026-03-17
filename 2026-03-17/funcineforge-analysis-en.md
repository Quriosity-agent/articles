# FunCineForge: The Complete Open-Source Pipeline for AI Movie Dubbing

> From Tongyi Lab + USTC — an end-to-end toolkit that builds dubbing datasets and a zero-shot dubbing model for real cinematic scenes.
> Repo: [FunAudioLLM/FunCineForge](https://github.com/FunAudioLLM/FunCineForge) | Paper: [arXiv:2601.14777](https://arxiv.org/abs/2601.14777) | Demo: [funcineforge.github.io](https://funcineforge.github.io/)

![FunCineForge Overview](https://opengraph.githubassets.com/1/FunAudioLLM/FunCineForge)
*FunCineForge GitHub repository (Source: GitHub / FunAudioLLM)*

---

## The Problem

Movie dubbing is deceptively hard. You need lip sync, correct timbre, emotional expression, and multi-speaker handling — all at once. Current approaches fail for two reasons:

1. **Bad datasets** — existing dubbing datasets are small, poorly annotated, have high word error rates, and only cover monologue scenes
2. **Weak models** — they only look at lip regions for alignment, which breaks down in real cinematic scenes with shot changes, multiple speakers, and complex staging

FunCineForge attacks both: **an automated dataset pipeline + an MLLM-based dubbing model.**

---

## Architecture: Two Core Components

### 1. Dataset Production Pipeline (5-Stage)

This is the most practically useful part. Feed it raw TV/film footage, get back high-quality dubbing training data:

| Stage | What It Does | Tech |
|-------|-------------|------|
| ① Normalize | Standardize formats, trim intros/outros, extract audio | ffmpeg |
| ② Separate | Split vocals from music/SFX | Speech Separation module |
| ③ Clip | Segment long videos into sentence-level clips with subtitles | VideoClipper (ASR + timestamps) |
| ④ Diarize | Multimodal active speaker recognition, extract face/lip data | Speaker Diarization (audio + video) |
| ⑤ CoT Correct | MLLM Chain-of-Thought reasoning to fix ASR + speaker labels | Gemini / Qwen multimodal LLMs |

**Stage 5 is the key innovation** — using a general-purpose multimodal LLM (recommended: Gemini 3 Pro) for CoT correction:

- Input: audio + ASR transcript + RTTM speaker labels
- Output: corrected text + speaker attributes (age, gender, timbre) + emotional clues
- Results: **CER dropped from 4.53% → 0.94%, speaker diarization error from 8.38% → 1.20%**

Better than human annotation.

### 2. Dubbing Model (MLLM-Based)

A multimodal LLM dubbing model that goes beyond lip-reading:

- **Full scene understanding** — uses entire video context, not just lip region
- **All scene types** — monologue, narration, dialogue, multi-speaker
- **Zero-shot** — no target speaker training data needed
- **Emotion-aware** — understands and reproduces character emotion

Inference code is open-sourced, runs on consumer GPUs:

```bash
cd exps
bash infer.sh
```

---

## CineDub Datasets

Built using the pipeline on classic film/TV:

- **CineDub-CN**: Chinese TV drama dubbing (Romance of the Three Kingdoms, Dream of the Red Chamber)
- **CineDub-EN**: English TV (Downton Abbey)

Each sample has exceptionally rich annotations:

```json
{
  "text": "If the king is wise, he naturally knows that even if I lose my head...",
  "speakers": [
    {"id": "1", "age": "middle-aged", "gender": "male", "timbre": "deep, calm, firm"}
  ],
  "clue": "A middle-aged male states his position with calm determination...",
  "emotion": "tension 0.9"
}
```

This annotation density is unprecedented in dubbing datasets.

---

## The CoT Prompt Design Is Worth Studying

The `cot.py` prompt engineering is textbook-quality for multimodal applications:

1. **Clear role** — "You are an expert in audio analysis and error correction"
2. **Staged tasks** — count speakers → analyze attributes → identify content → match speakers → summarize emotion
3. **Strict output format** — complete JSON schema with examples
4. **Bilingual** — separate Chinese and English prompts, adapted per language rather than translated

If you're building any MLLM-powered annotation system, study this file.

---

## What This Means for Builders

### Ready to Use
- **The pipeline generalizes** — any audio/video annotation project can reuse the 5-stage approach
- **CoT correction is a pattern** — using general MLLMs to fix specialized model output works for any annotation task
- **Inference is open** — consumer GPU, open checkpoints, ready to run

### Current Limitations
- Linux only
- CineDub uses classic film/TV footage (CC-BY-NC 4.0) — check licensing for commercial use
- Multi-speaker API still under development
- Training code not yet released (inference only)

### Technical Takeaways
- **MLLM-as-corrector** is a major emerging pattern — cheaper and more accurate than building perfect specialized models
- **Movie dubbing is just the start** — the pipeline works for audiobooks, game localization, educational content
- **CosyVoice3 tokenizer** integration signals deep ties with the Tongyi speech ecosystem

---

## Quick Start

```bash
# Clone + setup
git clone git@github.com:FunAudioLLM/FunCineForge.git
conda create -n FunCineForge python=3.10 -y && conda activate FunCineForge
sudo apt-get install ffmpeg
python setup.py

# Run inference
cd exps
bash infer.sh
```

To build your own dubbing dataset, follow the 5-stage pipeline. The critical step is Stage 5 CoT correction — you'll need a multimodal LLM API key (Gemini recommended).

---

## Bottom Line

FunCineForge is the most complete open-source movie dubbing system available — it gives you both the model and the tools to build your own training data. From Tongyi Lab with academic rigor and production-grade engineering.

**Who should care:** Teams working on speech synthesis, post-production, dubbing tools, or audio/video data annotation.

🦞
