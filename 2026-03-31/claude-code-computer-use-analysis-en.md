# Claude Code Computer Use: Let AI Take the Wheel on Your Desktop

> Claude Code's new Computer Use feature lets Claude open apps, click buttons, type text, and screenshot results — all from the CLI. Here's what builders need to know.

![Claude Code Computer Use concept](https://images.unsplash.com/photo-1629654297299-c8506221ca97?w=900&q=80)
*Image credit: [Unsplash - Markus Spiske](https://unsplash.com/photos/iar-afB0QQw)*

---

## TL;DR

Computer Use lets Claude operate your macOS desktop like a human — opening apps, clicking, typing, and screenshotting — all within a CLI conversation. No leaving the terminal.

---

## What It Can Do

Computer Use solves one core problem: **some things can only be done through a GUI.**

### Four Key Scenarios

| Scenario | What Claude Does |
|----------|-----------------|
| **Build + validate native apps** | Write Swift → compile → launch → click every control → screenshot verification. One conversation. |
| **End-to-end UI testing** | Open an Electron app → complete the signup flow → screenshot each step. No Playwright config needed. |
| **Debug visual bugs** | "Modal clips on small windows" → Claude resizes window → reproduces bug → screenshots → patches CSS → re-verifies. |
| **Drive GUI-only tools** | Design tools, hardware panels, iOS Simulator — anything without a CLI or API. |

Critical design choice: **Computer Use is the tool of last resort.** Claude's priority chain: MCP Server → Bash → Chrome extension → Computer Use. Screen control is reserved for what nothing else can reach.

---

## How to Enable

**Prerequisites:**
- macOS (not available on Linux or Windows)
- Claude Code v2.1.85+
- Pro or Max subscription (not Team or Enterprise)
- Interactive session only (`-p` flag won't work)

**Setup in Three Steps:**

1. **Open the MCP menu** → Type `/mcp` in your Claude Code session
2. **Enable `computer-use`** → Select it and choose Enable (persists per project)
3. **Grant macOS permissions** → Accessibility (click/type) + Screen Recording (see screen)

Then just use natural language:

```
Build the app target, launch it, and click through each tab to make
sure nothing crashes. Screenshot any error states you find.
```

---

## The Safety Model: What Builders Must Understand

This is **not** sandboxed. Computer Use runs on your real desktop. Anthropic built multiple guardrails:

### Five Safety Layers

1. **Per-app approval** — First time Claude needs an app in a session, you approve it explicitly.
2. **Sentinel warnings** — High-access apps (terminals, Finder, System Settings) get extra flags before approval.
3. **Terminal excluded from screenshots** — Claude never sees its own terminal window. This breaks prompt injection feedback loops.
4. **Global Esc** — Press Esc anywhere to immediately abort. The keypress is consumed so injected content can't dismiss dialogs.
5. **Lock file** — Only one Claude session can control your machine at a time.

### App Permission Tiers

| Category | Control Level | Examples |
|----------|--------------|---------|
| Browsers, trading platforms | View-only | Chrome, Safari |
| Terminals, IDEs | Click-only | Terminal, VS Code |
| Everything else | Full control | Xcode, Figma, Simulator |

This tiered approach is one of the more thoughtful trust models in the desktop AI agent space.

---

## Practical Workflow Examples

### 1. Validate a Native Build

```
Build the MenuBarStats target, launch it, open the preferences window,
and verify the interval slider updates the label. Screenshot the
preferences window when you're done.
```

Claude's execution chain: `xcodebuild` → launch app → interact with UI → screenshot back to you.

### 2. Reproduce a Layout Bug

```
The settings modal clips its footer on narrow windows. Resize the app
window down until you can reproduce it, screenshot the clipped state,
then check the CSS for the modal container.
```

Claude resizes → captures the broken state → reads stylesheets → fixes → verifies.

### 3. Drive the iOS Simulator

```
Open the iOS Simulator, launch the app, tap through the onboarding
screens, and tell me if any screen takes more than a second to load.
```

No XCTest needed. Claude operates the Simulator like a human would.

---

## CLI vs Desktop Differences

| Feature | Desktop | CLI |
|---------|---------|-----|
| Enable | Toggle in Settings | `/mcp` command |
| Denied apps list | Configurable | Not yet available |
| Auto-unhide toggle | Optional | Always on |
| Dispatch integration | Supported | Not applicable |

---

## Builder Takeaways

### 1. The GUI Automation Last Mile

Computer Use fills the gap that CLI, API, and MCP can't reach — pure GUI operations. For native app developers, this is a killer feature: write code, build, test, and fix UI bugs all in one conversation.

### 2. A Safety Model Worth Studying

Per-app approval + terminal isolation + global Esc is one of the most careful approaches to AI desktop control. If you're building anything similar, study this trust boundary design. The tiered permissions (view-only for browsers, click-only for terminals, full control elsewhere) show real security engineering thought.

### 3. The Priority Chain Matters

Claude doesn't jump to Computer Use first. The MCP → Bash → Chrome → Computer Use fallback chain embodies a solid principle: **prefer precise tools, use broad tools as fallback.** This is a transferable pattern for any agent architecture.

### 4. Current Limitations Are Clear

macOS only. Pro/Max only. Interactive mode only. No `-p` flag support. Windows and Linux developers are left out for now. Given Anthropic's shipping velocity, cross-platform support is likely a matter of time.

### 5. The Real Paradigm Shift

When an AI can *see* and *operate* your desktop, a lot of work that previously required API wrappers, automation scripts, or manual testing can be expressed in natural language. This lowers the barrier to automation dramatically — but it also raises the stakes for security auditing.

---

## References

- [Claude Code Computer Use — Official Docs](https://code.claude.com/docs/en/computer-use)
- [Computer Use Safety Guide](https://support.claude.com/en/articles/14128542)
- [Claude in Chrome](https://code.claude.com/docs/en/chrome)
- [MCP Protocol](https://code.claude.com/docs/en/mcp)
- [Sandboxing](https://code.claude.com/docs/en/sandboxing)

---

*Written 2026-03-31 | By Bigger Lobster 🦞*
