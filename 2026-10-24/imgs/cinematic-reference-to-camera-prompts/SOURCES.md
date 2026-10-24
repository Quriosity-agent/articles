# Sources and Verification

Article/review date: 2026-10-24, Australia/Melbourne.

## Origin

- Canonical post: https://x.com/Crypto_QianXun/status/2113805484239286697
- User supplied the same post with sharing query parameters; these are omitted from article attribution.
- Author display name: 千寻; account: `Crypto_QianXun`.
- Public metadata endpoint: https://api.fxtwitter.com/status/2113805484239286697
- Returned creation time: `Sat Oct 24 01:31:14 +0000 2026` (October 24 in Melbourne as well).
- The post recommends Shot.Cafe, FilmGrab, Eyecandy, Melies Cinematic Techniques, AI Camera Movements, and GrokFilm as a sequence for learning cinematic AI-video work.
- X direct retrieval and a fresh browser navigation returned HTTP 403. Text and timestamp were read from FxTwitter, a third-party representation, not an authenticated first-party post view.
- Metadata lists an approximately 30-second attached video. It was not downloaded, played, analyzed, or represented as independent evidence here. Screenshots below were captured separately from the linked websites.

## Official Pages Read

1. https://shot.cafe/ — search/browse dimensions, account collections, About, educational/research notice.
2. https://film-grab.com/ — film browsing.
3. https://film-grab.com/2026/09/28/a-different-man/ — film gallery and credit information.
4. https://eyecannndy.com/ — official technique categories.
5. https://eyecannndy.com/technique/dolly-zoom — official technique page readable through web extraction; a direct browser visit received a verification/403 page. No browser challenge bypass was attempted. The challenge screenshot was discarded rather than used as a product image.
6. https://melies.co/cinematic-techniques — technique directory.
7. https://melies.co/cinematic-techniques/camera-movement/dolly-in — definition, narrative purpose, physical travel/parallax, comparisons, prompts, and mistakes.
8. https://aicameramovements.com/ — movement cards, categories, Movement/Speed/Framing/End instructions, external generation links.
9. https://grokfilm.app/ and https://grokfilm.app/#index — loaded technique index and Studio status.

The public HTML/JavaScript served by GrokFilm was also inspected. `buildPrompt()` constructs ordinary entries as a cinematic film still plus the entry definition and shared style descriptors. The Grok action copies the prompt and opens `grok.com/imagine?prompt=...`. `buildBtn` opens a Coming Soon overlay, not a timeline editor. These observations describe the inspected public front end, not unavailable backend capabilities or affiliation with xAI.

Static extraction initially showed zero-valued GrokFilm placeholders. In the loaded browser the index populated; the article therefore does not misreport the library as empty. Catalog sizes are not used as quality benchmarks.

## Local Screenshots

Captured in a fresh, unauthenticated Playwright browser at a 1440 x 1000 CSS-pixel viewport. No personal account, private production project, generation request, or payment was used. All retained images were visually inspected. These are screenshots of public interfaces and their examples, not newly generated videos.

| File | Source/state |
|---|---|
| `shot-cafe-reference-search.webp` | `https://shot.cafe/`, homepage search, tags, attributes, and collections |
| `filmgrab-film-study.webp` | *A Different Man* gallery page linked above |
| `melies-dolly-in.webp` | Dolly In definition and mechanics page linked above |
| `camera-movement-library.webp` | `https://aicameramovements.com/`, overview and entry to library; retained as additional context |
| `camera-movement-cards.webp` | Same page, scrolled to movement cards |
| `grokfilm-index.webp` | `https://grokfilm.app/#index` after entering the loaded index |
| `grokfilm-studio-coming-soon.webp` | Same page after clicking “Build your GrokFilm” |

The browser session was closed after capture. Repository checks verify local image/link existence and bilingual index entries. No full-site interaction, copy-button integration, embedded-video playback, provider login, video generation, editing, export, model cost, or model quality comparison was tested.

## Editorial Scope and Rights

- The shot exercise, example prompt, checklist, and workflow interpretation are editorial additions, not quotations or successful generation results.
- The prompt was not tested. Duration and camera behavior are desired requirements, not claims of model reliability.
- The six resources were reviewed as complementary references, not a proven integrated production pipeline.
- Existing related article: `2026-07-08/2026-07-08-cinematic-reference-stack-ai-video-preproduction.md` and its English pair. This follow-up adds the terminology-to-instruction and acceptance-criteria angle.
- Screenshots retain visible site identity and source attribution. Site UI, film images, examples, logos, and other depicted material retain their respective ownership. This repository does not grant new rights to those materials or replace site/service terms.
- Film stills were not extracted into a training or production-reference dataset. No claim of unrestricted reuse or commercial clearance is made.
