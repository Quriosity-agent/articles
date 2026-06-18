# Google Keyword / Google AI source pages

Use when writing articles from `blog.google` / Google Keyword launch posts, especially Gemini/AI product announcements.

## Extraction pattern

1. Use the canonical URL from `link[rel=canonical]`, not the campaign-parameter URL, in article metadata.
2. Prefer the source publish date shown in the article (for example `Jun 09, 2026`) for the repo date folder, even if the task is run later.
3. Capture `document.querySelector('article')?.innerText`, plus metadata:
   - `document.title`
   - `meta[name=description]`
   - `meta[property="og:image"]`
   - all `article img`, `article video/source`, and `article a` nodes.
4. Download meaningful source media into `YYYY-MM-DD/imgs/<slug>/` and embed in both language versions:
   - hero / OG image from Google storage CDN;
   - relevant YouTube thumbnails when the article embeds demo videos;
   - a representative frame from downloadable MP4 demos when the page links a video download.
5. Verify downloaded media with `file`; for MP4 demos, extract a readable frame with ffmpeg rather than committing the whole video unless the user explicitly asks for video assets.
6. Inspect linked official docs/model cards/help pages when they contain operational detail the launch post omits. For Gemini Live Translate-style posts, useful companion sources include:
   - Google AI Developers API docs for model names, config fields, preview status, and code/API shape;
   - Google DeepMind model cards for evaluation dimensions, latency definitions, safety/watermarking notes;
   - product Help Center pages for current rollout limits, admin controls, privacy claims, and device restrictions;
   - official GitHub examples or partner docs for runtime architecture.
7. Keep the article analytical: distinguish launch narrative from deployable product constraints. Separate “model capability” from “product rollout/current beta limitations.”
8. Verify all Markdown image links locally before staging, then verify GitHub blob/raw article URLs and at least one raw image URL after push.

## Useful framing angles

- Treat real-time AI product launches as runtime/infrastructure changes, not just feature announcements.
- For Gemini Live API / audio products, call out stream-vs-request architecture: WebSockets, long-lived sessions, audio tracks, latency budgets, language state, permissions, privacy, and watermarking.
- When official docs separate specialized modes (for example Live Agent vs Live Translation), preserve that boundary in the article; do not blur a dedicated low-latency pipeline into a general-purpose agent.
