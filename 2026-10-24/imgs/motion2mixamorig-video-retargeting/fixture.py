import json
from pathlib import Path
import sys

import numpy as np
import trimesh
from scipy.spatial.transform import Rotation

from motion2mixamorig.diagnose import diagnose_run
from motion2mixamorig.mixamo.gltf import write_glb
from motion2mixamorig.mixamo.kinematics import MixamoBone, MixamoRig, mat4
from motion2mixamorig.mixamo.skinned_mesh import SkinnedMesh, YBotAsset


def main(out):
    root, head, wrist = "mixamorig:Hips", "mixamorig:Head", "mixamorig:LeftHand"
    order = [root, head, wrist]
    neutral = np.eye(3)
    centers = {root: [0, 100, 0], head: [0, 155, 0], wrist: [18, 155, 0]}
    bones = {}
    for i, name in enumerate(order):
        pos = np.array(centers[name], dtype=float)
        local = pos - centers[root] if i else pos
        bones[name] = MixamoBone(
            name, root if i else None, [] if i else order[1:], neutral,
            local, mat4(neutral, pos), mat4(neutral, local), np.zeros(3),
        )
    rig = MixamoRig(bones, order, 0.01, Path("synthetic"))
    inverse_bind = np.stack([np.linalg.inv(bones[n].rest_world) for n in order])
    sphere = trimesh.creation.icosphere(subdivisions=3)
    meshes = []
    for i, (name, part, position, size, color) in enumerate([
        ("Torso", root, [0, 115, 0], [19, 25, 11], [0.03, 0.18, 0.26]),
        ("Head", head, [0, 155, 0], [15, 16, 13], [0.12, 0.49, 0.43]),
        ("Hand proxy", wrist, [36, 155, 0], [9, 8, 9], [0.81, 0.25, 0.04]),
    ]):
        assert order[i] == part
        vertices = sphere.vertices * np.array(size) + position
        weights = np.zeros((len(vertices), len(order)))
        weights[:, i] = 1
        meshes.append(SkinnedMesh(name, vertices, sphere.faces, weights, inverse_bind, color))
    asset = YBotAsset(rig, meshes)
    for variant in ("clear", "crossing"):
        run = out / variant
        angles = [0] * 25 if variant == "clear" else np.r_[np.linspace(0, 150, 13), np.linspace(150, 0, 13)[1:]]
        frames = [{wrist: Rotation.from_euler("z", a, degrees=True).as_matrix()} for a in angles]
        write_glb(run / "mixamo_character.glb", asset, frames, [np.array(centers[root])] * len(frames), 24.0)
        result = diagnose_run(run, verbose=False)
        if variant == "clear":
            assert result["issues"] == []
        else:
            assert len(result["issues"]) == 1
            issue = result["issues"][0]
            assert set(issue["parts"]) == {"head", "left_hand"}
            assert issue["worst_frame"] == 12 and not issue["also_in_rest_pose"]
        print(variant, json.dumps(result["issues"]))


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve())
