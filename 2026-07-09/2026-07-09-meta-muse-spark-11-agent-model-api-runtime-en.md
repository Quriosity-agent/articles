---
title: "Meta Muse Spark 1.1 Deep Dive: Model APIs Are Becoming Compatibility Layers for Agent Runtimes"
date: 2026-07-09
source: "https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/"
canonical: "https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/"
tags:
  - Meta
  - Muse Spark 1.1
  - Meta Model API
  - Agent
  - Computer Use
  - Multimodal
  - Model API
---

# Meta Muse Spark 1.1 Deep Dive: Model APIs Are Becoming Compatibility Layers for Agent Runtimes

> **TL;DR:** Meta released Muse Spark 1.1 on July 9, 2026, and opened hosted access to U.S. developers through the public preview of Meta Model API. The consequential part is not only the benchmark profile. Meta is positioning the model to enter existing agent stacks directly: OpenAI Responses and Chat Completions compatibility, an Anthropic Messages format, a one-million-token context window, built-in search, structured output, parallel tool calls, multimodal input, and adjustable reasoning effort. Muse Spark 1.1 is designed less like a model waiting for chat requests and more like an agent-runtime foundation that OpenCode, Cline, OpenClaw, or a custom harness can drive.

- **Source:** [Introducing Muse Spark 1.1 - AI at Meta](https://ai.meta.com/blog/introducing-muse-spark-meta-model-api/)
- **Developer guide:** [Build with Muse Spark on Meta Model API](https://developer.meta.com/ai/resources/blog/build-with-muse-spark/)
- **Evaluation report:** [Muse Spark 1.1 Evaluation Report](https://ai.meta.com/static-resource/muse-spark-1-1-evaluation-report)
- **Published:** 2026-07-09
- **Accessed:** 2026-07-10
- **Tags:** Meta / Muse Spark 1.1 / Meta Model API / agent / computer use / multimodal / model API

## One-Sentence Take

**Muse Spark 1.1 matters because Meta is using a hosted API that fits existing agent protocols to compete for the model-runtime layer.**

Meta models have historically meant Llama and open weights to many developers. Muse Spark 1.1 takes a different route. The weights are not being released with this launch; the capability is delivered through Meta Model API. Developers do not deploy inference infrastructure. They change a base URL, API key, and model name.

Meta is now operating in two markets at once:

1. Muse Spark 1.1 powers Thinking mode for hundreds of millions of users across Meta AI.
2. On the developer side, it is a metered hosted service for agentic workloads, compatible with familiar SDKs.

The competitive set is therefore not only open-source models. It is the API and agent ecosystems occupied by OpenAI, Anthropic, Google, and other hosted providers.

## From Muse Spark to 1.1: Optimize the Whole Task

Muse Spark 1.1, developed by Meta Superintelligence Labs, upgrades the original Muse Spark introduced in April. Meta concentrates the changes in three areas:

- **end-to-end agent workflows:** stronger multi-turn memory, long-context coherence, and tool orchestration;
- **advanced coding:** diagnosis, feature work, migrations, and reliable tool use in complex repositories;
- **native multimodal perception:** image, video, and document understanding in one call, with perception feeding later action.

The shared theme is task duration.

Traditional model evaluation asks whether one answer is correct. The Muse Spark 1.1 materials repeatedly ask a different set of questions: can the model follow a changing goal, select tools, delegate to subagents, recover important state much later, inspect its own visual output, and keep working?

The optimization target is moving from response quality to run quality.

## Meta Model API: Compatibility Before Reinvention

At launch, Meta Model API exposes two request-format families:

| Developer ecosystem | Interface | State model |
|---|---|---|
| OpenAI SDK and compatible tools | Responses and Chat Completions | Responses can retain a thread through `previous_response_id`; Chat Completions is client-managed |
| Anthropic SDK and Claude-oriented tools | Messages | multi-turn state is client-managed |

An OpenAI-compatible client needs three core values:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.meta.ai/v1",
    api_key=MODEL_API_KEY,
)

response = client.responses.create(
    model="muse-spark-1.1",
    input="Explain a tool-call loop in one sentence.",
)
```

This is a practical distribution strategy. Meta is not asking developers to learn a new protocol before they can evaluate the model. Existing OpenAI or Anthropic harnesses can switch providers. OpenCode already has a Meta provider; other OpenAI-compatible CLIs can add a custom one.

Wire compatibility does not guarantee behavioral compatibility. Models still differ in how they follow system and developer messages, interpret tool schemas, compact context, and respond to reasoning controls. Meta explicitly recommends using developer messages for standing rules, and reasoning tokens are billed as output.

“Change two lines” is enough for a first call. Production migration still requires retesting prompts, tool-error recovery, structured-output reliability, and cost.

## One Million Tokens, with Active Context Management

Muse Spark 1.1 provides a one-million-token context window. More important is Meta's description of how the model uses it: remembering actions, retrieving information from much earlier work, and compacting the run while preserving critical steps needed later.

The long-horizon agent problem is not only what fits. It is what remains useful after hours of work. A run continuously accumulates:

- the original objective and later revisions;
- files and pages already inspected;
- tool results;
- failed attempts;
- subagent reports;
- verification evidence and open tasks.

Simply appending that history until it reaches one million tokens creates cost, retrieval noise, and attention dilution. Compaction is a runtime policy: which details can be summarized, and which constraints, evidence, and unfinished commitments must survive exactly?

The one-million-token window is best understood as working-memory capacity for an agent, not merely the ability to upload a larger PDF. The compaction policy determines whether that memory remains reliable.

## Multi-Agent Training: Main Agent and Subagent Are Different Jobs

Meta says Muse Spark 1.1 was trained to orchestrate multi-agent systems and reduce end-to-end latency.

As a main agent, it gathers context, makes a plan, and delegates execution across parallel subagents. As a subagent, it is expected to stay within its assignment, understand the tools available to it, and escalate when it cannot proceed.

That distinction matters. The hard part of multi-agent systems is rarely launching four model calls. It is defining the role boundaries:

- who owns the final objective;
- who can edit files or execute shell commands;
- how dependencies are represented;
- when a subagent should stop exploring;
- who arbitrates conflicting results;
- what intermediate state must be durable.

Meta's developer example runs the same Muse Spark model in four roles: product manager, backend, frontend, and technical writer. They coordinate through durable comments on a shared Kanban board. The product manager can plan and clarify but cannot use a terminal; engineering roles receive implementation tools.

This is closer to an auditable team system than a free-form agent group chat. Roles become permission contracts, dependencies become scheduling contracts, and Kanban comments become the persistence protocol.

## Computer Use: Know When to Script and When to Click

Muse Spark 1.1 is not designed to reason through every desktop action one click at a time. Meta says it was trained to write scripts when automation is faster, click when direct interaction is simpler, and batch actions when appropriate.

![Muse Spark operating Minesweeper through screenshot-based computer use](imgs/meta-muse-spark-11-agent-model-api-runtime/muse-spark-computer-use.webp)

The Minesweeper example in the developer guide runs inside an ephemeral Linux sandbox. The model receives screenshots, reasons about the board, and returns mouse and keyboard actions. The harness supplies the desktop and execution loop; Meta Model API does not automatically take over a developer's computer.

The boundary is important:

- the model provides perception, reasoning, and proposed actions;
- the harness provides screenshots, coordinate conversion, mouse and keyboard tools, and the loop;
- the sandbox isolates files, credentials, and irreversible operations;
- the verifier decides whether the task was actually completed.

A capable computer-use agent should not be doctrinaire about GUIs. Scripts are faster and more reliable for repeated structured operations. Direct manipulation is better for unfamiliar interfaces, visual state, and small interaction sequences. The valuable skill is choosing when to switch execution modes.

## Multimodal Means Perceive, Then Act

Muse Spark 1.1 understands images, video, audio, and documents. Meta's Marketplace example begins with smartphone video: the model selects useful frames, reasons about the product, then operates a browser to create a Facebook Marketplace listing.

The example places multimodality inside a complete workflow:

```text
Video input → identify product and usable frames → prepare listing data
            → open browser → fill fields → upload media → verify result
```

The same principle applies to coding agents. The model can inspect a screenshot of the page it just built, notice a layout failure, return to the code, and repair it. It can read an error screenshot first, use the pixels to localize the likely component, then search the repository.

Vision and coding are no longer separate endpoints. Perception is the observation in the agent loop; code and GUI operations are the actions.

## Benchmarks: Tool Use Is the Strength, but It Does Not Win Everywhere

Meta's official chart compares Muse Spark 1.1 with the original Muse Spark, Gemini 3.1 Pro, Claude Opus 4.8, and GPT-5.5.

![Muse Spark 1.1 official agent, coding, reasoning, and multimodal benchmark comparison](imgs/meta-muse-spark-11-agent-model-api-runtime/muse-spark-11-benchmarks.webp)

Several results define the model's profile:

| Benchmark | Muse Spark 1.1 | Leader in the chart | Signal |
|---|---:|---:|---|
| MCP Atlas | 88.1 | Muse Spark 1.1 | real MCP server and tool use is a clear strength |
| JobBench | 54.7 | Muse Spark 1.1 | strong professional tool use |
| Toolathlon-Verified | 75.6 | Opus 4.8: 76.2 | close to the leading result |
| OSWorld-Verified | 80.8 | Opus 4.8: 83.4 | strong GUI control, but not first |
| Humanity's Last Exam, with tools | 62.1 | Muse Spark 1.1 | strong tool-augmented reasoning |
| Terminal-Bench 2.1 | 80.0 | GPT-5.5: 83.4 | competitive frontier coding performance |
| SWE-Bench Pro | 61.5 | Opus 4.8: 69.2 | ahead of charted GPT-5.5 and Gemini, behind Opus |
| DeepSWE 1.1 | 53.3 | GPT-5.5: 67.0 | a meaningful gap remains on long-horizon SWE |
| BabyVision | 76.3 | GPT-5.5: 83.6 | multimodal does not mean universal leadership |

The restrained conclusion is that Muse Spark 1.1 is strongest on MCP use, professional tools, finance agents, and tool-augmented reasoning. Strong competitors remain on long-horizon coding, visual reasoning, and some computer-use evaluations.

The evaluation methodology adds important caveats:

1. All Muse Spark 1.1 results run through Meta Model API at `xhigh` reasoning effort.
2. For coding and agentic benchmarks, Meta prefers third-party self-reported scores and runs internal evaluations when those are unavailable.
3. For other benchmarks, Meta reports the more favorable result between self-reported scores and internal API reproduction.
4. Meta acknowledges that its common harness may not be tuned for proprietary competitors and may not show their best native performance.
5. Harnesses, tools, step limits, graders, and attempt counts still vary across benchmarks.

The chart is useful for understanding the model's shape. It is not a single reproducible “overall winner” calculation.

## Pricing: Meta Wants Long-Running Agent Volume

Meta Model API public-preview pricing is:

![Meta Model API launch pricing](imgs/meta-muse-spark-11-agent-model-api-runtime/meta-model-api-pricing.webp)

| Item | Price |
|---|---:|
| Input | `$1.25 / 1M tokens` |
| Cached input | `$0.15 / 1M tokens` |
| Output | `$4.25 / 1M tokens` |
| Web search grounding | `$2.50 / 1,000 queries` |

Each new account also receives a one-time `$20` credit.

The structure is designed for agent workloads: inexpensive context ingestion, much cheaper cached input, and separately metered search. For agents repeatedly reading the same repository, policy, tool definitions, or long documents, cache pricing may matter more than the headline input rate.

Reasoning tokens are billed as output, however, and Meta's published benchmarks use `xhigh`. Production teams should not compare `$1.25/$4.25` with other providers' headline prices in isolation. They need actual reasoning tokens, tool calls, search queries, retry rate, cache hits, and final completion rate per task.

The cheapest token does not always create the cheapest completed task. A model that avoids failed branches can cost less end to end.

## The Most Important Safety Sentence Is Not in the Launch Copy

The launch post says Muse Spark 1.1 operates within safe margins across Chemical and Biological, Cybersecurity, and Loss of Control frontier-risk categories. The 112-page evaluation report gives the more precise interpretation.

**Without mitigations, Meta cannot rule out Muse Spark 1.1 reaching the “high risk” capability threshold in both Chemical and Biological risk and Cybersecurity. After layered mitigations are applied, Meta assesses the residual deployment risk as “moderate or lower.”** Loss of Control capability remains moderate or lower.

This is not a semantic footnote. It is the deployment logic: the model may possess higher-risk capabilities, while access controls, monitoring, refusals, classifiers, and other system measures reduce residual risk enough for release.

For an agent API, that distinction is especially important. Meta also evaluated:

- direct jailbreaks and harmful requests;
- prompt injection from untrusted pages, documents, and repositories;
- developer-prompt attacks;
- misuse and false refusals in agent settings;
- risk escalation by coding agents;
- honesty, sycophancy, scheming, and evaluation awareness.

The report says Muse Spark 1.1 performs strongly on SWE-PI Synthetic, while the more realistic long-horizon SWE-PI Agent still shows elevated prompt-injection attack success. Any harness that reads websites, MCP output, `AGENTS.md`, or external documents must treat that content as untrusted and enforce permissions outside the model.

## How Development Teams Should Evaluate It

Muse Spark 1.1 is best added to a model router and tested on real work, not promoted to the only default based on the launch chart.

| Scenario | Recommendation |
|---|---|
| MCP and multi-tool agents | prioritize testing; this is the clearest official strength |
| OpenCode, Cline, OpenClaw, and compatible harnesses | migration is easy, but prompts and tool schemas still need retesting |
| long repositories, documents, and multi-hour tasks | measure whether critical constraints survive compaction |
| GUI plus shell workflows | check whether the model switches sensibly between scripts and clicks |
| front-end and visual debugging | use screenshot → code → browser verification loops |
| safety-sensitive tools | keep least privilege, sandboxes, confirmation gates, and injection defenses |
| global production | note that the preview currently targets U.S. developers |

Useful task-level metrics include:

- end-to-end completion, not only individual tool-call success;
- human interventions and replans;
- constraints lost after compaction;
- actual reasoning, output, search, and cached-input cost;
- duplicate or conflicting subagent work;
- recovery after tool failure;
- privilege escalation induced by untrusted content;
- whether a reviewer accepts the final deliverable.

## What the Launch Does Not Establish

The release has several clear boundaries.

First, Meta Model API is a public preview limited to U.S. developers. Production SLAs, region expansion, and long-term pricing may change.

Second, Muse Spark 1.1 is a hosted API launch, not a Llama-style open-weight release. Fast integration does not imply self-hosting, weight inspection, or independence from Meta's infrastructure.

Third, a one-million-token window does not guarantee equal recall everywhere in that window. The report gives Muse Spark 1.1 a 54.1 score on MRCR Long Context, below the charted GPT-5.5 result of 74.0. Long-context reliability still depends on the retrieval distribution and task.

Fourth, published benchmark results use `xhigh` reasoning effort. Production deployments may choose lower settings for latency and cost. Completion, speed, and spend need to be measured at each effort level.

## Conclusion

Muse Spark 1.1 advances Meta's model strategy in a consequential direction.

Meta is no longer influencing the market only through consumer Meta AI or open weights. It now offers a hosted, metered agent-model API compatible with OpenAI and Anthropic tooling. The million-token context window, active compaction, parallel subagents, visual computer use, and built-in search all point to the same objective: let the model own a complete run, not only the next response.

It is not first on every benchmark, and it is not an open-weight release. Public-preview status, U.S.-only access, `xhigh` evaluation cost, and dependence on system-level safety mitigations all belong in the decision.

The strategic signal is still clear: **the next model-API competition is not only about context, price, and one-shot answer quality. It is about entering an existing agent harness with minimal friction and working reliably inside it for a long time.**

Once protocols, tools, memory, vision, and subagents become standard interfaces, providers are no longer competing for a prompt. They are competing for the task runtime.
