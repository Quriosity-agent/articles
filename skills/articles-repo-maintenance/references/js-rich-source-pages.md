# JS-rich source pages for article writeups

Use when an article source is a modern, JS-heavy research/product page with embedded diagrams, demos, media, or tables.

## Extraction pattern

1. Load the page in browser tooling and capture `document.body.innerText` for the full article text, headings, footnotes, benchmark tables, and citation block.
2. Use DOM probes to inventory non-text assets:
   ```js
   [...document.querySelectorAll('img')].map(img => ({src: img.currentSrc || img.src, alt: img.alt, width: img.naturalWidth, height: img.naturalHeight}))
   [...document.querySelectorAll('video,source,audio')].map(e => ({tag: e.tagName, src: e.currentSrc || e.src, type: e.type, poster: e.poster}))
   [...document.querySelectorAll('figure,table,h2,h3')].map(e => ({tag: e.tagName, text: e.innerText.slice(0,1000), html: e.outerHTML.slice(0,500)}))
   [...document.querySelectorAll('a')].map(a => ({text: a.innerText, href: a.href}))
   ```
3. Download meaningful raster assets into `YYYY-MM-DD/imgs/<slug>/` and embed them in both language versions. Prefer the source asset URL (`currentSrc` / original CDN URL) over resized proxies.
4. For diagrams rendered as inline SVG/CSS rather than standalone images, do not invent a screenshot. Summarize the diagram's meaning in the article unless a reliable screenshot/export workflow is available.
5. Inspect important outbound links that ground the article's technical claims (papers, GitHub PRs/repos, docs, product pages, model cards). Capture titles/descriptions or key implementation facts.
6. If downloaded source images are large (especially multi-MB PNG hero/screenshots), compress them before staging, preferably to WebP via `baoyu-compress-image`, and update Markdown links to the compressed filenames. Verify the raw image URL after push.
7. Verify local Markdown image links by resolving them relative to each article file before staging.
8. After push, verify both GitHub blob URLs and raw Markdown URLs with `HEAD`/`urlopen`; verify at least one referenced raw image URL when images were added.

## Notes from Thinking Machines Lab-style pages

- The visible page may include raster hero/thumbnail/frame images plus inline SVG/CSS diagrams and audio/video demos.
- Benchmark tables can usually be captured from DOM `table.innerText` even when charts/plots are rendered with SVG.
- GitHub PR pages can be checked for `og:description` to capture concise implementation detail without scraping the full discussion.

## Notes from academic project pages with interactive 3D/model viewers

- For research landing pages that combine a project page, paper link, code link, video, raster thumbnails, and interactive 3D viewers (`model-viewer`, GLB/STL, embedded iframes), treat the task as a hybrid source: extract DOM text/assets from the project page, fetch authoritative paper metadata (arXiv/OpenReview when linked), and inspect the linked GitHub repo when available.

## Notes from self-contained research blog pages with `data:` media

- Some research blogs ship the whole article as a large static HTML file with meaningful figures embedded directly as `data:image/...;base64,...` URLs, including PNG/JPEG/GIF diagrams. Do not discard these as placeholders: decode the base64 payloads into `YYYY-MM-DD/imgs/<slug>/`, choose stable descriptive filenames, run `file <asset>` to verify extensions, and embed the meaningful decoded images/GIFs in both language versions.
- When the page also contains `video` nodes with `data:` posters or inline media, prefer preserving the article's explicit `img`/GIF figures first; only save the inline video if it is small and clearly needed. A readable first/last-frame pair or framework GIF often communicates the source evidence without committing a huge embedded MP4.
- BeautifulSoup text extraction from such pages may show mojibake for emoji/arrow characters even when the substantive text is intact. Normalize key metadata manually from visible text/HTML (title, authors, date, source URL) and avoid copying corrupted symbols into the article frontmatter.
- Inventory `model-viewer` sources separately from `img` nodes. If the 3D outputs are GLB/STL and there is no reliable static render workflow in the current task, do not drop visuals entirely: capture a readable browser screenshot of the hero/demo area and build a small contact sheet from meaningful raster inputs/examples. Embed the screenshot/contact sheet in both language versions.
- Verify screenshots/contact sheets with vision before committing; ensure they are not narrow, blank, or mostly whitespace. This is especially important for pages where interactive model panels may load differently than static images.

## Notes from JS/canvas-heavy product research posts

- Some source pages render key evidence (leaderboards, line charts, interactive diagrams) as `<canvas>` rather than downloadable images. First capture the numeric/semantic fallback from `canvas[role=img][aria-label]` and surrounding captions; then preserve the visual evidence with a browser or headless-Chrome screenshot crop.
- A reliable local pattern on macOS is:
  ```bash
  CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  "$CHROME" --headless=new --disable-gpu --hide-scrollbars \
    --window-size=1400,6000 \
    --screenshot="$asset_dir/full-page.png" "$url"
  ```
  Crop the relevant chart/diagram sections with PIL, convert crops to WebP, and delete the huge full-page PNG before staging.
- When an interactive comparison uses many full-resolution example images, do not embed every large raw image in the article body. Keep source assets if they are valuable, but create focused WebP contact sheets for the article (for example prompt-only vs all-regions, original vs reconstruction stages). Verify the contact sheets are readable before committing.
- In the article, separate exact source claims from interpretation: quote visible chart facts and official text (e.g. leaderboard ordering, CLIP similarity values from aria-label), then frame your analysis as the architectural implication rather than inventing unverified scores.

## Notes from OpenAI Developers / Cookbook pages

- Treat OpenAI Cookbook/tutorial pages as official-doc sources: keep the article analytical and operational rather than mirroring the guide. A good angle is often the runtime/product pattern behind the feature (for example: thread-scoped state, lifecycle controls, evidence checks, budget boundaries) rather than the command syntax alone.
- The rendered page may expose the complete article via `document.querySelector('article')?.innerText`, while `document.body.innerText` includes nav/sidebar noise. Use a DOM probe that captures `article` text plus `main img`, `main a`, and `main pre, main code` inventories.
- Preserve meaningful Cookbook diagrams/screenshots from `developers.openai.com/cookbook/assets/notebook-attachments/...` by downloading the `currentSrc` URLs, converting large PNGs to WebP, and embedding only the diagrams used by the article. Verify diagram readability with vision after compression.
- Cookbook pages often provide both “View on GitHub” and “Download raw” links to the source notebook. Capture those as source metadata when useful, but ground claims in the rendered guide plus the raw notebook only if the rendered page is incomplete.

## Notes from Claude / Webflow-style official blog pages

- `document.body.innerText` can capture the full article even when the browser accessibility snapshot initially looks like only nav/footer. Use a direct DOM text probe before assuming the page failed to load.
- Webflow pages may expose meaningful article images/charts as CDN `img` nodes with `naturalWidth/naturalHeight` reported as `0` because of lazy loading. Still download candidate `og:image` and article `image*.png` assets, then inspect them with vision; keep only images that add technical value (for example OSWorld/thinking-effort charts) and discard decorative SVGs/placeholders.
- For official engineering posts with charts, embed the useful chart images in both language versions near the relevant analysis section, not just the OG image at the top. Compress raster assets to WebP before staging and update Markdown references accordingly.

## Notes from login-gated Flutter/SPAs

- If a source URL resolves to a login screen but the requested route is meaningful (for example `/#/founder_space/client`), do not treat the visible login page as the entire source. Capture the login screenshot as the only verifiable visual evidence, then inspect public app artifacts such as `manifest.json`, `cus_style.js`, `main.dart.js`, route tables, and quoted UI strings.
- For Flutter Web bundles, useful evidence often appears as route names and UI labels in `main.dart.js` even when `document.body.innerText` is empty because the app renders to canvas. Download the bundle with `curl -L -A 'Mozilla/5.0' -o /tmp/<app>.js <script-url>` and search for route fragments, screen names, domain terms, and data-field labels.
- Article claims from bundle strings should be phrased as "public front-end strings/routes indicate" or "the app appears to include" unless authenticated data confirms the behavior. Avoid implying access to private records or screenshots beyond the login page.
- When writing from a login-gated app, separate hard evidence (page title, manifest/product name, login options, route names, visible UI strings) from analysis/implications (what the workflow suggests about the product category). Embed the screenshot in both language versions and verify it exists locally and as a raw GitHub asset after push.