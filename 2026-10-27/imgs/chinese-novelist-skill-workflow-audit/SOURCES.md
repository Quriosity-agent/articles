# Chinese Novelist Skill: Source and Probe Record

Review date: October 27, 2026 (Australia/Melbourne). This is a source audit, not a model benchmark or a completed-novel evaluation.

## Snapshot

- Repository: https://github.com/PenglongHuang/chinese-novelist-skill
- Inspected master: `7017828a0052e2e030d90d630446401a812e50e6`.
- Commit timestamp: `2026-10-21T00:26:33+08:00`.
- Latest formal release at review: [v2.3.1](https://github.com/PenglongHuang/chinese-novelist-skill/releases/tag/v2.3.1), published `2026-10-20T15:47:04Z`, verified through GitHub's releases/latest API. Release notes describe fact-ledger rules, quantitative style checks, checklist consolidation, and checker hardening. Article behavior follows the pinned master source rather than assuming every release snapshot is identical.
- README still highlights v2.0; current Roadmap records v2.3.1. Do not label the inspected project simply v2.0 or turn in-progress roadmap items into shipped software.
- Read: SKILL.md; initialization, planning, writing, final-validation, chapter-checklist, and shared-infrastructure documents; chapter/style guide; outline and chapter templates; ROADMAP.md; Python checker; MIT license.
- Examined Skill documents as source material only. Did not install or activate their novel-production instructions.

## Media

Copied unchanged from `assets/` at the pinned commit. All three images were visually inspected. They are upstream demonstrations, not this review's writing results. The completion screenshot uses older file numbering. The article describes current conventions instead of copying obsolete names. The sponsor banner was intentionally excluded.

Source prefix: https://github.com/PenglongHuang/chinese-novelist-skill/blob/7017828a0052e2e030d90d630446401a812e50e6/assets/

| Filename | Dimensions | SHA-256 |
|---|---|---|
| `phase2-plan.png` | 1444 x 784 | `629e34def401dab4abe2f5eb095183659ec095a2d6b8c6d856fd2203447a0fcd` |
| `memory-demo.png` | 1571 x 790 | `6459a4297cca00e539886ebaa8dfda953b9ecaa13ced8481be8312c8687a6478` |
| `phase4-done.png` | 1859 x 1003 | `9f2e80614e080afad0a862689ff2a7906e7c10a82ca7920a341cb639efdaff84` |

Upstream copyright: 2026 PenglongHuang. The unmodified MIT notice is preserved in `UPSTREAM-LICENSE.txt`.

## Reproduction

Source clone used for probes: `/tmp/chinese-novelist-article-20261027`. No dependency installation was needed; the checker uses Python's standard library. The review-created `probe_wordcount.py` loads the inspected checker and creates synthetic files only inside a temporary directory.

From this asset folder, with a clone at the recorded commit:

```sh
python3 probe_wordcount.py /tmp/chinese-novelist-article-20261027/scripts/check_chapter_wordcount.py
```

Result: exit 0, ten expected observations reproduced:

1. Mixed Chinese/Latin/digit fixture counts four basic CJK characters.
2. Chapter title is skipped; two-character prose meets minimum two, exit 0.
3. The same prose fails minimum three, exit 1.
4. Summary material and labels inflate two-character prose to count eight.
5. 5001 characters pass the default minimum-only check.
6. A negative minimum accepts empty prose.
7. Missing single file yields exit 2 and one file error.
8. A non-integer minimum yields exit 2 and a JSON error.
9. A directory scan passes an existing chapter despite a plan listing an additional missing chapter; total one, errors zero.
10. Arabic chapter numbers sort as 1, 2, 10.

The assertions intentionally reproduce both useful behavior and limitations; ten passing probes do not mean ten quality requirements satisfied. The missing-plan-chapter result concerns the script alone: the workflow separately instructs the Agent to check each planned file's existence.

Not tested: model output, semantic continuity, preference retention across real sessions, host tool compatibility, parallel conflict handling, end-to-end interruption recovery, generation costs, or complete manuscript quality. No API requests to model services, no private manuscript inputs, and no full novel generation were performed.
