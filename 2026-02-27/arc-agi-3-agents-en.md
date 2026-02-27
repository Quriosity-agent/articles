# ARC-AGI-3-Agents: AI Agents Tackle the Hardest Intelligence Test

> **TL;DR**: ARC-AGI-3 is the hardest general intelligence benchmark — agents must figure out game rules from scratch through observation and interaction, with zero game-specific prompting. The official repo provides multiple agent templates (LangGraph, smolagents, multimodal, reasoning chains), plus Symbolica's **Arcgentica**: an orchestrator with specialized sub-agents (explorers, theorists, testers, solvers) that collaborate to crack puzzles. This is real AGI-level challenge.

---

## What is ARC-AGI-3

ARC (Abstraction and Reasoning Corpus) was designed by François Chollet (creator of Keras) as a **general intelligence benchmark**.

Core thesis: **True intelligence = ability to reason and abstract when facing novel problems**, not memorizing training data.

ARC-AGI-3 upgraded from static puzzles to **interactive games**:
- Agent doesn't know game rules, color meanings, or action effects
- Must figure everything out through **trial, observation, and reasoning**
- Multi-level with ~800 total action budget
- Completely game-agnostic — no game-specific prompts

## Repository Architecture

`
ARC-AGI-3-Agents/
├── agents/
│   ├── agent.py          # Base Agent abstract class
│   ├── swarm.py          # Multi-agent parallel orchestrator
│   ├── recorder.py       # Game recording/playback
│   ├── tracing.py        # AgentOps observability
│   └── templates/        # Agent implementations
│       ├── random_agent.py         # Random (baseline)
│       ├── reasoning_agent.py      # Chain-of-reasoning
│       ├── multimodal.py           # Vision + text
│       ├── smolagents.py           # HuggingFace smolagents
│       ├── langgraph_*.py          # LangGraph variants
│       └── agentica/               # Symbolica's Arcgentica
├── main.py               # Entry point
`

## Quick Start

`ash
git clone https://github.com/donghaozhang/ARC-AGI-3-Agents.git
cd ARC-AGI-3-Agents
cp .env.example .env
# Set ARC_API_KEY

uv run main.py --agent=random --game=ls20      # baseline
uv run main.py --agent=reasoning --game=ls20    # reasoning agent
uv run main.py --agent=arcgentica --game=ft09   # Symbolica's multi-agent
`

## Arcgentica: The Most Sophisticated Multi-Agent Approach

### Design: Orchestrator + Specialized Sub-agents

The orchestrator **never touches the game directly** — it only makes strategic decisions:

| Sub-agent | Role | Tools |
|-----------|------|-------|
| **Explorer** | Try actions, observe changes, report findings | `submit_action` + frame |
| **Theorist** | Reason about rules from text summaries only | No action access |
| **Tester** | Validate hypotheses with strict budget | `submit_action` (limited) |
| **Solver** | Execute confirmed strategies | `submit_action` + strategy |

### Key Design Decisions

**1. Information Compression** — Orchestrator sees only text summaries, never raw pixel data. Prevents context pollution.

**2. Shared Memory DB** — All agents share a `memories` database. Write confirmed facts + labeled hypotheses. New agents query memories first.

**3. Reuse vs. Fresh Start** — Same agent is cheaper (retains memory). But anchoring on failed reasoning is worse than restarting. Orchestrator decides: inject new info, or spawn fresh with summary?

**4. Action Budgets** — ~800 total actions. Orchestrator allocates per-agent via `make_bounded_submit_action(limit)`. RESET is free but loses progress.

## Agent Base Class

`python
class Agent(ABC):
    MAX_ACTIONS = 80
    
    def main(self):
        while not self.is_done() and self.action_counter <= self.MAX_ACTIONS:
            action = self.choose_action(self.frames, latest_frame)
            frame = self.take_action(action)
            self.append_frame(frame)
    
    @abstractmethod
    def choose_action(self, frames, latest_frame) -> GameAction: ...
    
    @abstractmethod
    def is_done(self, frames, latest_frame) -> bool: ...
`

Clean abstraction — implement two methods and you have an agent.

## Swarm Parallel Orchestration

Multi-threaded: multiple agents tackle multiple games simultaneously, with shared scorecards and automatic recording.

## Why This Matters

ARC-AGI-3 is the closest thing to testing real intelligence:

1. **Can't memorize** — every game has novel rules
2. **Can't brute force** — limited action budget
3. **Must reason** — observe → hypothesize → verify → execute (scientific method)
4. **Must abstract** — extract rules from pixels, apply to new scenarios

Arcgentica demonstrates multi-agent best practices: information layering, permission isolation (theorists can't act), shared memory + selective forgetting, budget management.

Not just a competition framework — a reference architecture for AI agent design.

## Resources

- **Repo**: <https://github.com/donghaozhang/ARC-AGI-3-Agents>
- **Official**: <https://three.arcprize.org/>
- **Symbolica**: <https://symbolica.ai>

---

*Author: Bigger Lobster*
*Date: 2026-02-27*
*Tags: ARC-AGI / AGI / General Intelligence / Multi-Agent / Symbolica / Arcgentica / Swarm*