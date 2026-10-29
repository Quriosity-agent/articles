# Sources and Verification

- Canonical site: https://ai-costume-gallery.pages.dev/
- Page title: 衣装集 COSTUME-DB-01
- Creator link observed on page: https://x.com/giaaibusi
- Review date: 2026-10-29, Australia/Melbourne. No original launch date established.

## Evidence

Read the live introduction, usage hints, notices, category counts, and public inline HTML/JavaScript. Browser checks used ordinary spring outfits only. Observed:

- Complete-ID query `SPR-0001`: one result.
- `denim`, all categories: 151 results.
- `denim`, spring selected: 47 results.
- The ordinary spring grid rendered person-free outfit images.
- `SPR-0001` modal loaded `img/SPR-0001.webp`, browser natural dimensions 1366 x 2048; its thumbnail was 360 x 540.
- The original-image control linked to `png/SPR-0001.png`. It was not downloaded or independently decoded.
- Source `hit()` filters the category and requires every whitespace-separated query term to match an ID substring, category substring, or keyword prefix after selected Japanese-to-English dictionary translation. No semantic retrieval is implemented in that function.
- Public inline data uses JSON literals `META` and `D`; the script parses these literals without evaluating source JavaScript. It saves only aggregate counts and a source HTML hash, not the underlying dataset.

## Media and Permissions

The site permits free creative use, including commercial works, editing, and reference. It prohibits redistribution, republication, and resale of image data itself, including modified image data. Credit is optional. The creator states the images are fictional text-to-image outputs, not real product photographs, and does not warrant third-party noninfringement. The notices also restrict uses depicting real persons or minors and uses contrary to public order and morals.

No source outfit image, grid screenshot, or raw catalog dataset is included in this article package. `catalog-and-workflow.png` is an original chart from aggregate counts plus an editorial workflow suggestion. The eight category labels are translated, with the last identified as the site's label. This is a report of the published notices, not a legal determination or evidence of additional authorization.

## Reproduce

Use Node.js and the bundled `@napi-rs/canvas` package:

```sh
node 2026-10-29/imgs/ai-costume-gallery-outfit-reference/audit-and-chart.mjs /path/to/node_modules
```

The command fetches the current page and regenerates `data-audit.json` and the original chart. The source is mutable: compare the HTML hash and retrieval time, and do not interpret a later run as the same snapshot. The review-date label must be updated for a new review.

The audit checks record count, ID uniqueness, category counts against declared metadata, and the two denim keyword counts. It does not verify file existence across the catalog, download all images, establish unique garment designs, validate the creator's generation provenance, test any receiving AI model, or clear rights.
