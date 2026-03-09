# OpenAI CUA: Teaching AI to Use Computers Like Humans

> A deep dive into OpenAI's Computer-Using Agent and the GPT-5.4 sample app

## What is CUA?

CUA (Computer-Using Agent) is OpenAI's model for autonomous computer interaction. The core idea is deceptively simple: **let AI see the screen, move the mouse, and type on the keyboard** — just like a human would, instead of calling application-specific APIs.

Traditional AI agents need custom API integrations for every app. CUA takes a fundamentally different approach — it processes raw screen pixels, understands GUI elements (buttons, menus, text fields), and operates through a virtual mouse and keyboard. In theory, **anything a human can use, CUA can use**.

CUA originally powered OpenAI's [Operator](https://operator.chatgpt.com/) product and is now available to developers through the Responses API.

## The CUA Agent Loop

CUA operates through an iterative perception-reasoning-action cycle:

- **Perception**: Screenshots capture the current screen state, giving the model a visual snapshot
- **Reasoning**: Chain-of-thought reasoning determines the next steps, considering current and past screenshots and actions
- **Action**: The model performs clicks, scrolls, or keystrokes until the task is complete or user input is needed

This loop repeats until the model determines the task is done. For sensitive operations (logins, CAPTCHAs), CUA proactively asks for user confirmation.

## The GPT-5.4 CUA Sample App

[openai-cua-sample-app](https://github.com/donghaozhang/openai-cua-sample-app) is a TypeScript implementation demonstrating how to build browser-focused CUA workflows with GPT-5.4.

### Architecture

The project uses a pnpm monorepo structure:

- **apps/demo-web** — Next.js operator console for starting runs, viewing screenshots, and reviewing replay artifacts
- **apps/runner** — Fastify HTTP service managing workspaces, browser sessions, SSE streaming, and replay bundles
- **packages/runner-core** — Core orchestration: the Responses loop, scenario executors, and verification logic
- **packages/browser-runtime** — Playwright browser session abstraction
- **packages/scenario-kit** — Scenario manifests and prompt defaults
- **packages/replay-schema** — Shared contracts for requests, responses, replays, and errors
- **labs/** — Static lab templates copied into isolated run workspaces

### Two Execution Modes

The app supports two distinct modes of browser interaction:

- **native mode**: Exposes the Responses API's `computer` tool directly. The model issues raw click, drag, type, wait, and screenshot commands executed against the live browser
- **code mode**: Exposes a persistent Playwright JavaScript REPL via `exec_js`. The model writes JS code to script the browser rather than emitting raw mouse/keyboard actions

Both modes share the same scenario manifests and replay pipeline.

### Core Code: The Responses Loop

The heart of CUA lives in `packages/runner-core/src/responses-loop.ts`. Here's a simplified flow:

```typescript
// 1. Create OpenAI client
const client = new OpenAI({ apiKey });

// 2. Define tools
// Native mode
const tools = [{ type: "computer" }];
// Or code mode
const tools = [{
  type: "function",
  name: "exec_js",
  description: "Execute JavaScript in a persistent Playwright REPL.",
  parameters: {
    properties: {
      code: { type: "string", description: "JS to execute..." }
    },
    required: ["code"]
  }
}];

// 3. Iterative loop
for (let turn = 0; turn < maxResponseTurns; turn++) {
  const response = await client.responses.create({
    model: "gpt-5.4",
    instructions: systemPrompt,
    input: conversationHistory,
    tools,
  });

  // Handle computer_call (native mode)
  if (hasComputerCall(response)) {
    await executeActions(response.actions); // clicks, typing, etc.
    const screenshot = await page.screenshot();
    conversationHistory.push(screenshotAsInput(screenshot));
  }

  // Handle function_call (code mode)
  if (hasFunctionCall(response, "exec_js")) {
    const result = await executeInRepl(response.arguments.code);
    conversationHistory.push(functionResult(result));
  }

  // If model returns a message (no tool calls), task is done
  if (isMessageOnly(response)) break;
}
```

Key design decisions:
- Screenshot feedback after every turn so the model sees the result of its actions
- `computer_call` batches multiple actions per turn (click, type, keypress), executed together then screenshotted
- 120ms default delay between actions to mimic human pacing
- 20-second timeout on tool execution
- Abort signal support for graceful cancellation

### Built-in Scenarios

The app ships with three demo scenarios:

- **kanban-reprioritize-sprint** — Drag-and-drop reordering on a kanban board, testing stateful UI manipulation
- **paint-draw-poster** — Canvas drawing, testing precise cursor control
- **booking-complete-reservation** — Multi-step form completion with verification against a local confirmation record

Each scenario has deterministic verification — these are structured labs, not open-ended web browsing.

### Getting Started

```bash
git clone https://github.com/donghaozhang/openai-cua-sample-app
cd openai-cua-sample-app
corepack enable
pnpm install
cp .env.example .env
# Edit .env and set OPENAI_API_KEY

pnpm playwright:install    # Install Chromium
pnpm dev                   # Start dev server
# Open http://127.0.0.1:3000
```

Requirements:
- Node.js 22.20.0
- pnpm 10.26.0
- Playwright Chromium

Key environment variables:
- `OPENAI_API_KEY` — required
- `CUA_DEFAULT_MODEL` — defaults to `gpt-5.4`
- `CUA_RESPONSES_MODE` — `auto`, `fallback`, or `live`
- `NEXT_PUBLIC_CUA_DEFAULT_MAX_RESPONSE_TURNS` — defaults to 24

## CUA vs Anthropic Computer Use

OpenAI's CUA and Anthropic's Computer Use are the two leading approaches to "AI controlling computers." They share the same core idea (see screen → reason → act) but differ significantly in implementation:

**Model & Product**
- OpenAI CUA: Built on GPT-4o vision + reinforcement learning, delivered via Operator and the Responses API
- Anthropic: Built on Claude 3.5 Sonnet, delivered via the Messages API with `computer_20241022` tool type

**API Design**
- OpenAI: `computer` tool is a first-class type; actions are batched (multiple actions per turn)
- Anthropic: Each `tool_use` block returns a single action (`mouse_move`, `click`, `type`, etc.), requiring more round trips

**Runtime Environment**
- This sample app uses Playwright for browser management, supporting both headless and headful modes
- Anthropic's reference implementation runs a full desktop environment in Docker with VNC

**Benchmark Performance**
- CUA achieves 38.1% on OSWorld (Anthropic's previous SOTA: 22.0%)
- CUA achieves 58.1% on WebArena
- CUA achieves 87.0% on WebVoyager

**Safety**
- Both emphasize avoiding high-stakes environments
- CUA has `pending_safety_checks` that can pause before sensitive actions
- Anthropic relies on safety guidance in system prompts

**Developer Experience**
- OpenAI's sample is a well-structured TypeScript monorepo with scenario system and replay capabilities
- Anthropic's sample is Python-based, simpler and more direct, with Docker one-click setup

## What This Means

CUA represents a new paradigm for AI interaction: instead of writing API integrations for every application, AI uses the same interfaces humans do. This has enormous potential for test automation, RPA, accessibility, and more.

The current limitations are real though:
- **Slow** — every step requires screenshot capture, image transmission, and inference
- **Expensive** — massive token consumption on image processing
- **Unreliable** — complex task success rates remain well below human levels (OSWorld: 38% vs human 72%)
- **Risky** — giving AI computer control is inherently high-stakes

The value of this sample app is that it demonstrates a **complete, production-grade architecture** for CUA workflows — from API calls and browser management to event streaming and replay verification. All the critical pieces have reference implementations.

For developers looking to explore AI computer-use capabilities, this is one of the best starting points available today.

---

*2026-03-09*

🦞
