---
title: "NVIDIA Kimodo Deep Dive: How 700 Hours of MoCap Turn Motion Generation Into a Programmable Data Engine"
date: 2026-03-16
source: "https://research.nvidia.com/labs/sil/projects/kimodo/"
canonical: "https://research.nvidia.com/labs/sil/projects/kimodo/"
tags:
  - NVIDIA
  - Kimodo
  - Human Motion Generation
  - Motion Capture
  - 3D Animation
  - Humanoid Robotics
  - Diffusion
  - Physical AI
---

# NVIDIA Kimodo Deep Dive: How 700 Hours of MoCap Turn Motion Generation Into a Programmable Data Engine

> **TL;DR:** Kimodo from NVIDIA's Spatial Intelligence Lab is an offline kinematic motion diffusion model trained on 700 hours of high-quality optical motion capture. It combines text with full-body keyframes, hand and foot position or rotation targets, 2D paths, waypoints, and foot contacts. The important advance is not merely making a character move from a sentence. Kimodo produces editable, exportable, retargetable skeleton data that can enter animation tools, simulation, and physics-policy training. Constraint imputation and a root-first two-stage Transformer turn creative intent into structured motion assets. It still lacks scene understanding and physical guarantees, however, and practical limits include ten seconds per prompt, foot sliding, conflicting constraints, and weak G1 post-processing.

- **Project:** [Kimodo - NVIDIA Spatial Intelligence Lab](https://research.nvidia.com/labs/sil/projects/kimodo/)
- **Paper:** [Kimodo: Scaling Controllable Human Motion Generation](https://arxiv.org/abs/2603.15546)
- **Code:** [nv-tlabs/kimodo](https://github.com/nv-tlabs/kimodo)
- **Models:** [NVIDIA Kimodo collection on Hugging Face](https://huggingface.co/collections/nvidia/kimodo-v1)
- **Demo:** [Kimodo on Hugging Face Spaces](https://huggingface.co/spaces/nvidia/Kimodo)
- **Initial release:** 2026-03-16
- **Accessed:** 2026-07-16
- **Tags:** NVIDIA / Kimodo / human motion generation / motion capture / 3D animation / humanoid robotics / diffusion / Physical AI

## The One-Sentence Take

**Kimodo does not make text-to-motion behave more like video generation. It turns motion capture into a motion-data layer that can be queried, constrained, and synthesized at scale.**

That distinction matters.

A video model outputs pixels. Kimodo outputs a skeleton sequence with root positions, joint positions and rotations, velocities, and foot-contact states. The result can continue into a DCC tool, game engine, retargeting pipeline, MuJoCo, or physics-policy training without recovering pose from rendered video.

Text specifies what should happen. Paths and keyframes specify where, when, and in which pose it should happen. The model fills in the large amount of bodily motion that neither input explicitly describes.

In that sense, Kimodo behaves like a **motion compiler**: it accepts high-level intent plus partial specifications and emits a structured motion asset that downstream systems can consume.

## The Value of 700 Hours Is Control, Not Just Vocabulary

Kimodo was trained on 700 hours of optical motion capture from Bones Rigplay. The dataset includes 170 performers with a roughly even gender split. It covers locomotion, gestures, everyday activities, object interactions, game combat, dance, and athletics, along with styles such as tired, angry, happy, scared, drunk, injured, stealthy, old, and childlike.

Each recording has both an overview description and fine-grained labels for atomic action segments. The team used Qwen3-32B to rewrite descriptions into a consistent prompt style. It also stitched random clips and generated transitions between them to create more compositional training sequences.

Scale here should not be reduced to learning more action verbs.

The paper's scaling experiment deliberately preserved the same action categories in 10%, 50%, and 100% data subsets. Smaller subsets simply contained fewer performers and takes for each behavior. As data increased, R-precision and FID changed little, while foot skating and every constraint error consistently improved.

The additional mocap therefore teaches the model **the different natural ways a body can realize the same intent**. With only a few sparse keyframes, Kimodo must invent weight shifts, stride length, arm swing, and transition timing. Diverse performances of repeated actions supply that completion prior.

There is an important data caveat. Kimodo contrasts the common 30-hour HumanML3D benchmark with its 700 hours of higher-quality optical mocap, but the full Rigplay training set is not public. NVIDIA also releases checkpoints trained on 288 hours of public BONES-SEED data for reproducibility and comparison. The repository explicitly says those models are less capable than their Rigplay counterparts.

## Text Is Only the First Control Layer

Kimodo's inputs look much closer to an animation authoring interface than a single prompt box:

- text describes behavior, style, and sequential actions;
- full-body keyframes lock an entire pose at a chosen frame;
- end-effector constraints set hand or foot position and rotation;
- 2D waypoints ask the character to cross a ground coordinate at a particular time;
- dense root paths define continuous travel over an interval;
- foot-contact constraints specify whether a foot should touch the floor;
- multiple constraint types can be mixed with text.

![Kimodo interactive authoring demo with prompts, full-body keyframes, end-effector controls, root waypoints, and timeline tracks](imgs/nvidia-kimodo-controllable-motion-data-engine/kimodo-authoring-demo.png)

That interface supports several workflows: generate an in-between transition between two mocap clips, make an existing behavior follow a navigation path, place a hand near an object for a pick-and-place draft, or randomize paths and keyframes to synthesize diverse robot demonstrations.

These are not hard constraints in the physics-engine sense. Kimodo aims near each target, then the official demo applies IK, foot locking, and short optimization to tighten the result. On the best SOMA model, the paper reports 3.21cm average full-body keyframe error, 3.63cm end-effector position error, 6.88 degrees of end-effector rotation error, and 3.63cm root path or waypoint error. These are author-reported numbers under one test protocol. Post-processing can improve them, but they should not be compared directly across different skeletons, frame rates, and evaluators.

## How Constraints Enter the Diffusion Process

Kimodo's cleanest design decision is to represent target motion and generated motion in the same feature space.

Each frame contains:

- a smoothed global root position;
- a global root heading;
- joint positions relative to the smoothed root;
- global joint velocities;
- 6D global joint rotations;
- four contact flags for the left and right heels and toes.

When a user provides a position or rotation, the system builds a binary mask identifying which features at which frames are constrained. Before every denoising step, target values directly overwrite the corresponding values in noisy motion. The mask is concatenated with the motion features and passed into the Transformer.

```text
noisy motion + target motion + constraint mask
                    ↓
       overwrite constrained features
                    ↓
      denoiser fills the unknown motion
```

This imputation mechanism creates one control interface. A sparse pose, a continuous path, and the rotation of one hand are all known values in different parts of the same motion tensor. Kimodo does not need a separate ControlNet for every control type, nor expensive and unstable gradient optimization during inference.

## Two-Stage Transformers: Get There First, Then Decide How the Body Moves

Kimodo also separates root and body prediction.

![Kimodo official architecture: constraint overwriting followed by a two-stage root and body Transformer denoiser](imgs/nvidia-kimodo-controllable-motion-data-engine/kimodo-two-stage-denoiser.png)

At every denoising step:

1. the `Root Denoiser` reads the complete noisy motion, text, and constraints, then predicts a clean global root trajectory;
2. the system converts that global root into a more stable local velocity representation;
3. the `Body Denoiser` uses the root motion as context to predict body pose and contact;
4. root and body are recombined for the next denoising step.

Both Transformers use 16 layers, eight attention heads, and a hidden size of 1024, for 282 million learnable parameters in total. The design does not finish an entire root diffusion process and run body generation afterward. Root and body predictions are interleaved at every diffusion step so both can keep correcting each other.

This decomposition separates two competing objectives. A global root representation is useful for hitting a path in world space. Body motion is easier to learn from local root velocities that capture gait and contact. In the ablation study, replacing the two-stage model with one stage increased full-body keyframe error from 2.67cm to 8.37cm and end-effector position error from 3.09cm to 10.19cm, while also producing substantially more foot skating.

The smoothed root is not a visual flourish. A real pelvis sways sideways during walking, but an animator's navigation line is usually smooth. Kimodo treats the smooth path as the character's overall travel reference while allowing the pelvis to move naturally around it. Without this separation, a model may adopt a stiff or stealthy gait simply to keep the pelvis glued to a straight line.

## The Curriculum Teaches Two Different Skills

Kimodo does not train every control channel together from the first update.

- The first 500,000 steps are text-to-motion only, teaching the model motion distribution and semantics.
- The next 500,000 steps introduce randomized kinematic constraints, focusing on keyframes, hand and foot targets, root paths, and contacts.
- Sparse constraints gradually increase from one to at most 20 during phase two, and 25% of examples combine two constraint patterns.
- Text is dropped 10% of the time in both phases to enable classifier-free guidance.

The best model was trained at 30 fps with a batch size of 2,048 across 16 NVIDIA A100 SXM4 80GB GPUs. Inference uses 100 DDIM denoising steps by default, with independent guidance weights for text and constraints.

This curriculum explains the product behavior. Kimodo is not a text model with rules bolted onto the side. It first learns what natural motion looks like, then learns how to preserve that prior when parts of the answer have already been specified.

## From Model Output to Animation and Robot Data

The open repository includes more than checkpoints. `kimodo_demo` provides a local 3D editor with a timeline, `kimodo_gen` supports batch generation from the command line, and `kimodo_convert` handles format conversion.

Outputs can travel through several downstream pipelines:

```text
text + timeline constraints
          ↓
Kimodo kinematic motion
          ↓
foot locking / IK / constraint optimization
          ↓
NPZ / BVH / AMASS NPZ / MuJoCo qpos CSV
          ↓
DCC / game engine / retargeting / ProtoMotions / GMR
          ↓
character animation or physics-based humanoid policy
```

SOMA output fits human-character workflows. SMPL-X can be exported in AMASS format. G1 checkpoints can directly produce MuJoCo qpos CSV. ProtoMotions can ingest Kimodo NPZ or CSV files to train physics-based tracking policies, while GMR can retarget SMPL-X motion to other robots.

That is Kimodo's product difference from a generic text-to-motion demo. Its endpoint is not a character that appears to move. Skeletons, formats, constraints, retargeting, and simulation interfaces are part of the deliverable.

The robot examples still do not mean Kimodo directly controls hardware. Kimodo supplies a kinematic reference motion. A physics-based policy trained with systems such as GEAR-SONIC or ProtoMotions must handle balance, contact, torque, joint limits, and real execution. Generated motion is demonstration data, not a safety-validated control command.

## Kimodo Versus ARDY

NVIDIA's later [ARDY release](../2026-07-14/2026-07-14-nvidia-ardy-realtime-interactive-motion-control-en.md) carries forward Kimodo's text and kinematic controls, but the two systems work at different time scales.

| | Kimodo | ARDY |
|---|---|---|
| Primary role | Offline motion authoring and data synthesis | Real-time streaming motion control |
| Generation | Diffusion over a complete sequence | Autoregressive future windows |
| Default inference | 100 DDIM steps | 4 or 10 diffusion steps |
| Input changes | Regenerate an edited clip | Update and replan during playback |
| Best fit | Motion assets, in-betweening, batch demonstrations | Game runtime, interactive characters, online robot planning |

The paper reports that Kimodo takes roughly two to five seconds on an RTX 3090 to generate a clip of up to ten seconds, depending on duration. Its offline behavior is deliberate: full-sequence context and more denoising steps trade latency for quality and precise authoring. ARDY compresses related capabilities into an interactive runtime loop.

The simplest framing is: **Kimodo is a motion asset and data compiler; ARDY is a runtime motion controller.**

## Openness and Local Runtime Cost

The current repository provides checkpoints for SOMA, Unitree G1, and SMPL-X:

- Rigplay models use the complete 700-hour dataset and are the recommended variants;
- BONES-SEED models use 288 hours of public data and are weaker, but support reproducible comparison;
- the code is Apache-2.0;
- most checkpoints use the NVIDIA Open Model License;
- the SMPL-X Rigplay checkpoint uses the more restrictive NVIDIA R&D Model License;
- training data and third-party components have separate terms, so the whole stack cannot be described as one Apache-2.0 release.

Running both the model and text encoder on a GPU requires about 17GB of VRAM, mostly because of the LLM2Vec text encoder. NVIDIA says `TEXT_ENCODER_DEVICE=cpu` reduces VRAM below 3GB with a modest speed penalty. The project has been tested most extensively on RTX 3090, RTX 4090, and A100 GPUs, with Linux receiving the strongest support.

## How to Read the Benchmark

For the paper's Rigplay evaluation, 10% of motion was held out by behavior category so test actions were unseen during training. About 5,000 motions were used to measure text following, motion quality, foot skating, and multiple forms of constraint error.

The large model has 282 million parameters, the medium model 148 million, and the small model 56 million. More parameters, data, and batch size generally improve performance, but in different ways. Model size most clearly helps text alignment and FID. More data most clearly improves constraint accuracy and foot stability. Larger batches provide broader gains.

NVIDIA later released a public BONES-SEED benchmark with test data and the full evaluation pipeline. That matters more than one result table because other models can be measured with the same skeleton, data, and metric implementation.

Version history still matters. On May 3, 2026, the repository fixed how sparse-constraint metrics were averaged. The old implementation divided metrics that applied to only some test cases by the total number of motions, silently scaling displayed values. Text, foot-skate, and TMR metrics were unaffected. Early posts and screenshots should therefore be checked against the current documentation and corrected results.

## Practical Limits

Kimodo is much closer to a production tool than text-only motion generation, but the official documentation lists concrete limits:

- one prompt generates at most ten seconds; longer motion requires sequential prompts;
- except for a dense root path, each constraint type should stay below 20 keyframes;
- very long, complex, or out-of-distribution prompts can fail;
- contradictory text and constraints can create artifacts or be ignored;
- transitions consume part of the following segment in multi-prompt sequences;
- raw output may contain foot skating and may not exactly hit constraints;
- post-processing helps, but currently works poorly for the G1 skeleton.

There is also a more fundamental boundary: Kimodo is kinematic. It does not know the exact geometry of nearby objects, enforce scene collisions, guarantee stable balance, or prove that a robot can execute a motion. A hand target can be placed near an object, but actually grasping that object still requires scene, contact, and physics layers.

A serious evaluation should therefore ask more than whether the official videos look natural:

- How much error appears after retargeting to the production skeleton?
- What share of constraints only succeed after post-processing?
- How much manual cleanup remains for skating, floor penetration, and joint limits?
- Does batch diversity cover the states a downstream policy needs?
- How many generated references remain stable under physics tracking?
- Are the model, data, and product licenses compatible?

## Conclusion

Kimodo matters because it organizes motion generation into a complete data-production pipeline, not because it is one more model that turns text into movement.

Seven hundred hours of optical mocap provide a high-quality motion prior. A unified global representation gives text, paths, keyframes, and joint rotations one control surface. Root-first two-stage Transformers divide world-space travel from natural body motion. Export, retargeting, benchmarks, and simulation interfaces carry the result into animation and robotics systems.

It has not solved scene understanding, physical execution, or continuous long-horizon control. Those layers still require IK, collision handling, physics policies, and real-time systems such as ARDY.

Kimodo nevertheless points to a clear future: **the useful form of AI motion generation is not a clip that creators can only watch. It is infrastructure that makes high-quality mocap searchable by text, programmable with keyframes, and reusable across a production toolchain.**
