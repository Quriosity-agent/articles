# AgentCraft Deep Dive: Turning AI Agent Ops into an RTS Command Center

AgentCraft positions itself as **“the agent orchestrator you’ve trained for”**: a game-like control layer over coding agents (Claude Code, OpenCode, Cursor, and experimental OpenClaw support). Instead of juggling terminal tabs, you get a live map of agents, status signals, mission tracking, and intervention workflows.

![AgentCraft homepage hero: RTS-styled command center positioning](assets/agentcraft/hero-home.png)
*Homepage hero section: product positioning and quick-start command.*

## TL;DR for builders

- **Core idea:** Agent orchestration UI inspired by RTS mechanics.
- **Operational model:** lightweight hooks in agent CLIs emit events to AgentCraft server.
- **Fast start:** `npx @idosal/agentcraft` (auto-detects CLIs, installs hooks, starts server on port 2468).
- **Strongest value:** multi-agent visibility + lifecycle control + human-in-the-loop approvals.
- **Notable advanced features:** remote mobile control (PWA + push/quick-reply), isolated containers, integrated terminal, worktrees, mission persistence.
- **Pricing signal:** no public pricing page found (`/pricing` returns 404); docs consistently frame it as open-source.

---

## 1) Product positioning and workflow

AgentCraft is intentionally opinionated: it treats each coding agent as a unit/hero with state transitions (spawned, active, idle, waiting for permission, subagent activity, etc.).

From docs, the lifecycle is:
1. Install AgentCraft and hooks.
2. Spawn agents from UI (or let external CLI sessions appear automatically).
3. Observe real-time activity, files touched, and status changes.
4. Approve plans/permissions when needed.
5. Track completed missions with persisted history.

![AgentCraft docs overview page with core features and quick start](assets/agentcraft/docs-overview.jpg)
*Documentation overview: feature surface and supported integrations.*

### Why this matters technically

Most agent setups fail operationally, not model-wise:
- no single place to monitor many sessions,
- poor interrupt/approval UX,
- weak auditability of what changed and why.

AgentCraft addresses this with a unified event-driven control plane on top of existing CLI agents.

---

## 2) Feature set that actually impacts engineering teams

### A. Single-pane visibility and control
The map/roster model gives a central state view for many agents. This is useful when parallel work increases and “which agent needs me now?” becomes a bottleneck.

### B. Remote access done as operations tooling
AgentCraft ships secure tunnel sharing with TTL presets (15m / 1h / 4h / 8h), mobile PWA installability, and push notifications.

![Remote Access & Mobile docs page](assets/agentcraft/remote-access.jpg)
*Remote operations model: expiring tunnel + mobile tabs + quick-reply actions.*

The practical win: you can approve plans/permissions from phone without returning to your desk.

### C. Isolated containers for safer parallelism
Containerized heroes can run in Docker (cross-platform) or Apple Containers (macOS 26+), with network/filesystem/browser isolation.

![Isolated Agent Containers docs page](assets/agentcraft/containers.png)
*Isolation model: separate network stack, filesystem, and browser session per agent.*

This is especially useful when multiple agents run dev servers on the same port or when security boundaries matter.

### D. Deep Claude Code integration (primary)
Hooks in `~/.claude/settings.json` emit events like SessionStart, UserPromptSubmit, PreToolUse, PermissionRequest, SubagentStop.

![Claude Code integration docs page](assets/agentcraft/claude-integration.jpg)
*Event taxonomy for mapping CLI behavior into live orchestration UI.*

This event granularity is critical for accurate status transitions and intervention timing.

---

## 3) CLI and operational ergonomics

The CLI reference is pragmatic:
- `npx @idosal/agentcraft` for guided setup,
- `start/stop/status/open` for runtime control,
- `install/uninstall/restore` for hook lifecycle,
- `doctor` for diagnostics,
- `--all-projects` for cross-project session visibility,
- daemon mode and custom port support.

For teams, the standout is reversibility: **restore** path and hook merge behavior are documented (important for trust).

---

## 4) Builder takeaways (what I’d copy)

1. **Event hooks over model hacks**: leverage existing agent CLIs with minimal invasive instrumentation.
2. **Human-in-the-loop UX first**: plan approvals + permission gating are first-class states.
3. **Ops-grade mobile path**: PWA + push + quick-reply bridges desk/off-desk workflow.
4. **Isolation as product feature**: container runtime choice exposed in spawn flow, not hidden infra.
5. **Gamification without losing utility**: RTS metaphors help cognition if state fidelity remains high.

---

## 5) Limitations and risks to watch

- **No explicit pricing/commercial packaging page** at time of review (could change quickly).
- **Hook fragility surface**: depends on each upstream CLI’s settings/hook contracts.
- **Cognitive split risk**: game-like metaphor is compelling, but may distract if teams need strict enterprise dashboards.
- **Security trust model**: remote tunnels and auth-token handling need careful org review despite documented TTL/token controls.
- **Integration maturity variance**: Claude Code appears primary; OpenClaw marked experimental.

---

## 6) Who should adopt now

Best fit today:
- solo builders and small AI-native teams running many concurrent coding agents,
- teams needing quick intervention loops (approve/deny/reply) with minimal coordination overhead,
- developers wanting safer parallel runs via container isolation.

Less ideal if you need:
- procurement-ready enterprise controls/SLA language on day one,
- strict non-gamified operational surfaces for compliance-heavy environments.

---

## Final assessment

AgentCraft is not “just a fancy UI.” It’s an **operational abstraction** over agent workflows, with a strong emphasis on state visibility, interruption handling, and controlled parallelism. If your pain is agent coordination rather than model quality, AgentCraft’s architecture is directionally right and already practical.

**Signature:** 🦞
