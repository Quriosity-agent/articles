# Orca Deep Dive: The Next Layer of AI IDEs Is Not Chat, but a Parallel Agent Control Plane

> Repo: [stablyai/orca](https://github.com/stablyai/orca)  
> Inspected commit: `f708e57` (`fix: pr-bug-scan validated finding from #1877 (#1891)`)  
> Date: 2026-05-14  
> Tags: Orca / AI IDE / Parallel Agents / Worktrees / Electron / TypeScript / SSH / Mobile Companion

![stablyai/orca GitHub repo](imgs/orca-parallel-agent-ide-control-plane/github-repo.png)

If we roughly divide AI coding tools into layers, the first layer was code completion, the second was chat-based editing, and the third was putting a CLI coding agent into a terminal. Orca is working on the next problem: once a builder wants to run not one Claude Code, Codex, or OpenCode session, but a fleet of agents at the same time, the hard part is no longer model access. The hard part becomes **control, isolation, state, review, and remote execution**.

Orca’s README calls it “The AI Orchestrator for 100x builders”: run Claude Code, Codex, or OpenCode side-by-side across repos, with each agent in its own worktree and tracked in one place. That sounds like a product slogan, but the repository structure shows that this is not a thin UI shell. It is closer to a local-first agentic development environment: Electron desktop app, CLI, SSH relay, GitHub/Linear integration, mobile companion app, terminal and browser panes, AI diff review, usage tracking, and a command surface for multi-agent orchestration.

## A few grounded repository facts

At the time of inspection, `stablyai/orca` is an MIT-licensed TypeScript project. GitHub API metadata showed roughly **2.4k stars**, **162 forks**, default branch `main`, and TypeScript as the primary language. The repository was created on 2026-03-17, yet the GitHub page already showed **1,892 commits**, which suggests a very high shipping cadence.

I inspected commit `f708e57`. Excluding `.git`, `node_modules`, `dist/out/build`, and similar generated directories, the repository contains about **1,971 files**. It has **1,447 `.ts` files**, **313 `.tsx` files**, and **29 Markdown files**. A rough text/code line count came to about **472k lines**, including:

- `src/`: about **408k lines**, the core desktop app and runtime;
- `mobile/`: about **32k lines**, the mobile companion app;
- `tests/`: about **8.9k lines**, including Playwright/Electron E2E coverage;
- `docs/`: about **3.7k lines**, including multilingual READMEs, design docs, and style guidance;
- `skills/`: about **987 lines**, indicating that the project also stores agent-facing workflow assets.

These numbers should not be read as a precise LOC leaderboard, but they are enough to show that Orca is not merely “a terminal wrapper with buttons.” It is a fairly complete desktop development product.

## The product idea: turn agents from “sessions” into “workstations”

Most AI IDEs still treat an agent as a chat thread or a terminal session. Orca’s more interesting move is to treat each agent as a workstation that can be assigned, isolated, observed, reviewed, and discarded.

The key README features are not just “Claude Code support” or “Codex support.” They are the combination:

- **Worktree-native**: every feature or task gets its own Git worktree, reducing stashing, branch juggling, and accidental overlap;
- **Multi-agent terminals**: run multiple AI agents side-by-side in tabs and panes, with visible activity state;
- **Built-in source control**: review AI-generated diffs, edit, and commit inside the app;
- **GitHub integration**: PRs, issues, and Actions checks are linked to the relevant worktree;
- **SSH support**: connect to remote machines and run agents there;
- **Mobile companion app**: control agents from a phone.

The underlying bet is that future coding agents will not exist as one chat window. They will look more like a group of background workers. The human’s job shifts from typing every prompt to managing concurrent tasks: which task lives in which branch, which agent is stuck, which diff needs review, which remote environment is still alive, and which worktree should be merged or thrown away.

## Architecture: Electron UI + local runtime + CLI + relay

`package.json` shows an Electron + React + TypeScript application. `electron-vite` handles desktop builds, React 19 and shadcn/radix-style primitives drive the UI, `node-pty` and `@xterm/*` power terminal behavior, `better-sqlite3` stores local state, and `simple-git` plus GitHub/Linear integrations connect Orca back to the development workflow.

The repository can be read in several layers:

1. **`src/renderer/src`**: the desktop UI. It contains sidebar, tab bar, terminal pane, status bar, settings, stats, browser, markdown/editor, and many workspace components. Orca is not simply launching terminals; it is turning terminals, browsers, files, status, and diff review into composable panes in one workspace.
2. **`src/main`**: the Electron main process and local runtime capabilities. This layer handles windows, IPC, SSH, telemetry, updater flows, providers, agent hooks, port scanning, worktrees, and filesystem access.
3. **`src/shared`**: shared types, protocols, state schemas, and agent enums. `agent-kind.ts` maps Claude, Codex, OpenCode, Gemini, Hermes, Goose, Cursor, Qwen Code, and many others to telemetry kinds, which makes the intent clear: Orca wants to support a growing ecosystem of CLI agents, not a single model vendor.
4. **`src/cli`**: the command-line control surface. Beyond repo/worktree/terminal/browser operations, `src/cli/specs/orchestration.ts` defines commands for orchestration: `send`, `check`, `reply`, `inbox`, `task-create`, `task-list`, `task-update`, `dispatch`, `ask`, `run`, and decision gates.
5. **`mobile/`**: the mobile companion app, allowing users to observe or control agents away from the desktop.

Together, these layers form a local agent control plane: UI as the control surface, worktrees as isolation units, terminal/PTY as the execution layer, Git/GitHub/Linear as delivery interfaces, SSH relay as the remote execution boundary, and CLI orchestration as the automation layer.

## SSH is not a side feature; it defines the product boundary

Many desktop AI coding tools assume local execution. Orca’s `AGENTS.md` explicitly says that all changes must consider the SSH use case and must not assume local-only execution. The file `src/main/ssh/ssh-relay-session.ts` shows that SSH support is not just “open a terminal over SSH.” It includes session state, a multiplexer, provider registration, relay version mismatch handling, port scanning, agent hook relay, and remote filesystem/Git/PTY providers.

That is an important engineering signal. Orca treats remote execution as another provider behind the same local control plane. For real agent work, this matters: agents often need to run tests, builds, browsers, GPU tasks, private-network calls, or more stable Linux environments. Keeping everything on a user laptop is neither stable nor easy to audit.

## CLI orchestration is the hidden layer worth watching

The README shows the user-facing product, but `src/cli/specs/orchestration.ts` reveals a more strategic direction. It includes commands for:

- `orchestration send/check/reply/inbox`: inter-agent messages;
- `task-create/task-list/task-update`: task state management;
- `dispatch/dispatch-show`: dispatching tasks to a specific terminal or agent;
- `ask`: blocking questions to a coordinator;
- `run/run-stop`: starting or stopping a coordinator loop;
- `gate-create/gate-resolve/gate-list`: decision gates.

This already resembles a lightweight multi-agent scheduling system. Orca is not merely laying out multiple terminals on a grid; it is beginning to model tasks, messages, dispatch, decision points, and completion. For builders, this is the most reusable lesson: when the number of agents grows from one to five or ten, layout is not the core problem. The core problem is task lifecycle and human intervention.

## Why Git worktrees are the right isolation primitive

Many agent orchestration systems start by inventing a custom sandbox or database state model. For coding agents, Git worktrees are a pragmatic middle layer. They are lightweight, naturally tied to branches/diffs/commits, and allow multiple agents to work on the same repository in separate working directories.

By making worktrees a first-class concept, Orca puts agent output directly into a version-control model that developers already understand. That gives it several advantages:

1. **Conflict isolation**: agents do not overwrite one shared working directory;
2. **Natural review**: results appear as diffs, commits, and PRs;
3. **Cheap failure disposal**: a bad worktree can be deleted without polluting the main branch;
4. **Parallel scaling**: multiple tasks can move forward at once, while humans converge at review time.

This is why Orca feels different from a normal “AI chat inside an IDE.” It organizes around change sets and workspaces, not just conversations.

## Quality signals: tests, design system, and cross-platform constraints

The test suite covers worktree lifecycle, terminal panes, output scheduling, dead terminal stress, SSH localhost behavior, browser tabs, file opening, source-control discard confirmation, and resource usage reattach scenarios. `AGENTS.md` also requires UI work to follow `docs/STYLEGUIDE.md`, warns against hardcoding `metaKey`, and requires path handling through Node/Electron path utilities.

These details indicate product-grade complexity. Electron cross-platform behavior, terminal lifecycle, remote relay, agent hooks, persistent state, mobile connection, and diff review are all bug magnets. The repository’s recent history includes many fixes around bug-scan findings, macOS entitlements, Windows EPERM, release artifacts, and mobile documentation, which suggests the team is polishing the system against real usage.

## Limitations and risks

Orca’s direction is strong, but this category has unavoidable difficulty:

- **Complexity compounds quickly**: once a product supports multiple agents, platforms, SSH, mobile, GitHub/Linear, browser panes, and terminals, reliability matters more than feature count.
- **BYO subscription lowers the entry barrier but shifts account complexity**: users can bring their own Claude/Codex/OpenCode subscriptions, but Orca must deal with local CLIs, login state, quotas, usage, and recovery.
- **Multi-agent orchestration needs stronger semantics over time**: a terminal grid is only the beginning; long-term workflows need dependencies, result scoring, merge policies, rollback, and human approvals.
- **Security boundaries become sensitive**: agents can run commands, access repositories, connect to remote machines, and read/write files. Permissions, auditing, and prompt-injection resistance become product concerns.

## What builders should borrow

The most useful lesson from Orca is not “support many models.” It is the product abstraction:

- Use **Git worktrees** as the isolation unit for agent work;
- Use **terminal/PTY plus providers** to stay compatible with the existing CLI-agent ecosystem;
- Use **source-control review** to bring AI output back into the software engineering loop;
- Use **SSH relay** to decouple local UI from remote execution;
- Use **CLI orchestration** as the bridge to automation;
- Use a **mobile companion** because agent work spans devices and time.

This is also a signal for the AI IDE market. The next defensible layer is not just better autocomplete or a prettier chat panel. It is the system that makes “a fleet of agents working in real codebases” controllable, reviewable, recoverable, and remotely executable.

Orca is still moving fast, but it is asking the right question: when a coding agent stops being a single assistant and becomes a small team, what developers need is a control plane.
