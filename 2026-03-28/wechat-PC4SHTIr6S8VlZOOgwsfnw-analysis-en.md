# Tiangong AI's "AIGC Suite": World Model + Video + Music — Three Models Hit Global Tier-1 Simultaneously

> Source: [中国AIGC「全家桶」来了！三箭齐发杀入全球第一梯队](https://mp.weixin.qq.com/s/PC4SHTIr6S8VlZOOgwsfnw) (Xinzhiyuan, 2026-03-27)
> Event: 2026 Zhongguancun Forum, Kunlun Tech / Tiangong AI keynote

![Tiangong AI AIGC Suite Launch](https://matrix-game-v3.github.io/static/images/teaser.png)
*Image source: [Matrix-Game 3.0 Project Page](https://matrix-game-v3.github.io/)*

---

## TL;DR

Kunlun Tech's Tiangong AI dropped three models at Zhongguancun Forum — game world model **Matrix-Game 3.0**, video model **SkyReels V4**, and music model **Mureka V9**. All three rank in the global top tier of their respective tracks. They also announced a "3+1" AGI strategy: 4 SOTA models + 3 AI-native platforms + 1 Super Agent OS.

---

## 1. Matrix-Game 3.0: A World Model That Actually Remembers

### The Problem

Previous world models were glorified video generators — fine for a few seconds, then they "forgot" everything. Scenes warped, objects vanished mid-frame.

### Key Breakthroughs

**Data Engine**
- Dual-pipeline: UE5-based synthetic data across 1000+ scenes + RL-driven AI Agents exploring autonomously
- Every frame records video + 6-DoF camera pose + action commands in millisecond alignment
- Solves the fundamental issue that internet videos lack action-state causal pairs

**Memory Mechanism**
- Model retrieves earlier "memory frames" based on camera pose, not just recent frames
- Buildings you walked past, streets you turned down — the model remembers them
- This is what separates world models from video generation

**Self-Correction**
- Training explicitly models the error between generated and ground-truth frames
- Errors are re-injected as conditioning, forcing the model to learn recovery from drift states

**Real-Time Inference**
- Multi-segment autoregressive distillation + quantization + VAE decoder distillation
- **5B model achieves 720P at 40FPS real-time generation**
- Larger MoE-28B model supports both first-person and third-person views, ~60s generation

### Competitive Position

On the interactive world model track globally: Google DeepMind's Genie 3 is the closed-source benchmark. Matrix-Game 2.0 was the first open-source implementation. 3.0 surpasses 2.0 across memory, resolution, and real-time performance — now on par with Genie 3.

Notable: Yann LeCun's AMI company ($1.03B seed round) built Solaris on top of Matrix-Game 2.0.

**Open Source:**
- Homepage: https://matrix-game-v3.github.io/
- Code: https://github.com/SkyworkAI/Matrix-Game/tree/main/Matrix-Game-3
- Model: https://huggingface.co/Skywork/Matrix-Game-3.0

---

## 2. SkyReels V4: Audio-Visual Joint Generation

### The Problem

Four chronic issues in AI video: audio-visual desync, poor controllability, no narrative logic, hard to commercialize.

### Key Breakthroughs

**Audio-Visual Joint Generation**
- Custom symmetric dual-stream MMDiT architecture — audio and video are fused at the foundation level
- Not "generate video then dub" — simultaneous generation

**Full-Modal Input, Dual-Modal Output**
- Text, images, audio/video unified in one framework
- Start/end frame control, motion trajectories, multi-image reference all supported
- Grid reference: upload up to 9 story frames → generate coherent short drama in one shot

**Narrative Capability**
- Semantic Reward model evaluates story-level coherence, not just per-frame quality
- "Ladder curriculum learning": simple still-life → walking figures → complex drama, progressive complexity

**Editing**
- Multi-character dialogue with automatic shot-reverse-shot, line assignment, expression matching
- Character replacement: one photo + one real video = seamless swap
- Instruction-based removal: "find this person and this bottle, delete them"

**Performance:** 1080P / 32fps. Topped Artificial Analysis text-to-video (with audio) global leaderboard, surpassing Veo 3.1 and Sora 2.

---

## 3. Mureka V9: AI Music Goes From "Can Generate" to "Generates What You Actually Want"

### The Problem

AI music's bottleneck isn't generation ability — it's control. Lyrics land in the wrong section, vocals miss the emotional peaks, arrangement lacks intention.

### Key Breakthroughs

- Enhanced MusiCoT (Music Chain-of-Thought) for paragraph-level lyric semantic control
- Vocals now "sing right" — not just "sing something"
- Faster generation, cleaner mix, more variety from the same creative direction
- Seamless multilingual switching (Chinese/English/French/Spanish) with consistent vocal style

### Benchmarks

Mureka V8 already topped Artificial Analysis music leaderboard (vocal + instrumental dual champion, beating Suno V4.5 and Udio). V9 subjective scores: melody 7.25, expressiveness 6.89, arrangement 6.98 — all #1, surpassing Suno V5 and Minimax 2.5. Control precision jumped from 6.93 (V8) to 7.24 (V9).

### Product

Mureka Studio: partial editing, single-track generation, multi-track control, timeline sync, Remix + Agent-driven creation workflow.

---

## 4. The "3+1" AGI Strategy

CEO Zhou Yahui's 2026 strategy:

```
Foundation: 4 SOTA Models
  - Matrix-Game (game world model)
  - SkyReels (video)
  - Mureka (music)
  - Skywork 6.0 (Agent-oriented LLM)

Layer: 3 AI-Native Platforms
  - DramaWave (AI short drama)
  - Mureka (AI music)
  - Cat Forest Academy 2.0 (AI gaming)

Core: Skywork Super Agent
  - "One-person company OS for 500M creators"
  - Memory, planning, execution, collaboration
  - End-to-end: content creation → publishing → growth → monetization
```

Key thesis: **AI is transitioning from the "foundation model tool era" to the "AI-native platform economy era."** Models are engines, platforms are factories, creators are the bosses.

---

## Builder Takeaways

1. **World models ≠ video generation — it's causal modeling.** Given current state + action → predict next state. The memory mechanism (pose-based retrieval + memory frame injection) and self-correction (error re-injection conditioning) are transferable patterns for any long-sequence generation task.

2. **Joint audio-visual generation > post-hoc stitching.** SkyReels V4's symmetric dual-stream MMDiT fuses modalities at the architecture level. This design principle applies to any multi-modal synchronous output scenario.

3. **"Ladder curriculum learning" is a general pattern.** Simple → complex task progression + semantic reward (holistic coherence over per-frame quality) — useful training strategy beyond video narrative, applicable to any task requiring long-range consistency.

4. **Open-source world model you can run today.** Matrix-Game 3.0 is fully open (code + weights). The 5B model runs 720P/40FPS. If you're building games, simulations, or anything needing interactive environments, pull it and experiment.

5. **AI music competition has shifted from "can generate" to "controllability."** MusiCoT's paragraph-level semantic control and versioned iteration workflow are the differentiators. For builders evaluating music APIs, fine-grained control capability is now the key selection criterion.

---

## Links

- Matrix-Game 3.0: [Homepage](https://matrix-game-v3.github.io/) | [GitHub](https://github.com/SkyworkAI/Matrix-Game/tree/main/Matrix-Game-3) | [HuggingFace](https://huggingface.co/Skywork/Matrix-Game-3.0)
- Kunlun Tech / Tiangong AI: [Official Site](https://www.tiangong.cn/)
- Mureka Music: [mureka.ai](https://mureka.ai)

---

🦞
