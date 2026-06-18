# Benchmark / leaderboard source pages

Use this reference when writing articles from benchmark homepages, leaderboards, scorecards, or research launch pages (for example AI evals, model leaderboards, security benchmarks).

## Source collection checklist

1. Treat the public website as the primary rendered source, but collect backing sources too:
   - official paper / arXiv abstract;
   - GitHub README and docs;
   - Hugging Face / dataset pages if linked;
   - detail pages for individual scorecards, environments, or rows when available.
2. On JS-rich benchmark pages, extract structured evidence from the browser DOM:
   ```js
   ({
     title: document.title,
     text: document.body.innerText,
     headings: [...document.querySelectorAll('h1,h2,h3')].map(h => h.innerText),
     tables: [...document.querySelectorAll('table')].map(t => t.innerText),
     links: [...document.querySelectorAll('a,button')].map(a => ({text: a.innerText.trim(), href: a.href || null}))
   })
   ```
3. Preserve the article's key visual evidence locally. If the benchmark uses inline SVG/CSS charts or complex client-rendered tables that are hard to download directly, capture a full-page screenshot with `browser_vision`, then crop it with PIL into readable article assets and save as WebP:
   ```python
   from pathlib import Path
   from PIL import Image
   src = Path('/path/to/fullpage.png')
   outdir = Path('YYYY-MM-DD/imgs/<slug>')
   outdir.mkdir(parents=True, exist_ok=True)
   im = Image.open(src)
   im.crop((0, 0, im.width, 2500)).save(outdir/'hero-leaderboard.webp', 'WEBP', quality=82, method=6)
   ```
   Verify each crop with vision before embedding; full-page screenshots can be extremely tall and unreadable if embedded raw.
4. For leaderboard tables, include concrete fields rather than only qualitative claims: rank, model/regime, score/percentage, tier reach, mean/cost/spend, environment count, episode count, and verification regime where available.
5. Explain methodology limits separately from headline results: held-out status, whether zero-day discovery is measured, whether results are self-reported or independently verified, harness/scaffolding effects, and whether the benchmark measures full weaponization.

## Article structure that works well

- TL;DR with the benchmark's central thesis and headline signal.
- “What it measures” section that defines the benchmark axis or tiers.
- “Why this target/domain” section explaining target choice and realism.
- Concrete top-line results table.
- Methodology / verification section describing judge/oracle, harness, seeds, cost, and reproducibility.
- “Why the capability map matters more than the leaderboard” section when per-environment matrices exist.
- Comparison to related benchmarks.
- Practical implications and limitations.
