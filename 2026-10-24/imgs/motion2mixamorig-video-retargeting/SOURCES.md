# Sources and reproduction

- [Upstream release v0.1.8](https://github.com/MaxLiu22/Motion2MixamoRig/releases/tag/v0.1.8) and [submitted fork snapshot](https://github.com/donghaozhang/Motion2MixamoRig/tree/f05a718188026b06e7ee64b47bab077970444b19) both reference commit `f05a718188026b06e7ee64b47bab077970444b19`. Release dated 2026-10-24; reviewed 2026-11-17 (Melbourne). The macOS arm64 zip was the only binary asset on the upstream release. The snapshot's packaging command built and validated a macOS arm64 extension zip in a disposable checkout. It was not installed.
- [Official upstream demo video](https://github.com/MaxLiu22/Motion2MixamoRig/blob/v0.1.8/docs/assets/demo.mp4). The figures in this review do **not** come from that video or a Mixamo character.
- [GVHMR](https://github.com/zju3dv/GVHMR), [HaMeR](https://geopavlakos.github.io/hamer/), [SMPL-X](https://smpl-x.is.tue.mpg.de/), and the repository's [dependency notice](https://github.com/MaxLiu22/Motion2MixamoRig/blob/v0.1.8/NOTICE.md) are primary sources. Apache-2.0 for this project's own code does not override upstream terms.

## Synthetic downstream check

[fixture.py](fixture.py) creates an in-memory three-bone test asset with three closed meshes and one bone influence per vertex. It calls the unmodified upstream `write_glb` and `diagnose_run` functions. The control rotates nothing; the crossing clip animates only the hand proxy around a pivot. [readback.py](readback.py) imports that GLB into a fresh Blender scene, measures the evaluated hand mesh, and renders frames 0 and 12. The published WebP combines those renders side by side.

| Report at 1 cm threshold | Control | Deliberate crossing |
|---|---:|---:|
| Sampled frames | 25 | 25 |
| Detected part pairs | 0 | 1, head and left hand |
| Flagged frames | None | 9 through 15, worst at 12 |
| Estimated peak depth | 0 cm | 12.86 cm |

Blender 5.1.2 imported the crossing fixture as an armature, three skinned meshes, and the `mixamo_clip` action spanning frames 0–24 at 24 fps. It also imported a separate `Icosphere` bone-display helper, excluded from the mesh count. Evaluated hand-centroid X at frames 0, 12 and 24 was approximately 0.360 m, 0.024 m, and 0.360 m. The heuristic depth is not a ground-truth geometric measurement or an estimate of mocap accuracy.

Run these commands from this notes directory in a scratch environment:

```sh
out="$(mktemp -d)"
git clone --depth 1 --branch v0.1.8 https://github.com/MaxLiu22/Motion2MixamoRig "$out/src"
uv venv --python 3.12 "$out/venv"
uv pip install --python "$out/venv/bin/python" numpy==2.5.5 scipy==1.18.1 trimesh==5.2.1
PYTHONPATH="$out/src" "$out/venv/bin/python" fixture.py "$out/runs"
/Applications/Blender.app/Contents/MacOS/blender --background --factory-startup \
  --python-exit-code 1 --python readback.py -- "$out/runs"
```

This probe does not call video or photo inference, load an FBX, exercise the retarget solver or foot locking, check a real person's finger motion, or test the Blender extension UI. It uses no credentials, inference checkpoints, SMPL-X/MANO files, or Adobe assets.
