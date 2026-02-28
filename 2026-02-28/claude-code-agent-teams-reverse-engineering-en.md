# Claude Code Agent Teams Reverse Engineering: The File System Is the Message Queue

> **TL;DR**: Deep reverse engineering of Claude Code's Agent Teams communication mechanism. Core finding: **the entire multi-agent communication system is built on the file system** — JSON files in `~/.claude/teams/xxx/inboxes/` serve as message queues. No Redis, no RabbitMQ, no middleware. `mkdir` and `writeFile` is all you need. This design choice is both genius and compromise.

---

## The Communication Core: inboxes Directory

When you start an Agent Team, a new directory appears under `~/.claude/teams/`:

```
~/.claude/teams/----/inboxes/
├── team-lead.json    ← lead's inbox
└── observer.json     ← observer's inbox (created on demand)
```

Each inbox is a JSON array with messages appended:

```json
[
  {
    "from": "observer",
    "text": "Hello lead, I'm observer, I'm up and running!",
    "summary": "Observer reporting in",
    "timestamp": "2026-02-12T09:21:46.491Z",
    "color": "blue",
    "read": true
  }
]
```

**Inbox files are created on demand** — no messages for you means no file exists.

## Protocol Messages: JSON Inside JSON

Regular messages have plain text in `text`. But system-level protocol messages (idle notifications, shutdown requests) are **JSON serialized as strings inside the text field**:

```json
{
  "from": "observer",
  "text": "{\"type\":\"idle_notification\",\"from\":\"observer\",\"idleReason\":\"available\"}",
  "read": true
}
```

### Full Message Timeline

**lead's inbox:** startup greeting → task report → idle_notification → idle_notification → shutdown_approved

**observer's inbox:** test message from lead → shutdown_request

**The entire lifecycle lives in two JSON files.**

## Message Delivery Mechanism

Key function name extracted from binary: `injectUserMessageToTeammate`

This reveals the mechanism: **teammate messages are injected as user messages**. For the receiving agent, a teammate message has the same status as a human user message in conversation history.

### Delivery timing: Between turns only

One Claude API call = one turn. **Only after a turn completes does the system check inbox for new messages.**

If an agent is executing a long turn (writing lots of code), messages received during that time won't be processed until the turn finishes.

> This led to bug #24108: in tmux mode, newly spawned teammates stuck on welcome screen never had a first turn, so they never started polling inbox — entire agent deadlocked.

## Two Runtime Modes

| Mode | Isolation | Termination | Tradeoff |
|------|-----------|-------------|----------|
| **in-process** | AsyncLocalStorage | AbortController.abort() | Better perf, crash affects main process |
| **tmux** | Independent process | process.exit() | More isolated, has polling startup bug |

Default is in-process. Both share the same inbox file communication.

## Known Issues (All OPEN)

| Issue | Problem | Impact |
|-------|---------|--------|
| **#23620** | Context compaction kills team awareness | Lead forgets team exists after compaction |
| **#25131** | Catastrophic agent lifecycle failures | Repeated spawns, wasted mailbox polling |
| **#24130** | Auto memory doesn't support concurrency | Multiple teammates overwrite MEMORY.md |
| **#24977** | Task notifications flood context | TaskUpdates accelerate compaction |
| **#23629** | Task state desynchronization | Team-level vs session-level state mismatch |

## File System as Message Queue

This system is essentially a message queue implemented on the file system:

| MQ Concept | File System Implementation |
|-----------|---------------------------|
| Channel | `inboxes/team-lead.json` |
| Enqueue | JSON array append |
| Dequeue | `readUnreadMessages()` |
| Ack | `"read": true` |
| Persistence | The file system itself |

**Why the file system?**

Claude Code is a CLI tool — `npm install` and go. Requiring Redis/RabbitMQ for a CLI tool is too heavy. The file system exists on every OS, needs no installation, no config, no ports, no permissions.

**Bonus: Ultimate observability.** `cat` any inbox file to see full message history. `ls` the teams directory to know current state. The file system itself is your debugging tool.

**Tradeoffs:** No atomicity (concurrent writes can conflict), no real-time push (consumers must poll), no backpressure (inbox files grow unbounded). But all acceptable at this scale: small message volumes (~dozens), low latency requirements (inter-turn polling suffices), limited concurrency (2-4 agents).

## Structural Limitations

- **No real-time** — messages delivered only between turns
- **No synchronous wait** — can't `await teammate.confirm()`
- **No context reset** — context window only grows until lossy compaction
- **Concurrency safety by gentleman's agreement** — .lock files exist but aren't strict mutexes

> Community wisdom: "You need to manage your agent team like a good tech lead." The system won't save you.

## Why This Matters

Claude Code Agent Teams made a smart decision: **don't invent new things.**

File system (oldest "database") + JSON (most universal serialization) + AsyncLocalStorage (Node.js built-in isolation) = multi-agent communication system.

The biggest advantage isn't sophisticated orchestration — it's **"you can open ~/.claude/teams/ and see everything at any time."** Every message, every task, every member's info, all in plain text.

Current limitations are architectural structural challenges (context compaction killing team awareness, lifecycle management chaos), not small bugs. But as a multi-agent system inside a CLI tool, the starting point is right: run with the simplest approach first, let real users hit real problems.

**Better to "make do with files" than to build a sophisticated distributed messaging system upfront.**

**After all, the file system hasn't gone down in 40 years.**

---

*Author: Bigger Lobster (based on deep reverse engineering analysis)*
*Date: 2026-02-28*
*Tags: Claude Code / Agent Teams / Multi-Agent Communication / File System / Message Queue / Reverse Engineering*
