# Six Audio Sources for AI Video: Evidence Record

Reviewed October 27, 2026, Australia/Melbourne. Filed October 26 to match the source post date.

## Source Post

- URL: https://x.com/3three_AI/status/2114545802211103044
- Author: 三个三 / @3three_AI.
- Read the complete post through the in-app browser after the search browser returned HTTP 403. No login was performed.
- Visible date: October 26, 2026. Status-ID timestamp calculation: `2026-10-26T02:33:00.265Z`; do not interpret the browser's displayed clock as UTC.
- Six resolved destinations: https://pixabay.com/music/ ; https://freesound.org/ ; https://soundeffect-lab.info/ ; https://mixkit.co/free-sound-effects/transition/ ; https://elevenlabs.io/sound-effects ; https://github.com/Leonxlnx/earshot .
- Original post says Pixabay 300k+, Freesound 730k, Sound Effect Lab 2000+, and earshot 201. Current official pages show Pixabay 300k+, Freesound 737,948, and the inspected earshot bank contains 252 entries. No independent total count was made for Sound Effect Lab.
- Post image observed at `https://pbs.twimg.com/media/HVdNqCfb0AAV2yF?format=webp&name=small`. Visually inspected; it matches the higher-resolution upstream earshot montage preserved below. The small duplicate is not committed. Opening the photo viewer prompted login, so no further photo-viewer extraction was attempted.

## Official Pages Read

- Pixabay music: https://pixabay.com/music/
- Pixabay license summary: https://pixabay.com/service/license-summary/ (summary, not the full binding terms).
- Freesound: https://freesound.org/
- Freesound FAQ: https://freesound.org/help/faq/ (per-item CC licenses, registered login for downloads, Content ID caveats).
- Sound Effect Lab: https://soundeffect-lab.info/
- Sound Effect Lab terms: https://soundeffect-lab.info/agreement/ (commercial use, redistribution examples including editor stock banks, training and rights-registration restrictions).
- Mixkit transitions: https://mixkit.co/free-sound-effects/transition/ (42 listed at review).
- Mixkit sound effects: https://mixkit.co/free-sound-effects/ (no-signup and attribution statements).
- Mixkit license landing: https://mixkit.co/license/
- Full sound-effects license text: https://mixkit.co/license/modal/sfxFree/ . The landing-page button did not expose the text in the browser; the official indexed modal endpoint did. Read that endpoint directly before summarizing its rights/restrictions.
- ElevenLabs sound-effects page/FAQ: https://elevenlabs.io/sound-effects (free noncommercial vs paid commercial distinction). No price recommendation or universal copyright guarantee is made.

License descriptions are bounded summaries for asset selection, not an adjudication of any specific project's rights. The article does not redistribute recordings from these libraries.

## earshot Source Check

- Repository: https://github.com/Leonxlnx/earshot
- Pinned commit: `591fa3e028032e6dce56620a20e932e35667e8d8`, `2026-10-22T12:07:51+02:00`, release 0.4.0.
- Read README, package metadata, `earshot/forge/bank.py`, `earshot/forge/sfx.py`, `earshot/forge/kit.py`, `earshot/llm.py`, `docs/LIMITS.md`, `docs/CREDITS_FIT.md`, and the bank JSON structures.
- Clone: `/tmp/earshot-leon-article-20261027`.
- Structured Node JSON parse over `earshot/forge/bank/*.json` checked for duplicate IDs: `fit.json` 15, `forge04.json` 51, `forge_v2.json` 183, `pluck.json` 3; total 252 unique entries.
- This count is not a render test, sound-quality judgment, model benchmark, or compatibility check. No dependencies or model weights were installed, no models called, no user footage or audio supplied.
- Existing repository coverage was checked; this article uses a cross-resource workflow angle rather than replacing the older earshot deep dive.

Reproduction from the pinned source root:

```sh
node -e 'const fs=require("fs"),p=require("path"),dir="earshot/forge/bank",all=new Set();for(const f of fs.readdirSync(dir).filter(f=>f.endsWith(".json"))){const b=JSON.parse(fs.readFileSync(p.join(dir,f)));const ids=Object.keys(b.entries);for(const id of ids){if(all.has(id))throw Error("duplicate "+id);all.add(id)}console.log(f+": "+ids.length+" entries")}console.log("unique total: "+all.size)'
```

## Media

Both images copied unchanged from the pinned earshot `docs/media/`, visually inspected, and embedded in both language versions. These are upstream demonstration assets, not newly measured results. MIT notice preserved in `UPSTREAM-LICENSE.txt`, copyright 2026 Leon Lin.

| File | Dimensions | SHA-256 |
|---|---|---|
| `launch_frames.png` | 1932 x 818 | `0534071630cddfc1bd624f3e6e044970c836080a469129a8988e7e32f4b5d7a4` |
| `launch_sheet.png` | 2000 x 1331 | `cc49f68ef48566de0757f825b28b199acf0cc1d91be758f707a19966a0425b73` |

Sources: https://github.com/Leonxlnx/earshot/blob/591fa3e028032e6dce56620a20e932e35667e8d8/docs/media/launch_frames.png and https://github.com/Leonxlnx/earshot/blob/591fa3e028032e6dce56620a20e932e35667e8d8/docs/media/launch_sheet.png .
