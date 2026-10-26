"""Synthetic Blender importer smoke check; no video or trained reader involved."""
import argparse
import json
import math
from pathlib import Path
import runpy
import sys

import bpy
import numpy as np
from mathutils import Quaternion


argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
parser = argparse.ArgumentParser()
parser.add_argument('--repo', required=True)
parser.add_argument('--output', required=True)
args = parser.parse_args(argv)
source = Path(args.repo).resolve() / 'blender' / 'import_motion.py'
work = Path(args.output).resolve()
work.mkdir(parents=True, exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.object.armature_add()
arm = bpy.context.object
arm.name = 'ArticleRig'
bpy.ops.object.mode_set(mode='EDIT')
root = arm.data.edit_bones[0]
root.name = 'Root'
root.head, root.tail = (0, 0, 0), (0, 1, 0)
child = arm.data.edit_bones.new('Child')
child.head, child.tail, child.parent = (0, 1, 0), (0, 2, 0), root
fixed = arm.data.edit_bones.new('Unfitted')
fixed.head, fixed.tail, fixed.parent = (0, 2, 0), (0, 3, 0), child
bpy.ops.object.mode_set(mode='OBJECT')
arm.pose.bones['Unfitted'].rotation_mode = 'QUATERNION'
fixed_q = Quaternion((1, 0, 0), .2)
arm.pose.bones['Unfitted'].rotation_quaternion = fixed_q
bpy.ops.mesh.primitive_cube_add(size=.1, location=(2, 0, 0))
prop = bpy.context.object
prop.name = 'ArticleProp'
scene = bpy.context.scene
scene.frame_start, scene.frame_end = 1, 1
scene.render.fps, scene.render.fps_base = 24, 1
quats = np.zeros((3, 2, 4))
quats[:, :, 0] = 1
quats[1, 0] = [-math.cos(.2), 0, 0, -math.sin(.2)]
quats[2, 0] = [math.cos(.4), 0, 0, math.sin(.4)]
matrices = np.tile(np.eye(4), (3, 1, 1, 1))
matrices[:, 0, 0, 3] = [0, .25, .5]
motion = work / 'synthetic.npz'
np.savez(motion, times=[0, .5, 1], bones=['Root', 'Child'], root='Root',
         quaternions=quats, root_location=[[0, 0, 0], [.5, 0, 0], [1, 0, 0]],
         props=['ArticleProp'], armature_world=np.eye(4), prop_matrices=matrices)
was = bpy.context.preferences.edit.keyframe_new_interpolation_type
sys.argv = ['blender', '--', '--motion', str(motion), '--armature', arm.name,
            '--action', 'ArticleMotion', '--save', str(work / 'imported.blend')]
ns = runpy.run_path(str(source))
act = arm.animation_data.action
curves = ns['action_fcurves'](act)
assert act.name == 'ArticleMotion' and act.use_fake_user
assert len(curves) == 11, len(curves)
assert all([round(p.co.x, 6) for p in fc.keyframe_points] == [1, 13, 25] for fc in curves)
assert all(p.interpolation == 'LINEAR' for fc in curves for p in fc.keyframe_points)
qc = sorted([fc for fc in curves if fc.data_path == 'pose.bones["Root"].rotation_quaternion'],
            key=lambda fc: fc.array_index)
q = np.array([[fc.keyframe_points[i].co.y for fc in qc] for i in range(3)])
assert np.all((q[:-1] * q[1:]).sum(1) > 0)
assert all('Unfitted' not in fc.data_path for fc in curves)
assert np.allclose(tuple(arm.pose.bones['Unfitted'].rotation_quaternion), tuple(fixed_q))
assert bpy.context.preferences.edit.keyframe_new_interpolation_type == was
scene.frame_set(25)
assert np.allclose(tuple(arm.pose.bones['Root'].location), [1, 0, 0])
assert np.allclose(tuple(prop.location), [2.5, 0, 0])
assert scene.frame_end == 25
assert (work / 'imported.blend').exists()
report = dict(status='passed', blender=bpy.app.version_string, frames=[1, 13, 25],
              armature_fcurves=len(curves), root_translation=True, prop_translation=True,
              quaternion_hemisphere=True, linear_interpolation=True, unfitted_preserved=True,
              preferences_restored=True, blend_saved=True,
              scope='Synthetic importer only; no perception, fitting, skinning, export or visual QA')
(work / 'result.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print('ARTICLE_IMPORT_SMOKE', json.dumps(report))
