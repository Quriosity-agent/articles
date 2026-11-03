# Sources and Media

Review date: 2026-11-03, Australia/Melbourne. This article is explanatory analysis, not an internal Pando audit or performance reproduction.

## Primary Sources

- Requested announcement: https://x.com/OpenAIDevs/status/2117408792346509663 . Web retrieval returned 403; read successfully through the in-app browser. Visible timestamp 11:09 on November 3, 2026. Status-ID conversion gives `2026-11-03T00:09:30.305Z`, consistent with Melbourne time.
- Canonical engineering article: https://openai.com/index/scaling-git-at-openai/ . Official date November 2, 2026; credited to Aaron Friel, Taylor Blau, and Ted Nyman. Read through the web tool and the rendered in-app browser. The X thread's shortened article link redirects to this URL. Folder date follows the canonical article, not the later local date of the social announcement.
- Official consistency explanation: https://x.com/OpenAIDevs/status/2117408809224470742 . Read as part of the visible official thread.
- Official pack-selection explanation: https://x.com/OpenAIDevs/status/2117408834348310581 . Visible thread text establishes selection from haves/wants, stored pack links, dependencies, and potentially redundant objects. No unexpanded trailing text is relied upon.
- Official contribution follow-up: https://x.com/OpenAIDevs/status/2117409608352559584 . Links the canonical article and mentions interrupted-download cleanup work.
- Git protocol reference: https://git-scm.com/docs/gitprotocol-v2 . Read for capability negotiation and packfile URI framing, not a Pando performance test.
- Public Git distribution: https://github.com/openai/git . GitHub API reported default branch `codex`; inspected HEAD `9fe64f46bdef176eabbc4e7f1f15c8e4f8dbc325`. Read root README, COPYING, and `Documentation/technical/packfile-uri.adoc` at this fixed SHA. No repository code was built or executed. README identifies Git's GPLv2 licensing with compatible exceptions; the API license value `NOASSERTION` is not treated as a legal conclusion. This is Git source, not evidence that Pando server source is publicly released.
- Fixed technical document: https://github.com/openai/git/blob/9fe64f46bdef176eabbc4e7f1f15c8e4f8dbc325/Documentation/technical/packfile-uri.adoc . Supports protocol-v2 scope, empty default URI protocol configuration, download/index/connectivity sequencing, delta constraints, and authentication handling. Version-specific details are labeled accordingly.

## Claim Boundaries

The approximately 80% median push-latency reduction and near-petabyte daily data volume are OpenAI-reported operational observations. Neither is an independently measured result or an end-to-end developer-productivity speedup. The canonical page's interactive comparison labels itself as a synthetic teaching model rather than a production benchmark; no simulation result was collected for this article.

The branch/manifest example, proposed evaluation metrics, and discussion of workload-dependent CPU/network tradeoffs are editorial analysis. They are not descriptions of a new public Pando API. No internal service, public signup, deployable Pando release, or exact client compatibility matrix was verified. No API calls, paid generation, installs, Git configuration changes, or infrastructure migration were performed.

## Local Figures

Both are official OpenAI diagrams, saved from image URLs observed in the canonical page DOM. Copyright remains with the original rights holder; inclusion is for attributed technical discussion, not a claim of an open media license. Original SVG files are preserved; PNG copies are rasterizations for reliable article display.

1. `git-packfile-layout.svg` / `.png`: https://images.ctfassets.net/kftzwdyauwt9/4xklltw3tJY3qRk8mzW0l3/f7f44a2cb856b00677a31506465e6d1a/storing-git-objects-in-packfiles-diagram-desktop-light.svg?w=3840&q=90
2. `pando-branch-packs.svg` / `.png`: https://images.ctfassets.net/kftzwdyauwt9/5wDkqDPp9fjzOjtAQRDRzw/117b2f107fd11818f7e9154c958b0878/representing-branches-in-pando-diagram-desktop-light.svg?w=3840&q=90

No complete article body, social-post dump, embedded application code, or large video is republished. No third-party reply or engagement count is used as technical evidence.

## Reproduce Figure Rendering

```sh
node 2026-11-02/imgs/openai-pando-agent-scale-git/prepare-figures.mjs /path/to/node_modules
```

The script uses the desktop app's bundled `sharp`, rasterizes the saved SVGs at 1800 pixels wide, and prints output dimensions. Downloaded SVG MIME/type, successful PNG decoding, and label readability are checked separately from the truth of the technical claims illustrated.

Verified output dimensions: `git-packfile-layout.png` 1800 x 1502; `pando-branch-packs.png` 1800 x 1650. Both were visually inspected: diagram labels, object identifiers, arrows, and the distinction between Git ancestry and pack dependency are legible. The saved branch SVG renders the dependency arrow in black, so article captions describe its destination rather than repeating the page alt text's color description.
