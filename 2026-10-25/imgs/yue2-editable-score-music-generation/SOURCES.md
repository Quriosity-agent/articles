# Sources, Media, and Verification

Research/article date: 2026-10-25, Australia/Melbourne. This is a source review, not a new release announcement.

## Version and Scope

- User-provided repository: https://github.com/multimodal-art-projection/YuE
- Inspected branch: `main`.
- Inspected commit: `1647252d68b70cbead046ffd3f7caf036dde47ee`.
- Commit time: `2026-10-06T07:30:39Z`.
- Commit message: `docs: link SheetSage2 arXiv paper and citation`.
- Source package: `yue2-infer`, version `0.1.6`.
- Current README concerns YuE2; original YuE remains at https://github.com/multimodal-art-projection/YuE/tree/YuE-v1.
- README dates the initial YuE2 release to September 14, 2026, with later global/text-to-audio milestones. The original YuE branch records its initial release on January 26, 2025.
- The arXiv page for YuE2 lists submission on September 27, 2026; this is not substituted for repository launch milestones.
- No feature-by-feature runtime equivalence between old wheels, current source, YuE v1, or hosted services is claimed.

## Primary Sources

Pinned repository sources:

- [README](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/README.md)
- [Generation](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/docs/generation.md)
- [Covers](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/docs/covers.md)
- [Editing](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/docs/editing.md)
- [Benchmarks](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/docs/benchmarks.md)
- [Pipeline and artifacts](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/src/yue2/pipeline.py)
- [ABC helper](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/skills/yue2-music/scripts/abc_tools.py)
- [Instrumental workflow](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/skills/yue2-music/instrumental/README.md)
- [Package metadata](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/pyproject.toml)
- [Code license](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/LICENSE), [weight license](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/MODEL_LICENSE), and [third-party notices](https://github.com/multimodal-art-projection/YuE/blob/1647252d68b70cbead046ffd3f7caf036dde47ee/THIRD_PARTY_NOTICES.md).

Companion sources:

- https://huggingface.co/m-a-p/YuE2-3B — model card and earlier wheel instructions. The card's v0.1.5/Python 3.10+ example differs from the source v0.1.6 documentation recommending Python 3.12.
- https://map-yue2.github.io/ — loaded score/song and multi-turn editing interfaces, architecture explanation. Displayed tracks, versions, model names, and counts are upstream examples, not independent measurements.
- https://arxiv.org/abs/2609.33757 — YuE2 technical-report abstract, read as author-reported research. The entire paper and listening experiment were not independently reproduced.

Repository Skills were read only as source material; none was installed or adopted as instructions for this article task.

## Executed Verification

Temporary checkout: `/tmp/yue-article-20261025`.

No inference installation or model download was performed. The available system Python reported `3.15.0`; it was used only for standard-library-based helper checks, not as a validated GPU runtime.

```bash
python3 -m unittest discover -s tests -p 'test_skill_*.py' -v
```

Result: 35 tests passed in 0.225 seconds, exit 0, across these five files:

- `test_skill_abc_tools.py` — 18 tests.
- `test_skill_listen.py` — 4 tests.
- `test_skill_release.py` — 3 tests.
- `test_skill_requests.py` — 6 tests.
- `test_skill_transcribe_melody_only.py` — 4 tests, mocked model/torch/Transformers interfaces.

Release tests intentionally print bundle-verification failures for corrupt or unlisted fixtures; those negative cases passed. This was not an installation failure or a model execution.

```bash
python3 skills/yue2-music/scripts/abc_tools.py compare \
  examples/score.abc examples/score-jazz.abc
```

Result: `match: true`, voices `Vocal` and `Ins`, no differences, tempo change not allowed. The command's stated scope is exact symbolic melody and meter, with no claim about generated audio or unchanged harmony. Original and jazz fixtures were inspected; they retain melody while changing chord symbols.

The clone remained clean after the tests. No full test suite, CUDA/MPS/CPU model inference, transcription, synthesis, benchmark reproduction, auditory comparison, paid service, private material import, or package/Skill installation was performed. Public demos were displayed but not played. Browser session closed after capture.

## Retained Visuals

| Local file | Source | Notes |
|---|---|---|
| `architecture.png` | [Pinned assets/architecture.png](https://raw.githubusercontent.com/multimodal-art-projection/YuE/1647252d68b70cbead046ffd3f7caf036dde47ee/assets/architecture.png) | Unmodified upstream diagram; 2352 x 1191 PNG |
| `official-benchmark-overview.png` | [Pinned assets/frontier-teaser.png](https://raw.githubusercontent.com/multimodal-art-projection/YuE/1647252d68b70cbead046ffd3f7caf036dde47ee/assets/frontier-teaser.png) | Unmodified author-reported overview; 1980 x 854 PNG |
| `official-score-demo.webp` | https://map-yue2.github.io/#abc-cot-gen | Fresh browser capture, 1440 x 1000 viewport; loaded score/song interface, no playback |
| `official-agent-editing-demo.webp` | https://map-yue2.github.io/#agentic-music-editing | Same session, scrolled to the editing region; upstream nine-step/fourteen-version story, not a reproduced session |

SHA-256 of copied original assets:

```text
1926e7b5943d90c5b26426fdc5b3ff64b8552cce10fb5a7df60a077941d143b1  architecture.png
0f7e859bfee94eb456a1c38650eb6474568721356349ef490ac4a7e8bc49c68f  official-benchmark-overview.png
```

All four images were visually inspected; `file` identified the two copied PNGs and the two WebP screenshots. No audio, model weights, QR codes, or private material were retained in the article.

## Benchmark Boundaries

The displayed extract is from the authors' September 12, 2026 comparison of 192 prompts and 17 settings. SongBench Avg averages seven dimensions; it is not a listener preference percentage. Standard YuE2 selects between two candidates by PER, while best-of-8 uses SongBench Musicality, prompt control, and PER. Four ASR repeats per candidate are used for the reported PER selection. Other systems retain documented, nonidentical candidate protocols.

Both reported YuE2 settings use symbolic planning and the benchmark decoder `YuE2-Vae-legacy`; daily listening defaults to `YuE2-Vae`. A single pipeline call does not implement the full evaluation candidate selection. Composite chart axes are normalized indices, not success percentages, and small differences are not reported here as statistically significant. No comparative superiority was independently measured.

## Rights

Exact upstream `LICENSE` and `MODEL_LICENSE` copies are retained as `UPSTREAM-LICENSE.txt` and `MODEL-LICENSE.txt`. Main code is Apache 2.0; the YuE2 checkpoint weights use CC BY-NC 4.0 plus the stated individual-creator permission. Bundled components have their own notices; the instrumental helper package declares MIT for its own original instructions/scripts. No weights or helper source are redistributed here.

Diagrams, interfaces, example scores, song names, and other depicted material retain their respective ownership. Article inclusion does not grant rights to third-party music, lyrics, voices, trademarks, or model weights. The license summary is a description of the pinned project terms, not a commercial clearance determination for any particular deployment.
