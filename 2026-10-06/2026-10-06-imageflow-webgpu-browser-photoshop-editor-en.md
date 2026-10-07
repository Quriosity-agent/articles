---
title: "ImageFlow Deep Dive: Not 'Photoshop Rebuilt,' but WebGPU Moving Professional Image Editing Into the Browser"
date: 2026-10-06
source: "https://x.com/ybouane/status/2107450802612961602"
canonical: "https://imageflow.dev/"
tags:
  - ImageFlow
  - WebGPU
  - Browser Image Editor
  - Photoshop
  - PSD
  - On-device AI
  - Color Management
  - Creative Tools
---

# ImageFlow Deep Dive: Not “Photoshop Rebuilt,” but WebGPU Moving Professional Image Editing Into the Browser

> **TL;DR:** Yassine Bouanane launched ImageFlow with a deliberately provocative instruction to cancel Adobe subscriptions. ImageFlow is a free, Photoshop-style image editor that runs directly in a browser tab. It is not a static concept or a lightweight filter app wearing a familiar interface. The live `0.1.0` build tested on October 7, 2026 can create documents and exposes PSD saving, smart objects, adjustment layers, layer styles, vector masks, Liquify, Camera Raw, Relight, Depth Blur, content-aware fill, and local AI selection. Its About panel reported a WebGPU / Apple / Metal 3 renderer on the test Mac. More importantly, ImageFlow brings PSD/PSB, CMYK/Lab, variable fonts, HarfBuzz shaping, on-device models, and multi-format codecs into one browser runtime. “Everything Photoshop can do” remains launch copy, not a completed compatibility finding. This review did not validate complex PSD/RAW/CMYK round trips, long-session stability, plugins, or print color. The editor is currently free but proprietary, and its claim that files never leave the device has not yet been independently audited.

- **X post:** [Yassine Bouanane / `@ybouane`](https://x.com/ybouane/status/2107450802612961602)
- **Product:** [ImageFlow](https://imageflow.dev/)
- **Post date:** October 6, 2026
- **Tested build:** ImageFlow Photo Editor `0.1.0`, build `fd1b1ae`, October 7, 2026
- **Current price:** The official page reports free / USD 0
- **Software license:** Proprietary; the website grants a personal, non-exclusive, non-transferable license
- **Verified:** October 7, 2026

![Official ImageFlow visual for its Photoshop-grade browser editor](imgs/imageflow-webgpu-browser-photoshop-editor/01-imageflow-official-banner.png)

## The Short Version

The reason to pay attention to ImageFlow is not that it has earned the right to declare Photoshop replaced. It is that the product already places a set of professional editing primitives, historically associated with a large native desktop application, inside a directly accessible browser runtime.

The important combination is **a local document model, GPU composition, browser-side machine learning, and professional file interoperability**.

If ImageFlow only offered cropping, presets, background removal, and templates, it would be another online photo tool. Its ambition is deeper: preserve layers, masks, adjustments, smart objects, font axes, color modes, and a PSD workflow so that the browser becomes the workstation rather than the upload gate.

## What the Post Claims and What Is Actually Live

The launch post's strongest line is:

> Everything Photoshop can do, running free inside a single browser tab.

Bouanane later made the scope more specific in replies: full PSD support, WebGPU, smart objects, vectors, typography including variable fonts, CMYK, RAW, ICC profiles, Liquify, object selection, and layer styles.

Those claims do not become independently verified just because they appear in a follow-up. ImageFlow is, however, already more than a “launching in 24 hours” teaser. At verification time, `imageflow.dev` opened directly into the editor without a marketing landing page or account requirement.

The live check completed the following steps:

1. opened New Document and created a 1920x1080 RGB/8-bit document;
2. confirmed Bitmap, Grayscale, Duotone, Indexed Color, RGB, CMYK, Lab, and Multichannel in the mode selector;
3. found Save PSD, Save PSD As, Place Image, Place Linked, and format export commands under File;
4. found adjustment layers, layer styles, layer and vector masks, background removal, and smart objects under Layer;
5. found Filter Gallery, Liquify, Smart Filters, Depth Blur, and multiple traditional filter groups under Filter;
6. found Camera Raw, Relight, Apply Image, and Vectorize Bitmap under Image;
7. confirmed version `0.1.0`, with WebGPU / Apple / Metal 3 and Chrome 153 in About.

This establishes that the editor and its interface are real, and that WebGPU initialized successfully on the test machine. It does not establish behavior or pixel equivalence with Photoshop for every listed command.

![Six frames from the ImageFlow launch demo: browser execution, editing, content-aware fill, variable fonts, saving, and free positioning](imgs/imageflow-webgpu-browser-photoshop-editor/02-imageflow-launch-demo-contact-sheet.png)

## Why the Browser Can Carry This Editor Now

Professional image editing has been difficult to move to the web not because menus are difficult to reproduce, but because the system must combine high-throughput pixel computation, a complex document graph, font shaping, color conversion, large-file decoding, and low-latency interaction.

ImageFlow distributes these responsibilities across several browser runtime layers:

| Runtime layer | Publicly disclosed or observed role |
|---|---|
| WebGPU | Used for composition and display in the tested environment, backed by Apple Metal 3 |
| Document model | Layers, groups, clipping masks, adjustment layers, smart objects, smart filters, and masks |
| Browser-side ML | `onnxruntime-web` and `@huggingface/transformers` support local model features such as selection |
| Type system | HarfBuzz handles shaping; the interface exposes variable fonts and OpenType controls |
| File codecs | pdf.js, `@jsquash` codecs, FlashRaw, HEIC, GIF, and SVG components cover multiple formats |
| PWA file handling | The Web App Manifest registers PSD/PSB, PNG, JPEG, WebP, TIFF, GIF, and AVIF handlers |

The resulting architecture resembles a desktop application compressed into a browser:

```text
Local file / new document
        ↓
Format decoding, font shaping, color handling, and local models
        ↓
Layered document state and non-destructive editing
        ↓
WebGPU composition and interactive preview
        ↓
PSD or publication-format export
```

That is the significance of WebGPU. Canvas 2D is adequate for simple drawing, but it becomes a limiting abstraction for large canvases, complex blending, real-time filters, and deep compositions. WebGPU gives the web a modern path to the graphics processor: the browser supplies distribution and sandboxing, while the GPU runs the pixel pipeline.

## PSD Support Is Much Harder Than Opening a PSD

ImageFlow's File menu does not stop at Open. It explicitly offers Save PSD and Save PSD As. The launch film also shows a `golden-hour.psd` document alongside PNG, JPEG, WebP, AVIF, SVG, PDF, GIF, and TIFF deliverables.

![Layered editing in the launch film, with a type layer, toolbar, and PSD document visible together](imgs/imageflow-webgpu-browser-photoshop-editor/03-imageflow-layered-editor-demo.png)

In a professional workflow, “PSD support” has at least four levels:

1. **Open:** read dimensions and a composite preview without crashing;
2. **Parse:** preserve editable layers, groups, masks, text, effects, and smart objects;
3. **Round-trip:** save and reopen in Photoshop while retaining structure and appearance;
4. **Produce:** remain reliable with large files, linked assets, missing fonts, 16/32-bit data, CMYK/Lab, and edge-case formats.

The public interface shows that ImageFlow is aiming at level three, not merely building a PSD viewer. There is no published compatibility matrix, regression corpus, pixel-diff report, round-trip result set, or failure taxonomy yet. A Save PSD menu cannot be promoted into a claim of complete PSD compatibility.

This is where the product most needs to build trust. Design teams need a published test suite that explains which features survive unchanged, which are rasterized, which preserve appearance only, and which are not supported.

## CMYK, ICC, and Type Define the Professional Boundary

Background removal and content-aware fill make better launch footage, but less photogenic capabilities determine whether an editor can enter real brand and print workflows:

- CMYK, Lab, and Multichannel documents;
- reading, converting, preserving, and exporting ICC profiles;
- filter and compositing consistency at 8, 16, and 32 bits;
- missing-font substitution, OpenType features, and variable font axes;
- glyph, line-break, and baseline stability after reopening;
- round-trip behavior for smart objects, linked files, and embedded assets.

ImageFlow's New Document panel does list several professional color modes. The creator publicly claims CMYK, RAW, and ICC support. The live third-party notices identify HarfBuzz for shaping and a camera RAW decoder. These are signals of a serious editor rather than a cosmetic imitation.

“Selectable in a menu” and “trusted color management” remain different standards. Display profiles, soft proofing, rendering intents, black-point compensation, embedded profiles, and post-export validation all require direct testing. Without that evidence, print delivery should not be approved based on interface labels alone.

## Local AI as an Editing Primitive, Not a Chat Box

ImageFlow's AI direction differs from products that redraw an image after a natural-language instruction. The official feature list emphasizes on-device AI selection and background removal, while the interface exposes Object Selection, Remove Background, Content-Aware Fill, Depth Blur, and Relight.

These capabilities fit traditional editing grammar: build a selection, then produce a mask or fill; estimate depth, then adjust blur or lighting. The result returns to a layered document instead of ending as a single unstructured replacement image.

That matters more to professional workflows than adding a chat panel beside the canvas. Editors need AI to produce editable intermediate state: selections, masks, depth maps, adjustment parameters, or new layers.

Local models introduce their own compatibility surface: first-run downloads, caches, device memory, WebGPU support, low-end performance, and browser variance. ImageFlow has not published a standardized performance benchmark, so “lightning fast” remains the creator's characterization.

## Why “Everything Photoshop Can Do” Is Not Established

Photoshop is not a menu inventory. It is more than three decades of accumulated compatibility, automation, plugins, color management, printing, collaboration, and recovery from malformed files.

Adobe itself maintains a detailed comparison between Photoshop web and desktop. The web version still differs in warp, actions, several painting and typography capabilities, Neural Filters, parts of Smart Filters, Lens Correction, and other areas. Even one company moving its own document format across runtimes has to define gaps command by command. A third-party `0.1.0` build cannot prove total replacement by feature count.

A more useful evidence table is:

| Question | Current evidence |
|---|---|
| Is it a real browser editor? | Yes. It starts, creates documents, and exposes a working editor interface |
| Does it cover many Photoshop-style concepts? | Yes. Its menus, document model, and official feature list are unusually deep |
| Can it handle PSD/PSB? | Officially and visibly supported, but no complex round-trip test was run for this review |
| Does it use WebGPU? | Yes on the tested Mac, where About reported WebGPU / Apple / Metal 3 |
| Is all file processing local? | The site says so; this review did not perform a full network and privacy audit |
| Is it equivalent to Photoshop? | Not established; compatibility, stability, performance, and production evidence are missing |

“Everything” is an effective launch hook. It is not a procurement finding.

## Free, but Not Open Source

ImageFlow currently reports a price of USD 0, and the launch video displays `100% FREE`. It is not an open-source project.

The official [License](https://imageflow.dev/license) states that ImageFlow's source, compiled code, shaders, algorithms, lookup tables, and assets are proprietary. Users receive a personal, non-exclusive, non-transferable license to access it through the website. The terms restrict copying, modification, distribution, sublicensing, reverse engineering, decompilation, scraping, extraction, and machine-learning training.

That creates two practical distinctions:

1. **Free does not mean self-hostable.** If the service, terms, or availability changes, users do not automatically have source as a fallback.
2. **Open third-party components do not make the product open source.** pdf.js, ONNX Runtime Web, Transformers, HarfBuzz, and the other listed components retain their own licenses, while ImageFlow remains proprietary.

A team considering long-term production use should evaluate migration formats, offline behavior, version pinning, and an exit path in addition to the current zero price.

## What the Privacy Promise Still Needs

The homepage metadata says, `Nothing is uploaded; your files never leave your device.` Browser rendering, local models, and local file processing are consistent with that design direction. Photopea has also demonstrated that a mature in-browser editor can follow this architecture.

ImageFlow currently has no accessible `/privacy` page; that path returned 404 during verification. This review also did not load a confidential file and capture every network request, so it cannot independently confirm that every open, save, feedback, font, and model path avoids content transmission.

For ordinary test images, that is not a reason to avoid evaluation. For unreleased client assets, medical images, identity documents, or NDA-protected designs, a team should first perform:

1. network-request inspection;
2. an inventory of model, font, and telemetry domains;
3. IndexedDB, Cache Storage, and service-worker lifecycle checks;
4. cache clearing and local-copy deletion verification;
5. review of an explicit privacy policy and enterprise responsibility boundary.

“Local first” is an architectural direction. “Privacy audited” is a different class of evidence.

## Its Position Relative to Photopea and Photoshop Web

ImageFlow is not the first product to process PSDs locally in a browser. Photopea has done this for years; its official documentation says files do not leave the device and documents can be opened and saved as PSD. Adobe also offers Photoshop on the web and publishes the differences between its web and desktop versions.

ImageFlow's differentiation is better described as a combination of three choices:

- a highly familiar Photoshop interaction model with a deep professional menu surface;
- WebGPU as the current high-performance composition path;
- object selection, background removal, content-aware tools, depth, and relighting as on-device editing primitives.

![Launch-film deliverables: PSD plus PNG, JPEG, WebP, AVIF, SVG, PDF, GIF, and TIFF](imgs/imageflow-webgpu-browser-photoshop-editor/04-imageflow-export-formats-demo.png)

That makes it worth testing, but the competition will not be decided by whether a command exists. Photopea has maturity and an installed user base. Adobe has the document ecosystem and end-to-end workflow. ImageFlow must prove through compatibility, speed, stability, and better local AI editing that it is not only familiar but meaningfully easier for particular jobs.

## How a Production Team Should Evaluate ImageFlow

Do not begin with a client's only master file. Build a test corpus with known expected results:

1. a simple RGB PSD with layers, masks, type, blend modes, and adjustments;
2. a complex PSD with smart objects, linked resources, layer styles, clipping masks, and artboards;
3. type samples with variable fonts, multilingual shaping, OpenType features, and missing-glyph fallback;
4. color samples with embedded-profile RGB, CMYK, Lab, 16-bit TIFF, and RAW;
5. performance samples with large canvases, many layers, expensive filters, and repeated undo;
6. AI samples with fine hair, transparency, low-contrast objects, Depth Blur, and Relight;
7. round-trip tests by saving in ImageFlow and reopening in Photoshop and Photopea;
8. privacy checks across network activity, caches, model downloads, and clearing behavior.

For each sample, record open state, edited state, reopened state, pixel differences, layer structure, font substitution, profile handling, peak memory, and elapsed time. Only then can a team decide whether ImageFlow belongs in quick corrections, social graphics, web assets, or master-file production.

## Conclusion

ImageFlow's launch copy frames the question as whether users should keep paying Adobe. The more consequential question is: **how much professional image-editing state can a browser tab now carry?**

The live `0.1.0` interface already goes far beyond a lightweight web editor. It contains the right foundational pieces: a layered document, non-destructive edits, smart objects, traditional filters, color modes, variable type, PSD saving, local ML, and WebGPU rendering.

Replacing Photoshop has never meant reproducing its menus. It requires complex-file round trips, trustworthy color, performance ceilings, failure recovery, privacy, automation, plugins, and years of compatibility. ImageFlow has shown that the browser can enter that contest. It has not shown that the contest is over.

## Sources

1. Yassine Bouanane, ImageFlow launch post on X
   https://x.com/ybouane/status/2107450802612961602

2. Yassine Bouanane, follow-up on PSD, WebGPU, smart objects, typography, CMYK, RAW, and ICC
   https://x.com/ybouane/status/2107700833492017172

3. ImageFlow editor and product metadata
   https://imageflow.dev/

4. ImageFlow Web App Manifest
   https://imageflow.dev/manifest.webmanifest

5. ImageFlow License
   https://imageflow.dev/license

6. Adobe, “Compare Photoshop web and desktop features”
   https://helpx.adobe.com/photoshop/web/get-set-up/learn-the-basics/compare-photoshop-web-and-desktop-features.html

7. Photopea, “Introduction”
   https://www.photopea.com/learn/
