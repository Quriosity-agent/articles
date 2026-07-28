---
title: "Kimi K3 Open-Weight Release Audit: After 1.56TB of Weights, the Real Barrier Is Agent State Infrastructure"
date: 2026-07-27
source: "https://www.kimi.com/blog/kimi-k3"
canonical: "https://www.kimi.com/blog/kimi-k3"
related_sources:
  - "https://github.com/MoonshotAI/Kimi-K3"
  - "https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf"
  - "https://huggingface.co/moonshotai/Kimi-K3"
  - "https://platform.kimi.ai/docs/guide/kimi-k3-quickstart"
  - "https://recipes.vllm.ai/moonshotai/Kimi-K3"
  - "https://docs.sglang.io/cookbook/autoregressive/Moonshotai/Kimi-K3"
tags:
  - Kimi K3
  - Moonshot AI
  - Open Weight
  - Agent Infrastructure
  - Long Context
  - Kimi Delta Attention
  - Mixture of Experts
  - Model Serving
---

# Kimi K3 Open-Weight Release Audit: After 1.56TB of Weights, the Real Barrier Is Agent State Infrastructure

> **TL;DR:** Moonshot AI delivered Kimi K3's full weights and technical report on July 27, 2026. The Hugging Face repository contains 96 safetensors shards and reports about 1.56TB of storage. K3 has 2.78T total parameters, 104.2B activated parameters, a one-million-token context window, and native vision. The most consequential disclosure is not only KDA, Attention Residuals, or 16-of-896 expert routing. It is the state system built around million-token agent training and serving: resumable partial rollouts, external KV cache, pausable and forkable microVMs, joint KDA/MLA prefix caching, and session-affinity scheduling. The cost is equally explicit. Moonshot recommends supernodes with at least 64 accelerators for production, while the vLLM reference starts at eight GB300s. The custom Kimi K3 License is not Apache or MIT. K3 is genuinely open-weight, but it is data-center-scale open infrastructure rather than a workstation model.

- **Launch blog:** [Kimi K3: Open Frontier Intelligence](https://www.kimi.com/blog/kimi-k3)
- **Technical report:** [Kimi K3 Technical Report](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)
- **Repository:** [MoonshotAI/Kimi-K3](https://github.com/MoonshotAI/Kimi-K3)
- **Full weights:** [moonshotai/Kimi-K3](https://huggingface.co/moonshotai/Kimi-K3)
- **API guide:** [Kimi K3 Quickstart](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart)
- **Weights/report release:** 2026-07-27
- **Accessed:** 2026-07-28

## The one-sentence take

**The Kimi K3 release does not make a 2.8T model locally accessible. It makes the weights, architecture, long-horizon RL state management, and production serving design of a 3T-class multimodal agent model externally auditable at the same time.**

At the July 17 launch, K3 was still a collection of APIs, product demos, and Moonshot-reported benchmarks. The company promised full weights and a technical report by July 27. Both have now arrived, so the evaluation question changes from “will it really open?” to “which layers are open, and who can actually run them?”

## 1. What was actually released

The Hugging Face model repository now contains:

- 96 `safetensors` weight shards;
- model, tokenizer, and generation configurations;
- custom Transformers implementations for Kimi K3 and Kimi Linear;
- image-processing and multimodal preprocessing code;
- a full model card and evaluation notes;
- the Kimi K3 License.

At access time, the Hugging Face API reported roughly **1.561TB** of repository storage and **2,779,931,837,184** parameters. That storage figure already benefits from the native MXFP4 expert-weight format. Storing 2.78T parameters in BF16 would require substantially more space.

The GitHub repository primarily holds the README, license, report, and assets. It is not a complete training-code release. The public layer is therefore best described as **full model weights, the remote code required for inference, and a technical report**. Pretraining data, the full training pipeline, and a turnkey reproduction stack for 2.8T training are not public.

That makes K3 open-weight, not a fully open-source project in which every training ingredient is available.

## 2. The architecture scales three information paths at once

The report organizes K3 around three axes:

| Axis | Mechanism | Purpose |
|---|---|---|
| Sequence / token | Repeating 3 KDA layers + 1 Gated MLA layer | Use recurrent linear attention for long sequences while periodically preserving global attention |
| Depth / layer | Attention Residuals | Let a layer selectively retrieve earlier blocks instead of compressing all depth history into one residual stream |
| Channel / expert | Stable LatentMoE | Expand the expert pool in a lower-dimensional latent space, reducing communication and weight traffic when 16 experts are active |

![Kimi K3 architecture with KDA, Gated MLA, Attention Residuals, Stable LatentMoE, and MoonViT-V2](imgs/kimi-k3-open-weight-release-audit/01-architecture.jpg)

*Kimi K3 architecture. Each cycle contains three KDA layers and one Gated MLA layer. AttnRes retrieves across depth, Stable LatentMoE performs sparse channel mixing, and MoonViT-V2 provides the native vision path. Source: Kimi K3 Technical Report.*

The concrete model specification is:

- 93 layers: 69 KDA and 24 Gated MLA;
- 2.78T total parameters and about 104.2B activated per token;
- 896 routed experts, with 16 selected per token;
- two additional shared experts;
- hidden size 7,168 and 96 attention heads;
- a 401M-parameter, 27-layer MoonViT-V2;
- a maximum context of 1,048,576 tokens.

“Only 16 of 896 experts are active” does not mean only 104B weights need to be hosted. Compute is sparse, but all 2.78T expert weights still have to live across the cluster. Routing, all-to-all communication, and load balancing also remain active costs. That is why a 1.56TB compressed release is still a cluster problem.

## 3. A 2.5x scaling-efficiency gain is not 2.5x faster inference

The report says KDA, AttnRes, Stable LatentMoE, data, and training recipes together produce an approximately 2.5x improvement in overall scaling efficiency over Kimi K2. The number comes from scaling-law fits on held-out out-of-distribution validation loss: K3 needs fewer training FLOPs to reach the same fitted loss.

![Kimi K2 and Kimi K3 scaling-law curves and architecture comparison](imgs/kimi-k3-open-weight-release-audit/02-scaling-and-specs.jpg)

*K2/K3 scaling-law fits and architecture comparison. The 2.5x figure describes training scaling efficiency, not decoding throughput or end-to-end agent speed. Source: Kimi K3 Technical Report.*

It does not mean:

- K3 generates tokens 2.5x faster than K2;
- API costs automatically fall by 2.5x;
- K3 needs only 40% of K2's hardware;
- every benchmark improves by 2.5x.

The report also does not disclose the total pretraining-token count, total FLOPs, GPU count, or full training cost. It does disclose the data categories: Web Text, Code, Mathematics, Knowledge, and a large vision corpus. Visual data spans captions, interleaved image-text documents, OCR, perception, video, and code paired with rendered SVG, 3D, webpage, game, and CAD outputs.

## 4. Native multimodality and 1M context are curricula, not config flags

K3 jointly optimizes language and vision from the beginning of training rather than attaching a vision encoder to a finished language model. Image and text tokens participate in one next-token objective, with MoonViT-V2 features projected into the shared backbone.

Long context is also more than setting `max_position_embeddings` to one million. The report describes a four-stage curriculum:

1. pretraining begins at 8K;
2. it extends to 64K;
3. cooldown training moves to 256K;
4. the final stage reaches 1M.

KDA uses NoPE, encoding position implicitly through recurrent gates and decay, so it does not require RoPE rescaling. That does not make million-token retrieval automatic. Moonshot also synthesizes multimodal long-context tasks with evidence scattered across the full sequence, forcing the model to use distant information instead of relying on local patterns.

More importantly, the report treats one million tokens as agent-trajectory capacity. Reasoning, tool calls, observations, code, screenshots, and environment state accumulate together. Context is a runtime working-memory budget, not merely a document-ingestion number.

## 5. Three domains times three effort levels, distilled back into one model

K3 post-training has three stages: supervised fine-tuning, domain reinforcement learning, and Multi-Teacher On-Policy Distillation (MOPD).

RL is divided into three broad domains:

- general tasks: knowledge, vision, reasoning, faithfulness, search, and knowledge work;
- general agents: long-horizon assistance, deep research, and writing;
- coding agents: software engineering, coding practice, GPU kernels, and web development.

Each domain is trained at `low`, `high`, and `max` reasoning effort, producing nine expert policies. MOPD then consolidates those domain and budget specializations into one model.

This explains why the API now exposes all three effort levels. At launch, only `max` was available. After the weight release, `low`, `high`, and `max` are supported, with `max` remaining the default. These modes are not merely truncated chains of thought; token-budget constraints and curricula were part of RL.

Quantization-aware training begins at SFT. The MoE expert weights that dominate parameter memory use MXFP4, while activations use MXFP8. Attention, latent projections, shared experts, routers, and other non-expert components remain at higher precision. The official checkpoint is therefore not a community post-hoc 4-bit conversion. Its deployment format participated in post-training.

## 6. Million-token agent RL requires pausing both model and environment

Ordinary batch RL struggles with long-horizon agents. One trajectory may contain hundreds or thousands of tool calls and delay the whole batch. Pausing it across optimization iterations then requires both the model cache and the tool environment to survive.

K3 addresses this with a state-preservation stack:

- partial rollout pauses tail trajectories and resumes them in later iterations;
- active KV remains on GPU, while evicted reusable prefixes move to an external CPU DRAM pool;
- model and optimizer states are offloaded to NVMe between phases to free memory for rollout cache;
- the Firecracker-based AgentENV microVM runtime supports pause/resume, fork, and snapshot;
- incremental checkpoints store only dirty memory pages, with reported minimum checkpoint and resume latencies of 133ms and 49ms;
- paused sandboxes consume no CPU or memory while the agent waits for inference.

The report says K3 training and evaluation created **51,219,741 sandboxes** across **1,505,678 images**. That figure captures the change in agent-model training. The job is no longer only to optimize a loss; it is to operate a large fleet of recoverable, isolated computational environments.

## 7. Serving 1M context is about avoiding repeated prefill

K3 maintains two different state types. MLA KV cache grows with sequence length, while KDA keeps a fixed recurrent state per request. A prefix hit is valid only if both states can be restored at the same boundary.

The report therefore decouples coarse physical pages from fine prefix hashes. A 6,144-token physical block can contain twelve 512-token hash blocks, while KDA checkpoints are persisted at selected hash boundaries. On a hit at token 2,560, the server restores KDA state, copy-on-writes the partial MLA page, and resumes without recomputing the first 2,560 tokens.

![KDA-aware prefix caching with 512-token hash blocks inside a 6144-token physical block](imgs/kimi-k3-open-weight-release-audit/03-kda-prefix-cache.jpg)

*KDA-aware prefix caching. KDA checkpoints and MLA KV must hit at the same boundary before a long prefix can be reused. Source: Kimi K3 Technical Report.*

Production scheduling is cache-aware as well. A session is routed back to the cluster holding its prefix, with a secondary cluster preassigned for failover. Short requests under 2K and long requests up to 1M receive separate resource budgets so a burst of huge contexts cannot destroy time-to-first-token for everyone else.

The economics of one-million-token context therefore depend on reuse. The report's representative coding request carries a 400K historical prefix but adds only 4K new tokens. A cache hit avoids prefilling 400K again; a miss can be orders of magnitude more expensive.

## 8. Open weights do not make self-hosting ordinary

The public deployment guidance is unusually direct:

| Source | Reference starting point |
|---|---|
| Kimi technical blog | A supernode with 64 or more accelerators is recommended |
| vLLM recipe | At least 8 x GB300; multi-node for production traffic |
| SGLang cookbook | Platform recipes include 8 x B300, 8 x GB300, 16 x B200/H200, and 32 x H100 |
| SGLang large-scale presets | 16, 32, or 64 GPUs optimized for throughput or capacity |

Framework, hardware, context length, and concurrency change the minimum. No row is a universal guarantee. SGLang's low-HBM example deliberately reduces context to 65,536, while some 128K profiles need dedicated pipeline parallelism and cache-precision choices. A model advertising 1M context does not mean every public recipe can serve 1M at production concurrency.

K3 consequently has three distinct adoption modes:

1. **Official API or Kimi Code:** practical for most developers because Moonshot operates the weights, network, caches, and scheduler.
2. **Inference partner or large cloud cluster:** offers control over data, latency, customization, and unit economics, but requires multi-node serving expertise.
3. **Research download:** enables weight and implementation audit, but downloading 1.56TB is only the first requirement.

## 9. The harness must preserve complete thinking history

K3 always thinks and returns separate `reasoning_content` and final `content`. For multi-turn conversations and tool calls, the documentation requires the complete assistant message to be passed back unchanged, including:

- `reasoning_content`;
- `content`;
- `tool_calls`;
- other returned fields.

Keeping only the visible answer breaks the preserved-thinking-history regime used in training. Moonshot also warns that an incompatible harness, or switching to K3 in the middle of a session started with another model, can make output quality highly unstable.

Compatibility is therefore more than accepting an OpenAI-style endpoint. The agent framework must persist complete assistant state, tool results, and ordering correctly. That affects database schemas, log redaction, context compaction, model hot-swapping, and privacy policies.

Moonshot also lists excessive proactiveness as a limitation. K3 is trained for hard long-horizon tasks, so it may make unexpected decisions when the issue is small or the user's intent is ambiguous. Applications with strict boundaries should specify editable scope, approval gates, stop conditions, and rollback behavior in the system prompt or `AGENTS.md`.

## 10. The license is permissive, but not unconditional

The Kimi K3 License permits use, copying, modification, distribution, sublicensing, sale, deployment, and fine-tuning. Two commercial conditions deserve early legal review:

1. A company and its affiliates operating a Model-as-a-Service business with more than $20 million in aggregate revenue over any consecutive 12 months must enter a separate agreement with Moonshot before commercial use of K3 or derivatives.
2. A commercial product with more than 100 million monthly active users, or more than $20 million in monthly revenue, must prominently display `Kimi K3` in its interface.

Internal use and access through Moonshot's official products or certified inference partners receive specified exceptions.

“Full weights released” is accurate. “No commercial restrictions” is not. Enterprises need to distinguish internal inference, embedded product features, model API services, and large consumer products because the license treats them differently.

## 11. The benchmark picture is fuller, and still not a single race

The report adds third-party results current as of July 23: K3 scores 57.1 on Artificial Analysis Intelligence Index v4.1 and 74.7 on the Vals Index. At that snapshot it ranked first on WebDev Arena, eighth on Text Arena, and fourth on Agent Arena. These leaderboards move, and evaluations use different harnesses including Kimi Code, Claude Code, and Codex.

Moonshot's cost chart reports BrowseComp at 91.2% and $2.03 per task under its setup. On Kimi Code Bench 2.0, K3 scores four points below Claude Fable 5 at about 38% of the cost.

![Kimi K3 score versus per-task inference cost](imgs/kimi-k3-open-weight-release-audit/04-cost-efficiency.jpg)

*Score versus per-task inference cost across four suites. This measures model, harness, and price as a system, not bare models under one uniform runner. Source: Kimi K3 Technical Report.*

The figures support a claim that K3 is near the cost-efficiency frontier. They do not prove that self-hosting will be cheaper. The chart uses API prices or internal run costs and excludes cluster procurement, networking, idle capacity, operations, and recovery. For many teams, cache-hit pricing on the official API will be more practical than operating 16 to 64 high-end GPUs.

## Conclusion: K3 opens an auditable frontier system, not a local-running ticket

Kimi K3 fulfilled the two most important launch promises. Full weights and a 47-page technical report are public. Researchers can inspect 96 weight shards, native MXFP4, hybrid KDA/MLA, Attention Residuals, Stable LatentMoE, custom Transformers code, and the license.

The report's deeper lesson is that long-horizon agents have outgrown the model boundary. Million-token trajectories require model state, KV cache, sandbox, tool environment, checkpointing, scheduling, and recovery to persist together. Production serving must even know which cluster holds a session's history so it does not repeatedly recompute the world.

K3's openness should therefore be measured on three axes:

- **Research openness:** full weights and architecture are public; training data and a complete training stack are not.
- **Commercial openness:** broad use is allowed, with custom revenue, MaaS, and attribution conditions.
- **Deployment accessibility:** vLLM and SGLang provide paths, but the practical barrier remains 1.56TB of weights and a multi-node high-end GPU cluster.

K3 is not an open model that everyone can start beside a desk. It is a data-center-scale agent system that outsiders can finally audit, adapt, and host. That is the release's real significance.
