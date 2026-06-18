# OpenAI official news/product pages

Use these notes when Peter asks for an article based on an OpenAI `openai.com/index/...` announcement and the rendered page is JS-heavy, Cloudflare-protected, or only partially accessible.

## Durable workflow

1. Treat the user-provided OpenAI URL as the canonical source, but gather metadata from the RSS feed first:
   - `https://openai.com/news/rss.xml`
   - `https://openai.com/blog/rss.xml` often mirrors the same feed.
2. Locate the `<item>` whose `<link>` or `<guid>` matches the source URL (normalize trailing slash). Capture:
   - title
   - description / summary
   - link / guid
   - category
   - `pubDate`
3. Check `https://openai.com/sitemap.xml` and likely child sitemaps such as `https://openai.com/sitemap.xml/page/` for related canonical landing pages, forms, or product pages (for example a `gpt-rosalind` launch page linked by the same topic).
4. If the full article body is not reliably extractable, do **not** invent specific claims. Write the article as an analytical take grounded in the verified RSS summary and official URL, and explicitly include an `RSS summary` metadata line so readers can see the factual basis.
5. Keep the analysis at the capability/workflow/product-strategy level unless you have authoritative detailed body text, docs, or linked technical material.
6. Still follow the repo workflow: bilingual articles, README/MOC updates, selective staging, commit/push, and GitHub blob/raw verification.

## Example metadata block

```md
- **Source:** [Introducing new capabilities to GPT-Rosalind](https://openai.com/index/introducing-new-capabilities-to-gpt-rosalind/)
- **RSS summary:** “GPT-Rosalind advances life sciences research with enhanced biological reasoning, medicinal chemistry expertise, genomics analysis, and experimental workflow capabilities.”
- **Published:** 2026-06-03
- **Category:** Product
```

## Pitfalls

- Do not treat a Cloudflare/Next.js fallback page as evidence that the article does not exist; verify via RSS and sitemap.
- Do not over-claim detailed benchmarks, access rules, model architecture, customer names, or safety policies unless they appear in accessible official text or linked docs.
- Do not drop the original URL just because a related landing page appears in the sitemap; record both when useful.
