# Inside Shaders 4.0: Not an Effects Pack, but a Cross-Framework WebGPU Component Compiler

> **Bottom line:** The center of Shaders 4.0 is not “200 impressive shaders.” It is a serializable visual component tree. The same tree can be designed in a visual editor, rendered from React, Vue, Svelte, Solid, or vanilla JavaScript, then compiled into a minimized plan of WebGPU fragment, compute, and offscreen-texture passes. The runtime is WebGPU-only, however, and the cloud editor and Pro preset library are not part of the MIT package.

![The Shaders visual design editor](imgs/shaders-webgpu-component-compiler/design-editor.jpg)

The obvious description of [shader-effects-inc/shaders](https://github.com/shader-effects-inc/shaders) is “a web-effects component library.” Install an npm package, then stack Aurora, Glass, Glow, CursorTrail, or ReactionDiffusion as if they were ordinary framework components.

That description is correct but misses the important part. A conventional shader collection ships a GLSL/WGSL fragment, a few uniforms, and a demo. Shaders ships a common model spanning design, code, framework components, and GPU execution. An effect becomes a typed tree carrying parameters, layer relationships, masks, blending, animation drivers, and layout semantics rather than an isolated pixel function.

As of October 8, 2026, the latest release is [`v4.0.2`](https://github.com/shader-effects-inc/shaders/releases/tag/v4.0.2), at commit [`9435282`](https://github.com/shader-effects-inc/shaders/commit/9435282c29d3505c67eef427470c8d835095a199). This audit pins that snapshot instead of folding future site features or Pro content into the open runtime.

---

## 01 | Draw the Boundary First: The Engine Is Open, Not All of shaders.com

The repository's [MIT license](https://github.com/shader-effects-inc/shaders/blob/9435282c29d3505c67eef427470c8d835095a199/LICENSE) covers the WebGPU engine, built-in components, and bindings for React, Vue, Svelte, Solid, and JavaScript. The published `shaders@4.0.2` package contains that public implementation.

Several surrounding capabilities remain a separate platform or commercial layer:

- the shaders.com visual editor, accounts, and project storage;
- the advertised 1,000+ production presets and 55+ website sections;
- Pro preset installation, unlimited history, and one-click Framer installation;
- unwatermarked HD image and video export;
- the hosted MCP service at `shaders.com/mcp` and its account-backed capabilities.

The CLI bridges those layers. It detects a framework, writes `shaders.config.ts`, signs in through a browser, connects an online project, installs designs as ordinary component files, and records them in `shaders.lock.json`. Base components can be authored and rendered locally; preset search, project synchronization, and Pro installation call shaders.com APIs.

The changelog also says that `v3.2.475` was the last closed-source release. The public repository begins on September 29 and contains only 14 commits at the inspected snapshot. This is a mature codebase entering public history, not a system written from scratch in two weeks. Public commit count is not development age.

---

## 02 | The 199 Components Are the Surface; the Unified Definition Is the Product

![The Aurora generator component](imgs/shaders-webgpu-component-compiler/aurora.jpg)

The pinned source has **199 component directories** under `packages/core/src/shaders/`, grouped into textures, shapes, shape effects, blurs, distortions, adjustments, stylization, interactive effects, transitions, and utilities. A component is more than a WGSL string. It includes:

- a name, role, and input contract;
- typed props, defaults, and editor-control metadata;
- whether a value is a runtime uniform or a compile-time structural choice;
- pointer, time, child-layer, mask, and render-to-texture requirements;
- fragment, compute, host lifecycle, and cleanup behavior;
- cover media, documentation, and framework-codegen information.

Aurora is a generator that produces pixels independently. Glass is a shape effect that consumes prior content. ReactionDiffusion is a simulation with persistent frame-to-frame state. Blur may turn its input into a texture before processing it.

React, Vue, Svelte, Solid, and vanilla JS are not five manually maintained engines. Scripts generate framework components and export maps from the core definitions, keeping effect names, props, and defaults aligned. Framework packages mainly translate reactive state and DOM lifecycle into the same renderer.

That is the practical advantage over copying shader code: designers and engineers exchange the same executable visual tree rather than screenshots and implementation guesses.

---

## 03 | From Component Tree to GPU: Lower to an IR, Then Schedule Passes

One `<Shader>` owns one canvas. Its children enter a registry in layer order, and the composer lowers the tree into a `CompositionIR` with four important groups:

1. **compute steps** for particles, fluids, reaction-diffusion, and blur preprocessing;
2. **RTT passes** for subtrees that must render into a texture before another effect samples them;
3. a **final fragment pass** that writes tone-mapped output to the canvas;
4. resources and lifecycle for uniforms, textures, video, resize, frame hooks, and cleanup.

Execution is not “draw 199 components from top to bottom.” The renderer schedules compute updates, prepares render-to-texture results from leaves toward the root, then executes the final fullscreen output.

The composer also tries to remove RTT boundaries. UV effects such as Bulge or Twirl can sometimes push their coordinate transform down into a generator, asking the source to evaluate directly at the remapped coordinate. That saves a texture write and resample and avoids magnification being limited by an intermediate texture. Blur, feedback, complex masks, opacity boundaries, and true neighborhood sampling still force an offscreen pass.

Composition is therefore a small graphics compilation process, not a stack of independent canvases.

---

## 04 | Runtime and Structural Props Must Be Different

Most colors, positions, strengths, and time values live in uniform buffers. Updating them changes GPU data for the next frame without recompiling a pipeline.

Some choices alter the emitted WGSL: color-space branches, sampling modes, loop sizes, or whether an effect needs a compute pass. Those props are marked compile-time and enter a structural hash. A structural change builds a new composition; ordinary value changes reuse the existing pipeline.

That separation is what makes a visual editor feel responsive. The pipeline cache, structural hashing, and swap-when-ready logic prevent every slider movement from becoming a visible shader-compilation pause.

Custom components use the same machinery. `defineShader` accepts a stable raw WGSL body or the still-experimental std primitives. Custom props receive transformations, uniform bindings, framework wrappers, and editor metadata rather than escaping the runtime's type system.

---

## 05 | Sharing One GPUDevice Matters More Than Saving a Few Shader Instructions

![Glass combines child content, a shape field, offscreen textures, and compute blur](imgs/shaders-webgpu-component-compiler/glass.jpg)

By default, every `<Shader>` on a page shares one lazily created `GPUDevice`. That provides three direct benefits:

- compiled pipeline caches survive across components and SPA route changes;
- the page avoids requesting an adapter and device for every canvas;
- it stays below browser device limits and reduces GPU-resource churn.

The runtime also watches size and visibility. Offscreen canvases throttle to about 1 FPS. CSS size and pixel ratio determine backing resolution. A page-level circuit breaker stops new renderers after adapter, device, or out-of-memory failures rather than letting several effects freeze the tab together.

This is more representative of production performance work than removing a few multiplications from one shader. Complex effects can still be expensive: blur, feedback simulations, 3D distance fields, high DPR, and nested layers increase memory, dispatches, or pass count. The official skill recommends flat stacks, hiding unused layers instead of setting opacity to zero, and avoiding unnecessary nesting.

Distribution size is not free either. npm reports an unpacked size of about **29.1 MB** for `4.0.2`. The local full build emitted a roughly 2.49 MB minified vanilla-JS convenience bundle and a 3.3 MB React CDN bundle. Per-component exports and `sideEffects: false` allow normal bundlers to tree-shake selected imports, so those full bundles are not equivalent to every site's network cost. Import discipline still matters.

---

## 06 | WebGPU-Only Is a Clear Choice and the Largest Compatibility Boundary

The source explicitly rejects a WebGL context. The current renderer has one WebGPU path. “SSR safe” means modules can be imported on a server without touching `navigator.gpu`, and framework components avoid server rendering. It does not mean a server can generate pixels or an older browser silently falls back to WebGL.

When WebGPU is missing, no adapter can be granted, a device is lost, or initialization fails, the default behavior favors a transparent canvas and a quiet production console. Hosts can use `isWebGPUSupported`, the full async probe, and `onUnavailable` to select a still image, CSS background, or normal DOM fallback.

That policy is sensible for decorative visuals: a failed effect should not break the article or product beneath it. It is insufficient when the shader itself carries control state, data meaning, or navigation. Accessibility semantics, static alternatives, and `prefers-reduced-motion` remain application responsibilities.

---

## 07 | Frame-Locked Rendering Connects the Web to Video Without Becoming a Video Editor

Version 4.0.2 adds `createRendererFromJSON(...).renderFrame({ deltaSeconds })`. Once frame-locked mode begins, animation clocks stop following wall time and advance only by the host's supplied delta. Repeated `1/60` steps produce a deterministic 60 fps timeline; `deltaSeconds: 0` repaints without advancing time.

That matters for Puppeteer capture, Remotion integration, and offline video generation because machine speed no longer changes animation phase. By default, `renderFrame` also waits for a GPU fence so the host knows the canvas is complete before reading it.

Shaders is not a Remotion replacement. It does not provide a multi-shot timeline, audio, captions, media encoding, or final-program orchestration. Stateful feedback simulations must still advance frame by frame instead of jumping directly to frame 600. The package supplies a **deterministically stepped visual renderer**; a video system still owns timeline, composition, and output.

---

## 08 | Agent Skill and MCP: Let AI Operate Component Semantics Before Writing WGSL

The repository includes a substantial Agent Skill with all 199 components, composition rules, dynamic props, performance constraints, and cross-framework idioms. The site also publishes `llms.txt` and a complete component reference. The CLI installs the skill, while `install-mcp` configures the hosted MCP endpoint for Claude Code, Cursor, Codex, and other tools.

This narrows an agent's output space. It can select known components, use real props, and produce a component tree; only an unmet visual requirement should lead to custom WGSL. A structured catalog is easier to validate than an unconstrained model guessing a shader API, and the result remains editable in the visual tool.

The boundary matters: the open repository includes the skill documentation and MCP installer, but the MCP service itself is hosted by shaders.com. Preset search, cloud project synchronization, and Pro content depend on remote APIs and account permissions. This is not a fully offline open-source agent studio.

---

## 09 | One Default That Should Not Hide Behind the Visuals: Performance Telemetry

The telemetry source applies a **5% random sample** to regular `<Shader>` instances on external sites. Components marked as previews bypass random sampling. The payload includes:

- FPS, average/min/max/P99 frame time, jank, and budget usage;
- renderer type, draw calls, and texture count;
- component names, RTT requirement, and render order;
- the current domain, browser family, and desktop/mobile/tablet class;
- a random session ID, package version, and timestamp.

The payload does not contain component props, user content, or a full user-agent string, but it is sent to `shaders.com/api/telemetry`. `<Shader disableTelemetry>` and browser Do Not Track disable collection. The external-user path excludes shaders.com, localhost, and `127.0.0.1`.

The implementation is inspectable and has an explicit opt-out, which is better than invisible collection. The README and primary skill flow do not prominently explain it, however. Privacy-sensitive, internal, or regulated deployments should make `disableTelemetry` an explicit decision instead of relying on the 5% probability.

---

## 10 | Maturity: Strong Tests, Young Public Governance

I performed the following checks against the pinned commit:

- `pnpm install --frozen-lockfile` completed;
- **268 test files and 1,795 tests passed**;
- all eight workspace build tasks completed;
- generated files matched the tracked source after the build;
- Core Renderer, release checks, npm publication, and GitHub CodeQL checks on the pinned commit were green;
- `shaders@4.0.2` is published on npm, centered on `typegpu@0.12.3`.

The tests cover composition, structural hashing, WGSL snapshots, uniforms, device loss, RTT, compute scaffolds, and a large share of component contracts. This is clearly more than a gallery with source-shaped decoration. The local Vitest run primarily validates generated code and CPU-side behavior, however. **I did not complete pixel-level regression across Chrome, Safari, Firefox, and multiple physical GPUs, nor independently verify the company's claims of 16,000+ users, thousands of sites, or every performance result.**

Public governance is also new. The implementation is substantial, but its public Git history contains only 14 commits. Issue history, outside maintainership, and long-term upgrade evidence still need time to develop. MIT release is meaningful; it does not instantly create a mature community-governed project.

![ReactionDiffusion maintains compute state across frames rather than acting as a static fragment](imgs/shaders-webgpu-component-compiler/reaction-diffusion.jpg)

---

## 11 | Where It Fits, and Where It Does Not

Shaders is a strong fit for:

- product teams bringing GPU visuals into React, Vue, Svelte, or Solid component systems;
- design engineers who want the editor and source code to share one editable visual tree;
- interactive backgrounds, materials, lights, transitions, or pointer effects that do not justify a Three.js scene;
- toolchains that need fixed-time-step web visuals rendered frame by frame by a video host;
- teams that want agents constrained by component semantics before resorting to raw WGSL.

It is not a direct answer for:

- critical UI that must work without WebGPU and has no planned fallback;
- applications needing a general 3D scene graph, cameras, skeletal animation, physics, and broad material systems;
- complete video timelines, audio, encoding, and program orchestration;
- workflows requiring the editor, preset marketplace, MCP service, and runtime to be entirely offline and self-hosted.

A responsible adoption begins with one noncritical visual and two or three imports. Measure first-load JavaScript, GPU memory, interaction frame rate, low-end hardware, background tabs, no-WebGPU behavior, and reduced-motion handling before expanding the surface area.

---

## 12 | Conclusion: Shader Code Is Becoming an Intermediate Representation for Design Systems

The important move in Shaders 4.0 is not wrapping Aurora in `<Aurora />`. It is compressing information once scattered across shader files, uniform panels, framework state, and design mockups into a compilable, exportable, synchronized component tree.

That tree gives the editor, five framework targets, CLI, Agent Skill, MCP, and frame renderer one language. The GPU runtime then lowers it into fragment, compute, and only the necessary RTT passes. The commercial platform sells designed assets and workflow; the MIT repository opens the engine that executes the language.

The most accurate definition is therefore not “a WebGPU effects library,” but **a visual intermediate representation for design engineering, plus a runtime that compiles it onto the browser GPU.** It remains young, WebGPU-only, and dependent on explicit decisions about bundle size, telemetry, and hosted services. It nevertheless offers a much more production-shaped path than copying shader snippets from a gallery.

---

## Primary Sources

- [Shaders GitHub repository](https://github.com/shader-effects-inc/shaders)
- [Shaders site and visual editor](https://shaders.com/)
- [Shaders v4.0.2](https://github.com/shader-effects-inc/shaders/releases/tag/v4.0.2)
- [npm registry metadata for shaders 4.0.2](https://registry.npmjs.org/shaders/4.0.2)
- [`composer.ts`: component-tree composition](https://github.com/shader-effects-inc/shaders/blob/9435282c29d3505c67eef427470c8d835095a199/packages/core/src/gpu/composer.ts)
- [`root.ts`: GPU-device sharing and cache lifetime](https://github.com/shader-effects-inc/shaders/blob/9435282c29d3505c67eef427470c8d835095a199/packages/core/src/gpu/root.ts)
- [`support.ts`: WebGPU availability and failure policy](https://github.com/shader-effects-inc/shaders/blob/9435282c29d3505c67eef427470c8d835095a199/packages/core/src/gpu/support.ts)
- [`presetRenderer.ts`: frame-locked rendering](https://github.com/shader-effects-inc/shaders/blob/9435282c29d3505c67eef427470c8d835095a199/packages/core/src/presetRenderer.ts)
- [Telemetry sampling and opt-out](https://github.com/shader-effects-inc/shaders/blob/9435282c29d3505c67eef427470c8d835095a199/packages/core/src/telemetry/index.ts)
- [Shaders Agent Skill](https://github.com/shader-effects-inc/shaders/blob/9435282c29d3505c67eef427470c8d835095a199/skills/shaders/SKILL.md)
- [CLI documentation](https://shaders.com/docs/guide/cli)
- [Custom components](https://shaders.com/docs/guide/custom-shaders)
- [License and platform boundary](https://shaders.com/license)

*Audit date: October 8, 2026. Source snapshot: `v4.0.2` / `9435282c29d3505c67eef427470c8d835095a199`. The component catalog, hosted services, Pro entitlements, browser WebGPU support, and telemetry behavior will continue to change.*
