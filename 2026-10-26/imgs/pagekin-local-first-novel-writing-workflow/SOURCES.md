# Pagekin Source and Media Record

Reviewed October 26, 2026. This is a current-source review date, not the project's launch date.

## Source Snapshot

- Upstream: https://github.com/EthanYoQ/AI-Novel-Writer
- Product name: 书童 Pagekin / Pagekin; formerly AI Novel Writer.
- Inspected master commit: `62880d629af7bbfaf968c0cda5ae76816e917915`.
- Commit timestamp: `2026-10-26T00:46:52Z`.
- `package.json` version: `1.3.2`.
- Latest formal release at review: [v1.3.2](https://github.com/EthanYoQ/AI-Novel-Writer/releases/tag/v1.3.2), published `2026-10-22T03:08:03Z`, tag commit `305ee75`.
- The release tag and inspected master differ. Do not present all current-source mechanisms as independently tested release-package behavior.
- Primary evidence: pinned README, package metadata, source modules linked in the articles, and the tests below. Historical docs can lag current behavior; the articles follow current code for context selection and supported Skill text references.

## Media

All eight images were copied unchanged from the pinned upstream `docs/assets/readme/` folder and visually inspected. They are upstream-authored 1.3.0 UI illustrations of the sample novel, not screenshots of a locally launched app or independent writing results.

Source prefix: https://github.com/EthanYoQ/AI-Novel-Writer/blob/62880d629af7bbfaf968c0cda5ae76816e917915/docs/assets/readme/

| Local filename (same as upstream) | View | SHA-256 |
|---|---|---|
| `v130-zh-chapter.webp` | Chinese manuscript/review | `4281d370714962a38f306bcb51d15adae0e438c6d85ca0d5bed6e3767c698b7c` |
| `v130-zh-blueprint.webp` | Chinese chapter blueprint | `9821543d5b04f5f0958cb7e0aff10c3a60485fcd0e2b15847d2abe2a54ed3fb5` |
| `v130-zh-cast.webp` | Chinese character profile | `fe8354bbce061037adb36379e7357eb45e3dbd5edcf3923129fb30d779c9b29c` |
| `v130-zh-run.webp` | Chinese run panel | `c71dd9d2704789b9aa9c12109a5f8d7cbc83953d7a1f9d7780c3b427aadb4a0e` |
| `v130-en-chapter.webp` | English manuscript/review | `070902775dff412d8540093d114b6cd75b1c163d6348e32509b4dc2900c18adf` |
| `v130-en-blueprint.webp` | English chapter blueprint | `6b4738d21df46b0ef48a0ab87e13d67ddd1fc9610e0f13c30cd769fafb97fb72` |
| `v130-en-cast.webp` | English character profile | `47af5674efd36df700c7ed4e899425860c835f19d50dc1be2d8c05c0f884d5c1` |
| `v130-en-run.webp` | English run panel | `893b7ff66ead8813b4f2e1783f5d2dcd9bd6504ea4e2ace2218238ee4cbd6c68` |

The repository licenses the desktop application under GPL-3.0; no separate license was identified for this screenshot set. Upstream attribution and the unmodified license text are preserved in `UPSTREAM-LICENSE.txt`. Media use here is illustrative, not a claim of ownership or an independently generated UI demonstration.

## Focused Test Run

Source clone: `/tmp/pagekin-article-20261026`. Node `v25.7.0`; pinned package manager `pnpm 11.11.0`; Vitest `4.1.12`.

```sh
npx --yes pnpm@11.11.0 install --ignore-scripts --frozen-lockfile --filter ai-novel-writer
npx --yes pnpm@11.11.0 exec vitest run \
  src/shared/__tests__/human-confirmed-review.test.ts \
  src/shared/__tests__/writing-skills.test.ts \
  src/shared/__tests__/consistency-preflight.test.ts \
  src/shared/__tests__/chapter-goal-review.test.ts \
  src/shared/__tests__/review-generation-report.test.ts \
  src/services/generation/__tests__/task-budget-planner.test.ts \
  src/services/__tests__/finalization-snapshot.test.ts \
  electron/services/__tests__/writing-skill-package.test.ts
```

Result: exit 0, 8 test files passed, 184 tests passed. A repeat run also passed with the same count. The source checkout remained clean.

Not performed: complete test suite, application build, Electron launch, real provider requests, native SQLite integration, installer execution, power-loss recovery, or long-form creative-quality evaluation. No real API keys or private manuscripts were supplied. Source-level safeguards and selected unit tests are not an end-to-end product certification.
