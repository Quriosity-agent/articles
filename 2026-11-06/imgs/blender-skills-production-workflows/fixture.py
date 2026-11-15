import json
from pathlib import Path
import sys

import bpy
from mathutils import Vector

out = Path(sys.argv[sys.argv.index("--") + 1])
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

def material(name, color, metal=0.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metal
    bsdf.inputs["Roughness"].default_value = 0.36
    return mat

def box(name, size, location, mat, bevel):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name, obj.dimensions = name, size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(mat)
    if bevel:
        mod = obj.modifiers.new("Edge bevel", "BEVEL")
        mod.width, mod.segments = bevel, 3
    return obj

sage = material("MAT_Sage", (0.13, 0.38, 0.30), 0.38)
graphite = material("MAT_Graphite", (0.042, 0.055, 0.06), 0.55)
orange = material("MAT_Indicator", (0.91, 0.23, 0.035))
props = [
    box("SM_Relay_Housing", (2, 1.24, 0.84), (0, 0, 0.5), sage, 0.075),
    box("SM_Relay_Panel", (1.65, 0.08, 0.55), (0, -0.63, 0.52), graphite, 0.035),
    box("SM_Relay_Indicator", (0.46, 0.05, 0.12), (-0.46, -0.685, 0.58), orange, 0.02),
]
for i in range(4):
    props.append(box(f"SM_Relay_Vent_{i+1:02}", (0.085, 0.05, 0.27),
                     (0.22 + i*0.13, -0.686, 0.52), sage, 0.015))
bpy.ops.object.select_all(action="DESELECT")
for obj in props:
    obj.select_set(True)
for variant, apply_modifiers in [("base", False), ("beveled", True)]:
    bpy.ops.export_scene.gltf(filepath=str(out / f"relay-{variant}.glb"),
                              use_selection=True, export_format="GLB", export_apply=apply_modifiers)
box("Stage", (200, 200, 0.1), (0, 0, 0), material("MAT_Stage", (0.36, 0.40, 0.42)), 0)

def aim(obj):
    obj.rotation_euler = (Vector((0, 0, 0.45)) - obj.location).to_track_quat("-Z", "Y").to_euler()

for name, pos, energy, size in [
    ("Key", (1, -4, 5), 680, 4),
    ("Fill", (-4, -1, 2), 210, 3),
    ("Rim", (0, 4, 5), 520, 3),
]:
    bpy.ops.object.light_add(type="AREA", location=pos)
    light = bpy.context.object
    light.name, light.data.energy, light.data.size = name, energy, size
    aim(light)
bpy.ops.object.camera_add(location=(3.15, -5.4, 3.05))
scene.camera = bpy.context.object
scene.camera.data.type, scene.camera.data.ortho_scale = "ORTHO", 3.7
aim(scene.camera)
scene.render.engine = "CYCLES"
scene.cycles.device = "CPU"
scene.cycles.samples = 12
scene.cycles.use_denoising = True
scene.render.resolution_x, scene.render.resolution_y = 840, 560
scene.render.resolution_percentage = 100
scene.render.filepath = str(out / "relay.png")
bpy.ops.wm.save_as_mainfile(filepath=str(out / "relay.blend"))
bpy.ops.render.render(write_still=True)

expected = {obj.name for obj in props}
counts = {}
for variant in ("base", "beveled"):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=str(out / f"relay-{variant}.glb"))
    objects = list(bpy.context.scene.objects)
    assert all(obj.type == "MESH" for obj in objects)
    assert {obj.name for obj in objects} == expected
    materials = {m.name for obj in objects for m in obj.data.materials}
    assert materials == {"MAT_Graphite", "MAT_Indicator", "MAT_Sage"}
    for obj in objects:
        obj.data.calc_loop_triangles()
    counts[variant] = sum(len(obj.data.loop_triangles) for obj in objects)
    print("READBACK", json.dumps({"variant": variant, "meshes": len(objects),
          "triangles": counts[variant], "materials": sorted(materials), "names": sorted(expected)}))
assert counts["base"] == 84 and counts["beveled"] > counts["base"]
