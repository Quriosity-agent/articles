# Product landing pages with companion API docs

Use this when an article source is a product landing page that links to API documentation, SDK docs, pricing, or an OpenAPI/Scalar reference.

## Workflow

1. Treat the landing page as product positioning, not the full source of truth. Capture:
   - headline/tagline and primary capability list;
   - product modules/use cases shown on the page;
   - FAQ claims about data sources, privacy, storage, accuracy, and allowed use;
   - pricing/credits if visible.
2. Resolve companion docs from the landing page (for example `API Documentation`, `Docs`, `Developers`, `OpenAPI`, `SDKs`) and ground operational claims there.
3. If the docs are rendered by Scalar/OpenAPI tooling, fetch the OpenAPI JSON directly when available (common paths include `/openapi.json` or URLs embedded in the Scalar client link). Extract:
   - `info.title`, `info.description`, and version;
   - endpoint paths/methods/summaries/descriptions;
   - auth headers, error format, response lifecycle, rate limits, credit costs;
   - async workflow details such as create-and-poll APIs, result expiry, and status values.
4. Preserve useful visuals from the landing page as local assets. For dark, animated, or JS-heavy pages, a full-page headless Chrome screenshot plus focused WebP crops usually works well:
   - hero section;
   - product/module grid;
   - FAQ/compliance/privacy section.
   Verify crops visually and delete useless/blank crops before staging.
5. Be careful with screenshots of API docs rendered by client apps: headless screenshots may capture loading skeletons even when the DOM text/OpenAPI JSON is available. Prefer using the JSON/text as evidence; only embed docs screenshots if verified readable.
6. Compare landing-page pricing/credit claims with API-doc pricing/credits. If they differ, mention the discrepancy carefully as possibly different web-product vs API-product meters rather than assuming one is wrong.
7. For sensitive categories (identity intelligence, face search, KYC, OSINT, surveillance-adjacent tools), include an explicit trust/safety/privacy analysis section:
   - data-source boundaries;
   - probabilistic vs deterministic identity claims;
   - misidentification risk;
   - audit logs, permissions, KYC/usage review, removal/correction mechanisms;
   - risks of API-amplified abuse.
8. Validate article image links locally, scan for accidental secrets/examples that look like real API keys, then selectively stage only the article, assets, and intended README/MOC changes.

## Pitfalls

- Do not rely only on marketing copy when linked docs expose concrete endpoint behavior.
- Do not embed API keys or credential-looking examples from docs unless they are clearly placeholders; redact anything that resembles a real secret.
- Do not keep blank/skeleton API-doc screenshots as assets. Use DOM/OpenAPI extraction instead.
- Do not overstate claims like SOC 2, uptime, regions, or “does not store photos” beyond exactly what the public page says.