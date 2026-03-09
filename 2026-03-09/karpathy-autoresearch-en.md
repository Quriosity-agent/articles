# Karpathy's autoresearch: AI Agents Doing AI Research Autonomously

> "One day, frontier AI research used to be done by meat computers in between eating, sleeping, having other fun… That era is long gone." — Andrej Karpathy, March 2026

## What Is It?

[autoresearch](https://github.com/karpathy/autoresearch) is an open-source project released by Andrej Karpathy in March 2026. The concept is deceptively simple: **give an AI agent a real LLM training setup and let it experiment autonomously**.

The agent modifies training code, trains for 5 minutes, checks if the result improved, keeps or discards the change, and repeats. You go to sleep and wake up to a log of experiments and (hopefully) a better model.

In a [tweet announcing the project](https://x.com/karpathy/status/2029701092347630069), Karpathy shared that his agent completed 110 changes over 12 hours, bringing validation loss from 0.862415 down to 0.858039. He noted he'd spent more time optimizing the "meta-setup" (the agent workflow) than the training code itself — perhaps a preview of how AI research will work going forward.

## Architecture: Three Files, That's It

The project is deliberately minimal. Only three files matter:

- **`prepare.py`** — Fixed data preparation script. Downloads training data, trains a BPE tokenizer, provides dataloader and evaluation utilities. The agent never touches this file.
- **`train.py`** — The single file the agent edits. Contains the full GPT model definition, optimizer (Muon + AdamW), and training loop. Architecture, hyperparameters, batch size, optimizer — everything is fair game.
- **`program.md`** — Instructions for the agent. A lightweight "skill" file that tells the agent how to run experiments. This file is edited by the human.

The elegant insight: **you're not writing Python to do research anymore — you're writing Markdown that instructs an AI to do research**. As Karpathy puts it: "You are programming the program."

## The Research Loop: 5 Minutes Per Experiment

Here's how the autonomous research cycle works:

- **Step 1:** Agent reads `program.md` to understand goals and constraints
- **Step 2:** Agent analyzes current `train.py` and forms an improvement hypothesis
- **Step 3:** Agent modifies `train.py` (architecture changes, hyperparameter tuning, optimizer swaps, etc.)
- **Step 4:** Training runs for a fixed 5-minute wall-clock budget
- **Step 5:** Agent checks `val_bpb` (validation bits per byte) against previous best
- **Step 6:** If improved, keep the change; if regressed, revert
- **Step 7:** Log the experiment, return to Step 2

Key design decisions:

- **Fixed 5-minute time budget** — Regardless of what changes (model size, batch size, architecture), training time is constant. This makes experiments directly comparable. Expect ~12 experiments/hour, ~100 experiments overnight.
- **Single metric: val_bpb** — Bits per byte is vocabulary-size-independent, so even architectural changes that affect tokenization are fairly compared.
- **Single GPU, self-contained** — No distributed training, no complex configs. One GPU, one file, one metric.

## Getting Started

```bash
# Install uv package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Download data and train tokenizer (one-time, ~2 min)
uv run prepare.py

# Test with a manual training run (~5 min)
uv run train.py

# Then spin up your AI agent (Claude Code, Codex, etc.) and prompt:
# "Hi have a look at program.md and let's kick off a new experiment!"
```

Requirements: Single NVIDIA GPU (tested on H100), Python 3.10+, uv.

Community forks for macOS:
- [miolini/autoresearch-macos](https://github.com/miolini/autoresearch-macos)
- [trevin-creator/autoresearch-mlx](https://github.com/trevin-creator/autoresearch-mlx)

## Comparison with Other Automated Research Tools

autoresearch occupies a unique niche in the growing ecosystem of AI-powered research tools:

**ChatGPT Deep Research / Gemini Deep Research / Perplexity**
- Focus on **information retrieval and synthesis** — gathering papers, summarizing literature, writing reviews
- Essentially advanced search engines + summarizers
- They **don't** modify code, run experiments, or iterate on models

**Sakana AI's AI Scientist**
- Automatically generates research ideas, writes code, runs experiments, and drafts papers
- Broader scope (idea to paper), but weaker quality control per experiment
- autoresearch is more focused: one job (optimize training code), done deeply

**FARS (Fully Autonomous Research Systems)**
- Similar autonomous experimentation philosophy
- Typically more complex, involving multi-agent collaboration, paper writing, etc.
- autoresearch is intentionally simple — three files, one agent

**What makes autoresearch unique:**
- **True closed-loop experimentation** — Not just analysis and suggestions, but actually editing code, running training, and evaluating results
- **Radical simplicity** — Three files, zero config, plug and play
- **Human-auditable** — All changes happen in one file; diffs are easy to review
- **"Programming the program" paradigm** — You don't write research code; you write instructions that guide AI to write research code

## Why This Matters

Karpathy opens the README with a sci-fi vignette: a future where AI research is entirely conducted by autonomous agent swarms, the codebase has evolved into a self-modifying binary beyond human comprehension, and autoresearch is "the story of how it all began."

Setting aside the narrative flourish, this project demonstrates a genuine paradigm shift:

- The researcher's role moves from "writing code and running experiments" to "designing agent workflows"
- Experimental throughput is no longer bounded by human energy and time
- Small teams or individuals can have AI exploring the hypothesis space 24/7

This may be one of the most significant AI trends of 2026: **AI research itself is being automated by AI**.

---

*Written March 9, 2026*

🦞
