# Arcgentica Architecture Teardown: How Symbolica Uses Multi-Agent Orchestration to Tackle ARC-AGI-3

> **TL;DR:** Symbolica AI open-sourced Arcgentica — a multi-agent harness for ARC-AGI-3 built on the Agentica SDK. The core idea: an Orchestrator manages the big picture while dynamically spawning Explorer / Theorist / Solver sub-agents. Knowledge transfers across agents through a shared Memory database, and hard action budgets keep resource usage in check. Clean code, solid prompt engineering, and a design worth studying if you build agent systems.

**Repo:** [symbolica-ai/ARC-AGI-3-Agents (symbolica/arcgentica branch)](https://github.com/symbolica-ai/ARC-AGI-3-Agents/tree/symbolica/arcgentica)

---

## Background: What Is ARC-AGI-3?

ARC-AGI-3 is the third-generation general intelligence benchmark from ARC Prize. Unlike its predecessors, AGI-3 is an **interactive visual game** — the agent faces a 64×64 colored grid and must figure out game mechanics through directional keys, spacebar, and mouse clicks across multiple levels. No instructions, no tutorial, just trial and discovery.

This makes it an excellent testbed for agent systems: you need exploration, hypothesis formation, verification, and iteration — all within a finite action budget.

## Overall Architecture

*Architecture diagram derived from source code at [symbolica-ai/ARC-AGI-3-Agents](https://github.com/symbolica-ai/ARC-AGI-3-Agents/tree/symbolica/arcgentica) (MIT License)*

Arcgentica's architecture in one sentence: **The Orchestrator doesn't play the game — it only dispatches agents.**

```
Orchestrator (Claude Opus 4.6 / GPT-5.2)
  │
  ├── spawn_agent("Explorer") + bounded_submit_action(50)
  │     ├── Explores grid, tests actions, records discoveries
  │     └── Writes to Memories
  │
  ├── spawn_agent("Theorist")
  │     ├── Reads Memories, analyzes Explorer reports
  │     └── Forms/validates hypotheses
  │
  └── spawn_agent("Solver") + bounded_submit_action(100)
        ├── Reads Memories for known rules
        └── Executes solving sequence
```

### Key Design Decisions

**1. The Orchestrator Manages, Never Plays**

The Orchestrator doesn't get `submit_action`. It only has `make_bounded_submit_action(limit)` — a factory function. It **must** delegate action authority to sub-agents. This isn't a suggestion; it's an architectural constraint.

```python
# The Orchestrator's scope has no submit_action
# It can only create budgeted versions for sub-agents
orchestrator = await spawn(
    model=self.model.main_agent_model,
    premise=premise(self.model),
    scope={
        "spawn_agent": self.spawn_agent,
        "make_bounded_submit_action": make_bounded_submit_action,
        "memories": memories,
        ...
    },
)
```

**2. Action Budget Is a Hard Constraint**

`bounded_submit_action` is a wrapper with a counter. NOOP and RESET don't count, but ACTION1–ACTION6 decrement on every call. Over-budget? Exception.

```python
class bounded_submit_action:
    def __call__(self, action_name, x=0, y=0):
        if upper != "NOOP" and upper != "RESET":
            if self._used >= self._limit:
                raise ValueError("Action budget exhausted")
            self._used += 1
        return self._inner(action_name, x, y)
```

Why does this matter? When a sub-agent spawns its own sub-sub-agent, they share the same `submit_action` — the budget doesn't reset. This prevents infinite agent nesting from burning through resources.

**3. Shared Memory Is the Knowledge Transfer Backbone**

The `Memories` class isn't just a list. It has:
- `add(summary, details)` — structured writes
- `summaries()` — quick scan of known info
- `query(return_type, question)` — natural language retrieval powered by a dedicated memory agent

```python
# Natural language memory queries
result = await memories.query(str, "What does ACTION3 do?")
failed = await memories.query(list[str], "What strategies have failed?")
```

This means once an Explorer discovers "ACTION5 is the confirm key," the Solver doesn't have to rediscover it — just ask memory.

## Frame: The Agent's View of the World

The `Frame` class is the core interface between the agent and the game. It wraps the 64×64 grid data with a practical inspection toolkit:

| Method | Purpose |
|--------|---------|
| `render(crop=...)` | Text-render the grid, supports cropping |
| `diff(other)` | Find changed regions between two frames |
| `change_summary(other)` | One-line-per-region change overview |
| `find(*colors)` | Locate all pixels of given colors |
| `bounding_box(*colors)` | Bounding box of color regions |
| `color_counts()` | Color frequency stats |

Frames are **immutable** — once created, they can't be modified. This guarantees agents don't accidentally corrupt game state during reasoning.

```python
# Check changes after every action
new_frame = submit_action("ACTION4")  # Move right
print(new_frame.change_summary(old_frame))
# "24 cells changed across 3 region(s):
#   [10,5)-[15,10): 8 cells -- 0→5 ×6, 3→5 ×2 ..."
```

## Prompt Engineering: Not a Prompt, an Operations Manual

The `GAME_REFERENCE` in `prompts.py` isn't a typical system prompt — it's closer to an agent operations manual. Key highlights:

**Coordinates are means, not goals:**
> "Think 'A must reach B' not 'A must reach row 38.' If your hypothesis includes a specific coordinate as part of the goal, it is wrong."

**RESET is a last resort:**
> "RESET throws away ALL the work you did on this attempt... NEVER reset to 'think more carefully' or to 'try a clean approach.'"

**Know when to quit:**
> "If you have tried 2-3 variations of an approach and none produce the expected result, do NOT keep trying. Return to your caller with a clear report."

These aren't platitudes — they directly shape agent behavior and reduce wasted actions.

## Model Configuration

Two presets out of the box:

| Config | Main Agent | Sub-Agent | Context | Reasoning |
|--------|-----------|-----------|---------|-----------|
| OPUS_4_6 | claude-opus-4-6 | claude-opus-4-6 | 200K | high |
| GPT_5_2 | gpt-5.2 | gpt-5.2 | 400K | high |

Managed via a `ModelConfig` dataclass — switching models is a one-liner.

## Visualization and Debugging

Arcgentica ships with a built-in WebSocket real-time visualization system:

- `EventServer` — WebSocket server + JSONL logging
- `WsLogger` — Pushes agent lifecycle events to the frontend
- `UsageTracker` — Token usage accounting across all agents
- Single-file HTML frontend, zero build step
- Supports session replay (`replay.py`)

```bash
# Enable visualization
VISUALIZE=1 uv run main.py --agent=arcgentica --game=ls20

# Replay a recorded session
uv run python -m agents.templates.agentica.logging.replay session.jsonl --speed 4
```

## Performance in Practice

Based on Symbolica's published records, they've completed full runs on multiple ARC-AGI-3 games: ls20, vc33, ft09, and more. Full replay logs are provided. They're actively expanding to 25+ games (ar25, bp35, cd82, cn04, etc.), demonstrating reasonable generalization of the architecture.

## Takeaways for Agent Builders

1. **Orchestrators shouldn't do the work.** Separate decision-making from execution. Enforce this with architecture (withhold `submit_action`), not just prompts.

2. **Shared memory beats message passing.** Sub-agents don't need direct communication — everyone writes to memory, everyone reads from memory. Simple, decoupled, scalable.

3. **Give agents a budget, then enforce it hard.** `bounded_submit_action` is elegant: counter, shared state, exception on overrun. A hundred times more reliable than "please use actions wisely."

4. **Immutable data structures reduce bugs.** Once a Frame is created, it can't change. Need to compare two states? Use diff. No worrying about mutation side effects.

5. **Prompts are part of the design document.** Arcgentica's prompts weren't added as an afterthought — they were co-designed with the code. Every behavioral rule maps to an architectural enforcement.

---

**Source:** [symbolica-ai/ARC-AGI-3-Agents](https://github.com/symbolica-ai/ARC-AGI-3-Agents/tree/symbolica/arcgentica) — MIT License

🦞
