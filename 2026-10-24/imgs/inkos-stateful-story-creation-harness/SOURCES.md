# Sources, Media, and Verification

Research/article date: 2026-10-24, Australia/Melbourne. This is a review date, not a claimed release date.

## Repository and Version Boundaries

- Repository: https://github.com/Narcooo/inkos
- Inspected branch: `master`.
- Inspected commit: `56aa33b04a27c45cc7a91f3d018187a77aec54ea`.
- Commit timestamp: `2026-10-18T17:56:54Z`.
- Commit message: `fix(docs): point KK MCP links to the live connection guide`.
- Root and core package versions: `2.0.0`; README explicitly labels the branch development code.
- `npm view @actalk/inkos version dist-tags --json` returned version/latest `1.8.0`, canary `1.8.0-canary.56.1`.
- GitHub latest formal release: [v1.8.0](https://github.com/Narcooo/inkos/releases/tag/v1.8.0), published `2026-08-17T04:15:34Z`.
- No feature-by-feature diff or runtime equivalence between npm 1.8.0 and this development snapshot is claimed.

## Key Inspected Sources

All source links are pinned to the inspected revision:

- [README](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/README.md), [root package](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/package.json), and [core package](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/package.json).
- [Harness runtime](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/harness/runtime.ts), [contracts](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/harness/contracts.ts), and [execution evidence](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/harness/execution-evidence.ts).
- [Context compiler](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/harness/context-compiler.ts).
- [Memory retrieval](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/utils/memory-retrieval.ts) and local-search implementation.
- [Observations and source validation](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/models/observation.ts), [chapter review](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/pipeline/chapter-review.ts), and the story-review Skill.
- [Forecast runner](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/forecast/runner.ts), context builder, and store.
- [Atomic file sets](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/utils/atomic-file-set.ts) and [chapter versions](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/state/chapter-workspace.ts).
- [Artifact validation](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/harness/artifact-validation.ts) and selected pipeline-runner paths.
- [Interactive story delivery](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/harness/tools/film-delivery.ts) and [HTML player](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/interactive-film/export-html.ts).
- [External Skill loader](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/packages/core/src/skills/external-loader.ts).

The public Skills were inspected as source material, not installed as instructions for the article task. Sponsorship copy and model-superiority claims were not used as technical evidence.

## Executed Checks

Temporary source checkout: `/tmp/inkos-article-20261024`. It is not a global InkOS installation and may be cleaned later.

Dependency preparation, from repository root:

```sh
pnpm install --ignore-scripts --frozen-lockfile --filter @actalk/inkos-core...
```

Tests, from `packages/core`:

```sh
pnpm exec vitest run \
  src/__tests__/atomic-file-set.test.ts \
  src/__tests__/chapter-workspace.test.ts \
  src/__tests__/forecast-store.test.ts \
  src/__tests__/forecast-runner.test.ts \
  src/__tests__/creative-harness.flow.test.ts \
  src/__tests__/context-compaction.flow.test.ts \
  src/__tests__/runtime-state-store.test.ts \
  src/__tests__/local-search.test.ts \
  src/__tests__/external-skill-loader.test.ts
```

Result: Vitest 3.2.4, 9 files passed, 54 tests passed, process exit 0. Node emitted an experimental SQLite warning; it was not a failure. Tests use temporary fixtures and model substitutes, not real model requests. The upstream checkout remained clean after dependency preparation and tests.

These checks do not establish literary quality, end-to-end generation quality, complete UI behavior, billing, provider compatibility, arbitrary interruption safety, filesystem power-loss durability, or database-style multi-file snapshot isolation. No complete test suite, Studio server, global installation, real generation, cover request, paid service, or personal manuscript import was run.

## Retained Images

Both are unmodified, author-provided UI screenshots copied from the pinned public repository and visually inspected. They were not produced by this review. Displayed titles, counts, times, and story content are upstream example material, not independent test measurements.

| Local file | Pinned source | Dimensions | SHA-256 |
|---|---|---|---|
| `studio-dashboard.png` | [assets/studio-dashboard.png](https://raw.githubusercontent.com/Narcooo/inkos/56aa33b04a27c45cc7a91f3d018187a77aec54ea/assets/studio-dashboard.png) | 1600 x 1000 | `fa17bdfec4597c92379b2db2e5b9266c88ee68f6081fb418850e613e0b835969` |
| `interactive-story-graph.png` | [assets/interactive-film-e2e.png](https://raw.githubusercontent.com/Narcooo/inkos/56aa33b04a27c45cc7a91f3d018187a77aec54ea/assets/interactive-film-e2e.png) | 1600 x 1000 | `1ccecdea2082eff22545ea813b1af11552b2e6083b7efe2233e076a35019ee84` |

`file` identified both as PNG, RGB, non-interlaced. No QR codes, advertisements, personal material, or credentials were copied into the article.

## Rights

Upstream declares AGPL-3.0-only in package metadata. The exact repository license is retained as `UPSTREAM-LICENSE.txt`; [pinned license](https://github.com/Narcooo/inkos/blob/56aa33b04a27c45cc7a91f3d018187a77aec54ea/LICENSE).

Project branding, screenshots, and depicted creative material retain their respective ownership. Attribution and retention here do not imply additional trademark, source-work, model-service, or publishing permissions, nor a replacement of upstream terms by the surrounding article repository's terms.
