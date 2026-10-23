# Sources, Attribution, and Verification

Research date: 2026-10-24, Australia/Melbourne.
Article source date: 2026-10-22, from the inspected commit's UTC timestamp, not an inferred product-launch announcement.

## Upstream Identity

- Repository: https://github.com/nevertoday/xxd-panel-345
- Revision: `6bad98d47c8ac83b330da4abcbb949d1726c8e2e`
- Commit timestamp: `2026-10-22T14:19:18Z`
- Commit message: `feat: add Panel 345 soldier skill with 40 themed samples`
- README attribution: Xiaoxiaodong / 小小东, https://x.com/xiaoxiaodong01
- GitHub API confirmed the repository is public. One web-reader request returned 404; public GitHub API, Git transport, and pinned raw files were readable. No private repository permission was used.
- GitHub tags and Releases lists were empty during review.

## Inspected Sources

All paths below refer to the pinned revision:

- [README](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/README.md) and [English README](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/README.en.md).
- [Skill entry](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/SKILL.md).
- [Canonical brief](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/references/original-prompt/zh-CN.md).
- [Shared runtime](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/references/soldier-runtime.md) and [delivery adapter](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/references/xxd-panel-345-prompt.en.md).
- [Bitmap bridge](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/scripts/configured_imagegen.py).
- [Raster helper](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/scripts/compose_panel.py).
- [Preference helper](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/scripts/panel_preferences.py).
- [Manifest checker](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/scripts/check_samples.py), [manifest](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/references/samples.json), and [sample workflow](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/references/sample-workflow.md).
- [Release packaging workflow](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/.github/workflows/release-package.yml).
- [License](https://github.com/nevertoday/xxd-panel-345/blob/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/LICENSE).

The remote Skill was read as source material, not installed or adopted as instructions for this article task.

## Retained Images

Images are unmodified upstream examples. They are not new generations by the article author. The manifest supplies the Unsplash source IDs; those are upstream provenance records, not independently verified source-photo identities or model-generation logs.

| Local file | Upstream path | Dimensions | Manifest source ID | SHA-256 |
|---|---|---|---|---|
| `sample-01-teapot-top-bottom.png` | `assets/examples/sample-01.png` | 1152 x 1536 | `photo-1773669957516-30a37ccecb06` | `7c39a49eda4cb9d15813bfa333e55f3a54150e4a1fa94b634027cfa4d603acaf` |
| `sample-21-vase-left-right.png` | `assets/examples/sample-21.png` | 1536 x 864 | `photo-1533616688419-b7a585564566` | `c890019b641eac8c6cfad05ccdd0e75186195b80c4b474f40af167cbc012670d` |
| `sample-39-lantern-left-right.png` | `assets/examples/sample-39.png` | 1536 x 864 | `photo-1512456489623-977da999566b` | `beaabdd724d1d6d50678a75682b75281c9b9ef66a87c3a35285772d60e72daaf` |

Pinned raw image prefix:
`https://raw.githubusercontent.com/nevertoday/xxd-panel-345/6bad98d47c8ac83b330da4abcbb949d1726c8e2e/`

### License and Notices

The upstream README applies PolyForm Noncommercial License 1.0.0 to its Skill, prompts, scripts, documentation, and accompanying examples. The exact upstream license is retained in `UPSTREAM-LICENSE.txt`; official terms: https://polyformproject.org/licenses/noncommercial/1.0.0/.

Images remain attributed to the upstream project and their respective rights holders. Their presence in this research article does not grant commercial-use, trademark, or other additional permissions. Do not assume the license of the surrounding article repository replaces the upstream image terms.

The inspected source text contains no author-specific plain-text `Required Notice:` beyond the explanatory placeholder inside the license itself. That placeholder remains in the retained license; it is not asserted as actual authorship.

## Checks Performed

1. Parsed four Python scripts using `ast.parse`; all passed.
2. Ran ten custom offline assertions using the upstream helper functions: six geometry assertions, two preference checks, and two bridge parsing checks. No generation/configuration/network functions were invoked.
3. Verified 40 unique manifest entries: 20 top-bottom and 20 left-right. The canonical brief SHA-256 matched `e7713a4fd278ac599effcae033fc0170f773ca3ed456e9079b71221d14f8c278`; all entries refer to that brief.
4. Downloaded only the three images above; SHA-256 matched the manifest, `file` identified valid PNGs, and all three were visually inspected.
5. Reproduced a diagnostic boundary using the original sample-01 with an intentionally incorrect expected size:

```sh
python3 -B scripts/compose_panel.py --audit <sample-01.png> --layout top-bottom --size 1152x1538
```

The actual image is 1152 x 1536. Output reported `size OFF`, then seam y=768 with zero offset and a seam `OK` verdict. Process exit code was 0. This is a controlled negative expectation, not a claim that the upstream sample has the wrong declared size.

## Not Verified

No Skill installation, model call, paid generation, route probe, local credential/configuration access, actual batch generation, wallpaper generation, cross-provider comparison, or complete 40-image checker run was performed. Upstream `visual_review: passed` flags were not treated as independent review results.
