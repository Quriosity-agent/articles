# RGB Agent: Solving ARC-AGI-3 in 1,069 Actions — Fewer Than Humans

> **TL;DR**: Alexis Fox (Duke NLP) open-sourced the RGB Agent (Read-Grep-Bash), which completed all three ARC-AGI-3 preview games in just 1,069 actions — the lowest publicly reported count. Humans need ~900. The design philosophy is deceptively simple: let the agent decide what to abstract, not the harness.

---

## Background

We previously covered ARC-AGI-3 in depth in our [ARC-AGI-3-Agents analysis](../2026-02-27/arc-agi-3-agents.md). Quick recap:

- ARC-AGI-3 is an **interactive reasoning benchmark** designed by François Chollet's team
- Unlike previous versions, it uses video-game-like environments where agents must discover rules through exploration
- No instructions, no hints — pure exploration, observation, and reasoning
- Each frame is a 64×64 pixel RGB image with a 16-color palette
- Humans find it intuitive; AI systems struggle significantly

## What is the RGB Agent?

RGB = **Read-Grep-Bash**. The name says it all — an agent built on the most fundamental Unix tool philosophy.

### Core Architecture

![RGB Agent Architecture](rgb-agent-architecture.png)

The entire system runs inside a **Docker container**. The architecture is minimal:

```
┌─────────────────────── Docker Container ───────────────────────┐
│                                                                 │
│   ┌──────────┐    calls    ┌──────────────┐    file-based     │
│   │          │ ──────────→ │  Tool Space   │ ←──────────────→  │
│   │ LLM      │             │              │    memory access   │
│   │ (Opus    │             │  READ        │                    │
│   │  4.6)    │             │  GREP        │    ┌────────────┐  │
│   │          │             │  BASH*       │    │ Game Logs  │  │
│   └────┬─────┘             │ (*Python only)│ ──→│            │  │
│        │                   └──────────────┘    │ • Actions   │  │
│        │ Batched Actions                       │ • Scores    │  │
│        │ (up to 10)                            │ • 64×64 grid│  │
│        │                                       │ • Plans     │  │
│        ▼                                       └──────┬─────┘  │
│   ┌──────────┐                                        │        │
│   │ ARC-AGI-3│  Structured logs (actions, score,      │        │
│   │ Env      │  board state) ────────────────────────→┘        │
│   └──────────┘                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Key design: files are memory.** The LLM's context window is finite, so Game Logs serve as **persistent external memory**. The agent queries history via READ and GREP, overcoming context window limitations.

**Core loop (each step):**
1. LLM reads current state from Game Logs via READ/GREP
2. LLM reasons and formulates a plan
3. Plan is appended to Game Logs (persisted)
4. LLM sends **batched actions (up to 10)** to the ARC-AGI-3 environment
5. Environment executes actions, produces structured logs (actions, score, 64×64 board state)
6. Logs are written back to Game Logs
7. Cycle repeats

**Three tools, nothing more:**
- **READ** — read log files and state files
- **GREP** — search files for patterns (history recall)
- **BASH*** — execute Python scripts (*restricted to Python only — no arbitrary shell commands)

**What Game Logs contain (visible from architecture diagram):**
```
Action 20 | Level 1 | Attempt 1 | Plan Step 3/3
Score: 0 | State: NOT_FINISHED
Current Plan: Move Down 3 times from (38,19) to explore left column
Recent History:
  Step 14: ACTION1 → score 0 → changed (32,19) to blue
  Step 15: ACTION2 → score 0 → moved to (33,19)
  ...
[64×64 ASCII matrix representing current board state]
```

### Key Configuration

- `--max-actions 500`: budget of 500 actions per game
- `--analyzer-interval 10`: batch analysis every 10 steps
- `--operation-mode online`: supports online/offline/normal modes
- Multi-model support: Claude Opus 4.6 (default), GPT 5.2, Gemini 2.5 Pro, or anything on OpenRouter

## Design Philosophy

Alexis Fox articulated three core principles:

**1. The agent should decide what to abstract, not the harness**

- Many ARC-AGI-3 approaches pre-bake abstractions at the framework level (e.g., preprocessing pixels into grids, extracting color patterns)
- RGB Agent takes the opposite approach: feed raw observations to the agent and let it decide what matters
- This means the agent can discover abstraction patterns that human designers didn't anticipate

**2. Solve complex problems with the simplest tool combinations**

- Read (observe state), Grep (search for patterns), Bash (execute Python)
- No dependency on complex specialized frameworks — just Unix-philosophy small tools composed together
- Bash is restricted to **Python scripts only** — prevents the agent from taking shortcuts with arbitrary commands
- A simpler architecture is easier to debug and iterate on

**3. Files are the best memory**

- LLM context windows are finite (even 200K tokens isn't enough for full game history)
- Game Logs serve as **persistent external memory** — GREP searching is far more efficient than re-reading everything
- Every action result (action taken, score, 64×64 board state) is written as structured logs
- This is essentially a **searchable long-term memory system** bolted onto the LLM

## Results

- **Total actions**: 1,069 across all three preview games (ls20, vc33, ft09)
- **Human baseline**: ~900 actions
- **Lowest publicly reported count**
- Not quite human-level yet, but the gap is remarkably small

## Comparison with Arcgentica

In our previous article, we analyzed Symbolica's Arcgentica approach (orchestrator + explorer/theorist/tester/solver). Key differences:

- **Arcgentica**: heavy specialization, each sub-agent has a distinct role, shared memory database, compressed information passing
- **RGB Agent**: lighter swarm architecture, emphasizes agent-driven abstraction, analyzer does periodic batch planning
- Both agree on a core principle: **the orchestrator should never directly manipulate the game** — it makes strategic decisions only

## Takeaways

The RGB Agent's success highlights several interesting trends:

- **Simple architecture + strong model > complex architecture + weak model**: rather than designing elaborate multi-agent pipelines, give a powerful model (Claude Opus 4.6) more autonomy
- **Abstraction should be emergent, not prescribed**: let the agent discover patterns rather than engineering features by hand
- **Unix philosophy still works in the AI agent era**: small tools, pipelines, text interfaces — design principles from 50 years ago remain effective for LLM agents
- **ARC-AGI-3 is driving real research**: Mike Knoop (ARC Prize co-founder) cited this work, noting "ARC v3 starting to produce new research ideas for agents"

## Resources

- Original blog post: <https://blog.alexisfox.dev/arcagi3>
- Code repository: <https://github.com/alexisfox7/RGB-Agent>
- ARC-AGI-3 official: <https://three.arcprize.org/>
- Our ARC-AGI-3 agent framework analysis: [2026-02-27/arc-agi-3-agents.md](../2026-02-27/arc-agi-3-agents.md)

---

🦞
