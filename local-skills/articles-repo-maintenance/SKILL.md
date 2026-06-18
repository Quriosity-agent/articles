---
name: articles-repo-maintenance
description: Maintain Peter's articles repo with the correct date-folder layout, bilingual article pairing, and MOC updates.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [articles, markdown, bilingual, repo-maintenance, moc, indexing]
---

# Articles Repo Maintenance

Use this skill when working in Peter's articles repository at `/Users/peter/Desktop/code/articles/` (`Quriosity-agent/articles`).

## Repo conventions

- Main content repo path: `/Users/peter/Desktop/code/articles/`
- **Do not use** a nested `articles/` content subdirectory such as `/Users/peter/Desktop/code/articles/articles/`.
- The correct layout is **one level only**: date folders directly under the repo root, for example:
  - `2026-04-30/2026-04-30-some-article.md`
  - `2026-04-30/2026-04-30-some-article-en.md`
- Each article should have **Chinese and English versions**.
- `MOC.md` must be updated when adding or moving articles.
- `README.md` is the chronological index; `MOC.md` is the topic map.
- User preference: after writing/updating articles in this repo, **commit + push by default without asking**.
- User preference: after the article is finished and pushed, send Peter the final GitHub links for the Chinese and English versions in the completion reply.

## When adding a new article

1. Infer the article date from the filename.
2. Before drafting, search `README.md`, `MOC.md`, and recent date folders for the source URL, project name, or topic keywords. If prior coverage exists, do **not** silently duplicate the same article. Write a distinct follow-up angle (for example: feature reference vs patterns guide, implementation deep dive vs operating playbook) and link/position it accordingly.
3. Ensure the date folder exists **at repo root**.
4. Create both files:
   - `YYYY-MM-DD/YYYY-MM-DD-slug.md`
   - `YYYY-MM-DD/YYYY-MM-DD-slug-en.md`
4. If the source material includes images/screenshots/diagrams, download them into a local article asset folder (recommended: `YYYY-MM-DD/imgs/<slug>/`) and embed them in **both** Chinese and English articles using relative Markdown image links. Do not omit source images unless Peter explicitly asks for text-only.
   - For rendered Next.js image URLs such as `/_next/image?url=<encoded-source>&w=...` or `https://www.anthropic.com/_next/image?url=...`, decode the `url` query parameter and download the original CDN asset, not the resized proxy URL. Verify every relative image link exists before committing.
   - Some product/blog pages (for example MiniMax-style CDN pages) mix Next.js image proxies with direct `filecdn...` URLs and extensionless CDN paths. Download all meaningful body media, run `file <asset>` after download, and rename extensionless assets to the detected type (`.jpg`, `.png`, `.gif`, etc.) before embedding so GitHub/Markdown renderers handle them reliably.
   - If Python `urllib` times out or stalls while downloading CDN-hosted assets, retry with `curl -L --retry 3 --connect-timeout 20 --max-time 180 -A 'Mozilla/5.0' -o <file> <url>` rather than dropping the asset. Verify the downloaded file type with `file` and confirm Markdown references point to existing local files.
   - For pages where `baoyu-url-to-markdown` captures content but misses metadata (for example Anthropic research pages may show the publish date in rendered HTML while not exposing `article:published_time`), inspect the raw HTML or rendered page snippets for the date and use that date folder.
5. Add matching links in `MOC.md`.
6. Verify the new files and any asset folders are in the correct top-level date folder, not under any nested `articles/` directory.
7. Before staging, inspect `git diff -- README.md MOC.md` and the first relevant README section. README table rows must be normal Markdown rows (`| ... | ... |`), not accidentally doubled (`|| ... |`) or inserted into the repo description/header. If editing indexes programmatically, scope insertion to the target date section and verify the exact separator line by scanning for a line containing `------` inside that date section, rather than assuming one exact marker string. After insertion, run a quick grep/diff check for the new rows and fix any leading `||` before commit. When using `read_file`, remember its line-number gutter ends with `|`; a displayed `|| ...` can simply mean the content line starts with a valid Markdown `|`, so confirm suspicious doubled pipes with `git diff`, `sed`, or `repr()` before rewriting.
8. Commit and push.
   - If `git status` contains unrelated untracked/modified files from other concurrent article work, do **not** sweep them into this article's commit. Stage only the files for the current article plus the intended `README.md`/`MOC.md` index changes and assets. After push, mention any unrelated remaining dirty state briefly so Peter understands it was intentionally excluded.
   - If you need `git pull --rebase origin main` before pushing but the current article has unstaged changes, use a scoped stash for only this article's files (for example `git stash push -u -m '<article-slug>' -- README.md MOC.md YYYY-MM-DD/`), then `git pull --rebase origin main`, `git stash pop`, resolve if needed, and continue with selective staging. Do not use a broad stash that might hide unrelated user work.
9. After pushing, verify the GitHub/raw URLs are reachable (e.g. `urllib.request.urlopen` or `curl -I`) before sending links to Peter.

### Source-doc and official-doc article angle control

When the source is an official documentation page rather than a GitHub repo or social post, keep the article analytical and operational instead of mirroring the docs. If there is already an article on a related doc page, explicitly choose a non-overlapping angle, such as:

- feature mechanics/reference (`delegate_task` parameters, lifecycle, constraints);
- workflow patterns (`parallel research`, code review, compare alternatives, gather-then-analyze);
- operational playbook (prompt templates, verification, least-privilege toolsets);
- troubleshooting/configuration notes.

Use the official doc URL in the metadata block and verify the article does not merely restate the prior article's outline.

## When fixing structure

If files are misplaced under a nested `articles/` directory or sitting in the repo root instead of a date folder:

1. Parse the leading `YYYY-MM-DD` from each filename.
2. Move each file into the corresponding **top-level** date folder.
3. Update all `MOC.md` links from old forms such as:
   - `[[articles/YYYY-MM-DD/YYYY-MM-DD-slug|...]]`
   - `[[articles/YYYY-MM-DD-slug|...]]`
   to
   - `[[YYYY-MM-DD/YYYY-MM-DD-slug|...]]`
4. Re-scan for remaining files under any nested `articles/` directory.
5. Re-scan for missing bilingual pairs.
6. Commit and push.

## Cleanup of stale temporary/source files

When the user asks whether `tmp`, `_tmp`, Python scripts, or other non-article files are needed in the articles repo, inspect before deleting:

1. Check tracked/untracked state and gitlinks/submodules:
   ```bash
   git status --short
   git ls-files -s | grep -E '(^160000 .*tmp|[[:space:]]tmp/|/_tmp/|\.py$)' || true
   git config --file .gitmodules --get-regexp '.*' || true
   ```
2. For top-level `tmp/` or `_tmp/` entries, treat empty `160000` gitlinks with no `.gitmodules` mapping as stale unless a Markdown file or index directly references them. Remove with `git rm -r <path>`, remove the now-empty parent directory, add `tmp/` and `_tmp/` to `.gitignore`, then commit/push.
3. For Python files:
   - Root-level one-off maintenance scripts (encoding fixes, local migration helpers, hard-coded local paths) usually do **not** belong in the article repo; remove them after confirming no Markdown/index references.
   - Article-local asset generator scripts may belong if they reproduce committed images/diagrams referenced by articles. Prefer keeping them, but replace absolute machine-specific paths with relative paths such as `os.path.dirname(os.path.abspath(__file__))` and run the script to verify outputs still regenerate.
4. After cleanup, verify `git status --short` is clean after commit/push and re-scan for remaining tracked `tmp/`, `_tmp/`, or unintended root scripts.

## Pair verification check

Use a quick scan to ensure every base article has both languages:

- Chinese file: `base.md`
- English file: `base-en.md`

A valid pair means both exist for the same base path.

## Running article jobs via cron/background agents

When Peter asks to "cronjob" or otherwise schedule an article writeup from a URL, create a one-shot job rather than writing it inline. Use `deliver="origin"` so the completed job posts back to the same Discord thread. Include this skill in the job, enable at least `web`, `browser`, `terminal`, `file`, and `skills`; add `vision` for X/Twitter or visual/media-heavy sources. Schedule it for about one minute in the future using a tool-derived current time, and prompt the child agent to follow this repo's bilingual layout, image preservation, README/MOC updates, selective staging, commit/push, and GitHub link verification. Reply immediately with the cron `job_id`, source URL, and that the job will return links when complete.

When Peter wants multiple article jobs to run **now** and concurrently, prefer independent background Hermes processes over cron jobs or `delegate_task`. Use `terminal(background=true, notify_on_complete=true)` with one `hermes chat -q <prompt> --source <article-job-tag>` per article so each job survives Discord turn interrupts and can be polled by process session id. Do not wrap the command with shell backgrounding such as `nohup`, `&`, `disown`, or `setsid`; let the terminal tool manage lifecycle. For concurrent jobs in the same articles repo, instruct each child to use selective staging and `git pull --rebase` before push; for maximum safety, use a separate git worktree or temp clone per article and merge/index updates afterward. Avoid `delegate_task` for full article write/commit/push workflows because delegated children are synchronous to the parent turn and are not durable background workers.

## Completion reply checklist

After writing, verifying, committing, and pushing an article task, send a concise final reply that includes:

- Chinese article GitHub link and English article GitHub link.
- Commit hash/message when available.
- A brief note that `README.md`/`MOC.md` and local assets were updated if applicable.
- A brief note that GitHub/raw links were verified. Do not re-run completed work after context compaction; if the handoff says the repo is clean and links are verified, only report the result.

## Suggested verification steps

- List repo-root date folders and confirm article files live there.
- Search `MOC.md` for old broken `articles/...` paths.
- When verifying index links, remember `README.md` uses literal `.md` links while `MOC.md` uses Obsidian wikilinks without `.md`; verify MOC by searching for the slug/base path (e.g. `YYYY-MM-DD/slug` and `YYYY-MM-DD/slug-en`), not only `slug.md`.
- Scan all target article files for missing `-en.md` or missing Chinese counterpart.
- Review `git status` before commit.
- If an existing single-language article already exists, prefer **migrating + pairing** it instead of rewriting the original from scratch.
- For data/table-driven articles, verify the article contains concrete evidence, not just high-level analysis: name the specific companies/items, group them by category, and add an appendix/table with the underlying records when useful. If the user asks for “每家公司一段” / one paragraph per item from an image/table, preserve the original screenshot as a local asset, create a clearly numbered section for every source row, count the generated headings against the source count (for example 63 rows → 63 `###` headings in each language), and include a short caveat when some companies are stealth or only partially public.
- For X/Twitter article writeups, inspect the source page for images (`document.querySelectorAll('img')` or the X-to-Markdown media workflow), save meaningful media locally, and verify every image referenced in Markdown exists and is pushed.
- When an X/Twitter post is mainly a pointer to an external article, launch page, GitHub repo, model card, demo, or docs page, resolve the outbound link first (record both the X post and canonical external URL in the article metadata), then ground the writeup in that canonical source and any official docs it links to. This avoids unnecessary reverse-engineered X API usage while preserving the social source context.
- For X/Twitter posts that summarize a GitHub/model release, treat the post as social framing and verify concrete claims against authoritative sources before writing: README/docs/model cards, GitHub API metadata, release notes, and benchmark tables. If the post conflicts with the canonical source (for example parameter counts, license, star count, model size, supported languages, dates), explicitly note the correction and cite the canonical value rather than repeating the post's claim.
- For X/Twitter posts announcing an open-weight model or model leaderboard result, ground the article in the social post **plus** the official model/product page, GitHub README, Hugging Face collection/model cards, and benchmark images/tables. Preserve the tweet image and any official benchmark charts as local assets, and explicitly separate “open weights / open code” from commercial licensing rights when licenses are non-commercial or gated.
- For X/Twitter posts that point to a research/code/tutorial project, resolve all outbound links, then ground the article across the social post, canonical tutorial/product page, GitHub README/API metadata, and a shallow clone when useful. Inspect repo guidance files such as `CLAUDE.md`/`AGENTS.md`, experiment folders, figures, and infra docs; these often reveal the operational workflow and agent affordances better than the landing page alone. Preserve meaningful project visuals by combining rendered page screenshots, app/demo screenshots, X media thumbnails, and repo experiment figures when they substantively support the article.
- For X/Twitter posts that announce an official product/platform page but the rendered X page does not expose the outbound `t.co` link, use the X title/snapshot text as social context, search the exact announcement/topic to find the canonical official page, then ground the article in that page plus linked docs/release notes. Record both the X URL and canonical official URL(s) in the article metadata.
- For X/Twitter article cards or longform teasers that click through to `/i/article/<id>` behind a login wall, use `references/x-article-canonical-blog-cards.md`: preserve the original X status URL as `source`, record the discovered `x_article` id if visible after clicking, search exact card/title text to find the canonical public blog/article, and ground the writeup in that canonical page. Use DOM extraction such as `document.querySelector('article').innerText` on the canonical page when web extraction truncates. If `browser_get_images` only finds avatars/profile images and no meaningful body figures, proceed text-only rather than creating empty assets.
- For X/Twitter article cards whose canonical source is Substack or another public longform page with multiple figures, use `references/x-article-substack-roadmap.md`: extract the full article text and meta via browser DOM, decode Substack `image/fetch/.../<encoded-original-url>` URLs to original `substack-post-media` assets, download meaningful figures locally, optionally create a temporary contact sheet for triage, and remove that contact sheet before commit unless deliberately embedded. If the repo already has a broad article on the same concept, choose a distinct operational angle rather than duplicating the previous thesis.
- For long text-only X/Twitter posts, the browser snapshot/title may truncate while `document.querySelectorAll('article').map(a => a.innerText)` often exposes the complete post text even behind login/signup overlays. Use DOM article text as the quote source; use `browser_vision` mainly for screenshot evidence. If the post contains visible `t.co` outbound links, resolve them with `browser_navigate` one at a time and inspect the canonical pages before writing; browser navigation is more reliable than batch URL fetches for redirect-heavy `t.co` links.
- For X/Twitter Articles or longform posts with many inline tutorial screenshots/media, use `references/x-article-longform-media.md`: extract full `article.innerText`, download `pbs.twimg.com/media` assets as `name=orig`, preserve original frames locally, create readable WebP contact sheets for embedding, and avoid copying ad-like personal contact snippets from the social post into the article.
- For X/Twitter posts with embedded video/GIFs or login overlays where direct media extraction is impractical, use `browser_vision` to capture a screenshot of the visible post as an article asset, and describe the thumbnail/frame in the article only as context. Prefer pairing that with screenshots from the canonical page/scorecard/docs when those pages contain the authoritative data.
- For X/Twitter video/demo launch posts where `yt-dlp` can extract the media, use `references/x-video-product-launches.md`: download the video/thumbnail, extract representative frames or contact sheets, remove bulky `.mp4` files before commit unless explicitly needed, and ground the article in the canonical product/project/dataset/docs pages rather than the video alone.
- For X/Twitter posts where the main evidence is an image/table in the post, use `browser_get_images` to locate the `pbs.twimg.com/media/...` asset, download the `name=orig` variant with `curl -L`, inspect it with vision/OCR, and embed it locally in both language versions. Treat the image as source evidence, but ground broad technical claims in canonical sources (paper/project pages/docs). If web search is blocked by anti-bot pages, use authoritative APIs/pages directly where possible (for example arXiv API/abstract pages, official project pages, GitHub READMEs) rather than relying on search snippets.
- For external product-announcement pages, capture authoritative operational details from linked docs in addition to the marketing blog when available (commands, state files, lifecycle behavior, limitations). Keep the article analytical rather than a plain summary.
- For Google Keyword / Google AI launch pages (`blog.google`, especially Gemini/AI product announcements), use `references/google-keyword-source-pages.md`: use the canonical URL and source publish date, preserve meaningful Google CDN/video assets locally, inspect linked Google AI docs/model cards/help pages for operational constraints, and distinguish launch claims from current product limits.
- For OpenAI official news/product pages, use `references/openai-news-pages.md`: if the JS-rendered article is incomplete or Cloudflare-protected, verify existence and metadata through OpenAI RSS plus sitemap, record the RSS summary in article metadata, and keep claims cautious unless official full text or linked docs are available.
- For benchmark/leaderboard/community-scorecard sources, use `references/benchmark-leaderboard-pages.md`: collect the headline row plus linked detail page/scorecard; record rank, score, cost/spend, date, environment/level counts, episodes, actions/resets, code links, verification regime, and whether results are self-reported or independently verified. Treat social posts as framing, but ground numbers in the leaderboard, scorecard, paper, and official repository.
- For X/Twitter posts announcing TTS, STT, or real-time voice-agent model benchmark results, use `references/voice-agent-benchmark-sources.md`: preserve tweet leaderboard screenshots locally, resolve official product/docs/model pages, verify Artificial Analysis or similar benchmark methodology pages, distinguish streaming vs non-streaming STT and TTS quality vs latency, and explicitly note when a live dynamic leaderboard has changed from the screenshot rather than repeating “#1” as an evergreen fact.
- For JS-rich research/product pages with embedded diagrams, demos, benchmark tables, audio/video, or inline SVG/CSS figures, use `references/js-rich-source-pages.md`: probe `img`, `video`, `audio`, `figure`, `table`, and outbound links via the browser DOM; download meaningful raster assets; summarize inline diagrams when no reliable export exists; verify local images plus GitHub blob/raw URLs after push.
- For official model launch/blog/model-card sources (LLM or multimodal model releases, especially open-weight releases with benchmark charts), use `references/model-launch-source-pages.md`: ground the writeup across the launch blog, official docs/API page, Hugging Face/ModelScope card, GitHub repo, linked papers, and benchmark pages; preserve official charts locally as WebP; state harness/leaderboard caveats; separate open weights from practical serving cost; and choose a non-overlapping angle if the repo already has coverage of the model family.
- For Next.js/MDX company blogs where raw HTML is huge or slow to process (for example GitButler-style blog pages), prefer `browser_navigate` + `browser_console` DOM extraction over repeated raw-HTML terminal scraping: collect `document.querySelector('main').innerText`, `document.images` (`currentSrc`, `alt`, dimensions), meta tags (`article:published_time`, author, `og:image`), and main links in one structured object. Decode `/_next/image?url=<encoded-source>&w=...` to the original asset URL before downloading, preserve meaningful body figures locally, and verify image types/sizes before commit.
- For interactive JS/WebGL app pages where a plain headless screenshot captures an empty/default state, use `references/js-app-screenshot-cdp.md`: drive Chrome through the DevTools Protocol, click product UI such as “Load Sample Project”, capture the useful app state, convert to WebP, and verify with vision before embedding.
- For product landing pages that link companion API docs, SDK docs, pricing, or Scalar/OpenAPI references, use `references/product-landing-api-docs.md`: ground positioning in the landing page, operational claims in the docs/OpenAPI JSON, preserve verified landing-page screenshots, and include trust/safety analysis for sensitive categories like identity intelligence, face search, KYC, or OSINT.
- For community-hosted, unofficial, leaked, or allegedly leaked prompt/spec/config sources, do **not** present product names, model strings, launch claims, or roadmap details as confirmed facts. Frame the piece as analysis of a public sample/specimen unless an official source verifies it; add an explicit note in metadata/body that authenticity is unconfirmed, and focus the article on durable architecture lessons such as harness design, policy layering, tool contracts, runtime verification, and product implications.
- When an article source links companion PDFs that contain the authoritative proof, remarks, or technical appendix, download them and extract the first pages/full text for grounding before drafting. If `pdftotext` is unavailable, install/use Python `pypdf` for extraction; do not base a technical article only on the marketing/blog page when PDFs are the primary evidence.
- When drafting Markdown programmatically, avoid Python f-strings around article bodies that contain literal braces/backslashes, including LaTeX (`\\mathbb{Z}`), JSON/JSON5 examples (`{ "id": "..." }`), or config snippets. They can be parsed as f-string expressions and fail before writing. Prefer raw triple-quoted templates plus explicit placeholder replacement for titles, dates, source text, slug, and image paths.
- When client-rendered charts/tables cannot be downloaded as standalone images, capture a full-page screenshot, crop readable sections with PIL into local WebP article assets, and verify the crops with vision before embedding. Do not embed an enormous raw full-page screenshot if a focused crop communicates the evidence better.
- For WeChat/微信公众号 source articles (`mp.weixin.qq.com`), use the workflow notes in `references/wechat-source-articles.md`: capture text with Baoyu URL-to-Markdown, but use a rendered browser page plus full-page scrolling/DOM image extraction for complete media preservation.
- For Tencent Docs source documents (`docs.qq.com/doc/...`), use `references/tencent-docs-source-articles.md`: the visible page may expose only title/outline/word count, while full text is embedded in the `/dop-api/opendoc` JSONP payload under `clientVars.collab_client_vars.initialAttributedText.text[0]` as base64-encoded protobuf-like bytes containing UTF-8 text. Extract and clean that text, compare headings against the visible outline, then write an analytical article rather than mirroring the prompt dump.
- For Substack / Dwarkesh-style source articles, use `references/substack-source-articles.md`: extract full text from `article.innerText`, pull `datePublished` and hero images from meta/JSON-LD/raw HTML, prefer original `substack-post-media.s3.amazonaws.com` images over resized proxies, and crop full-page screenshots into focused assets before committing.

## Pitfalls

- Do not put new article files under `articles/articles/...` or `articles/YYYY-MM-DD/...`.
- The correct path style is `repo-root/YYYY-MM-DD/file.md`.
- Do not add only one language version unless the user explicitly asks for a one-language draft.
- Do not forget source images: Peter expects article tasks based on visual/social posts to include the relevant original images, not just text analysis.
- When moving files, update `MOC.md` paths in the same task.
- Repo-level scans may show many legacy patterns outside the requested scope; only normalize the scope requested unless asked to refactor the entire repository.
