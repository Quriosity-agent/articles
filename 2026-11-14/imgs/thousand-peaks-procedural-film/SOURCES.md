# Sources and reproduction

- **Upstream:** [0xCodez/thousand-peaks](https://github.com/0xCodez/thousand-peaks/tree/09a8c7e86b31ea7b1446b096de542c7d1994e7b2), with the [submitted fork](https://github.com/donghaozhang/thousand-peaks/tree/09a8c7e86b31ea7b1446b096de542c7d1994e7b2) checked out at the same revision. [v1.0](https://github.com/0xCodez/thousand-peaks/releases/tag/v1.0) was published on 2026-11-14 UTC. Review performed on 2026-11-15 in Melbourne.
- **Images:** Locally rendered from the original project, credited to 0xCodez / Beyond Dev. [Upstream license](UPSTREAM-LICENSE.txt). `key-25.jpg` is the authored camera at 25 s; `shifted-25.jpg` uses the alternate camera below at the same time; `shot-sheet.jpg` uses six authored-camera frames with timestamps added by the upstream tool.
- **Build check:** Local output and the committed HTML matched the [release asset metadata](https://api.github.com/repos/0xCodez/thousand-peaks/releases/tags/v1.0): 1,668,744 bytes, SHA-256 `f50d6cf11c808ef3342b467cd360195f346e995601d90fb9c0bf9f43d2419509`.
- **Environment:** Apple M4 Pro, macOS, Chrome 157.0.8103.51, ANGLE Metal, Node 25.7.0, FFmpeg 8.1. This is not a live frame-rate benchmark or a mobile test.

## Reproduce in a disposable upstream checkout

```sh
out="$(mktemp -d)"
npm install --ignore-scripts --no-audit --no-fund --package-lock=false
node tools/build.mjs --out "$out/rebuilt.html"
shasum -a 256 "$out/rebuilt.html" dist/thousand-peaks.html
node tools/shot.mjs --html "$out/rebuilt.html" --t 3.2,25,48.5,60.6,72,85 \
  --size 1280x720 --sheet --cols 3 --tile 640 --out "$out/shot-sheet.jpg"
node tools/shot.mjs --html "$out/rebuilt.html" --t 25 --size 1280x720 \
  --cam "-43,78,176,-4,86,60,48" --out "$out/shifted-25.jpg"
node tools/audio_probe.mjs --html "$out/rebuilt.html" --wav dist/score.wav
node tools/record.mjs --html "$out/rebuilt.html" --from 24 --to 26 \
  --fps 30 --size 960x540 --out "$out/excerpt.mp4"
ffprobe -v error -count_frames -show_streams "$out/excerpt.mp4"
ffmpeg -v error -xerror -i "$out/excerpt.mp4" -f null -
```

The WAV was 90 s, stereo PCM, 44.1 kHz. The excerpt had 60 H.264 frames and stereo AAC, with no decode errors. The full 1080p60 release MP4 was not reproduced or used as input.

## Offline and return-seek probe

Run the accompanying [probe.mjs](probe.mjs) from a copy next to the upstream `package.json` so Node can resolve `puppeteer-core`.

```sh
node probe.mjs "$out/rebuilt.html" "$out/probe"
ffmpeg -i "$out/probe/first-25.png" -i "$out/probe/returned-25.png" -lavfi psnr -f null -
```

The probe uses file URLs in a fresh headless Chrome page with offline mode enabled. No HTTP(S) requests or page errors were observed. The two adjacent captures at 25 s were byte-identical, but after rendering 85 s the returned shot at 25 s differed (58.77 dB average PSNR on RGB). This is a same-machine PNG comparison, not a claim about every frame or the reason for the difference. The probe also exercises the documented lake-level camera; the shifted image published in the article is the separate, usable view from the command above.
