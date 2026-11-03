# Openjutsu: Sources and Verification

- Review date: 2026-11-03, Australia/Melbourne. The article date is the review date, not an asserted launch date.
- Requested repository: https://github.com/donghaozhang/openjutsu
- Upstream: https://github.com/D3voz/openjutsu
- Pinned commit: `7fe118bb5a61fcfac0148e1bfea3dd29884dbf26`.
- Commit timestamp: 2026-10-30T07:49:48Z. Subject: `Update the relight README picture to show all seventeen looks`.
- GitHub repository metadata identified the requested repository as a fork. The comparison API returned `identical`, ahead 0 / behind 0: https://api.github.com/repos/donghaozhang/openjutsu/compare/D3voz:main...main
- The web reader returned a cache miss for the requested GitHub page. Primary material was obtained through GitHub's API, raw files, and a temporary sparse Git checkout. No application accounts or private material were accessed.

## Primary Material

All project links below are pinned to the reviewed commit:

- [README: scope, modes, requirements, timing, limitations, deployment, licensing](https://github.com/donghaozhang/openjutsu/blob/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/README.md)
- [MIT license](https://github.com/donghaozhang/openjutsu/blob/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/LICENSE)
- [Package scripts and dependencies](https://github.com/donghaozhang/openjutsu/blob/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/package.json)
- [Simple workflow configuration](https://github.com/donghaozhang/openjutsu/blob/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/lib/simple.ts)
- [Object workflow configuration](https://github.com/donghaozhang/openjutsu/blob/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/lib/object.ts)
- [Model and run-name configuration](https://github.com/donghaozhang/openjutsu/blob/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/lib/model.ts)
- [Submission and upload lifecycle](https://github.com/donghaozhang/openjutsu/blob/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/lib/comfy.ts)
- [Preflight checks](https://github.com/donghaozhang/openjutsu/blob/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/lib/setup.ts)
- [Authentication, origins, upload handling](https://github.com/donghaozhang/openjutsu/blob/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/lib/http.ts)
- [Startup listener/password checks](https://github.com/donghaozhang/openjutsu/blob/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/instrumentation.ts)
- [Picture workflow documentation](https://github.com/donghaozhang/openjutsu/blob/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/workflows/picture/README.md)
- [Face graph handling](https://github.com/donghaozhang/openjutsu/blob/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/lib/face.ts)
- [Color graph handling](https://github.com/donghaozhang/openjutsu/blob/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/lib/color.ts)

External primary policy checked November 3, 2026:

- [InsightFace license policy](https://github.com/deepinsight/insightface#license): MIT source code is distinct from the pretrained-model policy; buffalo_l commercial licensing is addressed separately. This is a source-policy description, not a legal opinion or a full license audit of the generation stack.

## Local Verification

A temporary sparse checkout was used for inspection at the pinned commit. No packages, Python runtime, custom nodes, or model weights were installed. The repository's existing pure workflow tests ran directly with Node.js `v25.7.0`:

```sh
node --test --experimental-strip-types \
  test/simple.test.ts \
  test/advanced.test.ts \
  test/object.test.ts \
  test/face.test.ts \
  test/color.test.ts \
  test/model.test.ts \
  test/montage.test.ts
```

Result: 65 tests; 65 passed; 0 failed; 0 skipped. Tests read the repository's exported workflow graphs and check transformations, parameters, references, and timing calculations. They do not execute ComfyUI nodes or infer generated-video quality. This was not the complete `npm test` script, which also includes other tests and TypeScript checking. No production build, application startup, GPU generation, network/privacy audit, speed comparison, or commercial-service comparison was performed.

The article's hardware and render timings are explicitly author-reported. External model availability, weights, implementation, and licenses were not comprehensively audited. The normal-map picture path is distinguished from the SAM-mask swap path, and requested duration is distinguished from frame-grid-aligned output duration.

## Local Figures

The following JPEGs are copied byte-for-byte from `docs/media/` at the pinned commit and visually inspected. They are project-provided demonstration graphics, not screenshots or results from a local app run:

| Local file | Pinned source | Purpose |
|---|---|---|
| `advanced_swap.jpg` | [Source](https://raw.githubusercontent.com/donghaozhang/openjutsu/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/docs/media/advanced_swap.jpg) | Assigning photographs to different people |
| `object_swap.jpg` | [Source](https://raw.githubusercontent.com/donghaozhang/openjutsu/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/docs/media/object_swap.jpg) | Text-targeted object editing with sunglasses example |
| `relight.jpg` | [Source](https://raw.githubusercontent.com/donghaozhang/openjutsu/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/docs/media/relight.jpg) | Image preparation, relighting, video stage, seventeen looks |
| `fix_faces.jpg` | [Source](https://raw.githubusercontent.com/donghaozhang/openjutsu/7fe118bb5a61fcfac0148e1bfea3dd29884dbf26/docs/media/fix_faces.jpg) | Face redraw and compositing concept |

Attribution: Openjutsu / D3voz and project contributors. The repository's MIT notice is retained in [LICENSE.txt](LICENSE.txt). Included for project analysis; demonstration stills cannot establish temporal consistency, lip accuracy, or general output quality.
