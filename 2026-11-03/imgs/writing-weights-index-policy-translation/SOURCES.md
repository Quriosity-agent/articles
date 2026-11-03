# Writing Weights Index: Sources and Verification

Review date: 2026-11-03, Australia/Melbourne.

## Social Sources

- Requested post: https://x.com/xingyudang/status/2117428789068386630 . Read successfully through the in-app browser after web retrieval returned 403. Visible time 12:28, November 3. Status-ID conversion gives `2026-11-03T01:28:57.895Z`, consistent with Melbourne.
- Policy comparison: https://x.com/xingyudang/status/2117428791660134736 . Author says direct Python policy generation performs better, particularly for open-source models, and describes writing weights as policy generation plus translation.
- Conversion comparison: https://x.com/xingyudang/status/2117428794994921953 . Chart footnote says Gemini scores are user-reported and not rerun locally.
- Original-study link: https://x.com/xingyudang/status/2117428797540577300 . Resolves to https://rikiyat.github.io/blog/weight-space-programming/ . The study is dated November 2; the requested cross-model index is a November 3 follow-up, so this article uses November 3.
- Carbon provenance: https://x.com/xingyudang/status/2117428799042134182 quotes https://x.com/wenhaocha1/status/2117383529273405747 . The requested author's text attributes Carbon results to that source. No model access or provider availability claims are inferred from names in the charts.

## Original Research and Pinned Records

Study authors: Rikiya Takehi, Jayden Teoh, Alex Zhang, and Omar Khattab, listed with MIT CSAIL affiliations. Read the blog's task definitions and distinctions between no-tool/no-feedback experiments and later tool-assisted experiments. The article focuses on Experiment 5 and the separate cross-model follow-up, not all eight experiments.

Public source: https://github.com/RikiyaT/lm_understand-logs . GitHub API reported `main` HEAD `4d09ba6d6a7e891dd8063974dfe81b3d78e3494f`. Read the root README, LICENSE, Experiment 5 README, evaluation JSON, Breakout application JSON, run JSON, and the beginning of its prompt. No source code or generated network was executed.

The original logs are available; they must not be described as absent. They are also not the full run records for the requested author's additional model leaderboard. The inspected thread does not establish every cross-model prompt, reasoning budget, generation attempt, parser configuration, raw per-game score, or confidence interval. The index cannot be independently recalculated for each model from the chart alone.

The original release's license assigns CC BY 4.0 to its logs/data/networks, MIT to author-written scripts, and GPL-3.0 to MinAtar source embedded in prompts; other third-party data retain their licenses. Attribution: the authors of *Sparks of Weight-Space Programming*, fixed repository commit above. This article reports selected aggregate facts and original analysis; it does not redistribute prompts, model responses or reasoning traces, source game code, or weight files.

## Figures

Source chart URLs observed in the requested thread DOM:

1. `writing-weights-index.webp`: https://pbs.twimg.com/media/HWKcRSLWEAAHM77?format=webp&name=small
2. `python-policy-index.webp`: https://pbs.twimg.com/media/HWKcjxtWUAETdWU?format=webp&name=small
3. `policy-to-weights-conversion.webp`: https://pbs.twimg.com/media/HWKdvr0WMAE5-jv?format=webp&name=small

The source-served files decode to 680 x 353, 680 x 353, and 680 x 448 respectively. Original-size PNG variants were unavailable (404), so only these actually retrieved WebP variants are included, without upscaling. All charts were visually inspected; numerical rows and the index formula are transcribed into article text for readability. The chart author's images are attributed, not represented as covered by the original research repository's CC BY license.

The chart marks a median weights/policy index ratio around 71% for its proprietary group and 10% for its open-weight group. The articles avoid treating that ratio as compiler correctness, raw reward retention, or a general ability measure. Rounded chart values cannot reproduce every displayed ratio precisely.

## Executed Checks

```sh
node 2026-11-03/imgs/writing-weights-index-policy-translation/audit-evidence.mjs
```

The script only fetches JSON from the pinned original study and performs arithmetic/assertions. It verifies the 20,486-parameter architecture; selected Breakout parser/application fields; author-reported tool-free flag; three original generated-policy means, episode counts, and best-seed baseline extraction; and index anchors q=0 -> 0, q=1 -> 50, q=3 -> 75. `evidence-audit.json` contains aggregates and manually transcribed chart rows, not new model evaluation results.

No model/API invocation, training, game rollout, generated-policy execution, complete event-stream audit, or reproduction of the cross-model leaderboard was performed. No claim is made that the original network-parser repair was independently rerun here.
