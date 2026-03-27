# Generating Final Fantasy Tactics-Style Isometric Sprites with AI: The Nano Banana 2 + Veo 3.1 Pipeline

> Original tweet: [@chongdashu](https://x.com/chongdashu/status/2037109734445084684) · 2026-03-26
> Article: *Generating Final Fantasy Tactics-Style Isometric Sprites With Nano Banana 2 + Veo 3.1*

![Article cover — isometric pixel sprites showcase](https://pbs.twimg.com/media/HEVEdgzW8AA7y-e.jpg)
*Image credit: [@chongdashu](https://x.com/chongdashu)*

---

## TL;DR

Chong-U (@chongdashu) published a detailed tutorial showing how to take a single non-isometric pixel art sprite and turn it into a **full isometric 8-way turnaround with walk animation** — the kind of asset you'd need for a Final Fantasy Tactics-style game.

The complete pipeline chains **5 AI tools**: Codex → GPT 5.4 → GPT Image 1.5 → Nano Banana 2 → Veo 3.1.

## Why This Matters

In traditional game dev, producing a complete isometric 8-direction sprite set with walk cycles is brutally time-consuming. A single character needs:
- 8 directional standing poses
- Walk cycle animation per direction (4-8+ frames each)
- Consistent perspective, lighting, and proportions

Doing this by hand: days per character. With this AI pipeline: **an afternoon**.

## The Pipeline, Step by Step

Chong-U also published a [full 14-minute video walkthrough](https://x.com/chongdashu/status/2037573384674930715) with timestamps:

### Step 1: Start With a Reference Image (01:19)

Don't generate from scratch. Begin with a pixel art character you like — it doesn't need to be isometric. A front-facing or side-view sprite works fine as the anchor.

### Step 2: Choose Your Image Generation Model (04:06)

**GPT Image 1.5 vs Nano Banana 2** comparison:
- GPT Image 1.5: Good overall quality, but diagonal directions can be inconsistent
- **Nano Banana 2**: Better diagonal views (NW, NE, SW, SE) and benefits more from higher-resolution input

Chong-U built a [fal.ai custom Skill](https://x.com/chongdashu/status/2037573384674930715) to quickly switch between image generation models for A/B testing.

### Step 3: Handle Transparency (04:23)

Generated images typically come with backgrounds. You'll need to remove them to get clean transparent PNGs — automatable with standard tooling.

### Step 4: Don't Generate All 8 Directions at Once (05:21)

This is the key insight — **only generate 4 cardinal directions** (N, E, S, W), then derive the diagonals from anchor + cardinals.

### Step 5: 4 Cardinals → 8 Directions (06:17 - 07:12)

1. Generate N, E, S, W poses
2. Combine "anchor + cardinal pairs" to derive NE, NW, SE, SW
3. This approach produces **far more consistent** results than asking the AI to generate all 8 at once

### Step 6: Stitching & Utilities (08:15)

Stitch all directional sprites into a standard sprite sheet format ready for game engines.

### Step 7: Walk Cycles with Veo 3.1 (10:48)

The most impressive step — use **Veo 3.1 Fast** to animate static sprites into smooth walk cycles. Each direction gets a fluid walking animation generated from the static pose.

### Step 8: Normalize & Export (13:22)

Use the Codex app to normalize all sprites and export them in game-ready formats.

## Tool Chain Summary

| Step | Tool | Purpose |
|------|------|---------|
| Concept & Code | GPT 5.4 / Codex | Reference descriptions, code assistance |
| Static Image Gen | GPT Image 1.5 / Nano Banana 2 | Generate directional sprites |
| Animation | Veo 3.1 Fast | Static sprites → walk cycle animation |
| Model Switching | fal.ai Skill | Quick A/B testing between image models |
| Post-Processing | Codex App | Stitching, normalization, export |

## Practical Takeaways

1. **Higher-res input images matter**: Nano Banana 2 output quality scales noticeably with input resolution
2. **Generate 4, derive 8**: Cardinal-first then derive diagonals is far more consistent than generating all 8 directly
3. **Nano Banana 2 > GPT Image 1.5 for isometric**: Especially for diagonal views — NB2 handles isometric perspective more accurately
4. **Use video models for animation**: Don't try to generate animation frames with image models. Veo 3.1's walk cycle results are significantly better

## Context

Chong-U has been on a sustained [FFT-inspired "vibe coding" journey](https://x.com/chongdashu/status/2026797130510127246) — previously building a full isometric tactics game prototype with AI (3D grid, 2D animated sprites, turn-based combat, pathfinding, basic AI). This article represents the culmination of his **game art asset generation** experiments, distilled into a reproducible pipeline.

## Builder Implications

- **Indie game devs**: This pipeline dramatically lowers the pixel art barrier. One person can produce quality FFT-style sprites that previously required a dedicated artist
- **Multi-tool AI pipelines**: The solution isn't one model doing everything — it's specialized tools composed together. Image gen, video gen, and code assistance each play their role
- **Pipeline design > single-shot prompting**: Good AI art isn't about one magical prompt. It's about designing a multi-step pipeline where each stage uses the right tool for the job

---

*Tweet stats: 284 ❤️ · 29 🔄 · 8 💬*

🦞
