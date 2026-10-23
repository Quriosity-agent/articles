# Sources and Media Provenance

Article source date: 2026-10-22. Research and download date: 2026-10-23.

## Source Post

- Original: https://x.com/wquguru/status/2113181135522214168
- Public transcription used because direct X access returned 403: https://api.fxtwitter.com/wquguru/status/2113181135522214168
- Transcription timestamp: `2026-10-22T08:10:18Z`.
- The post contains eight repository links and no attached photo/video in the retrieved transcription. Its GitHub preview card was not used as a product screenshot.
- The post's months-to-days and team-to-individual claims were not independently measured.

## Inspected Repository Snapshots

GitHub repository metadata, default-branch commit metadata, and READMEs were read. These are research-date snapshots, not necessarily the versions available when the post was written.

| Repository | Inspected commit | Commit time (UTC) |
|---|---|---|
| [Autumn-27/ScopeSentry](https://github.com/Autumn-27/ScopeSentry/tree/d770b7a137ec2de15816fea4bd561f49cf486db2) | `d770b7a137ec2de15816fea4bd561f49cf486db2` | 2026-10-11 03:21:00 |
| [morluto/rea](https://github.com/morluto/rea/tree/6c4d880f2dd9ca7d42593be916f90ec19b8a09d7) | `6c4d880f2dd9ca7d42593be916f90ec19b8a09d7` | 2026-10-23 08:10:04 |
| [usestrix/strix](https://github.com/usestrix/strix/tree/594398876f9cd465f00cce626d0cb98bfa5e1662) | `594398876f9cd465f00cce626d0cb98bfa5e1662` | 2026-10-23 03:28:10 |
| [vxcontrol/pentagi](https://github.com/vxcontrol/pentagi/tree/cffed9485aa1cca70762cd08a57ac62a80406258) | `cffed9485aa1cca70762cd08a57ac62a80406258` | 2026-10-22 23:20:46 |
| [AIPentest/CyberStrikeAI](https://github.com/AIPentest/CyberStrikeAI/tree/c0d5c8460ba1f29d00f0cfd47855d724e257c46f) | `c0d5c8460ba1f29d00f0cfd47855d724e257c46f` | 2026-10-23 03:45:15 |
| [Hinln/ARTEX](https://github.com/Hinln/ARTEX/tree/f3e3f54b6c93916388a0a3dc6a439893a9abe37a) | `f3e3f54b6c93916388a0a3dc6a439893a9abe37a` | 2026-10-08 11:05:50 |
| [NVIDIA/garak](https://github.com/NVIDIA/garak/tree/b656779427ad40929211e7736cbbaea64700b3be) | `b656779427ad40929211e7736cbbaea64700b3be` | 2026-10-21 21:37:41 |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo/tree/b678d240d8f1426bee776ff24c34252baa564e17) | `b678d240d8f1426bee776ff24c34252baa564e17` | 2026-10-23 01:53:13 |

Additional inspected sources:

- [ARTEX ScopeSentry synchronization implementation](https://github.com/Hinln/ARTEX/blob/f3e3f54b6c93916388a0a3dc6a439893a9abe37a/server/sync_scopesentry.go): HTTP MCP client, project/task selection, paging, type mapping, asset ingestion. This confirms implementation, not a live integration test.
- [CyberStrikeAI security model](https://github.com/AIPentest/CyberStrikeAI/blob/c0d5c8460ba1f29d00f0cfd47855d724e257c46f/docs/en-US/security-model.md).
- [CyberStrikeAI hardening](https://github.com/AIPentest/CyberStrikeAI/blob/c0d5c8460ba1f29d00f0cfd47855d724e257c46f/docs/en-US/security-hardening.md).
- [PentAGI Docker access warning](https://github.com/vxcontrol/pentagi/blob/cffed9485aa1cca70762cd08a57ac62a80406258/README.md#giving-agents-docker-without-giving-away-the-host).
- [Promptfoo CI/CD documentation](https://www.promptfoo.dev/docs/integrations/ci-cd/), live page read 2026-10-23.

No tools were installed, no targets scanned, no exploit tested, no model API called, and no comparative benchmark run. No private project material was used.

## Images

These unmodified upstream screenshots are retained as attributed editorial reference. Interface examples are not independent measurements, vulnerability validation, current rankings, or proof of deployment security. Copyright, branding, and any third-party content remain with their respective owners; repository licenses are not a claim that every depicted asset is freely reusable.

| Local file | Original source | Context |
|---|---|---|
| `scopesentry-dashboard.png` | [Pinned PNG](https://raw.githubusercontent.com/Autumn-27/ScopeSentry/d770b7a137ec2de15816fea4bd561f49cf486db2/docs/images/index-en.png) | ScopeSentry README example; 1493 x 867. README states AGPL-3.0 with additional commercial-use conditions; see its terms before software deployment. |
| `artex-exploration-graph.png` | [Pinned PNG](https://raw.githubusercontent.com/Hinln/ARTEX/f3e3f54b6c93916388a0a3dc6a439893a9abe37a/screenshots/graph.png) | ARTEX example graph; 2880 x 1800. Backup retains original project attribution and AGPL-3.0 license. |
| `promptfoo-evaluation-matrix.png` | [Pinned PNG](https://raw.githubusercontent.com/promptfoo/promptfoo/b678d240d8f1426bee776ff24c34252baa564e17/site/static/img/claude-vs-gpt-example@2x.png) | Promptfoo README example; 4476 x 3240. Repository is MIT licensed; shown values are demonstration results. |

All three files were checked with `file` and visually inspected after download. No executable tool payloads or raw scan data are included.
