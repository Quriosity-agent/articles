# MiniMax M3 Deep Dive: The Real Contest Is Not “Another Big Model,” but a Unified Agent Substrate for Coding, Long Context, and Multimodality

> **TL;DR:** The important part of MiniMax M3 is not just benchmark scores. It is a clearer product thesis: the next frontier model needs **strong coding / agent capability, million-token context, native multimodality, and computer use** at the same time. M3 uses MSA (MiniMax Sparse Attention) to turn 1M context into a scalable architectural capability, then packages it through MiniMax Code, Token Plan, and APIs as everyday agent infrastructure for developers.

- **Source:** [MiniMax M3: Frontier Coding, 1M Context, Native Multimodality — All in One Model](https://www.minimax.io/blog/minimax-m3)
- **Published:** 2026-05-31
- **Tags:** MiniMax M3 / Frontier Model / Coding Agent / 1M Context / Sparse Attention / Multimodal / MiniMax Code / Agent Harness

![MiniMax M3 benchmark overview](imgs/minimax-m3-frontier-model/01-minimax-m3-benchmark-overview.jpg)

## 1. M3’s core narrative: frontier capability is converging into a three-part bundle

MiniMax does not present M3 as a single-axis upgrade. It frames the model around a broader claim: the bar for frontier models is shifting from “strong language ability” to a three-part bundle — **specialized coding / agent capability, ultra-long context, and native multimodality**.

The official blog is explicit. M3 reaches frontier-level results across coding and agent benchmarks such as SWE-Bench Pro, Terminal-Bench 2.1, SWE-fficiency, KernelBench Hard, and MCP Atlas. It supports up to 1M tokens of context. It is trained from the start as a mixed-modality model, supporting image and video input as well as desktop computer use.

That means the selling point is not simply “this model can write code.” The stronger claim is: “this model can sit inside a long thread, understand papers, code, logs, figures, file systems, and tool feedback, then keep pushing an engineering task forward.” That is why the blog spends so much space on real tasks: reproducing a paper, optimizing an FP8 GEMM kernel, autonomously post-training base models, and running multi-agent workflows through MiniMax Code.

## 2. MSA: making million-token context an architectural capability, not just a resource budget

![MSA architecture](imgs/minimax-m3-frontier-model/02-m3-msa-arch.png)

The key architectural term behind M3 is **MSA (MiniMax Sparse Attention)**. MiniMax’s explanation is straightforward: complex agent tasks require context scaling, but full attention has a fundamental bottleneck — quadratic growth in compute.

MSA follows the sparse-attention route. Before attention computation, it performs more precise selection over KV blocks so the model does not need to attend densely to every token. MiniMax compares MSA with sparse approaches such as DSA and MoBA, arguing that MSA partitions KV blocks more accurately and therefore improves effective context coverage.

The implementation detail matters. The blog says MiniMax uses a **“KV outer gather Q”** operator organization: KV blocks are the outer loop, queries that hit each block are gathered, each block is read only once, and memory access remains as contiguous as possible. Under M3’s head configuration, MiniMax says this gives better arithmetic intensity than common methods and runs more than 4× faster than open-source Flash-Sparse-Attention and flash-moba.

The result has two layers:

1. **Capability:** 1M context is not only a marketing number. It can hold papers, code, experiment logs, and tool-call histories in one long structured thread.
2. **Cost:** At a 1M context length, M3’s per-token compute is one-twentieth of the previous-generation model; prefill is accelerated by more than 9×, and decoding by more than 15×.

For agent products, this is crucial. Long context is not useful merely because it can “stuff more documents.” It is useful because it reduces the friction of repeated summarization, state loss, file rereading, and task-memory reconstruction.

## 3. Coding capability: the target is long-term collaboration, not one-shot code generation

MiniMax lists the following coding / agent scores:

![MiniMax M3 detailed benchmark table](imgs/minimax-m3-frontier-model/08-img_v3_02128_b7726cd8-879a-4b7a-a9da-db4395ea597g-1780272508686.jpg)

| Benchmark | Official MiniMax M3 score |
|---|---:|
| SWE-Bench Pro | 59.0% |
| Terminal-Bench 2.1 | 66.0% |
| SWE-fficiency | 34.8% |
| KernelBench Hard | 28.8% |
| MCP Atlas | 74.2% |

A key detail is that MiniMax does not only emphasize benchmark results. It emphasizes the gap between current coding benchmarks and real developer experience. Real software work is not a one-shot prompt. It is a continuous session: users clarify requirements, models discuss solutions, tools fail, feedback arrives, and context switches happen mid-stream.

To reduce that gap, M3 training and evaluation include an **interactive user simulator framework**. The simulator aims to mimic real developer behavior during collaboration: requirement elaboration, solution discussion, feedback-based correction, continuous task switching, and complex project iteration. In other words, MiniMax is pushing the coding model from “code generator” toward “collaborative engineering agent.”

For product builders, this matters more than a single leaderboard. A useful coding agent must be stable on questions like:

- when to ask and when to act;
- how to preserve goal consistency after multiple feedback rounds;
- how to digest dense structured context from tool calls;
- how to convert failure into the next plan instead of ending the task;
- how to survive user interruptions, requirement changes, and task switches.

M3’s story is clearly moving in that direction.

## 4. Real tasks: three cases reveal more than the leaderboard

### 4.1 Reproducing an ICLR 2025 Outstanding Paper: a joint test of long context, multimodality, and coding

![Paper reproduction](imgs/minimax-m3-frontier-model/03-m3-paper-repro.png)

MiniMax asked M3 to reproduce the ICLR 2025 Outstanding Paper **Learning Dynamics of LLM Finetuning**. According to the blog, M3 ran autonomously for nearly 12 hours, produced 18 commits and 23 experimental figures, and completed the core experiments. It reproduced the prediction-probability trend during SFT, observed the squeezing effect in the DPO experiments, and verified the paper’s Extend mitigation method.

The difficulty here is not “understanding a code snippet.” The model must jointly process formulas, figures, code, experiment logs, and runtime feedback. Multimodality helps with figures and formulas. Long context keeps the paper and logs in one thread. Coding / agent capability keeps execution moving.

### 4.2 Hopper FP8 GEMM: from a non-running Triton skeleton to 71.3% peak utilization

![CUDA performance optimization](imgs/minimax-m3-frontier-model/04-m3-cuda-perf.gif)

The second case is more engineering-heavy: optimize an FP8 GEMM kernel on NVIDIA Hopper GPUs. MiniMax says the model started with only a task description, a benchmark script, and a Triton skeleton that could not run directly, with no high-performance reference implementation to copy.

Over roughly 24 hours, M3 completed 147 benchmark submissions and 1,959 tool calls. It moved from baseline implementation to autotune configuration, bottleneck diagnosis, CUDA Graph integration, persistent kernel rewriting, and host-side scheduling optimization. The final result raised Hopper FP8 peak utilization from 7.6% to 71.3%, a 9.4× speedup.

The signal is that high-value coding agents are not just business-code writers. They can keep iterating inside a dense feedback loop. MiniMax also notes that, except for Opus 4.7 and M3, most models stopped making progress and exited within the first 30 submissions, while M3’s best solution appeared on submission 145. “Willingness to continue exploring” and “ability to use long tool history” become real capabilities.

### 4.3 PostTrainBench: pushing agents into research automation

![PostTrainBench](imgs/minimax-m3-frontier-model/05-m3-posttrain-bench.gif)

The third case is PostTrainBench. M3 receives four base models that have only completed pretraining and do not yet have downstream capabilities. Within 12 hours, it must autonomously perform data synthesis, training, evaluation, and iteration. The goal is to give those base models basic capabilities across AIME2025, BFCL, GPQA Main, GSM8K, HumanEval, and related tasks.

MiniMax reports a score of 0.37 for M3, slightly below Opus 4.7 at 0.42 and GPT-5.5 at 0.39, but clearly ahead of the other models. This task is closer to an AI researcher workflow: there is no single clean reward, and the agent must decide what data to synthesize, which training strategy to use, and how to adjust the next round based on evaluation.

This is the key to MiniMax’s positioning of M3 as an agent substrate. Coding is the entry point; research automation is the longer-term direction.

## 5. MiniMax Code: model capability has to be productized into a harness

M3 is released alongside an updated **MiniMax Code**. MiniMax describes it as an agent product designed specifically for M3 and trained together with M3, so it can fully use M3’s long-context, coding / agent, and native multimodal capabilities.

The most interesting feature is **Agent Team**. It can break long-horizon complex tasks into multi-stage, concurrent, dynamically adjustable workflows, then have a cluster of agents execute them collaboratively. MiniMax also describes a **Producer + Verifier adversarial harness loop**: some agents produce, others verify and correct, allowing the system to reflect and self-correct during execution.

This resembles Claude Code’s recent Dynamic Workflows direction, but MiniMax frames the difference as follows: Claude Code emphasizes more fixed orchestration based on JS code, while MiniMax Code emphasizes “deep reflection and continuous error correction,” with users able to step in at any time to add requirements or correct direction.

For builders, the lesson is obvious: model capability must land inside a harness. Even a strong 1M-context model will struggle to become a reliable product without task decomposition, concurrent scheduling, verifiers, permission controls, logs, and recovery mechanisms.

## 6. Token Plan and API: making frontier models an everyday consumable

![MiniMax token plan](imgs/minimax-m3-frontier-model/06-m3-token-plan-2.png)

M3’s commercial packaging is aggressive. The updated MiniMax Token Plan has three tiers:

| Plan | Price | M3 token quota |
|---|---:|---:|
| Plus | $20 / month | ~1.7B tokens / month |
| Max | $50 / month | ~5.1B tokens / month |
| Ultra | $120 / month | ~9.8B tokens / month |

MiniMax emphasizes that text, image, speech, and music share the same usage pool. The strategy is clear: move frontier models from “expensive API calls” into everyday developer tooling, where long threads, many trials, and concurrent agent runs become economically feasible.

At the API layer, pricing depends on input length. Calls with ≤512K input tokens use the standard rate; calls above 512K use a higher long-context rate for workloads such as ultra-long document parsing and whole-repository code understanding. M3 also supports thinking on/off. Thinking mode suits complex reasoning, agentic tasks, and long-horizon collaboration; non-thinking mode is faster and better for latency-sensitive chat or code completion. Both modes share the same pricing and can be switched per request.

![MiniMax M3 API pricing](imgs/minimax-m3-frontier-model/07-20260601-101138-1780280144441.jpeg)

The API also supports standard and priority service tiers. Priority is intended for high-concurrency or SLA-sensitive use cases. It is currently enabled through sales support, with broader availability expected in the following days.

## 7. What to be cautious about

The release post is strong, but it is worth separating three kinds of signal:

1. **Official benchmark scores:** useful, but many evaluations use internal infrastructure, internal benchmarks, or custom scaffolding. Third-party replication will matter.
2. **Open-source promise:** MiniMax says it will release the technical report and open-source the corresponding model weights within 10 days. Community adoption will depend on weights, license, inference cost, and serving tooling.
3. **Agent product stability:** long autonomous demos are impressive, but production use still requires permissions, sandboxing, cost limits, failure recovery, auditability, and user control.

In short: M3 gives a very clear direction, but whether it becomes developer infrastructure depends on the maturity of the open weights, MiniMax Code, and the API stack.

## 8. My read: M3 is MiniMax’s shift from “model company” toward “agent infrastructure company”

The most important part of M3 is not that it approaches or beats a specific model on a specific benchmark. It is that MiniMax is now presenting model architecture, sparse attention, developer subscription, APIs, desktop agents, and multi-agent harnesses as one integrated system.

If the previous model race was about “who chats more intelligently,” the M3-style race is about:

- who can keep state across long tasks;
- who can self-correct through tool feedback;
- who can put multimodality, coding, and computer use into one execution loop;
- who can make real agent trial-and-error affordable with lower token economics;
- who can turn open-weight models into deployable, auditable, scalable engineering systems.

That is why M3 is worth watching. It is not just another model release. It is a bet that the future frontier-model contest happens at the combined layer of **agent runtime + long context + multimodal execution + developer economics**. For anyone building agent-native tools such as QCut or OpenClaw, this direction is especially relevant.