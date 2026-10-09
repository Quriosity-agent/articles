# REA Source Audit: Not an AI App Cloner, but an Agent Runtime with an Evidence Ledger for Reverse Engineering

> **Bottom line:** REA is neither a model that automatically reconstructs arbitrary software nor merely a Skill that teaches an agent how to use a disassembler. It is a TypeScript control plane that exposes Hopper, Ghidra, IDA, Chrome, JADX, static parsers, and runtime-observation tools through a shared CLI and MCP interface. Each finding is wrapped in Evidence that records target identity, provenance, confidence, limitations, and links to prior observations. Its real contribution is turning decompiler output into a traceable investigation. Its critical boundary is that local analysis does not mean every result stays on-device, and temporary isolation does not make untrusted binaries safe to parse.

![REA analyzing a local Mach-O binary in Hopper](imgs/rea-evidence-ledger-agentic-reverse-engineering-runtime/rea-hopper-analysis.png)

The user-provided [`donghaozhang/rea`](https://github.com/donghaozhang/rea) repository is a fork created on October 9, 2026. GitHub identifies both its parent and source as [`morluto/rea`](https://github.com/morluto/rea), and the npm package [`rea-agents`](https://www.npmjs.com/package/rea-agents) points to the same upstream repository. This article therefore uses the supplied link as its entry point while auditing the fork's fixed [`863674b`](https://github.com/donghaozhang/rea/tree/863674b2e92dd7c699768db82d521ccc88b7ebe4) snapshot, which reports `rea-agents@6.1.0`. Project ownership, stars, and release metadata refer to the upstream project.

At audit time, upstream had roughly 30,900 stars and 3,700 forks, and `v6.1.0` had been released that day. The repository was moving quickly, so every technical conclusion below is tied to the fixed snapshot rather than an assumed future `main`.

---

## 01 | Skill, MCP Runtime, Analysis Engine, and Code Generation Are Four Different Layers

REA's one-command setup makes it easy to describe the project as a reverse-engineering Skill. The source shows four separate layers:

| Layer | Responsibility | What it does not do |
|---|---|---|
| Skill / workflow instructions | Teaches an agent to investigate, trace, validate, and preserve unknowns | Does not read binaries or run a decompiler |
| CLI and MCP server | Defines tool contracts, manages sessions, selects providers, and returns structured results | Does not replace Hopper, Ghidra, or IDA analysis |
| Provider adapters | Connects local disassemblers, browsers, parsers, and runtime observers | Does not infer the product's intent for the agent |
| Host agent | Chooses follow-up questions, explains behavior, and writes and tests a candidate implementation | Generated code is not automatically equivalent to the original |

`rea setup` registers the MCP server and installs matching workflow instructions. They complement one another but are not the same thing. With only the Skill, an agent knows the method. It needs the MCP/CLI runtime and an available provider to obtain real disassembly, pseudocode, module relationships, or runtime observations.

REA also does not emit recovered original source. Its README draws the line explicitly: native workflows return pseudocode and assembly, JavaScript and Electron workflows recover modules and relationships, and the host agent uses those findings to explain, implement, and test.

---

## 02 | How an Investigation Actually Flows

![REA's official investigation flow: the agent asks, REA calls local analysis tools and returns evidence, then the agent explains, implements, and tests](imgs/rea-evidence-ledger-agentic-reverse-engineering-runtime/rea-investigation-flow.svg)

The source-level workflow can be summarized as follows:

1. The agent selects an MCP workflow or lower-level tool for the user's question.
2. A session binds the target, SHA-256 digest, analysis provider, and profile.
3. The provider adapter starts or connects to a local tool and performs static or runtime observation.
4. REA normalizes the result and attaches authority, confidence, limitations, and locations.
5. Evidence enters the current session ledger for later comparison, tracing, export, or reference.
6. The agent narrows the question with follow-up calls, then implements and validates a candidate in the user's project.

One important choice is that a selected provider is not silently replaced after a runtime failure. Hopper, Ghidra, and IDA may infer different function boundaries, types, and pseudocode for the same binary. An invisible fallback would make two results appear continuous even though their evidentiary source had changed. REA instead returns a typed failure and remediation, leaving any provider switch as an explicit decision.

---

## 03 | This Is No Longer “an MCP Wrapper for Hopper”

The generated `product-catalog.json` for this snapshot lists **139 MCP tools, 95 CLI commands, 6 MCP prompts, 27 provider entries, and 14 setup clients**. Its major target families include:

| Target | Primary path | Observable output |
|---|---|---|
| Native binaries | Hopper, Ghidra, IDA | Pseudocode, assembly, strings, symbols, calls, and references |
| JavaScript / Electron | AST, ASAR, source maps, CDP | Modules, imports, routes, IPC, preload, and native add-on relationships |
| Websites | Chrome-family browser, Playwright/CDP | DOM, scripts, requests, responses, screenshots, and runtime events |
| .NET | Built-in static metadata and CIL reader | Types, members, CIL, native dependencies, and build comparisons |
| Android | Headless JADX | Manifest declarations, classes, methods, and reference tracing |
| Firmware | Binwalk / Unblob | Regions, extraction results, and native-analysis handoffs |
| ELF / crashes / processes | pwntools, GDB/pwndbg, PTY capture | Layout, mitigation candidates, cores, terminal, and filesystem behavior |
| EVM | EVMole adapter | Selectors, byte offsets, inferred arguments, and mutability |
| Apple artifacts | Mach-O, plist, NIB, and asset-catalog readers | Bundle anatomy, signing, resources, and dynamic-library relationships |

This does not mean every capability is available on every computer. Hopper is separate commercial software. Ghidra, IDA, JDK, JADX, Binwalk, Unblob, Chrome, and platform tooling have their own installation, version, licensing, and host constraints. `tools/list` can expose the complete catalog, but actual callability comes from `binary_session.tool_availability`, not the README matrix.

---

## 04 | The Most Valuable Abstraction Is Evidence, Not Tool Count

The Evidence schema in `src/domain/evidence.ts` includes:

- target name, local path, format, architecture, and SHA-256;
- provider ID, name, version, and optional analysis profile;
- operation, parameters, raw result, and normalized result;
- `observed`, `derived`, or `inferred` confidence;
- `shipped-artifact`, `controlled-replay`, `historical-reference`, `external-service`, or `analyst-inference` authority;
- execution environment, limitations, and address, offset, or artifact-path locations;
- links to other Evidence records.

An `evidence_id` is a canonical digest of semantic content, not an incrementing database key. Imports are parsed and reauthenticated. Conflicting content under an existing ID is rejected. Recorded values become deeply immutable, and a bundle is fully validated before its records are merged atomically.

REA also tracks residual unknowns. When a call target cannot be resolved, runtime coverage is incomplete, or a comparison lacks sufficient authority, the system can retain what remains unknown, what kind of evidence would resolve it, and its current state. The agent does not have to fill the gap with a fluent guess.

This makes REA closer to an investigation-record protocol than a natural-language layer over disassembler buttons. It cannot guarantee that a conclusion is correct, but it makes a better question possible: did this claim come from shipped bytes, a controlled replay, a historical reference, or analyst inference?

---

## 05 | “Local Analysis” Is True, but It Does Not Mean “Fully Offline and Fully Private”

The README makes a careful claim: REA analyzes targets locally, the agent receives tool results, and the model provider has its own data policy. That qualification matters.

Confirmed local controls include:

- Hopper, Ghidra, IDA, and static parsers process the target on the host;
- Ghidra uses an isolated temporary project with private home, cache, and runtime directories, then deletes the temporary project when the session closes;
- local provider bridges authenticate with a random capability token and a current-user Unix socket;
- tokens travel through private session descriptors rather than command-line arguments or environment variables;
- setup first produces a concrete change plan, presents target files and external actions, waits for approval, and preserves backups of existing client configuration.

These controls do not create an end-to-end privacy boundary:

- pseudocode, strings, paths, and selected observations returned to the host agent may enter a cloud-model context;
- browser and runtime workflows may execute the target or access its pages, depending on the requested task;
- setup, update, and optional provider installation may contact npm, GitHub, or Hopper's official download origin;
- malicious processes running as the same operating-system user are outside the protection offered by a capability token.

The precise interpretation is: **the original target is analyzed by local tools by default, and REA does not upload the whole application to a proprietary analysis service; selected Evidence is still delivered to the host agent, whose model-provider policy governs the next data boundary.**

---

## 06 | It Implements Isolation Controls, but Explicitly Is Not a Sandbox

`SECURITY.md` does not market temporary directories as a security sandbox. It states that opening an untrusted binary delegates parsing and analysis to a local provider with the user's permissions.

The existing controls are meaningful:

- Ghidra imports only the requested target, bounds startup and protocol messages, requests CPU and heap limits, and cleans its private project;
- REA cleans only resources it can prove it owns rather than killing processes by name during recovery;
- Hopper downloads are restricted to the official HTTPS origin, size-bounded, and checked against the vendor-published checksum;
- setup records paths to existing Ghidra and Java installations but does not download or upgrade them;
- large results respect an MCP response budget, while complete Evidence can be atomically exported instead of materialized as an uncontrolled string.

The remaining attack surface is substantial. Disassemblers, archives, debug information, browser protocols, JADX, Binwalk, and format parsers all consume attacker-controlled bytes. A private project reduces accidental contamination and persistence; it does not neutralize a parser vulnerability.

Unknown samples still belong in a dedicated VM or isolated host, under a low-privilege account without production credentials, with controlled networking and a disposable workspace. REA's session isolation does not replace operating-system isolation.

---

## 07 | Reconstruction Must Stay Bound to Original Authority

REA frames the journey as Decompile → Understand → Recreate. The first two stages are supported by investigation tools. The third is normally performed by the host agent in the user's project.

That creates three different meanings of success:

1. **Observation success:** a tool returned an authenticated observation from a fixed target.
2. **Understanding success:** the agent's explanation is consistent with the Evidence and preserves unresolved unknowns.
3. **Reconstruction success:** the candidate passes tests, replay, byte comparison, or output comparison tied to original behavior.

Attractive pseudocode satisfies only the first layer. Code that compiles does not establish the third. Compiler optimization, unobserved branches, platform ABI, timing, filesystem effects, and network responses can all separate a plausible implementation from the original product.

The project's reconstruction obligation ledger, authority comparisons, and residual-unknown checks are useful responses to this problem. They still depend on the investigator designing sufficiently strong fixtures and verifiers. An Evidence ledger can prevent “unproven” from being silently rewritten as “proven”; it cannot invent the acceptance standard for the user.

---

## 08 | Strong Engineering Depth, with Visible Friction from Release Velocity

This snapshot contains 1,728 TypeScript files, 663 test files, 50 documentation files, and 17 GitHub Actions workflows. The `rea-agents@6.1.0` package contains 1,027 files and expands to about 6.36 MB, with 32 locked runtime dependencies. Local `npm ci` reported zero known vulnerabilities. Counts are not quality, but this is clearly beyond a weekend MCP wrapper.

I ran the following checks on the fixed snapshot:

- `npm ci`: passed;
- `npm run build`: passed and generated the 139-tool product catalog and completion ledger;
- `npm run test:fast`: 3,507 passed, 7 skipped, and 1 failed, for 3,515 tests total.

The single failure came from `MachOSliceArtifactReader.test.ts`. It hard-codes expected universal Mach-O slice lengths for the host's `/bin/ls`; the current system file reported slightly different extents. This does not invalidate the reader, but it exposes a classic source of brittle tests: an operating-system binary is not a stable fixture.

The broader testing model is unusually careful for an MCP repository. Module, composition, boundary, MCP-boundary, acceptance, conformance, and evaluation lanes are separated. Real Hopper, Ghidra, IDA, Chrome, Apple-artifact, and package paths have dedicated verifiers. The documentation explicitly refuses to treat recorded fixtures, injected providers, or package tests as proof that a real analysis engine works.

This audit did not install or launch Hopper, Ghidra, IDA, JADX, or Binwalk, and it did not run the real browser, Android, firmware, or Windows-provider E2E lanes. The verified scope is the source architecture, build, fast suite, and published CI design, not every provider on this computer.

---

## 09 | Who It Is For, and How to Preserve the Chain of Evidence

REA is a strong fit for:

- teams studying software they own or are authorized to inspect for compatibility, migration, debugging, or security research;
- analysts who need a shared record across Hopper, Ghidra, IDA, JavaScript, and runtime evidence;
- developers who want a coding agent to implement against concrete addresses, calls, modules, and observed behavior;
- engineering teams willing to pin target hashes, provider versions, analysis profiles, and acceptance fixtures.

It is a poor fit for:

- anyone expecting one-prompt automatic cloning of arbitrary applications;
- users who treat pseudocode as original source or compilation as behavioral equivalence;
- people opening unknown samples on a daily workstation that contains production credentials;
- teams that cannot establish authorization, licensing, or applicable legal rights before distributing a reconstruction.

An auditable adoption record should preserve the target hash, REA/package version, provider and version, complete Evidence bundle, unresolved unknowns, candidate implementation commit, and an original-versus-reconstruction comparison report. Without those artifacts, a long agent conversation quickly collapses back into an unverifiable “I inspected it, and this is probably how it works.”

---

## 10 | Conclusion: REA Makes the Reverse-Engineering Agent Account for Its Evidence

REA's headline is one MCP for reverse engineering, but the deeper implementation achievement is a shared investigation semantics. It connects multiple local tools to one session, binds every observation to a fixed target, provider, operation, authority, limitation, and evidence graph, then lets an agent iterate over that record.

That places it well beyond a disassembler MCP wrapper and beyond a standalone Agent Skill. The Skill teaches method. MCP carries tool calls. Providers observe real targets. The Evidence ledger keeps conclusions attached to their origins. A reconstruction still needs independent tests.

The most accurate description is therefore: **REA is an agent-facing reverse-engineering control plane and evidence protocol. It can make investigations faster, more continuous, and more auditable. It cannot automatically recover original source, replace authorization and isolation, or promote a model-generated look-alike into an equivalent implementation without proof.**

---

## Primary Sources

- [User-provided fork: donghaozhang/rea](https://github.com/donghaozhang/rea)
- [Upstream project: morluto/rea](https://github.com/morluto/rea)
- [Audited snapshot `863674b`](https://github.com/donghaozhang/rea/tree/863674b2e92dd7c699768db82d521ccc88b7ebe4)
- [REA website](https://rea.tools/)
- [npm: rea-agents 6.1.0](https://www.npmjs.com/package/rea-agents/v/6.1.0)
- [MCP runtime contracts](https://github.com/donghaozhang/rea/blob/863674b2e92dd7c699768db82d521ccc88b7ebe4/docs/mcp-contracts.md)
- [Architecture map](https://github.com/donghaozhang/rea/blob/863674b2e92dd7c699768db82d521ccc88b7ebe4/docs/architecture.mermaid)
- [Testing strategy](https://github.com/donghaozhang/rea/blob/863674b2e92dd7c699768db82d521ccc88b7ebe4/docs/testing.md)
- [Security policy](https://github.com/donghaozhang/rea/blob/863674b2e92dd7c699768db82d521ccc88b7ebe4/SECURITY.md)
- [MIT License](https://github.com/donghaozhang/rea/blob/863674b2e92dd7c699768db82d521ccc88b7ebe4/LICENSE)

*Audit date: October 9, 2026. Repository metrics, npm versions, provider support, and CI status will continue to change. This article covers lawful, authorized compatibility work, product understanding, and security research; it does not provide operational guidance for unauthorized targets. Source figures are preserved locally from the REA repository.*
