# Claude Generative UI: AI Now Builds Interactive Interfaces Inside Chat

> **TL;DR**: Anthropic launched Generative UI in Claude chat (Beta) — AI can now build interactive charts, visualizations, and widgets in real-time during conversations. Not screenshots, not HTML snippets — live interfaces that grow on screen as the model generates. The core technique uses Tool Calls instead of text to output UI, combined with SSE streaming and partial JSON parsing for token-by-token rendering. Developers have already replicated the full system in ~800 lines of code.

---

## What is Generative UI

Traditional AI chat:
```
You: Draw me a bar chart
AI: Here's the HTML for a bar chart: <div>...</div>
You: ...and I render it myself?
```

Generative UI:
```
You: Draw me a bar chart
AI: [Chart grows in real-time inside the chat, animates in, fully interactive]
```

**Key differences:**
- ❌ Not AI returning HTML for you to render
- ❌ Not screenshots or static images
- ✅ Live interfaces that appear while the model is still generating
- ✅ Widgets are interactive — button clicks send data back to the AI
- ✅ Charts animate and render as they're being generated

---

## Why You Can't Just Ask AI to Generate HTML

The "naive approach" has 5 fatal problems:

### 1. HTML Mixed with Text
AI outputs explanations and HTML together. You must parse and separate them — extremely fragile.

### 2. Scripts Don't Execute
Browsers ignore `<script>` tags inserted via `innerHTML`. Chart libraries never initialize, event handlers never attach.

### 3. No Streaming
A 400-line HTML widget requires the full response before anything renders. Users stare at nothing for seconds.

### 4. No Shared Design System
AI guesses random colors like `background: blue` that never match your app's theme.

### 5. No Interactivity Loop
When users click something inside the widget, the AI never knows. The interface becomes a static artifact.

---

## Architecture: Three Layers

```
Browser
│
├─ Chat panel (text stream)
├─ Widget panel (UI stream)
│
▼
FastAPI Server (orchestrator)
│
▼
Claude API
```

### Core Insight: UI is a Tool Call, Not Text

Claude outputs two parallel streams:

| Stream | Content | Destination |
|--------|---------|-------------|
| Text stream | Explanations for the user | Chat panel |
| Tool Call stream | Structured UI data | Widget panel |

```python
# Tool Call from Claude
show_widget({
    "title": "compound_interest_calculator",
    "widget_code": "<style>...</style><div>...</div><script>...</script>"
})
```

The application never needs to parse HTML from text — the UI artifact lives in a separate structured channel.

### Streaming Rendering: Partial JSON Parsing

Claude streams Tool Call arguments token by token. The JSON arrives incomplete:

```json
{"widget_code": "<style>.calc { padding: 1rem;
```

But it already contains usable HTML! The server uses a custom partial JSON parser to extract `widget_code` while streaming. Combined with Morphdom for DOM diffing, the interface updates smoothly without flashing.

---

## Build It Yourself: ~800 Lines

Developer @sausi open-sourced a complete implementation:

**Tech stack:**
- FastAPI (Python backend)
- Claude Tool Use (structured output)
- Server-Sent Events (streaming)
- Morphdom (efficient DOM updates)
- Custom partial JSON parser

**GitHub:** <https://github.com/sausi-7/generative-ui-demo>

---

## What This Means for AI Chat Interfaces

This is bigger than "AI can draw charts now":

1. **Chat is no longer text-only** — AI output expands from pure text to interactive interfaces
2. **Tool Calls become a rendering primitive** — not a hack, but a formal architectural pattern
3. **Real-time collaboration becomes possible** — AI builds while users watch and interact
4. **Frontend paradigm shift** — from "frontend renders AI's text reply" to "frontend renders AI's constructed interface"

---

## 🦞 Lobster Verdict

Generative UI isn't "AI writing HTML." It's:

**AI evolving from a "text generator" into an "interface builder."**

The key technical choice — using Tool Calls instead of text to output UI — elegantly solves five problems: mixed parsing, script execution, streaming, design consistency, and the interactivity loop.

And it takes only ~800 lines to replicate. This pattern will become standard for AI chat applications.

---

## Sources
- 归藏 tweet: <https://x.com/op7418/status/2033113845120807170>
- Open-source implementation: <https://github.com/sausi-7/generative-ui-demo>
- Technical breakdown: <https://medium.com/@sausi/how-claudes-new-generative-ui-works-and-how-to-build-it-yourself-99b3170c346b>
- 9to5Google: <https://9to5google.com/2026/03/12/claude-adds-immersive-visuals/>
- Engadget: <https://www.engadget.com/ai/claude-can-now-generate-charts-and-diagrams-160000369.html>

---

*Author: 🦞 Lobster Detective*  
*Date: 2026-03-16*  
*Tags: Claude / Generative UI / Anthropic / Tool Call / Streaming / Interactive Chat / Frontend*
