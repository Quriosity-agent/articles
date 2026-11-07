# Sources, Image Credits, and Local Verification

Reviewed November 8, 2026 (Australia/Melbourne).

- Requested fork: https://github.com/donghaozhang/vork
- Canonical repository: https://github.com/voyager-so/vork
- Product page: https://voyager.so/vork
- [Release metadata](https://api.github.com/repos/voyager-so/vork/releases/latest) gave `2026-11-06T14:37:36Z`, November 7 in Melbourne. The public `v0.1.0` tag resolves to `09dbd97a8601dbbd5870dc5a2856aa59d7ea21dd`.
- `git ls-remote` found both `main` heads at `44188baab29ad1c174c9e949c982d9edb45308fc`. Documentation and stills are pinned to that source revision. The benchmark report identifies `81ae2b0755bb696fc3e904744b76a103feded023` for its frozen draft/final results and distinguishes carried-forward numbers.

## Asset Provenance

| Local asset | Provenance |
|---|---|
| `custom-program.png` | Local Metal render of `examples/programs.json` in the official arm64 archive; uses bundled checker, stripe program, and brick texture. 480 × 270. |
| `first-final.png` | Local Metal final-profile color output from [upstream first-scene.json](https://github.com/voyager-so/vork/blob/44188ba/examples/first-scene.json). 640 × 480. |
| `first-final.view_normal.png` | View-space normals from the same command and frame as `first-final.png`. 640 × 480. |
| `seed-2-tracked.jpg` | [Voyager demonstration still](https://github.com/voyager-so/vork/blob/44188ba/docs/images/seed-2-tracked.jpg), tracked camera and approximate proxy geometry. Copied unchanged, 1280 × 720. |
| `seed-3-final.jpg` | [Voyager demonstration still](https://github.com/voyager-so/vork/blob/44188ba/docs/images/seed-3-final.jpg), later relighting and composite. Copied unchanged, 1280 × 720. |

Both seed stills use the plate **Tired Woman Sleeping on the Table**, Ron Lach / Pexels, [video 7983323](https://www.pexels.com/video/tired-woman-sleeping-on-the-table-7983323/), modified by the demonstration authors under the [Pexels License](https://www.pexels.com/license/). No endorsement by the performer is implied. [Upstream recipe and credits](https://github.com/voyager-so/vork/tree/44188ba/examples/vfx-artifact). No scene binaries, input video, or model weights are redistributed here.

## Local Smoke Test

- Hardware: Apple M4 Pro Mac mini, 48 GB. System: macOS 26.6.2 (`25G83`). Adapter diagnostics: Apple M4 Pro, Metal.
- Archive: `vork-0.1.0-darwin-arm64.tar.gz`, 140,796,041 bytes, from [official release assets](https://github.com/voyager-so/vork/releases/tag/v0.1.0). SHA-256 `677d1aad60ca86a6e8c480f623c2773658cc30d68a98a42ea11fc3d9c39f1d51`, matched the release's `SHA256SUMS`.
- `codesign --verify` passed for the extracted CLI, which is not a notarization check. Binary identity as printed: `vork 0.1.0 (commit 558c214f96e1; API v2)`. No assertion that the package was rebuilt from the public tag. No installer, global PATH edit, or cloud GPU was used.

With the release archive extracted to `runtime/` and the pinned source in `source/`, from their common scratch directory:

```sh
vork_local() {
  env HOME="$PWD/runtime-home" XDG_CACHE_HOME="$PWD/runtime-cache" \
    CFFIXED_USER_HOME="$PWD/runtime-home" runtime/vork "$@"
}
vork_local render source/examples/first-scene.json --profile std/previs \
  --diagnostics --out first-previs.png
vork_local render source/examples/first-scene.json --profile std/final \
  --channels color,depth,view_normal,object_index,camera --diagnostics --out first-final.png
vork_local render runtime/examples/programs.json --profile std/previs \
  --set resolution=480x270 --diagnostics --out custom-program.png
vork_local render runtime/examples/animated-light.json --profile std/previs \
  --diagnostics --out animated-light.mp4
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,avg_frame_rate,nb_frames,duration \
  -of json animated-light.mp4
ffmpeg -v error -xerror -i animated-light.mp4 -map 0:v:0 -f null -
ffmpeg -v error -i animated-light.mp4 -map 0:v:0 -f framemd5 -
```

The CLI wrote color, depth, normals, object-index and camera/metadata outputs as requested. PNG headers confirmed the 16-bit depth and object-index channels; the metadata mapped two pass IDs to scene nodes. The color and normal renders and custom-material image were visually inspected. `ffprobe` confirmed H.264, 320 × 180, 12 fps, 0.5 seconds, six frames. Full decode completed and frame hashes were all distinct. These are functional checks, not timings for comparing products. No local Blender comparison, large shot, VFX plate preparation, volume, motion-vector, EXR, or ProRes validation was performed.
