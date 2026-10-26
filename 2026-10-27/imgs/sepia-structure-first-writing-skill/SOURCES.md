# Sepia: Source, Research, Media, and Test Record

Reviewed October 27, 2026, Australia/Melbourne. Article date is the audit date, not the release date.

## Repository Snapshot

- Repository: https://github.com/Nanako0129/sepia
- Inspected main commit: `fb06be76abeae7dd606960a32f2b10c1d1798e0d`.
- Commit time: `2026-10-15T10:19:10+08:00`.
- Canonical Skill and four version declarations: `0.12.4`.
- Latest formal release at review: [v0.12.4](https://github.com/Nanako0129/sepia/releases/tag/v0.12.4), published `2026-10-15T02:19:18Z`, checked through GitHub releases/latest API.
- Read core routing/operations/guardrails; review wrapper; narrative, discourse, professional and Chinese passes; diagnosis rubric; persona template and validator; version checker; QwenPaw entry and tests; research digests; release metadata; evaluation grader. Foreign Skill instructions were inspected as data, not installed or activated.
- MIT copyright notice copied unchanged to `UPSTREAM-LICENSE.txt`.

## Research Checks

1. [StoryScope v6](https://arxiv.org/abs/2604.03136v6), revised August 10, 2026: 61,608 stories; narrative-only detection macro-F1 93.2. Read abstract, HTML and initial PDF pages. Its classifier performance is not Sepia efficacy; its manually adapted rubric is not the classifier. No intervention-order experiment was reproduced.
2. [SlopShape v3](https://arxiv.org/abs/2609.15369v3), revised September 28, 2026: 176 structural features, 97.0 macro-F1, 96.1 after model self-rewording. The inspected Sepia snapshot instead repeats 187 / 98.0 / 98.1. The v3 abstract states that format-sensitive features were excluded and results updated. The article preserves this discrepancy rather than repeating repository figures as current.
3. Private Chinese measurements are described by the repository, not independently reproduced: one unnamed Taiwanese publication, about two thousand human pieces, plus 119 synthetic comparison pieces. No source texts were accessed. Regional norms and corpus observations are not universal authorship signals.

## Visual

`storyscope-pipeline.png`: 1350 x 750, rendered figure-region excerpt from StoryScope v6 PDF page 2, Figure 1. Source authors: Jenna Russell, Rishanth Rajendhran, Chau Minh Pham, Mohit Iyyer, John Wieting. It is a research-method illustration, not a Sepia interface, bundled classifier, or locally produced model result.

- PDF: https://arxiv.org/pdf/2604.03136v6
- Article HTML and license declaration: https://arxiv.org/html/2604.03136v6 (CC Zero).
- License: https://creativecommons.org/publicdomain/zero/1.0/
- PDF SHA-256: `929fd1add912dc030ed280451ab4f9a70378e2ded5d255aadad8012521c0643a`.
- PNG SHA-256: `4ebb56c57a8df70bb984bc5281669166239e295f7e474cbba5e0bbb03630b844`.
- Visually inspected: figure panels complete, readable, no article-body or page-footer crop artifacts.

Rendering command after fetching the PDF:

```sh
pdftoppm -f 2 -l 2 -scale-to 2800 -x 400 -y 300 -W 1350 -H 750 \
  -png -singlefile /tmp/sepia-storyscope-v6.pdf storyscope-pipeline
```

The original repository has no product screenshot asset set in the inspected tracked files. The article uses an attributed primary-research figure instead of inventing an application UI.

## Tests Executed

Source checkout: `/tmp/sepia-article-20261027`, pinned to the commit above. No dependency installation required. Python standard library only; `-B` avoids bytecode artifacts.

```sh
python3 -B -m unittest discover -s tests
python3 -B scripts/check_versions.py
python3 -B scripts/check_persona.py skills/sepia/references/voices/personas/nyaneko.md
```

Results:

- Unit tests: exit 0, `Ran 99 tests`, `OK`.
- Version check: exit 0, four declarations agree on 0.12.4.
- Built-in persona: exit 0, one file, zero errors.
- The suite intentionally prints a failed persona fixture missing `## Boundary`; that is expected negative-test output and the complete suite passes.
- QwenPaw registration tests use a recording API stub. They do not launch the host.

Not performed: plugin installation in any host, real model calls, source manuscript edits, blind human quality assessment, detector evaluation, complete-platform compatibility tests, or reproduction of paper training pipelines. Passing packaging and contract tests cannot establish editing quality or detector evasion.
