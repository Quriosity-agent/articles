# GenCAD Deep Dive: Generating Editable CAD Programs from Images, Not Just 3D Meshes

> Source page: [GenCAD](https://gencad.github.io/)  
> Paper: [arXiv:2409.16294](https://arxiv.org/abs/2409.16294) / [OpenReview TMLR 2025 PDF](https://openreview.net/pdf?id=e817c1wEZ6)  
> Code: [ferdous-alam/GenCAD](https://github.com/ferdous-alam/GenCAD)  
> Authors: Md Ferdous Alam, Faez Ahmed (MIT)  
> Date: 2026-05-18  
> Tags: CAD / 3D Generation / Diffusion / Contrastive Learning / Engineering AI / Manufacturing

![GenCAD project page and image-to-CAD demo](imgs/gencad-image-conditioned-cad-programs/project-page-hero.webp)

At first glance, GenCAD looks like another “image to 3D” research project. The important part is subtler: it is not merely trying to produce a plausible 3D shape. It is trying to generate an **editable, replayable, engineering-oriented CAD program**.

That is a very different target from mesh, voxel, or point-cloud generation. Those representations are convenient for machine learning, but they often produce geometric shells that are hard for engineers to revise. GenCAD instead targets parametric CAD command sequences: modeling operations such as lines, arcs, circles, and extrusions, which can be converted into a solid model by a geometry kernel.

This article treats GenCAD less as a paper summary and more as an early CAD-generation system: why it matters, how its architecture is layered, what the open-source code reveals, and what remains before this class of model becomes a real industrial CAD agent.

---

## 1. The problem is not 3D; it is editable 3D

In 3D generation research, meshes, voxels, and point clouds are natural choices. Data is easier to obtain, networks are easier to train, and metrics are relatively mature. But CAD is not just about surface appearance.

A mechanical design usually needs:

- traceable modeling steps;
- parameters that can be modified rather than a sculpted mesh;
- downstream export into manufacturing, simulation, and assembly workflows;
- engineering semantics such as holes, slots, extrusions, and sketch planes;
- a state that humans or automation systems can continue editing during design-space exploration.

GenCAD’s core claim is that, conditioned on an image, it generates a CAD command sequence rather than only an uneditable 3D surface. The paper abstract states that its output includes the full parameterized CAD command history / CAD program.

That matters for AI engineering tools. A valuable CAD agent should not stop at “draw me a bracket-like object.” It should produce a design object that an engineer can open, modify, constrain, export, and manufacture.

---

## 2. GenCAD’s four-layer architecture: learn CAD language, align images, then diffuse in latent space

The project page summarizes GenCAD as four stages:

1. an autoregressive transformer encoder learns latent representations of CAD command sequences;
2. a contrastive learning model aligns the latent spaces of CAD command sequences and CAD images;
3. a latent diffusion model generates CAD-command latents conditioned on CAD images;
4. a decoder converts CAD latents back into parametric CAD commands.

From a builder’s perspective, this is three systems stitched together.

### First: a CAD program language model

The repository’s `model/autoencoder.py` defines the `VanillaCADTransformer` family. It does not directly predict point clouds. It embeds command tokens and argument tokens into a Transformer:

- command embeddings for operations such as line, arc, circle, EOS, and SOS;
- argument embeddings for discretized parameters;
- group embeddings for sketch/extrusion structure;
- an encoder/decoder path that compresses CAD sequences into a 256-dimensional latent and decodes them back into commands.

`config/configAE.py` exposes the representation constraints: `d_model=256`, `dim_z=256`, four encoder/decoder layers, eight heads, `max_total_len`, and related CAD sequence limits.

### Second: an image-CAD alignment layer

The `ccip` branch in `train_gencad.py` loads a CAD autoencoder checkpoint, constructs a `CLIP(image_encoder, cad_encoder, dim_latent=...)`, and trains it on paired CAD images and command sequences. The default visual backbone is `resnet-18`.

This creates a shared embedding space for CAD programs and CAD renderings. The image is not merely an input condition; it becomes comparable to CAD latents for retrieval and conditional generation.

### Third: a latent diffusion prior

The `dp` branch reads `cad_embeddings.h5` and `sketch_embeddings.h5`, then trains a `ResNetDiffusion + GaussianDiffusion1D` prior. The diffusion model does not generate pixels or meshes. It generates in CAD latent space.

That is a pragmatic design choice. The diffusion model handles a lower-dimensional latent distribution, while the decoder and CAD representation carry the burden of turning samples back into structured command sequences.

---

## 3. Why this is not just a landing-page demo: the code exposes a real training and inference pipeline

I inspected the current `main` branch of the GitHub repository (HEAD `f5484cf`). It is not just a project page with paper figures. It includes training, inference, data processing, and CAD export paths.

At inspection time, the GitHub API reported:

| Item | Value |
|---|---:|
| Stars | 2313 |
| Forks | 264 |
| Primary language | Python |
| Default branch | main |
| Public license | Not declared |
| Open issues | 29 |
| Latest push | 2025-07-14 |

A shallow local clone contains roughly 43 Python files and about 8k lines of Python code, alongside JSON data/results, image assets, a Dockerfile, and conda/pip dependency files. The major directories are:

- `cadlib/`: CAD primitives, extrusion, sketch logic, visualization, and geometry macros;
- `model/`: autoencoder, CLIP/CCIP, image encoder, and diffusion prior;
- `trainer/`: autoencoder, CCIP, and 1D diffusion trainers;
- `utils/`: datasets, losses, CAD vector / point-cloud / image utilities;
- `train_gencad.py`: the three-stage training entrypoint;
- `inference_gencad.py`: image-to-CAD inference with STL/PNG export;
- `stl2img.py`: STL visualization helper.

The README also provides both Docker and manual installation paths. Inference depends on `pythonocc-core` / OpenCascade and recommends `xvfb-run` for headless server visualization. That means the project is touching a real CAD geometry kernel rather than only rendering a web demo.

![GenCAD examples: conditional generation, diversity, and retrieval](imgs/gencad-image-conditioned-cad-programs/examples-contact-sheet.webp)

---

## 4. Generation, retrieval, and diversity: three uses of the same representation

The project page demonstrates three capabilities.

### Image-conditioned CAD generation

The input is a CAD rendering. The output is an interactively viewable 3D model. The paper and page emphasize that this is not just solid appearance; the target is CAD program generation.

### Diverse sampling from the same image

The sample-diversity section shows multiple CAD samples from a single input image. This is where the latent diffusion prior matters. For engineering design, it suggests candidate exploration rather than pure reconstruction.

But diversity alone is not engineering usefulness. A CAD agent needs diversity plus constraint satisfaction and manufacturability checks. GenCAD addresses a crucial “image to CAD program” step, but it does not yet close the full engineering loop.

### Image-conditioned CAD retrieval

The page also shows retrieval: using an image query to retrieve the top-3 CAD programs from a collection of about 7000 CAD programs. This may be more immediately productizable than generation. In an enterprise CAD library, searching for similar parts from a sketch, screenshot, or rendering is safer and easier to adopt than generating new parts from scratch.

From that perspective, GenCAD’s contrastive representation is not merely an intermediate module. It could become the foundation for CAD database search, design reuse, and part recommendation.

---

## 5. The product lesson: do not generate only the result; generate the operation history

The most reusable idea in GenCAD is not a particular model component. It is the choice of output object. The system does not settle for terminal geometry; it targets CAD command sequences.

That lesson generalizes across professional software:

- a video-editing agent should not only output an MP4; it should output an editable timeline;
- a design agent should not only output a PNG; it should output Figma layers, constraints, and components;
- a data-analysis agent should not only output a chart; it should output a notebook, SQL, or pipeline;
- a CAD agent should not only output a mesh; it should output editable CAD history.

For professional AI tools, the valuable intermediate object is usually not the pretty artifact. It is the **program state that can be operated on next**.

That is why GenCAD, despite being a research project, is highly relevant to agent and workflow products. It connects visual input, retrieval, diffusion generation, and parametric program reconstruction into an early pattern for moving from perception to engineering operation history.

---

## 6. Current limitations: several gaps remain before industrial CAD agents

GenCAD is promising, but it is not the same as production CAD automation.

First, the data remains based on DeepCAD-style programmatic CAD data and rendered images. Real enterprise CAD includes assemblies, standard parts, materials, tolerances, BOMs, manufacturing constraints, and historical naming conventions. Those are not purely geometric problems.

Second, generation needs a stronger validity loop. Can the command sequence reliably become a solid? Does it self-intersect? Does it satisfy design constraints? Is it manufacturable? Those questions require geometry-kernel checks and rule-based or simulation-based feedback.

Third, the repository is closer to a research reproduction pipeline than a product system. The README’s Evaluation section still says “Coming soon,” the license is not declared, checkpoints and datasets are distributed through Google Drive, and the inference script contains hard-coded checkpoint paths. Those are normal for paper code, but they are exactly the engineering layers that must be hardened for production use.

Fourth, image conditioning is inherently ambiguous. The same rendering can correspond to multiple CAD histories. GenCAD handles this through diffusion-based diversity, which is reasonable. But real CAD software also needs user constraints, dimensions, sketch intent, material context, and manufacturing context.

---

## 7. Conclusion: the right direction for CAD generation is editable programs, not beautiful shells

GenCAD’s value is that it brings CAD generation back to the engineering object itself. It does not merely generate a 3D shape that looks like a part; it generates a parametric program that can be interpreted by a CAD kernel and preserve command history.

That makes the problem harder than generic 3D generation, but also much closer to industrial reality.

For AI tool builders, the broader takeaway is simple: when AI enters professional software, do not optimize only for the final rendered artifact. Systems that actually enter workflows must emit editable, auditable, executable intermediate representations.

In CAD, that representation is a command sequence. In video, it is a timeline. In design, it is a layer tree. In code, it is a commit, diff, and test harness. GenCAD is one example in CAD, but it points to a general product principle: **the endpoint of AI generation should not be a dead file; it should be a state that the next round of human-machine collaboration can continue operating on.**
