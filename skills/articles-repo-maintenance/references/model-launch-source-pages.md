# Official model launch pages for article writeups

Use when the source is an official model release/blog/model card for an LLM or multimodal model, especially when it includes benchmark charts, architecture diagrams, model-card deployment notes, or agent-runtime claims.

## Source grounding pattern

1. Treat the launch blog as the narrative source, but verify operational claims against companion sources:
   - official API/docs page for model name, context length, output token limits, capabilities, thinking/tool/function-call behavior;
   - Hugging Face / ModelScope model card for license, parameter count, tensor types, supported serving frameworks, and local deployment notes;
   - GitHub repo for series overview, code/examples, license differences, and release lineage;
   - linked papers/arXiv pages for architecture claims such as sparse attention, IndexShare/IndexCache, MTP/speculative decoding, RL infrastructure;
   - linked benchmark sites for methodology, harness, leaderboard context, and caveats.
2. If the repo already has earlier coverage of the model family, choose a distinct follow-up angle. Example: if earlier GLM-5 coverage focused on Slime/DSA technical foundations, a GLM-5.2 article should focus on the long-horizon agent runtime stack: 1M context, effort control, serving, anti-hacking, and benchmark shift.
3. Do not turn official claims into evergreen absolutes. Use phrasing such as “officially reports,” “the benchmark page currently shows,” or “under this harness,” especially for leaderboards and model rankings.

## Media preservation

1. Use browser DOM extraction for JS-rich pages:
   ```js
   JSON.stringify({
     text: document.body.innerText,
     images: [...document.querySelectorAll('img')].map((img, i) => ({
       i, src: img.currentSrc || img.src, alt: img.alt,
       w: img.naturalWidth, h: img.naturalHeight
     })),
     links: [...document.querySelectorAll('a')].map(a => ({text: a.innerText.trim(), href: a.href}))
   })
   ```
2. Download meaningful benchmark/architecture/serving charts into `YYYY-MM-DD/imgs/<slug>/`; skip purely decorative logos unless they support the article.
3. Convert huge PNG charts to readable WebP before committing. Keep enough resolution for chart labels; a max width around 1800px usually works for GitHub-rendered articles.
4. A temporary contact sheet is useful for visual triage and vision verification, but remove it before commit unless the article explicitly embeds it.
5. Verify every Markdown image path exists relative to both the Chinese and English article files; after push, verify at least one raw image URL.

## Analysis angles that work well

- “Long context” as working-memory budget, not just document ingestion.
- Benchmark shift from patch-level coding to hour-scale engineering tasks.
- Thinking/effort controls as runtime scheduling and billing parameters.
- Architecture optimizations as a chain: sparse attention → index reuse → MTP/speculative decoding → KV-cache serving.
- Agentic RL reliability: reward hacking, anti-hack guards, tool-call auditing, and evaluation leakage controls.
- Open-weight reality: license openness versus actual serving cost and infrastructure requirements.

## Pitfalls

- Do not compare agentic benchmark scores as pure model ability when harnesses differ (Claude Code, Codex, Gemini CLI, OpenHands, mini-swe-agent, Terminus, etc.). State the harness where relevant.
- Do not equate open weights with easy local deployment for very large models; separate model-card availability from practical serving requirements.
- Do not omit official charts when they are central evidence; preserve and compress them locally.
- Avoid f-strings when writing Markdown that contains JSON/config snippets or LaTeX braces; use raw templates plus placeholder replacement.
