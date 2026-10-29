# AI Pose Gallery Chinese Edition: Evidence and Reproduction

Review date: October 28, 2026, Australia/Melbourne.

Supplemental original-site review: October 29, 2026, Australia/Melbourne. The original pinned audit and chart below remain unchanged.

## October 29 Sharing-Post and UI Supplement

- Requested source: https://x.com/Mrpinecone888/status/2115055965800435730 . Read in the in-app browser after the web tool returned 403. The post links to https://ai-pose-gallery.pages.dev/ and introduces 1,439 pose-reference images. It is the same original gallery covered here, so the existing bilingual article was updated rather than duplicated.
- Visible post time: 23:20, October 27, 2026. The DOM exposed no `time[datetime]` element. Applying the standard status-ID timestamp formula gives `2026-10-27T12:20:12.743Z`, or October 27 at 23:20 in Melbourne. This is a sharing-post timestamp, not a verified original-gallery launch date.
- Re-read the original site's public HTML, usage tips, and notices. The web tool also successfully retrieved those original-site notices. Creator credit remains ギア; a sharing post does not establish asset authorship or broaden the original permission terms.
- Original-site UI reports 288 groups / 1,439 images overall, 73 / 365 for standard full-body single-person, 14 / 70 after the standing-category filter, and 14 / 14 after selecting side views.
- Within those conditions, entering `full_single_P015_side` in the search field and allowing the input debounce to settle gives one group / one image. Its enlarged view loads `img/full_single_P015_side.png`; the browser reported natural dimensions 900 x 1200. No manual original-file download or all-library dimensional validation was performed.
- The original already supports grouping, angle filtering, and download controls. Corrected both articles so they do not attribute those existing features to the Chinese localization.
- This supplement concerns standard single-person standing references only. No adult pose artwork, source screenshots, or raw dataset are reproduced. No generation model, Chinese live-UI acceptance test, or new source-repository audit was run. The earlier figure is retained and was visually rechecked for readability.

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
