# X Article card → Substack roadmap/source article workflow

Use when an X/Twitter post is only an article card/teaser and clicking it reveals an `/i/article/<id>` login wall, but search finds a canonical Substack post or similar public article.

## Workflow

1. Open the X status in the browser and capture the visible card text, author, timestamp, view/engagement context, and discovered `/i/article/<id>` if clicking the card redirects to login.
2. Search exact card title/first sentence. Prefer the canonical public article (e.g. Substack) over reverse-engineered X extraction when available.
3. On the canonical article page, use browser DOM extraction rather than only web_extract if the article is long or image-heavy:
   - `document.querySelector('article').innerText` for full text.
   - `document.images` plus meta tags (`og:image`, `twitter:image`, `article:modified_time`, author) for media and metadata.
4. Preserve meaningful body figures locally. For Substack CDN URLs of the form `https://substackcdn.com/image/fetch/.../<encoded-original-url>`, decode the trailing encoded original URL and download the original `substack-post-media.s3.amazonaws.com/...` asset with `curl -L --retry 3 --connect-timeout 20 --max-time 180 -A 'Mozilla/5.0'`.
5. Verify downloaded media with `file`. If there are many article images, make a temporary contact sheet with PIL for visual triage, but remove the contact sheet before commit unless it is intentionally embedded.
6. Write an analytical article that records both:
   - `source`: the X status URL.
   - `canonical`: the public article URL.
   - `x_article`: the discovered `/i/article/<id>` URL when present.
7. If a prior article already covered the broad concept (e.g. Addy Osmani Loop Engineering), choose a distinct angle from the canonical article (e.g. adoption roadmap, four-condition test, minimum viable loop, failure modes) rather than duplicating the earlier thesis.
8. Embed only the figures that support the article; do not mirror every image if some are redundant. Verify each relative image link exists before commit.

## Verification

- `git diff -- README.md MOC.md` shows normal Markdown rows and correct date section.
- Article files contain both X source and canonical URL metadata.
- Every relative image link resolves locally.
- GitHub blob/raw links for both language versions return HTTP 200 after push.
