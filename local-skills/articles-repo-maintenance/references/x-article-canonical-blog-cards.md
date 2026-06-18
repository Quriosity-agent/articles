# X article cards that point to canonical blog posts

Use this note when an X/Twitter source is an article card or teaser for a longer post, especially when the public X page shows only a card and clicking it redirects to `/i/article/...` behind a login wall.

## Pattern

1. Open the X URL in the browser first.
2. Capture the publicly visible evidence from the snapshot/title:
   - author/handle;
   - card title/cover alt text;
   - timestamp and engagement metadata if visible;
   - any `/i/article/<id>` redirect revealed after clicking the card.
3. Do **not** block on reverse-engineered X export if the task is to write an article rather than archive the tweet.
4. Search exact card text or title fragments to find the canonical external post. For Addy Osmani-style posts, likely canonical URLs may live on `addyosmani.com/blog/...` or Substack mirrors.
5. Ground the article in the canonical post, not only the X card. Record both URLs in frontmatter:
   - `source`: original X status URL
   - `canonical`: canonical blog/article URL
   - `x_article`: `/i/article/<id>` if discovered
6. Use browser DOM extraction on the canonical page when `web_extract` truncates the article:
   - `document.querySelector('article').innerText`
   - article links via `article.querySelectorAll('a')`
7. Check `browser_get_images` on both the X page and canonical page. If only avatars/profile images are present and there are no meaningful body figures, do not create an empty asset folder; simply proceed text-only.
8. Verify the final bilingual files, README/MOC rows, commit/push, and GitHub blob/raw links as usual.

## Why this matters

X cards often expose enough public metadata to identify the real source even when X longform content is login-gated. The article should preserve the social source context while using the canonical page for the technical analysis and citations.