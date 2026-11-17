# Sources and reproduction

- [Pinned repository](https://github.com/ky-zo/fable-butterfly/tree/3f717953b78c36c9d0dc61be04ac55267563c152) and [public deployment](https://butterfly.kyzo.io/), checked November 17, 2026 (Melbourne). The public repository has no standalone license file at the checked revision. The images here are editorial screenshots of the credited work, not a redistributed project.
- [Prompt transcript](https://github.com/ky-zo/fable-butterfly/blob/3f717953b78c36c9d0dc61be04ac55267563c152/PROMPTS.md): 42 numbered user entries; not a tool trace, billing record, or independent model attribution.
- [World contract](https://github.com/ky-zo/fable-butterfly/blob/3f717953b78c36c9d0dc61be04ac55267563c152/docs/WORLD_GUIDE.md), [narrative arc](https://github.com/ky-zo/fable-butterfly/blob/3f717953b78c36c9d0dc61be04ac55267563c152/docs/ARC.md), and [interaction notes](https://github.com/ky-zo/fable-butterfly/blob/3f717953b78c36c9d0dc61be04ac55267563c152/docs/PLAY.md). The final scroll controls take precedence over earlier experiments recorded in PLAY.md.

## Build and capture

Ran `npm ci --no-audit --no-fund` and `npm run build` in an isolated checkout on macOS, then served `dist/` with the Vite preview server on loopback port 5207. The built entry HTML matched the deployed entry SHA-256 `f8a5fb5c027a0a637134108f8dacbe55da0e0a9871344bef5396c875ebaaf262`. All nine built JavaScript chunks and the CSS file returned HTTP 200 from the deployment and matched local bytes. This comparison excludes fonts and social-media assets.

```sh
npm ci --no-audit --no-fund
npm run build
npm run preview -- --host 127.0.0.1 --port 5207 --strictPort
```

With that preview running, use the upstream scripts from a second terminal. The page uses WebGL2; captures used headless Google Chrome with ANGLE Metal on Apple Silicon.

```sh
out="$(mktemp -d)"
export HL_URL=http://127.0.0.1:5207
node tools/scroll.mjs conservatory --input wheel --out "$out/desk"
node tools/scroll.mjs conservatory --input touch --out "$out/touch"
for world in conservatory latent corpus descent loom mirror; do
  node tools/shot.mjs "$world" --p 0.38 --frames 12 --size 960x540 --out "$out/$world.png"
done
```

- `conservatory.webp` and `touch-start.webp`: the desktop (1280×720) and touch-emulated portrait (390×844 CSS pixels, DPR 2) start captures from the scroll tests.
- `six-worlds.webp`: six screenshots at progress 0.38 in high quality, 12 stepped frames before capture, arranged in chapter order. These are re-rendered from the source, not frames cut from the social video.
- Test results: 22/22 desktop and 23/23 touch assertions passed. At settled progress 0.3744 (desktop) and 0.3608 (touch emulation), the camera vectors and lens parameters did not change while the butterfly moved 16.7 cm and 16.5 cm off its path respectively. The tested transition was Conservatory to Latent; all other chapters were spot-rendered, not played through. No physical phone, audio-quality or performance matrix testing.
