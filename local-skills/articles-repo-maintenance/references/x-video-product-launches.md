# X/Twitter video product launches: article grounding + media workflow

Use when Peter asks for an article from an X/Twitter post where the post is primarily a launch/demo video and the canonical product/project page contains the durable details.

## Workflow

1. Treat the X post as social framing, not the only source.
   - Extract visible post text with `document.querySelectorAll('article').map(a => a.innerText)`.
   - Capture/download X media when meaningful; for video posts, prefer `yt-dlp` for the actual video and thumbnail.
2. Resolve the canonical source.
   - If X does not expose the outbound link because of login overlays, use exact project/company/product terms from the post and the author profile text to find the official site, app, docs, GitHub/Hugging Face/model card, or whitepaper.
   - Record both the X URL and the canonical URL(s) in article metadata.
3. Preserve visual evidence locally, but do not commit bulky raw videos by default.
   - Useful commands:
     - `yt-dlp --no-playlist --write-thumbnail --convert-thumbnails jpg -o "$D/x-video.%(ext)s" '<x-url>'`
     - `ffmpeg -y -ss 00:00:03 -i "$D/x-video.mp4" -frames:v 1 "$D/x-video-frame.jpg"`
   - Save official page screenshots/posters/frames and build a readable contact sheet for embedding.
   - After extracting frames/contact sheets, remove large `.mp4` files unless the video itself is explicitly part of the article deliverable.
4. For 3D/AI/product launches, ground the analysis in durable details from official pages and data sources:
   - mission/positioning from the homepage;
   - product capability bullets from the launch/release section;
   - dataset/model facts from Hugging Face/GitHub/arXiv/API pages;
   - benchmark claims with caveats when the full report is gated or not reproducible.
5. Before commit, verify all Markdown image references exist locally, run `git diff --stat`, stage selectively, commit/push, and verify GitHub blob/raw URLs.

## Pitfalls

- Do not base a technical article only on a flashy X video when the official site/model card/dataset page contains the claims Peter will care about later.
- Do not commit 50MB+ demo videos just because `yt-dlp` downloaded them. Extract representative frames/contact sheets and keep the repo lean.
- Be cautious with self-reported benchmarks from launch pages. Present them as official claims and note when the full benchmark report is gated or not independently reproducible.
- If batch scripting large article writes is blocked by the runtime consent guard, stop and ask for permission instead of trying to bypass it. After consent, continue through normal file-write tools and verify the result.