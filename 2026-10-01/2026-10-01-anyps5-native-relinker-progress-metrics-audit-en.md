# AnyPS5 Source Audit: “Native” Does Not Mean Zero Translation, and 52%/76% Are Not Game Completion

> **Bottom line:** The screenshot shared by RedGamingTech is authentic. Running AnyPS5's own progress tool on the source snapshot immediately before the post reproduces `2301/3008 (76.5%)` declared system-library functions and `609/1166 (52.23%)` recognized GPU instructions. Those numbers are not “percent of PS5 emulated” or “percent of games that run.” AnyPS5 rewrites PS5 x86-64 executables into Linux ELF or Windows PE files, binds their imports to reimplemented system libraries, and recompiles RDNA shaders to SPIR-V/Vulkan. It avoids a conventional full-system emulator process, but it still performs substantial binary conversion, platform reimplementation, and graphics translation.

![The AnyPS5 progress screenshot attached to RedGamingTech's post](imgs/anyps5-native-relinker-progress-metrics-audit/redgamingtech-progress-post.jpg)

On October 1, 2026, [RedGamingTech posted](https://x.com/RedGamingTech/status/2105623011235934545) that AnyPS5 had mapped just over half of the GPU instructions and completed more than 75% of its system library, allowing PS5 games to run “natively” on PC “without an emulator.” By the October 9 audit, the post had accumulated roughly 591,000 views and more than 7,800 likes.

The framing is compelling, but it compresses three different questions: **Is the original PS5 executable still being run? At which layer is execution native? What do the two percentages actually count?**

---

## 01 | The Two Numbers Reproduce Exactly from the Post-Date Source

I checked out [`cc3d2d2`](https://github.com/boykopovar/AnyPS5/tree/cc3d2d21efef2d06c6a2f29d2eb0bc31eb1b10b6), the nearest repository commit before the post, and ran the project's own `tools/progress.py`:

| Metric | Done | Current inventory | Percentage |
|---|---:|---:|---:|
| Declared system-library functions | 2301 | 3008 | 76.50% |
| Catalogued RDNA GPU instructions | 609 | 1166 | 52.23% |

Every value matches the screenshot. The issue is therefore not whether the image was fabricated; it is how its denominators should be read.

The library total includes only functions that AnyPS5 had already declared under `core/libs/prx`. It is not the total number of functions exported by PS5 firmware, and it grows as the project discovers and declares more functions. The GPU total comes from the project's AMD RDNA 1 + RDNA 2 instruction catalog. An instruction moves to the completed side when the decoder recognizes it.

This is a **source-inventory dashboard**, not a **game-compatibility dashboard**.

---

## 02 | Why AnyPS5 Says It Is Not an Emulator

![Execution architecture redrawn from the AnyPS5 source](imgs/anyps5-native-relinker-progress-metrics-audit/anyps5-architecture-audit.svg)

The PS5 and mainstream PCs both use x86-64 CPUs. That gives AnyPS5 an option conventional console emulators do not always have. Its relinker reads a clean PS5 ELF supplied by the user and the PRX modules bundled with that game, then:

1. parses ELF structures, NID imports, dynamic sections, and syscalls;
2. rebuilds the container as a host-loadable Linux ELF or Windows PE;
3. optionally lowers supported AMD-only x86 instructions with `--to-intel`;
4. binds imports to replacement PRX shared libraries built by AnyPS5; and
5. lets the host operating system load the resulting executable.

At the process-model level, the project's claim is meaningful. It does not boot a virtual PS5, and it does not place a separate emulator process around a CPU instruction interpreter. The converted title is a normal host process, and much of its x86-64 code executes directly on the CPU.

But “native” must not be expanded into “the untouched PS5 file runs directly.” The container, imports, dynamic linking, and some CPU instructions are rewritten ahead of time. PS5 system calls and library behavior are reimplemented. Graphics commands and shaders pass through a separate translation pipeline.

The more precise label is **ahead-of-time relinking plus a compatibility layer**. It is not conventional full-system emulation, but it is not zero translation.

---

## 03 | The GPU Path Is Where the “Native” Label Becomes Especially Incomplete

AnyPS5 consumes PS5 AGC/PM4 command streams, reconstructs state, draws, and compute dispatches, then sends RDNA shaders through this pipeline:

`RDNA decode -> control-flow graph and structurization -> IR -> optimization -> SPIR-V -> Vulkan`

This is one of the hardest parts of the compatibility system. A shared CPU ISA does not make PS5 graphics APIs, resource descriptors, synchronization semantics, or Vulkan equivalent.

“52.23% GPU instructions” means the progress scanner found matching decoder coverage. It does not establish that:

- every operand form, format, dimension, and boundary case is correct;
- the shader can always be translated into valid SPIR-V;
- translated results numerically match PS5 hardware;
- resource state, synchronization, and pipeline combinations work in games; or
- performance, rendering correctness, and driver behavior are solved.

The project's own `TechnicalDebt.md` is candid. Some decoded instructions still throw for unsupported texture formats, filtering modes, indirect descriptors, cube boundaries, dynamic control flow, or storage variants. Other behavior has not been measured on PS5 hardware. **Recognizing an opcode is necessary, but it is not graphics compatibility.**

---

## 04 | “76.5% System Libraries” Does Not Mean 76.5% Behavioral Correctness

At the post-date snapshot, the script counted an `APS5_VABI` definition as implemented whenever its body did not directly call `NotImplemented_nid_no_patch`. The current scanner also recognizes some local stub wrappers and excludes test directories. All other definitions count as done.

That rule is useful for asking how many explicit throwing stubs remain. It cannot establish ABI or behavioral equivalence. The current technical-debt ledger still records boundaries such as:

- signatures borrowed from other compatibility projects but not verified on the console;
- UI calls that return “user canceled” without rendering a UI;
- an HMD path that only represents a disconnected device;
- network, entitlement, voice, and invitation APIs that cover only failure behavior;
- functions with unknown signatures or declarations inferred from a single title; and
- host-specific behavior where only synthetic tests exist.

The dashboard's exact definition of implemented is therefore: **a declared function that the scanner no longer recognizes as an all-throwing stub.** It does not mean the function's ABI, return values, side effects, and behavior across games have all been verified against a PS5.

---

## 05 | Eight Days Later It Reads 84.81% and 100%, but That Is Not a Game-Compatibility Jump

![AnyPS5 progress regenerated from the October 9, 2026 source](imgs/anyps5-native-relinker-progress-metrics-audit/anyps5-progress-2026-10-09.svg)

I regenerated the dashboard at the October 9 audit snapshot, [`6cc0503`](https://github.com/boykopovar/AnyPS5/tree/6cc0503dacc9d9697d23001d4103780ad2e9acba):

| Snapshot | System libraries | GPU instructions |
|---|---:|---:|
| October 1 post snapshot | 2301/3008, 76.50% | 609/1166, 52.23% |
| October 9 audit snapshot | 2573/3034, 84.81% | 1166/1166, 100.00% |

The project is moving remarkably quickly. The counting tool also changed during those eight days: it added opcode aliases and variants, learned function-try-blocks and stub wrappers, excluded test sources, and deduplicated libraries that share source files. The documentation explicitly notes that removing duplicate accounting can change a percentage without adding functionality.

This comparison proves rapid expansion of the code and tracked inventory, plus a rapid reduction in explicit pending entries. By itself, it does not prove that GPU behavior is now 100% correct or that 84.81% of the PS5 catalog is playable.

---

## 06 | The Public Compatibility Evidence Still Contains One Game

The current compatibility table lists one title: the 2D platformer **Dreaming Sarah**. Windows is marked “in game, playable,” with a reported 60 FPS on a GTX 1050 Ti and i5-7500 at 3.4 GHz, and 36 FPS on Intel HD 620 with an i5-7200 at 2.5 GHz. Linux remains a question mark.

That result matters. It shows that the architecture is more than a slide: at least one commercial title has completed a real path through relinking, dynamic-library binding, graphics, and input. A relatively light 2D title cannot be extrapolated to AAA games, complex online services, specialized peripherals, PSN, video decode, VR, shader-heavy engines, or anti-cheat systems.

Users must provide legally obtained clean ELFs and their bundled modules. The project does not distribute games, firmware, keys, or Sony proprietary libraries. Intel hosts may need `--to-intel`, while the documentation says some AMD-only instructions still cannot be lowered. Unsupported paths are generally designed to fail loudly instead of silently fabricating behavior.

---

## 07 | This Is a Real Large-Scale Engineering Project, with a Visible Red CI State

At audit time, AnyPS5 was GPL-2.0 software with roughly 17,600 stars and 1,400 forks. The checkout contained about 275,000 lines of C/C++/Python across more than 1,500 source files. Release `v0.1.1` provides relinker binaries and PRX bundles for Windows and Linux, putting the project beyond a source-only proof of concept.

On macOS, I built the relinker-only configuration and ran **34/34 tests successfully**. That validates current parsing, patching, and synthetic fixtures. It does not validate the full PRX set, Vulkan execution, or a PS5 game.

The GitHub Actions state for the same commit is worth preserving. Relinker jobs passed on macOS, Windows, and Ubuntu. Full Linux and Windows builds failed because a test header could not find `spirv/unified1/spirv.hpp`, so their full test stages never ran. The progress-publication workflow succeeded, but that does not make the complete build green.

This does not invalidate the project. It describes a repository under extremely rapid development. Any percentage should be read alongside a fixed commit, full CI status, the compatibility table, and technical debt rather than as an isolated badge.

---

## 08 | The Most Accurate Reading of the Post

Half of RedGamingTech's framing is correct: AnyPS5 exploits the shared x86-64 architecture to convert a title into a host-loadable process and avoid the central loop of a conventional CPU emulator. That is a technically meaningful compatibility strategy.

The phrase “without an emulator” makes the remaining compatibility work disappear rhetorically, even though it has only moved:

| Work often performed by an emulator | AnyPS5's path |
|---|---|
| Model CPU and system environment | Run most x86-64 directly; lower some AMD-only instructions ahead of time |
| Provide console system APIs | Reimplement PS5 PRX libraries and bind imports by NID |
| Translate graphics APIs and shaders | Recover PM4/AGC state and recompile RDNA shaders to SPIR-V/Vulkan |
| Maintain an emulator runtime | Move conversion into the relinker and let the host OS load the result |

The most accurate one-sentence description is: **AnyPS5 is not a conventional full-system PS5 emulator; it is a project that ahead-of-time relinks PS5 x86-64 programs for PCs and supplies system-library and GPU compatibility layers at runtime. The 52% and 76% figures measure engineering inventory, not game completion.**

---

## Primary Sources

- [RedGamingTech's post](https://x.com/RedGamingTech/status/2105623011235934545)
- [AnyPS5 GitHub repository](https://github.com/boykopovar/AnyPS5)
- [Post-date source snapshot `cc3d2d2`](https://github.com/boykopovar/AnyPS5/tree/cc3d2d21efef2d06c6a2f29d2eb0bc31eb1b10b6)
- [Audited source snapshot `6cc0503`](https://github.com/boykopovar/AnyPS5/tree/6cc0503dacc9d9697d23001d4103780ad2e9acba)
- [Architecture](https://github.com/boykopovar/AnyPS5/blob/6cc0503dacc9d9697d23001d4103780ad2e9acba/docs/dev/ARCHITECTURE.md)
- [Progress counting rules](https://github.com/boykopovar/AnyPS5/blob/6cc0503dacc9d9697d23001d4103780ad2e9acba/docs/dev/PROGRESS.md)
- [Compatibility table](https://github.com/boykopovar/AnyPS5/blob/6cc0503dacc9d9697d23001d4103780ad2e9acba/docs/user/COMPATIBILITY.md)
- [Technical debt](https://github.com/boykopovar/AnyPS5/blob/6cc0503dacc9d9697d23001d4103780ad2e9acba/docs/dev/TechnicalDebt.md)
- [v0.1.1 release](https://github.com/boykopovar/AnyPS5/releases/tag/v0.1.1)
- [GitHub Actions build for the audited commit](https://github.com/boykopovar/AnyPS5/actions/runs/37902713170)

*Audit date: October 9, 2026. Stars, download counts, dashboard values, and CI will continue to change; technical conclusions are pinned to the commits named above. This article covers compatibility research using lawfully obtained software and does not provide games, keys, firmware, or DRM-bypass instructions. The source post image and generated project dashboard are preserved locally; the architecture diagram was redrawn from the fixed source snapshot.*
