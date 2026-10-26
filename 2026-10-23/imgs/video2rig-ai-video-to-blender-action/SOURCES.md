# Sources, Media, and Verification

Source release date: 2026-10-23. Research and execution date: 2026-10-26, Australia/Melbourne. The article folder follows the first public release commit rather than claiming a new October 26 release.

## Attribution and Snapshot

- User-provided repository: https://github.com/donghaozhang/video2rig
- GitHub identifies this as a fork of https://github.com/canitcode/video2rig.
- Inspected fork commit: `55d51b3b9685125a8ea27841d6af9523f6352aa1`.
- Commit timestamp: `2026-10-23T12:35:15Z` (October 23 in Melbourne).
- Message: `video2rig: an AI video of your own model -> an animation of your own rig (first public release, AGPL-3.0)`.
- Upstream `canitcode/video2rig` HEAD was checked through the GitHub API and matched the fork commit. This is a point-in-time observation, not a promise that the branches remain identical.
- Copyright/author attribution in the inspected project is Can It Code, 2026.
- Temporary source checkout: `/tmp/video2rig-article-20261026`; it remained clean after inspection and smoke checks.

## Inspected Primary Sources

- [README](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/README.md)
- [Tutorial](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/TUTORIAL.md)
- [Method](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/docs/HOW-IT-WORKS.md)
- [Video requirements and optional paid API workflow](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/docs/VIDEO.md)
- [Configuration](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/docs/CONFIG.md)
- [Command routing](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/__main__.py)
- [Reader network](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/reader/net.py), [preparation](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/reader/prepare.py), [training](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/reader/train.py), and [clip routing/cache](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/reader/road.py)
- [Fitting implementation](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/reader/fit.py), inspected selectively rather than line-by-line validation of the entire solver.
- [Consistency check](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/check.py), [quality report](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/report.py), and [rig representation](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/rig.py)
- [Blender importer](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/blender/import_motion.py)
- [Optional BytePlus generation helper](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/video2rig/generate.py), [requirements](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/requirements.txt), and [license](https://github.com/donghaozhang/video2rig/blob/55d51b3b9685125a8ea27841d6af9523f6352aa1/LICENSE).

## Independent Importer Smoke Check

The host had Blender 5.1.2. A temporary factory-startup scene contained three newly created bones and one cube; there was no user asset or existing project. Two bones received three motion samples, while the third retained a nonidentity start rotation. The middle root quaternion intentionally used the negative equivalent to exercise hemisphere correction. The actual upstream `blender/import_motion.py` was executed unchanged.

The review-owned, portable check is retained as [verify_import_smoke.py](verify_import_smoke.py). Run only with Blender, a fresh output directory, and an inspected checkout at the pinned revision:

```bash
/Applications/Blender.app/Contents/MacOS/Blender \
  --background --factory-startup \
  --python /Users/peter/Desktop/code/articles/2026-10-23/imgs/video2rig-ai-video-to-blender-action/verify_import_smoke.py \
  -- --repo /tmp/video2rig-article-20261026 \
  --output /tmp/video2rig-import-portable-20261026
```

Result: process exit 0 and `ARTICLE_IMPORT_SMOKE` status `passed`. Its machine-readable output is retained as [import-smoke-result.json](import-smoke-result.json).

Assertions covered:

- Scene time mapping to frames 1, 13, and 25 at 24 fps.
- Named Action creation, fake-user retention, eleven armature F-curves, and three keys per curve.
- Linear interpolation and positive consecutive quaternion dot products after sign correction.
- No keyed channels on the unfitted bone and preservation of its initial quaternion.
- Restoration of the prior keyframe interpolation preference.
- Final root local position `(1, 0, 0)`, prop world position `(2.5, 0, 0)`, scene end frame 25, and a saved `.blend`.

A second Blender process reopened that saved file and separately asserted the Action identity and root/prop positions at frame 25. It exited 0 and printed `ARTICLE_IMPORT_REOPEN passed`. The existing BlenderMCP add-on reported that it cannot start a server in background mode; no GUI/MCP server interaction was used, and the assertions completed normally.

The JSON result describes the import smoke check; the separate file-reopen check is documented here rather than added retroactively to the program's output. Temporary `.npz`/`.blend` files are not committed to the public article.

This is not an end-to-end animation test. No model weights, PyTorch/Transformers inference environment, trained reader, UniRig installation, video-generation request, real tracking/fitting, skin deformation test, render review, FBX/glTF export, or game-engine acceptance was performed. Host Python lacked the inference stack; bundled Python exposed NumPy but not SciPy, OpenCV, PyTorch, or Transformers. No inference dependency installation was attempted. Blender's own Python/NumPy sufficed for the importer test.

## Benchmark and Platform Boundaries

The approximately 3-degree per-bone median error, nine-character synthetic benchmark, older-route approximately 21-degree example, reader errors, and GPU timings are author-reported. The public tree did not include the referenced `dev/bench/suite.py` or complete benchmark clips/rigs. Those results were not independently reproduced and do not establish universal accuracy on AI-generated clips.

Main reader training explicitly selects CUDA; the normal reading route chooses CPU when requested or CUDA is unavailable. No Apple MPS route was identified there. A successful Blender importer on macOS does not validate training, perception, or performance on a Mac.

The `check` command is separate from `run`. It evaluates agreement for two orthographic panels; other cameras get a warning. The body threshold `.015` is a code heuristic, not a general reconstruction guarantee. Reader-mode artifacts are required for this check, even though ordinary `run` can fall back to the older tracker route without a trained reader.

## Retained Official Images

Unmodified copies from `docs/images/` at the pinned commit, all visually inspected:

| File | Dimensions | SHA-256 |
|---|---|---|
| [start-picture.jpg](https://raw.githubusercontent.com/donghaozhang/video2rig/55d51b3b9685125a8ea27841d6af9523f6352aa1/docs/images/start-picture.jpg) | 1600 x 900 | `1b8fa91c7de21bcae1964564ab891f04b051dd84ecfd45d1113cf75fe997b640` |
| [reader-joints.jpg](https://raw.githubusercontent.com/donghaozhang/video2rig/55d51b3b9685125a8ea27841d6af9523f6352aa1/docs/images/reader-joints.jpg) | 1600 x 900 | `8e637cd82d68d709bbc8ec09cb292a7c87aec0ee6b67229d41e6f8af60b2c37b` |
| [fit-over-video.jpg](https://raw.githubusercontent.com/donghaozhang/video2rig/55d51b3b9685125a8ea27841d6af9523f6352aa1/docs/images/fit-over-video.jpg) | 1600 x 422 | `a14e8dc3b6516ca7f7a5a0b75833d791c8d240be8ce8de9cc8900ee28c4e8938` |
| [video-frames.jpg](https://raw.githubusercontent.com/donghaozhang/video2rig/55d51b3b9685125a8ea27841d6af9523f6352aa1/docs/images/video-frames.jpg) | 1600 x 905 | `b24870e90a81421c590d33eb356d63d26aaa699b3d7a5dbabd0b312c2bab43e0` |
| [autorig-poses.jpg](https://raw.githubusercontent.com/donghaozhang/video2rig/55d51b3b9685125a8ea27841d6af9523f6352aa1/docs/images/autorig-poses.jpg) | 1080 x 1440 | `bf28595607243f6c2cfc48917153357fd0e974a6a2fdaed2b52af5c5e09ededa` |

These are author examples, not the synthetic importer test or a reconstruction performed here. Static frame sheets do not establish video playback quality. No remote video was downloaded or played. No QR codes, credentials, or private material were retained.

## Rights

Copyright (C) 2026 Can It Code. The exact upstream AGPL-3.0 license is retained as `UPSTREAM-LICENSE.txt`. The README describes commercial animation use as permitted; no legal clearance determination for a particular deployment is made here. DINOv2 and bundled tracker components are described under Apache 2.0, and separately installed UniRig under MIT. Their source/weight notices and asset/service terms remain independently applicable.

Example imagery and depicted character designs retain their respective rights. Inclusion for attributed project analysis does not replace those terms with this article repository's license, or authorize redistribution of unrelated characters, models, or generated assets.
