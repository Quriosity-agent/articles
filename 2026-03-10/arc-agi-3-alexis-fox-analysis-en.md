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

- **Swarm orchestrator**: coordinates multiple sub-agents working in parallel
- **Analyzer**: performs batch analysis of game state at regular intervals (default: every 10 actions), producing plans for the next phase
- **Docker sandbox**: the analyzer runs code in an isolated opencode-sandbox container
- **Default model**: Claude Opus 4.6 as the analyzer's brain

### Key Configuration

- `--max-actions 500`: budget of 500 actions per game
- `--analyzer-interval 10`: analyze every 10 steps
- `--operation-mode online`: supports online/offline/normal modes
- Multi-model support: Claude, GPT 5.2, Gemini 2.5 Pro, or anything on OpenRouter

## Design Philosophy

Alexis Fox articulated two core principles:

**1. The agent should decide what to abstract, not the harness**

- Many ARC-AGI-3 approaches pre-bake abstractions at the framework level (e.g., preprocessing pixels into grids, extracting color patterns)
- RGB Agent takes the opposite approach: feed raw observations to the agent and let it decide what matters
- This means the agent can discover abstraction patterns that human designers didn't anticipate

**2. Solve complex problems with the simplest tool combinations**

- Read (observe state), Grep (search for patterns), Bash (execute actions)
- No dependency on complex specialized frameworks — just Unix-philosophy small tools composed together
- A simpler architecture is easier to debug and iterate on

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
