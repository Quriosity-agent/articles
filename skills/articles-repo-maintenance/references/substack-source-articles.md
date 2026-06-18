# Substack / Dwarkesh-style source articles

Use when the source article is a Substack post or Dwarkesh Podcast page.

## Extraction pattern

1. Load the canonical URL in browser tooling and capture the full article with:
   ```js
   ({
     title: document.title,
     text: document.querySelector('article')?.innerText || document.body.innerText,
     links: [...document.querySelectorAll('article a')].map(a => ({text: a.innerText, href: a.href})),
     imgs: [...document.querySelectorAll('article img')].map(img => ({alt: img.alt, src: img.currentSrc || img.src, w: img.naturalWidth, h: img.naturalHeight})),
     meta: [...document.querySelectorAll('meta')].map(m => ({name:m.getAttribute('name'), property:m.getAttribute('property'), content:m.getAttribute('content')})).filter(x => x.name || x.property)
   })
   ```
2. Substack pages often expose the complete text in `article.innerText` even when a subscribe modal overlays the browser snapshot. Do not rely only on the accessibility snapshot.
3. For dates and images, inspect raw HTML or JSON-LD for `datePublished`, `dateModified`, `og:image`, `twitter:image`, and source image URLs.
4. Prefer downloading the original `substack-post-media.s3.amazonaws.com/public/images/...` asset when available, rather than only the resized `substackcdn.com/image/fetch/...` proxy. Use `curl -L --retry 3 --connect-timeout 20 --max-time 180 -A 'Mozilla/5.0'`.
5. Capture a browser screenshot as secondary evidence if useful. If the screenshot is a very tall full-page capture, crop it to a focused header/section before committing; avoid huge, unreadable screenshots as article assets.
6. Keep the writeup analytical, not a mirror of the source. For conceptual essays, extract the thesis, historical examples, and operational implications for builders.
7. Verify every relative Markdown image link exists locally, then after push verify both article blob/raw URLs and at least one raw image URL.

## Pitfalls

- The subscribe modal is not a failure state; close it if convenient, but DOM extraction usually still works.
- Article `img` nodes may include avatars or comment profile images. Do not embed those unless they add substantive value. Prefer the source article hero/OG image plus a cropped article-header screenshot.
- Do not stage a full-page Substack screenshot if it includes comments/recommendations/footer and is much larger than needed for the article.