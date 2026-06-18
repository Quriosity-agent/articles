---
name: articles-repo-maintenance
description: Maintain this articles repository. Use when adding, updating, publishing, indexing, verifying, committing, or pushing articles; when converting source URLs such as WeChat, X/Twitter, Substack, Google/OpenAI/model launch pages, docs, benchmark pages, or product pages into bilingual Markdown articles; and when preserving article images/media, updating README.md/MOC.md, checking bilingual pairs, or returning public GitHub links.
---

# Articles Repo Maintenance

## Core Rules

- Work from the articles repository root.
- Keep article folders directly under the repo root: `YYYY-MM-DD/YYYY-MM-DD-slug.md`.
- Do not create or use a nested `articles/` content directory.
- Create bilingual pairs by default:
  - Chinese: `YYYY-MM-DD/YYYY-MM-DD-slug.md`
  - English: `YYYY-MM-DD/YYYY-MM-DD-slug-en.md`
- Preserve meaningful source media locally under `YYYY-MM-DD/imgs/<slug>/`.
- Embed local relative image links in both language versions.
- Update `README.md` as the chronological index and `MOC.md` as the topic map.
- Commit and push by default after article work unless the user explicitly says not to.
- Return verified GitHub links for Chinese and English articles after pushing.

## Workflow

1. Inspect current state:
   - Run `git status --short --branch`.
   - Check `README.md`, `MOC.md`, and recent date folders for the source URL, project name, slug, or topic keywords.
   - If related coverage already exists, write a distinct follow-up angle instead of duplicating the same article.
2. Resolve source and date:
   - Prefer the source publish date for the folder and filenames.
   - Record canonical source URLs in the article metadata/body when useful.
   - For social posts that point elsewhere, resolve the canonical external page and ground claims there.
3. Preserve media:
   - Download meaningful screenshots, diagrams, benchmark charts, tweet images, page figures, GIFs, or thumbnails.
   - Verify file types with `file` when URLs are extensionless or proxied.
   - Use stable names and embed only local paths.
4. Draft both articles:
   - Write analytical, operational articles rather than plain summaries.
   - Include concrete evidence, caveats, and source-specific context.
   - Use `references/writing-polish.md` for the final structure and humanizing pass.
5. Update indexes:
   - Add matching rows in `README.md`.
   - Add matching wikilinks in `MOC.md` without `.md`.
6. Verify before staging:
   - Check every image link exists.
   - Check each article has its bilingual pair.
   - Check `README.md` links point to real `.md` files.
   - Check `MOC.md` paths point to real article bases.
   - Run `git diff --check`.
7. Commit and push:
   - Stage only the current article files, relevant assets, `README.md`, and `MOC.md`.
   - Do not sweep unrelated dirty files into the commit.
   - If pushing requires a rebase, use a scoped stash for only the current article files.
   - Push to the active branch, normally `main`.
8. Verify public links:
   - Check GitHub blob/raw URLs are reachable before sending them to the user.
   - Mention any unrelated remaining dirty state if intentionally excluded.

## Source-Specific References

Load only the reference needed for the current source:

- WeChat / `mp.weixin.qq.com`: `references/wechat-source-articles.md`
- X/Twitter article cards: `references/x-article-canonical-blog-cards.md`
- X/Twitter longform media: `references/x-article-longform-media.md`
- X/Twitter Substack cards: `references/x-article-substack-roadmap.md`
- X/Twitter videos or demos: `references/x-video-product-launches.md`
- Google Keyword / Google AI launches: `references/google-keyword-source-pages.md`
- OpenAI official news/product pages: `references/openai-news-pages.md`
- Model launches, model cards, open-weight releases: `references/model-launch-source-pages.md`
- Benchmark or leaderboard pages: `references/benchmark-leaderboard-pages.md`
- Voice-agent benchmark sources: `references/voice-agent-benchmark-sources.md`
- JS-rich product/research pages: `references/js-rich-source-pages.md`
- Interactive JS/WebGL apps needing screenshots: `references/js-app-screenshot-cdp.md`
- Product landing pages with API docs: `references/product-landing-api-docs.md`
- Tencent Docs: `references/tencent-docs-source-articles.md`
- Substack / Dwarkesh-style articles: `references/substack-source-articles.md`

## WeChat Shortcut

For `mp.weixin.qq.com` sources:

1. Run Baoyu URL-to-Markdown for text/title/date.
2. Use a browser-rendered page and scroll through the full article to trigger lazy images.
3. Extract `document.images`; prefer `data-src` over transparent SVG `src` placeholders.
4. Keep meaningful `mmbiz.qpic.cn` article assets and filter WeChat chrome such as QR codes, avatars, and follow widgets.
5. Download assets with a WeChat referer and preserve GIFs when present.
6. Verify all local media links before committing.

## Writing Polish

Use `references/writing-polish.md` before finalizing:

- Repair structure before sentence-level polish.
- Remove filler, formulaic AI phrasing, unsupported hype, and vague transitions.
- Preserve facts, caveats, source dates, and technical claims.
- Keep articles analytical and useful: explain why the source matters, what workflow changes, and what teams should verify.

## Completion Reply

After a successful article task, reply concisely with:

- Chinese GitHub link.
- English GitHub link.
- Commit hash and message.
- Note that `README.md`, `MOC.md`, and local assets were updated when applicable.
- Note that public links were verified.
