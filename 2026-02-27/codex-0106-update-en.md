# Codex 0.106.0 Update: Your Agent Can Finally Ask Questions

> **TL;DR**: Codex 0.106.0 brings major updates: **"Ask Question" tool** lets the agent pause and ask you questions during coding (unlocking custom Plan Modes and brainstorming); **Agent Memory overhaul** (diff-based forgetting + usage-aware prioritization); **JavaScript REPL** for interactive debugging; **WebSocket v2 fixes**. The key shift: your agent is no longer heads-down guessing — it can stop and ask.

---

## 🎯 The Big One: Ask Question Tool

**Before:** Codex in default coding mode could only work silently. Unclear requirements? Guess. Multiple tech options? Pick one. Vague acceptance criteria? Write something and hope.

**Now:** The agent can **pause mid-task and ask you questions**.

This unlocks three previously impossible workflows:

### 1. Custom Plan Mode
Agent asks you when it hits ambiguity during planning instead of making assumptions.

### 2. Interactive Skills
Skills that need user input can pause and wait instead of guessing.

### 3. "Interview Me" Brainstorming
Tell the agent: "Help me define requirements for this project — ask me questions." It acts like a product manager, systematically turning vague ideas into clear specs.

### How to Enable

Off by default. Add to your config:

```toml
default_mode_request_user_input = true
```

## 🧠 Agent Memory Overhaul (v0.105 + v0.106)

### Diff-Based Forgetting
- Old: memory only grew, getting bloated over time
- New: **diff-based forgetting** — stale thread memory is surgically pruned
- Not a blunt reset, but precise removal of no-longer-relevant information

### Usage-Aware Prioritization
- Memory selection now considers **actual usage frequency**
- High-signal, frequently-accessed memories get priority loading
- Low-activity memories are automatically deprioritized

**Real-world result:** Memory is working "very well now." Agents remember what matters and forget what doesn't.

## 🖥️ JavaScript REPL (Experimental)

Available under `/experimental` menu: interactive JavaScript execution, website debugging, real-time code snippet testing. Agents can now run JS during debugging to verify results instead of guessing output.

## 🔌 WebSocket v2 Fixed

```toml
responses_websockets_v2 = true
```

WebSocket prewarm and request routing now fully functional. No more error/mismatch behavior.

## 🐧 Known Issues

- Linux voice transcription still unavailable
- Windows voice transcription unconfirmed

## 💭 Why This Matters

"Ask Question" seems like a small feature, but it is a paradigm shift.

Previous AI coding assistants were **one-directional**: you give instructions, they execute, and guess when uncertain. Now Codex becomes **bidirectional**: it pauses at critical decision points to ask you.

**Knowing when to ask questions is a sign of intelligence.**

Combined with the overhauled Memory system, Codex is evolving from a "one-shot code generator" into a "long-term coding partner with memory and communication skills."

---

*Author: 🦞 Bigger Lobster*
*Date: 2026-02-27*
*Source: @LLMJunky*
*Tags: Codex / OpenAI / Agent Memory / Ask Question / JavaScript REPL / WebSocket*
