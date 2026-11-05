# Claude Motion Ten-Repository Selection: Evidence

## Source and Scope

- Original post: https://x.com/double_burger_2/status/2117904522987376880
- Author: Leo / @double_burger_2.
- Source page displayed `19:59 · 4 Nov 2026`; the article uses the displayed publication date, without asserting a UTC time conversion.
- Reviewed 2026-11-05, Australia/Melbourne.
- The web reader returned HTTP 403. The normal in-app browser loaded the complete public post, its visible link titles, and author information. No account sign-in or posting occurred; the temporary tab was closed.
- Original link titles for Anatomy and Animate were only `http://github.com/anatomy` and `http://github.com/animate`; mg-styles-15 pointed to `http://github.com`. Corrected repository entries are independently matched, not presented as intact outbound links from the post.
- Earlier local articles supplied Anatomy and mg-styles-15 source pointers. Animate was located through focused web search and checked against the project's own README. Secondary search results were not used as technical evidence.
- This is a distinct follow-up to the October 21 eight-repository article, emphasizing motion principles, vocabulary, asset libraries, workflow gates, and license differences.

## Pinned Revisions

README and recursive Git trees were read for each project; selected implementation files were read where discussed. Revision links are immutable snapshots, not assertions that every repository was launched or updated on the article date.

| Repository | Inspected commit |
|---|---|
| lemomo-ai/lemo-opuscar | [bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00](https://github.com/lemomo-ai/lemo-opuscar/tree/bebbbe1aa92a3cb4bb6f83500e61b23a17d1aa00) |
| wheresryan22/anatomy | [1482e8469b0a9e0d8cc18ea2740a01423d29ae80](https://github.com/wheresryan22/anatomy/tree/1482e8469b0a9e0d8cc18ea2740a01423d29ae80) |
| LottieFiles/motion-design-skill | [f9a8a041b85185ee4881b3471d3415e939aac772](https://github.com/LottieFiles/motion-design-skill/tree/f9a8a041b85185ee4881b3471d3415e939aac772) |
| patch-gg/pixelfx | [a84159688af3ca37a4be05a0d422b94451b2e24e](https://github.com/patch-gg/pixelfx/tree/a84159688af3ca37a4be05a0d422b94451b2e24e) |
| feitangyuan/onetake | [abb6d17279cdc749e27e99aa534a062d8fd01ced](https://github.com/feitangyuan/onetake/tree/abb6d17279cdc749e27e99aa534a062d8fd01ced) |
| alchaincyf/huashu-art-motion | [8a0d7d72ca65fcce6f8ba82c4a6c8dfe35b8422c](https://github.com/alchaincyf/huashu-art-motion/tree/8a0d7d72ca65fcce6f8ba82c4a6c8dfe35b8422c) |
| cth9191/animate | [7e5eb56feb2dd573f890e1b7b34748af43d58263](https://github.com/cth9191/animate/tree/7e5eb56feb2dd573f890e1b7b34748af43d58263) |
| Vincentwei1021/mg-styles-15 | [49052d80bfaf9fa8412cc9710530e5e95a3b8d8c](https://github.com/Vincentwei1021/mg-styles-15/tree/49052d80bfaf9fa8412cc9710530e5e95a3b8d8c) |
| HeyChengC/vibe-knowledge-film | [62d51508aad00003dc6209afa80c4b5dc540de59](https://github.com/HeyChengC/vibe-knowledge-film/tree/62d51508aad00003dc6209afa80c4b5dc540de59) |
| showheyohtaki/motion-prompt | [7819d3879eb7d5a1475c11c001bedffb5cab64af](https://github.com/showheyohtaki/motion-prompt/tree/7819d3879eb7d5a1475c11c001bedffb5cab64af) |

onetake's inspected commit is dated November 5, after the post. This article reports the inspected state, not a reconstruction of exactly what every linked repository contained at posting time.

## Concrete Checks

- Motion Prompt `api/v1/catalog.json`: 192 actual elements, 192 unique IDs, eight packs, each containing 24 elements. This contradicts the post's description of fifteen ten-second styles.
- pixelfx recursive tree: 264 category-level JavaScript files under `src/fx/<category>/`; twenty are `_lib.js` helpers, leaving 244 effect modules. File counts establish inventory, not effect quality.
- LottieFiles `skills/motion-design/SKILL.md`: emotional intent and eight-step checklist; document-based guidance rather than a whole-film renderer.
- Animate `tools/build.mjs`: assembles project scene, style, score, and kit components; README establishes story/look/storyboard gates and seven built-ins plus custom references.
- vibe-knowledge-film `SKILL.md`: silent, 16:9 scope, facts, conceptual visualization, thirty-second approval gate. It explicitly excludes narrated talking-head work from this skill's scope.
- onetake `scripts/verify_promo.py`: carry scoring and other project-defined checks; a useful implemented rubric, not a standardized human-quality benchmark.

In a temporary sparse checkout of the pinned onetake commit, with Node.js v25.7.0:

```sh
node scripts/test_motion.js
```

The existing script returned `ALL PASS`, exit 0. It checks motion math, easing, springs, coordinate transforms, deterministic simulations, time warping, and UI helpers. No browser film render, sound review, commercial use, or aesthetic validation was performed. No skills were installed and no account/model was used to create a new film.

## License Boundaries

- onetake's fixed `LICENSE` is PolyForm Noncommercial 1.0.0. README separately describes commercial licensing and excludes complete film sources from public cases. No purchase was made and no price is relied upon in the article.
- Lemo README separates MIT code/docs, CC BY 4.0 demonstrations, third-party credits, and three excluded voice tracks.
- Huashu README excludes certain character artwork, overview/demo uses of that character, and unofficial mascot demonstrations from its MIT grant; font/stroke-data licenses are separate.
- pixelfx `NOTICE.md` identifies adapted MIT code and excludes the Patch Pixel font from the repository's general MIT license.
- vibe-knowledge-film `LICENSE` and README reserve third-party reference-film scripts/designs, including `examples/stim_B` and `examples/info_C`. None of those materials is reproduced here.
- These are descriptions of the projects' published notices, not a complete legal audit or a prediction about rights in generated outputs.

## Figures

Figures were downloaded from pinned upstream files and visually inspected. They illustrate existing project examples, not results reproduced during this review. Copyright notices and MIT terms are retained in [LICENSES.md](LICENSES.md).

| Article asset | Pinned source path | Treatment |
|---|---|---|
| `animate-styles.png` | `cth9191/animate@7e5eb56/docs/styles.png` | Original PNG, unchanged; credit cth9191 |
| `motion-vocabulary.gif` | `showheyohtaki/motion-prompt@7819d38/assets/preview-motion.gif` | Original GIF, unchanged; credit Shohei Ohtaki |
| `pixelfx-effects.jpg` | `patch-gg/pixelfx@a841596/docs/readme/montage.gif` | Extracted one frame at 1.5 seconds, JPEG encoded; credit Patch / Hugo Duprez and contributors |

The 5.5 MB pixelfx source GIF remains temporary research material rather than a committed raw asset. Extraction:

```sh
ffmpeg -hide_banner -loglevel error -ss 1.5 \
  -i montage.gif -frames:v 1 -q:v 2 pixelfx-effects.jpg
```

The static pixelfx image does not verify timing or animation continuity. No onetake case media, restricted Huashu character assets, or third-party reference-film footage is copied into this article.
