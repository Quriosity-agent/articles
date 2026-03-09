# RTK: The CLI Proxy That Cuts Your AI Coding Agent's Token Bill by 80%

> Every time your AI coding assistant runs `git status`, it burns ~2,000 tokens. The useful information? About 200. RTK fixes this.

## What Is RTK?

[RTK](https://github.com/rtk-ai/rtk) (Rust Token Killer) is a high-performance CLI proxy written in Rust that intercepts terminal commands executed by AI coding assistants (Claude Code, Cursor, etc.), intelligently filters and compresses the output, and reduces LLM token consumption by 60-90%.

- **Single Rust binary**, zero dependencies
- **<10ms overhead** per command
- **40+ commands** supported out of the box
- **MIT licensed**, fully open source

## Why Does This Matter?

AI coding assistants execute terminal commands constantly during a session. The problem: most of that output is noise.

Consider:

- `git push` outputs 15 lines, ~200 tokens → useful info is just `ok main` (~10 tokens)
- `cargo test` outputs 200+ lines → you only need the 2 failed tests (~20 lines)
- `ls -la` outputs 45 lines of permissions → the directory structure takes ~12 lines

In a typical dev session, these commands add up to ~118,000 tokens. With RTK? ~23,900 — **an 80% reduction**.

This isn't just about cost. Fewer tokens means more room in your context window for actual code and reasoning.

## Architecture

RTK's design is clean and modular, following a six-phase pipeline:

- **PARSE** — Clap parser extracts commands, arguments, and global flags
- **ROUTE** — Dispatches to specialized modules (git.rs, grep_cmd.rs, etc.)
- **EXECUTE** — Runs the original command, captures stdout/stderr/exit code
- **FILTER** — Applies smart filtering strategies to compress output
- **PRINT** — Outputs colorized, formatted results
- **TRACK** — Records token savings in SQLite for analytics

### Four Filtering Strategies

- **Smart Filtering** — Strips noise (comments, whitespace, boilerplate)
- **Grouping** — Aggregates similar items (files by directory, errors by type)
- **Truncation** — Keeps relevant context, cuts redundancy
- **Deduplication** — Collapses repeated log lines with occurrence counts

## Getting Started

```bash
# Homebrew (recommended)
brew install rtk

# Or curl install
curl -fsSL https://raw.githubusercontent.com/rtk-ai/rtk/refs/heads/master/install.sh | sh

# Or from source
cargo install --git https://github.com/rtk-ai/rtk
```

### Claude Code Integration (The Killer Feature)

```bash
# Install the global hook
rtk init --global

# Restart Claude Code. Done.
```

The hook transparently rewrites commands. When Claude Code runs `git status`, the hook silently rewrites it to `rtk git status`. Claude never sees the rewrite — it just gets compressed output.

### Usage Examples

```bash
# File operations
rtk ls .                        # Compact directory tree
rtk read file.rs                # Smart file reading
rtk read file.rs -l aggressive  # Function signatures only

# Git operations
rtk git status              # Compact status
rtk git log -n 10           # One-line commits
rtk git push                # Output: "ok main"

# Testing (failures only)
rtk test cargo test         # -90% tokens
rtk pytest                  # -90% tokens
rtk vitest run              # -99.5% tokens!

# Build & Lint
rtk tsc                     # TS errors grouped by file
rtk lint                    # ESLint grouped by rule
rtk cargo clippy            # -80%

# Analytics
rtk gain                    # Token savings summary
rtk gain --graph            # ASCII chart (last 30 days)
rtk discover                # Find missed optimization opportunities
```

## Command Coverage

RTK's modular architecture covers nearly every common dev scenario:

- **Git** — status, diff, log, add, commit, push, pull, branch, checkout (85-99% savings)
- **GitHub CLI** — pr list/view, issue list, run list (26-87% savings)
- **JS/TS ecosystem** — ESLint, TSC, Next.js, Prettier, Playwright, Vitest, Prisma, pnpm (70-99% savings)
- **Rust ecosystem** — cargo test/build/clippy (80-90% savings)
- **Python ecosystem** — pytest, ruff, pip (70-90% savings)
- **Go ecosystem** — go test/build/vet, golangci-lint (75-90% savings)
- **Containers** — Docker, Podman, kubectl (60-80% savings)
- **General** — grep, find, curl, wget, JSON, logs (50-95% savings)

## How It Compares

RTK occupies a unique niche in the AI dev tools landscape:

- **No optimization (baseline)** — Raw command output goes straight to the LLM. Wasteful but simple. RTK exists to fix this.
- **Prompt engineering / .claude config** — You can ask the AI to "be concise," but you can't control what `git push` prints. RTK intercepts at the command level, which is fundamentally more effective.
- **Context window tools** (repomix, aider's repo map) — These compress code context; RTK compresses command output. They're complementary, not competing.
- **Custom shell wrappers** — You could hand-roll scripts, but RTK gives you 40+ optimized commands out of the box, written in Rust with near-zero overhead.

## Design Philosophy

- **Fail-safe** — If filtering fails, fall back to raw output. Never lose information.
- **Exit code preservation** — Proper exit code propagation for CI/CD compatibility.
- **Tee mode** — On failure, saves full unfiltered output to a log file so the LLM can read it without re-executing.
- **Configurable** — Exclude specific commands, custom database paths, tee behavior control.
- **Dual hook strategies** — Auto-Rewrite (100% adoption) and Suggest mode (Claude decides autonomously, good for auditing).

## The Bottom Line

RTK solves a real, measurable problem: token waste in AI coding workflows. As tools like Claude Code become central to development, a CLI proxy that saves 80% of token consumption isn't a nice-to-have — it's essential infrastructure.

Written in Rust. Zero dependencies. <10ms overhead. 40+ commands. If you're using an AI coding assistant, RTK is worth your time.

- GitHub: https://github.com/rtk-ai/rtk
- Website: https://www.rtk-ai.app
- Discord: https://discord.gg/gFwRPEKq4p

🦞
