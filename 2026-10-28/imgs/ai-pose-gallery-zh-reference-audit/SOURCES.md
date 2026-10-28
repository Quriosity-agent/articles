# AI Pose Gallery Chinese Edition: Evidence and Reproduction

Review date: October 28, 2026, Australia/Melbourne.

## Sources and Scope

- Post: https://x.com/anhao_ai/status/2115070903386296398 . Read in the in-app browser after the search browser returned 403. Visible time was 00:19 October 28. The status-ID-derived UTC time is `2026-10-27T13:19:34.141Z`, also October 28 in Melbourne.
- Repository: https://github.com/anhao/ai-pose-gallery-zh . Pinned commit `072a3690af6e7e0011abbe0fa1ccc08939fbb47d`, timestamp `2026-10-27T22:32:19+08:00`, analytics-script addition.
- Chinese live URL resolved from the post: https://ai-pose-gallery.anhao.app/ . Search-browser retrieval failed; the gallery UI was not exercised here. Implementation statements refer to the pinned source, not a live UI acceptance test.
- Original site: https://ai-pose-gallery.pages.dev/ . Read public usage tips and notices with the web tool. Original creator credited by the source: ギア, https://x.com/giaaibusi . The quoted original post was visible inside Anhao's post; a separate web-tool retrieval of that original X URL failed.
- Read `README.md`, `LICENSE`, core HTML routing/search/lightbox/loading code, usage notices, `scripts/apply_translation.py`, `scripts/verify.py`, `scripts/build.sh`, `_headers`, and Japanese/Chinese metadata. No source scripts were executed.
- Sparse source checkout: `/tmp/ai-pose-gallery-article-20261028`, created with `--filter=blob:none --sparse`, adding only `data` and `scripts`. Root files were included by sparse checkout. Source image directories were not checked out or fully decoded. Git tree checks do not fetch or validate all image contents.

## Rights and Content Handling

- Original-site notice allows creative commercial/reference use while explicitly prohibiting redistribution/republication/resale of image data, original or modified. It also restricts use involving real people or minors and inappropriate uses.
- Repository MIT scope excludes image assets and original metadata. Its noncommercial sentence differs from the original notice and the mirror's translated help. The mirror help explicitly asks its maintainer to confirm public-display/republication permission separately. No supplementary authorization was verified, and no infringement determination is made.
- No source thumbnails, full images, original dataset, gallery screenshots, or cover collage are republished in this article. Original source images were not used in generation. Adult-oriented categories are not illustrated or explored.
- The article's figure is original explanatory artwork drawn from aggregate counts. No source pose artwork is copied or modified.

## Independent Structural Audit

Run from the articles repository:

```sh
node 2026-10-28/imgs/ai-pose-gallery-zh-reference-audit/audit-data.mjs \
  /tmp/ai-pose-gallery-article-20261028
```

Result: exit 0, eight checks true; persisted aggregate report in `data-audit.json`.

- 1439 records and 1439 unique IDs.
- 288 groups using the frontend's collection-plus-pose-number key.
- 287 groups with five distinct angles, one with four. The four-angle record group lacks the low-angle view; this is a metadata coverage observation, not a missing-tracked-file claim.
- 2878 unique image paths, all present in the pinned Git tree.
- Japanese-to-Chinese record order, IDs, and thumbnail/full-image paths preserved.
- 26 categories and five angle labels.
- 288 Japanese names become 287 Chinese names: two source names translate to the same nonsexual leaning-forward/hands-on-knees label. This is a naming collision, not loss of a pose group.
- Counts do not establish translation accuracy, image contents, decode integrity, consistent anatomy, camera calibration, or model pose adherence.

No full upstream verification run was made because the image set was intentionally not fetched. Its script's header/size checks are described from source, not presented as a completed image QA result.

## Figure

`data-coverage.png`, 1440 x 930, original aggregate-count chart. Generated with the review-created `render-chart.mjs` using the desktop app's bundled `@napi-rs/canvas`; no new package installation was needed. System and bundled Python lacked matplotlib, so the existing Node canvas library was used instead.

```sh
node 2026-10-28/imgs/ai-pose-gallery-zh-reference-audit/render-chart.mjs \
  /Users/peter/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules \
  2026-10-28/imgs/ai-pose-gallery-zh-reference-audit/data-audit.json \
  2026-10-28/imgs/ai-pose-gallery-zh-reference-audit/data-coverage.png
```

Chart labels shorten two collection names for neutral presentation; the aggregate report preserves their source labels. Full-body standard: 365 records / 73 groups; alternate full-body series: 399 / 80; upper-body: 400 / 80; paired series: 275 / 55.

PNG SHA-256: `f481ca3b5abe676355370046f9e788dfdd45ee12efecf729407825b01274e8c2`.

Visually inspected: all labels and values legible, complete bars, no overlap or clipping. This is not a product screenshot or generated-pose comparison.
