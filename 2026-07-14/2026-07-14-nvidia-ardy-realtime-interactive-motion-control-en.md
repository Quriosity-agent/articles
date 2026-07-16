---
title: "NVIDIA ARDY Deep Dive: AI Character Animation Is Becoming a Real-Time, Replannable Motion-Control Layer"
date: 2026-07-14
source: "https://x.com/Stefan_3D_AI/status/2077070556579696836"
canonical: "https://research.nvidia.com/labs/sil/projects/ardy/"
tags:
  - NVIDIA
  - ARDY
  - Human Motion Generation
  - 3D Animation
  - Humanoid Robotics
  - Diffusion
  - Physical AI
---

# NVIDIA ARDY Deep Dive: AI Character Animation Is Becoming a Real-Time, Replannable Motion-Control Layer

> **TL;DR:** ARDY, from NVIDIA's Spatial Intelligence Lab, turns text-to-motion from an offline generation job into a streaming control system. While a character is moving, the user can replace the text prompt, click a new waypoint, add a full-body keyframe, or constrain hand and foot positions and rotations. The model replans the future from already generated motion. It achieves this with a hybrid representation that keeps root motion explicit while compressing body motion into a latent, a two-stage Transformer that predicts root before body, and non-blocking replanning that hides inference behind a playback buffer. The paper reports 33ms average latency on an RTX 4090 for a four-step diffusion model generating a 40-frame, two-second window. ARDY still outputs kinematic skeleton motion, not a production-ready animation with collisions, scene awareness, or physical stability; its robot demonstration relies on the SONIC tracking policy to execute the plan.

- **Original post:** [Stefan 3D AI on X](https://x.com/Stefan_3D_AI/status/2077070556579696836)
- **Project:** [ARDY - NVIDIA Spatial Intelligence Lab](https://research.nvidia.com/labs/sil/projects/ardy/)
- **Paper:** [arXiv:2607.08741](https://arxiv.org/abs/2607.08741)
- **Code:** [nv-tlabs/ardy](https://github.com/nv-tlabs/ardy)
- **Models:** [NVIDIA ARDY collection on Hugging Face](https://huggingface.co/collections/nvidia/ardy)
- **Paper submitted:** 2026-07-09
- **Models released:** 2026-07-10
- **Post published:** 2026-07-14
- **Accessed:** 2026-07-16
- **Tags:** NVIDIA / ARDY / human motion generation / 3D animation / humanoid robotics / diffusion / Physical AI

## One-Sentence Take

**ARDY matters because it puts a generative model inside the character-control loop: motion is no longer generated once and edited later; it can be steered by new intent and spatial constraints while it plays.**

That changes the unit of interaction between an animator and a motion model.

Most generative motion tools behave like rendering jobs. A user supplies a prompt and constraints, waits for a complete clip, reviews it, changes the input, and generates again. ARDY shortens that loop until it fits inside the motion itself. The user can change action semantics, give the character a new destination or ground path, specify a future full-body pose, or constrain only the position and orientation of an end effector.

![ARDY source demo contact sheet showing text-to-motion, combined constraints, keyboard control, local UI, and Unreal Engine previews](imgs/nvidia-ardy-realtime-interactive-motion-control/x-demo-contact-sheet.jpg)

The source post describes the result as “Kimodo × MotionBricks.” The analogy captures the product shape. Kimodo emphasizes high-quality offline authoring under text and broad kinematic constraints. MotionBricks emphasizes low-latency runtime motion and interactive control. ARDY tries to bring the semantic and constraint range of the former into the interactive timescale occupied by the latter.

It is not a simple combination of two systems, however. ARDY redesigns the representation and generation process so text, motion history, and future constraints can condition one autoregressive diffusion model.

## What “Real Time” Means Here

“No baking, no waiting” is effective social copy. The paper gives it a more precise definition.

ARDY's deployed Core model runs at 20 fps and predicts 40 frames per call, a two-second future window. On an RTX 4090, the paper reports:

| Configuration | Generated window | Average latency | Role |
|---|---:|---:|---|
| four diffusion steps | 40 frames / 2 seconds | 33ms | lowest interaction latency, no extra buffer frame |
| ten diffusion steps | 40 frames / 2 seconds | 63ms | slightly better control accuracy, one replan buffer frame |

The 33ms number does not mean that each animation frame takes 33ms to synthesize. It is the average time to generate a two-second chunk. While the character plays already generated motion, the background thread prepares the next window. As long as production stays ahead of playback, motion appears continuous.

When text or constraints change suddenly, the system does not erase everything and freeze. It uses a small number of already generated future frames as a **replan buffer**. Those frames continue playing and simultaneously become history for the new generation call. The replacement motion is attached after the buffer.

Latency-aware replanning matters more than a headline FPS figure. An interactive system must absorb input changes without pausing, popping, or teleporting the character.

## Hybrid Representation: Precise Paths, Expressive Bodies

ARDY addresses a structural tradeoff.

Representing every joint position and rotation explicitly makes controls interpretable but produces a high-dimensional generative problem. Compressing the entire body into a latent is efficient, but the character's world-space root path can drift. A beautifully moving body that misses its destination is still unusable in a game or robot.

ARDY splits motion into:

- **explicit global root features** for translation, heading, and path in the scene;
- **a latent body embedding** produced by a motion tokenizer for pose, style, and action detail.

The default tokenizer packs four frames into each patch. Its encoder and decoder are eight-layer causal Transformers. The paper settles on finite scalar quantization, not because FSQ wins every metric, but because it remains more stable than the vanilla autoencoder, which can diverge on longer horizons.

The split resembles two layers in an animation stack. Root motion determines where the character actually travels. Body motion determines how it walks, gestures, leans, or turns. A single latent no longer has to satisfy both objectives implicitly.

## Two-Stage Denoising: Destination Before Detail

The denoiser mirrors the representation split.

![ARDY official two-stage transformer denoiser architecture](imgs/nvidia-ardy-realtime-interactive-motion-control/ardy-two-stage-denoiser.png)

At every diffusion step:

1. the `Root Transformer` predicts clean global root motion from text, history, and spatial constraints;
2. the `Body Transformer` predicts latent body tokens conditioned on that clean root;
3. the two outputs form a complete hybrid motion prediction for the next denoising step.

This is a causal priority rather than merely a parallel engineering decomposition: determine the character's position and direction first, then adapt body motion to that trajectory.

The ablation supports the choice. On constrained generation, a one-stage model records 0.164m waypoint error versus 0.024m for ARDY. Joint-position error falls from 0.101m to 0.025m. A fully explicit representation also performs worse overall on text alignment, FID, and constraint accuracy.

## One Interface for Text, Paths, and Keyframes

ARDY represents spatial constraints as a masked motion sequence. A known target position or rotation is inserted at a particular joint and time; unconstrained components remain masked. The same mechanism can express:

- root waypoints and dense ground trajectories;
- full-body keyframes;
- hand and foot positions;
- joint rotations and orientations;
- arbitrary combinations of those conditions.

A constraint does not have to fall inside the current two-second generation window. Training uses variable history lengths and future constraint tokens beyond the current window, allowing the model to begin adapting toward a more distant target. The paper's trained history and future context reach eight seconds; its method comparison lists eight seconds of history and ten seconds of future context.

This does not mean ARDY sees every detail of a goal one minute away. The interactive demo truncates context. A far-future target is initially excluded and becomes conditioning only when the rolling window approaches it. The system performs rolling long-horizon control, not infinite-context planning.

## What the Benchmarks Establish

On autoregressive text-plus-constraint generation in HumanML3D, ARDY and DiP have the same reported 0.15-second benchmark latency, but differ substantially in control error. This latency was measured on one A100 under the paper's benchmark configuration, so it is not directly comparable with the four-step, 33ms RTX 4090 interactive-demo result above.

| Setting | Method | R-Precision ↑ | FID ↓ | Joint error ↓ |
|---|---|---:|---:|---:|
| in-horizon goal | DiP | 0.609 | 0.967 | 9.20cm |
| in-horizon goal | ARDY | 0.690 | 0.092 | 2.48cm |
| out-of-horizon goal | DiP | 0.599 | 1.453 | 17.64cm |
| out-of-horizon goal | ARDY | 0.684 | 0.100 | 2.92cm |

The out-of-horizon result is the consequential one. Moving the target outside the initial generation window raises DiP's joint error from 9.20cm to 17.64cm. ARDY remains at 2.92cm. It is doing more than following a point inside the next two seconds; it uses history and distant constraints to infer how to approach the goal over time.

The paper also reports 240 side-by-side perceptual comparisons. For out-of-horizon goals, participants preferred ARDY for motion quality, semantic alignment, and goal accuracy at rates of 65.8%, 67.5%, and 64.6%, respectively. DiP received 9.2%, 7.5%, and 4.2%, with the remainder counted as ties.

These are author-reported results under the paper's own implementations and protocol, not an independent reproduction. HumanML3D preprocessing was also modified to preserve native joint rotations needed for real-time animation. Cross-paper comparisons must keep the retargeting and evaluator details attached to the numbers.

## What Was Actually Released

The release is more complete than a paper-plus-video announcement:

- GitHub includes inference code, an interactive demo, command-line generation, visualization, and a motion-correction extension;
- Hugging Face hosts four public, ungated checkpoints;
- Core models use a 27-joint skeleton at 20 fps with 8- and 40-frame horizons;
- Unitree G1 models use a 34-joint skeleton at 25 fps with 8- and 52-frame horizons;
- the CLI writes `.npz`, with a MuJoCo qpos `.csv` added for G1;
- the local interactive demo runs at `http://localhost:2333`.

Installation is not a one-click web experience. The primary tested environment is Ubuntu 22.04, Python 3.11, an RTX 4090, and NVIDIA driver 575. Core inference requires PyTorch 2.4 or later. TensorRT is optional, and first-time engine compilation can take several minutes.

Text encoding uses LLM2Vec over the gated `Meta-Llama-3-8B-Instruct`, so users need approved Hugging Face access and a token. The default GPU bfloat16 text encoder uses roughly 14GB of VRAM. It can be moved to the CPU, reducing GPU memory pressure at the cost of slower prompt encoding.

The source post's 20–24GB VRAM figure is Stefan's test observation, not a standardized paper benchmark. The official sources establish the RTX 4090 setup and the text encoder's roughly 14GB allocation. Total memory varies with checkpoint, TensorRT engines, precision, and CPU offload.

“Open source” also needs qualification. The code is Apache-2.0. Model checkpoints use the NVIDIA Open Model Agreement. Optional Bones data has separate terms, and the Llama 3 text encoder retains Meta's access and license conditions. Local and commercial use do not mean every component ships under one open-source license.

## The Missing Layers Between Demo and Production

ARDY outputs pose sequences: global root translation, joint rotations and positions, and foot contacts. It does not produce a finished Unreal or Blender scene with a skinned character, camera, cloth, facial animation, collision, and environmental interaction.

A production pipeline still looks like this:

```text
Text / path / keyframes
          ↓
ARDY skeleton motion
          ↓
Skeleton mapping and retargeting
          ↓
Foot correction, IK, collision, and scene constraints
          ↓
Final character in a game engine, DCC, or simulator
```

The repository includes optional post-processing to reduce foot skating and improve constraint hits. It is slower and disabled by default. The model card also warns that motion may slide, jitter, or miss the text; the model is strongest on locomotion, gestures, combat, dance, and everyday actions; it does not understand surrounding objects; and it does not target cartoon or physically implausible motion. Each checkpoint emits one skeleton. A Rigplay-trained SOMA checkpoint is still listed as coming soon.

ARDY is best understood as a **motion planner and authoring controller**, not a complete animation agent.

## Why the Robot Demo Is Not “The Same Model Drives the Robot”

The project page shows a Unitree G1 responding to online text and constraints, but the control chain contains another critical layer: SONIC.

ARDY generates target motion. SONIC, a physics-based tracking policy, turns that kinematic target into whole-body robot control. The real robot still has to handle dynamics, contact, balance, joint limits, and sim-to-real mismatch.

The accurate architecture is:

```text
User text / waypoint / keyframe
                ↓
ARDY: real-time motion planning
                ↓
SONIC: physical tracking and control
                ↓
Unitree G1: execution
```

That separation is more useful than a claim that one model does everything. Animation and robotics can share high-level action semantics and motion plans, while the lower layer connects to either retargeting and IK in a game engine or a physical robot controller.

## Who Should Test It Now

ARDY is especially relevant to three groups:

1. **game and digital-human teams:** test whether NPCs can follow runtime intent while respecting navigation and key poses;
2. **animation-tool builders:** turn generation from a clip button into a motion-drafting layer that can be steered continuously on a timeline;
3. **robotics and simulation teams:** convert text and sparse spatial goals into motion plans for a downstream physics policy.

Useful evaluation goes beyond replaying the official demo:

- switch prompts three times during one walk and inspect transition quality;
- reverse a path or move a waypoint and check root stability and foot sliding;
- combine text, a hand target, and a future full-body keyframe to expose constraint conflicts;
- run long autoregressive sessions and measure drift, jitter, and pose degradation;
- retarget to the production skeleton and measure the latency added by contact correction;
- compare CPU and GPU text encoding for interaction delay and memory use;
- verify whether `torch.compile` or plain PyTorch meets the runtime budget without TensorRT.

## Conclusion

ARDY moves generative animation closer to a control system.

It retains the semantics of text while treating paths, keyframes, and joint goals as spatial conditions. It does not wait for a complete clip. It rolls a future window forward and replans continuously when input changes. The explicit-root/latent-body representation, root-first two-stage denoising, and latency-aware replan buffer are the technical core of that behavior.

It is not the end of the animation pipeline. Physics, collision, object interaction, skeleton adaptation, facial performance, and final shot construction remain outside the model. Robot execution likewise depends on a physical controller such as SONIC.

ARDY still makes the direction clear: **the next step for AI animation is not producing a motion clip faster. It is turning motion generation into a runtime that continuously accepts intent, constraints, and eventually environmental feedback.**
