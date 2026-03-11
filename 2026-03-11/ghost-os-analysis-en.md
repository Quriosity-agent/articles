# Ghost OS Technical Analysis: Making AI Agents Actually Use Your Computer

Repository: <https://github.com/donghaozhang/ghost-os>

Ghost OS is an open-source **macOS computer-use runtime** for AI agents. Instead of keeping agents trapped inside a chat box, it exposes desktop interaction through MCP tools so Claude Code, Cursor, VS Code, and other MCP clients can operate real apps.

The key point: Ghost OS is not “just screenshot clicking.” It combines:

1. **Accessibility tree first (AX-first)** for structured UI understanding
2. **CDP + local VLM fallback** for hard web app cases
3. **Recipe replay** to convert one-time reasoning into repeatable workflows

---

## 1) What Ghost OS Is (Product Positioning)

From the codebase (`Sources/GhostOS/*`, `vision-sidecar/server.py`), Ghost OS is best understood as a **computer-use execution layer**, not a full agent framework.

- Northbound: MCP tool surface (`MCPServer.swift`, `MCPTools.swift`)
- Southbound: macOS AX APIs, input injection, window control, screenshots
- Side channel: Python sidecar with local ShowUI-2B grounding
- Memory/automation layer: JSON recipes (`RecipeEngine.swift`, `recipes/*.json`)

In practical terms, Ghost OS gives agent builders a stable runtime for “do this in real UI,” not just “plan this in text.”

---

## 2) Core Architecture

### 2.1 MCP control plane: synchronous and reliability-focused

- Stdio JSON-RPC server with both Content-Length and NDJSON transport support
- Global AX timeout is explicitly set (`AXTimeoutConfiguration.setGlobalTimeout(5.0)`) to avoid indefinite AX hangs
- Tool dispatch and result formatting are centralized (`MCPDispatch.swift`)

This is a deliberate reliability choice: fail fast with context, instead of hanging forever.

### 2.2 Perception: AX-first with semantic depth tunneling

`Perception.swift` provides `ghost_context/state/find/read/inspect/...` with layered strategies:

- AX tree search as default path
- Semantic-depth tunneling to traverse deep web trees without paying depth cost for empty layout containers
- DOM-id-based lookup for web controls when available
- CDP fallback (`CDPBridge.swift`) and then vision fallback (`VisionPerception`)

This hybrid is a major strength: structured semantics first, pixels only when needed.

### 2.3 Actions: native AX operations first, synthetic input fallback

`Actions.swift` follows a consistent action loop:

1. Locate target
2. Try AX-native operation (`AXPress`, `AXValue`, etc.)
3. Fallback to synthetic input / coordinate action if needed
4. Verify with readback and waits

The v2.1 additions (`ghost_hover`, `ghost_long_press`, `ghost_drag`, `ghost_annotate`) close many real-world gaps in desktop automation.

### 2.4 Vision sidecar: local grounding service

`vision-sidecar/server.py` provides:

- `/ground` (implemented): find one element coordinate via ShowUI-2B
- `/detect` and `/parse` (currently placeholders)

So the current vision stack is strongest at **single-target grounding**, not full-screen dense UI detection.

### 2.5 Recipe engine: workflow compilation and replay

`RecipeEngine.swift` + `RecipeStore.swift` + bundled recipes implement:

- Parameter substitution (`{{param}}`)
- Preconditions
- Step execution with `wait_after`
- Failure policies (`stop` / `skip`)
- Structured step results and diagnostics

This is where Ghost OS becomes operationally scalable: first solve, then replay cheaply and reliably.

---

## 3) Execution Workflow in Practice

A typical loop for a multi-step task:

1. `ghost_recipes` to discover existing workflows
2. `ghost_run` if recipe exists
3. Execute typed steps (click/type/press/hotkey/wait)
4. Fall back from AX → CDP → VLM when necessary
5. Return structured step-level outcomes

This lowers recurring model cost because not every run requires deep planning.

---

## 4) Target Users and Practical Use Cases

### Target users

- Builders shipping MCP-enabled AI products
- Teams automating cross-app desktop workflows
- Users requiring local execution and data control

### Good use cases

- Cross-app automation (browser + Slack + Finder)
- Repeatable operational tasks (emailing, downloading, filing)
- Turning expert interaction sequences into shareable recipe assets

---

## 5) Practical Comparison with Adjacent Ecosystems

### vs Anthropic Computer Use / Operator-style screenshot-first systems

Ghost OS advantages:
- Structured AX semantics improve explainability and debugging
- Local-first architecture improves privacy/control
- Recipe layer enables workflow reuse

Screenshot-first systems advantage:
- More uniform cross-platform interaction model

Takeaway: Ghost OS is more “macOS-native engineering runtime,” less “universal pixel bot.”

### vs Playwright/browser-only automation

Playwright is excellent for web apps but does not solve native desktop app workflows. Ghost OS explicitly targets both browser and native macOS contexts.

### vs OpenClaw browser automation ecosystems

OpenClaw excels in browser control pipelines; Ghost OS extends to full macOS UI via AX. They are complementary depending on task boundaries.

---

## 6) Strengths Observed in the Repo

1. **Clear modular architecture** across MCP/perception/action/vision/recipes
2. **Strong diagnostics and setup UX** (`ghost setup`, `ghost doctor`)
3. **Reliability engineering details** (AX timeouts, fallback layering, wait primitives)
4. **Local execution path** with no mandatory cloud dependency for grounding
5. **Workflow asset model** through JSON recipes

---

## 7) Current Limitations

1. **Platform scope**: macOS-focused by design
2. **Vision completeness gap**: `/detect` and `/parse` are placeholders today
3. **Web complexity remains hard**: Chrome AX flattening still requires fallback logic
4. **Coordinate/window edge cases**: fullscreen, multi-monitor, minimized windows, Spaces
5. **Recipe drift**: UI changes can break recipes without versioning and tests

---

## 8) Concrete Takeaways for Builders

1. Treat Ghost OS as a **runtime layer**, not your whole agent architecture
2. Use a strict operating pattern: `ghost_context` → action → `ghost_wait`
3. Prefer DOM-id/CDP when available in web flows; use VLM grounding as escalation
4. Build recipe regression checks for critical business workflows
5. Keep failure context logs (window/app/url/step) as first-class telemetry

---

## Final Verdict

Ghost OS is a strong implementation of a practical idea: agentic computer use should be **structured, debuggable, and reusable**.

Its core bet—AX-first perception plus local visual fallback plus recipe replay—is technically sound for serious desktop automation on macOS.

For builders trying to move from “agent demos” to “reliable cross-app execution,” Ghost OS is a very useful reference architecture and runtime foundation.

🦞
