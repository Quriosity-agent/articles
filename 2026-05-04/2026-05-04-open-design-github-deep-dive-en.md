# Open Design GitHub Deep Dive: Turning Claude Design’s Closed Experience into a Local-First Open Engineering System

GitHub repository: <https://github.com/donghaozhang/open-design>  
Upstream repository referenced by the README: <https://github.com/nexu-io/open-design>  
Inspected commit: `e9cc1fb` (2026-05-04)

---
**Author:** 🦞 Lobster Detective / 龙虾侦探  
**Date:** 2026-05-04  
**Tags:** Open Design, Claude Design, Coding Agents, Design Systems, Skills, Local-first, Next.js, Electron, AI Design Tools
---

If you describe **Open Design** merely as “an open-source Claude Design clone,” you miss what makes the repository interesting.

The most valuable part of products like Claude Design is not that “the model can draw a page.” It is the artifact loop: a vague brief becomes a previewable, editable, exportable design artifact. The system clarifies the brief, picks a visual direction, applies design rules, generates HTML/decks/prototypes, and renders the result inside an interactive preview surface.

Open Design tries to take that closed-source experience apart and rebuild it as a local-first, BYOK, agent-swappable, skill-driven, design-system-aware engineering system.

I cloned and inspected the repository. My conclusion: **this is not a simple UI demo. It is an attempt to productize AI design generation as a local daemon + web UI + agent adapter layer + skill registry + design-system catalog.** For builders, the key lesson is not the visual styling of any one screen. The important part is how the project defines boundaries: who owns the agent loop, who owns artifacts, who owns taste, and who owns runtime permissions.

---

## 1. What is this project really?

The README positions it clearly:

> The open-source alternative to Claude Design. Local-first, web-deployable, BYOK at every layer.

More precisely, Open Design is an **agent orchestration shell for design artifacts**:

- The frontend is a Next.js 16 + React 18 web app.
- A local Node/Express daemon owns filesystem access, agent spawning, skills, design systems, artifact persistence, and exports.
- An optional Electron shell wraps the same web experience as a desktop app.
- Open Design does not implement its own agent. It calls the coding-agent CLI already installed on the user’s machine: Claude Code, Codex, Cursor Agent, Gemini CLI, OpenCode, Qwen, Copilot, Hermes, Kimi, and others.
- Design capability is not hidden inside one giant prompt. It lives in `skills/`, `design-systems/`, and `craft/` folders.

Put together, these choices define the product’s core difference:

**Open Design does not want to be another model product. It wants to be a local control plane for AI design workflows.**

That distinction matters. If it rewrote the entire agent loop, it would drown in model calls, tool protocols, permission handling, context management, and streaming parsers. If it were just a web prompt box, it would never reach the artifact-first experience that makes Claude Design compelling. Open Design chooses the middle path: it keeps the product-layer experience, but delegates the model and agent loop to the user’s existing coding agent.

---

## 2. Repository scale: not a weekend hack

A quick scan of the current tree shows that this is already a substantial monorepo:

- Around **1,204 files**.
- Around **230,387 lines** of text content.
- **245 TypeScript files / ~70,618 lines**.
- **351 Markdown files / ~60,158 lines**.
- **135 HTML examples and templates / ~36,759 lines**.
- **51 TSX files / ~20,786 lines**.
- Root-level modules include `apps/`, `packages/`, `tools/`, `skills/`, `design-systems/`, `prompt-templates/`, `craft/`, `e2e/`, and `docs/`.
- The current tree contains **63 skill directories**, **139 design-system directories**, plus prompt-template assets for media generation.

There is some visible documentation drift: the README table mentions “31 skills / 129 design systems,” while the GitHub description mentions “19 Skills / 71 Design Systems.” That usually means the project is moving fast and the docs are catching up with the actual resource catalog.

Either way, this is far beyond “one page and one API route.” It is a fast-moving engineering system:

```text
apps/
  web        Next.js App Router frontend
  daemon     Local privileged process: REST/SSE, agents, artifacts, SQLite
  desktop    Electron shell
  packaged   Packaged Electron runtime glue
packages/
  contracts       Shared web/daemon DTOs and protocols
  sidecar-proto   Open Design sidecar business protocol
  sidecar         Generic sidecar runtime
  platform        OS/process primitives
tools/
  dev        Local development lifecycle control plane
  pack       macOS/Windows/Linux packaging control plane
skills/       Design-artifact generation capabilities
design-systems/ Brand DESIGN.md catalogs
craft/        Universal design craft rules: typography, color, anti-ai-slop
e2e/          Playwright and integration tests
```

The project is not only trying to make a demo work. It is explicitly designing for local runtime, packaging, agent extensibility, design resources, tests, and documentation.

---

## 3. The key architecture choice: Web App + Local Daemon

`docs/architecture.md` describes three deployment topologies.

The default is fully local: the browser talks to a Next.js dev server, the web app proxies to a local `od daemon`, and the daemon spawns Claude/Codex/Cursor/Gemini-style CLIs.

The second topology deploys the web layer to Vercel while keeping the daemon on the user’s machine, exposed through a tunnel. The UI can live in the cloud, but keys and local CLI access remain on the user’s computer.

The third topology is pure web + API fallback. If no local CLI is available, the app can call an Anthropic/OpenAI-compatible API directly. This is a degraded mode: it gives users a trial path, but it loses the full local filesystem and CLI-agent experience.

This split is practical:

1. **The web UI stays lightweight and deployable**  
   Next.js owns chat, artifact tree, iframe preview, comment mode, and exports. It can run locally or on Vercel.

2. **The daemon owns dangerous capabilities**  
   Filesystem access, SQLite, agent spawning, skills scanning, artifact storage, and export pipelines all live in the daemon. The browser never directly touches sensitive local resources.

3. **Agent CLIs run inside an artifact working directory**  
   Each generation happens in a real on-disk project folder. The agent can read, write, and edit files. The output can be reviewed with Git. This is much more builder-friendly than storing generated HTML as opaque database blobs.

4. **Cloud is not the default dependency**  
   Local-first means API keys, private design systems, and generated artifacts do not have to leave the user’s machine by default.

Many AI products start as cloud SaaS and later add a “local mode.” Open Design starts from the local daemon and then leaves room for web deployment.

---

## 4. Agent adapters: do not reinvent the agent loop

The most reusable design decision lives in `docs/agent-adapters.md`:

> We delegate the entire agent loop — model calls, tool use, context management, permission handling, resume, cancel — to the user's existing code agent CLI.

This is a sober engineering call.

Modern coding-agent CLIs already contain complex behavior:

- Claude Code has tool use, permission modes, stream-json, and skills.
- Codex has headless exec, reasoning-effort controls, and model configuration.
- Cursor Agent has workspace semantics.
- Gemini, OpenCode, Qwen, and Copilot each have distinct input/output formats.
- ACP JSON-RPC gives tools like Devin, Kimi, Kiro, and Mistral Vibe a more protocolized path.

If Open Design implemented another full agent runtime, it would become a model-provider and CLI-compatibility company. That is not the job of a design tool.

So it defines an `AgentAdapter` abstraction:

- `detect()` checks PATH and config directories to know whether a CLI is installed and authenticated.
- `capabilities()` tells the UI whether the agent supports streaming, surgical edits, resume, native skill loading, and permission modes.
- `run()` launches the CLI inside the artifact cwd and maps stdout/stderr into unified events.
- `cancel()` and `resume()` provide lifecycle control.

The product consequence is important: **the UI can degrade based on real agent capabilities instead of pretending every agent behaves like Claude Code.**

If an agent supports surgical edits, the UI can enable click-to-refine. If it does not, Open Design can hide that feature and fall back to whole-file regeneration. This is how a multi-agent product avoids becoming “works on my CLI, breaks on yours.”

---

## 5. Skills Protocol: design capability as files, not a prompt black box

Another core asset is `skills/`.

Open Design adopts Claude Code’s `SKILL.md` convention: a skill is a folder containing at least `SKILL.md`, optionally with `assets/`, `references/`, templates, and example HTML. On top of that, Open Design adds optional `od:` frontmatter fields:

- `mode`: prototype / deck / template / design-system.
- `preview.type`: html / jsx / pptx / markdown.
- `design_system.requires`: whether to inject `DESIGN.md`.
- `craft.requires`: whether to inject universal craft rules.
- `inputs`: structured UI forms.
- `parameters`: live tweak sliders.
- `outputs`: primary and secondary export files.
- `capabilities_required`: UI gating based on agent capability.

This is healthier than putting all design knowledge into one enormous hidden prompt.

A good skill can be versioned, forked, reviewed, copied, and shared. It can declare that it generates a landing page, dashboard, mobile onboarding flow, deck, weekly update, finance report, or product spec. It can ship an `example.html` as a quality reference.

From a builder perspective, file-based skills bring three benefits:

1. **Reuse**: every generation does not start from a blank prompt.
2. **Auditability**: a team can review exactly what design rules and workflow instructions a skill injects.
3. **Distribution**: third-party skills can spread like GitHub repos or packages.

This is one of Open Design’s clearest answers to Claude Design: in a closed product, “design capability” lives inside proprietary prompts and internal tools. Open Design tries to turn it into ordinary files.

---

## 6. Design systems: pull taste out of chat context

One of the hardest problems in AI design tools is that the model keeps reinventing the brand. Ask for “Stripe-like,” and it may only learn purple gradients and large headings. Ask for “premium,” and it may produce AI slop: excessive glassmorphism, meaningless glow, and default `#6366f1` accents.

Open Design’s answer is `DESIGN.md`.

A design system should not live only in chat context. It should be a versionable file containing:

- Visual Theme & Atmosphere
- Color Palette & Roles
- Typography Rules
- Component Stylings
- Layout Principles
- Depth & Elevation
- Do’s and Don’ts
- Responsive Behavior
- Agent Prompt Guide

The repository contains a large `design-systems/` catalog covering product styles such as Linear, Stripe, Vercel, Airbnb, Tesla, Notion, Anthropic, Apple, Cursor, Supabase, Figma, and Xiaohongshu.

Even more interesting is `craft/`. These are not brand-specific rules. They are universal design-craft constraints: typography, color, anti-ai-slop, and similar quality-floor guidance.

That gives Open Design two separate axes of taste:

- `DESIGN.md` for brand-specific rules.
- `craft/*.md` for universal design discipline.

This is a useful abstraction. Many AI design tools ship style presets, but fewer explicitly productize the craft rules that prevent generic AI-looking output.

---

## 7. Artifact-first: generated output must be real files

Open Design’s artifact store is also worth studying. `docs/architecture.md` describes artifacts as plain files under `.od/artifacts/<id>/`, with `artifact.json`, `index.html`, `assets/`, and append-only history in `history.jsonl`.

This is different from database-centered AI products.

Plain files have advantages:

- They can be reviewed with Git diff.
- The agent can read and modify them again.
- They can be exported as HTML, PDF, ZIP, Markdown, or PPTX.
- They can outlive Open Design itself.
- Builders can debug them with familiar tools.

For design tools, this matters a lot. If a generated design only lives inside a SaaS database, it is hard to bring into engineering workflows. If it is HTML, JSX, Markdown, PPTX JSON, and assets, it can move through PRs, CI, packaging, and handoff.

The preview system follows the same principle: raw HTML can render in an iframe; JSX can render via vendored React 18 + Babel in a sandboxed iframe; decks can preview as swipeable pages; exports can turn artifacts into PDF/PPTX/ZIP.

The product is not “a chat box that outputs an image.” It pushes the agent to produce maintainable artifacts.

---

## 8. Engineering boundaries: a disciplined monorepo

The repository’s `AGENTS.md` is unusually detailed, which suggests the project is already being maintained with AI agents in the loop. A few boundary rules stand out:

- `packages/contracts` must remain pure TypeScript, with no dependency on Next.js, Express, Node filesystem APIs, SQLite, daemon internals, or sidecar control-plane code.
- Sidecar concepts must stay in sidecar layers; app business logic should not know about runtime stamps.
- Local lifecycle must go through `pnpm tools-dev`; root aliases like `pnpm dev` or `pnpm start` are intentionally avoided.
- Packaged runtime paths must be namespace-scoped and must not depend on daemon or web ports.
- New `.js`, `.mjs`, or `.cjs` files require a generated/vendor/compatibility reason and must pass residual-JS checks.

These details may look mundane, but they are the kind of constraints that keep an agent-maintained codebase from collapsing into architectural drift.

Open Design is itself a design system for agents, and its own repository is written with agent-aware maintenance rules. That self-referential aspect is interesting: the codebase is not only designed for humans, but for humans and agents maintaining it together.

---

## 9. Current limitations and risks

The project is promising, but not yet a polished, mature product.

The main risks I see:

1. **Documentation drift**  
   README numbers, GitHub description numbers, and actual directory counts are not fully aligned. This is normal for a fast-moving project, but it needs cleanup.

2. **Multi-agent support is expensive to maintain**  
   Every CLI changes flags, auth behavior, streaming formats, and permission modes. Without strong adapter tests, this can become fragile.

3. **The local daemon security model must be explicit**  
   The daemon can spawn agents and read/write files. CWD sandboxing, allowed directories, SSRF protection, skill trust, and permission posture all need careful handling.

4. **Architecture does not automatically guarantee design quality**  
   Skills and `DESIGN.md` provide a quality floor, but output still depends heavily on the underlying model and agent. The hard part is not generating HTML; it is generating consistently tasteful, non-generic design.

5. **Artifact UX still needs polish**  
   Comment mode, surgical edits, slider tweaks, version history, and export fidelity are where Claude Design-like products win or lose. Open Design has the right abstractions, but the end-to-end feel will determine whether it becomes a daily tool.

---

## 10. Who should study it?

Open Design is especially relevant to three groups of builders.

First, **people building AI creative tools**. If you are working on video, image, slide, webpage, or marketing-material generation, the lesson is: do not stop at prompt-to-output. Build an artifact lifecycle.

Second, **people building coding-agent platforms**. The adapter design is pragmatic: do not rewrite the agent loop; detect, wrap, degrade, and normalize events.

Third, **teams trying to connect company design systems to AI**. The `DESIGN.md + skill + craft` stack is much more maintainable than describing a brand in every prompt.

If you work on local AI tools such as QCut, OpenClaw, or Hermes, the value is easy to recognize. Unlike traditional SaaS AI tools, Open Design is not trying to centralize everything in the cloud. It organizes the user’s local agents, filesystem, and existing toolchain into a coherent product loop.

---

## Conclusion: Open Design turns AI design into a composable local engineering system

The most interesting part of Open Design is not that it copies the surface of Claude Design.

The real value is in its abstractions:

- **Agent adapters** connect different coding-agent CLIs to one design workflow.
- **Skill registry** turns design capability into versionable, distributable folders.
- **Design-system resolver** pulls brand taste into `DESIGN.md` instead of hidden prompts.
- **Craft rules** productize universal design discipline.
- **Artifact store** makes generated output real files rather than one-off chat messages.
- **Local daemon** keeps dangerous capabilities on the user’s machine while exposing a clean web interface.

This points to a broader direction: next-generation AI creative tools will not merely be “models that draw better.” They will look more like **local-first production systems**. The model generates, the agent operates on files, skills define workflows, design systems define taste, the daemon owns permissions and lifecycle, and the UI provides feedback and control.

Open Design is still moving quickly, but it already offers a clear builder lesson:

**If you want to build a truly usable AI design product, do not only optimize prompts. Design the engineering system that lets prompts land safely, run repeatedly, be audited, be edited, and be exported.**
