# Source and Reproduction Notes

Reviewed 2026-11-25, Australia/Melbourne.

- Source: [ChetasLua/noroi-iwai](https://github.com/ChetasLua/noroi-iwai/tree/edd3b89753d8f17353ec17f8738b39a781667c6b).
- Commit: `edd3b89753d8f17353ec17f8738b39a781667c6b`.
- Images were rendered from the unmodified shot code, not downloaded from a promotional video. Character/IP attribution remains with the source project and Gege Akutami. This note grants no license to the underlying work. No LICENSE file was present in the reviewed snapshot.
- Local test environment: macOS; Python 3.12.12; Node 25.7.0; NumPy 2.5.5; OpenCV headless 5.1.0.95; SciPy 1.18.1; Pillow 13.0.0; Numba 0.68.1; PyCairo 1.29.2; SoundFile 0.14.0. An existing Homebrew Cairo installation was reused to build PyCairo in a disposable virtual environment. This was not a fresh-machine dependency test.
- The renderer's `.mm/env/bin/python`, `ffmpeg` and `ffprobe` paths were supplied through local environment symlinks. No tracked source file was changed. Empty `cache`, `out`, `qa` and `dist` directories were prepared in the sparse checkout.

## Preserved Images

All five are 960 x 540 JPEGs from the source's full 1920 x 1080 frame, including `comp.finish` and `comp.to8`, resized by its `tools/still.py --scale 0.5` option.

| Article asset | Shot/local frame | Command |
| --- | --- | --- |
| `b1-hill-f36.jpg` | b1 / 36 | `python tools/still.py b1 36 54 --scale 0.5 --out <scratch-output>` |
| `d4-windup-f40.jpg` | d4 / 40 | `python tools/still.py d4 40 54 55 --scale 0.5 --out <scratch-output>` |
| `d4-impact-f54.jpg` | d4 / 54 | Same command as above |
| `d4-impact-f55.jpg` | d4 / 55 | Same command as above |
| `g4-ink-f90.jpg` | g4 / 90 | `python tools/still.py g4 90 --scale 0.5 --out <scratch-output>` |

The extra b1 frame 54 was inspected as a generated file but is not included in the article assets. Still renders alone do not establish motion quality.

## Bounded Verification

1. `python tools/render.py d4 --range 36:48 --jobs 2 --out <scratch>/d4-36-47.mkv` produced H.264, 1920 x 1080, 24 fps, 12 frames and 0.5 seconds. `ffprobe -count_frames` checked the frame count; `ffmpeg -v error -i <clip> -f null -` completed without decode errors. This partial shot is not a full film.
2. `node audio/voice.mjs --lead <scratch>/lead-b1.wav b1` ran twice. Both outputs were 48 kHz, PCM signed 16-bit, mono, 211,200 samples / 4.4 seconds. SHA-256 for each: `83b808978066c4497e1823c4ac5d8fe4877d76a3c0fa988ac268e6d5fb96a362`. Decoded peak was 0.7999878; samples were finite and non-silent. The audio is not republished here. These measurements do not establish perceptual singing quality.
3. `python tools/events.py` collected 694 events from 37 actual shot event lists, with zero draft-fallback shots. Mapping and mixing every event were not tested.
4. Assertions checked 37 shot modules, 37 timeline entries, contiguous timing, 2,736 total frames, 114 seconds and 76 bars at 1.5 seconds each. Python files were syntax-parsed. These are targeted checks, not an upstream test-suite pass.
5. Imported `shots.e4.rnd` and `shots.h2.rnd` in separate subprocesses with `PYTHONHASHSEED=1` and `77`; five random values from each using the same probe arguments matched. No complete e4/h2 frame comparison was performed.
6. `node audio/band.mjs check` ran and reported 87 non-chord tones longer than 0.3 seconds. This is a musical diagnostic, not a failed-test count or proof that the notes are mistakes. No full band, choir or final mix was rendered.

No model API was called during these probes. No complete 114-second movie was assembled or reviewed, no subjective listening claim is made, and no source project binaries, caches or dependencies are included in this articles commit.
