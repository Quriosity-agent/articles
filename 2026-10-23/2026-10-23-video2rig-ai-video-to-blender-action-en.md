---
title: "video2rig: Fitting AI Video Back onto Your Own Blender Rig"
date: 2026-10-23
source: "https://github.com/donghaozhang/video2rig"
tags:
  - video2rig
  - Blender
  - Character Animation
  - Motion Reconstruction
  - Image-to-Video
  - DINOv2
  - Synthetic Data
  - UniRig
---

# video2rig: Fitting AI Video Back onto Your Own Blender Rig

AI video can make a character lift an arm, run, or stagger, but the resulting pixels do not contain skeletal curves for a game engine. video2rig attempts to bridge that gap: render a first frame from an existing 3D character, animate it with image-to-video, then fit the depicted motion back onto that character's skeleton.

**The deliverable is an editable Blender Action, not a new character model or a general service that recovers arbitrary rigs from internet videos.** A known asset, starting pose, and camera setup are essential inputs.

![Upstream video and fitted original rig comparison](imgs/video2rig-ai-video-to-blender-action/fit-over-video.jpg)

*Author-provided example: video on the left, the fitted original character on the right. This is not motion reconstructed during this review.*

This review inspected the October 23, 2026 first public commit [`55d51b3`](https://github.com/donghaozhang/video2rig/tree/55d51b3b9685125a8ea27841d6af9523f6352aa1) on October 26. The supplied `donghaozhang/video2rig` is a fork of [`canitcode/video2rig`](https://github.com/canitcode/video2rig); both main branches pointed to the same revision when checked. The project is attributed to Can It Code, not newly authored by the fork owner.

## Connecting an Existing Asset to a Video Model

The pipeline has six main steps:

```text
Existing 3D asset and skinned armature
    → Export rig, mesh, and starting pose
    → Render a first frame with fixed cameras
    → Train a character-specific joint reader, reusable across moves
    → Generate a motion clip with image-to-video
    → Read joints, fit the rig, and import a Blender Action
```

For an unrigged asset, the project provides an auto-rigging route through separately installed UniRig, with a mesh-centerline fallback. This does not replace asset creation: geometry, textures, skeleton, and skinning still need usable quality. [Tutorial](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/TUTORIAL.md)

![Upstream auto-rig pose checks](imgs/video2rig-ai-video-to-blender-action/autorig-poses.jpg)

*Author-provided pose sheet. Inspect deformation and misplaced skin weights; it does not establish universally correct automatic rigging.*

This makes the tool relevant to an existing-character workflow. A concept image alone, or an unrelated film clip, lacks the required foundation.

## Why Two Views of the Same First Frame Matter

The default first frame combines front and side views and retains camera parameters. Their observations constrain a joint's position in space. With one view, depth depends more heavily on the starting pose and skeleton priors.

![Front and side views in the upstream start frame](imgs/video2rig-ai-video-to-blender-action/start-picture.jpg)

*Author-provided start image: plain background, visible floor, full body, and motion clearance. It is designed for measurement rather than final-film presentation.*

The generated clip should preserve that first frame, maintain fixed cameras, avoid cuts, retain the full body, and minimize effects and strong blur. Crucially, both panels must depict the same motion at the same time. Having two views does not guarantee the generator maintains multi-view consistency. [Video requirements](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/docs/VIDEO.md)

![Upstream generated-video frame sequence](imgs/video2rig-ai-video-to-blender-action/video-frames.jpg)

*The author's frame sheet illustrates correspondence throughout the motion. No complete clip was played or reproduced for this review.*

The authors tested Seedance clips. Other first-frame video generators are proposed as compatible in principle, not individually validated integrations.

## Synthetic Labels for One Character's Joint Reader

Rather than imposing one fixed human pose template, video2rig randomly poses the asset's own rig, renders it through the known cameras, and obtains joint projections from the known geometry. The reader learns that character under those cameras, not a specific animation.

The network combines DINOv2-small with a joint-heatmap decoder and a fine-detail branch. Its embeddings and first four Transformer blocks are frozen; later blocks remain trainable. It is not merely a prompt over an entirely frozen vision model. Training also handles visibility and appearance/blur augmentation. [Network implementation](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/reader/net.py), [method description](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/docs/HOW-IT-WORKS.md)

![Upstream joint-reader visualization](imgs/video2rig-ai-video-to-blender-action/reader-joints.jpg)

*Author-provided predictions. Heatmap peaks supply confidence, but confidence does not guarantee correct interpretation of generated footage.*

The reuse boundary matters: changing the character, rig, or starting views requires preparing an appropriate reader again. “Train once, use for multiple moves” is conditional on the asset and camera setup.

## Two-Dimensional Observations Still Need Constrained Fitting

Detected points are not a stable 3D animation by themselves. The main route handles left/right ambiguities, confidence weights, joint ranges, smoothing, and ground constraints. It also supplies foot locking, step-derived root travel, and some limb-through-body suppression.

These are engineering corrections, not a complete physics simulation. For example, `steps` can turn an in-place run with backward-sliding feet into forward root travel. The reconstructed character may consequently advance while the source video stays centered; overlay drift is not automatically a fitting fault. [Fitting code](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/reader/fit.py)

There is also an important fallback: `run` uses the joint reader when `reader/reader.pt` exists. Without it, or with `--old`, it takes the BootsTAPIR point-tracking and older solving route. Getting an output after skipping training does not establish that the same method ran. [Command routing](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/__main__.py)

The authors report approximately three degrees of median per-bone direction error on known-motion renders across nine characters, versus approximately twenty-one degrees on one older-route running example. Those are author-reported synthetic measurements, not independent accuracy results on AI video. The public tree did not include the referenced `dev/bench/suite.py` or complete benchmark assets; the figures were not reproduced here.

## Outputs and Acceptance Checks Are Different Things

The solver exports `.npz` data containing times, bone rotations, root translation, and prop transforms. `blender/import_motion.py` writes an Action, maps content times to scene frames, and uses quaternion rotations with linear keys. Blender can then edit the animation and export through its FBX or glTF workflow. The `.npz` is not already a delivered engine asset. [Importer](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/blender/import_motion.py)

Two review commands are worth preserving:

| Command | Purpose and boundary |
|---|---|
| `python -m video2rig check <project> <clip>` | Assess two-orthographic-view agreement and other indicators; unsupported cameras receive a warning, not a correctness certificate |
| `python -m video2rig review <project> <clip>` | Produce video/fit comparisons and an additional view to expose depth and contact problems |

`check` returns FAIL with a nonzero exit when median body disagreement exceeds approximately 1.5% of character height. This is a heuristic in the inspected code, and a separately invoked command: `run` does not automatically perform all input acceptance checks. [Check implementation](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/check.py)

A convincing input-camera match can conceal incorrect depth. The authors disclose a single-view stone-lifting example that matches through the original camera but places the stone near the hip from the side. Fully occluded limbs, detailed fingers, and weapon-axis twist are additional limitations, not solved merely by having a rig.

## Hardware and the Meaning of Local

Documentation targets Windows/Linux, Python 3.10–3.12, Blender 5.1, and NVIDIA RTX 30-series or newer hardware, with reported tests on 12 GB cards. Approximately forty minutes for reader preparation/training and around a minute for a clip are upstream observations, not timings measured here. [Requirements](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/README.md)

The training entry selects CUDA explicitly. Reading an existing reader can use CPU, but the inspected route does not automatically select Apple MPS. Running the Blender importer on a Mac does not validate the default reader-training pipeline there.

Reading and fitting can run locally, while image-to-video generally remains an external step. The repository also includes an optional paid BytePlus generation helper with credentials, a budget ledger, and saved task IDs for recovery. Account-free local processing is not an entirely offline, free workflow. [Generation helper](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/generate.py)

## What This Review Actually Executed

Using **Blender 5.1.2**, this review created three simple bones and a cube prop in a temporary empty scene, then supplied three synthetic motion samples to the upstream importer. Checks passed for:

- Mapping 0, 0.5, and 1 second to frames 1, 13, and 25 at 24 fps and creating an Action.
- Root/prop translation, quaternion hemisphere correction, and linear interpolation.
- Preserving an unfitted bone's initial rotation and restoring the editing preference.
- Saving a `.blend` and reopening it in another process to verify the Action and final root/prop positions.

This validates **synthetic motion import and persistence only**, not skin deformation, training, video perception, real fitting, FBX/glTF export, or animation quality. No inference dependencies or model weights were installed, no private character was imported, and no generation service was called. [Verification script and record](imgs/video2rig-ai-video-to-blender-action/SOURCES.md)

Project code is AGPL-3.0; DINOv2, BootsTAPIR, and separately installed UniRig retain their respective licenses. The authors permit commercial animation use, but asset rights, generation-service terms, and software redistribution conditions remain separate questions. [License](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/LICENSE)

video2rig's useful idea is **using the asset to create its own labels, asking a video model for a motion proposal, then recovering editable skeletal animation**. Treat it as an animation-draft workflow: validate one short move for view consistency, contact, and skinning before scaling up. A comparison image alone is not engine-ready delivery.
