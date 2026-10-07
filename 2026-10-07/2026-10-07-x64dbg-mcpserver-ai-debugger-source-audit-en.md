# x64DbgMCPServer Source Audit: AI Can Really Drive x64dbg, but the Default Security Boundary Lags Behind Its Power

> **In one sentence:** x64DbgMCPServer is not a demo in which an AI guesses at debugger buttons from screenshots. It is an in-process C# plugin that exposes registers, memory, disassembly, call stacks, breakpoints, and execution control as MCP tools. Yet the current build listens on all interfaces by default, starts without authentication, and contains a supposedly diagnostic export tool that writes to a hard-coded memory address, so it belongs only in an isolated, disposable, explicitly authorized debugging environment.

![Early example from the upstream README of x64DbgMCPServer starting inside x64dbg](imgs/x64dbg-mcpserver-ai-debugger-source-audit/startup-log.png)

The repository supplied for this article is [`donghaozhang/x64DbgMCPServer`](https://github.com/donghaozhang/x64DbgMCPServer). Provenance matters here: it is a fork of [`AgentSmithers/x64DbgMCPServer`](https://github.com/AgentSmithers/x64DbgMCPServer). On October 7, 2026, both repositories pointed to commit `a8303d7ac7bfd251b9da83b80c9d1d4407ddd8df`, with the fork zero commits ahead and zero behind.

The implementation, history, and design credit discussed below therefore belong to the upstream AgentSmithers project and its contributors. The linked `donghaozhang` repository was an unchanged mirror at the time of inspection.

---

## 01 | What it is: an MCP control plane inside the debugger

x64DbgMCPServer is neither a standalone debugger nor a screen-automation wrapper. It builds on the `DotNetPluginCS` C# plugin scaffold, compiles into a `.dp64` or `.dp32` plugin, and calls x64dbg's Bridge, Script, and plugin APIs through P/Invoke.

The full path looks like this:

```text
Cursor / Claude Desktop / Windsurf / another MCP client
                    |
             HTTP + SSE / Streamable HTTP
                    |
       SimpleMcpServer (in-process HttpListener)
                    |
       [Command] reflection + JSON Schema binding
                    |
        x64dbg Bridge / Script / command engine
                    |
              the debugged Windows process
```

That distinction is important. The model is not reading pixels or OCR output. It receives debugger-native state: register values, loaded modules, threads, call stacks, disassembly, string references, and cross-references. x64dbg's official documentation explicitly supports automation through plugins and Bridge debug functions; `DbgCmdExecDirect`, which this project uses extensively, executes an x64dbg command on the calling thread.

This is best understood as an Agent API added to an existing debugger, not a general computer-use agent learning to operate x64dbg.

---

## 02 | Twenty-six business tools plus Echo: this is not a read-only assistant

After excluding commented declarations and the two lifecycle commands restricted to x64dbg itself, the inspected commit contains **26 MCP-facing business tools**. The server adds a built-in `Echo`, so `tools/list` can expose up to 27 tools. Tools marked `DebugOnly` disappear when there is no active debug session.

The surface falls into four groups:

| Capability | Representative tools | Effective privilege |
|---|---|---|
| State inspection | `GetAllRegisters`, `GetAllActiveThreads`, `GetAllModulesFromMemMap`, `GetCallStack` | Read live debugger and process state |
| Code analysis | `ReadDismAtAddress`, `SearchForStrings`, `FindAllMem`, `refstr`, `FindXrefs` | Search memory and return disassembly, strings, and references |
| Debug control | `LoadBinary`, `run`, `PauseDebug`, `StopDebug`, `RestartDebug`, `StepInto/Over/Out` | Launch a program and alter execution flow |
| Mutation | `SetBreakpoint`, `DeleteBreakpoint`, `WriteMemToAddress`, `CommentOrLabelAtAddress`, `ExecuteDbgCommand`, `DumpModuleToFile` | Patch memory, change debugger metadata, run arbitrary x64dbg commands, or write files |

`ExecuteDbgCommand` is the most consequential escape hatch. If the server lacks a dedicated tool for an operation, the model can still submit an arbitrary x64dbg command string. The named tool list therefore understates the real capability ceiling.

There is also thoughtful Agent-oriented engineering here. `McpParam` supports examples, enums, regex patterns, and numeric bounds. Search results are capped around 50 or 100 entries to protect the model's context window. Several errors give syntax hints that help an LLM correct module names or breakpoint targets. This is more than a handful of methods placed behind an HTTP port; it is an attempt to build a debugger interface that an LLM can navigate and repair its calls against.

![Plugin files and dependencies shown in the upstream README](imgs/x64dbg-mcpserver-ai-debugger-source-audit/plugin-ui.png)

---

## 03 | How the MCP layer works: lightweight and direct, with more security responsibility

The server does not use ASP.NET Core or Kestrel. It creates a raw `System.Net.HttpListener` inside the plugin process. `SimpleMcpServer` reflects over `[Command]` methods, prebuilds tool definitions and input schemas, and handles:

- `initialize`;
- `tools/list` and `tools/call`;
- `prompts/list` and `resources/list`;
- long-lived SSE and modern Streamable HTTP;
- a 15-second SSE heartbeat;
- a compatibility path for legacy `rpc.discover`.

The implementation advertises MCP protocol version `2025-11-25`. Cursor can connect directly to the SSE URL. For Claude Desktop and Windsurf, the README still recommends the author's separate `MCPProxy-STDIO-to-SSE` bridge because direct SSE has previously hit context-deadline timeouts.

This approach keeps deployment compact: the plugin and its DLLs live beside the debugger, with no separate Web host. It also means authentication, binding, CORS, request concurrency, debugger-thread rules, and lifecycle management all have to be correct inside the plugin itself.

---

## 04 | The main problem is not MCP; it is the default trust boundary

The code already contains Bearer-token validation and performs a constant-time comparison. The problem is that **the actual plugin startup path never supplies a token**.

It constructs the server as:

```csharp
new SimpleMcpServer(typeof(DotNetPlugin.Plugin), GMcpServerConfig)
```

That overload is explicitly documented in the source as disabling authentication and forwards `bearerToken: null` to the full constructor. The persisted configuration contains only an IP address and a port. No other startup path inspected here wires a secret into the server.

The default network configuration compounds the issue:

- `IpAddress` defaults to `+`, and the port defaults to `50300`;
- `HttpListener` therefore registers `http://+:50300/`, which can bind across hostnames and interfaces rather than loopback only;
- responses include `Access-Control-Allow-Origin: *`;
- transport is plain HTTP;
- the README suggests granting a wildcard URL ACL to `Everyone` on Windows;
- yet `GetDisplayUrl()` converts `+` into `127.0.0.1`, making the displayed URL look loopback-only.

Put together, the default state may expose a service capable of launching programs, controlling execution, patching process memory, running arbitrary debugger commands, and writing files to the local network without active authentication, while its displayed URL encourages the user to believe it is local-only.

The upstream README itself acknowledges under Known Issues that the compiled build listens on all IPs and says a future release should move to `127.0.0.1`. For the current version, that is a deployment blocker, not a minor hardening suggestion.

---

## 05 | The most serious behavior mismatch: “dump module” first patches the target

`DumpModuleToFile` is described as writing the current module's registers and disassembly to a text report. Its name implies “read debugger state, then write a report.” Before opening the report, however, the implementation runs this code:

```csharp
IntPtr ptr = new IntPtr(0x14000140B);
byte[] nops = Enumerable.Repeat((byte)0x90, 7).ToArray();
bool success = WriteMemory(address, nops);
```

It unconditionally attempts to write seven NOP bytes to the fixed address `0x14000140B`. That address almost certainly came from a developer sample and was left in a general-purpose tool path.

The problem is broader than a likely failed write:

- another target may have mapped memory at that address and be silently modified;
- neither the tool name nor its description warns the client about mutation;
- the file argument accepts an absolute path and opens it in overwrite mode;
- none of the business tools sets `readOnlyHint`, `destructiveHint`, `idempotentHint`, or `openWorldHint`, so clients receive no per-tool risk classification.

The MCP project's own guidance stresses that Tool Annotations are hints, not an enforcement boundary. Even so, omitting them from a high-privilege server weakens the client's opportunity to present confirmation and approval UI.

The hard-coded patch should be removed from `DumpModuleToFile`. If patching is intentional, it belongs in a separately named, explicitly parameterized tool that requires human confirmation by default.

---

## 06 | Maturity: successful builds do not validate the debugger workflow

The inspected head was merged on October 4, 2026, in PR #41, which added debug-lifecycle tools and fixed a menu-icon crash. GitHub Actions shows successful x64 and x86 Windows builds for that exact commit. The project targets the classic Windows-only `.NET Framework 4.7.2` and uses DllExport/ILRepack to produce x64dbg-compatible plugin artifacts.

No test project or test source was found in the repository. The two workflows restore, build, and upload artifacts; they do not launch x64dbg, load the plugin, connect an MCP client, attach a sample process, and verify the tool results end to end.

Other early-project signals remain visible:

- the README says not every command is fully implemented;
- some documented command names no longer match the current code;
- commands such as `run` use fixed delays of 250 milliseconds or several seconds rather than a complete event-driven wait model;
- the repository root has no `LICENSE` file, and GitHub reports no detected license, so public source visibility does not itself grant permission to copy, modify, or redistribute the code.

**This audit was performed on macOS. It verified Git history, source, tool declarations, configuration, CI records, and official screenshots, but it did not run x64dbg on Windows, load the plugin, or connect a live MCP client.** The architecture and risky code paths are confirmed; production-ready debugger behavior is not independently validated here.

![Early MCP client and x64dbg plugin-menu example from the upstream README](imgs/x64dbg-mcpserver-ai-debugger-source-audit/command-output.png)

---

## 07 | What would make it a more trustworthy debugging Agent

The highest-priority work is clear:

1. Bind to `127.0.0.1` by default and make the displayed URL match the real listener exactly.
2. Wire the existing Bearer-token implementation into configuration, require authentication by default, and support rotation.
3. Add accurate read-only, destructive, idempotent, and open-world annotations to every tool.
4. Separate inspection tools from execution and mutation capabilities, exposing only the read-only set by default.
5. Require human confirmation and durable audit logs for memory writes, binary loading, arbitrary commands, and file output.
6. Delete the hard-coded NOP patch from `DumpModuleToFile` and constrain its output directory.
7. Replace fixed sleeps with debugger events and explicit states for “run until break” and “wait for module.”
8. Add Windows end-to-end tests covering plugin load, tool discovery, sample launch, breakpoints, stepping, reads, denied writes, disconnects, and reconnects.
9. Add an explicit license so users do not confuse public visibility with permission to redistribute.

Until then, a responsible evaluation should use only software the operator owns or is authorized to analyze, inside an isolated Windows VM with disposable samples. Keep the service loopback-only, block bridged networking, avoid wildcard administrator URL bindings, and verify memory, breakpoints, and execution state manually in x64dbg after each Agent action.

---

## 08 | Conclusion: it proves the value of an Agent debugger and why permissions cannot be an afterthought

x64DbgMCPServer's strongest contribution is moving “AI debugging” from visual button clicking into the debugger's internal semantics. A model can query registers, modules, threads, call stacks, strings, cross-references, and disassembly, then set breakpoints, step, and resume execution. That structured loop is genuinely better suited to reverse engineering and complex failure analysis than generic computer control.

It also demonstrates a recurring Agent-tooling mistake: maximizing what the model can do before deciding who may call it, where it is exposed, which actions require approval, and whether a tool's description matches its real side effects. That delay may be an inconvenience for a read-only file tool. For a tool that can patch a live process, it is the security boundary.

The most accurate assessment is therefore neither “AI has taken over x64dbg” nor “this is only a concept demo.” **It is a real, direct, high-privilege debugger bridge. Precisely because the bridge is real, authentication, network isolation, capability separation, and behavioral honesty must come before a larger tool list.**

---

## Primary sources

- [The supplied donghaozhang/x64DbgMCPServer fork](https://github.com/donghaozhang/x64DbgMCPServer)
- [Upstream AgentSmithers/x64DbgMCPServer](https://github.com/AgentSmithers/x64DbgMCPServer)
- [Audited commit `a8303d7`](https://github.com/AgentSmithers/x64DbgMCPServer/commit/a8303d7ac7bfd251b9da83b80c9d1d4407ddd8df)
- [Plugin startup selects the no-token server constructor](https://github.com/AgentSmithers/x64DbgMCPServer/blob/a8303d7ac7bfd251b9da83b80c9d1d4407ddd8df/DotNetPlugin.Impl/Plugin.Commands.cs#L89-L105)
- [Default IP, port, and displayed URL](https://github.com/AgentSmithers/x64DbgMCPServer/blob/a8303d7ac7bfd251b9da83b80c9d1d4407ddd8df/DotNetPlugin.Impl/McpServerConfig.cs#L11-L65)
- [Server construction, Bearer token, and listener prefix](https://github.com/AgentSmithers/x64DbgMCPServer/blob/a8303d7ac7bfd251b9da83b80c9d1d4407ddd8df/DotNetPlugin.Impl/MCPServer.cs#L194-L245)
- [CORS and authorization implementation](https://github.com/AgentSmithers/x64DbgMCPServer/blob/a8303d7ac7bfd251b9da83b80c9d1d4407ddd8df/DotNetPlugin.Impl/MCPServer.cs#L549-L589)
- [Hard-coded NOP write in `DumpModuleToFile`](https://github.com/AgentSmithers/x64DbgMCPServer/blob/a8303d7ac7bfd251b9da83b80c9d1d4407ddd8df/DotNetPlugin.Impl/Plugin.Commands.cs#L3296-L3353)
- [Official x64dbg plugin documentation](https://help.x64dbg.com/en/latest/developers/plugins/)
- [x64dbg documentation for `DbgCmdExecDirect`](https://help.x64dbg.com/en/latest/developers/functions/debug/DbgCmdExecDirect.html)
- [Official MCP blog: Tool Annotations are risk hints, not enforcement](https://blog.modelcontextprotocol.io/posts/2026-03-16-tool-annotations/)
- [x64 Windows build record](https://github.com/AgentSmithers/x64DbgMCPServer/actions/runs/37189335491/job/111398057141)
- [x86 Windows build record](https://github.com/AgentSmithers/x64DbgMCPServer/actions/runs/37189335490/job/111398057104)

*Audit date: October 7, 2026. This article discusses authorized software debugging and security research only. The code and defaults may change; all findings correspond to commit `a8303d7ac7bfd251b9da83b80c9d1d4407ddd8df`.*
