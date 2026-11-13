# Sources and Verification

Reviewed November 13, 2026 in Melbourne. The article date follows the reviewed source snapshot, not the release tag.

- [Requested fork](https://github.com/donghaozhang/music-skill) and [upstream](https://github.com/owoevan-dev/music-skill) both returned `229892c0af07a98e14edcd283ba7e201c6a67eb7` for `refs/heads/main`. The source commit reports November 12 at 13:47:03 +08:00.
- [v0.6.0](https://github.com/owoevan-dev/music-skill/releases/tag/v0.6.0) resolves to `a14504fee9dbd33956b2d59d580ca16e760899f8`. The reviewed `main` is not the release tag; its documentation and example set include later changes.
- [Skill instructions](https://github.com/owoevan-dev/music-skill/blob/229892c/skills/music-production/SKILL.md), [render/cache source](https://github.com/owoevan-dev/music-skill/blob/229892c/skills/music-production/scripts/musiclib/render.py), [before/after example](https://github.com/owoevan-dev/music-skill/tree/229892c/examples/before-after), and [third-party notices](https://github.com/owoevan-dev/music-skill/blob/229892c/THIRD_PARTY.md) support the architecture, upstream A/B observations, and license distinctions.

## Local Assets

| File | Provenance |
|---|---|
| `cairnfire-piano-roll.png` | [Upstream visualization](https://github.com/owoevan-dev/music-skill/blob/229892c/docs/images/cairnfire.png), copied unchanged; visually inspected, 1920 × 1080 PNG. Derived from the upstream Cairnfire project; not a local DAW screenshot. |
| `porch-light-before.mid` | Local MIDI export of the original eight-bar Porch Light project from the published example script. |
| `porch-light-after.mid` | Local MIDI export after changing the flute note `flute_b005_n000` from pitch 73 to 76. |

Upstream dedicates the Porch Light composition to CC0 and uses MIT for its source code and project. Its Windows audio comparisons are not local render results. The project identifies the compositions and recordings on [examples-4](https://github.com/owoevan-dev/music-skill/releases/tag/examples-4) as CC0. Neither a sample bank nor an upstream executable is redistributed here.

## Reproduction

Temporary macOS arm64 venv: Python 3.12.12, NumPy 2.1.2 from the pinned requirements, pytest 9.2.0 and PyYAML 6.0.3. From the reviewed checkout, with that environment active:

```sh
python -m pip install --only-binary=:all: -r skills/music-production/requirements.txt
python -m pip install --only-binary=:all: pytest==9.2.0 PyYAML==6.0.3
env -u MUSIC_SKILL_CONFIG python -m pytest -q tests

work=$(mktemp -d)
cli=skills/music-production/scripts/studio.py
python examples/before-after/porch_light.py "$work"
python "$cli" revise "$work/song.json" --track flute --note flute_b005_n000 \
  --pitch 76 --output "$work/song_r2.json"
python "$cli" export-midi "$work/song.json" --output "$work/before.mid"
python "$cli" export-midi "$work/song_r2.json" --output "$work/after.mid"
python "$cli" inspect-midi "$work/before.mid"
python "$cli" inspect-midi "$work/after.mid"
```

- `23 passed`; the no-config self-check test asserts 122 internal checks. The seven compose-script tests compare structured project data (excluding the documented extra history entry in the Skybutton rerun); they do not render the audio.
- Both MIDI files were format 1, 960 ticks per quarter note, five tracks, 157 notes, zero unclosed notes and zero stray note-offs. Before SHA-256: `60712b4f8adb8e49d3d13d03812266aa88a7426b74aec06ccea69823be2617d3`. After: `03ec5cc4f2da576746d0430dacf0db72f9ed30560d18cc70799bc9472a7c1485`.
- Downloaded [the upstream Skybutton Speedway MP3](https://github.com/owoevan-dev/music-skill/releases/download/examples-4/skybutton-speedway.mp3) for inspection. SHA-256 `46c21f51733fae57b5aa9db3da0114bf0cdf2008cb04ff70a89d8a4984492347`. `ffprobe` reported MP3, 48,000 Hz, two channels, 91.000 seconds. `ffmpeg -v error -xerror -i skybutton-speedway.mp3 -map 0:a:0 -f null -` completed without error. The original release remains the listening link; no MP3 copy is committed.
- No configured local synth/FluidSynth render, audio A/B, loop-seam measurement, DAW import, new composition benchmark, or musical listening verdict. No agent install, full bank setup, or upload.
