# Claude Fable 5 System Prompt Sample: What It Really Reveals Is the Product Shape of an Agent Harness

Source: <https://github.com/elder-plinius/CL4R1T4S/blob/main/ANTHROPIC/CLAUDE-FABLE-5.md>  
Local material: `/Users/peter/Downloads/CL4R1T4S/CLAUDE-FABLE-5.md` and `CLAUDE-FABLE-5.zh-CN.md`  
Published: 2026-06-11  
Note: This is a system-prompt sample from the community repository CL4R1T4S. It should not be treated as officially confirmed Anthropic material; this article analyzes it as an example of agent product architecture.

---
**Author:** 🦞 龙虾侦探 / Lobster Detective  
**Date:** 2026-06-11  
**Tags:** Claude, System Prompt, Agent Harness, Safety Policy, Tools, MCP, Artifacts, Search, Prompt Engineering
---

The easiest way to read `Claude Fable 5 — System Prompt` is as gossip: a new model name, Claude 5, a Mythos-class tier above Opus, and product strings that look like future launches. But if we only look at the names, we miss the useful part.

The valuable signal is that this sample is not merely a “personality prompt.” It is a full agent harness specification. It combines product identity, refusal policy, tone, mental-health boundaries, search behavior, copyright constraints, MCP recommendations, file creation, computer use, artifacts, persistent storage, tool schemas, and citation rules into one runtime contract.

In other words, modern system prompts for major AI products are no longer just “you are a helpful assistant.” They are becoming policy layers for an operating system: defining who the model is, what it may call, when it must verify facts, how to treat untrusted web pages, when to say less, when to refuse, how to generate deliverable files, and how to preserve state across longer tasks.

---

## One-sentence takeaway

**The most important signal is not whether “Claude Fable 5” is real; it is that large AI products are turning the system prompt into the control plane of an agent runtime.**

Structurally, the sample contains at least eight layers:

| Layer | What appears in the sample | Product meaning |
|---|---|---|
| Identity | Claude Fable 5, product surfaces, API model strings, knowledge cutoff | Model identity is treated as mutable product state, not a static self-introduction |
| Safety | Weapons, drugs, malware, legal/financial advice, wellbeing, self-harm boundaries | Refusal policy becomes scenario-specific behavior, not a single template |
| Tone | Warm tone, minimal bullets, at most one clarification question, avoid over-formatting | Writing style becomes part of product UX |
| Search | When to search, how to verify current facts, how to cite | Parametric knowledge and product-backed facts are explicitly separated |
| Tools | bash, web search, web fetch, image search, file creation, places, weather, and more | The system prompt becomes a human-readable compilation of tool API schemas |
| Agent runtime | Computer use, file handling, artifacts, package management, MCP suggestions | The model is not only chatting; it is operating inside a controlled execution environment |
| Copyright | Search results, long excerpts, song lyrics, copyrighted content constraints | Compliance moves into the generation path, not just post-hoc moderation |
| State | Memory, artifact storage, persistent key-value storage | Long-lived state becomes an explicit part of interaction design |

For teams building Hermes, OpenClaw, QCut, browser agents, or desktop agents, this is the important lesson: differentiation is no longer only about which model you use. It is about whether you have an external runtime that makes the model reliable.

---

## 1. This is not a prompt; it is a product specification

Early system prompts had a narrow job: define the assistant’s role and basic behavior. “You are a helpful assistant.” “Be concise.” “Refuse dangerous content.”

This sample belongs to a different era. Its structure reads like a product spec: define model identity and product surfaces, then define safety boundaries, tone, search rules, tool-calling rules, file-creation rules, artifact behavior, MCP recommendation logic, and full tool definitions.

That means a production AI system prompt now serves three roles.

First, it is a UX specification. The model should be warm, honest, avoid unnecessary questions, avoid over-formatting, and refuse without turning the refusal into a bullet list. These are not safety rules; they are product-experience rules.

Second, it is a safety-policy interpreter. The prompt breaks risk into separate domains: malware, weapons, drugs, self-harm, mental health, legal and financial advice, political persuasion, and creative writing about public figures. Each domain has a different boundary.

Third, it is the protocol layer for tool execution. Exposing tools is not enough. The model also needs to know when to search, when not to assume a file exists, when to create a file, when to present a downloadable artifact, and when web content should be treated as untrusted input.

For agent products, the system prompt should not be treated as an ever-growing magic spell. It should be treated as part of the harness: versioned, tested, minimized, layered, and evaluated by scenario.

---

## 2. Safety policy is moving from “refusal templates” to interaction dynamics

One subtle line in the sample matters: when a conversation feels risky or off, saying less and giving shorter replies is safer.

That is not a static refusal rule. It is an interaction policy. Many failures do not start with one obviously disallowed request. They emerge through multi-turn boundary drift: the user reframes, claims educational intent, emphasizes public availability, or turns malicious intent into “research.” The sample explicitly says not to rationalize compliance merely because information is public or the user claims legitimate research intent.

This matters even more for agents. A chat model that makes a mistake produces a bad answer; an agent with tools may execute commands, write files, call APIs, send messages, or browse the web. Safety therefore has to enter the execution layer, not just the output layer.

A practical implication: production agents should have “reduced-permission modes.” When risk rises, the system should reduce information density, limit tools, require human confirmation, switch to read-only mode, preserve audit logs, or disable certain capabilities entirely.

---

## 3. Search rules reveal a product boundary: what the model knows is not what the product guarantees

The sample repeatedly tells Claude to search official documentation or support pages before answering questions about Anthropic products, features, limits, prices, current events, and other facts that may have changed.

That rule looks ordinary, but it marks an important boundary. What a model may remember in its weights is not necessarily what the product is willing to guarantee. Product features, APIs, pricing, limits, and permissions change quickly. If the model answers from memory, it may wrap stale facts in confident language.

The architecture is clear: the model understands the question and writes the answer; search and citations bring in current facts; product policy decides which questions must go through verification.

For developers, this is more important than merely “adding a web_search tool.” Tool availability does not guarantee correct tool use. You need a search contract: which questions require lookup, which sources are authoritative, how to handle uncertain results, when to say information may be stale, and how to prevent untrusted web pages from becoming instructions.

---

## 4. MCP and tool recommendation point toward platformization

The sample contains an `mcp_app_suggestions` section describing connector directories, third-party MCP app opt-in, direct tool calls, and what not to do.

That suggests a shift from “a few built-in tools” toward a platform model: tool marketplace, permission model, automatic recommendation, and auditable invocation. MCP is valuable not only because it gives the model more interfaces, but because it standardizes tool discovery, authorization, descriptions, calls, and auditability.

This is natural for Notion, Slack, Linear, GitHub, Google Drive, and internal enterprise systems. Users do not want to manually stitch APIs together, and they do not want to grant every permission at once. A better product shape is: the model detects a missing capability, recommends a connector, explains why it is needed, waits for authorization, and then operates within a limited scope.

But this also creates pressure on system-prompt design. The more tools you have, the less plausible it becomes to load all tool instructions all the time. Future agent harnesses need on-demand loading: task-relevant tool schemas, policies, and examples should be loaded when needed; irrelevant tools should not pollute the context.

---

## 5. Artifacts and persistent storage show that the chat window is becoming an app container

The artifact section is especially interesting. It does not only describe how to create files or present outputs. It also describes how artifacts can use `window.storage` as persistent key-value storage for journals, trackers, leaderboards, and collaborative tools.

That means products like Claude are expanding from “answering questions” into “generating small usable applications.” If an artifact can persist state, it is no longer just a one-off HTML preview; it becomes a lightweight application container.

Two product implications follow.

First, AI-generated interfaces need a state model. A tracker, editor, dashboard, or collaboration tool without persistence is a demo. With persistence, it can become something the user returns to.

Second, state requires permission and visibility semantics. The sample distinguishes personal data from shared data and requires user disclosure when shared data is used. “Let the AI make an app” is therefore not just a frontend-generation problem. It is also about data scope, privacy, sharing boundaries, and user notice.

---

## 6. Computer-use rules prove that the hard parts are coordinates, files, packages, and delivery

The computer-use section includes skills, file creation, file handling, output production, file sharing, and package management. These are highly operational details, not chatbot personality instructions.

That is because once a model starts using a computer, reliability becomes concrete. Does the file actually exist? Is the path correct? Can dependencies be installed? Is the generated result deliverable? Is tool output trustworthy? Is a web page trying to inject instructions? After a file is created, does the user receive an actual downloadable result?

This matches the experience of building Hermes and OpenClaw. Agent failures often come not from “the model cannot reason,” but from the runtime failing to constrain environment facts. The agent thinks a file exists when it does not; it thinks a command succeeded because stdout looked plausible; it writes into a temporary directory; it treats web-page text as user instructions.

The core of computer use is therefore not “clicking the mouse.” It is whether the harness can close the loop between observation, planning, execution, verification, and delivery.

---

## 7. The sample also exposes the ceiling of giant prompt design

Putting all these rules into one system prompt has a benefit: the model can see a unified product policy across many situations. But it also has costs.

The first cost is context pollution. Tool schemas, safety rules, search rules, copyright constraints, product descriptions, and tone guidance are all loaded together, even for simple questions.

The second cost is conflict management. Different rules may pull in different directions: ask fewer questions, but clarify missing information; avoid bullets, but structure technical reports; provide factual information, but avoid long copyrighted excerpts; use tools, but distrust web content.

The third cost is evaluation difficulty. In a 100KB-level prompt, changing one line may affect dozens of behaviors. Without regression tests, it is hard to know whether the change improved the product or broke something elsewhere.

A more sustainable direction is layered system prompting: keep core identity and baseline safety resident; load task-specific tools, domain policies, and output templates on demand; inject runtime policy dynamically for high-risk contexts; pass long-horizon state through files and memory rather than one enormous prompt.

---

## 8. Practical takeaways for agent product teams

If we treat this sample as product-design material rather than leak gossip, the lessons are straightforward.

First, system prompts should be versioned. They are product behavior, not temporary prompts. Every change deserves a diff, test cases, and a rollback path.

Second, tool schemas should never be exposed naked. Every tool needs call conditions, permission boundaries, failure handling, output verification, and delivery rules.

Third, search should have an authority strategy. Product features, pricing, APIs, and real-world status should prefer official documentation, not arbitrary search results.

Fourth, agents need evidence chains. When they write files, run commands, send messages, or call APIs, there should be verifiable output. “The model said it is done” is not enough.

Fifth, long context should be split into skills, templates, and policy modules. Cramming everything into the system prompt becomes expensive, hard to test, and prone to conflicts.

Sixth, safety policy should enter the runtime. When risk rises, the system should reduce permissions, switch to read-only behavior, request confirmation, or block tools, instead of relying only on a different refusal style.

---

## Conclusion: beyond prompt leaks, the real story is agent product architecture

Whether this `Claude Fable 5` sample is authentic is hard to verify from a community repository alone. Treating the model names and product claims as confirmed facts would be unwise.

But as a system-prompt sample, it is valuable. It shows a broader trend: AI product competition is moving from “can the model answer?” to “can the product organize the model, tools, policies, files, search, state, and delivery into a reliable runtime?”

The moat is not only a smarter model. It is a better agent harness. The model generates intelligence; the harness turns that intelligence into controllable, auditable, deliverable product behavior.
