---
title: "Machine Skill Source Audit: Not 3D Image Generation, but a Browser Studio for Simulation, Cutaways, and Film"
date: 2026-10-12
source: "https://x.com/konstantinsaifo/status/2109782163591721100"
canonical: "https://github.com/AirsupHQ/machine-skill"
tags:
  - Machine Skill
  - Airsup
  - Claude Code
  - Agent Skill
  - Three.js
  - Physics Simulation
  - Mechanical Engineering
  - WebGL
  - Deterministic Rendering
  - Source Audit
---

# Machine Skill Source Audit: Not 3D Image Generation, but a Browser Studio for Simulation, Cutaways, and Film

> **Bottom line:** [Machine Skill](https://github.com/AirsupHQ/machine-skill) is neither text-to-3D nor a prompt that merely tells Claude Code to draw like an engineer. It is an executable Agent Skill. The agent researches dimensions and operating points, constructs the machine from procedural Three.js geometry, drives speed, thrust, flow, temperature, and failure with a compact physics solver, then turns the same page into an interactive cutaway and a deterministic short film. Its real contribution is not “one sentence in.” It is that **geometry, physics, explanatory UI, and publication video share one runnable source artifact.**

![The Machine Skill turbofan in its default view, captured locally from the official example for this audit](imgs/machine-skill-physics-simulation-film-studio/turbofan-default.webp)

- **Source post:** [Konstantin Saifoulline on X](https://x.com/konstantinsaifo/status/2109782163591721100)
- **Official repository:** [AirsupHQ/machine-skill](https://github.com/AirsupHQ/machine-skill)
- **Live lab:** [Airsup Machine Skill Lab](https://airsup.ai/lab/skill)
- **Pinned audit commit:** [`e0bd066`](https://github.com/AirsupHQ/machine-skill/tree/e0bd066ac5beaf48512935de2fc0f0e55636853a)
- **Source published:** 2026-10-12
- **Audited:** 2026-10-15

## What one sentence actually produces

The source post gives a simple installation command:

```sh
npx skills add AirsupHQ/machine-skill -g -a claude-code
```

The user can then ask Claude Code for a turbofan, mechanical watch, ventricular-assist pump, or hydro turbine. The output is not an image. It consists of two artifacts:

1. a machine-specific HTML page that can orbit, throttle, cut away, explode, x-ray, slow down, label, and fail;
2. a 20–30 second film recorded frame by frame from that page in landscape, square, or portrait format.

The repository currently includes four complete examples: a turbofan, methalox rocket engine, API 610 process pump, and API 617 multistage centrifugal compressor. During this audit, all four deployed HTML pages matched the files at the pinned commit byte for byte by SHA-256. The live gallery is therefore serving inspectable repository artifacts, not a separate opaque backend result.

## More than a Skill: five layers of a small production system

The repository is only about 19MB, but its architecture is clear.

| Layer | Main files | Responsibility |
|---|---|---|
| Agent procedure | `SKILL.md` | Research, modeling, solving, four visual-critique rounds, and delivery criteria |
| Page runtime | `kit/lab-kit.js` | Roughly 1,500 lines of Three.js studio lighting, materials, geometry, cutaways, explode mode, and timeline |
| Physics recipes | `references/solvers.md` | Simplified equations for turbines, rockets, piston engines, watches, pumps, rotors, and motors |
| Machine implementation | `examples/*.html` | Per-machine dimensions, parts, solver, interactions, and failure logic |
| QA and film | `shot.mjs`, `record.mjs`, `pinkscan.mjs` | Review stills, frame-stepped capture, magenta-frame protection, and video output |

Claude is not renaming a fixed 3D model. For every machine, it must author a new “machine program”: proportions, components, materials, state variables, equations, controls, and failure conditions connected to the shared runtime.

## Breakthrough one: geometry is computational input, not decoration

Machine Skill requires dimensions in metres in the machine's coordinate system. Revolved bodies, shells, pipes, gears, springs, bolts, and airfoils come from procedural geometry. Repeated blades, teeth, and fasteners contribute to the stated part count.

The geometry also feeds computation:

- the fan annulus area enters the air-mass-flow calculation;
- blade volume multiplied by titanium density and a hollow fraction estimates blade mass;
- blade mass, centroid radius, and angular speed determine imbalance load;
- rocket throat and exit areas determine area ratio, exit Mach number, and thrust coefficient;
- the cutaway shader uses the back faces of closed solids to render metal section faces and hatching.

That connects “looks like an engine” to “the visible model contributes to the displayed numbers.” It is not CAD, but it is more defensible than typing unrelated constants into a dashboard.

![The turbofan cutaway exposes compressor, combustor, turbines, live labels, and flow streaks](imgs/machine-skill-physics-simulation-film-studio/turbofan-cutaway.webp)

## Breakthrough two: every machine carries a small, transparent solver

The project does not pretend to run CFD or FEA in the browser. It uses zero-dimensional or lumped-parameter models to animate the most important causal relationships.

### Turbofan: a Brayton cycle drives the scene

The turbofan starts from static sea-level ISA conditions. N1 determines inlet Mach, mass flow, bypass ratio, pressure ratios, and turbine inlet temperature. Compressor heating, fuel-air ratio, turbine work balance, and two nozzle velocities ultimately produce thrust. First-order lags model spool acceleration and decay.

Thrust, N1, turbine gas temperature, and fuel flow all come from that solver. When the user throws a fan blade, geometry estimates its mass and `F = mω²r` produces the imbalance load that drives visible vibration and spool-down.

### Rocket: nozzle equations produce thrust; a thermal model produces burn-through

The rocket example combines a methalox chamber approximation, characteristic velocity, choked throat flow, isentropic area ratio, and thrust coefficient. Chamber pressure is the control; thrust, specific impulse, mass flow, exit Mach, and pump power update live.

“Cut the regen cooling” is not merely a red animation. Heat flux and the thermal mass of the copper liner raise wall temperature over time. At 1,356K, burn-through and shutdown are triggered. The model is coarse, but the causal chain is inspectable in source.

![The rocket cutaway joins geometry, flow, chamber-pressure control, and thrust in one page](imgs/machine-skill-physics-simulation-film-studio/rocket-cutaway.webp)

## Breakthrough three: one state serves both interactive teaching and film

Interactive 3D demos often split into two projects: a web application and a second Blender, After Effects, or Remotion timeline for publication. Machine Skill instead gives the page a deterministic film clock.

In `?film=1` mode, simulation time advances only when the recorder calls `step(1/fps)`. `record.mjs` waits for each WebGL frame and pipes PNGs to FFmpeg. The default 28-second narrative is fixed:

1. type the one-line machine request;
2. assemble parts in order;
3. move a control and run the solver;
4. cut the machine open with live labels;
5. explode the assembly;
6. trigger a solver-driven failure.

This is not a conventional video editor. It is a **director mode for an interactive simulation**. One state machine controls values, part motion, camera events, and failure consequences. When the page changes, the film can be regenerated without manually resynchronizing captions.

The repository also handles a peculiar production failure: under GPU pressure, headless Chromium can return a solid magenta frame. A screenshot guard retries bad frames, while `pinkscan.mjs` downsamples the finished film and searches for high pink coverage or a sudden magenta flash. That small feature is strong evidence that the authors have used the pipeline for real output rather than merely documenting a recording command.

## The process pump shows a path beyond social-media demos

Version 1.1.0 added refinery training examples. The API 610 pump page does more than render a polished blue pump. It keeps the pump curve, system curve, BEP, available versus required NPSH, seal leakage, vibration, and an operator-rounds checklist in the same state. Changing VFD speed and discharge-valve opening moves the operating point. Dropping tower level drives the simplified model into cavitation.

![The API 610 example places the 3D asset, operating curves, and operator-rounds data in one view](imgs/machine-skill-physics-simulation-film-studio/process-pump.webp)

This suggests a more durable use than a striking feed video: equipment training, maintenance explanation, design review, and sales engineering. It is not a high-fidelity digital twin, but it can turn a static manual into a browser explainer that users operate, open, and deliberately fail.

## Relationship to Anatomy: shared inspiration, different objectives

The repository explicitly credits [Anatomy](https://github.com/wheresryan22/anatomy) and says its numbered-beat film inspired this project. Both combine an Agent Skill, procedural geometry, browser rendering, and visual review, but their centers of gravity differ.

| | Anatomy | Machine Skill |
|---|---|---|
| Primary subject | Invent a physical machine to explain an abstract concept | Reconstruct an existing real-world machine and operating point |
| Primary output | SVG/WebGL/experimental 3D technical visual | Three.js interactive simulation plus automated film |
| Core constraints | Semantic metaphor, geometry ledger, collision/terminal/depth audits | Real dimensions, procedural solids, compact physics solver, product-photography look |
| Strongest verification | Richer automated geometry and browser-interaction audits | Review captures, performance counters, deterministic capture, and magenta-frame scanning |
| Current weakness | Complex work is slow; 3D remains beta | No equivalent automated geometry suite or cross-machine numerical regression |

Anatomy asks how structure itself can explain a concept. Machine Skill asks how one real machine's structure, values, and camera language can share a runtime. It is not a replacement for Anatomy; it specializes the pattern for mechanical engineering and publication-ready film.

## What this audit reproduced

I checked out the pinned commit on an Apple Silicon Mac, installed the declared Playwright dependency, and ran the official examples through the project's own `shot.mjs` and `record.mjs`.

| Check | Result | Evidence boundary |
|---|---|---|
| Turbofan default and cutaway captures | 3,597 parts, 644,188 triangles, 21 materials, about 61fps | One run of the project script on this Mac, not a cross-device benchmark |
| Rocket cutaway | 57 parts, 118,920 triangles, 26 materials, about 61fps | Confirms the official example loaded and changed interaction state |
| Process pump | 281 parts, 377,094 triangles, 39 materials, about 61fps | No independent calibration against a physical API 610 pump |
| Live-gallery parity | All four deployed HTML pages matched the pinned repository examples by SHA-256 | Establishes deployment parity at audit time |
| Deterministic recording | Produced a 960×540, 15fps, two-second H.264 file; full decode passed | Short pipeline probe, not an acceptance test of the complete 28-second film |
| Pink scan | `pinkscan clean` | Covers only the two-second output |

## Three boundaries that “real” must not conceal

### 1. Real equations do not mean engineering certification

The README is explicit: these are small honest models, not CFD or FEA. Numbers are sanity-checked against public operating points rather than certified. A zero-dimensional turbofan cycle cannot resolve blade-level flow. A lumped rocket thermal model cannot replace coolant-channel analysis or structural thermal stress.

The system is useful for explaining why a changed input produces a changed result. It must not be used to design equipment that flies, contains pressure, or enters a human body.

### 2. One HTML file is not fully offline

The project's own `lab-kit.js` is inlined, but pages still import Three.js 0.170 and addons from jsDelivr, fonts from Google, and optionally an HDR environment from Poly Haven. The output is a single-file deliverable with no build step, not a fully vendored offline artifact. Long-term archives and restricted networks would need to localize those dependencies.

### 3. QA is a production procedure, not yet a test system

The Skill requires four rounds of screenshot criticism. `shot.mjs` reports frame rate, part count, and triangles, and the recorder has practical guards. The repository has no GitHub Actions workflow or automated test command, however. `evals/evals.json` currently contains five prompts and prose descriptions of expected output; it does not execute geometric, equation, or numerical checks.

At audit time, the upstream repository also had an open issue about zero-length normals producing NaNs and bloom-amplified black rectangles, plus open pull requests for Windows ANGLE, resize offsets, and OpenCode support. These do not invalidate the bundled examples, but they place the project at an early engineering stage.

## The broader product lesson

Machine Skill collapses a workflow that is usually fragmented into one executable explanation:

- research notes become source comments and a visible “How it is computed” panel;
- geometry supplies appearance as well as area, volume, and centroid;
- the solver drives numbers, color, motion, and failure;
- interaction state becomes camera events;
- publication video deterministically replays the page instead of duplicating its timeline.

That pattern is valuable for educational visualization, industrial sales, equipment training, and technical media. It does not eliminate modeling work. It reduces the cost of **rebuilding the same knowledge separately as a CAD-like illustration, web interaction, explanatory copy, and short video.**

## Conclusion

Machine Skill's strongest property is not that Claude can make something engine-shaped from one sentence. The real product is a strict output contract: a machine needs realistic proportion, recognizable parts, material separation, a compact solver for its hero metric, a computed failure, and a visual narrative that can be recorded repeatedly.

Compared with a generic Three.js prompt, it adds a shared runtime, mechanical geometry, solver recipes, critique rounds, and a film pipeline. Compared with professional CAD and CAE, it remains deliberately light and does not claim manufacturing accuracy.

**The best description is a browser machine-demonstration studio for coding agents: build the machine as a runnable explanation, then film that explanation directly.**

## Primary sources

- [Source post - X](https://x.com/konstantinsaifo/status/2109782163591721100)
- [AirsupHQ/machine-skill](https://github.com/AirsupHQ/machine-skill)
- [Pinned audit commit `e0bd066`](https://github.com/AirsupHQ/machine-skill/tree/e0bd066ac5beaf48512935de2fc0f0e55636853a)
- [Machine Skill Agent instructions](https://github.com/AirsupHQ/machine-skill/blob/e0bd066ac5beaf48512935de2fc0f0e55636853a/SKILL.md)
- [Shared Three.js runtime](https://github.com/AirsupHQ/machine-skill/blob/e0bd066ac5beaf48512935de2fc0f0e55636853a/kit/lab-kit.js)
- [Solver recipes](https://github.com/AirsupHQ/machine-skill/blob/e0bd066ac5beaf48512935de2fc0f0e55636853a/references/solvers.md)
- [Deterministic recorder](https://github.com/AirsupHQ/machine-skill/blob/e0bd066ac5beaf48512935de2fc0f0e55636853a/scripts/record.mjs)
- [Live Machine Skill Lab](https://airsup.ai/lab/skill)
- [Open rendering issue #4](https://github.com/AirsupHQ/machine-skill/issues/4)
- [Anatomy](https://github.com/wheresryan22/anatomy)

*This audit is pinned to commit `e0bd066ac5beaf48512935de2fc0f0e55636853a`. All four images were captured locally from the official examples at that commit; they are not generated marketing stills. Frame-rate and scene statistics describe this Mac and this run only. The physical models were not independently calibrated and must not be used for safety-critical engineering or certification.*
