# 🎭 Agency Agents: 144 AI Specialist Personas in One Repo — Your Virtual Company, Ready to Deploy

> **Repo:** [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)
> **Stars:** 64k+ ⭐ | **Forks:** 9.7k | **License:** MIT
> **TL;DR:** Not another prompt template library. A full system of AI agent personalities with character, workflows, deliverables, and KPIs.

---

## What Is This?

Most AI prompt libraries give you "Act as a developer" with a paragraph of vague instructions. `agency-agents` is fundamentally different — each agent has a **complete personality**: a name, a voice, a domain expertise workflow, code examples, and measurable success metrics.

144 agents organized into **12 divisions**, mirroring a real agency structure:

| Division | Count | Example Agents |
|----------|-------|----------------|
| 💻 Engineering | 27 | Frontend Dev, Backend Architect, Security Engineer, Solidity |
| 🎨 Design | 8 | UI/UX, Brand Guardian, Whimsy Injector |
| 💰 Paid Media | 7 | PPC Strategy, Search Query Analysis, Ad Audit |
| 💼 Sales | 8 | Outbound Strategy, Discovery Coach, Deal Strategist |
| 📢 Marketing | 30+ | SEO, TikTok, Reddit, Xiaohongshu, Bilibili, Douyin |
| 📊 Product | 5 | Sprint Prioritizer, Trend Research, Behavioral Nudge |
| 🎬 PM | 6 | Studio Producer, Jira Workflow Steward |
| 🧪 Testing | 8 | API Testing, Performance Benchmarker, Accessibility Auditor |
| 🛟 Support | 6 | Customer Support, Finance, Compliance, Infra |
| 🥽 Spatial | 6 | XR Interface, visionOS, WebXR |
| 🎮 Game Dev | 16 | Unity / Unreal / Godot / Roblox / Blender |
| 📚 Academic | 5 | Anthropologist, Geographer, Psychologist |

**Notable:** The repo has significant China-market coverage — WeChat Mini Programs, Feishu integration, Xiaohongshu, Bilibili, Douyin, Kuaishou, Zhihu, Baidu SEO, and cross-border e-commerce agents. This is rare for an English-first open source project.

---

## Technical Architecture: What Does an Agent File Look Like?

Each agent is a Markdown file with YAML frontmatter:

```yaml
---
name: Frontend Developer
description: Expert frontend developer...
color: cyan
emoji: 🖥️
vibe: Builds responsive, accessible web apps...
---
```

The body follows a consistent structure:
1. **Identity & Memory** — Role definition + memory model
2. **Core Mission** — Specific responsibilities with code examples
3. **Critical Rules** — Domain-specific hard constraints
4. **Workflow Process** — Step-by-step operational procedures
5. **Success Metrics** — Quantifiable delivery standards

The key insight: these aren't just "system prompts." They're behavioral specifications that force LLMs into domain-specific thinking patterns.

---

## Multi-Tool Integration: The Killer Feature

The repo ships `convert.sh` + `install.sh` scripts that transform agent files into native formats for every major agentic coding tool:

```
Supported tools:
├── Claude Code     → ~/.claude/agents/ (native .md, no conversion)
├── GitHub Copilot  → ~/.github/agents/
├── Cursor          → .cursor/rules/*.mdc
├── Aider           → CONVENTIONS.md
├── Windsurf        → .windsurfrules
├── Gemini CLI      → ~/.gemini/extensions/
├── Antigravity     → ~/.gemini/antigravity/skills/
├── OpenCode        → .opencode/agents/
├── OpenClaw        → SOUL.md + AGENTS.md + IDENTITY.md
├── Qwen Code       → ~/.qwen/agents/
└── Kimi Code       → ~/.config/kimi/agents/
```

Installation:

```bash
# Generate integration files for all tools
./scripts/convert.sh

# Interactive install (auto-detects installed tools)
./scripts/install.sh

# Target a specific tool
./scripts/install.sh --tool cursor

# Parallel mode for speed
./scripts/convert.sh --parallel --jobs 8
```

The installer scans your system, presents a checkbox UI, and lets you pick exactly which tools to install for. No vendor lock-in.

---

## Real-World Use Cases

### Scenario 1: Startup MVP

**Team:** Frontend Developer + Backend Architect + Growth Hacker + Rapid Prototyper + Reality Checker

Each agent knows its boundaries. The frontend agent insists on Core Web Vitals. The backend agent defaults to API versioning. The growth hacker produces viral loop designs. You get specialized output instead of generic advice.

### Scenario 2: Paid Media Account Takeover

**Team:** Paid Media Auditor → Tracking Specialist → PPC Strategist → Search Query Analyst → Ad Creative Strategist

This mirrors exactly how a real ad agency handles new client onboarding: audit → tracking verification → structure optimization → creative refresh — all within 30 days.

### Scenario 3: Full Cross-Functional Discovery

The repo includes a complete [Nexus Spatial Discovery](https://github.com/msitarzewski/agency-agents/blob/main/examples/nexus-spatial-discovery.md) example where 8 division agents work in parallel to produce a unified product plan.

---

## Why This Matters

**1. Solves the "AI is too generic" problem**

General-purpose LLMs can discuss anything but go deep on nothing. These agent personas force domain-specific thinking, producing measurably better output.

**2. Composable agent teams**

Instead of one AI doing everything, you assemble specialists like LEGO. Security Engineer reviews code + Code Reviewer checks architecture + Technical Writer handles docs.

**3. Tool-agnostic**

Not locked to any IDE or AI platform. Whether you use Cursor, Claude Code, or Gemini CLI, the same agents work everywhere.

**4. Community-driven and battle-tested**

Started from a Reddit post, grew to 64k+ stars. New agent PRs come in daily. The Chinese contribution guide signals a truly international community.

---

## Practical Advice for Builders

1. **Don't install all 144 at once** — Start with 3–5 agents relevant to your current project
2. **Fork and customize** — Adapt agent personalities to your tech stack (swap React for your framework)
3. **Use the Orchestrator** — The Agents Orchestrator agent can coordinate multi-agent workflows
4. **Watch your context window** — Each agent's system prompt consumes tokens; load only what you need

---

## Links

- **GitHub:** <https://github.com/msitarzewski/agency-agents>
- **Contributing Guide:** <https://github.com/msitarzewski/agency-agents/blob/main/CONTRIBUTING.md>
- **Chinese Contributing Guide:** <https://github.com/msitarzewski/agency-agents/blob/main/CONTRIBUTING_zh-CN.md>

---

![Agency Agents repo screenshot](https://opengraph.githubassets.com/1/msitarzewski/agency-agents)
*Image source: GitHub OpenGraph — msitarzewski/agency-agents*

---

🦞
