# VM0 Technical Architecture Deep Dive: Turning an AI Teammate into an App Layer, Permission Layer, and MicroVM Runtime

> Repo: [vm0-ai/vm0](https://github.com/vm0-ai/vm0)  
> Inspected commit: `2b64ac7` (`refactor(api): migrate zero runs create route (#13076)`)  
> Date: 2026-05-13  
> Tags: VM0 / Zero / AI Agent Runtime / Firecracker / Sandbox / Hono / Next.js / Agent Infrastructure

![VM0 GitHub repository screenshot](imgs/vm0-ai-agent-runtime-architecture/github-repo.png)

VM0 is not just a “Slack bot plus LLM calls” project. It is closer to an enterprise-grade **AI teammate runtime**: product entry points on Slack/Web/CLI, a middle control plane for agents, orgs, connectors, permissions, billing, schedules, memory, and artifacts, and a Rust-based Firecracker microVM execution layer underneath.

The shortest summary of its architecture is:

> **Take agents out of the chat box and place them inside an authorized, queued, auditable, isolated, resumable runtime.**

This article breaks down VM0 from the perspective of repository structure, run lifecycle, isolation model, connector permissions, storage, and testing culture.

---

## This Is Not a Demo Repository

I inspected commit `2b64ac7`. The GitHub page shows roughly **1.1k stars / 61 forks**, and the latest main-branch commit is `refactor(api): migrate zero runs create route (#13076)`, which signals an actively evolving migration and refactor effort.

From the repository layout, VM0 is already a full platform codebase:

| Metric | Count |
|---|---:|
| Working-tree files, excluding `.git` / deps / build dirs | ~6,672 |
| Rust crates | 19 |
| TypeScript files | 3,329 |
| TSX files | 392 |
| Rust files | ~232 |
| SQL migration files | 368 |
| Hono API route files | 153 |
| Next.js route handlers | 266 |
| DB schema files | 82 |
| Connector implementation files | 180 |
| Bats E2E tests | 56 |
| Playwright E2E tests | 9 |

The important part is the layering:

- `turbo/apps/web/`: Next.js Web app and many legacy API routes still being migrated.
- `turbo/apps/api/`: New API service based on Hono, OpenTelemetry, Sentry, and Axiom logging.
- `turbo/apps/platform/`: Vite/React platform UI for activity, schedules, connectors, agents, permissions, billing, and more.
- `turbo/apps/cli/`: `@vm0/cli`, covering auth, compose, run, volume, artifact, `zero` subcommands, and computer-use features.
- `turbo/packages/db/`: Drizzle schemas for orgs, agents, runs, runner queues, connectors, secrets, schedules, billing, and more.
- `turbo/packages/connectors/`: 100+ tool connectors, OAuth providers, firewall policies, and permission rules.
- `crates/`: Rust sandbox runtime: runner, Firecracker backend, guest agent, vsock, NBD COW, guest download.
- `docs/`: architecture, resource model, testing, dev workflow, security, and operations docs.
- `.claude/skills/`: project skills for coding agents, including testing, database development, code quality, and project principles.

VM0’s core asset is therefore not a single UI or prompt. It is a full-stack agent platform, from product entry points down to sandbox execution.

---

## A Five-Layer View of VM0

Based on `docs/architecture.md`, `docs/resource-model.md`, and the actual code structure, VM0 can be modeled as five layers:

```text
User entry layer
  Slack / Web app / CLI / Telegram / Phone / API
        ↓
Product control plane
  agents / schedules / chats / orgs / billing / permissions / connectors
        ↓
Run control plane
  run create → context resolution → runner_job_queue → realtime notification
        ↓
Execution layer
  Rust runner → Firecracker microVM → guest-init / guest-agent / guest-download
        ↓
Persistence and audit layer
  Postgres / Drizzle / R2 storages / artifacts / memories / logs / network traces
```

The key idea: an agent’s “intelligence” is not the same as product capability. What makes it deployable inside teams is the middle stack: permissions, context resolution, isolation, auditability, and recovery.

---

## Layer 1: Product Entry Is a Set of Channel Adapters

VM0’s README positions Zero as a teammate that can handle reports, triage, outreach, and research in Slack or on the web. The code shows that it is not a single-channel product:

- `apps/web/app/api/zero/slack/*`: Slack OAuth, events, interactive messages, commands, and channels.
- `apps/web/app/api/telegram/*`: Telegram webhook, register, setup status.
- `apps/web/app/api/zero/voice-chat/*` and `zero/voice-io/*`: voice sessions, STT, TTS, and quota.
- `apps/platform/src/views/zero-page/`: Web agent chat, settings, activity, connectors, schedules.
- `apps/cli/src/commands/zero/*`: CLI management for agents, schedules, orgs, variables, remote agents, skills, and search.

So VM0’s product abstraction is not “a chat app.” It is a multi-entry agent control plane. Slack is only one channel; Web, CLI, Telegram, and voice all share the same underlying agent/run/resource model.

That matters because the same agent may be triggered from different contexts, but identity, permissions, memory, artifacts, and connectors should not become separate systems per channel.

---

## Layer 2: The Org + User Resource Model Solves Credential Ownership

`docs/resource-model.md` is one of the most important documents in the repo. It splits execution into two org concepts:

1. **Agent Org**: where the agent definition lives; owns agent compose and volumes.
2. **Runtime Org + userId**: the user context that triggers the run; owns artifacts, memories, secrets, variables, connectors, and model providers.

This solves a real team problem:

> If Team A publishes an agent and User B runs it, the run should use User B’s authorized GitHub/Slack/Linear/Gmail credentials in the current org — not the agent author’s credentials.

VM0 documents a two-phase resolution flow:

```text
Phase 1: Runtime Org + userId
  ├── secrets
  ├── model provider credentials
  ├── connector tokens / OAuth refresh
  └── variables

Phase 2: Agent Org + Runtime Org
  ├── volumes
  ├── artifact storage
  ├── memory storage
  └── presigned storage manifest
```

This is much safer than putting every token into an agent config. Agents can be shared, but runtime credentials remain bound to the triggering user. Agent definitions and user-private resources are separated. Scheduled runs also carry their own `(orgId, userId)`, preserving identity boundaries over time.

---

## Layer 3: Run Creation Is the Heart of VM0

The latest commit is about migrating the `zero runs create route`, which makes this a good place to inspect. `turbo/apps/api/src/signals/routes/zero-runs.ts` hands run creation to `createZeroRun$`, which then calls `createAgentRun$`.

The flow looks like this:

```text
POST /zero/runs
  ↓
Auth + capability check: agent-run:write
  ↓
load Zero agent + validate visibility
  ↓
load user info / connectors / custom connectors
  ↓
resolve firewall policies + framework skills
  ↓
createAgentRun$
  ↓
resolve compose / model provider / secrets / variables / storage manifest
  ↓
insert agent_runs + runner_job_queue
  ↓
publishRunnerJobNotification via realtime
```

A few details in `zero-runs-create.service.ts` are especially telling:

- It mounts system skills into `/home/user/.claude/skills` or `/home/user/.codex/skills`, depending on the agent framework.
- It appends agent identity, tone, current user info, and Zero CLI usage instructions to the system prompt.
- It explicitly disallows tools such as `CronCreate`, `CronList`, `CronDelete`, `ScheduleWakeup`, and `AskUserQuestion`, avoiding recursive scheduling or direct user prompts from inside the sandbox.
- It generates callback secrets for agent-triggered runs, making callbacks verifiable.
- It passes permission policies, connector allowlists, and custom connector allowlists into the underlying run.

VM0 is not “send prompt to model.” At run creation time, it binds identity, permissions, skills, model provider, connectors, memory/artifacts, callbacks, quotas, and queueing into one executable context.

---

## Layer 4: The Database Queue Bridges API and Rust Runtime

`runner_job_queue` is the boundary between the Web/API world and the Rust runtime world. Its Drizzle schema contains:

- `runId`: primary key referencing `agent_runs`.
- `runnerGroup`: which runner group should execute the job.
- `profile`: default `vm0/default`.
- `sessionId`: for session affinity.
- `claimedAt`: claim status.
- `executionContext`: JSONB; comments note that secrets are encrypted with AES-256-GCM.
- `expiresAt`: TTL cleanup.

`dispatchRun()` in `agent-run-create.service.ts` does four important things:

1. Builds the runner job payload.
2. Inserts into `runnerJobQueue`.
3. Updates `agentRuns.runnerGroup`.
4. Calls `publishRunnerJobNotification()` to wake a runner.

`docs/architecture.md` adds the runner behavior: runners subscribe to Ably channel `runner-group:{org}/{name}`, wake on notification, HTTP poll, atomically claim jobs, execute inside Firecracker, and report completion through webhooks.

This design keeps API servers from directly launching VMs. They write a durable queue entry and publish a wakeup signal. Runners can scale independently, fall back to 30-second polling, and use session affinity. The queue also stores temporary execution context rather than long-lived secrets.

---

## Layer 5: Firecracker MicroVMs Are the Real Moat

`crates/README.md` explains the Rust workspace clearly:

| Crate | Role |
|---|---|
| `runner` | Polls jobs, manages VM lifecycle, proxy, service install, and bridges to `sandbox-fc` |
| `sandbox` | Sandbox traits and shared types |
| `sandbox-fc` | Firecracker implementation: VM lifecycle, network namespace pool, NBD COW, snapshot restore |
| `nbd-cow` | Userspace NBD copy-on-write block device |
| `vsock-host` / `vsock-guest` / `vsock-proto` | Host/guest IPC protocol |
| `guest-init` | PID 1 inside the Firecracker VM |
| `guest-agent` | Runs CLI commands, heartbeat, telemetry, checkpointing inside the VM |
| `guest-download` | Downloads and extracts R2 storage archives |
| `ably-subscriber` | Runner realtime notification client |

`docs/architecture.md` adds more operational detail: each agent execution runs in a Firecracker microVM with KVM hardware isolation; VM boot takes roughly 3–5 seconds; each VM gets its own network namespace; HTTP/HTTPS is logged through mitmproxy; rootfs uses a shared read-only base plus NBD COW to avoid copying a full disk per run.

The important design choice is that VM0 does not use Docker as the final isolation boundary. If an agent can execute shell commands, read and write code, install packages, call APIs, and carry user credentials, it should be treated as an untrusted workload. Firecracker gives VM0 a cleaner boundary.

---

## Storage: R2 + Presigned URLs + Manifest, Not API-Proxy File Streaming

VM0 uses Cloudflare R2 as the storage layer. The documented flow is:

```text
CLI → tar.gz archive → presigned PUT URL → R2
DB records: storage_id, version_id, s3_key

API → presigned GET URL → storage manifest JSON
sandbox → direct download from R2 → extract to mount paths
```

This has several practical advantages:

- Large files do not need to pass through the API server.
- Artifacts, memories, and volumes can all be managed as versioned archives.
- Sandboxes receive short-lived presigned URLs rather than broad storage credentials.
- Resume and checkpoint flows can be based on artifact/memory versions instead of local VM state.

For an agent platform, artifacts and memory are not just “file storage.” They are what make an agent a long-lived teammate rather than a one-shot command runner.

---

## Permissions Are a Connector Firewall, Not a Single Toggle

The README says VM0 supports 100+ tools. In the repo, the practical implementation lives in `turbo/packages/connectors/` and `turbo/packages/firewalls-generator/`:

- `connectors/src/connectors/*.ts` contains about 180 connector files.
- `oauth-providers/providers/` includes handlers for Figma, Atlassian, Microsoft, Spotify, ElevenLabs, Fal, Brevo, and more.
- `firewall-types.ts`, `firewall-loader.ts`, and `firewall-rule-matcher.ts` turn connector permissions into matchable tool/network policies.
- `zero-runs-create.service.ts` resolves firewall policies from allowed connector types and passes them into the run execution context.

This is crucial. Enterprise agents do not merely need to “connect to GitHub.” They must answer:

- Can this agent read the repo? Can it write?
- Which API endpoints can it access?
- How are OAuth tokens refreshed?
- Are connector tokens injected as secrets?
- Does the agent ever see raw token values?
- Is each API call auditable?

VM0’s direction is to keep connector, secret, firewall, network log, and permission policy in the same run pipeline. That is much closer to production than a “tool list plus prompt instructions.”

---

## The API Is Migrating from Next.js to Hono

The repo is visibly in transition: `apps/web` still has many Next route handlers, while `apps/api` is becoming the new API service.

`CLAUDE.md` states this explicitly: API traffic is migrating from `apps/web` to `apps/api`, and feature work must keep both implementations in sync until the relevant route is fully API-authoritative.

`apps/api/src/app-factory.ts` shows the migration strategy:

- A Hono app registers new typed routes.
- It adds OpenTelemetry middleware, route baggage, CORS, and Axiom log flushing.
- Unmigrated routes fall back by proxying to `VM0_WEB_URL`, keeping legacy traffic alive.

This is a pragmatic migration path: no big-bang rewrite, but a new API domain that gradually absorbs routes while proxying legacy traffic. The cost is temporary complexity; the benefit is continuous product operation.

---

## Testing and Engineering Culture: A Repo for Humans and Agents

One striking signal is that VM0 includes `.claude/skills/` and `.claude/commands/` in the repository.

These are not primarily for end users. They are for coding agents working inside the repo:

- `testing`: integration-test-first rules, real DB/filesystem, mock only external dependencies.
- `project-principles`: YAGNI, no defensive programming, type safety, zero lint tolerance.
- `database-development`: database workflow.
- `code-quality`: lint/typecheck/knip rules.
- `.claude/commands/tech-debt-*`: commandized workflows for tech debt research and issue creation.

This reveals a self-hosting direction: VM0 is not only building an agent product, it is making its own repo legible and operable by agents. For agent-heavy engineering, putting project principles and workflows into agent-readable files is more useful than hiding them in Notion.

---

## Design Choices Worth Borrowing

### 1. Model “an agent run” as a durable run

VM0 does not treat a run as a single HTTP request. It has `agent_runs`, `runner_job_queue`, statuses, heartbeats, callbacks, queues, concurrency limits, usage events, billing, and logs. That is what makes runs queueable, recoverable, auditable, billable, cancellable, and retryable.

### 2. Split resource ownership into Agent Org and Runtime Org

This maps much better to real teams: agents can be shared, but credentials and outputs must belong to the triggering user.

### 3. Put connector permissions into execution context

Permissions should not only appear in the UI. VM0 sends connector allowlists, firewall policies, secrets, and network policies into the run payload so lower layers can enforce them.

### 4. Use microVMs as the untrusted workload boundary

If an agent can run shell commands, edit repositories, install packages, and call APIs, it needs a clear isolation boundary. Firecracker is a strong architectural choice.

### 5. Migrate APIs incrementally with a proxy fallback

The Hono API plus legacy Next fallback proxy is a realistic pattern for fast-moving products.

---

## Risks and Complexity

VM0’s architecture is powerful, but it is not simple:

1. **Large platform surface**: Next.js, Hono, Vite, Rust, Firecracker, R2, Postgres, Ably, Axiom, Sentry, Clerk, and Stripe are all part of the system.
2. **API migration overhead**: `apps/web` and `apps/api` coexist, which creates synchronization costs.
3. **Self-hosting is non-trivial**: Firecracker needs bare-metal Linux, KVM, kernel/rootfs setup, NBD, network namespaces, and mitmproxy.
4. **Connector permissions are a long-term maintenance burden**: 100+ connectors means OAuth, refresh, API shape, rate limits, and audit rules constantly change.
5. **Security claims require end-to-end consistency**: credentials, microVM isolation, audit trails, token injection, proxying, network policy, encryption, and log redaction must all work across every path.

So VM0 is best understood as a rapidly evolving “agent OS startup repo,” not a lightweight library.

---

## What Builders Should Learn from VM0

If you are building agent products, VM0 suggests several lessons:

- **Do not reduce agent platforms to chat UIs.** Chat is an entry point; the real system is identity, permissions, state, execution, and audit.
- **Do not put tool governance only in prompts.** Permissions need to live in the data model, execution context, and network boundary.
- **Do not treat sandboxing as optional.** Task-executing agents need a clear isolation layer.
- **Do not ignore artifacts and memory.** Long-lived teammates require versioned, recoverable, isolated state.
- **Do not keep agent development conventions only in human docs.** Agent-readable skills for workflow, tests, code quality, and project principles will matter more over time.

VM0’s most interesting part is not that Zero can write reports, outreach, or triage. It is that the runtime beneath those capabilities is being engineered as a multi-layer control system.

That may be the real boundary between an AI chatbot and an AI teammate:

> A chatbot answers. An AI teammate safely acts.

VM0’s repository is an attempt to engineer the “safely acts” part.
