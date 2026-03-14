# Embedding an AI Agent in QCut: Anthropic Claude SDK vs Pi Mono

> QCut is a video editor. We want users to edit video with natural language. Which SDK should we pick?

## Context

QCut is an Electron + React video editor with:
- **87+ CLI commands** with JSON output and session mode
- **19 Claude Code Skills** in `.agents/skills/`
- Full TypeScript codebase

Goal: let end users (no Claude Code / Codex installed) give natural language commands inside QCut to edit video.

## The Candidates

| Dimension | Anthropic Claude SDK | Pi Mono |
|-----------|---------------------|---------|
| **Package** | `@anthropic-ai/sdk` | `badlogic/pi-mono` (7 sub-packages) |
| **License** | MIT | MIT |
| **Stars** | ~15K | ~23.6K |
| **Maintainer** | Anthropic (official team) | Mario Zechner (solo) |
| **Model support** | Claude only | All providers (OpenAI, Google, Anthropic, local, etc.) |
| **What you get** | API client + Tool Calling | Unified LLM API + Agent Runtime + TUI + Web UI |
| **Agent loop** | Build your own | Built-in |
| **TypeScript** | ✅ Native | ✅ Native |

## 1. Architecture: What You Get vs What You Build

### Anthropic Claude SDK
```
You get:    API calls + Tool Calling protocol
You build:  Agent loop, tool registry, context management, error handling, UI
```

The SDK is an HTTP client. You call `messages.create()`, pass tool definitions, get back `tool_use` blocks, execute them yourself, push results back. The loop is yours.

### Pi Mono
```
You get:    Unified LLM API + Agent Runtime + tool system + TUI/Web UI
You build:  QCut-specific tool adapters, Electron UI integration
```

Pi Mono's equivalent of the Claude SDK is `pi-llm` (unified API), but it also gives you `pi-agent` (agent loop), `pi-tools` (tool registration), even `pi-tui` and `pi-web`.

### Verdict
**Pi Mono gives you more, you build less.** But "more" also means more dependencies and more abstractions to understand.

## 2. Model Flexibility

This is the biggest divergence.

- **Claude SDK**: Locked to Claude. Opus is expensive ($15/M input), Haiku is cheap but limited.
- **Pi Mono**: Same code runs Claude / GPT / Gemini / local models. Users choose.

**For QCut:** A video editing agent needs strong reasoning (understand intent → decompose into CLI command sequences), but also cost control. Multi-provider support lets you route simple tasks ("add a subtitle") to cheap models and complex tasks ("recut this for better pacing") to strong ones.

## 3. Agent Loop Complexity

**Claude SDK approach:**
```typescript
// You write this loop yourself
while (true) {
  const response = await client.messages.create({ tools, messages });
  if (response.stop_reason === 'end_turn') break;
  for (const block of response.content) {
    if (block.type === 'tool_use') {
      const result = await executeTool(block.name, block.input);
      messages.push({ role: 'assistant', content: [block] });
      messages.push({ role: 'user', content: [{ type: 'tool_result', tool_use_id: block.id, content: result }] });
    }
  }
}
```
Looks simple, but production code needs: parallel tool calls, error recovery, context window truncation, token accounting, streaming. ~500-1000 lines of real code.

**Pi Mono approach:**
```typescript
const agent = createAgent({ model: 'claude-sonnet-4-20250514', tools: qcutTools });
const result = await agent.run('Lower the volume of the second clip by 50%');
```
Loop, retry, context management all built-in. You focus on writing QCut tool definitions.

## 4. Maintenance Risk

This is Pi Mono's biggest weakness.

| Risk | Claude SDK | Pi Mono |
|------|-----------|---------|
| Maintainer count | Anthropic team (dozens) | Mario Zechner (1) |
| Corporate backing | Anthropic ($600B+ valuation) | None |
| Abandonment risk | Very low | Medium-high |
| API change response | Immediate | Depends on Mario's availability |
| Security patches | Guaranteed | Uncertain |

**23.6K stars ≠ stability.** Solo projects get abandoned all the time. QCut is a commercial product—this risk matters.

## 5. Integration with QCut CLI

QCut has 87+ CLI commands with JSON output. Both approaches integrate the same way:

```typescript
// Tool registration is identical for both
const tools = [
  {
    name: 'qcut_add_subtitle',
    description: 'Add subtitle at specified timestamp',
    parameters: { text: 'string', startTime: 'number', duration: 'number' },
    execute: async (params) => {
      return await exec(`qcut subtitle add --text "${params.text}" --start ${params.startTime} --duration ${params.duration} --json`);
    }
  }
];
```

**Integration difficulty is the same.** The difference is in the layer above (agent loop), not the tool layer.

## 6. Cost

API costs are pure pass-through for both approaches:

| Model | Input $/M tokens | Output $/M tokens |
|-------|------------------|-------------------|
| Claude Opus 4 | $15 | $75 |
| Claude Sonnet 4 | $3 | $15 |
| Claude Haiku 3.5 | $0.80 | $4 |
| GPT-4.1 | $2 | $8 |
| Gemini 2.5 Pro | $1.25 | $10 |
| Gemini 2.5 Flash | $0.15 | $0.60 |

**Multi-provider = more room for cost optimization.** Simple tasks on Flash/Haiku, complex tasks on Sonnet/4.1.

## 7. What Else Is Out There?

| Option | Strength | Weakness |
|--------|----------|----------|
| **OpenRouter API** | Unified API, 50+ models | Just API routing, agent loop is yours |
| **Vercel AI SDK (`ai`)** | Mature, multi-provider, great streaming | Web-oriented, agent loop support is basic |
| **Roll your own** | Full control | Significant effort, reinventing wheels |

**Vercel AI SDK** deserves serious consideration—more providers than Claude SDK, more stable than Pi Mono (Vercel team maintains it), and the Next.js ecosystem is Electron-friendly.

## Recommendation

**For QCut's specific situation, a two-phase approach:**

### Short-term (MVP): Anthropic Claude SDK + lightweight custom agent loop
- QCut already has 19 Claude Code Skills; team knows the Claude ecosystem
- Agent loop code is manageable (~500 lines) and fully under your control
- Validate the product experience with Sonnet 4 first; multi-model isn't needed yet

### Medium-term (productionize): Migrate to Vercel AI SDK
- When you need multi-model support and cost optimization, swap to the `ai` package
- API layer replacement cost is low (tool definitions stay the same)
- Vercel team maintains it; stability is guaranteed

### Not recommended: Pi Mono
- Despite having the most features, solo-maintainer risk is too high
- QCut is a commercial product; you can't bet on one person's enthusiasm

---

*Tech selection is always about tradeoffs. Shipping something that works beats spending six months picking the "best" option.* 🦞
