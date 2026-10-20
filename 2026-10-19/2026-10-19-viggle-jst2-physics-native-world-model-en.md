---
title: "Inside Viggle JST-2: One 3D Token System for Scenes, Characters, and Motion"
date: 2026-10-19
source: "https://x.com/ViggleAI/status/2112202244779061382"
canonical: "https://viggle.ai/jst2"
tags:
  - Viggle
  - JST-2
  - World Model
  - Physics-Native Token
  - 3D Gaussian Splatting
  - Character Animation
  - Motion Capture
  - PINOC
  - MCP
  - Physical AI
---

# Inside Viggle JST-2: One 3D Token System for Scenes, Characters, and Motion

> **TL;DR:** Viggle released JST-2 on October 19, 2026 and calls it a physics-native world foundation model. Its most important feature is not a single generated video, but a shared representation: scenes, characters, and motion become `Physics-Native Tokens` with explicit XYZ coordinates plus learned attribute and dynamics vectors. A decoder can turn that state into images or 3D Gaussian splats, allowing a camera to move through an existing world without regenerating a video and allowing characters to carry animation behavior into PINOC, API, and MCP workflows. “Physics-native” does not mean complete learned physics, however. Character motion uses learned dynamics, while scene collisions and object interactions still depend on rule-based physics. The speed and benchmark results are also vendor-reported and have not been independently reproduced.

![Viggle JST-2 launch](imgs/viggle-jst2-physics-native-world-model/jst2-launch.jpg)

- **Source post:** [ViggleAI on Physics-Native Tokens](https://x.com/ViggleAI/status/2112202244779061382)
- **Official launch:** [Introducing Viggle JST-2](https://viggle.ai/jst2)
- **Released:** October 19, 2026
- **Available through:** PINOC in the browser, API, and MCP
- **Model status:** Hosted service; the launch does not provide JST-2 weights or training code

## One-sentence verdict

**JST-2 is trying to give agents a persistent 3D world state they can revisit, animate, and extend, rather than merely a better-looking video.**

Conventional video models usually compress a world into pixels or a spatiotemporal latent. They can produce convincing frames, but structure such as where a chair exists, how an occluded hand continues moving, or whether a room remains stable after the camera turns must be inferred indirectly from appearance.

JST-2 takes a different route. It first represents persistent parts of a world, then applies a viewpoint, motion, or force, and finally decodes an image or 3D output. Viggle calls those parts atoms. They are not chemical atoms; they are learned tokens standing for pieces of matter or object parts.

That makes JST-2 look less like a video renderer and more like a **generative scene runtime**.

## What the architecture image actually says

![JST-2 Physics-Native Token architecture](imgs/viggle-jst2-physics-native-world-model/physics-native-token-architecture.png)

The source post contains only two short paragraphs. The architecture diagram carries most of the argument:

```text
real images → JST encoder ┐
                          ├→ Physics-Native Tokens
multimodal prompt → generator ┘

Physics-Native Tokens
  + viewpoint
  + motion / force
        ↓
    JST decoder
        ↓
image or 3D Gaussian splats
```

Each token contains at least three kinds of information:

| Component | Role |
|---|---|
| Explicit `xyz` | Locates an object part in 3D space |
| Attribute vector | Encodes appearance, material, and other learned properties |
| Dynamics vector | Encodes how that part moves or deforms under action |

The encoder infers tokens from one or more real views. The generator can produce the same token type from a multimodal prompt. The decoder then combines world state with a chosen viewpoint and motion or force conditions to produce an image or splats.

The key is not simply that the system is “3D.” It is that **the same state can be read repeatedly**. Once a scene exists, moving the camera rerenders its splats locally in the browser. The model is called again when new content must be generated. That is materially different from drawing another video every time the camera changes.

## Why Gaussian splats fit this design

![Worlds generated with JST-2](imgs/viggle-jst2-physics-native-world-model/jst2-generated-worlds.webp)

3D Gaussian Splatting represents a scene with many oriented Gaussian primitives carrying position, color, opacity, and scale. It renders quickly, works well for free-viewpoint browser experiences, and preserves image-derived appearance without requiring a clean polygon mesh.

That complements the JST-2 design:

- tokens hold persistent spatial state;
- the decoder turns that state into viewable splats;
- the browser can render them without querying the model for every frame;
- additional views can extend the world while retaining spatial context.

Viggle says JST-2 accepts up to 64 input views as a spatial context window. Instead of producing one isolated panorama, the model can expand a world one view at a time and condition later additions on what already exists.

Splats also explain several limits. They are not clean topology. Close surfaces, holes or merging around joints, occlusion boundaries, and precise collisions remain difficult. They are useful for previs, interactive experiences, and game prototypes. They do not automatically replace a final mesh pipeline that needs editable topology, UVs, collision bodies, and production-ready materials.

## How to read the “one-second 3D scene” claim

Viggle reports that JST-2's feed-forward architecture produces a 3D scene in roughly one second at under $0.01 of inference cost, compared with roughly five to six minutes for Marble.

Three conditions matter:

1. the one-second figure measures model inference on an **NVIDIA B200**;
2. it explicitly excludes network latency, queues, loading, and browser rendering;
3. the launch page does not publish a reproducible harness proving that output quality, resolution, inputs, and expansion scope are normalized against Marble.

The supported conclusion is that feed-forward scene generation can become interactive. It does not mean every laptop creates a finished high-quality world in one second, nor does it establish an independently verified speed championship.

The workflow implication is more interesting than the headline. If a new view takes seconds to infer while existing splats remain locally explorable, an agent can loop through generate, inspect, choose a direction, and extend instead of waiting for a long video render before making the next decision.

## Characters are generated with motion information

JST-2 also places character appearance and motion dynamics in the same representation. Viggle says the model can create a complete full-body character from text or one image, including cropped, occluded, or upper-body-only inputs.

Dynamics vectors encode how parts deform under motion. JST-native characters can therefore receive generated motion without a separate manual rigging and skinning pass. This does not make skeleton concepts disappear; it means the model absorbs work that traditionally happened as a specialist binding stage.

Two deliverables should remain distinct:

- a **JST-2 character** is an animatable Gaussian splat character. Public MCP documentation uses `.vsplat`, rendered through the Viggle Splat Engine on the web or in Unity;
- a **JST-2 motion** can be delivered as GLB, FBX, or USDZ and can drive standard 3D rigs, making it easier to bring into Blender, Unity, Unreal, and other established pipelines.

“One image to an animatable character” is valuable, but it is not the same as “one image to a universally editable, production-quality mesh.” Character appearance and motion data have different interoperability boundaries.

## Text and video both become full-body 3D motion

JST-2 accepts two classes of motion input:

- text-to-motion for dodges, rolls, kicks, dances, door opening, and other actions;
- video-to-motion that reconstructs a visible performance in 3D and infers movement for occluded body parts.

The result can be applied directly to JST-2 characters without a separate retargeting step, while remaining compatible with standard rigs. This moves beyond character replacement in a finished video. The output can be reassigned to another character, reframed, edited, and imported into a game engine.

That is the deeper transition from Viggle Meme Maker to PINOC. The former answers “put this character into that clip.” The latter begins to supply character and motion assets for games, animation, and previs.

## The benchmarks are promising, but vendor-run

Viggle published blind comparisons for character generation, animation readiness, and motion. Its methodology says competing systems received the same inputs and assets were generated in batches through each vendor's API. `Average Score` equally weights the criteria and Overall Preference, draws count as half a win, and 50% means parity.

| Task | Baseline | JST-2 Average Score |
|---|---|---:|
| Image-to-character | Meshy 7.1 | 58.4% |
| Image-to-character | Tripo H3.1 | 73.2% |
| Animation readiness | Meshy 7.1 | 73.8% |
| Animation readiness | Tripo H3.1 | 88.9% |
| Text-to-motion | Cartwheel Swing | 74.8% |
| Text-to-motion | HY-Motion-1.0 | 80.0% |
| Video-to-motion | Cartwheel Comic 4 | 58.1% |
| Video-to-motion | DeepMotion Animate 3D | 89.1% |

This is more systematic than a hand-picked launch reel. It also separates facial detail, joint alignment, hand articulation, deformation, foot contact, and motion smoothness.

The evaluation still comes from the model vendor. The public pages do not provide JST-2 weights, a complete test set, per-sample outputs, evaluator counts, or a runnable benchmark harness. The careful wording is therefore “Viggle's blind tests report a lead over these baselines,” not “JST-2 is proven to be the best 3D model.” Results near the parity line, particularly character generation against Meshy and video motion against Cartwheel, deserve practical testing rather than headline treatment.

## MCP turns a web feature into an agent tool

The launch explicitly supports Codex, Claude Code, and other MCP clients. The public PINOC MCP can let an agent:

- browse and retrieve preset motions;
- generate motion from text;
- recover 3D motion from video;
- generate a character from photos or a description;
- wait for asynchronous jobs and download assets;
- check credits and separate read-only from credit-spending permissions.

This is stronger than asking an agent to click through a website. Generation, waiting, and asset retrieval become named tool calls. An agent connected to PINOC plus Blender, Unity, or Unreal tooling could create a motion, retrieve the GLB or FBX, and place it into a project in one workflow.

There is an important scope boundary. The current public PINOC MCP page enumerates character and motion tools; it does not expose every Scene-generation and world-expansion capability shown on the JST-2 launch page as a named MCP tool. “Available via API or MCP” should not be expanded into a claim that the entire world editor is already agent-accessible.

## The easiest way to misread “physics-native”

Physics-Native Tokens make position and dynamics explicit in the representation. They do not turn JST-2 into a general physics simulator.

Viggle documents several current limits:

- Gaussian holes, merging, or collapse can appear at shoulders, armpits, and between fingers;
- hair, clothing, and materials soften at close range;
- unusual human proportions and non-humanoid silhouettes can cause bad joint placement;
- clothing, hair, and accessories deform with the body but do not yet simulate inertia or mutual collision;
- scene collisions and object interactions still use rule-based physics.

Replacing those rules with learned interaction dynamics is a JST-3 goal. That roadmap also defines JST-2 precisely: it has learned part of how characters move, not the full physics of how arbitrary objects affect one another.

## Where it can matter now

JST-2 is most plausible today in four workflows:

1. **Game prototypes and NPC blocking:** create characters, motion, and explorable locations before final asset production;
2. **Film previs:** block movement, fights, and camera ideas from phone footage or text without waiting for finished characters;
3. **Interactive content:** reuse one spatial state across viewpoints and additions instead of baking a fixed clip;
4. **Agent asset production:** expose motion and characters as queryable, generatable, downloadable tools instead of manually transferred web outputs.

Robot simulation, autonomous driving, construction, and a broader “experience engine for physical AI” remain longer-term directions. The launch demonstrates reconstruction from sparse observations, but it does not publish robot-policy training, physics-accuracy, or sim-to-real results. Visual spatial consistency alone is not evidence of a reliable simulator.

## How a team should evaluate it

A production trial should use fixed inputs and inspect the full handoff:

| Stage | Acceptance questions |
|---|---|
| Scene | Do novel views stay structurally consistent? Does expansion alter old regions? Do splats break at close range? |
| Character | Are occluded parts plausible? Do hands, faces, unusual bodies, and joints survive motion? |
| Motion | Are rhythm, foot contact, fingers, rapid rotations, and occluded movement preserved? |
| Pipeline | Do GLB, FBX, and USDZ import with correct axes, bones, loops, and retargeting? |
| Agent | Are permissions, credit confirmation, timeouts, refunds, expired links, and task recovery explicit? |
| Rights | Are the person, source performance, IP character, training material, and output cleared for the intended use? |

Latency should also be separated into inference, service queue, upload, polling, download, DCC import, and manual repair. That is how the launch's one-second model number becomes a team's actual delivery time.

## Conclusion

Viggle's X post appears to introduce one token representation. It actually reveals a larger product trajectory: from pixel-level character replacement toward persistent 3D state, then from that state into browsers, game engines, and agents.

The significance of JST-2 is not the phrase “physics-native.” It is the decision to keep spatial position, appearance attributes, and motion dynamics in one generative representation. The output no longer has to end as a video; it can remain a state that is observed, combined, and driven again.

JST-2 is still not a complete learned-physics world simulator or an open-weight research release. Most evidence comes from Viggle's launch pages and internal blind tests, while Gaussian characters, close detail, difficult deformation, scene collision, and tool availability have practical boundaries.

The most accurate description is: **JST-2 has moved from generating pictures of worlds toward generating world state that can keep working. Turning that state into a trustworthy physical world still requires JST-3 and independent evaluation.**

## References

- [ViggleAI X post: Physics-Native Tokens](https://x.com/ViggleAI/status/2112202244779061382)
- [Introducing Viggle JST-2](https://viggle.ai/jst2)
- [JST-2 Character benchmark](https://viggle.ai/research/jst2-character)
- [JST-2 Motion benchmark](https://viggle.ai/research/jst2-motion)
- [PINOC MCP Server](https://viggle.ai/pinoc/mcp)
- [PINOC product overview](https://viggle.ai/pinoc)
- [Viggle Research index](https://viggle.ai/research)

*This article is based on Viggle's October 19, 2026 X post and JST-2 launch, character, motion, PINOC, and MCP pages available on October 20. Images come from Viggle's official X account and website. Speed, cost, user, and benchmark figures are vendor-reported. I did not receive JST-2 weights, training data, or an independent benchmark harness, and I did not run a paid generation, so these figures are not presented as third-party reproductions.*
