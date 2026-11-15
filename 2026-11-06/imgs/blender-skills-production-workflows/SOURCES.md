# Sources and test notes

Reviewed on 2026-11-15 (Australia/Melbourne). The article directory uses the source snapshot's date, not a release date.

- [Submitted fork](https://github.com/donghaozhang/blender-skills/tree/904f095d8f36a6e72adaebb08d07f884a074743d) and [original upstream at the same revision](https://github.com/arjun988/blender-skills/tree/904f095d8f36a6e72adaebb08d07f884a074743d).
- Inventory: 94 `SKILL.md` files and 175 files under `references/` in `.claude/skills`. Recursive diff against `.cursor/skills` produced no differences.
- [MCP for Blender](https://github.com/ahujasid/mcp-for-blender) is an independent project. The local test below did not install or call it.

## Reproduce the local Blender test

[fixture.py](fixture.py) builds the original prop and produces `relay.png`, `relay.blend`, and two GLBs in a scratch directory. The PNG is a render of the source scene, not a re-render of either imported GLB. The script resets its Blender scene to empty before each import. Use background mode, not a session containing unsaved work.

```sh
out="$(mktemp -d)"
/Applications/Blender.app/Contents/MacOS/blender --background --factory-startup \
  --python-exit-code 1 --python fixture.py -- "$out"
```

Tested on macOS with Blender 5.1.2 (build hash `ec6e62d40fa9`). Render: Cycles on CPU, 840 × 560 pixels, 12 samples with denoising. Readback counted the triangulated mesh faces after import.

| File | Meshes | Triangles | Material names |
|---|---:|---:|---|
| `relay-base.glb` | 7 | 84 | MAT_Graphite, MAT_Indicator, MAT_Sage |
| `relay-beveled.glb` | 7 | 1,316 | MAT_Graphite, MAT_Indicator, MAT_Sage |

Both imports retained `SM_Relay_Housing`, `SM_Relay_Panel`, `SM_Relay_Indicator`, and `SM_Relay_Vent_01` through `SM_Relay_Vent_04`. Neither retained staging objects. This checks geometry counts and names in Blender, not appearance parity, engine compatibility, or the behavior of the agent playbooks.
