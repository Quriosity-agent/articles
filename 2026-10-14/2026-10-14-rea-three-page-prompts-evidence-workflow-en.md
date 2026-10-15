---
title: "Inside REA's Three-Page Prompt Pack: Copying It into Codex Does Not Make Codex a Decompiler"
date: 2026-10-14
source: "https://x.com/qwerty__cs/status/2110345831635452411"
canonical: "https://github.com/morluto/rea"
tags:
  - REA
  - Reverse Engineering
  - Codex
  - Claude Code
  - MCP
  - Agent Skill
  - Evidence Ledger
  - Ghidra
  - Hopper
---

# Inside REA's Three-Page Prompt Pack: Copying It into Codex Does Not Make Codex a Decompiler

> **TL;DR:** The three-page prompt pack circulating on X is not a decompiler, nor does it give an ordinary Codex session the ability to inspect APKs, IPAs, EXEs, or firmware. Its real contribution is to compress REA's investigation discipline into a copyable entry point: map one feature, audit what remains unknown, run a bounded observation only when necessary, build an independent implementation, and verify each claim. The capability still comes from a connected REA MCP server, the target artifact, providers such as Hopper, Ghidra, IDA, or JADX, and retained Evidence. Without that stack, the text can produce a plan. With it, the prompts can orchestrate a real investigation.

![REA prompt workflow page 1](imgs/rea-three-page-prompts-evidence-workflow/rea-prompt-workflow-page-1.jpg)

- **Source post:** [the three-page compilation posted by qwerty__cs](https://x.com/qwerty__cs/status/2110345831635452411)
- **Pages two and three:** [the follow-up post in the same thread](https://x.com/qwerty__cs/status/2110346010593837566)
- **Quoted article:** [a third-party tutorial by 0xCodila](https://x.com/0xCodila/status/2109623431763292649)
- **Official project:** [morluto/rea](https://github.com/morluto/rea)
- **Official MCP prompt documentation:** [Guided MCP prompts and completion](https://github.com/morluto/rea/blob/cf0a38ad9774ee9acff3164052688f7a58a1c72c/docs/mcp-prompts.md)
- **Published:** 2026-10-14
- **Accessed:** 2026-10-15

## One-sentence verdict

**This is not reverse-engineering expertise encoded in a magic prompt. It is a worksheet for an Agent that already has reverse-engineering tools.**

If REA is a laboratory, the three pages are the procedure. Codex or Claude Code is the researcher, MCP is the instrument interface, Hopper/Ghidra/IDA/JADX are the instruments, the Evidence ledger is the lab notebook, and behavioral comparison is acceptance testing.

Remove any critical layer and the claim that one can paste the prompt and immediately reverse engineer anything becomes misleading.

## First, correct the attribution

The source post says the REA author released the prompts, and the image header names the project's creator. The three tall images with large headings, product logos, and a numbered walkthrough are not, however, official release graphics found in the REA repository.

The verifiable relationship is more precise:

1. The core prompt language comes from REA's official workflow and MCP prompts.
2. The source thread was posted by `@qwerty__cs`.
3. It quote-posts a third-party tutorial by `@0xCodila`.
4. The images repackage official text for social distribution.

This article therefore treats the images as a **third-party quick-reference guide to REA**, while using the current GitHub source and documentation to establish the capability boundary.

## What the three pages actually contain

### Page one: investigate first, then preserve uncertainty

The first page introduces two moves:

- **Map & Understand:** investigate one feature through entry points, relevant functions, data flow, and static evidence.
- **Find the Gap:** audit unknowns that remain open, conflict with one another, are blocked by tooling, or have genuinely been resolved by evidence.

The valuable part is not the suggested tool names. It is the repeated demand to separate three epistemic states:

| State | Meaning |
|---|---|
| Observation | What a tool actually read or a runtime capture actually observed |
| Inference | An explanation derived from evidence, with confidence and alternatives |
| Unknown | A question that incomplete, unsupported, or conflicting coverage cannot answer |

That distinction targets a common failure mode in coding Agents: finding a few strings or functions and narrating a possible path as confirmed product behavior. REA's current Skill makes the same rule explicit. Static analysis cannot be presented as runtime observation, and incomplete evidence cannot justify a claim of original source recovery.

### Page two: observe, implement independently, and test claim by claim

![REA prompt workflow page 2](imgs/rea-three-page-prompts-evidence-workflow/rea-prompt-workflow-page-2.jpg)

The second page advances from understanding to reconstruction:

- **Watch It Run:** design a bounded, cleanable runtime experiment only when static evidence is insufficient.
- **Build Your Version:** implement against behavior that has actually been established.
- **Verify Against Original:** mark each finite acceptance claim as pass, fail, or unknown.

The order matters. A generic request to “clone this app” tends to mix observation with implementation. The Agent guesses how the product works while writing UI, then substitutes visual resemblance for behavioral equivalence. REA asks for an evidence-backed behavior specification first, followed by implementation and a compatible comparison against the original target.

“Build Your Version” is not automatic authorization. Ownership, research permission, execution scope, data access, licensing, and applicable law still constrain the task. A prompt cannot grant those rights.

### Page three: make version differences and crashes evidence questions too

![REA prompt workflow page 3](imgs/rea-three-page-prompts-evidence-workflow/rea-prompt-workflow-page-3.jpg)

The third page adds two recurring tasks:

- **Compare Two Versions:** compare files, functions, resources, and runtime behavior across two shipped artifacts.
- **Trace a Crash:** keep observed failure, statically reachable paths, inferred causality, and unobserved paths separate.

This reveals REA's real emphasis. It is less about one-click decompilation than maintaining evidence state through a long investigation. A string present in version A and absent from version B does not prove a feature was removed. A function that can reach a crash site is not necessarily the cause seen at runtime. The prompts make the Agent state that distance.

## What this adds beyond asking Codex to reverse engineer something

| Common failure in a generic request | Constraint added by the REA workflow |
|---|---|
| Ambiguous target and version | Bind a specific artifact, path, and question first |
| Broad scanning from the start | Begin with the smallest useful inventory and expand around hypotheses |
| Treating string hits as facts | Separate observations, inferences, and unknowns |
| Presenting static results as runtime behavior | Require bounded runtime Evidence for runtime claims |
| Concluding absence after a failed search | Preserve search boundaries and residual unknowns |
| Declaring success after producing similar UI | Evaluate a finite specification as pass/fail/unknown |
| Repeating analysis in every turn | Reuse sessions, Evidence IDs, and retained findings |

The main improvement is not raw model intelligence. It is **investigation discipline, reusable state, and explicit completion criteria**. That is the practical advantage for Codex, Claude Code, Cursor, and similar Agents.

## The prompt is only one layer of the system

REA's current documentation explicitly says that its MCP prompts complement the generated tool catalog. They do not add, remove, or invoke tools by themselves. The complete stack contains at least these layers:

| Layer | Responsibility |
|---|---|
| Three-page prompt guide | Gives the user a natural-language task template |
| REA Skill | Defines target routing, Evidence discipline, unknown handling, and completion |
| REA MCP / CLI | Exposes structured tools, sessions, and Evidence |
| Provider | Actually reads the target through Hopper, Ghidra, IDA, JADX, or a JavaScript analyzer |
| Agent | Selects the next action, interprets results, and maintains the investigation narrative |
| Verification environment | Compares the reconstructed behavior or output with the target |

With only the text, Codex may know that a tool ought to be called while having no such tool. The same is true of installing only the Skill: the current official Skill says that installation does not register the MCP server, install analysis engines, or add tools to an Agent that is already running.

## The official implementation is more careful than the social graphic

At the inspected revision, REA exposes six provider-neutral guided MCP prompts:

| Prompt | Purpose |
|---|---|
| `investigate_feature` | Trace a feature from discovery into function Evidence |
| `compare_application_versions` | Compare two shipped artifacts |
| `verify_reconstruction` | Evaluate a finite reconstruction specification |
| `trace_crash` | Correlate a crash symptom with static paths and optional runtime Evidence |
| `audit_residual_unknowns` | Audit unresolved unknowns |
| `prepare_bounded_process_capture` | Design a controlled process experiment before execution |

Three implementation details are especially important:

1. Prompt arguments and completion selections are treated as untrusted selection data, not instructions or authorization.
2. Tool results return Evidence inline; an Evidence ID is a traceable reference inside a session, not a substitute for the content.
3. Completion suggests candidates but does not read the target, start analysis, or broaden an operation.

Together they create a useful Agent safety boundary: **a suggestion is not an action, an argument is not authorization, and an identifier is not the Evidence itself.**

## Different targets still require different tools

The claim that APKs, iPhone apps, Windows executables, firmware, and closed-source software are all supported should be read as a routing ambition, not a guarantee that one installation can analyze every target on any machine.

| Target | Remaining real-world requirements |
|---|---|
| Electron / JavaScript | REA can use its JavaScript static-analysis path without a native decompiler |
| Android APK | Bring-your-own Java/JADX prerequisites and capabilities exposed by the current provider |
| Native macOS, iOS, or Windows binary | An available Hopper, Ghidra, or IDA engine with support for the format |
| Firmware | A recognized image format, extraction tooling, and architecture support |
| Runtime observation | A host capable of executing the target and an explicitly authorized scope |
| Packing, obfuscation, integrity checks | These may still reduce static visibility or block experiments |

Prompts select and orchestrate capabilities. They do not create them.

## A more accurate way to use the pack

For legitimate, authorized compatibility work, debugging, security research, or clean-room implementation, a defensible workflow is:

1. Identify the artifact, version, hash, and one concrete question.
2. Verify that REA tools are visible in the current Agent session, not merely that a Skill file exists.
3. Confirm that the target's required provider is available.
4. Begin with the smallest static overview and retain Evidence plus search boundaries.
5. Keep unconfirmed behavior as unknown instead of filling gaps with plausible prose.
6. Design a bounded runtime observation only when static evidence cannot answer the question.
7. Write an independent behavioral specification rather than claiming to have recovered the original source.
8. Compare each requirement reproducibly and allow unknown as a result.
9. Preserve tool versions, target identity, limitations, and remaining questions for the next pass.

This does not remove the expertise barrier. It moves the Agent's output from “an answer that sounds plausible” toward an investigation record that can be challenged, reviewed, and reproduced.

## How this relates to the earlier REA source audit

The earlier article, [“REA Source Audit: Not an AI App Cloner, but an Agent Runtime with an Evidence Ledger for Reverse Engineering”](../2026-10-09/2026-10-09-rea-evidence-ledger-agentic-reverse-engineering-runtime-en.md), answered what the complete REA system is.

The three-page pack answers a different question: **how does an ordinary user enter that system through natural language?**

They are not competing approaches. The prompt is the entrance, the Skill is the operating procedure, MCP and providers are the execution layer, and Evidence plus verification prevent the Agent from presenting a guess as completed work.

## Conclusion

The prompt pack is worth keeping, but not mythologizing.

Its strongest idea is not a clever sentence. It is a closed investigation loop: **identify the target, manage unknowns, observe within bounds, implement independently, and verify claim by claim.** That is substantially better than telling Codex to analyze and clone an app, because the model receives an evidence format and an explicit stopping condition.

Copying three images still does not install tools, connect MCP, authorize target access, or turn a similar implementation into an equivalent one. The hard work moves from manually operating every reverse-engineering tool to jointly defining the question, reviewing Evidence, controlling runtime scope, and testing the result.

**It is an interface to REA, not REA itself; a method for a reverse-engineering Agent, not universal decompilation capability.**

## References

- [Source post - X](https://x.com/qwerty__cs/status/2110345831635452411)
- [Follow-up prompt images - X](https://x.com/qwerty__cs/status/2110346010593837566)
- [Quoted third-party article - X](https://x.com/0xCodila/status/2109623431763292649)
- [REA official repository](https://github.com/morluto/rea)
- [REA guided MCP prompts](https://github.com/morluto/rea/blob/cf0a38ad9774ee9acff3164052688f7a58a1c72c/docs/mcp-prompts.md)
- [REA Skill at the inspected commit](https://github.com/morluto/rea/blob/cf0a38ad9774ee9acff3164052688f7a58a1c72c/.agents/skills/reverse-engineer-anything/SKILL.md)
- [REA website](https://rea.tools/)

*The inspected official repository revision was `cf0a38ad9774ee9acff3164052688f7a58a1c72c`, accessed on 2026-10-15. REA changes quickly; tool names, client support, and provider prerequisites may move. The three images came from the supplied X thread and are preserved locally in this repository. Their layout is third-party packaging, not official REA artwork. This article discusses only legitimate, authorized research, interoperability, debugging, and security analysis.*
