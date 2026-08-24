---
title: "Grok Bot 0.18 Reconstructed: The Signal Is Not 'Leaked Source,' but an Auditable Agent Runtime From a Binary App"
date: 2026-08-23
source: "https://github.com/b-nnett/grok-bot-0.18-reconstructed"
tags:
  - Grok Bot
  - Cursor
  - Anysphere
  - Electron
  - Agent Runtime
  - MCP
  - Codex
  - Claude Code
  - Reverse Engineering
---

# Grok Bot 0.18 Reconstructed: The Signal Is Not 'Leaked Source,' but an Auditable Agent Runtime From a Binary App

> **TL;DR:** `b-nnett/grok-bot-0.18-reconstructed` is not Anysphere's original monorepo and not an official Grok Bot release. It is an unofficial, source-oriented reconstruction of the publicly shipped Grok Bot 0.18.0 macOS app. The project keeps the checksum-pinned shipped renderer, rebuilds runtime boundaries such as Electron main, host, coordinator, local execution, and protocol in readable TypeScript, then packages the result as a separate bundle ID with an ad-hoc signature. The interesting part is not UI cloning. It is a rare look at how a desktop AI agent can be decomposed into routing, tools, MCP, credentials, sandboxing, provenance, and reproducible packaging.

- **Source:** [b-nnett/grok-bot-0.18-reconstructed](https://github.com/b-nnett/grok-bot-0.18-reconstructed)
- **Published:** repository created on 2026-08-23 UTC, latest listed commit on 2026-08-23 UTC
- **Checked:** 2026-08-25
- **Status when checked:** public TypeScript repo, 2 commits, about 1.2k stars and 1.3k forks
- **Tags:** Grok Bot / Cursor / Anysphere / Electron / Agent Runtime / MCP / Codex / Claude Code / OpenRouter / Reverse Engineering

![Grok Bot reconstructed Router settings](imgs/grok-bot-018-reconstructed/01-router-settings.png)

## 1. Start With The Boundary: This Is Not Official Source

The easiest mistake is to read this repository as a Grok Bot source-code leak. The README and NOTICE say something narrower: this is a hacking and research project, not Anysphere's original monorepo, not an official Grok Bot release, and not a grant of any upstream source license.

The base input is the publicly distributed Grok Bot 0.18.0 app. PROVENANCE records the macOS arm64 DMG URL, SHA-256, and original `app.asar` SHA-256. The repository also preserves the Windows x64 installer through Git LFS. Reconstructed builds use a different bundle ID and an ad-hoc signature, and the upstream app installed on the machine is not overwritten.

So the useful question is not "is this official?" It is:

1. Does the project state provenance clearly?
2. Does it separate artifact-backed behavior from inference?
3. Does it keep hash pins and reproducible checks?
4. Does it spell out redistribution, copyright, trademark, and service-term risk?

This repository is unusually careful on those points. It does not present itself as a sanctioned replacement. It presents itself as a research-grade reconstruction of a desktop AI agent runtime.

## 2. The Real Object Is The Agent Runtime, Not The UI

The README's architecture sketch is the key object:

```text
polished shipped renderer
          │
          │ desktop preload / RPC
          ▼
     Electron main
          │
          ├── settings, secrets, auth and plugin lifecycle
          ├── remote box connector
          └── owned local Docker connector
                       │
                       ▼
              coordinator + host
                       │
              inference router
           ┌───────────┼───────────┐
        Cursor      Claude       Codex / OpenRouter
                       │
                 Grok Bot MCP tools
```

That diagram is a reminder that a desktop AI agent is no longer "a chat window plus a model API." It contains at least six layers:

1. **Renderer:** chat UI, settings, message stream, plugin entry points.
2. **Preload / RPC bridge:** a narrow bridge between UI and privileged runtime.
3. **Electron main:** settings, secrets, authentication, updates, telemetry, plugin lifecycle.
4. **Host / coordinator:** turn execution, streaming, tool calls, MCP bridge, conversation state.
5. **Box / local execution:** remote or local execution environment.
6. **Provider router:** a way to connect the same product shell to Cursor, Claude Code, Codex, or OpenRouter.

That is why the repository matters. It exposes a layer of AI product competition that is not just model quality. Whoever controls the agent runtime controls tool protocols, context management, sandbox boundaries, credential reuse, cost accounting, and failure recovery.

## 3. Why It Keeps The Shipped Renderer

One of the better engineering choices in the project is that it does not pretend to recover a full frontend source tree.

The README says the distributed app did not include the authored frontend source or source maps. It contained optimized production JavaScript and CSS chunks. Those chunks were enough to inspect behavior and recover contracts, but not enough to recreate the original React components, names, comments, file structure, or design-system source.

So the project uses a hybrid design:

1. Application runtimes under `source/` are reconstructed in readable TypeScript.
2. The polished shipped renderer remains the UI baseline.
3. A narrow deterministic transform adds the reconstructed Router settings UI.
4. Original and patched renderer chunk hashes are recorded and verified.
5. The packaged app uses a separate bundle identity and disables the upstream updater.

That is more valuable than rebuilding a similar-looking frontend from scratch. It respects the evidence boundary. If the original frontend source is not present, do not invent it. Recover the runtime contracts, bundle hashes, DOM signatures, IPC/RPC behavior, and repeatable runtime observations.

PROVENANCE makes this explicit through an evidence-only reconstruction rule. UI-facing recovery must have an artifact anchor: emitted code, source-path markers, extracted capsules or source maps, shipped strings/assets/CSS, renderer DOM signatures, IPC/RPC contracts, or repeatable observations of the shipped runtime. Passing typecheck or build is not proof of provenance.

That is a useful discipline for AI-era reverse engineering: **do not let plausible completions fill an evidence gap.**

## 4. Router Is The Product Experiment

The reconstruction is the research layer. Router is the product experiment.

The current settings surface lets the user choose the backend for new turns:

| Provider | Authentication | Tool support |
|---|---|---|
| Cursor | Existing Grok Bot / Cursor session | Native Grok Bot tools and plugins |
| Claude Code | Existing local Claude Code login | Routed Grok Bot MCP tools |
| Codex | Existing local ChatGPT / Codex login | Direct Responses transport with Grok Bot tools |
| OpenRouter | API key saved through the desktop secrets bridge | Grok Bot tool-execution loop |

The important detail is that Claude Code and Codex do not require separate API keys when their local clients are already authenticated. The desktop app reuses local agent-client authentication instead of asking the user to paste credentials into yet another tool.

The project also preserves streaming responses, thinking state, reactions, rich plugin mentions, and MCP tool execution across routed conversations. So this is not merely changing a `model=` parameter. It tries to keep the product experience stable while swapping the inference and tool-execution transport underneath.

For developers, that is the more interesting pattern: stable UI and tool contracts, pluggable providers, local authentication reuse, and local usage accounting.

## 5. Local Docker Exposes The Next Agent Boundary

The other important experiment is the local Docker sandbox.

The upstream Grok Bot flow uses a remote box. This reconstruction adds a **Use local Docker VM** toggle. When enabled, the box host and execution daemon run inside an owned local container instead of connecting to the remote sandbox.

The README lists several boundaries:

1. The container binds only to loopback ports.
2. Host and daemon artifacts are mounted read-only in content-addressed form.
3. Existing provider authentication is reused where needed.
4. The container is validated before the coordinator connects.
5. Settings lifecycle stops or replaces the container.

This matters because AI coding-agent safety is not only about refusal behavior or IDE permission prompts. The real boundary sits in execution:

1. Which files can the agent read?
2. Which network paths can it access?
3. Where do its tool binaries come from?
4. How does the app prove the runtime has not changed?
5. How are credentials reused, isolated, and revoked?

A local sandbox is not automatically safer than a remote sandbox, but it shifts control back to the local machine. That lets engineering teams inspect runtime, network, mounts, and lifecycle. This will become a meaningful product layer for agent systems.

## 6. The Build Chain Is About Reproducibility

The quick start looks like an ordinary Node/Electron workflow:

```sh
git lfs install
git lfs pull
npm ci
npm run bootstrap
npm run check
npm run package
open "dist/Grok Bot 0.18 Reconstructed.app"
```

The important parts are `bootstrap` and `package`.

`npm run bootstrap` first uses the Git LFS preservation copy of the pinned 0.18.0 DMG. If it is absent, the script falls back to the original public URL. `GROK_BOT_018_APP` can also point to an existing local app copy. Bootstrap verifies the DMG and `app.asar`, caches the matching Electron runtime, and hydrates the ignored `src/app/dist` build input.

`npm run package` runs checks, compiles reconstructed runtimes, applies the narrow renderer/settings transform, creates the app bundle, assigns a reconstructed bundle identity, ad-hoc signs it, and verifies the result.

For a reconstruction project, the point is not "it ran once on my machine." The point is that readers can see:

1. Which inputs are pinned.
2. Which outputs are generated.
3. Which directories must stay out of Git.
4. Which hashes are verified.
5. Which upstream behaviors are disabled by default, including the official updater, Sentry, and upstream telemetry.

Reproducibility is part of the trust model.

## 7. Legal And Security Caveats Are Not Fine Print

NOTICE and SECURITY are unusually direct.

NOTICE says the repository is not affiliated with or endorsed by Anysphere, Cursor, xAI, or SpaceX. It does not assert or grant an upstream source-code license. The absence of the original binary payload and recovery evidence from Git does not, by itself, make the reconstructed implementation safe to redistribute. Anyone publishing or distributing it needs an independent review of copyright, trademark, third-party dependencies, and service terms.

SECURITY says this is a small-club reconstruction, not a supported production distribution. Users should not reuse real credentials or sensitive accounts while experimenting. Reconstructed packages default the official updater, Sentry, and upstream telemetry off at the Electron-main packaging boundary. Bootstrap downloads and hydrated `app.asar` inputs are checksum-pinned. `npm audit` still reports compatibility advisories in pinned Electron 42.1, Undici 5 / Connect 1, AI SDK 4, and OpenTelemetry stacks; major upgrades are intentionally tracked as follow-up work rather than silently changing runtime behavior during cleanup.

Those caveats define the correct use case. This repository is better suited for:

1. Studying desktop AI agent architecture.
2. Learning Electron runtime boundaries.
3. Comparing remote boxes with local sandboxes.
4. Understanding provider routing and MCP tool bridges.
5. Running small technical experiments.

It should not be marketed as a production-safe Grok Bot replacement.

## 8. What Agent Product Teams Should Notice

The repo is useful because it turns "AI desktop app" into several concrete product surfaces:

1. **UI and runtime can separate.** The renderer can remain a shipped baseline while runtimes are reconstructed in readable TypeScript.
2. **Model backends can be routed.** Cursor, Claude Code, Codex, and OpenRouter can sit behind one tool-execution loop.
3. **MCP is a tool contract layer.** The reusable asset is the tools/plugins protocol, not a single provider API call.
4. **Authentication is becoming local.** Reusing local logged-in CLI or agent clients is closer to real desktop UX than scattering API keys.
5. **Sandboxing is a product capability.** Remote box versus local Docker is a tradeoff across security, privacy, cost, latency, and auditability.
6. **Release governance matters.** Hash pins, clean-history export, LFS preservation, generated-artifact exclusion, and telemetry boundaries are part of the product's credibility.

Seen next to Cursor, Codex, Claude Code, and Grok Bot, the direction is clear. AI coding products will not compete only on which model writes better code. They will compete on who can organize models, tools, sandboxes, context, permissions, and cost into a stable runtime.

## 9. My Read: An Agent Runtime Dissection

I would not treat `grok-bot-0.18-reconstructed` as an ordinary open-source app, and I would not treat it as an official product announcement. It is closer to a dissection of an agent runtime.

It shows four important asset classes in desktop AI agents:

1. **Product shell:** chat experience, settings, plugin entry points, state feedback.
2. **Runtime protocol:** RPC, MCP, coordinator, tool execution, streaming state.
3. **Execution boundary:** remote box, local Docker, filesystem, network, credential scope.
4. **Supply-chain discipline:** hashes, signing, LFS, clean export, telemetry boundary, audit trail.

Models will keep improving, but agent products will not win on model calls alone. The durable advantage will come from making these runtime boundaries legible, verifiable, replaceable, and governable.

That is why this repository is worth studying. It is not a "Grok Bot source leak" story. It is a concrete signal that AI desktop apps are moving from chat interfaces toward programmable agent operating layers.

## Sources

1. b-nnett/grok-bot-0.18-reconstructed
   https://github.com/b-nnett/grok-bot-0.18-reconstructed

2. README.md
   https://github.com/b-nnett/grok-bot-0.18-reconstructed/blob/main/README.md

3. PROVENANCE.md
   https://github.com/b-nnett/grok-bot-0.18-reconstructed/blob/main/PROVENANCE.md

4. NOTICE.md
   https://github.com/b-nnett/grok-bot-0.18-reconstructed/blob/main/NOTICE.md

5. SECURITY.md
   https://github.com/b-nnett/grok-bot-0.18-reconstructed/blob/main/SECURITY.md

6. docs/ARCHITECTURE.md
   https://github.com/b-nnett/grok-bot-0.18-reconstructed/blob/main/docs/ARCHITECTURE.md

7. docs/PUBLISHING.md
   https://github.com/b-nnett/grok-bot-0.18-reconstructed/blob/main/docs/PUBLISHING.md
