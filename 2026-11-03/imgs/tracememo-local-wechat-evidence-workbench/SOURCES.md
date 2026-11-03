# TraceMemo: Source and Verification Notes

Review date: 2026-11-03, Australia/Melbourne.

## Version and Scope

- Requested repository: https://github.com/Wxw-Gu/TraceMemo
- Inspected stable `main`: `d6d837e6f6705741000b747af99d75ab120281bd`, October 27, 2026. GitHub metadata and the public page were read, followed by fixed-revision raw documents and source.
- `package.json` reports 2.5.2; root README still contains a 2.5.1 support statement. Latest release at review: https://github.com/Wxw-Gu/TraceMemo/releases/tag/v2.5.2 , published `2026-10-27T07:45:37Z`. Its tag points to `9608077b90cd6665214dce93939dcff89d498681`, not the later inspected main commit. Release artifact availability is not treated as proof of runtime compatibility.
- Repository tree at inspected commit: 884 blobs, 89,483,505 aggregate blob bytes, as reported by the GitHub tree API. A case-insensitive standard LICENSE/LICENCE/COPYING filename search across the tree returned no files; GitHub repository license metadata was null. These observations do not establish a particular legal license.
- This is a local chat-data workbench, not an arbitrary WeChat Official Account article URL downloader.

## Documentation Read

At the pinned commit: root README and package manifest; `docs/README.md`; `docs/concepts/how-it-works.md`; `docs/concepts/answer-sources.md`; `docs/user-guide/privacy.md`; `docs/user-guide/export.md`; `docs/platform/macos.md`; `docs/agent/reader-skill.md`; `docs/agent/api-security.md`.

These distinguish ordinary local operations, remote Provider calls, Reader Skill versus Agent Hub, export media limits, generated-versus-sent outcomes, and macOS security prerequisites. Project privacy descriptions are attributed rather than represented as a complete traffic audit. No SIP instructions were executed or included as an installation recipe.

## Implementation Read

- `src/main/knowledge/knowledge-store.ts`: selected source around account-derived paths, account guards, SQLite FTS5 creation, and BM25 ranking. This supports a verified full-text search path, not an assertion that every retrieval path excludes vector search.
- `src/main/services/ai-search-evidence.ts`: identity deduplication, candidate ordering, program-owned `E` identifiers, and `sanitizeAnswerCitations`. The sanitizer recognizes `[E<number>]` markers and removes IDs outside its allow-list. It does not prove that a claim is semantically entailed by the cited message.
- `src/main/http-server.ts`: loopback defaults, CORS parsing, Bearer matching, route names including send/scheduled tasks, and dispatcher authorization. Public health is distinct from authorized data/action endpoints.
- `src/main/api-token-store.ts`: full file read; 32 random bytes, base64url, Electron safeStorage encryption, `0600` persistence, and failure states when secure storage is unavailable.

No downloaded project source or native component was executed. No dependency installation, application launch, API access, database/key extraction, account linking, chat reading, model call, scheduled task, or message sending was performed. The review is not a runtime/security audit or a test-suite pass.

## Figures

Both files are existing project screenshots at the same pinned commit:

- `first-use-welcome.png`: https://raw.githubusercontent.com/Wxw-Gu/TraceMemo/d6d837e6f6705741000b747af99d75ab120281bd/public/first-use-welcome.png ; 1448 x 982.
- `ai-search.png`: https://raw.githubusercontent.com/Wxw-Gu/TraceMemo/d6d837e6f6705741000b747af99d75ab120281bd/public/ai-search.png ; 1484 x 1116.

They retain the old WechatExplorer branding. They were visually inspected and decoded locally. They are not screenshots of this user's account, installed app state, or tests performed for the article. The example chat/financial summary is not independently verified or endorsed. Images are attributed project illustrations; no open media license or relicensing is claimed.
