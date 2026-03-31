# lark-cli: The Official Lark/Feishu CLI — 200+ Commands, 19 Agent Skills, Built for Humans and AI

> **Repo:** [github.com/larksuite/cli](https://github.com/larksuite/cli) | MIT License | Go + Node.js  
> **TL;DR:** Lark's official CLI tool designed for both humans and AI Agents. Covers 11 business domains (Calendar, Messenger, Docs, Sheets, Base, Mail, Tasks, Wiki, Contacts, Meetings, Drive) with 200+ commands and 19 structured Agent Skills.

---

## Why This Matters

The AI Agent tooling ecosystem is going through a critical shift in 2026: **tools must be designed for both humans and agents from the ground up**. Lark's `lark-cli` is a textbook example — it's not a thin API wrapper with an agent adapter bolted on. It's an **Agent-Native office automation CLI**.

What this means for builders:
- Your Claude Code / Codex / coding agent can **operate Lark directly** — send messages, create docs, manage calendar, query databases
- Zero glue code. `npm install` and go.
- 19 pre-built Skills for common workflows — agents work out of the box

![lark-cli GitHub repository](https://opengraph.githubassets.com/1/larksuite/cli)
*Image source: GitHub - larksuite/cli*

---

## Core Architecture: Three-Layer Command System

The most interesting design decision in `lark-cli` is its **three-layer command architecture**, letting you pick the right granularity:

### Layer 1: Shortcuts

Prefixed with `+`, friendly for both humans and AI, with smart defaults:

```bash
# View today's agenda
lark-cli calendar +agenda

# Send a message
lark-cli im +messages-send --chat-id "oc_xxx" --text "Hello"

# Create a document
lark-cli docs +create --title "Weekly Report" --markdown "# Progress\n- Completed feature X"
```

### Layer 2: API Commands

Auto-generated from Lark OAPI metadata, 100+ commands mapped 1:1 to platform endpoints:

```bash
lark-cli calendar calendars list
lark-cli calendar events instance_view --params '{"calendar_id":"primary"}'
```

### Layer 3: Raw API

Call any Lark Open Platform endpoint directly, covering 2500+ APIs:

```bash
lark-cli api GET /open-apis/calendar/v4/calendars
lark-cli api POST /open-apis/im/v1/messages --params '{"receive_id_type":"chat_id"}' \
  --body '{"receive_id":"oc_xxx","msg_type":"text","content":"{\"text\":\"Hello\"}"}'
```

**Why this design works:** Most CLIs offer a single abstraction layer. Three layers let beginners use shortcuts, power users use API commands, and agents dynamically pick the right granularity for the task.

---

## 19 Agent Skills: Plug-and-Play Lark Automation

This is `lark-cli`'s killer feature. Each Skill is a structured capability pack that agents can load directly:

| Skill | Capabilities |
|-------|-------------|
| `lark-calendar` | Events, agenda view, free/busy queries, time suggestions |
| `lark-im` | Send/reply messages, group management, search, file upload/download |
| `lark-doc` | Create/read/update/search documents (Markdown-based) |
| `lark-sheets` | Spreadsheet read/write, append, find, export |
| `lark-base` | Tables, fields, records, dashboards, data analytics |
| `lark-mail` | Send/receive email, search, forward, draft management |
| `lark-task` | Task management, subtasks, reminders, member assignment |
| `lark-event` | WebSocket real-time event subscriptions + regex routing |
| `lark-wiki` | Knowledge spaces, nodes, document management |
| `lark-skill-maker` | Custom Skill creation framework |

Notable: `lark-event` supports **WebSocket real-time event subscriptions with regex routing** — agents can listen for Lark events and respond automatically, no polling needed.

Two **workflow Skills** stand out:
- `lark-workflow-meeting-summary`: Auto-aggregate meeting minutes into structured reports
- `lark-workflow-standup-report`: Auto-summarize agenda and todos

---

## Security: Built In, Not Bolted On

For a tool designed to be called by AI agents, `lark-cli` gets security right:

1. **Input injection protection** — prevents prompt injection via command parameters
2. **Terminal output sanitization** — blocks malicious content from polluting agent context
3. **OS-native keychain storage** — credentials never stored as plaintext config files
4. **Dry-run preview** — preview side-effect commands before executing

```bash
# Preview what would happen before actually sending
lark-cli im +messages-send --chat-id oc_xxx --text "hello" --dry-run
```

5. **Identity switching** — distinguish between user and bot identities

```bash
lark-cli calendar +agenda --as user
lark-cli im +messages-send --as bot --chat-id "oc_xxx" --text "Hello"
```

---

## Quick Start (3 Minutes)

### Install

```bash
npm install -g @larksuite/cli
npx skills add larksuite/cli -y -g
```

### Configure (one-time)

```bash
lark-cli config init          # Interactive guided app credential setup
lark-cli auth login --recommend  # OAuth login with recommended scopes
```

### Use

```bash
lark-cli calendar +agenda
lark-cli im +messages-send --chat-id "oc_xxx" --text "Done!"
lark-cli docs +create --title "Weekly Report" --markdown "# This Week"
```

### AI Agent Integration

For agents (Claude Code, Codex, etc.) operating Lark:

```bash
# Step 1: Install
npm install -g @larksuite/cli
npx skills add larksuite/cli -y -g

# Step 2: Configure (runs in background, outputs auth URL for user)
lark-cli config init --new

# Step 3: Login (same pattern)
lark-cli auth login --recommend

# Step 4: Verify
lark-cli auth status
```

---

## Output Formats & Advanced Usage

```bash
--format json      # Full JSON (default)
--format pretty    # Human-readable
--format table     # Table view
--format ndjson    # Newline-delimited JSON (pipe-friendly)
--format csv       # CSV

--page-all         # Auto-paginate all pages
--page-limit 5     # Max 5 pages
```

**Schema introspection** — inspect any API's parameters, request body, response structure:

```bash
lark-cli schema calendar.events.instance_view
```

---

## How It Compares

| Dimension | lark-cli | Google Workspace CLI (gws) | Slack CLI |
|-----------|----------|---------------------------|-----------|
| Agent Skills | ✅ 19 pre-built | ❌ None | ❌ None |
| Three-layer commands | ✅ Shortcut + API + Raw | ❌ API only | ❌ API only |
| Dry-run | ✅ | ❌ | ❌ |
| Injection protection | ✅ | ❌ | ❌ |
| Open source | ✅ MIT | ✅ Apache 2.0 | Partial |

The key differentiator: `lark-cli` is **Agent-Native by design**, not agent-compatible as an afterthought.

---

## Builder Use Cases

1. **AI-powered office automation**: Let Claude Code send daily reports, create calendar events, search documents
2. **Team workflow automation**: Listen for Lark events → Agent processes → writes results back
3. **Data analysis pipelines**: Pull data from Lark Base → analyze → generate reports back to Docs
4. **DevOps integration**: CI/CD notifications, alerting, on-call reminders via Lark Messenger

---

## Risk Notes

The official docs explicitly warn: this tool carries inherent risks when invoked by AI agents (hallucination, unpredictable execution, prompt injection). Recommendations:
- Don't modify default security settings
- Don't add the integrated Lark bot to group chats
- Understand the scope of permissions you authorize

---

## Bottom Line

`lark-cli` represents a trend: **enterprise SaaS CLIs evolving from "human tools" to "agent tools"**. Its three-layer command architecture, 19 pre-built Skills, and security-by-default design are worth studying regardless of whether you use Lark.

If your team is on Lark/Feishu and exploring AI agent automation, this is probably the cleanest integration path available today.

🦞
