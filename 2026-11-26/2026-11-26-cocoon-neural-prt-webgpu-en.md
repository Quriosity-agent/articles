# Cocoon: Blender Traces the Light, WebGPU Shades 87,260 Fibres

> Silk cocoons descend into the dark, glow from within, and drop as their supporting webs break strand by strand. Yuri Artiukh's 26-second loop renders live in the browser. Blender still does an important job: it calculates how light travels through the shell and between the fibres offline, so small networks can learn the result.

- Yuri Artiukh (@akella), Codevember 2026 experiment 20, posted November 26, 2026. [Original X post](https://x.com/akella/status/2125917117526540700)
- [Live sketch](https://akella.github.io/codevember-2026/20/) · [Author's technical notes](https://akella.github.io/codevember-2026/20/notes.html) · [Source snapshot reviewed](https://github.com/akella/codevember-2026/tree/902fcb1f492dac4138d72aad16dd85af71ceeda4/20-cocoon)
- Tested in Chrome 158 on a Mac with a 1000 × 1000 canvas. I verified that the scene moved and changed the internal light at a fixed time. I did not retrain the models or reproduce the author's performance figures.

![At 18.5 seconds in the original clip: warm light, silk, and out-of-focus cocoons](imgs/cocoon-neural-prt-webgpu/x-loop-18-5s.webp)

*Frame from Yuri Artiukh's X clip at 18.5 seconds. The original post has a 1024 × 1024, 30 fps recording; the website renders the scene live.*

## 1. The Network Learns Lighting, Not Geometry

The nine cocoons in the main scene are instances of one detailed asset. It has a shell and **87,260 fibres**, including wound silk, loose loops, short down and long strays, with about **1.38 million curve control points** per cocoon. Scripts including `bake/hero.py` construct that shape. The model does not generate it as the scene plays. It predicts how much light and what colour a point on the silk sends toward the viewer. [Geometry script](https://github.com/akella/codevember-2026/blob/902fcb1f492dac4138d72aad16dd85af71ceeda4/20-cocoon/bake/hero.py) · [Technical notes](https://akella.github.io/codevember-2026/20/notes.html)

| Stage | What happens |
| --- | --- |
| Offline reference renders | Cycles renders 1,400 views at 576 × 576 and 48 samples, recording the lamps and internal light separately. |
| Offline fitting | Small networks, spatial feature textures and per-fibre parameters learn how the geometry responds to light. |
| Page load | The browser unpacks the curves and trained data, builds shell relief on the GPU, and solves several web-tearing trajectories in workers. |
| Each frame | WebGPU updates the shading that needs it, draws the fibres as narrow ribbons along their curves, and applies depth of field, bloom and tone mapping. |

This is neither generated video nor a Gaussian splat. The main scene uses raw WebGPU for computation and drawing. Three.js supplies camera math and orbit controls rather than the main shading pipeline. [Training script](https://github.com/akella/codevember-2026/blob/902fcb1f492dac4138d72aad16dd85af71ceeda4/20-cocoon/bake/train_hero.py) · [WebGPU entry point](https://github.com/akella/codevember-2026/blob/902fcb1f492dac4138d72aad16dd85af71ceeda4/20-cocoon/src/glow/index.ts)

## 2. Why This Is More Than a Baked Texture

A conventional light bake can store how a surface looks under fixed lights. Change those lights, and the baked result does not update by itself. Here, **precomputed radiance transfer (PRT)** means learning the asset's response to light, not just storing its appearance under one setup. The contribution of a lamp is split into two parts: one depends on where you are on the silk and the viewing direction; the other depends on the light direction. Their dot product gives the response. Contributions add up, so the renderer can fold the lamps into the network's final layer instead of running the full network once per lamp at every curve point. That does not make scheduling, shadow calculations or total rendering cost independent of lamp count. [Cocoon's lighting formulation](https://akella.github.io/codevember-2026/20/notes.html) · [Neural PRT paper](https://repo-sam.inria.fr/fungraph/neural-prt/)

**One change at second 13.** I held the playhead using the sketch's debug interface and changed `inside` from the default `1.1` to `0`. The cocoons and hanging strands stayed in place, while the warm glow in the sharp foreground cocoon faded. Both images were rendered by the website, not colour-graded from a recording.

| Default internal light `1.1` | Internal light `0` |
| --- | --- |
| ![Second 13 with the default internal light](imgs/cocoon-neural-prt-webgpu/browser-13s-inside-on.webp) | ![The same moment with internal light turned off](imgs/cocoon-neural-prt-webgpu/browser-13s-inside-off.webp) |

The learned response belongs to this asset; it is not a drop-in relighter for arbitrary GLBs. Shadows between cocoons use ellipsoidal approximations, and tiny strand glints are added by hand. The scene also dims the outside light as the cocoon glows, so it reads as a lantern. That is a cinematography choice, not a physical property of silk. [Approximations and limitations](https://akella.github.io/codevember-2026/20/notes.html)

## 3. The Largest Savings Come From Leaving Unchanged Light Alone

With a fixed camera, the renderer can store the interior and exterior responses separately, then mix them at draw time. A stationary cocoon can brighten without recalculating all its lighting. Rotating cocoons refresh when needed; other updates are staggered. Out-of-focus cocoons use fewer, wider fibres, and shading between selected control points can be interpolated. This removes work where the camera is least likely to reveal the difference. The notes describe a useful counterexample: one optimization made the scene black and still timed faster, prompting the author to compare rendered pixels alongside frame times. [Performance and image checks](https://akella.github.io/codevember-2026/20/notes.html)

The final figure in the notes is **about 12.3 ms per frame at 2268 × 1473 on an M1 Max**. The earlier 54 ms row used seven cocoons at 1600 × 900, so those numbers are not a controlled speedup comparison. Nor is **72 KB** the whole download: that is the weight footprint. The author's breakdown totals roughly **5.97 MB** after including geometry, learned textures, per-fibre features and code. [Frame and download breakdown](https://akella.github.io/codevember-2026/20/notes.html)

## 4. What to Borrow for a Browser-Based Shot

The useful target is a shot with a known asset, changing light, and a material whose fibres or translucency matter. Start with one object and a Cycles reference, then match the camera in the browser and compare brightness, silhouette detail and transmission. Only then decide what must update live and what can disappear into depth of field. For a single fixed MP4, offline rendering may be simpler. This pipeline earns its complexity when the scene should still respond after it has shipped.

The loop is a separate technique worth borrowing. Workers solve the tearing during page load, and playback samples those trajectories at different phases for each cocoon. The objects are outside the picture at the ends of their cycles, so the scene can repeat without dissolving the first and last frames together. [Loop timeline](https://github.com/akella/codevember-2026/blob/902fcb1f492dac4138d72aad16dd85af71ceeda4/20-cocoon/src/glow/life.ts)
