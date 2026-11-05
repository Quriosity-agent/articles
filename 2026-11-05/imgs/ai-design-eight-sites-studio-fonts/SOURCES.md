# Eight AI Design Links: Follow-Up Source Record

## Original and Editorial Scope

- Post: https://x.com/I_am_Aiabir/status/2118180756698923263
- Author shown: Abida Jule / @I_am_Aiabir.
- Displayed time: `14:17 · 5 Nov 2026`. Article uses that displayed date without asserting an exact UTC conversion.
- Reviewed 2026-11-05, Australia/Melbourne.
- The web reader returned a cache miss for the post. The ordinary in-app browser exposed the full public text and all eight link titles. Embedded media reported unavailable playback, so no claim is made to have watched it.
- Four entries repeat the earlier five-site guide. This is a follow-up focused on Studio versus prompts, cost scope, font-match labels, and the Godly redirect, not a duplicate rewrite of the earlier gallery descriptions.

## Primary Evidence

| Page | Evidence used |
|---|---|
| https://studio.motionsites.ai/ | Public description, chat input, design browsing, brand-restyling entry, custom images/video/code claims |
| https://studio.motionsites.ai/pricing | Live rendered plan scope and FAQs; see observation below |
| https://motionsites.ai/ | Prepared prompt positioning, Apps/Sections filters, page/section examples, public EMBER.dsgn preview |
| https://lovable.dev/pricing | Official description of credits, variable consumption, and build/Cloud/app-AI scope; no exact Lovable subscription-price claim is made |
| https://www.fontinlogo.com/ | Visible relationship labels: verified, based on, modified, closest, community suggestion/designed; text previews and catalog positioning |
| https://godly.website/ | HTTP redirect and direct browser navigation to Recent |
| https://recent.design/info | Official statement that Recent replaces Godly and has a broader feed |
| https://land-book.com/ | Gallery and filter scope, refreshed during this review |
| https://landdding.com/ | Landing-page/template curation, refreshed during this review |
| https://60fps.design/ | Interaction-reference positioning, refreshed during this review |

Individual Font In Logo detail pages were also opened, but one web-reader response included multiple mutually exclusive template labels. The article therefore relies on the current homepage's classifications rather than treating every scraped detail-page label as a true font attribution. No font identity was independently verified against a brand's primary design files.

## Studio Observations

The web reader could not load Studio, while its normal browser UI and ordinary public requests loaded successfully. In the browser, navigated from the homepage to Pricing and expanded only the hosting and ownership FAQ entries. No plan was changed and the payment control was not activated.

Observed launch pricing:

| Plan | Monthly display | AI budget | Design count shown |
|---|---|---|---|
| Starter | $25, with $49 struck through | $25 | 5 per month |
| Basic | $99, with $149 struck through | $99 | Unlimited |
| Pro | $199, with $299 struck through | $199 | Unlimited |
| Studio | $499, with $699 struck through | $499 | Unlimited |

The displayed currency symbol is retained as `$`; the article does not convert it to Australian dollars or independently establish settlement currency. The page states budgets refresh at renewal and are consumed by AI work, with upgrading or waiting when exhausted. “Unlimited” design count is not treated as unlimited AI usage.

Expanded FAQ observations:

- Hosting and domain setup are not provided; code is downloaded for hosting elsewhere.
- Provider says the user owns the website, can download full code at no extra charge, and retains supplied content.

These are public service statements, not legal assurance or proof of a tested export. No login, purchase, upload, generation job, code download, domain setup, or matched Lovable comparison occurred. The temporary browser tab was closed.

## Redirect Verification

Direct browser navigation from `https://godly.website/` ended at `https://recent.design/?ref=godly`, displaying Recent's gallery. A separate public HTTP header check showed:

```text
https://godly.website/ -> 301 -> http://recent.design/?ref=godly
http://recent.design/?ref=godly -> 301 -> https://recent.design/?ref=godly
https://recent.design/?ref=godly -> 200
```

This verifies the observed destination, not ownership history or a continuing separate awards program.

## Media Provenance

Three public source images were inspected and preserved for attributed editorial illustration. They are not screenshots from a generated project or assets released under an asserted open-source license. Brand names, artwork, and designs retain their respective rights.

| Local file | Public source | Treatment |
|---|---|---|
| `motionsites-studio-preview.jpg` | https://studio.motionsites.ai/og-image.jpg | Original homepage Open Graph image; MotionSites Studio. Branding only, not generation proof. |
| `font-in-logo-preview.jpg` | https://www.fontinlogo.com/images/1.jpg | Original homepage Open Graph image; Font In Logo / Azwedo. No font binary included. |
| `motionsites-gallery-example.jpg` | https://image.mux.com/iK2ACd5wEwi7ORN8i16kl59Cck01IREnB3hX6EnnqiUk/animated.webp?width=640&fps=15 | EMBER.dsgn preview URL exposed in MotionSites' homepage image markup; converted to a static JPEG with macOS `sips`. Not re-created from a prompt. |

The animated WebP was temporary research material, not committed. Local FFmpeg could not decode that animation; `sips` successfully produced the inspected static representation. No timing or movement conclusion is drawn from that JPEG.

```sh
sips -s format jpeg motionsites-ember-preview.webp --out motionsites-gallery-example.jpg
```

Earlier sources are linked as historical records, not substituted for current verification of Studio or the redirect. No paid prompt/template, restricted font, or source-code export is redistributed.
