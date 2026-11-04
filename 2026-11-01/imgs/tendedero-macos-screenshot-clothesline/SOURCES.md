# Tendedero: Sources and Verification

## Version and Date

- Requested repository: https://github.com/donghaozhang/tendedero
- Upstream and author: https://github.com/alejandrobujan/tendedero / Alejandro Buján.
- Review date: 2026-11-04, Australia/Melbourne.
- Article date: 2026-11-01, matching the reviewed upstream release `v1.8.1`, published `2026-11-01T02:17:17Z`. This is not the product launch date.
- Product launch: 2026-10-07, according to the official website and press kit.
- Pinned revision: `6df2cfe6455b39c0356c606992361b08ae6b8941`, commit subject `Tendedero 1.8.1`, timestamp `2026-11-01T02:14:10Z`.
- GitHub's comparison endpoint returned `identical`, ahead 0 / behind 0 for the fork and upstream `main` during review: https://api.github.com/repos/donghaozhang/tendedero/compare/alejandrobujan:main...main
- The GitHub web reader returned a cache miss for the requested fork. GitHub API, raw files, and a temporary sparse Git checkout supplied the primary source material.

## Primary Sources

- [Pinned README](https://github.com/donghaozhang/tendedero/blob/6df2cfe6455b39c0356c606992361b08ae6b8941/README.md): scope, gestures, installation, requirements, privacy positioning.
- [Release 1.8.1](https://github.com/alejandrobujan/tendedero/releases/tag/v1.8.1): complete-image fix and distribution claims. The API returned one `Tendedero-1.8.1.dmg` asset, 2,455,827 bytes; the app was not downloaded or installed.
- [Official website](https://tendedero.app/): browser demonstration is separate from the native app; no browser-demo interaction test was performed.
- [Official press kit](https://tendedero.app/press/): launch date and explicit editorial media permission.
- [ScreenshotWatcher.swift](https://github.com/donghaozhang/tendedero/blob/6df2cfe6455b39c0356c606992361b08ae6b8941/Sources/Tendedero/ScreenshotWatcher.swift): filesystem events, candidate filtering, completed-file checks, retry limits.
- [Inbox.swift](https://github.com/donghaozhang/tendedero/blob/6df2cfe6455b39c0356c606992361b08ae6b8941/Sources/Tendedero/Inbox.swift): screenshot preferences, destination, saved settings, restoration.
- [Line.swift](https://github.com/donghaozhang/tendedero/blob/6df2cfe6455b39c0356c606992361b08ae6b8941/Sources/Tendedero/Line.swift): capacity, pinned state, inbox Trash behavior, external-file hiding, twenty-step in-memory manual undo, persistent paths. Automatic capacity eviction uses `step: nil` and is not recorded in that undo stack.
- [ClipboardWatcher.swift](https://github.com/donghaozhang/tendedero/blob/6df2cfe6455b39c0356c606992361b08ae6b8941/Sources/Tendedero/ClipboardWatcher.swift): opt-in polling, excluded types, local PNG storage and permissions.
- [GrabArea.swift](https://github.com/donghaozhang/tendedero/blob/6df2cfe6455b39c0356c606992361b08ae6b8941/Sources/Tendedero/GrabArea.swift): drag-operation negotiation and menus.
- [LinePanel.swift](https://github.com/donghaozhang/tendedero/blob/6df2cfe6455b39c0356c606992361b08ae6b8941/Sources/Tendedero/LinePanel.swift): transparent nonactivating panel and screen placement.
- [FullScreen.swift](https://github.com/donghaozhang/tendedero/blob/6df2cfe6455b39c0356c606992361b08ae6b8941/Sources/Tendedero/FullScreen.swift): default full-screen exclusion and override. It uses private WindowServer symbols; source availability and successful compilation are not evidence of future OS compatibility.
- [AppDelegate.swift](https://github.com/donghaozhang/tendedero/blob/6df2cfe6455b39c0356c606992361b08ae6b8941/Sources/Tendedero/AppDelegate.swift): lifecycle restoration, watched folders, capacity calculation, website update link.
- [Package.swift](https://github.com/donghaozhang/tendedero/blob/6df2cfe6455b39c0356c606992361b08ae6b8941/Package.swift): macOS 14 target, no declared external package dependencies.
- [CONTRIBUTING.md](https://github.com/donghaozhang/tendedero/blob/6df2cfe6455b39c0356c606992361b08ae6b8941/CONTRIBUTING.md): product boundaries and network policy.
- [LICENSE](https://github.com/donghaozhang/tendedero/blob/6df2cfe6455b39c0356c606992361b08ae6b8941/LICENSE): MIT code with separate name/icon/artwork restrictions. Media reuse below relies on press permission, not on treating documentation images as MIT assets.

## Verification Performed

Read-only source inspection plus build/check outputs in a temporary checkout. Toolchain: Apple Swift `6.4` (`swiftlang-6.4.0.34.1`), reported target `arm64-apple-macosx26.0`.

```sh
swift scripts/check-strings.swift
swift build -c debug
```

- Localization result: `64 strings, checked in az, en, es, fr, gl, hi, ja, ko, pt-BR, tr, zh-Hans`; exit 0, no warnings printed. This is key coverage, not a linguistic-quality assessment.
- Build result: `Build complete! (8.78 sec.)`; exit 0. This was the SwiftPM debug executable build, not the universal app-bundle/signing script or a notarized release verification.
- No app launch, installation, screenshot preference changes, clipboard reads, watched-folder registration, or deletion of user media occurred.
- No runtime network capture, interaction test, full-screen/multiple-display test, performance benchmark, or validation of every macOS/architecture combination was performed.
- No test target is declared in the inspected `Package.swift`; build and string checks are not claimed as a unit-test suite.

## Editorial Media

The press page states that its images and video may be used in coverage of Tendedero. Assets were retrieved November 4, 2026 and visually inspected. Credit: Alejandro Buján / Tendedero. No native-app screenshots were captured from the user's Mac.

| Local asset | Source | Treatment |
|---|---|---|
| `tendedero-hero-light.png` | https://tendedero.app/assets/press/tendedero-hero-light.png | Original press PNG, unmodified; illustrative artwork |
| `tendedero-gestures-light.png` | https://tendedero.app/assets/press/tendedero-gestures-light.png | Original press PNG, unmodified; gesture explanation |
| `tendedero-native-demo-11.jpg` | https://tendedero.app/assets/video/tendedero.mp4 | Single frame at 11 seconds from official Mac demonstration, JPEG extraction only |

Frame extraction:

```sh
ffmpeg -hide_banner -loglevel error -ss 11 \
  -i tendedero.mp4 -frames:v 1 -q:v 2 tendedero-native-demo-11.jpg
```

The source video was used as temporary research material; only the credited frame is included in the article assets. Its staged business data is not independently verified. The figures illustrate the source's presentation, not measured usability or compatibility.
