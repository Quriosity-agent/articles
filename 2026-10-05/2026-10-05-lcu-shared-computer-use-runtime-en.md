---
title: "Inside LCU: Sharing a Local Computer Use Runtime Across Claude Code, Pi, and Codex CLI"
date: 2026-10-05
source: "https://x.com/dotey/status/2107144243726729645"
tags:
  - LCU
  - Computer Use
  - Claude Code
  - Codex CLI
  - Pi
  - MCP
  - JavaScript REPL
  - Accessibility
  - Agent Harness
  - Source Audit
---

# Inside LCU: Sharing a Local Computer Use Runtime Across Claude Code, Pi, and Codex CLI

You may prefer one model's reasoning and coding while wanting another system's desktop tools. LCU addresses that combination: it connects the Computer Use runtime in a locally installed OpenAI desktop application to an external agent, providing a shared interface for observing windows, clicking, typing, and reading results.

Baoyu introduced `amontlabs/lcu` on October 5, 2026. His post identifies the central design accurately: reuse the installed runtime and expose it through MCP and a persistent JavaScript REPL. By this article's October 23 review, the latest release was `v0.12.0`, with changes to prerequisites and integrations.

![LCU project showreel cover](imgs/lcu-shared-computer-use-runtime/lcu-poster.jpg)

*Project-published showreel cover. All images here are upstream media; LCU was not run against the reviewer's desktop.*

- Source: [Baoyu's LCU post](https://x.com/dotey/status/2107144243726729645), published October 5, 2026, at 16:21 UTC
- Project: [amontlabs/lcu](https://github.com/amontlabs/lcu), [website](https://lcu.amontlabs.com/)
- Reviewed release: [v0.12.0](https://github.com/amontlabs/lcu/releases/tag/v0.12.0), published October 21, 2026
- Commit: `99d0759a7610e38251037759a69fcdbef816a8c2`
- Scope: source, installation and adapter documentation, upstream verification records, and official OpenAI Computer Use documentation. No runtime installation or independent desktop reproduction was performed.

## Separating the model, harness, and desktop runtime

The architecture has four roles:

```text
Model: understand the goal and choose the next step
    ↓
Claude Code / Pi / Codex CLI: sessions, tools, and user decisions
    ↓
LCU: runtime discovery, MCP, approvals, and lifecycle adaptation
    ↓
Local OpenAI Computer Use runtime: observe and operate desktop apps
```

LCU locates an installed official ChatGPT desktop app, checks the supported platform and application structure, and uses its Node, REPL, and Computer Use components. In the source, `lcu/runtime.mjs` manages launch paths and environment, while `adapters/client.mjs` and `adapters/claude.mjs` manage host connections and result delivery.

This lets the model and execution tools be chosen somewhat independently. Claude Code can retain its own model and session management while delegating desktop actions to the bridged runtime.

**The lack of a ChatGPT or Codex sign-in requirement concerns this local execution channel.** The harness still needs its own authentication or model service. LCU supplies no model quota. It is a third-party MIT project; the OpenAI application, runtime, and instructions retain their own terms and are not made open source by LCU. [Installation documentation](https://github.com/amontlabs/lcu/blob/v0.12.0/docs/INSTALLATION.md)

## Two model tools expose a programmable interface

The principal adapters expose two tools to the model:

| Tool | Role |
|---|---|
| `js` | Execute code in a persistent JavaScript environment containing the `cua` object |
| `js_reset` | Reset that JavaScript environment |

Screenshots, clicks, typing, and scrolling are methods on `cua` and its target objects. The model first obtains current state and documentation, then selects an app or browser target.

A first call can contain only:

```javascript
await cua.getState();
```

After reading the returned guidance, a separate call selects an app:

```javascript
let app = await cua.getApp("TextEdit");
```

Later calls can reuse `app` and follow the runtime documentation to read accessibility information, capture screenshots, or interact. New windows, focus changes, and page loads require fresh observations before further decisions.

This design lets a call combine a few predictable operations and retain variables for later use. It reduces round trips and repeated target discovery. It does not make a long sequence immune to changing UI state; observations or screenshots must verify the outcome.

OpenAI's official Computer Use documentation also describes code execution, persistent environments, and returning observations. That general API integration path and LCU's reuse of desktop-app components are different product integration routes. The documentation does not make LCU an officially released OpenAI SDK. [Official guide](https://developers.openai.com/api/docs/guides/tools-computer-use)

## Why accessibility information helps

With screenshots alone, a model must infer controls from pixels. Accessibility information can also provide exposed text, control types, and interaction targets, making it easier to select a specific element.

In suitable applications, this reduces coordinate errors caused by window movement, scaling, or resolution changes. The application must expose useful accessibility data. Custom canvases, games, and complex editors may still require visual and coordinate-based interaction.

![Calendar and TextEdit in the project demonstration](imgs/lcu-shared-computer-use-runtime/project-demo-frame.jpg)

*Frame at 16 seconds from the project's 30-second showreel, illustrating reading Calendar and typing a note in TextEdit. This is upstream demonstration media, not a task completed during this review.*

## Approvals and task completion need host integration

An MCP connection leaves several questions unresolved. Who displays approval requests? Who receives the person's decision? Who tells the runtime to release control when a turn ends or is interrupted? Can a child agent finishing accidentally stop its parent?

Much of LCU's engineering addresses these questions. Its current Claude Code adapter includes the `lcu-approve` mod, which presents app approvals through a question card in the Claude app or an approval pane in the terminal. A person can allow the current conversation, allow persistently when the runtime offers that choice, or deny.

![Application approval in Claude](imgs/lcu-shared-computer-use-runtime/claude-app-approval.png)

*Upstream v0.9.1 screenshot: a person chooses whether to grant access to Zed.*

The source also maintains model-hidden lifecycle calls such as `turn_ended`. Two public model tools therefore coexist with additional host control channels.

An optional Claude Code cross-turn setting handles background work or operations continuing after a turn ends. It is off by default, and app permissions and harness tool approvals still apply. Platform adaptation may add wrappers or change instruction delivery, so reusing the original runtime does not mean the surrounding integration contains no adaptation. [Adapter documentation](https://github.com/amontlabs/lcu/blob/v0.12.0/docs/ADAPTERS.md)

![LCU approved-app management](imgs/lcu-shared-computer-use-runtime/approved-apps.png)

*Upstream UI showing persistent grants, conversation grants, and revocation controls.*

## What changed after the source post

| Topic | October 5 post | Findings as of October 23 |
|---|---|---|
| Prerequisites | Python 3.12+ | User installation no longer needs Python; it uses the installed app's Node |
| Main harnesses | Pi, Codex CLI, Claude Code | Remain the principal documented paths |
| Experimental integrations | Oh My Pi and Hermes | DeepSeek Harness added; v0.12.0 reports live verification on macOS arm64 only |
| Browser | Chrome requires opt-in | Official extension and site approval remain; status checks now cover Chrome, Edge, Brave, Opera, and Vivaldi |
| Windows | Candidate | Still outside this release's supported delivery platforms |

An older post should therefore lead to a fresh release check. In particular, a status command recognizing a browser family does not prove that full browser tasks have passed. [v0.12.0 release](https://github.com/amontlabs/lcu/releases/tag/v0.12.0)

## Supported systems

The macOS target is Apple Silicon, with Accessibility and screen-recording permissions for the relevant components. Linux targets ARM64 or x86-64, an Ubuntu 24.04-compatible glibc environment, and an existing X11 desktop with a D-Bus session.

Intel Macs, native Wayland, and musl Linux are unsupported. LCU itself does not create a desktop or VM.

External browser control is an additional opt-in capability using the official extension and site approvals. Claude Code's Chrome path remains experimental, with limitations around temporary-tab cleanup after some interruptions. Permission to call LCU tools does not grant access to every app and website.

## What byte-identical guidance proves

The comparison mentioned by Baoyu has corresponding records. Project documentation reports byte-identical MCP initialization instructions and first-call `cua.getState()` guidance between the original service and LCU relays on a particular macOS app version. It also records a browser-section difference in the `js` description because LCU defaults to the computer surface alone. [Instruction-delivery record](https://github.com/amontlabs/lcu/blob/v0.12.0/docs/INSTRUCTIONS.md)

This supports the claim that the model receives the relevant original interface and guidance. It does not establish equal long-task success, visual reasoning, recovery, or permission behavior when a different model is attached.

The upstream evidence has several distinct levels:

| Evidence | Supported conclusion | What it does not establish |
|---|---|---|
| MCP initialization, persistent variables, and reset comparison | Interface and state forwarding work | A real GUI action occurred |
| Screenshot bytes and text-result forwarding | The harness receives expected data | The model understands it and completes a task |
| Independent file check after a TextEdit save | A specific combination completed a real edit and save | Compatibility with every app or new version |
| Stop/Interrupt records | Cleanup occurred on a particular path | Every interruption path works in every harness |

For example, an October 21 upstream record reports desktop checks with ChatGPT `26.1013.40934`, CUA `0.0.30`, and LCU `0.11.8`. Claude Code calculated a result and saved Unicode text; Codex CLI completed a Calculator task, with independent result checks. The same record explicitly excludes browser-action verification. It is not a new acceptance run for every v0.12.0 platform. [Specific verification record](https://github.com/amontlabs/lcu/blob/v0.12.0/docs/verification/macos-chatgpt-26.1013-2026-10-21.md)

This article reviewed those records and source without reproducing them locally.

## Its value depends on the task

For people already working in Claude Code, Pi, or Codex CLI who need to inspect native applications, read windows, or perform occasional desktop interactions, LCU provides a way to reuse an existing execution system.

When a task already has a stable CLI, file API, or application-specific interface, that path is usually easier to verify. LCU is particularly useful where a workflow crosses into a GUI without a suitable interface: checking what an application actually displays or completing a UI-only step.

A meaningful first acceptance check uses a harmless window: approve the target app, obtain readable state and a screenshot, perform a small action, and independently confirm the result. Installation, `doctor`, and a successful tool response should be checked separately from the actual application state. Publishing, sending, and deleting still require authorization for the task itself.

LCU demonstrates that an agent's tools can be selected separately from its model and harness. Its value lies in connecting the original execution capability while handling external-host approvals, results, and lifecycle. Actual capability depends on the model, target application, and verification across those layers.

## Sources

- [Baoyu's source post](https://x.com/dotey/status/2107144243726729645)
- [LCU v0.12.0 source](https://github.com/amontlabs/lcu/tree/v0.12.0) and [release notes](https://github.com/amontlabs/lcu/releases/tag/v0.12.0)
- [Installation](https://github.com/amontlabs/lcu/blob/v0.12.0/docs/INSTALLATION.md), [Adapters](https://github.com/amontlabs/lcu/blob/v0.12.0/docs/ADAPTERS.md), and [Instructions](https://github.com/amontlabs/lcu/blob/v0.12.0/docs/INSTRUCTIONS.md)
- [Parity Status](https://github.com/amontlabs/lcu/blob/v0.12.0/docs/PARITY-STATUS.md) and [Dependency Provenance](https://github.com/amontlabs/lcu/blob/v0.12.0/docs/PROVENANCE.md)
- [Official OpenAI Computer Use documentation](https://developers.openai.com/api/docs/guides/tools-computer-use)

*Versions, platforms, and approval behavior may change. Findings reflect the specified source version and cited records as of October 23, 2026. Upstream demonstrations and test reports are not presented as independent local verification.*
