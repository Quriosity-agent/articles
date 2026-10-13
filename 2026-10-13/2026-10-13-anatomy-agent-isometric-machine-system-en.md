# Inside Anatomy: Not an Illustration Prompt, but a Verifiable Isometric Machine-Drawing System for Agents

> **Bottom line:** [`donghaozhang/anatomy`](https://github.com/donghaozhang/anatomy) is neither a new image model nor a SaaS that turns one sentence into an illustration. The repository supplied by the user is a synchronized fork of [`wheresryan22/anatomy`](https://github.com/wheresryan22/anatomy). What the project actually ships is an Agent Skill, a framework-free JavaScript/TypeScript geometry kit, and a browser acceptance harness. Claude Code, Codex, or another coding agent must reinterpret an abstract concept as a physical machine that explains itself, then implement that machine as SVG, WebGL, or experimental orbitable 3D. Anatomy does not draw instead of the agent. It constrains how the agent turns an explanation into auditable code.

![Anatomy's Raptor engine example combines an SVG machine with a WebGL plume](imgs/anatomy-agent-isometric-machine-system/raptor-engine-firing.webp)

This audit is pinned to the October 13, 2026 commit [`454a0ef`](https://github.com/wheresryan22/anatomy/tree/454a0ef801b6d9b905f08309d094491c7085b3dd). At audit time, the supplied fork and upstream `main` resolved to the same commit. The upstream repository had 6,389 stars and 456 forks, and its latest release was [`v1.1.0`](https://github.com/wheresryan22/anatomy/releases/tag/v1.1.0). Those counts will change; the technical findings below are tied to the pinned source.

---

## 01 | The central rule: the object is the explanation

Technical illustrations often collapse into colored boxes, arrows, and labels. Anatomy deliberately reverses that habit in [`SKILL.md`](https://github.com/wheresryan22/anatomy/blob/454a0ef801b6d9b905f08309d094491c7085b3dd/SKILL.md): before drawing a flowchart, the agent must invent a physical object whose structure and motion carry the meaning.

- A token bucket can become a literal hopper, reservoir, and valve.
- A GPU context can become a gantry, worktable, and memory gauges.
- A cache key can become a pin-tumbler lock.
- A scheduler or feedback loop can become a test rig with conveyors, returns, and live readouts.

That is the real difference between Anatomy and a “cyberpunk isometric illustration” prompt. A prompt mostly specifies style. Anatomy specifies an **explanatory model, parts, coordinate system, occlusion, interaction state, and acceptance process**. A successful result does not merely resemble a machine; readers should infer the original concept from its form and behavior.

![Ripple Tank turns wave sources, a medium, reflections, and live measurements into a legible apparatus](imgs/anatomy-agent-isometric-machine-system/ripple-tank.webp)

---

## 02 | It behaves like a small visual compiler pipeline

Anatomy divides production into stages that resemble a compiler:

1. **Set the specification.** Choose Figure, Hero, or Epic scope and define canvas, information density, and motion depth.
2. **Collect facts.** Gather real numbers, states, constraints, and causal relationships instead of working from a vague topic.
3. **Invent the machine.** Choose a physical apparatus that maps those relationships without falling back to boxes and arrows.
4. **List the parts.** Hero and Epic work usually begins with 40 or more visible components, then a world-coordinate plan.
5. **Build geometry once.** The same geometry drives rendering, collisions, occlusion, and audits so visual and validation logic do not drift apart.
6. **Resolve painter order.** Isometric projection and depth relationships determine the draw sequence.
7. **Add state.** Readouts, controls, hover, drag, keyboard input, and motion must reflect the same internal model.
8. **Accept in the browser.** Capture and operate the result across light and dark themes, desktop and mobile, zoom, hover, and reduced motion.

This is not a generator with a bundle of templates. The agent still writes the artifact. The Skill turns open-ended creation into an engineering process with intermediate representations and acceptance gates. The cost is equally clear: the repository describes the work as intentionally slow. Complex figures are not a seconds-long text-to-image operation.

---

## 03 | Three output paths: SVG, WebGL, and a custom 3D runtime

The first path is pure SVG, delivered as a standalone HTML page, a lone SVG, or React components. `iso-kit` provides the isometric camera, primitives, page shell, and CSS; `lathe` builds rotational forms; `tube` handles pipes and cables. React is used only for React deliverables. The core kit has no `package.json` and no runtime framework dependency.

The second path combines SVG and WebGL. Machine structure, labels, and controls remain in SVG, while continuous effects such as fire, exhaust, water, caustics, and lighting occupy a Canvas between back and front SVG layers. If WebGL is unavailable, the SVG fallback is still expected to remain legible rather than leaving a black artifact.

The third path is a beta 3D runtime. It does not use Three.js. Parts are reprojected and reshaded each frame, with an orbit camera, joints, and depth audits layered on top. The repository currently treats this as an example and test capability, not a production-ready general 3D engine.

![Turning Dial demonstrates orbitable 3D parts, an articulated hand, and synchronized readouts](imgs/anatomy-agent-isometric-machine-system/turning-dial.webp)

---

## 04 | The reusable breakthrough is the geometry ledger

The most valuable component is [`kit/audit.mjs`](https://github.com/wheresryan22/anatomy/blob/454a0ef801b6d9b905f08309d094491c7085b3dd/kit/audit.mjs). As the artifact draws solids, the kit also records real bounds, faces, tubes, terminals, supports, and depth relationships. The auditor can then check:

- clearances and solid penetration;
- tube terminals, loose ends, supports, and folds;
- self-overlap, profile wobble, pipe crowding, and seating;
- shape coverage, stand-ins, and painter depth order;
- 3D joints, dynamic parts, and occlusion across camera positions.

That is materially stronger than adding “avoid intersections” to a prompt because the check runs against geometry the agent actually emitted, not an assurance in generated prose.

The ledger has a clear boundary. Decorative lines may be authored directly in SVG markup and never enter the geometry records, so [`scripts/lines.mjs`](https://github.com/wheresryan22/anatomy/blob/454a0ef801b6d9b905f08309d094491c7085b3dd/scripts/lines.mjs) separately inspects line endings in headless Chrome. Even a completely green automated audit proves only that recorded geometry satisfies implemented invariants. It does not prove conceptual accuracy, physical truth, or aesthetic quality.

---

## 05 | The browser is a second test instrument, not just a preview

[`capture.mjs`](https://github.com/wheresryan22/anatomy/blob/454a0ef801b6d9b905f08309d094491c7085b3dd/scripts/capture.mjs) records desktop, mobile, hover, zoom, and reduced-motion states while reporting console failures, sideways scrolling, and readout issues. [`drive.mjs`](https://github.com/wheresryan22/anatomy/blob/454a0ef801b6d9b905f08309d094491c7085b3dd/scripts/drive.mjs) sends real pointer, key, and drag actions, waits for state transitions, and can test no-WebGL fallbacks, line endings, and 3D orbit behavior.

The Skill does not treat screenshots as ceremonial output. It tells the agent to read the contact sheet and inspect 4x close-ups in both themes for seams, floating parts, collisions, and typography. Human review remains essential because automation can detect structural errors but cannot decide whether the machine explains the concept well.

---

## 06 | How much better is it than asking Codex directly?

For a decorative one-off image, directly asking Codex to write SVG or calling an image model will be faster. Anatomy pays off when the goal is a **repeatable, interactive, regression-tested** technical visual:

| Directly prompt a coding agent | Use Anatomy |
|---|---|
| Style and structure emerge in one generation | Establish a semantic metaphor, parts list, and coordinate plan first |
| Rendering and collision checks may use different logic | One geometry model drives both drawing and audits |
| “Looks correct” may be the agent's own assertion | Geometry, browser, interaction, and screenshot evidence exists |
| A local edit can break occlusion or responsive behavior | Depth, terminals, mobile, zoom, and fallback paths can regress-test |
| The output may be only an image | The output is readable source, a standalone page, or React components |

It does not automatically improve the model's taste or make an ordinary agent a mechanical engineer. The agent still performs the two hardest jobs: inventing the right physical metaphor and implementing tens or hundreds of parts correctly. Anatomy raises the **process floor and visibility of errors**; it cannot guarantee that every model will match the official examples.

---

## 07 | Publishing treats reproducibility seriously, with a privacy cost

Community publishing runs only after an explicit user request or confirmation. The publisher copies source, records author, title, license, agent/model, up to 600 characters of the prompt, and optional elapsed time and token count. A kit fingerprint identifies the tool revision. The gallery rebuilds submissions inside a locked sandbox and rejects networking, `eval`/`new Function`, frames and cookies, environment reads, outside imports, nondeterminism, and forced animation under reduced motion.

This makes a gallery entry closer to reproducible source, but it also means metadata may reveal the original prompt, model choice, and work estimates. A dry run deserves review before `publish` is treated like an ordinary upload button.

---

## 08 | What I verified

I checked out pinned commit `454a0ef` on an Apple Silicon Mac, ran the test suite with the exact temporary dependencies used by CI, and rebuilt several official examples.

| Check | Result in this audit | Evidence boundary |
|---|---|---|
| Test suite | 38 test files; 245/245 passed, 0 failed, about 57.9 seconds | Local result, not every Chrome/OS environment |
| Arcade Cabinet geometry audit | 349 items, 243 solids, 15 tubes, and 1,290 overlap/order rules; zero clearance, terminal, loose-end, depth, self-overlap, wobble, saddle, stand-in, or crowding violations; audit passed | Proves the example satisfies encoded rules, not its semantic quality |
| Raptor Engine geometry audit | 478 items, 267 solids, and 80 tubes; checked 1,707,703 overlaps and 4,292 order rules with zero failing categories; passed in 168.3 seconds | Shows the depth of a complex-scene audit and that full verification is not lightweight |
| Turning Dial 3D verification | 88 parts; lock, dial, and articulated-hand dynamic layers verified; build took about 0.9 seconds | Repository example scale, not a general 3D benchmark |
| Example rebuilds | Dial Indicator, Ripple Tank, Arcade Cabinet, and Turning Dial were deterministic; the Git worktree remained unchanged after rebuilding | Demonstrates fixed-input build determinism |
| Latest official `main` CI | 244 of 245 tests passed; `drive preserves a successful wait condition` failed at its Chrome `until` wait | Current `main` cannot honestly be called green |

The latest official failure needs context. The previous `main` commit and the `v1.1.0` release commit were green. The diff from that green commit to current `main` changes only time-estimate wording in the Skill and the changelog, not the browser driver. The same current commit passed all 245 tests locally. The evidence therefore points more strongly to an environment-sensitive or intermittent browser wait than to a confirmed renderer regression. Still, the red upstream status remains an open risk until it passes again.

The repository reports 60fps for a small 3D figure and roughly 20fps on desktop and 13–15fps on a throttled phone for its 380-part stress case. Those are project-reported measurements, not independently reproduced cross-device benchmarks.

---

## 09 | The most accurate positioning

Anatomy fits machines, instruments, tools, furniture, and technical systems that can be explained spatially. It is not intended for charts, exact maps, people-centered stories, or instant image generation. WebGL effects require browser GPU support, 3D remains beta, and the project's own guidance says a full 30-part 3D orbit audit may take 15–20 minutes.

The best description is therefore neither “Remotion for diagrams” nor merely “an isometric illustration Skill.” Anatomy is a **visual engineering specification, geometry runtime, and browser acceptance harness for coding agents**. It asks an agent to deliver more than a polished screenshot: a source-defined artifact that can be operated, degraded gracefully, rebuilt, and challenged with evidence about where it may be wrong.

---

## Primary sources

- [User-supplied fork: `donghaozhang/anatomy`](https://github.com/donghaozhang/anatomy)
- [Upstream repository: `wheresryan22/anatomy`](https://github.com/wheresryan22/anatomy)
- [Pinned audit commit `454a0ef`](https://github.com/wheresryan22/anatomy/tree/454a0ef801b6d9b905f08309d094491c7085b3dd)
- [The Skill workflow](https://github.com/wheresryan22/anatomy/blob/454a0ef801b6d9b905f08309d094491c7085b3dd/SKILL.md)
- [Kit architecture](https://github.com/wheresryan22/anatomy/blob/454a0ef801b6d9b905f08309d094491c7085b3dd/references/kit.md)
- [Browser verification](https://github.com/wheresryan22/anatomy/blob/454a0ef801b6d9b905f08309d094491c7085b3dd/references/verify.md)
- [3D beta notes and project-reported performance](https://github.com/wheresryan22/anatomy/blob/454a0ef801b6d9b905f08309d094491c7085b3dd/references/3d.md)
- [Publishing, sandboxing, and metadata](https://github.com/wheresryan22/anatomy/blob/454a0ef801b6d9b905f08309d094491c7085b3dd/references/publish.md)
- [Current `main` CI run `38317963428`](https://github.com/wheresryan22/anatomy/actions/runs/38317963428)
- [`v1.1.0` release](https://github.com/wheresryan22/anatomy/releases/tag/v1.1.0)

*Audit date: October 13, 2026. Repository size, stars, forks, releases, CI, and performance will change; technical findings are pinned to commit `454a0ef`. Example images are local copies of assets in that commit. Performance numbers are explicitly identified as project-reported. I did not independently validate cross-device frame rates, output quality across arbitrary agents, or the production security of the community publishing service.*
