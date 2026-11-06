# Sources and Verification

- Repository: https://github.com/guohuiyuan/go-music-dl
- Release: https://github.com/guohuiyuan/go-music-dl/releases/tag/v1.1.4
- Public release metadata: https://api.github.com/repos/guohuiyuan/go-music-dl/releases/latest
- Release publication: `2026-11-05T02:39:18Z`, also November 5 in Melbourne. Review date: November 6, 2026 (Australia/Melbourne).
- Source reviewed: `d5e7749772e932a15c8fc9ab75ebdfacd446b557`, matching the release's displayed revision and the cloned `main` at review time.
- Pinned dependency: `github.com/guohuiyuan/music-lib v1.1.1-0.20261018010056-7cc4467b4e30`, from `go.mod`. Read the Apple adapter in the resolved module, including the preview-only built-in download path. No DRM workflow exercised or recommended.

## Image Provenance

| Local file | Original file at reviewed revision | Use |
|---|---|---|
| `web-search.png` | [screenshots/web1.png](https://github.com/guohuiyuan/go-music-dl/blob/d5e7749772e932a15c8fc9ab75ebdfacd446b557/screenshots/web1.png) | Upstream README image, 2516 x 1331; shows search modes, providers, and results |
| `tui-results.png` | [screenshots/tui1.png](https://github.com/guohuiyuan/go-music-dl/blob/d5e7749772e932a15c8fc9ab75ebdfacd446b557/screenshots/tui1.png) | Upstream README image, 1259 x 617; shows selection and multi-source terminal results |

Both PNGs were visually inspected and copied unchanged. They illustrate upstream UI, not a locally captured run or a guarantee of current provider behavior. The upstream repository identifies AGPL-3.0 for its software. No separate rights are claimed for any album art or third-party branding visible in the screenshots.

## Focused Test Runs

Environment: macOS arm64, `go1.26.3`, unmodified shallow checkout of the reviewed revision. Commands run from the source checkout:

```bash
go test -mod=readonly ./internal/web \
  -run '^(TestAI|TestParseAIPlayerSources|TestExecuteAISongSearch)' -count=1 -v
go test -mod=readonly ./internal/web ./core \
  -run '^(TestDownloadContainer|TestFindBestSwitchSong|TestValidateSwitchCandidates|TestStandardLRCForExport|TestSaveDownloadedSongLyricSidecar|TestDetectAudioExtBySignature|TestParseContentRangeTotal|TestFetchBytesWithMimeUsesRangeDownload|TestBuildDownloadFilenameUsesTemplate)' \
  -count=1 -v
```

- First run: 22 passing top-level tests, `internal/web`.
- Second run: five passing top-level tests in `internal/web`, nine in `core`. Subtests are not counted separately.
- The player tests use in-process HTTP handlers, fake provider results, and hub subscriptions. The Range test uses a loopback server. Source-switch and queue tests use test fixtures; file-handling checks use temporary paths.
- These runs did not validate live SSE delivery to a browser, audible playback, current provider availability, full-track or lossless access, package signing/installation, or WebDAV against a live account. No platform credentials were configured or music fetched from upstream providers.
