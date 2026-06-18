# WeChat source article workflow notes

Use when the user asks to write an article from a `mp.weixin.qq.com/s/...` source and preserve media.

## Reliable extraction pattern

1. Run the configured WeChat-to-Markdown extraction workflow first to capture text/title/author/date. If a local Baoyu URL-to-Markdown tool is available, use it like this:
   ```bash
   npx -y bun <path-to-baoyu-url-to-markdown>/scripts/main.ts '<wechat-url>' -o /tmp/wechat-source.md --timeout 60000
   ```
   If that tool is not available, use browser-rendered DOM extraction and keep the source URL in metadata.
2. Do not rely on direct `python requests`/`curl` HTML for media. WeChat often serves an incomplete or script-gated HTML body with missing `mmbiz`, `data-src`, `msg_title`, and lazy-loaded assets.
3. Open the URL in a browser-capable tool, scroll through the whole page to trigger lazy loading, then extract `document.images` fields (`src`, `data-src`, `alt`, dimensions). The real media URLs are often `mmbiz.qpic.cn` URLs and may include GIFs. For WeChat pages that still show transparent SVG placeholders after scrolling, **prefer each image element's `data-src`** over `src`; `data-src` often contains the complete `mmbiz.qpic.cn/...#imgIndex=N` asset even when `src` is a 1px SVG.
4. Filter out WeChat chrome assets such as QR codes, author avatars, follow widgets, and `res.wx.qq.com` UI images. Keep article `data-src` images ordered by `imgIndex` plus the `cover_image` when useful.
5. Download the meaningful article images/GIFs into `YYYY-MM-DD/imgs/<slug>/` with stable ordered names such as `00-cover.jpg`, `01-hero.png`, etc. Use a WeChat referer when downloading (`Referer: https://mp.weixin.qq.com/`) and strip only the local `#imgIndex` fragment, not query parameters such as `wx_fmt`.
6. Embed selected media inline in both the Chinese and English articles. If the source has many assets, add a final media archive section that references any downloaded files not used in the main body so the repository preserves the source visual context.
7. If the WeChat article links a companion technical report/PDF that contains authoritative numbers or methodology, download it and extract text (for example with `pypdf`) before drafting; ground technical claims in the PDF as well as the WeChat summary.
8. Verify every relative image link exists before commit, then commit/push and verify GitHub/raw URLs are reachable.

## Pitfalls

- Markdown converters may capture transparent SVG placeholders instead of real WeChat images.
- Image extraction commands that regex-match `mmbiz.qpic.cn` can trigger hostname/security false positives if the regex escaping is interpreted as a host. Prefer browser DOM extraction or carefully quote/escape shell commands.
- WeChat image URLs are not stable long-term external dependencies; keep local copies in the repo rather than hotlinking.
