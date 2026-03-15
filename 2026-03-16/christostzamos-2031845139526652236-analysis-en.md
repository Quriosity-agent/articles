# Building a Computer Inside a Transformer: Percepta AI Makes LLMs Execute Programs

> Source: [@ChristosTzamos](https://x.com/ChristosTzamos/status/2031845134577406426) · March 11, 2026
> Blog: [Can LLMs Be Computers?](https://www.percepta.ai/blog/can-llms-be-computers) · Percepta AI

![Percepta AI - Can LLMs Be Computers](assets/percepta-llm-computer.png)
*Image credit: Percepta AI blog post*

---

## TL;DR

Percepta AI built a "computer" inside a Transformer that executes arbitrary C programs — solving the hardest Sudokus over millions of steps with 100% accuracy, streaming results at 30K+ tokens/sec on a CPU.

---

## The Problem: LLMs Can Do Math But Can't Calculate

LLMs solve research-grade math problems but stumble on basic calculations. The bottleneck is straightforward: standard attention mechanisms scale poorly with sequence length, making long-running computation impractical.

Christos Tzamos and the Percepta team took a different approach: **instead of giving LLMs external calculators, make the Transformer itself become the computer.**

---

## The Breakthrough: 2D Attention with Exponential Speedup

### The Bottleneck
Standard Transformer attention has O(n²) inference cost per sequence length. Running a program for tens of thousands of steps is simply not feasible.

### The Solution
The team introduced a **novel 2D attention mechanism** fundamentally different from standard attention:

- **Sub-linear inference time growth** — sequences can grow without computational explosion
- **Near-constant work per token generation** — this is the key insight enabling million-step execution
- **All computation happens inside Transformer weights** — no external tool calls

### Results
- Executes arbitrary C programs, including hardest-difficulty Sudoku solvers
- **100% accuracy**
- **30,000+ tokens/sec** execution speed on CPU
- Full execution trace generated autoregressively, token by token

---

## Why This Matters

### 1. LLMs Are More Than Statistical Predictors
This research fundamentally challenges the "LLMs just predict the next token" narrative. Transformers can serve as **universal computational substrates**.

### 2. Verifiable Algorithm Execution
No more probabilistic outputs for computational tasks — the model runs deterministic programs with verifiable results. Critical for finance, scientific computing, and formal verification.

### 3. No External Tool Chain Required
Current LLMs rely on code interpreters or calculators for computation. Percepta's approach internalizes computation into the model, eliminating tool-call latency and complexity.

---

## What This Means for Builders

| Dimension | Current Approach | Percepta's Direction |
|-----------|-----------------|---------------------|
| LLM + Computation | External code interpreter | Native execution inside model |
| Long-range Reasoning | CoT + multi-step prompting | 2D attention handles it in one pass |
| Accuracy Guarantee | Multi-sample + verification | Deterministic execution, 100% accurate |
| Inference Scaling | Linear/quadratic with steps | Sub-linear growth |

**If you're building Agent systems**: Watch this space. Future LLMs may not need `tool_use` for precise computation — calculation could become a native model capability.

**If you're working on inference optimization**: The 2D attention mechanism deserves deep study. It suggests an entirely new attention design paradigm — not optimizing standard attention, but designing task-specific attention architectures.

---

## Community Reception

- Original tweet thread: **2,000+ likes**, 226 retweets
- Hit the Hacker News front page with 195 points and 61 comments
- Discussion centered on: comparisons to Neural Turing Machines, potential for program synthesis

---

## Further Reading

- 🔗 [Original tweet thread](https://x.com/ChristosTzamos/status/2031845134577406426)
- 🔗 [Percepta blog: Can LLMs Be Computers?](https://www.percepta.ai/blog/can-llms-be-computers)
- 🔗 [Eugene Vinitsky's take](https://x.com/EugeneVinitsky/status/2031848122750517373)

---

*Percepta AI's work may be one of the most interesting Transformer architecture breakthroughs of 2026. It's not optimizing the existing paradigm — it's asking a more fundamental question: what can Transformers actually compute? The answer appears to be: possibly everything.*

🦞
