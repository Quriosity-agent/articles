import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

out = Path(sys.argv[sys.argv.index("--") + 1]).resolve()
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = 24
bpy.ops.import_scene.gltf(filepath=str(out / "crossing" / "mixamo_character.glb"))
rigs = [obj for obj in scene.objects if obj.type == "ARMATURE"]
meshes = [obj for obj in scene.objects if obj.type == "MESH" and obj.name.startswith("skinned_mesh_")]
actions = list(bpy.data.actions)
print("OBJECTS", [(obj.name, obj.type) for obj in scene.objects])
hand = next(obj for obj in meshes if "Hand proxy" in obj.name)
assert rigs and len(meshes) == 3 and actions
assert any(mod.type == "ARMATURE" for mod in hand.modifiers)


def center(frame):
    scene.frame_set(frame)
    obj = hand.evaluated_get(bpy.context.evaluated_depsgraph_get())
    return sum((obj.matrix_world @ v.co for v in obj.data.vertices), Vector()) / len(obj.data.vertices)


a, b, c = (center(f) for f in (0, 12, 24))
assert abs(a.x - .36) < .001 and b.x < .04 and (a - c).length < .001
print("READBACK", json.dumps({"meshes": len(meshes), "armatures": len(rigs),
      "actions": [{"name": ac.name, "frames": list(ac.frame_range)} for ac in actions],
      "hand_x_m": [a.x, b.x, c.x]}))

for obj in meshes:
    for poly in obj.data.polygons:
        poly.use_smooth = True
scene.world = bpy.data.worlds.new("Studio")
scene.world.color = (.26, .26, .26)
aim = Vector((.07, 0, 1.33))


def point_at(obj):
    obj.rotation_euler = (aim - obj.location).to_track_quat("-Z", "Y").to_euler()


bpy.ops.object.camera_add(location=(.08, -4, 1.42))
scene.camera = bpy.context.object
point_at(scene.camera)
scene.camera.data.type = "ORTHO"
scene.camera.data.ortho_scale = 1.0
for pos, power, size in [((-1, -3, 4), 300, 2), ((2, 1, 2), 140, 1.25)]:
    bpy.ops.object.light_add(type="AREA", location=pos)
    light = bpy.context.object
    light.data.energy, light.data.size = power, size
    point_at(light)
scene.render.engine = "CYCLES"
scene.cycles.samples = 12
scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = 560, 500
scene.render.resolution_percentage = 100
for frame in (0, 12):
    scene.frame_set(frame)
    scene.render.filepath = str(out / f"frame-{frame}.png")
    bpy.ops.render.render(write_still=True)
